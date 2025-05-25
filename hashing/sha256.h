#ifndef SHA256_H
#define SHA256_H

/**
 * @brief SHA-256 Hash Implementation
 * 
 * Core algorithm for SHA-256 hash function without file operations or main function.
 * Provides functionality to compute SHA-256 hashes of input data.
 */

#include <stdint.h>
#include <stddef.h>

/**
 * @brief Converts a 32-bit value to bytes (big-endian)
 * @param val The 32-bit value to convert
 * @param bytes The output byte array (must be at least 4 bytes)
 */
void to_bytes_sha256(uint32_t val, uint8_t *bytes);

/**
 * @brief Converts 4 bytes to a 32-bit integer (big-endian)
 * @param bytes The input byte array (must be at least 4 bytes)
 * @return The converted 32-bit value
 */
uint32_t to_uint32_sha256(const uint8_t *bytes);

/**
 * @brief Computes the SHA-256 hash of the input data
 * @param input_data The input data to hash
 * @param input_len Length of the input data in bytes
 * @param output_hash The output hash (must be at least 32 bytes)
 */
void sha256_encrypt(const uint8_t *input_data, size_t input_len, uint8_t *output_hash);

/**
 * @brief Placeholder for API consistency, not a real function as SHA-256 is one-way
 * @param hash_input The hash to "decrypt"
 * @param hash_len Length of the hash input
 * @param output_data Output buffer
 * @return Always returns -1 as SHA-256 is not decryptable
 */
int sha256_decrypt(const uint8_t *hash_input, size_t hash_len, uint8_t *output_data);

/**
 * @brief Converts a SHA-256 hash to a hexadecimal string
 * @param hash The SHA-256 hash (32 bytes)
 * @param hex_output Output buffer for the hex string (must be at least 65 bytes)
 */
void sha256_hash_to_hex(const uint8_t *hash, char *hex_output);

/**
 * @brief Compares two SHA-256 hashes for equality
 * @param hash1 First hash (32 bytes)
 * @param hash2 Second hash (32 bytes)
 * @return 0 if equal, non-zero otherwise
 */
int sha256_compare_hashes(const uint8_t *hash1, const uint8_t *hash2);

#endif