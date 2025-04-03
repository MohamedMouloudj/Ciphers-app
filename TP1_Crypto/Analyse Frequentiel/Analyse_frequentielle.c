#include <stdio.h>
#include <ctype.h>
#include <string.h>

#define ALPHABET_SIZE 26

void analyse_frequentielle(const char *texte, int frequences[], int *total_lettres) {
    *total_lettres = 0;
    for (int i = 0; i < ALPHABET_SIZE; i++) {
        frequences[i] = 0;
    }
    
    for (int i = 0; texte[i] != '\0'; i++) {
        char c = tolower(texte[i]);
        if (c >= 'a' && c <= 'z') {
            frequences[c - 'a']++;
            (*total_lettres)++;
        }
    }
}

int main() {
    char texte[1000];
    int frequences[ALPHABET_SIZE];
    int total_lettres;
    
    printf("Entrez le texte à analyser:\n");
    fgets(texte, sizeof(texte), stdin);
    
    analyse_frequentielle(texte, frequences, &total_lettres);
    
    printf("Lettre | Fréquence | Pourcentage\n");
    printf("--------------------------------\n");
    for (int i = 0; i < ALPHABET_SIZE; i++) {
        if (frequences[i] > 0) {
            double pourcentage = (frequences[i] / (double)total_lettres) * 100.0;
            printf("%c      | %d        | %.2f%%\n", 'a' + i, frequences[i], pourcentage);
        }
    }
    
    return 0;
}
