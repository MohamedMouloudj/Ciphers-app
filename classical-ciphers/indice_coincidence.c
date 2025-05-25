#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include "indice_coincidence.h"

#define ALPHABET_SIZE 26

double calculer_indice_coincidence(const char *texte) {
    int frequences[ALPHABET_SIZE] = {0};
    int total_lettres = 0;
    
    // Count letter frequencies (only a-z and A-Z)
    for (int i = 0; texte[i] != '\0'; i++) {
        if (isalpha((unsigned char)texte[i])) {
            char c = tolower((unsigned char)texte[i]);
            frequences[c - 'a']++;
            total_lettres++;
        }
    }
    
    // Handle edge cases
    if (total_lettres <= 1) {
        return 0.0;
    }
    
    // Calculate Index of Coincidence
    // IC = Σ(n_i × (n_i - 1)) / (N × (N - 1))
    double somme = 0.0;
    for (int i = 0; i < ALPHABET_SIZE; i++) {
        somme += (double)frequences[i] * (frequences[i] - 1);
    }
    
    return somme / (double)(total_lettres * (total_lettres - 1));
}

// int main() {
//     char texte[10000]; // Increased buffer size for longer texts
    
//     printf("Enter text to analyze (English IC is typically around 0.067):\n");
//     fgets(texte, sizeof(texte), stdin);
    
//     // Remove trailing newline if present
//     size_t len = strlen(texte);
//     if (len > 0 && texte[len-1] == '\n') {
//         texte[len-1] = '\0';
//     }
    
//     double ic = calculer_indice_coincidence(texte);
    
//     printf("Index of Coincidence: %.6f\n", ic);
//     printf("Reference values: English (~0.067), French (~0.078), German (~0.076), Random (~0.038)\n");
    
//     return 0;
// }

