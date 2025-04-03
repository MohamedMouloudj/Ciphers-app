#include <stdio.h>
#include <ctype.h>
#include <string.h>

#define ALPHABET_SIZE 26

double calculer_indice_coincidence(const char *texte) {
    int frequences[ALPHABET_SIZE] = {0};
    int total_lettres = 0;
    
    // Compter les fréquences des lettres
    for (int i = 0; texte[i] != '\0'; i++) {
        char c = tolower(texte[i]);
        if (c >= 'a' && c <= 'z') {
            frequences[c - 'a']++;
            total_lettres++;
        }
    }
    
    if (total_lettres <= 1) return 0.0;
    
    // Calcul de l'indice de coïncidence
    double ic = 0.0;
    for (int i = 0; i < ALPHABET_SIZE; i++) {
        ic += (double)(frequences[i] * (frequences[i] - 1));
    }
    ic /= (double)(total_lettres * (total_lettres - 1));
    
    return ic;
}

int main() {
    char texte[1000];
    
    printf("Entrez le texte à analyser:\n");
    fgets(texte, sizeof(texte), stdin);
    
    double ic = calculer_indice_coincidence(texte);
    
    printf("Indice de coïncidence : %.6f\n", ic);
    
    return 0;
}

