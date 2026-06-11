import unittest
from Bai1 import Wallet, InvalidAmountError, InsufficientBalanceError


class TestWallet(unittest.TestCase):
    def setUp(self):
        self.wallet = Wallet()

    def test_deposit_success(self):
        self.wallet.deposit_money(500000)
        self.assertEqual(self.wallet.balance, 500000)

        self.wallet.deposit_money(10000)
        self.assertEqual(self.wallet.balance, 510000)

    def test_transfer_insufficient_balance(self):
        self.wallet.deposit_money(300000)
        with self.assertRaises(InsufficientBalanceError):
            self.wallet.transfer_money("0987654321", 500000)

    def test_invalid_amount(self):
        # Kiểm tra nạp tiền âm
        with self.assertRaises(InvalidAmountError):
            self.wallet.deposit_money(-100000)

        # Kiểm tra nạp tiền bằng 0
        with self.assertRaises(InvalidAmountError):
            self.wallet.deposit_money(0)

        # Kiểm tra chuyển tiền âm
        with self.assertRaises(InvalidAmountError):
            self.wallet.transfer_money("0987654321", -50000)


if __name__ == "__main__":
    unittest.main()
