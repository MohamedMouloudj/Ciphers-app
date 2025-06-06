#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "caesar.h"

// Fonction de chiffrement de César
char* chiffrementCesar(const char *message, int decalage) {
    if (message == NULL) {
        return NULL;
    }
    char *result = (char*) malloc(strlen(message) + 1);
    if (result == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return NULL;
    }
    strcpy(result, message);
    for (int i = 0; result[i] != '\0'; i++) {
        if (isalpha(result[i])) {
            char base = isupper(result[i]) ? 'A' : 'a';
            result[i] = (result[i] - base + decalage) % 26 + base;
        }
    }
    result[strlen(message)] = '\0';
    return result;
}

// Fonction de déchiffrement de César
char* dechiffrementCesar(const char *message, int decalage) {
    if (message == NULL) {
        return NULL;
    }
    
    size_t len = strlen(message);
    char *result = (char*) malloc(len + 1);
    if (result == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return NULL;
    }

    for (size_t i = 0; i < len; i++) {
        if (isalpha(message[i])) {
            char base = isupper(message[i]) ? 'A' : 'a';
            result[i] = (message[i] - base - decalage + 26) % 26 + base;
        } else {
            result[i] = message[i];
        }
    }
    result[len] = '\0';
    return result;
}

// int main() {
//     char texte[MAX_TEXT];
//     int cle, choix;

//     // Affichage du menu
//     printf("1. Chiffrer\n2. D%cchiffrer\n",130);
//     scanf("%d", &choix);
//     getchar(); // Pour consommer le retour à la ligne

//     // Saisie du texte
//     printf("Entrez le texte: ");
//     fgets(texte, MAX_TEXT, stdin);
//     texte[strcspn(texte, "\\n")] = 0; // Retirer le retour à la ligne

//     // Saisie de la clé
//     printf("Entrez la clé (nombre): ");
//     scanf("%d", &cle);

//     // Traitement selon le choix
//     if (choix == 1) {
//         char* res=chiffrementCesar(texte, cle);
//         printf("%s\n", res);
//     } else if (choix == 2) {
//         char* res=dechiffrementCesar(texte, cle);
//         printf("%s\n", res);
//     } else {
//         printf("Choix invalide.\n");
//     }

//     return 0;
// }
