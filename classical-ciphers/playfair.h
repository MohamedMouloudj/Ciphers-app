#ifndef PlAYFAIR_H
#define PlAYFAIR_H

#define SIZE 5
void prepareKey(char *key, char matrix[SIZE][SIZE]);
void prepareText(char *text);
void encryptPlayfair(char *text, char matrix[SIZE][SIZE], char *result);
void decryptPlayfair(char *text, char matrix[SIZE][SIZE], char *result);
void findPosition(char matrix[SIZE][SIZE], char ch, int *row, int *col);
void displayMatrix(char matrix[SIZE][SIZE]);

#endif