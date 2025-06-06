/*
 * Refactored MD5 implementation - Core algorithm only
 * No constants, no file operations, no main function
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

// leftrotate function definition
#define LEFTROTATE(x, c) (((x) << (c)) | ((x) >> (32 - (c))))

void to_bytes(uint32_t val, uint8_t *bytes)
{
    bytes[0] = (uint8_t) val;
    bytes[1] = (uint8_t) (val >> 8);
    bytes[2] = (uint8_t) (val >> 16);
    bytes[3] = (uint8_t) (val >> 24);
}

uint32_t to_int32(const uint8_t *bytes)
{
    return (uint32_t) bytes[0]
        | ((uint32_t) bytes[1] << 8)
        | ((uint32_t) bytes[2] << 16)
        | ((uint32_t) bytes[3] << 24);
}

void get_md5_constants(uint32_t **k_table, uint32_t **r_table) {
    // Dynamically allocate and initialize k constants
    static uint32_t k[64] = {
        0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
        0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
        0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
        0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
        0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
        0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
        0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
        0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
        0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
        0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
        0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
        0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
        0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
        0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
        0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
        0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
    };
    
    // Dynamically allocate and initialize r constants
    static uint32_t r[64] = {
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
        5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
    };
    
    *k_table = k;
    *r_table = r;
}

void md5_encrypt(const uint8_t *input_data, size_t input_len, uint8_t *output_hash) {
    uint32_t *k, *r;
    get_md5_constants(&k, &r);
    
    // Hash variables
    uint32_t h0, h1, h2, h3;
    
    // Message processing variables
    uint8_t *msg = NULL;
    size_t new_len, offset;
    uint32_t w[16];
    uint32_t a, b, c, d, i, f, g, temp;
    
    // Initialize hash values
    h0 = 0x67452301;
    h1 = 0xefcdab89;
    h2 = 0x98badcfe;
    h3 = 0x10325476;
    
    // Pre-processing: padding
    for (new_len = input_len + 1; new_len % (512/8) != 448/8; new_len++)
        ;
    
    msg = (uint8_t*)malloc(new_len + 8);
    if (msg == NULL) {
        return; // Memory allocation failed
    }
    
    memcpy(msg, input_data, input_len);
    msg[input_len] = 0x80; // append the "1" bit
    
    for (offset = input_len + 1; offset < new_len; offset++)
        msg[offset] = 0; // append "0" bits
    
    // Append length in bits at the end
    to_bytes(input_len * 8, msg + new_len);
    to_bytes(input_len >> 29, msg + new_len + 4);
    
    // Process message in 512-bit chunks
    for(offset = 0; offset < new_len; offset += (512/8)) {
        
        // Break chunk into sixteen 32-bit words
        for (i = 0; i < 16; i++)
            w[i] = to_int32(msg + offset + i * 4);
        
        // Initialize hash value for this chunk
        a = h0;
        b = h1;
        c = h2;
        d = h3;
        
        // Main loop - 64 rounds
        for(i = 0; i < 64; i++) {
            
            if (i < 16) {
                f = (b & c) | ((~b) & d);
                g = i;
            } else if (i < 32) {
                f = (d & b) | ((~d) & c);
                g = (5 * i + 1) % 16;
            } else if (i < 48) {
                f = b ^ c ^ d;
                g = (3 * i + 5) % 16;
            } else {
                f = c ^ (b | (~d));
                g = (7 * i) % 16;
            }
            
            temp = d;
            d = c;
            c = b;
            b = b + LEFTROTATE((a + f + k[i] + w[g]), r[i]);
            a = temp;
        }
        
        // Add this chunk's hash to result
        h0 += a;
        h1 += b;
        h2 += c;
        h3 += d;
    }
    
    // Cleanup
    free(msg);
    
    // Output hash in little-endian format
    to_bytes(h0, output_hash);
    to_bytes(h1, output_hash + 4);
    to_bytes(h2, output_hash + 8);
    to_bytes(h3, output_hash + 12);
}

// MD5 doesn't have a traditional "decrypt" function since it's a hash function
// This function exists for API consistency but just returns an error indicator
int md5_decrypt(const uint8_t *hash_input, size_t hash_len, uint8_t *output_data) {
    // MD5 is a one-way hash function - decryption is not possible
    // Return -1 to indicate this operation is not supported
    return -1;
}

// Utility function to convert hash to hexadecimal string
void md5_hash_to_hex(const uint8_t *hash, char *hex_output) {
    int i;
    for (i = 0; i < 16; i++) {
        sprintf(hex_output + (i * 2), "%02x", hash[i]);
    }
    hex_output[32] = '\0';
}

// Utility function to compare two MD5 hashes
int md5_compare_hashes(const uint8_t *hash1, const uint8_t *hash2) {
    return memcmp(hash1, hash2, 16);
}