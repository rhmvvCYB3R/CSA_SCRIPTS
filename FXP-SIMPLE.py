import math

def bin_to_dec(binary_str, bits, code_type="U2"):
    """
    Converts a binary string to its decimal equivalent based on the specified code type.
    """
    if not binary_str:
        return 0

    if code_type == "U2":
        if binary_str[0] == '1':  # Negative number in U2
            return int(binary_str, 2) - (1 << bits)
        else:  # Positive number
            return int(binary_str, 2)
    elif code_type == "SM":
        if binary_str[0] == '1':  # Negative number in Sign-Magnitude
            return -int(binary_str[1:], 2)
        else:  # Positive number
            return int(binary_str[1:], 2)
    elif code_type == "U1":
        if binary_str[0] == '1':  # Negative number in One's Complement
            # Invert and convert to decimal, then negate
            # Note: For -0 (11...1), this would result in +0 (00...0).
            inverted_magnitude = ''.join(['1' if bit == '0' else '0' for bit in binary_str[1:]])
            return -int(inverted_magnitude, 2)
        else:  # Positive number
            return int(binary_str, 2)
    return None 

def dec_to_bin(decimal_val, bits, code_type="U2"):
    """
    Converts a decimal number to its binary string representation (U2/SM/U1).
    """
    if decimal_val >= 0:
        return bin(decimal_val)[2:].zfill(bits)
    else:
        if code_type == "U2":
            # For negative U2, add to 2^bits and convert
            return bin((1 << bits) + decimal_val)[2:].zfill(bits)
        elif code_type == "SM":
            sign_bit = '1'
            magnitude = abs(decimal_val)
            # Ensure magnitude is (bits - 1) long
            return sign_bit + bin(magnitude)[2:].zfill(bits - 1)
        elif code_type == "U1":
            # Convert absolute value to binary, then invert for magnitude
            pos_val_bin = bin(abs(decimal_val))[2:].zfill(bits - 1)
            inverted_magnitude = ''.join(['1' if bit == '0' else '0' for bit in pos_val_bin])
            return '1' + inverted_magnitude
    return None

def sign_extend(binary_str, target_bits, code_type):
    """
    Sign-extends a binary number to target_bits based on the code type.
    For U1/U2, repeats the sign bit. For SM, pads magnitude with zeros.
    """
    current_bits = len(binary_str)
    if current_bits >= target_bits:
        # If current bits are already target_bits or more, return as is.
        # This implies no extension is needed or truncation for larger inputs (handled elsewhere if required).
        return binary_str 

    sign_bit = binary_str[0]
    extension_amount = target_bits - current_bits

    if code_type == "SM":
        # For Sign-Magnitude, the magnitude is zero-extended.
        # Sign bit remains, then zero-pad the magnitude part.
        return sign_bit + binary_str[1:].zfill(target_bits - 1)
    elif code_type in ["U1", "U2"]:
        # For One's and Two's Complement, repeat the sign bit.
        return sign_bit * extension_amount + binary_str
    else:
        raise ValueError(f"Unsupported code type for sign extension: {code_type}")


