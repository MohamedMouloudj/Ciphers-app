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
- Python-to-C integration using cffi for seamless function calls

## Project Structure

```
cipher-app/
├── cipher_app.py    # Main PyQt5 application
├── ciphers-list.ui  # UI design file created with Qt Designer
├── classical-ciphers # Directory for classical cipher implementations
│   └── [ciphers].c   # C source files for each cipher algorithm
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

3. Optional - Compile your C cipher library into a shared object file (`.so` or `.dll` depending on your OS):
   For Linux/MacOS:
   ```
   gcc -shared -o cipher.so -fPIC ciphers.c
   ```
   For Windows:
   ```
   gcc -shared -o cipher.dll -fPIC ciphers.c
   ```

## Usage

1. Run the application (make sure you are in the project directory):

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
char* cipher_encrypt(const char* input, char* key);

// For decryption
char* cipher_decrypt(const char* input, char* key);
```

### Python-C Integration

The Python application uses cffi to load and call the C functions:

```python
import cffi
ffi = cffi.FFI()
ffi.cdef("""
    char* cipher_encrypt(const char* input, char* key);
    char*int cipher_decrypt(const char* input, char* key);
""")
lib = ffi.dlopen("cipher.so")  # Load the shared library
```

## Extending the Application

### Adding New Ciphers

1. Implement the new cipher algorithm in C, adding functions to `ciphers.c`
2. Update the Python code to include the new cipher in the dropdown menu
3. Add handling for the new cipher's key requirements

## Requirements

- Python 3.6 or higher
- PyQt5
- cffi
- C compiler (gcc, clang, etc.)
