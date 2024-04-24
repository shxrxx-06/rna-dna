import argparse
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def encrypt_file(file_path, key, key_size):
    if key_size == 128:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    elif key_size == 192:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key[:24]), modes.CBC(iv), backend=default_backend())
    elif key_size == 256:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key[:32]), modes.CBC(iv), backend=default_backend())
    else:
        raise ValueError("Invalid key size. Key size must be 128, 192, or 256 bits.")

    encryptor = cipher.encryptor()

    with open(file_path, 'rb') as file:
        plaintext = file.read()

    # Pad the plaintext before encryption
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()

    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    output_file = f'encrypted_file_{key_size}_bits.txt'
    with open(output_file, 'wb') as encrypted_file:
        encrypted_file.write(ciphertext)

    print(f"File encrypted with {key_size}-bit key. Encrypted file saved as {output_file}")

def decrypt_file(file_path, key, key_size):
    if key_size == 128:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    elif key_size == 192:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key[:24]), modes.CBC(iv), backend=default_backend())
    elif key_size == 256:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key[:32]), modes.CBC(iv), backend=default_backend())
    else:
        raise ValueError("Invalid key size. Key size must be 128, 192, or 256 bits.")

    decryptor = cipher.decryptor()

    with open(file_path, 'rb') as file:
        ciphertext = file.read()

    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    output_file = f'decrypted_file.txt'
    with open(output_file, 'wb') as decrypted_file:
        decrypted_file.write(plaintext)

    print(f"File decrypted with {key_size}-bit key. Decrypted file saved as {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Encrypt/Decrypt a file using AES algorithm.')
    parser.add_argument('mode', choices=['encrypt', 'decrypt'], help='Mode: encrypt or decrypt')
    parser.add_argument('file_path', help='Path to the file')
    parser.add_argument('key_size', type=int, choices=[128, 192, 256], help='Key size (128, 192, or 256 bits)')
    parser.add_argument('--key', required=True, help='AES key')
    args = parser.parse_args()

    # Validate the length of the key based on the key size
    if len(args.key.encode('ascii')) != args.key_size // 8:
        raise ValueError(f"Invalid key length for {args.key_size}-bit key.")

    key_bytes = args.key.encode('ascii')
    if args.key_size == 192 and len(key_bytes) < 24:
        key_bytes = key_bytes.ljust(24, b'\x00')
    elif args.key_size == 256 and len(key_bytes) < 32:
        key_bytes = key_bytes.ljust(32, b'\x00')

    if args.mode == 'encrypt':
        encrypt_file(args.file_path, key_bytes, args.key_size)
    else:
        decrypt_file(args.file_path, key_bytes, args.key_size)

if __name__ == "__main__":
    main()
