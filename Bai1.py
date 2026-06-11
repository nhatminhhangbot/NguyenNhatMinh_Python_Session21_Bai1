import logging
import os

logging.basicConfig(
    filename='momo_transactions.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)


class InvalidAmountError(Exception):
    pass


class InsufficientBalanceError(Exception):
    pass


balance = 0


def deposit_money(money):
    global balance
    if money <= 0:
        logging.error(f'InvalidAmountError: Attempted to process {money} VND.')
        raise InvalidAmountError("Lỗi: Số tiền giao dịch phải lớn hơn 0.")

    balance += money
    logging.info(
        f'Deposit successful: +{money} VND. Current Balance: {balance}')
    return balance


def handle_deposit():
    print("\n--- NẠP TIỀN VÀO VÍ ---")
    while True:
        try:
            money = int(input("Nhập số tiền cần nạp: "))
            new_balance = deposit_money(money)
            print(f"Nạp tiền thành công: +{money:,} VND")
            print(f"Số dư hiện tại: {new_balance:,} VND")
            break
        except ValueError:
            print("Lỗi: Vui lòng nhập số tiền hợp lệ.")
            logging.error("ValueError: Invalid numeric input for deposit.")
        except InvalidAmountError as e:
            print(f"{e}")


def transfer_money(money, phone_number):
    global balance
    if money <= 0:
        logging.error(f"InvalidAmountError: Attempted to process {money} VND.")
        raise InvalidAmountError("Lỗi: Số tiền giao dịch phải lớn hơn 0.")

    if money > balance:
        logging.error(
            f"InsufficientBalanceError: Attempted to transfer {money} VND with balance {balance} VND.")
        raise InsufficientBalanceError(
            "Giao dịch thất bại: Số dư của bạn không đủ."
        )

    if money >= 10000000:
        logging.warning(
            f"High value transaction detected: {money} VND to {phone_number}")

    balance -= money
    logging.info(
        f'Transfer successful: -{money} VND to {phone_number}. Current Balance: {balance}')
    return balance


def handle_transfer():
    print("\n--- CHUYỂN TIỀN ---")
    while True:
        phone_number = input("Nhập số điện thoại người nhận: ").strip()
        if (len(phone_number) == 10 and phone_number.isdigit() and phone_number.startswith("0")):
            break
        print("Lỗi: Số điện thoại phải đúng định dạng 10 số.")

    while True:
        try:
            money = int(input("Nhập số tiền cần chuyển: "))
            new_balance = transfer_money(money, phone_number)
            print(
                f'\nChuyển tiền thành công tới số điện thoại {phone_number}.')
            print(f'Số tiền đã chuyển: {money:,} VND')
            print(f'Số dư còn lại: {new_balance:,} VND')
            break
        except ValueError:
            print("Lỗi: Vui lòng nhập số tiền hợp lệ.")
            logging.error("ValueError: Invalid numeric input for transfer.")
        except InvalidAmountError as e:
            print(f"{e}")
        except InsufficientBalanceError as e:
            print(f"\n{e}")
            print(f"Số dư hiện tại: {balance:,} VND")


def handle_view_logs():
    if not os.path.exists("momo_transactions.log") or os.path.getsize("momo_transactions.log") == 0:
        print('Chưa có lịch sử giao dịch nào trong hệ thống.')
        return

    print('\n--- 5 SỰ KIỆN GẦN NHẤT TRONG HỆ THỐNG ---')
    with open("momo_transactions.log", "r", encoding='utf-8') as f:
        lines = f.readlines()
        for index, line in enumerate(lines[-5:], 1):
            print(f"{index}. {line.strip()}")


def handle_show_balance():
    print("\n--- SỐ DƯ VÍ MOMO ---")
    print(f"Số dư hiện tại: {balance:,} VND")
    logging.info(f"Balance checked. Current Balance: {balance}")


def display_menu():
    print("\n========== VÍ MOMO GIẢ LẬP ==========")
    print("1. Nạp tiền vào ví")
    print("2. Chuyển tiền")
    print("3. Xem lịch sử hệ thống")
    print("4. Xem số dư tài khoản")
    print("5. Thoát chương trình")
    print("===============================================")


def main():
    while True:
        display_menu()
        choice = input("Chọn chức năng (1-5): ").strip()

        if choice == "1":
            handle_deposit()
        elif choice == "2":
            handle_transfer()
        elif choice == "3":
            handle_view_logs()
        elif choice == "4":
            handle_show_balance()
        elif choice == "5":
            print("Cảm ơn bạn đã sử dụng dịch vụ.")
            logging.info("System shutdown.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn từ 1 đến 5!")
            logging.warning("Invalid menu choice selected.")


if __name__ == "__main__":
    main()
