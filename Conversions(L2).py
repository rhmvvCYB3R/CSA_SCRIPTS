def binary_to_gray(binary: str) -> str:
    binary = binary.strip()
    if not binary:
        return ""
    gray = binary[0]
    for i in range(1, len(binary)):
        gray += str(int(binary[i - 1]) ^ int(binary[i]))
    return gray


def base14_to_decimal(number: str) -> float:
    number = number.strip().upper()
    digits = '0123456789ABCD'
    if '.' in number:
        int_part, frac_part = number.split('.')
    else:
        int_part, frac_part = number, ''

    def digit_value(d):
        if d in digits:
            return digits.index(d)
        else:
            raise ValueError(f"Invalid base-14 digit: {d}")

    result = 0
    for i, d in enumerate(reversed(int_part)):
        result += digit_value(d) * (14 ** i)
    for i, d in enumerate(frac_part):
        result += digit_value(d) * (14 ** -(i + 1))
    return round(result, 3)


def binary_fraction_to_decimal(bin_frac: str) -> float:
    bin_frac = bin_frac.strip()
    if '.' not in bin_frac:
        raise ValueError("Input must contain '.' for fractional part")
    frac_part = bin_frac.split('.')[1]
    result = 0.0
    for i, bit in enumerate(frac_part):
        if bit not in '01':
            raise ValueError("Invalid binary digit in fractional part")
        result += int(bit) * (2 ** -(i + 1))
    return round(result, 4)


def binary_to_decimal(bin_str: str) -> float:
    bin_str = bin_str.strip()
    if '.' in bin_str:
        int_part, frac_part = bin_str.split('.')
    else:
        int_part, frac_part = bin_str, ''
    int_val = int(int_part, 2) if int_part else 0
    frac_val = binary_fraction_to_decimal("0." + frac_part) if frac_part else 0.0
    return int_val + frac_val


def hex_to_decimal_sign_magnitude(hex_str: str) -> int:
    hex_str = hex_str.strip()
    if not hex_str.startswith("#") or len(hex_str) != 4:
        raise ValueError("Input must be in format '#XYZ' (3 hex digits after #)")
    num = int(hex_str[1:], 16)
    sign = (num >> 11) & 1  # старший бит — знак
    magnitude = num & 0x7FF  # 11 бит — величина
    return -magnitude if sign == 1 else magnitude


def hex_to_decimal_U1(hex_str: str) -> int:
    hex_str = hex_str.strip()
    if not hex_str.startswith("#") or len(hex_str) != 4:
        raise ValueError("Input must be in format '#XYZ' (3 hex digits after #)")
    num = int(hex_str[1:], 16)
    sign = (num >> 11) & 1
    if sign == 0:
        return num
    max_val = (1 << 12) - 1  # 4095 (12 бит)
    inverted = max_val - num
    return -inverted


def hex_to_decimal_U2(hex_str: str) -> int:
    hex_str = hex_str.strip()
    if not hex_str.startswith("#") or len(hex_str) not in (3, 4):
        raise ValueError("Input must be in format '#XX' or '#XYZ' (2 or 3 hex digits after #)")
    num = int(hex_str[1:], 16)
    bits = (len(hex_str) - 1) * 4  # количество бит: 2 символа * 4 = 8 бит, 3 символа *4 = 12 бит
    if num & (1 << (bits - 1)):  # проверка старшего бита
        return num - (1 << bits)
    return num



def hex_to_decimal(hex_str: str) -> int:
    hex_str = hex_str.strip()
    if not hex_str.startswith("#"):
        raise ValueError("Input must start with '#'")
    return int(hex_str[1:], 16)


def sign_magnitude_to_decimal(bin_str: str) -> int:
    bin_str = bin_str.strip()
    if len(bin_str) < 2:
        raise ValueError("Input binary string too short")
    if any(c not in '01' for c in bin_str):
        raise ValueError("Input must be binary digits only")
    sign = int(bin_str[0])
    value = int(bin_str[1:], 2)
    return -value if sign == 1 else value


def U1_to_decimal(bin_str: str) -> int:
    bin_str = bin_str.strip()
    if len(bin_str) == 0:
        raise ValueError("Empty input")
    if any(c not in '01' for c in bin_str):
        raise ValueError("Input must be binary digits only")
    if bin_str[0] == '1':
        inverted = ''.join('1' if b == '0' else '0' for b in bin_str)
        return -int(inverted, 2)
    return int(bin_str, 2)


def U2_to_decimal(bin_str: str) -> int:
    bin_str = bin_str.strip()
    if any(c not in '01' for c in bin_str):
        raise ValueError("Input must be binary digits only")
    val = int(bin_str, 2)
    if bin_str[0] == '1':
        val -= (1 << len(bin_str))
    return val


def detect_gray_code_order_error(codes: list) -> int:
    for i in range(1, len(codes)):
        if len(codes[i]) != len(codes[i - 1]):
            return i + 1
        diff = sum(a != b for a, b in zip(codes[i], codes[i - 1]))
        if diff != 1:
            return i + 1
    return -1


def max_value_11bit() -> float:
    # Максимальное значение для 11-битного числа с фиксированной точкой (6 бит целая часть, 5 бит дробная)
    # 6 бит целая часть => max 2^6 - 1 = 63
    # 5 бит дробная часть => 1 - 2^-5 = 0.96875
    # Итог: 63 + 0.96875 = 63.96875
    return 63.96875


def min_value_11bit_sign_magnitude() -> float:
    return -63.96875


def min_value_11bit_U1() -> float:
    return -63.0


