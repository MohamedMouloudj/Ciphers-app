#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

// First 32 bits of the fractional parts of the cube roots of the first 64 prime numbers
const uint32_t k[] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
};

// SHA-256 operations
#define ROTRIGHT(word, bits) (((word) >> (bits)) | ((word) << (32-(bits))))
#define CH(x, y, z) (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x, y, z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define EP0(x) (ROTRIGHT(x, 2) ^ ROTRIGHT(x, 13) ^ ROTRIGHT(x, 22))
#define EP1(x) (ROTRIGHT(x, 6) ^ ROTRIGHT(x, 11) ^ ROTRIGHT(x, 25))
#define SIG0(x) (ROTRIGHT(x, 7) ^ ROTRIGHT(x, 18) ^ ((x) >> 3))
#define SIG1(x) (ROTRIGHT(x, 17) ^ ROTRIGHT(x, 19) ^ ((x) >> 10))

// Helper function to convert from big-endian to little-endian
void to_bytes(uint32_t val, uint8_t *bytes) {
    bytes[0] = (uint8_t) (val >> 24);
    bytes[1] = (uint8_t) (val >> 16);
    bytes[2] = (uint8_t) (val >> 8);
    bytes[3] = (uint8_t) val;
}

// Helper function to convert from little-endian to big-endian
uint32_t to_uint32(const uint8_t *bytes) {
    return ((uint32_t) bytes[0] << 24) | 
           ((uint32_t) bytes[1] << 16) | 
           ((uint32_t) bytes[2] << 8) | 
           ((uint32_t) bytes[3]);
}

// SHA-256 implementation
void sha256(const uint8_t *initial_msg, size_t initial_len, uint8_t *digest) {
    // Initialize hash values
    // (first 32 bits of the fractional parts of the square roots of the first 8 primes)
    uint32_t h0 = 0x6a09e667;
    uint32_t h1 = 0xbb67ae85;
    uint32_t h2 = 0x3c6ef372;
    uint32_t h3 = 0xa54ff53a;
    uint32_t h4 = 0x510e527f;
    uint32_t h5 = 0x9b05688c;
    uint32_t h6 = 0x1f83d9ab;
    uint32_t h7 = 0x5be0cd19;

    // Message preparation
    uint8_t *msg = NULL;
    
    // Calculate padding
    size_t padded_len;
    for (padded_len = initial_len + 1; padded_len % 64 != 56; padded_len++);
    padded_len += 8; // for the length field
    
    // Allocate memory for padded message
    msg = (uint8_t*)malloc(padded_len);
    if (msg == NULL) {
        fprintf(stderr, "Failed to allocate memory\n");
        return;
    }
    
    // Copy original message
    memcpy(msg, initial_msg, initial_len);
    
    // Append the bit '1' to the message
    msg[initial_len] = 0x80; 
    
    // Append zeros
    for (size_t i = initial_len + 1; i < padded_len - 8; i++) {
        msg[i] = 0;
    }
    
    // Append message length in bits (big-endian)
    uint64_t bit_len = initial_len * 8;
    for (int i = 0; i < 8; i++) {
        msg[padded_len - 8 + i] = (bit_len >> (56 - i * 8)) & 0xFF;
    }
    
    // Process the message in successive 512-bit chunks
    for (size_t i = 0; i < padded_len; i += 64) {
        uint32_t w[64];
        
        // Break chunk into sixteen 32-bit big-endian words
        for (int j = 0; j < 16; j++) {
            w[j] = ((uint32_t) msg[i + j * 4] << 24) |
                   ((uint32_t) msg[i + j * 4 + 1] << 16) |
                   ((uint32_t) msg[i + j * 4 + 2] << 8) |
                   ((uint32_t) msg[i + j * 4 + 3]);
        }
        
        // Extend the sixteen 32-bit words into sixty-four 32-bit words
        for (int j = 16; j < 64; j++) {
            w[j] = SIG1(w[j-2]) + w[j-7] + SIG0(w[j-15]) + w[j-16];
        }
        
        // Initialize working variables to current hash value
        uint32_t a = h0;
        uint32_t b = h1;
        uint32_t c = h2;
        uint32_t d = h3;
        uint32_t e = h4;
        uint32_t f = h5;
        uint32_t g = h6;
        uint32_t h = h7;
        
        // Main loop
        for (int j = 0; j < 64; j++) {
            uint32_t temp1 = h + EP1(e) + CH(e, f, g) + k[j] + w[j];
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
        
        // Add the compressed chunk to the current hash value
        h0 += a;
        h1 += b;
        h2 += c;
        h3 += d;
        h4 += e;
        h5 += f;
        h6 += g;
        h7 += h;
    }
    
    // Free the padded message
    free(msg);
    
    // Produce the final hash value (big-endian)
    to_bytes(h0, digest);
    to_bytes(h1, digest + 4);
    to_bytes(h2, digest + 8);
    to_bytes(h3, digest + 12);
    to_bytes(h4, digest + 16);
    to_bytes(h5, digest + 20);
    to_bytes(h6, digest + 24);
    to_bytes(h7, digest + 28);
}

int main(int argc, char **argv) {
    char *msg;
    size_t len;
    uint8_t hash[32];
    
    // Check arguments
    if (argc < 2) {
        printf("usage: %s 'string'\n", argv[0]);
        return 1;
    }
        
    msg = argv[1];
    len = strlen(msg);
    
    sha256((uint8_t*)msg, len, hash);
    
    printf("SHA-256 hash: ");
    for (int i = 0; i < 32; i++) {
        printf("%02x", hash[i]);
    }
    printf("\n");
    
    return 0;
}
