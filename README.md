# Cipher Application

A comprehensive application that provides a graphical user interface built with PyQt5 for accessing various cipher algorithms implemented in C. This project demonstrates the integration of Python UI code with C-based cryptographic implementations.

## Features

- Support for multiple cipher algorithms:
  - Caesar
  - Vigenere
  - Substitution
  - RSA
  - AES
  - DES....
- User-friendly PyQt5 interface for entering plaintext and ciphertext
- Dynamic key input fields that adapt based on the selected cipher
- High-performance cipher implementations in C
- Python-to-C integration using ctypes

## Project Structure

```
cipher-app/
├── cipher_app.py    # Main PyQt5 application
├── ciphers-list.ui  # UI design file created with Qt Designer
├── ciphers.c        # C implementation of cipher algorithms
├── ciphers.h        # Header file for cipher algorithms
├── requirements.txt # Python dependencies
└── README.md        # Project documentation
```

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/MohamedMouloudj/Ciphers-app.git
   cd cipher-app
   ```

2. Install the required Python dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Compile the C cipher library:
   ```
   gcc -shared -o ciphers.so -fPIC ciphers.c
   ```

## Usage

1. Run the application:

   ```
   python cipher_app.py
   ```

2. Select a cipher from the dropdown menu
3. Enter the required key(s) in the provided fields
4. To encrypt: Enter text in the "Encrypt" field and click "Launch"
5. To decrypt: Enter text in the "Decrypt" field and click "Launch"

## Implementation Details

### PyQt5 UI

The UI is built using PyQt5 and Qt Designer. The `ciphers-list.ui` file defines the layout and elements of the interface, which is loaded at runtime by the Python code.

### C Cipher Implementations

The cipher algorithms are implemented in C for optimal performance. The C functions follow this general signature:

```c
// For encryption
int cipher_encrypt(const char* input, char* key, char* output, int output_size);

// For decryption
int cipher_decrypt(const char* input, char* key, char* output, int output_size);
```

### Python-C Integration

The Python application uses ctypes to load and call the C functions:

```python
self.cipher_lib = ctypes.CDLL("./ciphers.so")
result_buffer = ctypes.create_string_buffer(1024)
self.cipher_lib.cipher_function(input.encode('utf-8'), key.encode('utf-8'),
                              result_buffer, ctypes.c_int(len(result_buffer)))
```

## Extending the Application

### Adding New Ciphers

1. Implement the new cipher algorithm in C, adding functions to `ciphers.c`
2. Update the Python code to include the new cipher in the dropdown menu
3. Add handling for the new cipher's key requirements

## Requirements

- Python 3.6 or higher
- PyQt5
- C compiler (gcc, clang, etc.)
