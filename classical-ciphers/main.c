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

#define SIZE 5
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

    snprintf(result_buffer, sizeof(result_buffer), "Unsupported cipher: %s", cipher);
    return result_buffer;
}
