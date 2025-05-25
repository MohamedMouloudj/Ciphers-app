#ifndef AFFINE_H
#define AFFINE_H

#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT __attribute__((visibility("default")))
#endif

// Encrypts plaintext using Affine Cipher and stores result in provided buffer
EXPORT void affine_encrypt(const char* plaintext, int a, int b, char* result);

// Decrypts ciphertext using Affine Cipher and stores result in provided buffer
EXPORT void affine_decrypt(const char* ciphertext, int a, int b, char* result);

#endif
