#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MODULUS 26
#define MAX_TEXT_LENGTH 1000

// Function to calculate the determinant of a matrix
int determinant(int a, int b, int c, int d) {
    return (a * d - b * c);
}

// Function to calculate the modular multiplicative inverse
int modInverse(int a) {
    for (int i = 0; i < MODULUS; i++) {
        if ((a * i) % MODULUS == 1)
            return i;
    }
    return -1; // No inverse exists
}

// Function to get adjoint matrix
void adjoint(int keyMatrix[2][2], int adjMatrix[2][2]) {
    // Swap a and d, negate b and c
    adjMatrix[0][0] = keyMatrix[1][1];
    adjMatrix[1][1] = keyMatrix[0][0];
    adjMatrix[0][1] = -keyMatrix[0][1];
    adjMatrix[1][0] = -keyMatrix[1][0];
    
    // Ensure all values are positive
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            adjMatrix[i][j] = (adjMatrix[i][j] % MODULUS + MODULUS) % MODULUS;
        }
    }
}

// Function to check if the key matrix is valid for the Hill cipher
int isValidKey(int keyMatrix[2][2]) {
    int det = determinant(keyMatrix[0][0], keyMatrix[0][1], keyMatrix[1][0], keyMatrix[1][1]);
    det = (det % MODULUS + MODULUS) % MODULUS; // Ensure positive value
    
    // Check if determinant has an inverse
    return (modInverse(det) != -1);
}

// Function to clean and prepare text for encryption/decryption
void prepareText(char *input, char *output) {
    int j = 0;
    for (int i = 0; input[i] != '\0'; i++) {
        if (isalpha(input[i])) {
            output[j++] = toupper(input[i]);
        }
    }
    output[j] = '\0';
    
    // Ensure length is even by padding with 'X' if necessary
    int len = strlen(output);
    if (len % 2 != 0) {
        output[len] = 'X';
        output[len + 1] = '\0';
    }
}

// Function to encrypt a message using the Hill cipher
void encrypt(char *plaintext, int keyMatrix[2][2], char *ciphertext) {
    int len = strlen(plaintext);
    int pos = 0;
    
    // Process pairs of characters
    for (int i = 0; i < len; i += 2) {
        // If the length is odd, append 'X' for the last character
        if (i + 1 >= len) {
            plaintext[i + 1] = 'X';
            len++;
        }
        
        // Convert letters to numbers (0-25)
        int p1 = toupper(plaintext[i]) - 'A';
        int p2 = toupper(plaintext[i + 1]) - 'A';
        
        // Apply the Hill cipher formula
        int c1 = (keyMatrix[0][0] * p1 + keyMatrix[0][1] * p2) % MODULUS;
        int c2 = (keyMatrix[1][0] * p1 + keyMatrix[1][1] * p2) % MODULUS;
        
        // Convert back to letters
        ciphertext[pos++] = c1 + 'A';
        ciphertext[pos++] = c2 + 'A';
    }
    
    ciphertext[pos] = '\0';
}

// Function to decrypt a message using the Hill cipher
void decrypt(char *ciphertext, int keyMatrix[2][2], char *plaintext) {
    int len = strlen(ciphertext);
    int pos = 0;
    
    // Calculate the determinant and its modular inverse
    int det = determinant(keyMatrix[0][0], keyMatrix[0][1], keyMatrix[1][0], keyMatrix[1][1]);
    det = (det % MODULUS + MODULUS) % MODULUS; // Ensure positive value
    int detInverse = modInverse(det);
    
    // Calculate the inverse key matrix
    int inverseMatrix[2][2];
    int adjMatrix[2][2];
    adjoint(keyMatrix, adjMatrix);
    
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            inverseMatrix[i][j] = (detInverse * adjMatrix[i][j]) % MODULUS;
        }
    }
    
    // Process pairs of characters
    for (int i = 0; i < len; i += 2) {
        // Convert letters to numbers (0-25)
        int c1 = toupper(ciphertext[i]) - 'A';
        int c2 = toupper(ciphertext[i + 1]) - 'A';
        
        // Apply the inverse formula
        int p1 = (inverseMatrix[0][0] * c1 + inverseMatrix[0][1] * c2) % MODULUS;
        int p2 = (inverseMatrix[1][0] * c1 + inverseMatrix[1][1] * c2) % MODULUS;
        
        // Convert back to letters
        plaintext[pos++] = p1 + 'A';
        plaintext[pos++] = p2 + 'A';
    }
    
    plaintext[pos] = '\0';
}