def add_binary(num1_str, num2_str, incoming_carry, code_type="U2"):
    """
    Performs binary addition and returns sum, carry bits, and NZVC conditions.
    Code_type specifies the representation for NZVC calculation.
    Handles different lengths by sign-extending.
    """
    # Determine the effective number of bits for the operation.
    # This should be the length of the longest input number *after* potential padding
    max_len = max(len(num1_str), len(num2_str))

    # Apply sign extension if numbers have different lengths
    num1_str_extended = sign_extend(num1_str, max_len, code_type)
    num2_str_extended = sign_extend(num2_str, max_len, code_type)
    
    bits = max_len

    sum_bits = [''] * bits
    # carries stores from c0 (incoming) to c_n (carry out of MSB)
    carries = [''] * (bits + 1) 
    
    current_carry = incoming_carry
    carries[0] = str(incoming_carry) # c0 is the initial incoming carry

    # Perform addition from right to left (LSB to MSB)
    for i in range(bits - 1, -1, -1):
        bit1 = int(num1_str_extended[i])
        bit2 = int(num2_str_extended[i])

        s = bit1 ^ bit2 ^ current_carry # Sum bit
        c = (bit1 & bit2) | (bit1 & current_carry) | (bit2 & current_carry) # Carry out for this position

        sum_bits[i] = str(s)
        # Store carries: carries[1] is c1, carries[bits] is c_n
        carries[bits - i] = str(c) 
        current_carry = c

    final_sum_str = "".join(sum_bits)
    
    # Handle end-around carry for U1
    carry_out_msb_before_eac = int(carries[bits]) # This is c_n
    if code_type == "U1" and carry_out_msb_before_eac == 1:
        # Perform end-around carry: add 1 to the result
        temp_sum_int = int(final_sum_str, 2) + 1
        final_sum_str = bin(temp_sum_int)[2:].zfill(bits)
        if len(final_sum_str) > bits:
            final_sum_str = final_sum_str[-bits:] # Truncate if it grows
            
    # NZVC conditions
    # N is 1 if MSB of result is 1
    N = int(final_sum_str[0]) 
    
    # Z is 1 if result is zero
    Z = 1 if int(final_sum_str, 2) == 0 else 0 
    
    # C is the carry out of the MSB (c_n)
    C = carry_out_msb_before_eac 
    
    # Overflow (V) for signed addition.
    V = 0 
    if code_type == "U2":
        # V = (carry_in_MSB XOR carry_out_MSB)
        # carry_in_MSB is carries[bits-1] (c_n-1, the carry into the most significant bit position)
        # carry_out_MSB is carries[bits] (c_n, the carry out from the most significant bit position)
        V = int(carries[bits-1]) ^ int(carries[bits]) 
    elif code_type == "U1":
        # Overflow in U1: if both operands have the same sign and the result has a different sign
        val1_dec = bin_to_dec(num1_str_extended, bits, code_type)
        val2_dec = bin_to_dec(num2_str_extended, bits, code_type)
        res_dec = bin_to_dec(final_sum_str, bits, code_type)

        # Check if operands have the same sign
        if (val1_dec >= 0 and val2_dec >= 0) or (val1_dec < 0 and val2_dec < 0):
            # Check if result has a different sign
            if (val1_dec >= 0 and res_dec < 0) or (val1_dec < 0 and res_dec >= 0):
                V = 1

    # Return carries from c_n down to c0 (reverse order for output display)
    # carries list: [c0, c1, ..., c_n-1, c_n]
    # To get c_n, c_n-1, ..., c0, we reverse a slice including all carry values.
    return final_sum_str, "".join(carries[bits::-1]), N, Z, V, C 

def negate_sm(binary_str):
    """Negates a number in Sign-Magnitude code."""
    if not binary_str:
        return ""
    # Simply flip the sign bit
    negated_str = '1' if binary_str[0] == '0' else '0'
    negated_str += binary_str[1:]
    return negated_str

def negate_u1(binary_str):
    """Negates a number in U1 (One's Complement) code and determines NZVC."""
    bits = len(binary_str)
    
    # Negation in U1 is simply inverting all bits
    negated_val_bin = ''.join(['1' if bit == '0' else '0' for bit in binary_str])
    
    # Determine NZVC conditions for negation in U1
    N = int(negated_val_bin[0]) # N is 1 if MSB of result is 1
    Z = 1 if int(negated_val_bin, 2) == 0 else 0 # Z is 1 if result is zero
    
    # Overflow (V) for U1 negation: Generally, not defined in the same way as U2.
    # If the input is '11...1' (negative zero) and it negates to '00...0' (positive zero),
    # there isn't typically an overflow condition, though the existence of two zeros is a property.
    # For a general negation operation, V is often 0 unless specific rules state otherwise.
    V = 0 
    
    # Carry (C) for U1 negation: Not directly applicable as a carry from an adder.
    C = 0 
    
    return negated_val_bin, N, Z, V, C

