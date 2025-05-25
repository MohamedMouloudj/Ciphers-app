#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "sha256.h"

// SHA-256 constants
static const uint32_t k[] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
};

// SHA-256 macros
#define ROTRIGHT(word, bits) (((word) >> (bits)) | ((word) << (32-(bits))))
#define CH(x, y, z) (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x, y, z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define EP0(x) (ROTRIGHT(x, 2) ^ ROTRIGHT(x, 13) ^ ROTRIGHT(x, 22))
#define EP1(x) (ROTRIGHT(x, 6) ^ ROTRIGHT(x, 11) ^ ROTRIGHT(x, 25))
#define SIG0(x) (ROTRIGHT(x, 7) ^ ROTRIGHT(x, 18) ^ ((x) >> 3))
#define SIG1(x) (ROTRIGHT(x, 17) ^ ROTRIGHT(x, 19) ^ ((x) >> 10))

void to_bytes_sha256(uint32_t val, uint8_t *bytes) {
    bytes[0] = (uint8_t)(val >> 24);
    bytes[1] = (uint8_t)(val >> 16);
    bytes[2] = (uint8_t)(val >> 8);
    bytes[3] = (uint8_t)val;
}

uint32_t to_uint32_sha256(const uint8_t *bytes) {
    return ((uint32_t)bytes[0] << 24) | 
           ((uint32_t)bytes[1] << 16) | 
           ((uint32_t)bytes[2] << 8) | 
           ((uint32_t)bytes[3]);
}

void sha256_hash_to_hex(const uint8_t *hash, char *hex_output) {
    for (int i = 0; i < 32; i++) {
        sprintf(hex_output + (i * 2), "%02x", hash[i]);
    }
    hex_output[64] = '\0';
}

int sha256_compare_hashes(const uint8_t *hash1, const uint8_t *hash2) {
    return memcmp(hash1, hash2, 32);
}

int sha256_decrypt(const uint8_t *hash_input, size_t hash_len, uint8_t *output_data) {
    // SHA-256 is a one-way hash function and cannot be decrypted
    return -1;
}

void sha256_encrypt(const uint8_t *input_data, size_t input_len, uint8_t *output_hash) {
    // Initialize hash values (first 32 bits of the fractional parts of the square roots of the first 8 primes 2..19)
    uint32_t h0 = 0x6a09e667;
    uint32_t h1 = 0xbb67ae85;
    uint32_t h2 = 0x3c6ef372;
    uint32_t h3 = 0xa54ff53a;
    uint32_t h4 = 0x510e527f;
    uint32_t h5 = 0x9b05688c;
    uint32_t h6 = 0x1f83d9ab;
    uint32_t h7 = 0x5be0cd19;

    // Pre-processing: adding padding bits
    size_t padded_len;
    for (padded_len = input_len + 1; padded_len % 64 != 56; padded_len++);
    padded_len += 8;
    
    uint8_t *msg = malloc(padded_len);
    if (!msg) return;
    
    // Copy original message
    memcpy(msg, input_data, input_len);
    
    // Append the '1' bit (plus zero padding to make it a byte)
    msg[input_len] = 0x80;
    
    // Append zeros
    for (size_t i = input_len + 1; i < padded_len - 8; i++) {
        msg[i] = 0;
    }
    
    // Append original length in bits as 64-bit big-endian integer
    uint64_t bit_len = input_len * 8;
    for (int i = 0; i < 8; i++) {
        msg[padded_len - 8 + i] = (bit_len >> (56 - i * 8)) & 0xFF;
    }
    
    // Process the message in successive 512-bit chunks
    for (size_t chunk = 0; chunk < padded_len; chunk += 64) {
        uint32_t w[64];
        
        // Break chunk into sixteen 32-bit big-endian words
        for (int i = 0; i < 16; i++) {
            w[i] = ((uint32_t)msg[chunk + i * 4] << 24) |
                   ((uint32_t)msg[chunk + i * 4 + 1] << 16) |
                   ((uint32_t)msg[chunk + i * 4 + 2] << 8) |
                   ((uint32_t)msg[chunk + i * 4 + 3]);
        }
        
        // Extend the first 16 words into the remaining 48 words w[16..63]
        for (int i = 16; i < 64; i++) {
            w[i] = SIG1(w[i-2]) + w[i-7] + SIG0(w[i-15]) + w[i-16];
        }
        
        // Initialize working variables for this chunk
        uint32_t a = h0;
        uint32_t b = h1;
        uint32_t c = h2;
        uint32_t d = h3;
        uint32_t e = h4;
        uint32_t f = h5;
        uint32_t g = h6;
        uint32_t h = h7;
        
        // Compression function main loop
        for (int i = 0; i < 64; i++) {
            uint32_t temp1 = h + EP1(e) + CH(e, f, g) + k[i] + w[i];
            uint32_t temp2 = EP0(a) + MAJ(a, b, c);
            
            h = g;
            g = f;
            f = e;
            e = d + temp1;
            d = c;
            c = b;
            b = a;
            a = temp1 + temp2;
        }
        
        // Add this chunk's hash to result so far
        h0 += a;
        h1 += b;
        h2 += c;
        h3 += d;
        h4 += e;
        h5 += f;
        h6 += g;
        h7 += h;
    }
    
    free(msg);
    
    // Produce the final hash value (big-endian)
    to_bytes_sha256(h0, output_hash);
    to_bytes_sha256(h1, output_hash + 4);
    to_bytes_sha256(h2, output_hash + 8);
    to_bytes_sha256(h3, output_hash + 12);
    to_bytes_sha256(h4, output_hash + 16);
    to_bytes_sha256(h5, output_hash + 20);
    to_bytes_sha256(h6, output_hash + 24);
    to_bytes_sha256(h7, output_hash + 28);
}