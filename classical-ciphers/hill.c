// hill.c - Hill Cipher Implementation
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "hill.h"

#define MODULUS 26
#define MAX_TEXT_LENGTH 1000

// Internal helper functions
static int determinant(int a, int b, int c, int d) {
    return (a * d - b * c);
}

static int modInverse(int a) {
    a = (a % MODULUS + MODULUS) % MODULUS;
    for (int i = 1; i < MODULUS; i++) {
        if ((a * i) % MODULUS == 1)
            return i;
    }
    return -1; // No inverse exists
}

static void adjoint(int keyMatrix[2][2], int adjMatrix[2][2]) {
    // For 2x2 matrix: adjoint swaps diagonal elements and negates off-diagonal
    adjMatrix[0][0] = keyMatrix[1][1];
    adjMatrix[1][1] = keyMatrix[0][0];
    adjMatrix[0][1] = -keyMatrix[0][1];
    adjMatrix[1][0] = -keyMatrix[1][0];
    
    // Ensure all values are positive in mod 26
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            adjMatrix[i][j] = (adjMatrix[i][j] % MODULUS + MODULUS) % MODULUS;
        }
    }
}

static int isValidKey(int keyMatrix[2][2]) {
    int det = determinant(keyMatrix[0][0], keyMatrix[0][1], keyMatrix[1][0], keyMatrix[1][1]);
    det = (det % MODULUS + MODULUS) % MODULUS;
    return (modInverse(det) != -1);
}

static void prepareText(const char *input, char *output) {
    int j = 0;
    for (int i = 0; input[i] != '\0'; i++) {
        if (isalpha(input[i])) {
            output[j++] = toupper(input[i]);
        }
    }
    output[j] = '\0';
    
    // Pad with 'X' if odd length
    int len = strlen(output);
    if (len % 2 != 0) {
        output[len] = 'X';
        output[len + 1] = '\0';
    }
}

// Exportable Functions

/**
 * Encrypt text using Hill cipher
 * @param plaintext: Input text to encrypt
 * @param keyMatrix: 2x2 key matrix (values 0-25)
 * @param ciphertext: Output buffer (must be allocated by caller)
 * @return: 0 on success, -1 on error
 */
int hill_encrypt(const char *plaintext, int keyMatrix[2][2], char *ciphertext) {
    if (!plaintext || !keyMatrix || !ciphertext) {
        return -1; // Invalid parameters
    }
    
    // Validate key matrix
    if (!isValidKey(keyMatrix)) {
        return -1; // Invalid key matrix (determinant has no inverse)
    }
    
    // Prepare text (remove non-alphabetic, convert to uppercase, pad if needed)
    char prepared[MAX_TEXT_LENGTH];
    prepareText(plaintext, prepared);
    
    int len = strlen(prepared);
    if (len == 0) {
        ciphertext[0] = '\0';
        return 0;
    }
    
    int pos = 0;
    
    // Process pairs of characters
    for (int i = 0; i < len; i += 2) {
        // Convert letters to numbers (0-25)
        int p1 = prepared[i] - 'A';
        int p2 = prepared[i + 1] - 'A';
        
        // Apply Hill cipher matrix multiplication
        int c1 = (keyMatrix[0][0] * p1 + keyMatrix[0][1] * p2) % MODULUS;
        int c2 = (keyMatrix[1][0] * p1 + keyMatrix[1][1] * p2) % MODULUS;
        
        // Ensure positive values
        c1 = (c1 + MODULUS) % MODULUS;
        c2 = (c2 + MODULUS) % MODULUS;
        
        // Convert back to letters
        ciphertext[pos++] = c1 + 'A';
        ciphertext[pos++] = c2 + 'A';
    }
    
    ciphertext[pos] = '\0';
    return 0;
}

/**
 * Decrypt text using Hill cipher
 * @param ciphertext: Input text to decrypt
 * @param keyMatrix: 2x2 key matrix (values 0-25)
 * @param plaintext: Output buffer (must be allocated by caller)
 * @return: 0 on success, -1 on error
 */
