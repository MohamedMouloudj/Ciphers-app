#ifndef MD5_H
#define MD5_H

/**
 * @brief MD5 Hash Implementation
 * 
 * Core algorithm for MD5 hash function without file operations or main function.
 * Provides functionality to compute MD5 hashes of input data.
 */

#include <stdint.h>

/**
 * @brief Converts a 32-bit value to bytes
 * @param val The 32-bit value to convert
 * @param bytes The output byte array (must be at least 4 bytes)
 */
void to_bytes(uint32_t val, uint8_t *bytes);

/**
 * @brief Converts 4 bytes to a 32-bit integer
 * @param bytes The input byte array (must be at least 4 bytes)
 * @return The converted 32-bit value
 */
uint32_t to_int32(const uint8_t *bytes);

/**
 * @brief Gets the constant tables used in MD5 algorithm
 * @param k_table Pointer to receive the k constants table
 * @param r_table Pointer to receive the r constants table
 */
void get_md5_constants(uint32_t **k_table, uint32_t **r_table);

/**
 * @brief Computes the MD5 hash of the input data
 * @param input_data The input data to hash
 * @param input_len Length of the input data in bytes
 * @param output_hash The output hash (must be at least 16 bytes)
 */
void md5_encrypt(const uint8_t *input_data, size_t input_len, uint8_t *output_hash);

/**
 * @brief Placeholder for API consistency, not a real function as MD5 is one-way
 * @param hash_input The hash to "decrypt"
 * @param hash_len Length of the hash input
 * @param output_data Output buffer
 * @return Always returns -1 as MD5 is not decryptable
 */
int md5_decrypt(const uint8_t *hash_input, size_t hash_len, uint8_t *output_data);

/**
 * @brief Converts an MD5 hash to a hexadecimal string
 * @param hash The MD5 hash (16 bytes)
 * @param hex_output Output buffer for the hex string (must be at least 33 bytes)
 */
void md5_hash_to_hex(const uint8_t *hash, char *hex_output);

/**
 * @brief Compares two MD5 hashes for equality
 * @param hash1 First hash
 * @param hash2 Second hash
 * @return 0 if equal, non-zero otherwise
 */
int md5_compare_hashes(const uint8_t *hash1, const uint8_t *hash2);


#endif