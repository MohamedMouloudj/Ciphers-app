#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "affine.h"

#define ALPHABET_SIZE 26

// Extended Euclidean Algorithm to find modular inverse
static int mod_inverse(int a, int m) {
    int m0 = m, t, q;
    int x0 = 0, x1 = 1;

    if (m == 1)
        return 0;

    while (a > 1) {
        q = a / m;
        t = m;

        m = a % m;
        a = t;

        t = x0;
        x0 = x1 - q * x0;
        x1 = t;
    }

    if (x1 < 0)
        x1 += m0;

    return x1;
}

static char encode_char(char c, int a, int b) {
    if (isalpha(c)) {
        char base = isupper(c) ? 'A' : 'a';
        return (char)(((a * (c - base) + b) % ALPHABET_SIZE) + base);
    }
    return c;
}

static char decode_char(char c, int a_inv, int b) {
    if (isalpha(c)) {
        char base = isupper(c) ? 'A' : 'a';
        int x = c - base;
        return (char)(((a_inv * (x - b + ALPHABET_SIZE)) % ALPHABET_SIZE) + base);
    }
    return c;
}

void affine_encrypt(const char* plaintext, int a, int b, char* result) {
    if (!plaintext || !result) return;

    size_t len = strlen(plaintext);
    for (size_t i = 0; i < len; ++i) {
        result[i] = encode_char(plaintext[i], a, b);
    }
    result[len] = '\0';
}

void affine_decrypt(const char* ciphertext, int a, int b, char* result) {
    if (!ciphertext || !result) return;

    int a_inv = mod_inverse(a, ALPHABET_SIZE);
    if (a_inv == 0) {
        result[0] = '\0';  // indicate failure
        return;
    }

    size_t len = strlen(ciphertext);
    for (size_t i = 0; i < len; ++i) {
        result[i] = decode_char(ciphertext[i], a_inv, b);
    }
    result[len] = '\0';
}
