import sys
import unittest
from unittest.mock import patch, mock_open
from io import StringIO
from pathlib import Path

sys.path.append('../')
from balance_command import BalanceCommand


def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


# Test the key generator
class TestBalanceCommand(unittest.TestCase):
    def setUp(self):
        self.bb = BalanceCommand(address="my_address",
                                 network="mock",
                                 input_file="input_file.txt",
                                 inform="toml",
                                 key_type="test")

    # test BalanceCommand class creation
    def test_bitcoin_balance_creation(self):
        bb = BalanceCommand(address="my_address",
                            network="testnet",
                            input_file="input_file.txt",
                            inform="toml")

        self.assertEqual('my_address', bb.address)
        self.assertEqual('testnet', bb.network)
        self.assertEqual('input_file.txt', bb.input_file)
        self.assertEqual('toml', bb.inform)

        bb = BalanceCommand()

        self.assertEqual(None, bb.address)
        self.assertEqual('testnet', bb.network)
        self.assertEqual(None, bb.input_file)
        self.assertEqual('toml', bb.inform)
        self.assertEqual('BSV_Testnet', bb.key_type)

    # test get_balance with no address parameter
    def test_get_balance_no_address(self):
        self.bb.address = None
        expected_output = "Error: No address provided.\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.bb.get_balance()
            self.assertEqual(fake_out.getvalue(), expected_output)

    # test loading key from toml file
    @patch('pathlib.PosixPath.is_file', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='[key_info]\nprivate_key = "cNae3oKZozV7aDVAb31PL6LtGB8R66zqEToiv36Q96urJfN5Lrr6"\nbitcoin_address = "msJjhsacnGxvzFMHBXoqdr63DhVRXdPQjS"\n')
    def test_load_key_from_file(self, mock_open_file, mock_is_file):
        self.bb.input_file = "/app/data/input_file.txt"
        assert self.bb.address == "my_address"
        self.bb.load_key_from_file()
        mock_is_file.assert_called_once_with()
        mock_open_file.assert_called_once_with(Path('/app/data/input_file.txt'), 'r')
        self.assertEqual(self.bb.address, "msJjhsacnGxvzFMHBXoqdr63DhVRXdPQjS")

    # test loading key from pem file
    @patch('pathlib.PosixPath.is_file', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQg9UgQ6ADRTosvl43bg5zp\nWU3cFFnuMA0MO5mQpw0yIKmhRANCAAS0+wZKso7C2qmxYsbEvK88us9aop4JTDb9\nnjAqlYPw6ik7Iybiu1aYtVggdWSDfJrEVQcuNdcWGuKohHfU/F6X\n-----END PRIVATE KEY-----\n')
    def test_load_from_pem(self, mock_open_file, mock_is_file):
        self.bb.inform = "pem"
        self.bb.input_file = "/app/data/input_file.txt"
        assert self.bb.address == "my_address"

        self.bb.load_key_from_file()
        mock_is_file.assert_called_once_with()
        mock_open_file.assert_called_once_with(Path('/app/data/input_file.txt'), 'r')

        assert self.bb.address == "mg7k4cWKZAH6dHFAk4GPjuWFvmFZBHKf7s"
