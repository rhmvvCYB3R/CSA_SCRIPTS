import math

def binary_to_decimal():
    binary_str = input("Введите бинарное число (например, 1110011110): ").strip()
    return int(binary_str, 2)

def binary_to_hex():
    binary_str = input("Введите бинарное число с пробелами (например, 1001 0011 1000): ").strip()
    return hex(int(binary_str.replace(" ", ""), 2))[2:].upper()

def min_bits_needed():
    min_val = int(input("Введите минимальное значение (например, 58): "))
    max_val = int(input("Введите максимальное значение (например, 101): "))
    return math.ceil(math.log2(max_val - min_val + 1))

def hex_to_binary():
    hex_str = input("Введите шестнадцатеричное число без #: ").strip()
    return bin(int(hex_str, 16))[2:]

def even_parity_bit():
    binary_str = input("Введите последовательность битов (например, 0011 1110 0): ").strip()
    total_ones = binary_str.replace(" ", "").count("1")
    return '0' if total_ones % 2 == 0 else '1'

def odd_parity_bit():
    binary_str = input("Введите последовательность битов (например, 0011 1110 0): ").strip()
    total_ones = binary_str.replace(" ", "").count("1")
    return '1' if total_ones % 2 == 0 else '0'

def hex_to_decimal():
    hex_str = input("Введите шестнадцатеричное число без #: ").strip()
    return int(hex_str, 16)

def bits_needed_for_states():
    print("Введите состояния контроллера через запятую (например: R,YR,Y,G,none):")
    states = input().strip().split(",")
    return math.ceil(math.log2(len(states)))

def print_menu():
    print("\nВыберите задачу:")
    print("1. NBC -> Decimal")
    print("2. Binary -> Hexadecimal")
    print("3. Min bits needed (от min до max)")
    print("4. Hex -> Binary")
    print("5. Even parity bit")
    print("6. Odd parity bit")
    print("7. Hex -> Decimal")
    print("8. Bits needed for controller states")
    print("0. Выход")

def main():
    while True:
        print_menu()
        choice = input("Введите номер задачи: ").strip()

        try:
            if choice == '1':
                print("Результат:", binary_to_decimal())
            elif choice == '2':
                print("Результат:", binary_to_hex())
            elif choice == '3':
                print("Результат:", min_bits_needed())
            elif choice == '4':
                print("Результат:", hex_to_binary())
            elif choice == '5':
                print("Результат (бит четности):", even_parity_bit())
            elif choice == '6':
                print("Результат (бит нечетности):", odd_parity_bit())
            elif choice == '7':
                print("Результат:", hex_to_decimal())
            elif choice == '8':
                print("Результат:", bits_needed_for_states())
            elif choice == '0':
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
        except Exception as e:
            print("Ошибка:", e)

if __name__ == "__main__":
    main()
