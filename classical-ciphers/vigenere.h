#ifndef VIGENERE_H
#define VIGENERE_H

#define ALPHABET_SIZE 26
#define MAX_TAILLE 1000

void vigenere_chiffrer(const char *texte, const char *cle, char *texte_chiffre);
void vigenere_dechiffrer(const char *texte_chiffre, const char *cle, char *texte_dechiffre);
void trouver_cle(const char *texte, const char *texte_chiffre, char *cle);

#endif