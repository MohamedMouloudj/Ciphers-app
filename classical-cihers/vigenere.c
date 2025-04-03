#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

#define ALPHABET_SIZE 26
#define MAX_TAILLE 1000

// chiffrement Vigeneere
char* vigenere_chiffrer(const char *texte, const char *cle) {
    int len_texte = strlen(texte);
    int len_cle = strlen(cle);
    int j = 0;
    char *texte_chiffre = (char*)malloc(len_texte + 1); // Allouer la mémoire

    if (texte_chiffre == NULL) {
        printf("Erreur d'allocation mémoire\n");
        return NULL;
    }

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
    return texte_chiffre; // Retourne le texte chiffré
}

// Déchiffrementt
char* vigenere_dechiffrer(const char *texte_chiffre, const char *cle) {
    int len_texte = strlen(texte_chiffre);
    int len_cle = strlen(cle);
    int j = 0;
    char *texte_dechiffre = (char*)malloc(len_texte + 1); // Allouer memory

    if (texte_dechiffre == NULL) {
        printf("Erreur d'allocation mémoire\n");
        return NULL;
    }

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
    return texte_dechiffre; // Retourne le texte déchiffré
}


char* trouver_cle(const char *texte, const char *texte_chiffre) {
    int len_texte = strlen(texte);
    char *cle = (char*)malloc(len_texte + 1); // Allouer la mémoire

    if (cle == NULL) {
        printf("Erreur d'allocation mémoire\n");
        return NULL;
    }

    for (int i = 0; i < len_texte; i++) {
        if (isalpha(texte[i]) && isalpha(texte_chiffre[i])) {
            char base = isupper(texte[i]) ? 'A' : 'a';
            cle[i] = ((texte_chiffre[i] - texte[i] + ALPHABET_SIZE) % ALPHABET_SIZE) + base;
        } else {
            cle[i] = ' ';
        }
    }
    cle[len_texte] = '\0';
    return cle; // Retourne la clé trouvée
}

// Fonction Protocole : interaction avec user
void protocole() {
    char texte[MAX_TAILLE], texte_chiffre[MAX_TAILLE], cle[MAX_TAILLE];
    int choix;

    printf("Choisissez une option :\n1 - Chiffrement\n2 - Déchiffrement\n3 - Trouver la clé\n");
    scanf("%d", &choix);
    getchar(); // Consomme le retour à la ligne

    switch (choix) {
        case 1: {
            printf("Entrez le texte clair : ");
            fgets(texte, MAX_TAILLE, stdin);
            texte[strcspn(texte, "\n")] = 0;  // Supprimer le \n à la fin
            
            printf("Entrez la clé : ");
            fgets(cle, MAX_TAILLE, stdin);
            cle[strcspn(cle, "\n")] = 0;  // Supprimer le \n à la fin
            
            char *texte_chiffre = vigenere_chiffrer(texte, cle);
            if (texte_chiffre != NULL) {
                printf("Texte chiffré : %s\n", texte_chiffre);
                free(texte_chiffre);  // Libérer la mémoire allouée
            }
            break;
        }
        case 2: {
            printf("Entrez le texte chiffré : ");
            fgets(texte_chiffre, MAX_TAILLE, stdin);
            texte_chiffre[strcspn(texte_chiffre, "\n")] = 0;  // Supprimer le \n à la fin
            
            printf("Entrez la clé : ");
            fgets(cle, MAX_TAILLE, stdin);
            cle[strcspn(cle, "\n")] = 0;  // Supprimer le \n à la fin
            
            char *texte = vigenere_dechiffrer(texte_chiffre, cle);
            if (texte != NULL) {
                printf("Texte déchiffré : %s\n", texte);
                free(texte);  // Libérer la mémoire allouée
            }
            break;
        }
        case 3: {
            printf("Entrez le texte clair : ");
            fgets(texte, MAX_TAILLE, stdin);
            texte[strcspn(texte, "\n")] = 0;  // Supprimer le \n à la fin

            printf("Entrez le texte chiffré : ");
            fgets(texte_chiffre, MAX_TAILLE, stdin);
            texte_chiffre[strcspn(texte_chiffre, "\n")] = 0;  // Supprimer le \n à la fin

            char *cle = trouver_cle(texte, texte_chiffre);
            if (cle != NULL) {
                printf("Clé trouvée : %s\n", cle);
                free(cle);  // Libérer la mémoire allouée
            }
            break;
        }
        default:
            printf("Choix invalide.\n");
            break;
    }
}

int main() {
    protocole(); 
    return 0;
}
