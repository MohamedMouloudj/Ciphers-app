#ifndef ANALYSE_FREQUENTIELLE_H
#define ANALYSE_FREQUENTIELLE_H

#define ALPHABET_SIZE 26

void analyse_frequentielle(const char *texte, int frequences[], int *total_lettres);
void printFrequenciestable(int frequences[ALPHABET_SIZE], int total_lettres);

#endif