// Function to safely get integer input with error handling
int getIntInput() {
    char buffer[100];
    int value;
    int valid = 0;
    
    while (!valid) {
        if (fgets(buffer, sizeof(buffer), stdin) == NULL) {
            printf("Error reading input. Please try again: ");
            continue;
        }
        
        // Check if input is a valid integer
        if (sscanf(buffer, "%d", &value) != 1) {
            printf("Invalid input. Please enter a number (0-25): ");
            continue;
        }
        
        valid = 1;
    }
    
    return value;
}

// Main function with enhanced user interface and robust input handling
int main() {
    int keyMatrix[2][2];
    char input[MAX_TEXT_LENGTH], processed[MAX_TEXT_LENGTH], result[MAX_TEXT_LENGTH];
    int choice;
    int validKey = 0;
    
    printf("======================================\n");
    printf("        HILL CIPHER ALGORITHM         \n");
    printf("======================================\n\n");
    
    // Keep asking for key matrix until a valid one is provided
    while (!validKey) {
        printf("Enter the 2x2 key matrix values (0-25):\n");
        
        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 2; j++) {
                printf("Enter element [%d][%d]: ", i, j);
                keyMatrix[i][j] = getIntInput();
                
                // Ensure values are within valid range
                keyMatrix[i][j] = keyMatrix[i][j] % MODULUS;
                if (keyMatrix[i][j] < 0) {
                    keyMatrix[i][j] += MODULUS;
                }
            }
        }
        
        // Check if the key is valid
        if (!isValidKey(keyMatrix)) {
            printf("\nERROR: The key matrix is not invertible. Choose a different key.\n");
            printf("Hint: The determinant must have a modular inverse modulo 26.\n\n");
            printf("Let's try again with a different key matrix.\n\n");
        } else {
            validKey = 1;
        }
    }
    
    // Display the key matrix
    printf("\nYour key matrix is:\n");
    for (int i = 0; i < 2; i++) {
        printf("[ ");
        for (int j = 0; j < 2; j++) {
            printf("%2d ", keyMatrix[i][j]);
        }
        printf("]\n");
    }
    
    // Menu for operation choice
    do {
        printf("\n======================================\n");
        printf("Choose an operation:\n");
        printf("1. Encrypt a message\n");
        printf("2. Decrypt a message\n");
        printf("3. Exit\n");
        printf("Enter your choice (1-3): ");
        
        int validChoice = 0;
        while (!validChoice) {
            if (scanf("%d", &choice) != 1) {
                printf("Invalid input. Please enter a number (1-3): ");
                while (getchar() != '\n'); // Clear input buffer
                continue;
            }
            validChoice = 1;
        }
        
        while (getchar() != '\n'); // Clear input buffer
        
        switch (choice) {
            case 1: // Encryption
                printf("\n=== ENCRYPTION ===\n");
                printf("Enter the message to encrypt: ");
                fgets(input, MAX_TEXT_LENGTH, stdin);
                input[strcspn(input, "\n")] = 0; // Remove newline
                
                prepareText(input, processed);
                
                if (strlen(processed) == 0) {
                    printf("\nWarning: No valid alphabetic characters found in the input.\n");
                    break;
                }
                
                printf("\nProcessed input (uppercase, no spaces): %s\n", processed);
                
                encrypt(processed, keyMatrix, result);
                
                printf("Encrypted message: %s\n", result);
                break;
                
            case 2: // Decryption
                printf("\n=== DECRYPTION ===\n");
                printf("Enter the message to decrypt (uppercase letters only): ");
                fgets(input, MAX_TEXT_LENGTH, stdin);
                input[strcspn(input, "\n")] = 0; // Remove newline
                
                prepareText(input, processed);
                
                if (strlen(processed) == 0) {
                    printf("\nWarning: No valid alphabetic characters found in the input.\n");
                    break;
                }
                
                printf("\nProcessed input: %s\n", processed);
                
                decrypt(processed, keyMatrix, result);
                
                printf("Decrypted message: %s\n", result);
                break;
                
            case 3: // Exit
                printf("\nExiting program. Goodbye!\n");
                break;
                
            default:
                printf("\nInvalid choice. Please enter a number between 1 and 3.\n");
        }
    } while (choice != 3);
    
    return 0;
}