int hill_decrypt(const char *ciphertext, int keyMatrix[2][2], char *plaintext) {
    if (!ciphertext || !keyMatrix || !plaintext) {
        return -1; // Invalid parameters
    }
    
    // Validate key matrix
    if (!isValidKey(keyMatrix)) {
        return -1; // Invalid key matrix
    }
    
    // Prepare text
    char prepared[MAX_TEXT_LENGTH];
    prepareText(ciphertext, prepared);
    
    int len = strlen(prepared);
    if (len == 0) {
        plaintext[0] = '\0';
        return 0;
    }
    
    // Calculate determinant and its modular inverse
    int det = determinant(keyMatrix[0][0], keyMatrix[0][1], keyMatrix[1][0], keyMatrix[1][1]);
    det = (det % MODULUS + MODULUS) % MODULUS;
    int detInverse = modInverse(det);
    
    if (detInverse == -1) {
        return -1; // Cannot decrypt - no inverse exists
    }
    
    // Calculate inverse key matrix
    int adjMatrix[2][2];
    int inverseMatrix[2][2];
    
    adjoint(keyMatrix, adjMatrix);
    
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            inverseMatrix[i][j] = (detInverse * adjMatrix[i][j]) % MODULUS;
            inverseMatrix[i][j] = (inverseMatrix[i][j] + MODULUS) % MODULUS;
        }
    }
    
    int pos = 0;
    
    // Process pairs of characters
    for (int i = 0; i < len; i += 2) {
        // Convert letters to numbers (0-25)
        int c1 = prepared[i] - 'A';
        int c2 = prepared[i + 1] - 'A';
        
        // Apply inverse matrix multiplication
        int p1 = (inverseMatrix[0][0] * c1 + inverseMatrix[0][1] * c2) % MODULUS;
        int p2 = (inverseMatrix[1][0] * c1 + inverseMatrix[1][1] * c2) % MODULUS;
        
        // Ensure positive values
        p1 = (p1 + MODULUS) % MODULUS;
        p2 = (p2 + MODULUS) % MODULUS;
        
        // Convert back to letters
        plaintext[pos++] = p1 + 'A';
        plaintext[pos++] = p2 + 'A';
    }
    
    plaintext[pos] = '\0';
    return 0;
}

/**
 * Validate Hill cipher key matrix
 * @param keyMatrix: 2x2 key matrix to validate
 * @return: 1 if valid, 0 if invalid
 */
int hill_validate_key(int keyMatrix[2][2]) {
    if (!keyMatrix) return 0;
    
    // Check if all values are within valid range (0-25)
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            if (keyMatrix[i][j] < 0 || keyMatrix[i][j] >= MODULUS) {
                return 0;
            }
        }
    }
    
    return isValidKey(keyMatrix);
}

/**
 * Get key validation requirements as a string
 * @param buffer: Output buffer for requirements (must be allocated by caller)
 * @param bufferSize: Size of the output buffer
 */
void hill_get_key_requirements(char *buffer, int bufferSize) {
    if (!buffer || bufferSize < 200) return;
    
    snprintf(buffer, bufferSize,
        "Hill Cipher Key Requirements:\n"
        "- 2x2 matrix with integer values\n"
        "- All values must be between 0-25\n"
        "- Matrix determinant must be coprime to 26\n"
        "- Common valid determinants: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25\n"
        "- Example valid key: [[3,2],[5,7]] (det=11)");
}

//Example usage and testing 
// int main() {
//     // Test key matrix (determinant = 3*7 - 2*5 = 11, which is coprime to 26)
//     int key[2][2] = {{3, 2}, {5, 7}};
    
//     char plaintext[] = "HELLO ";
//     char ciphertext[MAX_TEXT_LENGTH];
//     char decrypted[MAX_TEXT_LENGTH];
    
//     printf("Original: %s\n", plaintext);
    
//     // Test encryption
//     if (hill_encrypt(plaintext, key, ciphertext) == 0) {
//         printf("Encrypted: %s\n", ciphertext);
        
//         // Test decryption
//         if (hill_decrypt(ciphertext, key, decrypted) == 0) {
//             printf("Decrypted: %s\n", decrypted);
//         } else {
//             printf("Decryption failed!\n");
//         }
//     } else {
//         printf("Encryption failed!\n");
//     }
    
//     // Test key validation
//     printf("Key valid: %s\n", hill_validate_key(key) ? "Yes" : "No");
    
//     char requirements[500];
//     hill_get_key_requirements(requirements, sizeof(requirements));
//     printf("\n%s\n", requirements);
    
//     return 0;
// }