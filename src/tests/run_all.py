import test_key_generator as tkg
import test_bitcoin_balance as tbb
import test_address as ta
import test_pkeyformat as tpf
import test_transaction as tt

# run all tests
if __name__ == '__main__':
    tkg.run_tests(tkg.TestKeyGenerator)
    tbb.run_tests(tbb.TestBalanceCommand)
    ta.run_tests(ta.TestAddressCommand)
    tpf.run_tests(tpf.TestPkeyformatCommand)
    tt.run_tests(tt.TestTransactionCommand)
    print('End of test run.')
    print('Exiting.')
