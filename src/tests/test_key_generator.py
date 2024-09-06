import sys
import unittest
from unittest.mock import patch, mock_open, MagicMock
import tempfile
import toml
from io import StringIO
import os

sys.path.append('../')
sys.path.append('../../tx-engine-package')
from key_command import KeyCommand


def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

# Test the key generator
class TestKeyGenerator(unittest.TestCase):

    def setUp(self):
        self.kg = KeyCommand(seed="my_seed", nonce="123456")


    # test KeyGenerator class creation
    def test_key_generator_creation(self):
        mykg = KeyCommand(seed="my_seed", 
                            nonce="123456",
                            output_file="output_file.txt",
                            param_file="param_file.txt",
                            genparam=True,
                            outform="toml",
                            list_all=True,
                            network='testnet')
        
        self.assertEqual('my_seed', mykg.seed)
        self.assertEqual('123456', mykg.nonce)
        self.assertEqual('output_file.txt', mykg.output_file)
        self.assertEqual('param_file.txt', mykg.param_file)
        self.assertEqual(True, mykg.genparam)
        self.assertEqual('toml', mykg.outform)
        self.assertEqual(True, mykg.list_all)
        self.assertEqual('testnet', mykg.network)

        self.assertEqual('my_seed', self.kg.seed)
        self.assertEqual('123456', self.kg.nonce)


    # test creating parameters from the seed and nonce and writing to stdout in toml format
    def test_generate_parameter_toml_stdout(self):


        expected_output = '\n\n[key_input]\nseed = "my_seed"\nnonce = "123456"\n\n\n'

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.kg.generate_parameters()
            self.assertEqual(fake_out.getvalue(), expected_output)


    # test creating parameters from the seed and nonce and writing to file in toml format
    def test_generate_parameter_toml_file(self):

        expected_output = '[key_input]\nseed = "my_seed"\nnonce = "123456"\n'
        with patch('builtins.open', new_callable=mock_open()) as m:
            self.kg.output_file = "output_file.txt"
            self.kg.generate_parameters()
            m.assert_called_with('/app/data/output_file.txt', 'w')
            m().write.assert_called_with(expected_output)


    # test creating parameters from the seed and nonce and writting to stdout as string representation of dictionary
    def test_generate_parameter_str_stdout(self):

        expected_output = "\n\n{'key_input': {'seed': 'my_seed', 'nonce': '123456'}}\n\n\n"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.kg.outform = "str"
            self.kg.generate_parameters()
            self.assertEqual(fake_out.getvalue(), expected_output)


    # test ERROR condition writing to file with other outform (not toml)
    def test_generate_parameter_str_file_error(self):
            
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.kg.outform = "str"
            self.kg.output_file = "output_file.txt"
            with self.assertRaises(SystemExit) as cm:
                self.kg.generate_parameters()
                self.assertEqual(cm.exception.code, 1)
       
        
    # test ERROR condition with no seed and nonce
    def test_generate_parameter_no_seed_nonce(self):
            
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.kg.seed = None
            self.kg.nonce = None
            with self.assertRaises(SystemExit) as cm:
                self.kg.generate_parameters()
                self.assertEqual(cm.exception.code, 1)     


    # test generate key from parameter file
    def test_generate_key_from_file(self):
        # Known parameters to write to the file
        known_params = '[key_input]\nseed = "my_seed"\nnonce = "123456"\n'

        known_private_key = 'cQ8GHAKR2SVEktDFwRYT715itDzTKMxoio22mSJi5Bmcx9RMm7pa'
        known_bitcoin_address = 'mpunbTFKMq2aNkqnyE55bHNPixFay2GVNS'
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(known_params.encode())
            temp_file_path = temp_file.name
        
        try:
            with patch('sys.stdout', new=StringIO()) as fake_out:
                # Call the function to test
                self.kg.param_file = temp_file_path
                self.kg.generate_key()

                 # Get the output from stdout
                generated_output = fake_out.getvalue()

                self.assertIn(known_private_key, generated_output)
                self.assertIn(known_bitcoin_address, generated_output)

        finally:
            # Clean up the temporary file
            os.remove(temp_file_path)

    # test generate key from parameter file - mainnet
    def test_generate_key_from_file_mainnet(self):
        # Known parameters to write to the file
        known_params = '[key_input]\nseed = "my_seed"\nnonce = "123456"\n'

        known_private_key = 'KymGpFKZbNnybSjzZ1jKjgafFzh3eus7eksZf1rCa57chQFbcFmz'
        known_bitcoin_address = '1APqJQALYobKbeNBFf6hmNA4rxet1f8JS7'
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(known_params.encode())
            temp_file_path = temp_file.name
        
        try:
            with patch('sys.stdout', new=StringIO()) as fake_out:
                # Call the function to test
                self.kg.param_file = temp_file_path
                self.kg.network = "mainnet"
                self.kg.generate_key()

                 # Get the output from stdout
                generated_output = fake_out.getvalue()

                self.assertIn(known_private_key, generated_output)
                self.assertIn(known_bitcoin_address, generated_output)

            # Debugging output
            # print(f"Generated output: {generated_output}")
        finally:
            # Clean up the temporary file
            os.remove(temp_file_path)



    # test list all keys
    # test-list-keys still to do.
    # list all (testnet)
    # list all (mainnet)
# run_tests(TestKeyGenerator)



# Ideas for things to test:
# ------------------------- 
# - argument parsing
# - key functions
# - transaction functions
# - config functions
# - file functions