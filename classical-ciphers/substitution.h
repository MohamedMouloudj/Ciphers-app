#ifndef SUBSTITUTION_H
#define SUBSTITUTION_H

#define ALPHABET_SIZE 26

// Générer une table de substitution aléatoire
void genererTableAleatoire(char table_originale[], char table_substituee[]);

// Saisie manuelle de la table de substitution
void saisirTable(char table_originale[], char table_substituee[]);

// Chiffrement par substitution
void chiffrer(const char *texte, char *resultat, char table_originale[], char table_substituee[]);

// Déchiffrement par substitution
void dechiffrer(const char *texte, char *resultat, char table_originale[], char table_substituee[]);

#endif // SUBSTITUTION_H