def negate_u2(binary_str):
    """Negates a number in U2 (Two's Complement) code and determines NZVC."""
    bits = len(binary_str)
    
    # Handle the special case of the most negative number (-2^(bits-1))
    # E.g., for 8-bit, 10000000 (-128). Its negation (+128) cannot be represented.
    if binary_str[0] == '1' and binary_str[1:] == '0' * (bits - 1):
        negated_val_bin = binary_str # Remains itself, or is an error condition
        
        N = 1 # Still negative
        Z = 0 # Not zero
        V = 1 # Overflow occurs because positive equivalent is out of range
        C = 0 # No carry out for standard negation interpretation
        
        return negated_val_bin, N, Z, V, C

    # 1. Invert all bits (One's Complement)
    inverted_bits = ''.join(['1' if bit == '0' else '0' for bit in binary_str])
    
    # 2. Add 1 to the result (mimic add_binary for this specific addition)
    # We convert to int, add 1, then convert back to binary string of correct length
    temp_sum = int(inverted_bits, 2) + 1
    negated_val_bin = bin(temp_sum)[2:].zfill(bits)
    
    # If adding 1 results in an extra bit (e.g., 0111 (+7) becomes 1000 (-8)),
    # this extra bit is implicitly truncated for U2 negation.
    if len(negated_val_bin) > bits:
        negated_val_bin = negated_val_bin[-bits:] 

    # Determine NZVC conditions for general negation in U2
    N = int(negated_val_bin[0]) # N: Sign of the result
    Z = 1 if int(negated_val_bin, 2) == 0 else 0 # Z: Is result zero?
    V = 0 # V: For all other cases besides the most negative number, V=0.
    C = 0 # C: Carry flag for negation is typically 0.
    
    return negated_val_bin, N, Z, V, C

def extend_sm(binary_str, target_bits):
    """Extends a Sign-Magnitude binary number to target_bits."""
    current_bits = len(binary_str)
    if current_bits > target_bits:
        return "Error: Target bits less than current bits."
    
    sign_bit = binary_str[0]
    magnitude = binary_str[1:]
    
    # For Sign-Magnitude, the magnitude is zero-extended.
    extended_magnitude = magnitude.zfill(target_bits - 1) 
    return sign_bit + extended_magnitude

def extend_u(binary_str, target_bits):
    """Extends a U1 (One's Complement) or U2 (Two's Complement) binary number to target_bits."""
    current_bits = len(binary_str)
    if current_bits > target_bits:
        return "Error: Target bits less than current bits."
    
    sign_bit = binary_str[0]
    
    # For U1/U2, extend by repeating the sign bit (sign extension).
    extension_bits = sign_bit * (target_bits - current_bits)
    return extension_bits + binary_str

def display_menu():
    print("\n--- Choose a Task ---")
    print("1. Add N-bit numbers and determine carries (C_n down to C_0)")
    print("2. Add 8-bit numbers and determine result, NZVC conditions")
    print("3. Add N-bit numbers and determine result, NZVC conditions")
    print("4. Negate a number in Sign-Magnitude code")
    print("5. Negate a number in U1 (1C) code and determine NZVC") # Updated description
    print("6. Negate a number in U2 (2C) code and determine NZVC") # Updated description
    print("7. Extend a Sign-Magnitude number to N bits")
    print("8. Extend a U1/U2 number to N bits") 
    print("9. Add two numbers of different lengths (U1/U2) and determine result, NZVC conditions")
    print("10. Add two N-bit numbers (U1/U2) and determine result, NZVC conditions") 
    print("0. Exit")
    print("----------------------")

def get_binary_input(prompt, num_bits=None):
    while True:
        s = input(prompt).strip()
        if not all(bit in '01' for bit in s):
            print("Error: Please enter only 0s and 1s.")
            continue
        if num_bits and len(s) != num_bits:
            print(f"Error: Please enter exactly {num_bits} bits.")
            continue
        return s

