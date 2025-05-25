# RSA Encryption/Decryption Module with Custom Keys
import random
import math

def power(base, expo, m):
    """Fast modular exponentiation"""
    res = 1
    base = base % m
    while expo > 0:
        if expo & 1:
            res = (res * base) % m
        base = (base * base) % m
        expo = expo // 2
    return res

def gcd(a, b):
    """Calculate greatest common divisor"""
    while b != 0:
        a, b = b, a % b
    return a

def modInverse(e, phi):
    """Find modular inverse using Extended Euclidean Algorithm"""
    def extendedGCD(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extendedGCD(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd_val, x, y = extendedGCD(e, phi)
    if gcd_val != 1:
        return -1  # Modular inverse doesn't exist
    return (x % phi + phi) % phi

def isPrime(n, k=5):
    """Miller-Rabin primality test"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as d * 2^r
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Miller-Rabin test
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = power(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = power(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generatePrime(bits=16):
    """Generate a random prime number"""
    while True:
        n = random.getrandbits(bits)
        n |= (1 << bits - 1) | 1  # Set MSB and LSB to 1
        if isPrime(n):
            return n

def validatePrimes(p, q):
    """
    Validate prime numbers p and q
    Returns: (is_valid, error_message)
    """
    # Check if p and q are integers
    if not isinstance(p, int) or not isinstance(q, int):
        return False, "p and q must be integers"
    
    # Check if p and q are positive
    if p <= 1 or q <= 1:
        return False, "p and q must be greater than 1"
    
    # Check if p and q are prime
    if not isPrime(p):
        return False, f"p = {p} is not a prime number"
    
    if not isPrime(q):
        return False, f"q = {q} is not a prime number"
    
    # Check if p and q are different
    if p == q:
        return False, "p and q must be different prime numbers"
    
    # Check if p and q are large enough for practical use
    if p < 11 or q < 11:
        return False, "p and q should be at least 11 for better security"
    
    # Check if n = p*q is large enough to handle ASCII characters
    n = p * q
    if n <= 255:
        return False, f"n = p*q = {n} is too small. Need n > 255 to handle all ASCII characters"
    
    return True, "Valid primes"

def validatePublicExponent(e, phi_n):
    """
    Validate public exponent e
    Returns: (is_valid, error_message)
    """
    # Check if e is an integer
    if not isinstance(e, int):
        return False, "e must be an integer"
    
    # Check range: 1 < e < phi(n)
    if e <= 1:
        return False, "e must be greater than 1"
    
    if e >= phi_n:
        return False, f"e must be less than phi(n) = {phi_n}"
    
    # Check if gcd(e, phi(n)) = 1
    if gcd(e, phi_n) != 1:
        return False, f"gcd(e, phi(n)) must be 1. Current gcd({e}, {phi_n}) = {gcd(e, phi_n)}"
    
    # Common good choices for e
    common_e_values = [3, 17, 257, 65537]
    if e in common_e_values:
        return True, f"Valid public exponent (common secure choice: {e})"
    
    return True, "Valid public exponent"

def validatePrivateExponent(d, e, phi_n):
    """
    Validate private exponent d
    Returns: (is_valid, error_message)
    """
    # Check if d is an integer
    if not isinstance(d, int):
        return False, "d must be an integer"
    
    # Check range: 1 < d < phi(n)
    if d <= 1:
        return False, "d must be greater than 1"
    
    if d >= phi_n:
        return False, f"d must be less than phi(n) = {phi_n}"
    
    # Check if e*d ≡ 1 (mod phi(n))
    if (e * d) % phi_n != 1:
        return False, f"e*d must be congruent to 1 modulo phi(n). Current: ({e}*{d}) mod {phi_n} = {(e * d) % phi_n}"
    
    return True, "Valid private exponent"

def validateKeySet(p, q, e, d=None):
    """
    Validate complete RSA key set
    Returns: (is_valid, error_messages_list, computed_values)
    """
    errors = []
    computed = {}
    
    # Validate primes
    p_valid, p_msg = validatePrimes(p, q)
    if not p_valid:
        errors.append(p_msg)
        return False, errors, computed
    
    # Compute derived values
    n = p * q
    phi_n = (p - 1) * (q - 1)
    computed['n'] = n
    computed['phi_n'] = phi_n
    
    # Validate public exponent
    e_valid, e_msg = validatePublicExponent(e, phi_n)
    if not e_valid:
        errors.append(e_msg)
        return False, errors, computed
    
    # If d is provided, validate it; otherwise compute it
    if d is not None:
        d_valid, d_msg = validatePrivateExponent(d, e, phi_n)
        if not d_valid:
            errors.append(d_msg)
            return False, errors, computed
        computed['d'] = d
    else:
        computed_d = modInverse(e, phi_n)
        if computed_d == -1:
            errors.append(f"Cannot compute private exponent d for given e = {e}")
            return False, errors, computed
        computed['d'] = computed_d
    
    return True, ["All parameters are valid"], computed

def generateKeys():
    """Generate RSA key pair with random primes"""
    p = generatePrime(16)
    q = generatePrime(16)
    while p == q:
        q = generatePrime(16)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose e
    e = 65537  # Common choice
    if gcd(e, phi) != 1:
        e = 3
        while gcd(e, phi) != 1:
            e += 2
    
    # Compute d
    d = modInverse(e, phi)
    if d == -1:
        return generateKeys()  # Retry
    
    return e, d, n, p, q

def stringToNumbers(message):
    """Convert string message to list of numbers"""
    return [ord(char) for char in message]

def numbersToString(numbers):
    """Convert list of numbers back to string"""
    try:
        return ''.join([chr(num) for num in numbers])
    except ValueError:
        return "Error: Invalid character codes"

def encryptNumber(m, e, n):
    """Encrypt a single number"""
    return power(m, e, n)

def decryptNumber(c, d, n):
    """Decrypt a single number"""
    return power(c, d, n)

# Global variables to store keys
_custom_keys = None
_generated_keys = None

def setCustomKeys(p, q, e, d=None):
    """
    Set custom RSA keys
    Args:
        p, q: Prime numbers
        e: Public exponent
        d: Private exponent (optional, will be computed if not provided)
    Returns: (success, message, key_info)
    """
    global _custom_keys
    
    is_valid, messages, computed = validateKeySet(p, q, e, d)
    
    if is_valid:
        _custom_keys = {
            'p': p,
            'q': q,
            'e': e,
            'd': computed['d'],
            'n': computed['n'],
            'phi_n': computed['phi_n']
        }
        return True, "Custom keys set successfully", _custom_keys
    else:
        return False, "; ".join(messages), None

def useGeneratedKeys():
    """Switch to using automatically generated keys"""
    global _generated_keys
    if _generated_keys is None:
        e, d, n, p, q = generateKeys()
        _generated_keys = {
            'p': p,
            'q': q,
            'e': e,
            'd': d,
            'n': n,
            'phi_n': (p-1)*(q-1)
        }
    return _generated_keys

def getCurrentKeys():
    """Get currently active keys"""
    if _custom_keys is not None:
        return _custom_keys
    else:
        return useGeneratedKeys()

def encrypt(message, use_custom_keys=True):
    """
    Encrypt a string message using RSA
    Args:
        message: String to encrypt
        use_custom_keys: If True, uses custom keys; if False, uses generated keys
    Returns: tuple (encrypted_numbers, public_key_info)
    """
    if not isinstance(message, str):
        raise ValueError("Message must be a string")
    
    # Get appropriate keys
    if use_custom_keys and _custom_keys is not None:
        keys = _custom_keys
    else:
        keys = useGeneratedKeys()
    
    e, n = keys['e'], keys['n']
    numbers = stringToNumbers(message)
    
    # Check if all characters can be encrypted
    for i, num in enumerate(numbers):
        if num >= n:
            raise ValueError(f"Character '{message[i]}' (code {num}) is too large for key size (n={n})")
    
    # Encrypt each character
    encrypted_numbers = [encryptNumber(num, e, n) for num in numbers]
    
    return encrypted_numbers, (e, n)

def decrypt(encrypted_numbers, use_custom_keys=True):
    """
    Decrypt encrypted numbers back to string message
    Args:
        encrypted_numbers: List of encrypted numbers
        use_custom_keys: If True, uses custom keys; if False, uses generated keys
    Returns: decrypted string message
    """
    if not isinstance(encrypted_numbers, list):
        raise ValueError("Encrypted data must be a list of numbers")
    
    # Get appropriate keys
    if use_custom_keys and _custom_keys is not None:
        keys = _custom_keys
    else:
        keys = useGeneratedKeys()
    
    d, n = keys['d'], keys['n']
    
    # Decrypt each number
    decrypted_numbers = [decryptNumber(num, d, n) for num in encrypted_numbers]
    
    return numbersToString(decrypted_numbers)

def getKeyValidationConditions():
    """
    Return the conditions that RSA keys must satisfy
    """
    return {
        "Prime conditions": [
            "p and q must be integers",
            "p and q must be greater than 1",
            "p and q must be prime numbers",
            "p and q must be different from each other",
            "p and q should be at least 11 for basic security",
            "n = p*q must be greater than 255 to handle all ASCII characters"
        ],
        "Public exponent (e) conditions": [
            "e must be an integer",
            "1 < e < phi(n), where phi(n) = (p-1)*(q-1)",
            "gcd(e, phi(n)) must equal 1",
            "Common secure choices: 3, 17, 257, 65537"
        ],
        "Private exponent (d) conditions": [
            "d must be an integer",
            "1 < d < phi(n)",
            "e*d ≡ 1 (mod phi(n)) - this means (e*d) mod phi(n) = 1"
        ],
        "Security recommendations": [
            "Use primes with at least 512 bits for real applications",
            "Ensure p and q are similar in size but not too close",
            "Use well-tested values for e like 65537",
            "Keep private key components (d, p, q) secret"
        ]
    }

# Example usage and testing
if __name__ == "__main__":
    print("=== RSA Key Validation Conditions ===")
    conditions = getKeyValidationConditions()
    for category, rules in conditions.items():
        print(f"\n{category}:")
        for rule in rules:
            print(f"  • {rule}")
    
    print("\n=== Testing Custom Keys ===")
    
    # Test with small primes (should work for demo)
    p, q, e = 61, 53, 17
    success, msg, keys = setCustomKeys(p, q, e)
    print(f"Setting keys p={p}, q={q}, e={e}")
    print(f"Result: {msg}")
    
    if success:
        print(f"Computed values: n={keys['n']}, d={keys['d']}, phi(n)={keys['phi_n']}")
        
        # Test encryption/decryption
        test_message = "Hello!"
        print(f"\nTesting with message: '{test_message}'")
        
        try:
            encrypted_data, public_key = encrypt(test_message)
            print(f"Encrypted: {encrypted_data}")
            
            decrypted_message = decrypt(encrypted_data)
            print(f"Decrypted: '{decrypted_message}'")
            print(f"Success: {test_message == decrypted_message}")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n=== Testing Invalid Keys ===")
    # Test with invalid keys
    invalid_cases = [
        (4, 7, 5),    # p=4 is not prime
        (7, 7, 5),    # p=q (same primes)
        (7, 11, 77),  # e >= phi(n)
        (7, 11, 6),   # gcd(e, phi(n)) != 1
    ]
    
    for p, q, e in invalid_cases:
        success, msg, _ = setCustomKeys(p, q, e)
        print(f"Keys p={p}, q={q}, e={e}: {msg}")