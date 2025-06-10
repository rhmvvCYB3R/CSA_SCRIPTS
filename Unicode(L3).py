def utf8_task_1():
    binary_input = input("Enter 32-bit binary string (space-separated): ")
    try:
        bits = binary_input.replace(' ', '')
        if len(bits) != 32:
            return "-1" 
        
        codepoint = int(bits, 2)
        
        if not (0x000000 <= codepoint <= 0x10FFFF):
            return "-1"
        
        try:
            char = chr(codepoint)
            utf8_bytes = char.encode('utf-8')
            return ' '.join(f"{byte:08b}" for byte in utf8_bytes)
        except ValueError:
            return "-1"
    except ValueError:
        return "-1"
    except Exception:
        return "-1"

def utf8_task_2():
    bytes_str = input("Enter UTF-8 bytes (space-separated): ")
    try:
        byte_value_strings = bytes_str.strip().split()
        
        for b_str in byte_value_strings:
            if not (len(b_str) == 8 and all(bit in '01' for bit in b_str)):
                return "-1"

        original_info_bits = ""
        num_bytes = len(byte_value_strings)
        
        if not num_bytes:
            return "-1"

        first_byte_bin = byte_value_strings[0]

        if first_byte_bin.startswith('0'):
            if num_bytes != 1: return "-1"
            original_info_bits = first_byte_bin[1:]
        elif first_byte_bin.startswith('110'):
            if num_bytes < 2 or not all(b.startswith('10') for b in byte_value_strings[1:]): return "-1"
            original_info_bits = first_byte_bin[3:]
        elif first_byte_bin.startswith('1110'):
            if num_bytes < 3 or not all(b.startswith('10') for b in byte_value_strings[1:]): return "-1"
            original_info_bits = first_byte_bin[4:]
        elif first_byte_bin.startswith('11110'):
            if num_bytes < 4 or not all(b.startswith('10') for b in byte_value_strings[1:]): return "-1"
            original_info_bits = first_byte_bin[5:]
        elif first_byte_bin.startswith('111110'):
            if num_bytes < 5 or not all(b.startswith('10') for b in byte_value_strings[1:]): return "-1"
            original_info_bits = first_byte_bin[6:]
        elif first_byte_bin.startswith('1111110'):
            if num_bytes < 6 or not all(b.startswith('10') for b in byte_value_strings[1:]): return "-1"
            original_info_bits = first_byte_bin[7:]
        else:
            return "-1"

        for i in range(1, num_bytes):
            original_info_bits += byte_value_strings[i][2:]

        if not original_info_bits:
            return "-1"
        
        codepoint = int(original_info_bits, 2)

        if not (0x000000 <= codepoint <= 0x10FFFF):
            return "-1"

        char = chr(codepoint)
        shortest_utf8_bytes = char.encode('utf-8')
        
        return '.'.join(f"{b:08b}" for b in shortest_utf8_bytes)
    except Exception:
        return "-1"

def utf8_task_3():
    bytes_str = input("Enter UTF-8 bytes (space-separated): ")
    try:
        byte_value_strings = bytes_str.strip().split()
        
        for b_str in byte_value_strings:
            if not (len(b_str) == 8 and all(bit in '01' for bit in b_str)):
                return "-1"

        original_info_bits = ""
        num_bytes = len(byte_value_strings)

        if not num_bytes:
            return "-1"
        first_byte_bin = byte_value_strings[0]

        if first_byte_bin.startswith('0'): 
            if num_bytes != 1: return "-1"
            original_info_bits = first_byte_bin[1:]
        elif first_byte_bin.startswith('110'):
            if num_bytes < 2 or not all(b.startswith('10') for b in byte_value_strings[1:]): return "-1"
            original_info_bits = first_byte_bin[3:]
        elif first_byte_bin.startswith('1110'):
            if num_bytes < 3 or not all(b.startswith('10') for b in byte_value_strings[1:]): return "-1"
            original_info_bits = first_byte_bin[4:]
        elif first_byte_bin.startswith('11110'):
            if num_bytes < 4 or not all(b.startswith('10') for b in byte_value_strings[1:]): return "-1"
            original_info_bits = first_byte_bin[5:]
        elif first_byte_bin.startswith('111110'):
            if num_bytes < 5 or not all(b.startswith('10') for b in byte_value_strings[1:]): return "-1"
            original_info_bits = first_byte_bin[6:]
        elif first_byte_bin.startswith('1111110'):
            if num_bytes < 6 or not all(b.startswith('10') for b in byte_value_strings[1:]): return "-1"
            original_info_bits = first_byte_bin[7:]
        else:
            return "-1"

        for i in range(1, num_bytes):
            original_info_bits += byte_value_strings[i][2:]
        
        if not original_info_bits:
            return "-1"

        codepoint = int(original_info_bits, 2)
        
        if not (0x000000 <= codepoint <= 0x10FFFF):
             return "-1"

        ascii_value = codepoint & 0x7F 
        return f"{ascii_value:07b}" 
    except Exception:
        return "-1"

