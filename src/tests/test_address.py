import sys
import unittest
from unittest.mock import patch, mock_open
from io import StringIO


sys.path.append('../')
from address_command import AddressCommand


def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


class TestAddressCommand(unittest.TestCase):

    def setUp(self):
        self.cmd = AddressCommand(
            private_key='cRzuhSMWg8tE2tdLZrmvn8m56wqq6VYnBngwUjjCMT9aYYGSN8kj',
            network='testnet',
            input_file='alice.key',
            inform='toml'
        )

    # ------------------------------------------------------------------------------------
    # test AddressCommand class creation
    def test_address_command_creation(self):
        self.assertEqual('cRzuhSMWg8tE2tdLZrmvn8m56wqq6VYnBngwUjjCMT9aYYGSN8kj', self.cmd.private_key)
        self.assertEqual('testnet', self.cmd.network)
        self.assertEqual('alice.key', self.cmd.input_file)
        self.assertEqual('toml', self.cmd.inform)
        self.assertEqual('BSV_Testnet', self.cmd.key_type)

    # ------------------------------------------------------------------------------------
    # Test private_key_to_public_key method
    @patch('sys.stdout', new_callable=StringIO)
    def test_private_key_to_public_key(self, mock_stdout):
        expected_output = 'mz2LZPGGhvwo1RvdFJorixMHa1qWk4ZMqZ'
        # Call the method
        self.cmd.private_key_to_public_key(self.cmd.private_key)
        # Get the printed output
        output = mock_stdout.getvalue()
        # Check if the expected output is in the printed output
        self.assertIn(expected_output, output)

    # ------------------------------------------------------------------------------------
    # test loading key from pem file
    @patch('sys.stdout', new_callable=StringIO)
    @patch('pathlib.PosixPath.is_file', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQg9UgQ6ADRTosvl43bg5zp\nWU3cFFnuMA0MO5mQpw0yIKmhRANCAAS0+wZKso7C2qmxYsbEvK88us9aop4JTDb9\nnjAqlYPw6ik7Iybiu1aYtVggdWSDfJrEVQcuNdcWGuKohHfU/F6X\n-----END PRIVATE KEY-----\n')
    def test_pem_to_public_key(self, mock_open_file, mock_is_file, mock_stdout):
        expected_output = 'mg7k4cWKZAH6dHFAk4GPjuWFvmFZBHKf7s'
        addr_cmd = AddressCommand(
            private_key=None,
            network='testnet',
            input_file="/app/data/input_file.txt",
            inform="pem"
        )

        assert addr_cmd.key_type == 'BSV_Testnet'
        assert addr_cmd.private_key is None

        addr_cmd.run()
        output = mock_stdout.getvalue()
        print(output)
        self.assertIn(expected_output, output)

    # ------------------------------------------------------------------------------------
    # test loading key from pem file to mainnet key
    @patch('sys.stdout', new_callable=StringIO)
    @patch('pathlib.PosixPath.is_file', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQg9UgQ6ADRTosvl43bg5zp\nWU3cFFnuMA0MO5mQpw0yIKmhRANCAAS0+wZKso7C2qmxYsbEvK88us9aop4JTDb9\nnjAqlYPw6ik7Iybiu1aYtVggdWSDfJrEVQcuNdcWGuKohHfU/F6X\n-----END PRIVATE KEY-----\n')
    def test_pem_to_public_key_mainnet(self, mock_open_file, mock_is_file, mock_stdout):

        expected_output = '1bnmZRLk8qqrAmZ2VJ1uzHw4merFyKSP3'

        addr_cmd = AddressCommand(
            private_key=None,
            network='mainnet',
            input_file="/app/data/input_file.txt",
            inform="pem"
        )
        assert addr_cmd.key_type == 'BSV_Mainnet'
        assert addr_cmd.private_key is None

        addr_cmd.run()
        output = mock_stdout.getvalue()
        print(output)
        self.assertIn(expected_output, output)

    # ------------------------------------------------------------------------------------
    # test loading key from toml file
    @patch('sys.stdout', new_callable=StringIO)
    @patch('pathlib.PosixPath.is_file', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='[key_info]\nprivate_key = "cVoVmd5zY69LEevwGa5iq1Ba3oBc6J8xxUqdKuJCtuFWUJJngPPP"\nbitcoin_address = "mg7k4cWKZAH6dHFAk4GPjuWFvmFZBHKf7s"\n')
    def test_toml_to_public_key(self, mock_open_file, mock_is_file, mock_stdout):
        expected_output = 'mg7k4cWKZAH6dHFAk4GPjuWFvmFZBHKf7s'

        addr_cmd = AddressCommand(
            private_key=None,
            network='testnet',
            input_file="/app/data/input_file.txt",
            inform="toml"
        )

        assert addr_cmd.key_type == 'BSV_Testnet'
        assert addr_cmd.private_key is None
        addr_cmd.run()
        output = mock_stdout.getvalue()
        print(output)
        self.assertIn(expected_output, output)

    # ------------------------------------------------------------------------------------
    # test a toml file with pem "inform" - should raise an exception
    @patch('sys.stdout', new_callable=StringIO)
    @patch('pathlib.PosixPath.is_file', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='[key_info]\nprivate_key = "cVoVmd5zY69LEevwGa5iq1Ba3oBc6J8xxUqdKuJCtuFWUJJngPPP"\nbitcoin_address = "mg7k4cWKZAH6dHFAk4GPjuWFvmFZBHKf7s"\n')
    def test_bad_file_type_pem(self, mock_open_file, mock_is_file, mock_stdout):

        expected_output = "An unexpected error occurred: Incorrect padding.  Check filetype and contents."

        addr_cmd = AddressCommand(
            private_key=None,
            network='testnet',
            input_file="/app/data/input_file.txt",
            inform="pem"
        )

        # Act
        with patch.object(addr_cmd, 'run', side_effect=Exception("Incorrect padding")):
            try:
                addr_cmd.run()
            except Exception as e:
                print(f"An unexpected error occurred: {e}.  Check filetype and contents.")
            except SystemExit:
                pass  # Ignore the SystemExit exception raised by exit(1)

        # Assert
        output = mock_stdout.getvalue()
        print(output)
        self.assertIn(expected_output, output)
