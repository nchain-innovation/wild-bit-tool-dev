import unittest
from unittest.mock import patch


def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


class TestArgumentHandler(unittest.TestCase):

    @patch('sys.argv', ['bbt.sh', 'key'])
    def test_key_command(self):
        # handler = ArgumentHandler()
        # self.assertTrue(hasattr(handler, 'key'))
        pass

    # @patch('sys.argv', ['bbt.sh', 'balance'])
    # def test_balance_command(self):
    #     handler = ArgumentHandler()
    #     self.assertTrue(hasattr(handler, 'balance'))

    # @patch('sys.argv', ['bbt.sh', 'address'])
    # def test_address_command(self):
    #     handler = ArgumentHandler()
    #     self.assertTrue(hasattr(handler, 'address'))

    # @patch('sys.argv', ['bbt.sh', 'transaction'])
    # def test_transaction_command(self):
    #     handler = ArgumentHandler()
    #     self.assertTrue(hasattr(handler, 'transaction'))

    # @patch('sys.argv', ['bbt.sh', 'pkeyformat'])
    # def test_pkeyformat_command(self):
    #     handler = ArgumentHandler()
    #     self.assertTrue(hasattr(handler, 'pkeyformat'))

    # @patch('sys.argv', ['bbt.sh', 'consolidate'])
    # def test_consolidate_command(self):
    #     handler = ArgumentHandler()
    #     self.assertTrue(hasattr(handler, 'consolidate'))

    # @patch('sys.argv', ['bbt.sh', 'unknown'])
    # def test_unknown_command(self):
    #     with self.assertRaises(SystemExit):
    #         ArgumentHandler()

# if __name__ == '__main__':
#     unittest.main()


# NEED  TO TEST IF EITHER PARAMFILE OR GENPARAM IS SPECIFIED
# test         # Custom validation for mutually exclusive arguments
        # if not args.paramfile and not args.genparam:
        #     parser.error("Either -paramfile or -genparam must be specified.")


# Next test - transaction parameters
    # # ------------------------------------------------------------------------------------
    # # Test warning of genparam with broadcast
    # # bbt transaction -genparam --broadcast false
    # @patch('sys.stdout', new_callable=StringIO)
    # def test_genparam_broadcast_warning(self, mock_stdout):

    #     expected_output = 'Warning: --broadcast has no effect when used with -genparam'

    #     # Initialize the TransactionCommand
    #     cmd = TransactionCommand(
    #         genparam=True,
    #         network='testnet',
    #         inform='toml',
    #         fee=300,
    #         broadcast='false'
    #     )

    #     # Call the method to generate parameters to file
    #     cmd.run()

    #     # Get the printed output
    #     output = mock_stdout.getvalue()

    #     # Check if the expected output is in the printed output
    #     self.assertIn(expected_output, output)