def biased_to_decimal(bin_str: str) -> int:
    n = len(bin_str)
    if any(c not in '01' for c in bin_str):
        raise ValueError("Input must be binary digits only")
    bias = (2 ** (n - 1)) - 1
    val = int(bin_str, 2)
    return val - bias


def bcd_to_decimal(bcd_str: str) -> int:
    bcd_str = bcd_str.strip()
    if len(bcd_str) % 4 != 0:
        raise ValueError("BCD string length must be multiple of 4")
    decimal_str = ""
    for i in range(0, len(bcd_str), 4):
        nibble = bcd_str[i:i + 4]
        if any(c not in '01' for c in nibble):
            raise ValueError("BCD must contain only binary digits")
        val = int(nibble, 2)
        if val > 9:
            raise ValueError(f"Invalid BCD digit: {nibble}")
        decimal_str += str(val)
    return int(decimal_str)


def decimal_to_bcd(decimal: int) -> str:
    if decimal < 0:
        raise ValueError("BCD supports only non-negative integers")
    decimal_str = str(decimal)
    bcd_str = ""
    for digit in decimal_str:
        val = int(digit)
        bcd_str += format(val, '04b')
    return bcd_str


def menu():
    while True:
        print("\nSelect a task:")
        print("1. Binary → Gray code")
        print("2. Base-14 → Decimal")
        print("3. Binary fraction → Decimal")
        print("4. Binary with fractional part → Decimal")
        print("5. Sign-Magnitude hex (#XYZ) → Decimal")
        print("6. 1's Complement (U1) hex (#XYZ) → Decimal")
        print("7. 2's Complement (U2) hex (#XYZ) → Decimal")
        print("8. Hex #XYZ → Decimal")
        print("9. Sign-Magnitude binary → Decimal")
        print("10. 1's Complement (U1) binary → Decimal")
        print("11. 2's Complement (U2) binary → Decimal")
        print("12. First error in Gray code sequence")
        print("13. Max value (Sign-Magnitude, 11-bit FXP)")
        print("14. Max value (1's Complement, 11-bit FXP)")
        print("15. Max value (2's Complement, 11-bit FXP)")
        print("16. Min value (Sign-Magnitude, 11-bit FXP)")
        print("17. Min value (1's Complement, 11-bit FXP)")
        print("18. Biased coding to decimal")
        print("19. BCD to decimal")
        print("20. Decimal to BCD")
        print("0. Exit")

        choice = input("Your choice: ").strip()
        try:
            if choice == "0":
                break
            elif choice == "1":
                b = input("Enter binary number (e.g. 10101): ")
                print("Gray code:", binary_to_gray(b))
            elif choice == "2":
                num = input("Enter base-14 number (e.g. 869.69 or 8A9.BC): ")
                print("Decimal:", base14_to_decimal(num))
            elif choice == "3":
                b = input("Enter binary fraction (e.g. 0.1001): ")
                print("Decimal:", binary_fraction_to_decimal(b))
            elif choice == "4":
                b = input("Enter binary number with fraction (e.g. 101100.011): ")
                print("Decimal:", binary_to_decimal(b))
            elif choice == "5":
                hex_val = input("Enter hex number in Sign-Magnitude format (e.g. #1F7): ")
                print("Decimal:", hex_to_decimal_sign_magnitude(hex_val))
            elif choice == "6":
                hex_val = input("Enter hex number in 1's Complement (U1) format (e.g. #1A3): ")
                print("Decimal:", hex_to_decimal_U1(hex_val))
            elif choice == "7":
                hex_val = input("Enter hex number in 2's Complement (U2) format (e.g. #1C3): ")
                print("Decimal:", hex_to_decimal_U2(hex_val))
            elif choice == "8":
                hex_val = input("Enter hex number (e.g. #1A3): ")
                print("Decimal:", hex_to_decimal(hex_val))
            elif choice == "9":
                bin_val = input("Enter sign-magnitude binary string (e.g. 100101): ")
                print("Decimal:", sign_magnitude_to_decimal(bin_val))
            elif choice == "10":
                bin_val = input("Enter U1 binary string (e.g. 11001): ")
                print("Decimal:", U1_to_decimal(bin_val))
            elif choice == "11":
                bin_val = input("Enter U2 binary string (e.g. 11001): ")
                print("Decimal:", U2_to_decimal(bin_val))
            elif choice == "12":
                n = int(input("Enter number of Gray codes: "))
                codes = []
                for i in range(n):
                    codes.append(input(f"Code {i + 1}: "))
                error_pos = detect_gray_code_order_error(codes)
                if error_pos == -1:
                    print("No errors detected in Gray code sequence.")
                else:
                    print(f"First error at position {error_pos}")
            elif choice == "13":
                print("Max value (Sign-Magnitude, 11-bit FXP):", max_value_11bit())
            elif choice == "14":
                print("Max value (1's Complement, 11-bit FXP): 63.96875")
            elif choice == "15":
                print("Max value (2's Complement, 11-bit FXP): 63.96875")
            elif choice == "16":
                print("Min value (Sign-Magnitude, 11-bit FXP):", min_value_11bit_sign_magnitude())
            elif choice == "17":
                print("Min value (1's Complement, 11-bit FXP):", min_value_11bit_U1())
            elif choice == "18":
                bin_val = input("Enter biased binary code: ")
                print("Decimal:", biased_to_decimal(bin_val))
            elif choice == "19":
                bcd_val = input("Enter BCD string (e.g. 000100100011): ")
                print("Decimal:", bcd_to_decimal(bcd_val))
            elif choice == "20":
                dec_val = int(input("Enter decimal number (non-negative): "))
                print("BCD:", decimal_to_bcd(dec_val))
            else:
                print("Invalid choice, try again.")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    menu()

