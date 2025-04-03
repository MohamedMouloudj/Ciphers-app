#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_TEXT 256

// Fonction de chiffrement de César
void chiffrementCesar(char *message, int decalage) {
    for (int i = 0; message[i] != '\0'; i++) {
        if (isalpha(message[i])) {
            char base = isupper(message[i]) ? 'A' : 'a';
            message[i] = (message[i] - base + decalage) % 26 + base;
        }
    }
}

// Fonction de déchiffrement de César
void dechiffrementCesar(char *message, int decalage) {
    for (int i = 0; message[i] != '\0'; i++) {
        if (isalpha(message[i])) {
            char base = isupper(message[i]) ? 'A' : 'a';
            message[i] = (message[i] - base - decalage + 26) % 26 + base;
        }
    }
}

int main() {
    char texte[MAX_TEXT];
    int cle, choix;

    // Affichage du menu
    printf("1. Chiffrer\n2. Déchiffrer\n");
    scanf("%d", &choix);
    getchar(); // Pour consommer le retour à la ligne

    // Saisie du texte
    //printf("Entrez le texte: ");
    fgets(texte, MAX_TEXT, stdin);
    texte[strcspn(texte, "\\n")] = 0; // Retirer le retour à la ligne

    // Saisie de la clé
    //printf("Entrez la clé (nombre): ");
    scanf("%d", &cle);

    // Traitement selon le choix
    if (choix == 1) {
        chiffrementCesar(texte, cle);
        printf("%s\n", texte);
    } else if (choix == 2) {
        dechiffrementCesar(texte, cle);
        printf("%s\n", texte);
    } else {
        printf("Choix invalide.\n");
    }

    return 0;
}
