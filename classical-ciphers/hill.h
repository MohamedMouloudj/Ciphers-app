#ifndef HILL_H
#define HILL_H
#define MODULUS 26
#define MAX_TEXT_LENGTH 1000

// Function to calculate the determinant of a matrix
int determinant(int a, int b, int c, int d);

// Function to calculate the modular multiplicative inverse
int modInverse(int a);

// Function to get adjoint matrix
void adjoint(int keyMatrix[2][2], int adjMatrix[2][2]);

// Function to check if the key matrix is valid for the Hill cipher
int isValidKey(int keyMatrix[2][2]);

// Function to clean and prepare text for encryption/decryption
void prepareTextHill(char *input, char *output);

// Function to encrypt a message using the Hill cipher
void encrypt(char *plaintext, int keyMatrix[2][2], char *ciphertext);

// Function to decrypt a message using the Hill cipher
void decrypt(char *ciphertext, int keyMatrix[2][2], char *plaintext);

// Function to safely get integer input with error handling
int getIntInput();

#endif // HILL_H