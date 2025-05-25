# Power function to return value of a^b mod P
def power(a, b, p):
    if b == 0:
        return 1
    elif b == 1:
        return a % p
    else:
        return pow(a, b, p)

def generate_dh_public_key(private_key, P=23, G=9):
    """Generate Diffie-Hellman public key from user-provided private key"""
    # Calculate public key using the private key provided by the user
    public_key = power(G, private_key, P)
    return public_key

def calculate_shared_secret(other_public_key, my_private_key, P):
    """Calculate shared secret from other party's public key"""
    return power(other_public_key, my_private_key, P)

def dh_encrypt(message, shared_secret):
    """Encrypt message using shared secret (XOR cipher)"""
    # Simple XOR encryption using shared secret
    key_bytes = str(shared_secret).encode()
    message_bytes = message.encode()
    encrypted = bytearray()
    
    for i in range(len(message_bytes)):
        encrypted.append(message_bytes[i] ^ key_bytes[i % len(key_bytes)])
    
    return encrypted.hex()

def dh_decrypt(encrypted_message, shared_secret):
    """Decrypt message using shared secret (XOR cipher)"""
    # Simple XOR decryption using shared secret
    key_bytes = str(shared_secret).encode()
    try:
        encrypted_bytes = bytes.fromhex(encrypted_message)
    except ValueError:
        raise ValueError("Invalid hexadecimal input for decryption")
    
    decrypted = bytearray()
    
    for i in range(len(encrypted_bytes)):
        decrypted.append(encrypted_bytes[i] ^ key_bytes[i % len(key_bytes)])
    
    return decrypted.decode('utf-8', errors='ignore')

# Legacy function names for backward compatibility
encrypt = dh_encrypt
decrypt = dh_decrypt

def main():
    # Example usage with user-provided keys
    P, G = 23, 9
    print(f"Public parameters - P: {P}, G: {G}")
    
    # Alice provides her private key
    alice_private = 4  # This would be provided by the user
    alice_public = generate_dh_public_key(alice_private, P, G)
    print(f"Alice - Private key: {alice_private}, Public key: {alice_public}")
    
    # Bob provides his private key
    bob_private = 3  # This would be provided by the user
    bob_public = generate_dh_public_key(bob_private, P, G)
    print(f"Bob - Private key: {bob_private}, Public key: {bob_public}")
    
    # They exchange public keys and calculate shared secret
    alice_secret = calculate_shared_secret(bob_public, alice_private, P)
    bob_secret = calculate_shared_secret(alice_public, bob_private, P)
    
    print(f"Alice's shared secret: {alice_secret}")
    print(f"Bob's shared secret: {bob_secret}")
    
    # Example of encryption and decryption
    message = "Secret message"
    encrypted = dh_encrypt(message, alice_secret)
    decrypted = dh_decrypt(encrypted, bob_secret)
    
    print(f"Original message: {message}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")

if __name__ == "__main__":
    main()