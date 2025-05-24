#ifndef INDICE_COINCIDENCE_H
#define INDICE_COINCIDENCE_H

#define ALPHABET_SIZE 26

/**
 * Calculate the index of coincidence for a given text.
 * The index of coincidence is a measure of the probability that two randomly
 * selected letters from the text are the same.
 *
 * @param texte The input text to analyze
 * @return The calculated index of coincidence value
 */
double calculer_indice_coincidence(const char *texte);

#endif