def utf8_task_4():
    bytes_str = input("Enter UTF-8 bytes (space-separated): ")
    try:
        byte_value_strings = bytes_str.strip().split()
        if not byte_value_strings:
            return "-1"

        original_info_bits = ""
        first_byte_bin = byte_value_strings[0]

        for b_str in byte_value_strings:
            if not (len(b_str) == 8 and all(bit in '01' for bit in b_str)):
                return "-1"

        num_input_bytes = len(byte_value_strings)

        if first_byte_bin.startswith('0'):
            if num_input_bytes != 1: return "-1"
            original_info_bits = first_byte_bin[1:]
        elif first_byte_bin.startswith('110'):
            if num_input_bytes < 2 or not all(b.startswith('10') for b in byte_value_strings[1:]): return "-1"
            original_info_bits = first_byte_bin[3:]
        elif first_byte_bin.startswith('1110'):
            if num_input_bytes < 3 or not all(b.startswith('10') for b in byte_value_strings[1:]): return "-1"
            original_info_bits = first_byte_bin[4:]
        elif first_byte_bin.startswith('11110'):
            if num_input_bytes < 4 or not all(b.startswith('10') for b in byte_value_strings[1:]): return "-1"
            original_info_bits = first_byte_bin[5:]
        elif first_byte_bin.startswith('111110'):
            if num_input_bytes < 5 or not all(b.startswith('10') for b in byte_value_strings[1:]): return "-1"
            original_info_bits = first_byte_bin[6:]
        elif first_byte_bin.startswith('1111110'):
            if num_input_bytes < 6 or not all(b.startswith('10') for b in byte_value_strings[1:]): return "-1"
            original_info_bits = first_byte_bin[7:]
        else:
            return "-1"

        for i in range(1, num_input_bytes):
            original_info_bits += byte_value_strings[i][2:]

        effective_codepoint_value_bits = '00' + original_info_bits
        
        final_result_bytes = []

        encoding_schemes = [
            (1, '0', 7, 7),
            (2, '110', 5, 11),
            (3, '1110', 4, 16),
            (4, '11110', 3, 21),
            (5, '111110', 2, 26),
            (6, '1111110', 1, 31)
        ]

        for (n_output_bytes, header_prefix_template, header_info_bits_len, total_info_bits_capacity) in encoding_schemes:
            if total_info_bits_capacity >= len(effective_codepoint_value_bits):
                padding_zeros_count = total_info_bits_capacity - len(effective_codepoint_value_bits)
                
                full_bit_string_to_encode = ('0' * padding_zeros_count) + effective_codepoint_value_bits
                
                current_bytes_output = []
                
                header_info_bits = full_bit_string_to_encode[:header_info_bits_len]
                header_byte_str = header_prefix_template + header_info_bits
                current_bytes_output.append(int(header_byte_str, 2))
                
                remaining_codepoint_bits_for_data_bytes = full_bit_string_to_encode[header_info_bits_len:]
                
                for i in range(n_output_bytes - 1):
                    chunk = remaining_codepoint_bits_for_data_bytes[i*6:(i+1)*6]
                    data_byte_str = '10' + chunk
                    current_bytes_output.append(int(data_byte_str, 2))
                
                final_result_bytes = current_bytes_output
                break

        if not final_result_bytes:
            return "-1"

        return '.'.join(f"{b:08b}" for b in final_result_bytes)

    except Exception:
        return "-1"

def utf8_task_5():
    # Maximum value for a 32-bit unsigned integer (all ones)
    # This is 2^32 - 1 = 4,294,967,295
    return "11111111 11111111 11111111 11111111"

def utf8_task_6():
    # Minimum value for a 32-bit unsigned integer (all zeros)
    # This is 0
    return "00000000 00000000 00000000 00000000"

def utf8_task_7():
    # Average value for a 32-bit unsigned integer range (0 to 2^32 - 1)
    # (0 + (2^32 - 1)) // 2 = (4294967295) // 2 = 2147483647
    # 2147483647 in binary (32 bits) is 01111111 11111111 11111111 11111111
    return "01111111 11111111 11111111 11111111"


def menu():
    while True:
        print("""
Choose a task:
1. Convert 32-bit binary to UTF-8
2. Shortest alternative UTF-8 code
3. Get ASCII binary code from UTF-8
4. Alternative UTF-8 with n leading zeros before first 1 in info byte
5. Max value in UTF-32 (as 32-bit integer)
6. Min value in UTF-32 (as 32-bit integer)
7. Avg value in UTF-32 (as 32-bit integer)
0. Exit
        """)
        choice = input("Your choice: ")
        if choice == '1':
            print("Result:", utf8_task_1())
        elif choice == '2':
            print("Result:", utf8_task_2())
        elif choice == '3':
            print("Result:", utf8_task_3())
        elif choice == '4':
            print("Result:", utf8_task_4())
        elif choice == '5':
            print("Result:", utf8_task_5())
        elif choice == '6':
            print("Result:", utf8_task_6())
        elif choice == '7':
            print("Result:", utf8_task_7())
        elif choice == '0':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu()