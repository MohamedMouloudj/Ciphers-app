#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define ALPHABET_SIZE 26
#define MAX_TAILLE 1000

void vigenere_chiffrer(const char *texte, const char *cle, char *texte_chiffre) {
    int len_texte = strlen(texte);
    int len_cle = strlen(cle);
    int j = 0;

    for (int i = 0; i < len_texte; i++) {
        if (isalpha(texte[i])) {
            char base = isupper(texte[i]) ? 'A' : 'a';
            char base_cle = isupper(cle[j % len_cle]) ? 'A' : 'a';
            texte_chiffre[i] = ((texte[i] - base + (cle[j % len_cle] - base_cle)) % ALPHABET_SIZE) + base;
            j++;
        } else {
            texte_chiffre[i] = texte[i];
        }
    }
    texte_chiffre[len_texte] = '\0';
}

void vigenere_dechiffrer(const char *texte_chiffre, const char *cle, char *texte_dechiffre) {
    int len_texte = strlen(texte_chiffre);
    int len_cle = strlen(cle);
    int j = 0;

    for (int i = 0; i < len_texte; i++) {
        if (isalpha(texte_chiffre[i])) {
            char base = isupper(texte_chiffre[i]) ? 'A' : 'a';
            char base_cle = isupper(cle[j % len_cle]) ? 'A' : 'a';
            texte_dechiffre[i] = ((texte_chiffre[i] - base - (cle[j % len_cle] - base_cle) + ALPHABET_SIZE) % ALPHABET_SIZE) + base;
            j++;
        } else {
            texte_dechiffre[i] = texte_chiffre[i];
        }
    }
    texte_dechiffre[len_texte] = '\0';
}

void trouver_cle(const char *texte, const char *texte_chiffre, char *cle) {
    int len_texte = strlen(texte);
    for (int i = 0; i < len_texte; i++) {
        if (isalpha(texte[i]) && isalpha(texte_chiffre[i])) {
            char base = isupper(texte[i]) ? 'A' : 'a';
            cle[i] = ((texte_chiffre[i] - texte[i] + ALPHABET_SIZE) % ALPHABET_SIZE) + base;
        } else {
            cle[i] = ' ';
        }
    }
    cle[len_texte] = '\0';
}

// int main() {
//     char texte[MAX_TAILLE], texte_chiffre[MAX_TAILLE], cle[MAX_TAILLE];
//     int choix;

//     printf("Choisissez une option:\n1 - Chiffrement\n2 - Déchiffrement\n3 - Trouver la clé\n");
//     scanf("%d", &choix);
//     getchar(); // Consomme le retour à la ligne

//     if (choix == 1) {
//         printf("Entrez le texte clair : ");
//         fgets(texte, MAX_TAILLE, stdin);
//         texte[strcspn(texte, "\n")] = 0;
        
//         printf("Entrez la clé : ");
//         fgets(cle, MAX_TAILLE, stdin);
//         cle[strcspn(cle, "\n")] = 0;
        
//         vigenere_chiffrer(texte, cle, texte_chiffre);
//         printf("Texte chiffré : %s\n", texte_chiffre);
//     } 
//     else if (choix == 2) {
//         printf("Entrez le texte chiffré : ");
//         fgets(texte_chiffre, MAX_TAILLE, stdin);
//         texte_chiffre[strcspn(texte_chiffre, "\n")] = 0;
        
//         printf("Entrez la clé : ");
//         fgets(cle, MAX_TAILLE, stdin);
//         cle[strcspn(cle, "\n")] = 0;
        
//         vigenere_dechiffrer(texte_chiffre, cle, texte);
//         printf("Texte déchiffré : %s\n", texte);
//     } 
//     else if (choix == 3) {
//         printf("Entrez le texte clair : ");
//         fgets(texte, MAX_TAILLE, stdin);
//         texte[strcspn(texte, "\n")] = 0;

//         printf("Entrez le texte chiffré : ");
//         fgets(texte_chiffre, MAX_TAILLE, stdin);
//         texte_chiffre[strcspn(texte_chiffre, "\n")] = 0;

//         trouver_cle(texte, texte_chiffre, cle);
//         printf("Clé trouvée : %s\n", cle);
//     } 
//     else {
//         printf("Choix invalide.\n");
//     }

//     return 0;
// }
