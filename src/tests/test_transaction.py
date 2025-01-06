import sys
import unittest
from unittest.mock import patch, mock_open
from io import StringIO

sys.path.append('../')
from transaction_command import TransactionCommand


def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


class TestTransactionCommand(unittest.TestCase):

    def setUp(self):
        self.cmd = TransactionCommand(
            paramfile='/app/data/input_file.txt',
            genparam=True,
            out='/app/data/output_file.txt',
            broadcast='false',
            network='testnet',
            amount=1000,
            sender='sender_address',
            sender_key='sender_private_key',
            inform='toml',
            fee=500,
            recipient='recipient_address',
            change='change_address'
        )

    # ------------------------------------------------------------------------------------
    # test TransactionCommand class creation
    def test_transaction_command_creation(self):
        self.assertEqual('/app/data/input_file.txt', self.cmd.paramfile)
        self.assertEqual(True, self.cmd.genparam)
        self.assertEqual('/app/data/output_file.txt', self.cmd.out)
        self.assertEqual('false', self.cmd.broadcast)
        self.assertEqual('testnet', self.cmd.network)
        self.assertEqual(1000, self.cmd.amount)
        self.assertEqual('sender_address', self.cmd.sender)
        self.assertEqual('sender_private_key', self.cmd.sender_key)
        self.assertEqual('toml', self.cmd.inform)
        self.assertEqual(500, self.cmd.fee)
        self.assertEqual('recipient_address', self.cmd.recipient)
        self.assertEqual('change_address', self.cmd.change)
        self.assertEqual('BSV_Testnet', self.cmd.key_type)
        self.assertIsNotNone(self.cmd.interface)

    # ------------------------------------------------------------------------------------
    # Test generate_parameters_to_stdio method
    # default parameters
    # -------------------------------------------------------------------------------------
    @patch('sys.stdout', new_callable=StringIO)
    def test_generate_parameters_to_stdio(self, mock_stdout):

        # Expected output
        expected_output = """Generating parameters\n\n\n[interface]
interface_type = "woc"
network_type = "testnet"

[tx_info]
create_change_output = true
change_output_public_key = "<sender address>"
tx_default_fee = 300
"""

        # Initialize the TransactionCommand with default parameters
        cmd = TransactionCommand(
            genparam=True,
            network='testnet',
            broadcast='true',
            inform='toml',
            fee=300
        )

        # Call the method to generate parameters to stdio
        cmd.run()

        # Get the printed output
        output = mock_stdout.getvalue()

        # Check if the expected output is in the printed output
        self.assertIn(expected_output, output)

    # ------------------------------------------------------------------------------------
    # Test generate_parameters_to_file method
    # transaction -genparam -out test_tx_out.toml
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_generate_parameters_to_file(self, mock_stdout, mock_open):

        expected_output = 'Parameters generated, saved to file: /app/data/output_file.txt'
        # Parameters generated, saved to file: test_tx_out.toml

        # Initialize the TransactionCommand
        cmd = TransactionCommand(
            genparam=True,
            network='testnet',
            broadcast='true',
            inform='toml',
            fee=300,
            out='/app/data/output_file.txt',
        )

        # Call the method to generate parameters to file
        cmd.run()

        # Get the printed output
        output = mock_stdout.getvalue()

        # Check if the expected output is in the printed output
        self.assertIn(expected_output, output)

        # Check if the file is opened
        mock_open.assert_called_once_with('/app/data/output_file.txt', 'w')

        # Check if the file is written to
        mock_open().write.assert_called_once_with("""[interface]
interface_type = "woc"
network_type = "testnet"

[tx_info]
create_change_output = true
change_output_public_key = "<sender address>"
tx_default_fee = 300
""")

    # ------------------------------------------------------------------------------------
    # Test genparam with mainnet flag
    # bbt transaction -genparam --network mainnet
    #
    @patch('sys.stdout', new_callable=StringIO)
    def test_genparam_mainnet(self, mock_stdout):

        # Expected output
        expected_output = """
[interface]
interface_type = "woc"
network_type = "mainnet"

[tx_info]
create_change_output = true
change_output_public_key = "<sender address>"
tx_default_fee = 300
"""

        # Initialize the TransactionCommand
        cmd = TransactionCommand(
            genparam=True,
            network='mainnet',
            broadcast='true',
            inform='toml',
            fee=300
        )

        # Call the method to generate parameters to stdio
        cmd.run()

        # Get the printed output
        output = mock_stdout.getvalue()

        # Check if the expected output is in the printed output
        self.assertIn(expected_output, output)

    # ------------------------------------------------------------------------------------
    # Test genparam with amount flag and sender flag
    # bbt transaction -genparam --amount 1000 -sender mg7k4cWKZAH6dHFAk4GPjuWFvmFZBHKf7s
    @patch('sys.stdout', new_callable=StringIO)
    def test_genparam_amount_sender(self, mock_stdout):

        # Initialize the TransactionCommand
        cmd = TransactionCommand(
            genparam=True,
            network='mock',
            broadcast='true',
            inform='toml',
            fee=300,
            amount=1000,
            sender='mg7k4cWKZAH6dHFAk4GPjuWFvmFZBHKf7s'
        )

        cmd.interface.balance = {'confirmed': 3100, 'unconfirmed': 0}
        cmd.interface.utxo = {'mg7k4cWKZAH6dHFAk4GPjuWFvmFZBHKf7s': [
            {'height': 1631214, 'tx_pos': 0, 'tx_hash': 'ba37f74000558e145f1e1789c642fb69d2384b39211f4943c46de016f791451e', 'value': 1000},
            {'height': 1631214, 'tx_pos': 1, 'tx_hash': 'ba37f74000558e145f1e1789c642fb69d2384b39211f4943c46de016f791451e', 'value': 2100}
        ]}

        # Expected output
        expected_output = """Generating parameters\n\n\n[[transactioninput]]
tx_hash = "ba37f74000558e145f1e1789c642fb69d2384b39211f4943c46de016f791451e"
tx_pos = 0
amount = 1000
private_key_for_signing = "<key for signing>"

[[transactioninput]]
tx_hash = "ba37f74000558e145f1e1789c642fb69d2384b39211f4943c46de016f791451e"
tx_pos = 1
amount = 2100
private_key_for_signing = "<key for signing>"

[interface]
interface_type = "woc"
network_type = "mock"

[tx_info]
create_change_output = true
change_output_public_key = "mg7k4cWKZAH6dHFAk4GPjuWFvmFZBHKf7s"
tx_default_fee = 300
"""

        # Call the method to generate parameters to stdio
        cmd.run()
        # Get the printed output
        output = mock_stdout.getvalue()
        # # Check if the expected output is in the printed output
        self.assertIn(expected_output, output)

    # ------------------------------------------------------------------------------------
    # Test genparam with amount flag and sender_key flag
    # bbt transaction -genparam --amount 1000 -sender_key alice.key
    @patch('sys.stdout', new_callable=StringIO)
    @patch('useful.read_toml_file')
    def test_genparam_amount_senderkey(self, mock_read_file, mock_stdout):

        # Mock the return value of read_file
        mock_read_file.return_value = {
            'key_info': {
                'private_key': 'cVoVmd5zY69LEevwGa5iq1Ba3oBc6J8xxUqdKuJCtuFWUJJngPPP',
                'bitcoin_address': 'mg7k4cWKZAH6dHFAk4GPjuWFvmFZBHKf7s'
            }
        }

        # Initialize the TransactionCommand
        cmd = TransactionCommand(
            genparam=True,
            network='mock',
            broadcast='true',
            inform='toml',
            fee=300,
            amount=1000,
            sender_key='/app/data/alice.key'
        )

        cmd.interface.balance = {'confirmed': 3100, 'unconfirmed': 0}

        cmd.interface.utxo = {'mg7k4cWKZAH6dHFAk4GPjuWFvmFZBHKf7s': [
            {'height': 1631214, 'tx_pos': 0, 'tx_hash': 'ba37f74000558e145f1e1789c642fb69d2384b39211f4943c46de016f791451e', 'value': 1000},
            {'height': 1631214, 'tx_pos': 1, 'tx_hash': 'ba37f74000558e145f1e1789c642fb69d2384b39211f4943c46de016f791451e', 'value': 2100}
        ]}

        # Expected output
        expected_output = """Generating parameters\n\n\n[[transactioninput]]
tx_hash = "ba37f74000558e145f1e1789c642fb69d2384b39211f4943c46de016f791451e"
tx_pos = 0
amount = 1000
private_key_for_signing = "cVoVmd5zY69LEevwGa5iq1Ba3oBc6J8xxUqdKuJCtuFWUJJngPPP"

[[transactioninput]]
tx_hash = "ba37f74000558e145f1e1789c642fb69d2384b39211f4943c46de016f791451e"
tx_pos = 1
amount = 2100
private_key_for_signing = "cVoVmd5zY69LEevwGa5iq1Ba3oBc6J8xxUqdKuJCtuFWUJJngPPP"

[interface]
interface_type = "woc"
network_type = "mock"

[tx_info]
create_change_output = true
change_output_public_key = "<sender address>"
tx_default_fee = 300


"""
        # Call the method to generate parameters to stdio
        cmd.run()

        # Verify that read_file was called with the correct arguments
        mock_read_file.assert_called_once_with('/app/data/alice.key')

        # # Get the printed output
        output = mock_stdout.getvalue()

        # # # Check if the expected output is in the printed output
        self.assertIn(expected_output, output)

    # ------------------------------------------------------------------------------------
    # Test genparam with amount and sender_key in pem format
    # bbt transaction -genparam --amount 1000 -sender_key alice.key
    @patch('sys.stdout', new_callable=StringIO)
    @patch('useful.read_pem_file')
    def test_genparam_amount_senderkey_pem(self, mock_read_file, mock_stdout):
        # Mock the return value of read_file
        mock_read_file.return_value = '-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQg9UgQ6ADRTosvl43bg5zp\nWU3cFFnuMA0MO5mQpw0yIKmhRANCAAS0+wZKso7C2qmxYsbEvK88us9aop4JTDb9\nnjAqlYPw6ik7Iybiu1aYtVggdWSDfJrEVQcuNdcWGuKohHfU/F6X\n-----END PRIVATE KEY-----\n'
        # Initialize the TransactionCommand
        cmd = TransactionCommand(
            genparam=True,
            network='mock',
            broadcast='true',
            inform='pem',
            fee=300,
            amount=1000,
            sender_key='/app/data/alice.key'
        )
        cmd.interface.balance = {'confirmed': 3100, 'unconfirmed': 0}
        cmd.interface.utxo = {'mg7k4cWKZAH6dHFAk4GPjuWFvmFZBHKf7s': [
            {'height': 1631214, 'tx_pos': 0, 'tx_hash': 'ba37f74000558e145f1e1789c642fb69d2384b39211f4943c46de016f791451e', 'value': 1000},
            {'height': 1631214, 'tx_pos': 1, 'tx_hash': 'ba37f74000558e145f1e1789c642fb69d2384b39211f4943c46de016f791451e', 'value': 2100}
        ]}
        # Expected output
        expected_output = """[[transactioninput]]
tx_hash = "ba37f74000558e145f1e1789c642fb69d2384b39211f4943c46de016f791451e"
tx_pos = 0
amount = 1000
private_key_for_signing = "cVoVmd5zY69LEevwGa5iq1Ba3oBc6J8xxUqdKuJCtuFWUJJngPPP"

[[transactioninput]]
tx_hash = "ba37f74000558e145f1e1789c642fb69d2384b39211f4943c46de016f791451e"
tx_pos = 1
amount = 2100
private_key_for_signing = "cVoVmd5zY69LEevwGa5iq1Ba3oBc6J8xxUqdKuJCtuFWUJJngPPP"

[interface]
interface_type = "woc"
network_type = "mock"

[tx_info]
create_change_output = true
change_output_public_key = "<sender address>"
tx_default_fee = 300
"""
        # Call the method to generate parameters to stdio
        cmd.run()
        # Verify that read_file was called with the correct arguments
        mock_read_file.assert_called_once_with('/app/data/alice.key')
        # # Get the printed output
        output = mock_stdout.getvalue()
        # # # Check if the expected output is in the printed output
        self.assertIn(expected_output, output)

    # ------------------------------------------------------------------------------------
    # Test genparam with fee, recipient, change
    # bbt transaction -genparam --amount 1000 -sender_key alice.pem -inform pem -fee 500 -recipient mg7k4cWKZAH6dHFAk4GPjuWFvmFZBHKf7s -change mg7k4cWKZAH6dHFAk4GPjuWFvmFZBHKf7s
    @patch('sys.stdout', new_callable=StringIO)
    @patch('useful.read_pem_file')
    def test_genparam_fee_recipient_change(self, mock_read_file, mock_stdout):
        # Mock the return value of read_file
        mock_read_file.return_value = '-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQg9UgQ6ADRTosvl43bg5zp\nWU3cFFnuMA0MO5mQpw0yIKmhRANCAAS0+wZKso7C2qmxYsbEvK88us9aop4JTDb9\nnjAqlYPw6ik7Iybiu1aYtVggdWSDfJrEVQcuNdcWGuKohHfU/F6X\n-----END PRIVATE KEY-----\n'
        # Initialize the TransactionCommand
        cmd = TransactionCommand(
            genparam=True,
            network='mock',
            broadcast='true',
            inform='pem',
            fee=500,
            amount=1000,
            sender_key='/app/data/alice.key',
            recipient='mjK9HXAwspAu3YdmqZZ9JGDfbvfsorierQ',
            change='mg7k4cWKZAH6dHFAk4GPjuWFvmFZBHKf7s'
        )
        cmd.interface.balance = {'confirmed': 3100, 'unconfirmed': 0}
        cmd.interface.utxo = {'mg7k4cWKZAH6dHFAk4GPjuWFvmFZBHKf7s': [
            {'height': 1631214, 'tx_pos': 0, 'tx_hash': 'ba37f74000558e145f1e1789c642fb69d2384b39211f4943c46de016f791451e', 'value': 1000},
            {'height': 1631214, 'tx_pos': 1, 'tx_hash': 'ba37f74000558e145f1e1789c642fb69d2384b39211f4943c46de016f791451e', 'value': 2100}
        ]}
        # Expected output
        expected_output = """[[transactioninput]]
tx_hash = "ba37f74000558e145f1e1789c642fb69d2384b39211f4943c46de016f791451e"
tx_pos = 0
amount = 1000
private_key_for_signing = "cVoVmd5zY69LEevwGa5iq1Ba3oBc6J8xxUqdKuJCtuFWUJJngPPP"

[[transactioninput]]
tx_hash = "ba37f74000558e145f1e1789c642fb69d2384b39211f4943c46de016f791451e"
tx_pos = 1
amount = 2100
private_key_for_signing = "cVoVmd5zY69LEevwGa5iq1Ba3oBc6J8xxUqdKuJCtuFWUJJngPPP"

[[transactionoutput]]
public_key = "mjK9HXAwspAu3YdmqZZ9JGDfbvfsorierQ"
amount = 1000
op_return = false
data_to_encode = ""

[interface]
interface_type = "woc"
network_type = "mock"

[tx_info]
create_change_output = true
change_output_public_key = "mg7k4cWKZAH6dHFAk4GPjuWFvmFZBHKf7s"
tx_default_fee = 500
"""
        # Call the method to generate parameters to stdio
        cmd.run()
        # Verify that read_file was called with the correct arguments
        mock_read_file.assert_called_once_with('/app/data/alice.key')
        output = mock_stdout.getvalue()
        # # # Check if the expected output is in the printed output
        self.assertIn(expected_output, output)

    # ------------------------------------------------------------------------------------
    # Test genparam output to file
    # bbt transaction -genparam --amount 10 -out output_file.toml
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_genparam_output_to_file(self, mock_stdout, mock_open):
        expected_output = 'Parameters generated, saved to file: /app/data/output_file.toml'
        # Initialize the TransactionCommand
        cmd = TransactionCommand(
            genparam=True,
            network='mock',
            broadcast='true',
            inform='toml',
            fee=300,
            amount=10,
            out='/app/data/output_file.toml',
        )
        # Call the method to generate parameters to file
        cmd.run()
        # Get the printed output
        output = mock_stdout.getvalue()
        # Check if the expected output is in the printed output
        self.assertIn(expected_output, output)
        # Check if the file is opened
        mock_open.assert_called_once_with('/app/data/output_file.toml', 'w')
        # Check if the file is written to
        mock_open().write.assert_called_once_with("""[interface]
interface_type = "woc"
network_type = "mock"

[tx_info]
create_change_output = true
change_output_public_key = "<sender address>"
tx_default_fee = 300
""")

    # ------------------------------------------------------------------------------------
    # Test paramfile flag
    # bbt transaction -paramfile input_file.toml
    @patch('transaction.read_toml_file')
    @patch('sys.stdout', new_callable=StringIO)
    def test_paramfile(self, mock_stdout, mock_read_file):

        mock_read_file.return_value = {
            "transactioninput": [
                {
                    "input_tx_hash": "01000000015e0e47ce9c004147ca26a528edc09a2fd352e33bcb80b986685814580dba9840010000006b483045022100db2932276998523885af95f936f42c3465f15ec3449cf552b2e9f72a20a7cfa202200f530c5e6e4bd4bb1cee4f6faead4d33a5f7f3f37a9224889e93206517f609ce412103b4fb064ab28ec2daa9b162c6c4bcaf3cbacf5aa29e094c36fd9e302a9583f0eaffffffff02e8030000000000001976a9140694591e4bf16f2b2b64989192778e772d21f5d788ac34080000000000001976a9140694591e4bf16f2b2b64989192778e772d21f5d788ac00000000",
                    "tx_hash": "ba37f74000558e145f1e1789c642fb69d2384b39211f4943c46de016f791451e",
                    "tx_pos": 0,
                    "amount": 1000,
                    "private_key_for_signing": "cVoVmd5zY69LEevwGa5iq1Ba3oBc6J8xxUqdKuJCtuFWUJJngPPP"
                }
            ],
            "transactionoutput": [
                {
                    "public_key": "mjK9HXAwspAu3YdmqZZ9JGDfbvfsorierQ",
                    "amount": 99,
                    "op_return": False,
                    "data_to_encode": ""
                }
            ],
            "interface": {
                "interface_type": "mock",
                "network_type": "testnet"
            },
            "tx_info": {
                "create_change_output": True,
                "change_output_public_key": "mg7k4cWKZAH6dHFAk4GPjuWFvmFZBHKf7s",
                "tx_default_fee": 300
            }
        }

        expected_output = '''01000000011e4591f716e06dc443491f21394b38d269fb42c689171e5f148e550040f737ba000000006a473044022006130fa71cfc4ae86cb74ad28a31242cef2c4cd38fe69f3881dbf8bf3b9b309c02204e427a957bd2e2faab64fb386001fc47a1915bdb87161aa1f6587d1873df22cf412103b4fb064ab28ec2daa9b162c6c4bcaf3cbacf5aa29e094c36fd9e302a9583f0eaffffffff0263000000000000001976a91429a4afaebc18ee3d027504363f71a189fbff792088ac59020000000000001976a9140694591e4bf16f2b2b64989192778e772d21f5d788ac00000000'''
        expected_amounts = '''Amounts:
\tAmount In: 	1000
\tAmount Out: 	99
\tFee: 		300
\tChange: 	601'''

        # Initialize the TransactionCommand
        cmd = TransactionCommand(
            genparam=True,
            paramfile='/app/data/input_file.toml',
            network='mock',
            broadcast='false',
            inform='toml',
            fee=300,
        )

        cmd.run()

        # Get the printed output
        output = mock_stdout.getvalue()

        # Assert that 'input_file.toml' was read
        mock_read_file.assert_called_with('/app/data/input_file.toml')

        # Check if the expected output is in the printed output
        self.assertIn(expected_output, output)
        self.assertIn(expected_amounts, output)

    # ------------------------------------------------------------------------------------
    # Test paramfile flag with no inputs in the file
    # bbt transaction -paramfile input_file.toml
    @patch('transaction.read_toml_file')
    @patch('sys.stdout', new_callable=StringIO)
    def test_paramfile_no_inputs(self, mock_stdout, mock_read_file):
        # Mock the read_file function to return a dictionary without the required key
        mock_read_file.return_value = {
            'transactionoutput': [
                {
                    'public_key': 'mjK9HXAwspAu3YdmqZZ9JGDfbvfsorierQ',
                    'amount': 99,
                    'op_return': False,
                    'data_to_encode': ''
                }
            ],
            'interface': {
                'interface_type': 'woc',
                'network_type': 'testnet'
            },
            'tx_info': {
                'create_change_output': True,
                'change_output_public_key': '<sender address>',
                'tx_default_fee': 300
            }
        }

        expected_error_message = "Error: Missing key: 'transactioninput' in the parameter file:  '/app/data/input_file.toml'. Please check the file and try again."

        # Initialize the TransactionCommand
        cmd = TransactionCommand(
            genparam=True,
            paramfile='/app/data/input_file.toml',
            network='mock',
            broadcast='false',
            inform='toml',
            fee=300,
        )

        # Run the command and expect a KeyError
        with self.assertRaises(SystemExit) as context:
            cmd.run()

        # Check if the SystemExit code is 1
        self.assertEqual(context.exception.code, 1)

        # Get the printed output
        output = mock_stdout.getvalue()

        # Get the printed output
        output = mock_stdout.getvalue()

        # Assert that 'input_file.toml' was read
        mock_read_file.assert_called_with('/app/data/input_file.toml')

        # Check if the expected error message is in the printed output
        self.assertIn(expected_error_message, output)

    # ------------------------------------------------------------------------------------
    # Test paramfile flag with no inputs in the file
    # bbt transaction -paramfile input_file.toml
    @patch('transaction.read_toml_file')
    @patch('sys.stdout', new_callable=StringIO)
    def test_paramfile_no_outputs(self, mock_stdout, mock_read_file):
        # Mock the read_file function to return a dictionary without the required 'transactionoutput' key
        mock_read_file.return_value = {
            'interface': {
                'interface_type': 'woc',
                'network_type': 'testnet'
            },
            'tx_info': {
                'create_change_output': True,
                'change_output_public_key': '<sender address>',
                'tx_default_fee': 300
            }
        }

        expected_error_message = "Error: Missing key: 'transactionoutput' in the parameter file:  '/app/data/input_file.toml'. Please check the file and try again."

        # Initialize the TransactionCommand
        cmd = TransactionCommand(
            genparam=True,
            paramfile='/app/data/input_file.toml',
            network='mock',
            broadcast='false',
            inform='toml',
            fee=300,
        )

        # Run the command and expect a SystemExit
        with self.assertRaises(SystemExit) as context:
            cmd.run()

        # Check if the SystemExit code is 1
        self.assertEqual(context.exception.code, 1)

        # Get the printed output
        output = mock_stdout.getvalue()

        # Assert that 'input_file.toml' was read
        mock_read_file.assert_called_with('/app/data/input_file.toml')

        # Check if the expected error message is in the printed output
        self.assertIn(expected_error_message, output)

    # ------------------------------------------------------------------------------------
    # Test paramfile flag with change address provided in the file
    # bbt transaction -paramfile input_file.toml
    @patch('transaction.read_toml_file')
    @patch('sys.stdout', new_callable=StringIO)
    def test_paramfile_no_changeaddress(self, mock_stdout, mock_read_file):
        # Mock the read_file function to return the provided configuration
        mock_read_file.return_value = {
            'transactioninput': [
                {
                    'tx_hash': "ba37f74000558e145f1e1789c642fb69d2384b39211f4943c46de016f791451e",
                    'tx_pos': 0,
                    'amount': 1000,
                    'private_key_for_signing': "cVoVmd5zY69LEevwGa5iq1Ba3oBc6J8xxUqdKuJCtuFWUJJngPPP"
                }
            ],
            'transactionoutput': [
                {
                    'public_key': "mjK9HXAwspAu3YdmqZZ9JGDfbvfsorierQ",
                    'amount': 99,
                    'op_return': False,
                    'data_to_encode': ""
                }
            ],
            'interface': {
                'interface_type': 'woc',
                'network_type': 'testnet'
            },
            'tx_info': {
                'create_change_output': True,
                'change_output_public_key': "<sender address>",
                'tx_default_fee': 300
            }
        }

        expected_error_message = "Error: Invalid change_output_public_key: <sender address> is not a real address. Please check the parameter file: '/app/data/input_file.toml' and try again."

        # Initialize the TransactionCommand
        cmd = TransactionCommand(
            genparam=True,
            paramfile='/app/data/input_file.toml',
            network='mock',
            broadcast='false',
            inform='toml',
            fee=300,
        )

        # Run the command and expect a SystemExit
        with self.assertRaises(SystemExit) as context:
            cmd.run()

        # Check if the SystemExit code is 1
        self.assertEqual(context.exception.code, 1)

        # Get the printed output
        output = mock_stdout.getvalue()

        # Assert that 'input_file.toml' was read
        mock_read_file.assert_called_with('/app/data/input_file.toml')

        # Check if the expected error message is in the printed output
        self.assertIn(expected_error_message, output)
