import sys
import unittest
from unittest.mock import patch, mock_open
from io import StringIO
from pathlib import Path

sys.path.append('../')
sys.path.append('../../tx-engine-package')
from pkeyformat_command import PkeyformatCommand




def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

class TestPkeyformatCommand(unittest.TestCase):

    def setUp(self):
        
        self.cmd = PkeyformatCommand(
            pkey= 'cRzuhSMWg8tE2tdLZrmvn8m56wqq6VYnBngwUjjCMT9aYYGSN8kj',
            input_file='alice.key',
            inform='toml',
            from_format='wif',
            to_format='int',
            network='testnet'
        )


    # ------------------------------------------------------------------------------------
    # test AddressCommand class creation
    def test_address_command_creation(self):
        
        self.assertEqual('cRzuhSMWg8tE2tdLZrmvn8m56wqq6VYnBngwUjjCMT9aYYGSN8kj', self.cmd.private_key)
        self.assertEqual('alice.key', self.cmd.input_file)
        self.assertEqual('toml', self.cmd.inform)
        self.assertEqual('wif', self.cmd.from_format)
        self.assertEqual('int', self.cmd.to_format)
        self.assertEqual('testnet', self.cmd.network)
        self.assertEqual('test', self.cmd.key_type)

    
    # ------------------------------------------------------------------------------------
    # Test wif to int 
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_wif_to_int(self, mock_exit, mock_stdout):
        expected_output = '59616176374971377858165786258601335398869230661003382236873763496247842879996'

        addr_cmd = PkeyformatCommand(
            pkey='cRzuhSMWg8tE2tdLZrmvn8m56wqq6VYnBngwUjjCMT9aYYGSN8kj', 
            input_file=None,
            inform='toml',
            from_format='wif', 
            to_format='int',
            network='testnet'
        )

        # Assert initial state
        assert addr_cmd.key_type == 'test'

        # Run the command and handle SystemExit
        with self.assertRaises(SystemExit) as cm:
            addr_cmd.run()

        # Capture  output
        output = mock_stdout.getvalue()
        
        # Assert the expected output is in the captured output
        self.assertIn(expected_output, output)
        
        # Assert exit(0) was called
        self.assertEqual(cm.exception.code, 0)



    # ------------------------------------------------------------------------------------
    # Test wif to hex
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_wif_to_hex(self, mock_exit, mock_stdout):
        expected_output = '83cd8f60e7b49e13194fb2113e23236764325a3d3fac8fba9239854a1588b9fc'

        addr_cmd = PkeyformatCommand(
            pkey='cRzuhSMWg8tE2tdLZrmvn8m56wqq6VYnBngwUjjCMT9aYYGSN8kj', 
            input_file=None,
            inform='toml',
            from_format='wif', 
            to_format='hex',
            network='testnet'
        )
        # Run the command and handle SystemExit
        with self.assertRaises(SystemExit) as cm:
            addr_cmd.run()

        # Capture  output
        output = mock_stdout.getvalue()
        
        # Assert the expected output is in the captured output
        self.assertIn(expected_output, output)
        

    # ------------------------------------------------------------------------------------
    # Test int to hex
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_int_to_hex(self, mock_exit, mock_stdout):
        expected_output = '83cd8f60e7b49e13194fb2113e23236764325a3d3fac8fba9239854a1588b9fc'

        addr_cmd = PkeyformatCommand(
            pkey='59616176374971377858165786258601335398869230661003382236873763496247842879996', 
            input_file=None,
            inform='toml',
            from_format='int', 
            to_format='hex',
            network='testnet'
        )
        # Run the command and handle SystemExit
        with self.assertRaises(SystemExit) as cm:
            addr_cmd.run()

        # Capture  output
        output = mock_stdout.getvalue()
        
        # Assert the expected output is in the captured output
        self.assertIn(expected_output, output)


    # ------------------------------------------------------------------------------------
    # Test int to wif
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_int_to_wif(self, mock_exit, mock_stdout):
        expected_output = 'cRzuhSMWg8tE2tdLZrmvn8m56wqq6VYnBngwUjjCMT9aYYGSN8kj'

        addr_cmd = PkeyformatCommand(
            pkey='59616176374971377858165786258601335398869230661003382236873763496247842879996', 
            input_file=None,
            inform='toml',
            from_format='int', 
            to_format='wif',
            network='testnet'
        )
        # Run the command and handle SystemExit
        with self.assertRaises(SystemExit) as cm:
            addr_cmd.run()

        # Capture  output
        output = mock_stdout.getvalue()
        
        # Assert the expected output is in the captured output
        self.assertIn(expected_output, output)


    # ------------------------------------------------------------------------------------
    # Test hex to wif
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_hex_to_wif(self, mock_exit, mock_stdout):
        expected_output = 'cRzuhSMWg8tE2tdLZrmvn8m56wqq6VYnBngwUjjCMT9aYYGSN8kj'

        addr_cmd = PkeyformatCommand(
            pkey='83cd8f60e7b49e13194fb2113e23236764325a3d3fac8fba9239854a1588b9fc', 
            input_file=None,
            inform='toml',
            from_format='hex', 
            to_format='wif',
            network='testnet'
        )
        # Run the command and handle SystemExit
        with self.assertRaises(SystemExit) as cm:
            addr_cmd.run()

        # Capture  output
        output = mock_stdout.getvalue()
        
        # Assert the expected output is in the captured output
        self.assertIn(expected_output, output)


    # ------------------------------------------------------------------------------------
    # Test hex to wif
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_hex_to_int(self, mock_exit, mock_stdout):
        expected_output = '59616176374971377858165786258601335398869230661003382236873763496247842879996'

        addr_cmd = PkeyformatCommand(
            pkey='83cd8f60e7b49e13194fb2113e23236764325a3d3fac8fba9239854a1588b9fc', 
            input_file=None,
            inform='toml',
            from_format='hex', 
            to_format='int',
            network='testnet'
        )
        # Run the command and handle SystemExit
        with self.assertRaises(SystemExit) as cm:
            addr_cmd.run()

        # Capture  output
        output = mock_stdout.getvalue()
        
        # Assert the expected output is in the captured output
        self.assertIn(expected_output, output)



    # ------------------------------------------------------------------------------------
    # test loading key from toml file
    @patch('sys.exit')
    @patch('builtins.open', new_callable=mock_open, read_data='[key_info]\nprivate_key = "cRzuhSMWg8tE2tdLZrmvn8m56wqq6VYnBngwUjjCMT9aYYGSN8kj"\nbitcoin_address = "mz2LZPGGhvwo1RvdFJorixMHa1qWk4ZMqZ"\n')
    @patch('pathlib.PosixPath.is_file', return_value=True)
    @patch('sys.stdout', new_callable=StringIO)
    def test_toml_to_int(self, mock_stdout, mock_is_file, mock_open_file, mock_exit):
        
        expected_output = '59616176374971377858165786258601335398869230661003382236873763496247842879996'

        addr_cmd = PkeyformatCommand(
            pkey=None, 
            input_file='/app/data/input_file.txt',
            inform='toml',
            from_format='wif', 
            to_format='int',
            network='testnet'
        )

        assert addr_cmd.key_type == 'test'
        assert addr_cmd.private_key == None

         # Run the command and handle SystemExit
        with self.assertRaises(SystemExit) as cm:
            addr_cmd.run()

        output = mock_stdout.getvalue()

        self.assertIn(expected_output, output)


    # ------------------------------------------------------------------------------------
    # test loading key from pem file
    @patch('sys.exit')
    @patch('builtins.open', new_callable=mock_open, read_data='-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQg9UgQ6ADRTosvl43bg5zp\nWU3cFFnuMA0MO5mQpw0yIKmhRANCAAS0+wZKso7C2qmxYsbEvK88us9aop4JTDb9\nnjAqlYPw6ik7Iybiu1aYtVggdWSDfJrEVQcuNdcWGuKohHfU/F6X\n-----END PRIVATE KEY-----\n')     
    @patch('pathlib.PosixPath.is_file', return_value=True)
    @patch('sys.stdout', new_callable=StringIO)
    def test_pem_to_int(self, mock_stdout, mock_is_file, mock_open_file, mock_exit):
        
        expected_output = '110943977574299588079135027069764758606913326570652510108968462252246438125737'

        addr_cmd = PkeyformatCommand(
            pkey=None, 
            input_file='/app/data/input_file.txt',
            inform='pem',
            from_format='wif', 
            to_format='int',
            network='testnet'
        )

        assert addr_cmd.key_type == 'test'
        assert addr_cmd.private_key == None

         # Run the command and handle SystemExit
        with self.assertRaises(SystemExit) as cm:
            addr_cmd.run()

        output = mock_stdout.getvalue()

        self.assertIn(expected_output, output)


    # ------------------------------------------------------------------------------------
    # test loading key from pem file to mainnet key in wif format
    @patch('sys.exit')
    @patch('builtins.open', new_callable=mock_open, read_data='-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQg9UgQ6ADRTosvl43bg5zp\nWU3cFFnuMA0MO5mQpw0yIKmhRANCAAS0+wZKso7C2qmxYsbEvK88us9aop4JTDb9\nnjAqlYPw6ik7Iybiu1aYtVggdWSDfJrEVQcuNdcWGuKohHfU/F6X\n-----END PRIVATE KEY-----\n')     
    @patch('pathlib.PosixPath.is_file', return_value=True)
    @patch('sys.stdout', new_callable=StringIO)
    def test_pem_to_int(self, mock_stdout, mock_is_file, mock_open_file, mock_exit):
        
        expected_output = 'L5SWJi6972T55DTftAGbTggWRZtCRr3GtShADUqhPnbWDZAciATX'

        addr_cmd = PkeyformatCommand(
            pkey=None, 
            input_file='/app/data/input_file.txt',
            inform='pem',
            from_format='wif', 
            to_format='wif',
            network='mainnet'
        )

        assert addr_cmd.key_type == 'main'
        assert addr_cmd.private_key == None

         # Run the command and handle SystemExit
        with self.assertRaises(SystemExit) as cm:
            addr_cmd.run()

        output = mock_stdout.getvalue()

        self.assertIn(expected_output, output)

    # ------------------------------------------------------------------------------------
    # test incorrect "from" format
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.exit')
    def test_int_to_hex_error(self, mock_exit, mock_stdout):
        expected_output = 'Failed to get address for private key: cRzuhSMWg8tE2tdLZrmvn8m56wqq6VYnBngwUjjCMT9aYYGSN8kj, check arguments and retry'

        addr_cmd = PkeyformatCommand(
            pkey='cRzuhSMWg8tE2tdLZrmvn8m56wqq6VYnBngwUjjCMT9aYYGSN8kj', 
            input_file=None,
            inform='toml',
            from_format='int', 
            to_format='hex',
            network='testnet'
        )
        # Run the command and handle SystemExit
        with self.assertRaises(SystemExit) as cm:
            addr_cmd.run()

        # Capture  output
        output = mock_stdout.getvalue()
        
        # Assert the expected output is in the captured output
        self.assertIn(expected_output, output)



