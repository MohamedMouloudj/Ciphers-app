#ifndef HILL_H
#define HILL_H
#define MODULUS 26
#define MAX_TEXT_LENGTH 1000

// Main functions
int hill_encrypt(const char *plaintext, int keyMatrix[2][2], char *ciphertext);
int hill_decrypt(const char *ciphertext, int keyMatrix[2][2], char *plaintext);

// Utility functions
int hill_validate_key(int keyMatrix[2][2]);
void hill_get_key_requirements(char *buffer, int bufferSize);

#endif