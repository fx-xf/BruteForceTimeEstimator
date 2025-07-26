#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import secrets  # For secure random password generation
import string  # For character sets
import sys  # For system exit

def generate_password(length=16, use_uppercase=True, use_digits=True, use_symbols=True):
    """Generates a secure random password based on user-specified criteria."""
    characters = string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    if not characters:
        raise ValueError("At least one character type must be selected.")

    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def get_user_input():
    """Prompts user for password generation preferences."""
    try:
        length_input = input("Enter password length (default 16): ").strip()
        length = int(length_input) if length_input else 16
        
        if length < 4:
            print("Minimum password length is 4 characters. Setting to 4.")
            length = 4

        uppercase_input = input("Use uppercase letters? (Y/n, default Y): ").strip().lower()
        use_uppercase = uppercase_input != 'n'
        
        digits_input = input("Use digits? (Y/n, default Y): ").strip().lower()
        use_digits = digits_input != 'n'
        
        symbols_input = input("Use special characters? (Y/n, default Y): ").strip().lower()
        use_symbols = symbols_input != 'n'
        
        return length, use_uppercase, use_digits, use_symbols
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except EOFError:
        print("\nInput error.")
        sys.exit(1)
    except ValueError:
        print("Invalid length input. Using default value 16.")
        return 16, True, True, True

def main():
    """Main function to run the password generator."""
    print("Secure Password Generator")
    
    length, use_uppercase, use_digits, use_symbols = get_user_input()
    
    try:
        password = generate_password(length, use_uppercase, use_digits, use_symbols)
        print(f"\nYour generated password:\n{password}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()