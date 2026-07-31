import sys
import unittest
from unittest.mock import patch

sys.path.append('../')
from useful import build_interface_config, add_interface_to_config


def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


class TestInterfaceConfig(unittest.TestCase):

    # ------------------------------------------------------------------------------------
    # testnet / mainnet -> WhatsOnChain (woc)
    def test_testnet_uses_woc(self):
        self.assertEqual(
            build_interface_config('testnet'),
            {'interface_type': 'woc', 'network_type': 'testnet'})

    def test_mainnet_uses_woc(self):
        self.assertEqual(
            build_interface_config('mainnet'),
            {'interface_type': 'woc', 'network_type': 'mainnet'})

    # ------------------------------------------------------------------------------------
    # mock -> in-memory interface
    def test_mock_uses_mock(self):
        self.assertEqual(
            build_interface_config('mock'),
            {'interface_type': 'mock', 'network_type': 'testnet'})

    # ------------------------------------------------------------------------------------
    # regtest -> local node over rpc, defaulting to the docker node
    def test_regtest_defaults(self):
        with patch.dict('os.environ', {}, clear=True):
            config = build_interface_config('regtest')
        self.assertEqual(config, {
            'interface_type': 'rpc',
            'network_type': 'testnet',
            'user': 'bitcoin',
            'password': 'bitcoin',
            'address': 'node1:18332',
        })

    # regtest connection details come from the environment when set
    def test_regtest_env_override(self):
        env = {'RPC_USER': 'alice', 'RPC_PASSWORD': 's3cret', 'RPC_HOST': '127.0.0.1:18332'}
        with patch.dict('os.environ', env, clear=True):
            config = build_interface_config('regtest')
        self.assertEqual(config['interface_type'], 'rpc')
        self.assertEqual(config['user'], 'alice')
        self.assertEqual(config['password'], 's3cret')
        self.assertEqual(config['address'], '127.0.0.1:18332')

    # ------------------------------------------------------------------------------------
    # an unknown network is a hard error
    def test_invalid_network_exits(self):
        with self.assertRaises(SystemExit):
            build_interface_config('bogusnet')

    # ------------------------------------------------------------------------------------
    # the persisted param file records routing only - never RPC credentials
    def test_add_interface_to_config_omits_secrets(self):
        data = {}
        with patch.dict('os.environ', {'RPC_PASSWORD': 'do-not-persist'}, clear=True):
            add_interface_to_config(data, 'regtest')
        self.assertEqual(data['interface'], {
            'interface_type': 'rpc',
            'network_type': 'testnet',
        })
        self.assertNotIn('user', data['interface'])
        self.assertNotIn('password', data['interface'])
        self.assertNotIn('address', data['interface'])


if __name__ == '__main__':
    run_tests(TestInterfaceConfig)
