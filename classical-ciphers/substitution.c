#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define ALPHABET_SIZE 26

// Générer une table de substitution aléatoire
void genererTableAleatoire(char table_originale[], char table_substituee[]) {
    char alphabet[ALPHABET_SIZE + 1] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    strcpy(table_originale, alphabet);
    
    // Copier l'alphabet avant de le mélanger
    char shuffled[ALPHABET_SIZE + 1];
    strcpy(shuffled, alphabet);
    
    // Mélanger aléatoirement l'alphabet avec l'algorithme Fisher-Yates
    for (int i = ALPHABET_SIZE - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        char temp = shuffled[i];
        shuffled[i] = shuffled[j];
        shuffled[j] = temp;
    }
    strcpy(table_substituee, shuffled);
}

// Saisie manuelle de la table de substitution
void saisirTable(char table_originale[], char table_substituee[]) {
    printf("Entrez l'alphabet d'origine (26 lettres majuscules) :\n");
    scanf("%s", table_originale);
    printf("Entrez la table de substitution correspondante (26 lettres majuscules) :\n");
    scanf("%s", table_substituee);
}

// Fonction protocole
int protocole(const char *texte, char *resultat, int mode) {
    // Retourne 1 si le mode est 'chiffrement', 0 si 'dechiffrement'
    if (mode == 1) {
        printf("Mode: Chiffrement\n");
        return 1; // Chiffrement
    } else if (mode == 2) {
        printf("Mode: Déchiffrement\n");
        return 0; // Déchiffrement
    } else {
        printf("Mode inconnu.\n");
        return -1; // Erreur
    }
}

// Chiffrement par substitution
char* chiffrer(const char *texte, char table_originale[], char table_substituee[]) {
    int longueur = strlen(texte);
    char *resultat = (char*) malloc(longueur + 1);
    if (resultat == NULL) {
        fprintf(stderr, "Allocation mémoire échouée\n");
        return NULL;
    }
    
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
    resultat[longueur] = '\0';
    return resultat;
}

// Deechiffrement par substitution
char* dechiffrer(const char *texte, char table_originale[], char table_substituee[]) {
    int longueur = strlen(texte);
    char *resultat = (char*) malloc(longueur + 1);
    if (resultat == NULL) {
        fprintf(stderr, "Allocation mémoire échouée\n");
        return NULL;
    }
    
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
            resultat[i] = lettre; // Conserver_les_caractères non_alphabétiques
        }
    }
    resultat[longueur] = '\0';
    return resultat;
}

// testt
// int main() {
//     srand(time(NULL));
//     char table_originale[ALPHABET_SIZE + 1];
//     char table_substituee[ALPHABET_SIZE + 1];
//     char texte[256], *resultat;
//     int choix, mode;
    
//     // Choix entre remplir table automatiquement ou manuellement
//     printf("Choisissez la méthode de remplissage de la table :\n");
//     printf("1. Automatique\n2. Manuelle\n");
//     scanf("%d", &choix);
//     getchar(); // Pour éviter le bug de scanf
    
//     if (choix == 1) {
//         genererTableAleatoire(table_originale, table_substituee);
//     } else {
//         saisirTable(table_originale, table_substituee);
//     }
    
//     printf("Table d'origine      : %s\n", table_originale);
//     printf("Table de substitution: %s\n", table_substituee);
    
//     // Choisir le mode de chiffrement ou de déchiffrement
//     printf("Choisissez le mode :\n1. Chiffrement\n2. Déchiffrement\n");
//     scanf("%d", &mode);
//     getchar();
    
//     printf("Entrez le texte (majuscule uniquement) : ");
//     fgets(texte, sizeof(texte), stdin);
//     texte[strcspn(texte, "\n")] = 0; // Supprimer le \n final

//     // Appliquer le protocole pour déterminer si on chiffre ou déchiffre
//     int mode_protocole = protocole(texte, resultat, mode);
    
//     if (mode_protocole == 1) {
//         resultat = chiffrer(texte, table_originale, table_substituee);
//     } else if (mode_protocole == 0) {
//         resultat = dechiffrer(texte, table_originale, table_substituee);
//     } else {
//         printf("Erreur dans le choix du mode.\n");
//         return -1;
//     }
    
//     printf("Résultat : %s\n", resultat);
//     free(resultat); // N'oubliez pas de libérer la mémoire allouée
//     return 0;
// }
