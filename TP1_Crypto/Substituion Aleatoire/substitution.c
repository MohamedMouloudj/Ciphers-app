#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define ALPHABET_SIZE 26

// Générer une table de substitution aléatoire
void genererTableAleatoire(char table_originale[], char table_substituee[]) {
    char alphabet[ALPHABET_SIZE] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    strcpy(table_originale, alphabet);
    
    // Mélanger aléatoirement l'alphabet pour obtenir une substitution
    for (int i = 0; i < ALPHABET_SIZE; i++) {
        int j = rand() % ALPHABET_SIZE;
        char temp = alphabet[i];
        alphabet[i] = alphabet[j];
        alphabet[j] = temp;
    }
    strcpy(table_substituee, alphabet);
}

// Saisie manuelle de la table de substitution
void saisirTable(char table_originale[], char table_substituee[]) {
    printf("Entrez l'alphabet d'origine (26 lettres majuscules) :\n");
    scanf("%s", table_originale);
    printf("Entrez la table de substitution correspondante (26 lettres majuscules) :\n");
    scanf("%s", table_substituee);
}

// Chiffrement par substitution
void chiffrer(const char *texte, char *resultat, char table_originale[], char table_substituee[]) {
    for (int i = 0; texte[i] != '\0'; i++) {
        char lettre = texte[i];
        if (lettre >= 'A' && lettre <= 'Z') {
            for (int j = 0; j < ALPHABET_SIZE; j++) {
                if (lettre == table_originale[j]) {
                    resultat[i] = table_substituee[j];
                    break;
                }
            }
        } else {
            resultat[i] = lettre; // Conserver les caractères non alphabétiques
        }
    }
    resultat[strlen(texte)] = '\0';
}

// Déchiffrement par substitution
void dechiffrer(const char *texte, char *resultat, char table_originale[], char table_substituee[]) {
    for (int i = 0; texte[i] != '\0'; i++) {
        char lettre = texte[i];
        if (lettre >= 'A' && lettre <= 'Z') {
            for (int j = 0; j < ALPHABET_SIZE; j++) {
                if (lettre == table_substituee[j]) {
                    resultat[i] = table_originale[j];
                    break;
                }
            }
        } else {
            resultat[i] = lettre; // Conserver les caractères non alphabétiques
        }
    }
    resultat[strlen(texte)] = '\0';
}

int main() {
    srand(time(NULL));
    char table_originale[ALPHABET_SIZE + 1];
    char table_substituee[ALPHABET_SIZE + 1];
    char texte[256], resultat[256];
    int choix, mode;
    
    printf("Choisissez la méthode de remplissage de la table :\n");
    printf("1. Automatique\n2. Manuelle\n");
    scanf("%d", &choix);
    getchar(); // Pour éviter le bug de scanf
    
    if (choix == 1) {
        genererTableAleatoire(table_originale, table_substituee);
    } else {
        saisirTable(table_originale, table_substituee);
    }
    
    printf("Table d'origine      : %s\n", table_originale);
    printf("Table de substitution: %s\n", table_substituee);
    
    printf("Choisissez le mode :\n1. Chiffrement\n2. Déchiffrement\n");
    scanf("%d", &mode);
    getchar();
    
    printf("Entrez le texte (majuscule uniquement) : ");
    fgets(texte, sizeof(texte), stdin);
    texte[strcspn(texte, "\n")] = 0; // Supprimer le \n final

    if (mode == 1) {
        chiffrer(texte, resultat, table_originale, table_substituee);
    } else {
        dechiffrer(texte, resultat, table_originale, table_substituee);
    }
    
    printf("Résultat : %s\n", resultat);
    return 0;
}

