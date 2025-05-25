#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT __attribute__((visibility("default")))
#endif

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include "playfair.h"
#include "caesar.h"
#include "vigenere.h"
#include "substitution.h"
#include "indice_coincidence.h"
#include "Analyse_frequentielle.h"
#include "affine.h"
#include "hill.h"

#define SIZE 5
#define MAX_TEXT_LENGTH 1000
static char result_buffer[1000];

EXPORT const char* handle_cipher_file(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        snprintf(result_buffer, sizeof(result_buffer), "Error: can't open file %s", filename);
        return result_buffer;
    }

    char cipher[64] = {0}, mode[16] = {0}, plain_text[1000] = {0};
    char prv_key[64] = {0}, pub_key[64] = {0};

    char line[1024];
    while (fgets(line, sizeof(line), file)) {
        if (sscanf(line, "cipher: %63s", cipher)) continue;
        if (sscanf(line, "mode: %15s", mode)) continue;
        if (sscanf(line, "plain_text: %999[^\n]", plain_text)) continue;
        if (sscanf(line, "prv_key: %63s", prv_key)) continue;
        if (sscanf(line, "pub_key: %63s", pub_key)) continue;
    }

    fclose(file);

    printf("== Loaded Input ==\n");
    printf("Cipher: %s\n", cipher);
    printf("Mode: %s\n", mode);
    printf("Text: %s\n", plain_text);
    printf("Key: %s\n", prv_key);
    printf("Public Key: %s\n", pub_key);
    printf("===================\n");

    if (strcmp(cipher, "playfair") == 0) {
        char matrix[SIZE][SIZE];
        char result[1000] = {0};
        prepareKey(prv_key, matrix);
        if (strcmp(mode, "encrypt") == 0) {
            prepareText(plain_text);
            encryptPlayfair(plain_text, matrix, result);
        } else {
            decryptPlayfair(plain_text, matrix, result);
        }
        snprintf(result_buffer, sizeof(result_buffer), "%s", result);
        return result_buffer;
    }

    if (strcmp(cipher, "caesar") == 0) {
        int shift = atoi(prv_key);
        if (strcmp(mode, "encrypt") == 0) {
            char* encrypted = chiffrementCesar(plain_text, shift);
            if (encrypted == NULL) {
                snprintf(result_buffer, sizeof(result_buffer), "Error: Caesar encryption returned NULL");
            } else {
                snprintf(result_buffer, sizeof(result_buffer), "%s", encrypted);
                free(encrypted);
            }
        } else {
            char* decrypted = dechiffrementCesar(plain_text, shift);
            if (decrypted == NULL) {
                snprintf(result_buffer, sizeof(result_buffer), "Error: Caesar decryption returned NULL");
            } else {
                snprintf(result_buffer, sizeof(result_buffer), "%s", decrypted);
                free(decrypted);
            }
        }
        return result_buffer;
    }

    if (strcmp(cipher, "vigenere") == 0) {
        char result[1000] = {0};
        if (strcmp(mode, "encrypt") == 0) {
            vigenere_chiffrer(plain_text, prv_key, result);
        } else {
            vigenere_dechiffrer(plain_text, prv_key, result);
        }
        snprintf(result_buffer, sizeof(result_buffer), "%s", result);
        return result_buffer;
    }

    if (strcmp(cipher, "substitution") == 0) {
        char table_originale[ALPHABET_SIZE + 1] = {0};
        char table_substituee[ALPHABET_SIZE + 1] = {0};
        if (strlen(prv_key) == 0) {
            genererTableAleatoire(table_originale, table_substituee);
        } else {
            strcpy(table_substituee, prv_key);
            char alphabet[ALPHABET_SIZE + 1] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
            strcpy(table_originale, alphabet);
        }
        
        printf("Original Table: %s\n", table_originale);
        printf("Substituted Table: %s\n", table_substituee);
        
        char result[1000] = {0};
        if (strcmp(mode, "encrypt") == 0) {
            chiffrer(plain_text, result, table_originale, table_substituee);
        } else {
            dechiffrer(plain_text, result, table_originale, table_substituee);
        }
        snprintf(result_buffer, sizeof(result_buffer), "%s", result);
        return result_buffer;
    }

    if (strcmp(cipher, "Coincidence_index") == 0) {
        double ic = calculer_indice_coincidence(plain_text);
        snprintf(result_buffer, sizeof(result_buffer), "Index of Coincidence: %.6f", ic);
        return result_buffer;
    }
    
    if (strcmp(cipher, "Analyse_frequentielle") == 0) {
        int frequences[ALPHABET_SIZE] = {0};
        int total_lettres = 0;
        analyse_frequentielle(plain_text, frequences, &total_lettres);
        printFrequenciestable(frequences, total_lettres);
        snprintf(result_buffer, sizeof(result_buffer), "Analysis complete. Check console output for frequency table.");
        return result_buffer;
    }

    if (strcmp(cipher,"affine")==0){
        int a, b;
        char result[1000] = {0};
        if (sscanf(prv_key, "%d,%d", &a, &b) != 2) {
            snprintf(result_buffer, sizeof(result_buffer), "Error: Affine key should be in format 'a,b'");
            return result_buffer;
        }
        
        if (strcmp(mode, "encrypt") == 0) {
            affine_encrypt(plain_text, a, b, result);
        } else {
            affine_decrypt(plain_text, a, b, result);
        }
        snprintf(result_buffer, sizeof(result_buffer), "%s", result);
        return result_buffer;
    }

    if (strcmp(cipher, "hill") == 0) {
        int key[2][2];
        char result[1000] = {0};

        // Parse the key from prv_key string (format: "a,b,c,d")
        int values[4];
        int scanned = sscanf(prv_key, "%d,%d,%d,%d", 
                           &values[0], &values[1], 
                           &values[2], &values[3]);

        if (scanned != 4) {
            snprintf(result_buffer, sizeof(result_buffer), 
                    "Error: Hill key should be in format 'a,b,c,d' for 2x2 matrix");
            return result_buffer;
        }

        // Fill the matrix
        key[0][0] = values[0]; key[0][1] = values[1];
        key[1][0] = values[2]; key[1][1] = values[3];

        // Validate the key
        if (!hill_validate_key(key)) {
            snprintf(result_buffer, sizeof(result_buffer), 
                    "Error: Invalid Hill cipher key (determinant must be coprime with 26)");
            return result_buffer;
        }

        // Perform encryption or decryption
        if (strcmp(mode, "encrypt") == 0) {
            if (hill_encrypt(plain_text, key, result) != 0) {
                snprintf(result_buffer, sizeof(result_buffer), "Error during Hill encryption");
                return result_buffer;
            }
        } else {
            if (hill_decrypt(plain_text, key, result) != 0) {
                snprintf(result_buffer, sizeof(result_buffer), "Error during Hill decryption");
                return result_buffer;
            }
        }

        snprintf(result_buffer, sizeof(result_buffer), "%s", result);
        return result_buffer;
    }
    

    snprintf(result_buffer, sizeof(result_buffer), "Unsupported cipher: %s", cipher);
    return result_buffer;
}
