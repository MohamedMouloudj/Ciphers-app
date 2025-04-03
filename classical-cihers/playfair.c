/**
 * Playfair Cipher Implementation in C
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define SIZE 5
#define ALPHABET_SIZE 26

// Function prototypes
void prepareKey(char *key, char matrix[SIZE][SIZE]);
void prepareText(char *text);
void encrypt(char *text, char matrix[SIZE][SIZE], char *result);
void decrypt(char *text, char matrix[SIZE][SIZE], char *result);
void findPosition(char matrix[SIZE][SIZE], char ch, int *row, int *col);
void displayMatrix(char matrix[SIZE][SIZE]);

int main() {
    char key[100], text[1000], result[1000];
    char matrix[SIZE][SIZE];
    int choice;
    
    printf("Playfair Cipher Implementation\n");
    
    printf("Enter the key: ");
    fgets(key, sizeof(key), stdin);
    key[strcspn(key, "\n")] = '\0';  // Remove newline
    
    prepareKey(key, matrix);
    
    printf("\nGenerated Playfair Matrix:\n");
    displayMatrix(matrix);
    
    printf("\nEnter 1 for Encryption, 2 for Decryption: ");
    scanf("%d", &choice);
    getchar();  // Consume newline
    
    printf("Enter the text: ");
    fgets(text, sizeof(text), stdin);
    text[strcspn(text, "\n")] = '\0';  // Remove newline
    
    // Convert text to uppercase
    for (int i = 0; text[i]; i++) {
        text[i] = toupper(text[i]);
    }
    
    prepareText(text);
    
    if (choice == 1) {
        encrypt(text, matrix, result);
        printf("\nEncrypted text: %s\n", result);
    } else if (choice == 2) {
        decrypt(text, matrix, result);
        printf("\nDecrypted text: %s\n", result);
    } else {
        printf("\nInvalid choice!\n");
    }
    
    return 0;
}

// Prepare the key matrix for Playfair cipher
void prepareKey(char *key, char matrix[SIZE][SIZE]) {
    // Convert key to uppercase
    for (int i = 0; key[i]; i++) {
        key[i] = toupper(key[i]);
    }
    char used[ALPHABET_SIZE] = {0};
    int i, j, k = 0;
    
    // Mark J as used (we'll replace J with I in the implementation)
    used['J' - 'A'] = 1;
    
    // Fill the matrix with the key
    for (i = 0; i < SIZE; i++) {
        for (j = 0; j < SIZE; j++) {
            if (key[k]) {
                // Skip non-alphabetic characters
                while (key[k] && !isalpha(key[k])) {
                    k++;
                }
                
                if (!key[k]) break;
                
                char ch = key[k++];
                if (ch == 'J') ch = 'I';  // Replace J with I
                
                // If character not already used, add to matrix
                if (!used[ch - 'A']) {
                    matrix[i][j] = ch;
                    used[ch - 'A'] = 1;
                } else {
                    j--;
                }
            } else {
                break;
            }
        }
        
        if (!key[k] && i < SIZE) break;
    }
    
    // Fill the rest of the matrix with remaining letters
    for (char ch = 'A'; ch <= 'Z'; ch++) {
        if (!used[ch - 'A'] && ch != 'J') {
            if (i < SIZE) {
                matrix[i][j++] = ch;
                if (j == SIZE) {
                    i++;
                    j = 0;
                }
            }
        }
    }
}

// Prepare the plaintext according to Playfair cipher rules
void prepareText(char *text) {
    int len = strlen(text);
    int i, j = 0;
    char temp[2000];
    
    // Remove non-alphabetic characters and replace J with I
    for (i = 0; i < len; i++) {
        if (isalpha(text[i])) {
            temp[j++] = (text[i] == 'J') ? 'I' : text[i];
        }
    }
    temp[j] = '\0';
    
    // Insert X between same letter pairs and ensure even length
    j = 0;
    for (i = 0; i < strlen(temp); i++) {
        text[j++] = temp[i];
        if (i < strlen(temp) - 1 && temp[i] == temp[i + 1]) {
            text[j++] = 'X';
        }
    }
    
    // Add an X if the length is odd
    if (j % 2 != 0) {
        text[j++] = 'X';
    }
    
    text[j] = '\0';
}

// Find the position of a character in the matrix
void findPosition(char matrix[SIZE][SIZE], char ch, int *row, int *col) {
    if (ch == 'J') ch = 'I';  // Replace J with I
    
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            if (matrix[i][j] == ch) {
                *row = i;
                *col = j;
                return;
            }
        }
    }
}

// Encrypt the plaintext using Playfair cipher
void encrypt(char *text, char matrix[SIZE][SIZE], char *result) {
    int len = strlen(text);
    int row1, col1, row2, col2;
    int k = 0;
    
    for (int i = 0; i < len; i += 2) {
        findPosition(matrix, text[i], &row1, &col1);
        findPosition(matrix, text[i + 1], &row2, &col2);
        
        if (row1 == row2) {  // Same row
            result[k++] = matrix[row1][(col1 + 1) % SIZE];
            result[k++] = matrix[row2][(col2 + 1) % SIZE];
        } else if (col1 == col2) {  // Same column
            result[k++] = matrix[(row1 + 1) % SIZE][col1];
            result[k++] = matrix[(row2 + 1) % SIZE][col2];
        } else {  // Rectangle case
            result[k++] = matrix[row1][col2];
            result[k++] = matrix[row2][col1];
        }
    }
    
    result[k] = '\0';
}

// Decrypt the ciphertext using Playfair cipher
void decrypt(char *text, char matrix[SIZE][SIZE], char *result) {
    int len = strlen(text);
    int row1, col1, row2, col2;
    int k = 0;
    
    for (int i = 0; i < len; i += 2) {
        findPosition(matrix, text[i], &row1, &col1);
        findPosition(matrix, text[i + 1], &row2, &col2);
        
        if (row1 == row2) {  // Same row
            result[k++] = matrix[row1][(col1 - 1 + SIZE) % SIZE];
            result[k++] = matrix[row2][(col2 - 1 + SIZE) % SIZE];
        } else if (col1 == col2) {  // Same column
            result[k++] = matrix[(row1 - 1 + SIZE) % SIZE][col1];
            result[k++] = matrix[(row2 - 1 + SIZE) % SIZE][col2];
        } else {  // Rectangle case
            result[k++] = matrix[row1][col2];
            result[k++] = matrix[row2][col1];
        }
    }
    
    result[k] = '\0';
}

// Display the Playfair matrix
void displayMatrix(char matrix[SIZE][SIZE]) {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            printf("%c ", matrix[i][j]);
        }
        printf("\n");
    }
}