def get_int_input(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = int(input(prompt))
            if min_val is not None and val < min_val:
                print(f"Error: Please enter a number no less than {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"Error: Please enter a number no greater than {max_val}.")
                continue
            return val
        except ValueError:
            print("Error: Please enter an integer.")

def get_code_type_input(prompt_msg, allowed_types=["U1", "U2", "SM"]):
    while True:
        code_type = input(prompt_msg).strip().upper()
        if code_type in allowed_types:
            return code_type
        else:
            print(f"Error: Valid code types are: {', '.join(allowed_types)}.")

# --- Main Program Loop ---
while True:
    display_menu()
    choice = input("Your choice: ")

    if choice == '1':
        print("\n--- Add N-bit Numbers and Determine Carries ---")
        code_type = get_code_type_input("Choose number representation for addition (U1 or U2): ", allowed_types=["U1", "U2"])
        bits = get_int_input("Enter the number of bits for the numbers (e.g., 3 for 3-bit numbers): ", min_val=1)
        num1 = get_binary_input(f"Enter the first {bits}-bit number (binary): ", bits)
        num2 = get_binary_input(f"Enter the second {bits}-bit number (binary): ", bits)
        incoming_carry = get_int_input("Enter the 'incoming' carry (0 or 1): ", min_val=0, max_val=1)
        
        _, carries_str, _, _, _, _ = add_binary(num1, num2, incoming_carry, code_type)
        
        # carries_str is c_n c_{n-1} ... c0. We need to find c_n, c_{n-1}, ..., c_0 in that order.
        # The list 'carries' inside add_binary is [c0, c1, ..., c_n]. 
        # When reversed, it becomes [c_n, c_{n-1}, ..., c0].
        # So, carries_str already contains the correct order for display.
        print(f"Carries (c{bits} down to c0): {carries_str}")
        
    elif choice == '2':
        print("\n--- Add 8-bit Numbers and Determine Result, NZVC Conditions ---")
        code_type = get_code_type_input("Choose number representation for addition (U1 or U2): ", allowed_types=["U1", "U2"])
        num_bits = 8
        num1 = get_binary_input(f"Enter the first {num_bits}-bit number (binary): ", num_bits)
        num2 = get_binary_input(f"Enter the second {num_bits}-bit number (binary): ", num_bits)
        incoming_carry = get_int_input("Enter the 'incoming' carry (0 or 1): ", min_val=0, max_val=1)
        
        final_sum_str, carries_details, N, Z, V, C = add_binary(num1, num2, incoming_carry, code_type)
        decimal_result = bin_to_dec(final_sum_str, num_bits, code_type)
        
        print(f"Result in decimal: {decimal_result}.{N}{Z}{V}{C}")
        print(f"Carries (c{num_bits} down to c0): {carries_details}")

    elif choice == '3':
        print("\n--- Add N-bit Numbers and Determine Result, NZVC Conditions ---")
        code_type = get_code_type_input("Choose number representation for addition (U1 or U2): ", allowed_types=["U1", "U2"])
        bits = get_int_input("Enter the number of bits for the numbers (e.g., 4 for 4-bit numbers): ", min_val=1)
        num1 = get_binary_input(f"Enter the first {bits}-bit number (binary): ", bits)
        num2 = get_binary_input(f"Enter the second {bits}-bit number (binary): ", bits)
        incoming_carry = get_int_input("Enter the 'incoming' carry (0 or 1): ", min_val=0, max_val=1)
        
        final_sum_str, carries_details, N, Z, V, C = add_binary(num1, num2, incoming_carry, code_type)
        decimal_result = bin_to_dec(final_sum_str, bits, code_type)
        
        print(f"Result in decimal: {decimal_result}.{N}{Z}{V}{C}")
        print(f"Carries (c{bits} down to c0): {carries_details}")

    elif choice == '4':
        print("\n--- Negate a Number in Sign-Magnitude Code ---")
        num = get_binary_input("Enter the number in Sign-Magnitude code (binary): ")
        negated_num = negate_sm(num)
        print(f"Negation result: {negated_num}")

    elif choice == '5':
        print("\n--- Negate a Number in U1 (1C) Code and Determine NZVC ---")
        num = get_binary_input("Enter the number in U1 (1C) code (binary): ")
        negated_num_str, N, Z, V, C = negate_u1(num)
        
        decimal_result = bin_to_dec(negated_num_str, len(num), "U1")
        print(f"Negation result: {decimal_result}.{N}{Z}{V}{C}")
            
    elif choice == '6':
        print("\n--- Negate a Number in U2 (2C) Code and Determine NZVC ---")
        num = get_binary_input("Enter the number in U2 (2C) code (binary): ")
        negated_num_str, N, Z, V, C = negate_u2(num)
        
        decimal_result = bin_to_dec(negated_num_str, len(num), "U2")
        print(f"Negation result: {decimal_result}.{N}{Z}{V}{C}")

    elif choice == '7':
        print("\n--- Extend a Sign-Magnitude Number ---")
        num = get_binary_input("Enter the number in Sign-Magnitude code (binary): ")
        target_bits = get_int_input("Enter the desired number of bits for extension: ", min_val=len(num))
        extended_num = extend_sm(num, target_bits)
        print(f"Extended number: {extended_num}")

    elif choice == '8':
        print("\n--- Extend a U1/U2 Number ---")
        # For U1/U2 extension, the logic is the same: sign extension
        code_type_ext = get_code_type_input("Choose code type for extension (U1 or U2): ", allowed_types=["U1", "U2"]) 
        num = get_binary_input(f"Enter the number in {code_type_ext} code (binary): ")
        target_bits = get_int_input("Enter the desired number of bits for extension: ", min_val=len(num))
        extended_num = extend_u(num, target_bits) 
        print(f"Extended number: {extended_num}")

    elif choice == '9':
        print("\n--- Add Two Numbers of Different Lengths and Determine Result, NZVC Conditions ---")
        code_type = get_code_type_input("Choose number representation for addition (U1 or U2): ", allowed_types=["U1", "U2"])
        num1 = get_binary_input("Enter the first binary number (e.g., 00000001): ")
        num2 = get_binary_input("Enter the second binary number (e.g., 111110): ")
        incoming_carry = get_int_input("Enter the 'incoming' carry (0 or 1): ", min_val=0, max_val=1)
        
        final_sum_str, carries_details, N, Z, V, C = add_binary(num1, num2, incoming_carry, code_type)
        
        # The number of bits for decimal conversion should be the maximum length after sign-extension
        max_len = max(len(num1), len(num2))
        decimal_result = bin_to_dec(final_sum_str, max_len, code_type)
        
        print(f"Result in decimal: {decimal_result}.{N}{Z}{V}{C}")
        print(f"Carries (c{max_len} down to c0): {carries_details}") 

    elif choice == '10':
        print("\n--- Add Two N-bit Numbers and Determine Result, NZVC Conditions ---")
        code_type = get_code_type_input("Choose number representation for addition (U1 or U2): ", allowed_types=["U1", "U2"])
        num_bits = get_int_input("Enter the number of bits for the numbers (e.g., 8 or 4): ", min_val=1)
        num1 = get_binary_input(f"Enter the first {num_bits}-bit number (binary): ", num_bits)
        num2 = get_binary_input(f"Enter the second {num_bits}-bit number (binary): ", num_bits)
        incoming_carry = get_int_input("Enter the 'incoming' carry (0 or 1): ", min_val=0, max_val=1)
        
        final_sum_str, carries_details, N, Z, V, C = add_binary(num1, num2, incoming_carry, code_type)
        decimal_result = bin_to_dec(final_sum_str, num_bits, code_type)
        
        print(f"Result in decimal: {decimal_result}.{N}{Z}{V}{C}")
        print(f"Carries (c{num_bits} down to c0): {carries_details}") 

    elif choice == '0':
        print("Exiting program. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")