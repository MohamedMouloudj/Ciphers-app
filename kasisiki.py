import re
import numpy as np
from collections import Counter
from itertools import cycle
from math import gcd
from functools import reduce

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def clean_text(text):
    return re.sub(r'[^A-Z]', '', text.upper())

def kasiski_examination(ciphertext, min_length=3):
    sequences = {}
    for i in range(len(ciphertext) - min_length):
        seq = ciphertext[i:i + min_length]
        for j in range(i + min_length, len(ciphertext) - min_length):
            if ciphertext[j:j + min_length] == seq:
                distance = j - i
                if seq not in sequences:
                    sequences[seq] = []
                sequences[seq].append(distance)

    gcds = [reduce(gcd, distances) for distances in sequences.values() if len(distances) > 1]
    
    if gcds:
        probable_key_length = Counter(gcds).most_common(1)[0][0]
    else:
        probable_key_length = None

    return probable_key_length

def index_of_coincidence(text):
    N = len(text)
    freqs = Counter(text)
    return sum(f * (f - 1) for f in freqs.values()) / (N * (N - 1))


def split_text_by_key_length(text, key_length):
    columns = ['' for _ in range(key_length)]
    for i, char in enumerate(text):
        columns[i % key_length] += char
    return columns

def frequency_analysis(columns):
    key = ''
    for col in columns:
        freqs = Counter(col)
        most_frequent = freqs.most_common(1)[0][0]  # Most common letter
        shift = (ALPHABET.index(most_frequent) - ALPHABET.index('E')) % 26  # Assuming 'E' is most frequent in French
        key += ALPHABET[shift]
    return key

def vigenere_decrypt(ciphertext, key):
    plaintext = []
    key_cycle = cycle(key)

    for letter in ciphertext:
        shift = ALPHABET.index(next(key_cycle))
        decrypted_letter = ALPHABET[(ALPHABET.index(letter) - shift) % 26]
        plaintext.append(decrypted_letter)

    return "".join(plaintext)

# -----------------------
#  the Analysis
# -----------------------

ciphertext = """
NLSWMOCJECLFEFBOZTGJUBQUGJOXAUKAUOVUWUDONJOHJOCSRVUBTFULNDZF
RYICMTNLSMWVVZEDXFTAECITUVCSMTCJECUFPHCOAQGBVOVUCCOSZEGZROXF
TJUCAJQUSCQHPPFSKBVPVOATWYLKDJCIIVQUGLTVIQGYEXVJVLDOAPTNAXQT
CAIYVTKSECBEQUCSUQGYADQGRVUBTFULNDZFRYICMTFPNFMTVPRNIOUKECAP
NBTSWOUKEMGCGYSOKVTPTOMGHPCKKFULTNMQTVMYCWQPREVFEBLDCSGKEVIT
GJUBQUGHUCMJPKEVMVTZEACJRLSOVBFVPDIOVBNOIQRYOMPFRYOKKUKCEOTM
GZPOCWGUTBMEWPROTFUYICYVGZEDXSQAEQMSNLUBABEAIPADQUTBMMGZCIJF
TTEXIDGZLKAFPZILQMKZADQPPLTVIGQYMKBJQUCYVUKUUOLFULMZTPALSKQO
UPQEMMCKOZBJQUDOBFEONYTPIPECIWCUCOMTUVNDLFULLOUFPASMTFUWOEZS
GUFYZDGYLKZFUPLSMOELFKKFCJECLFHPS
"""

ciphertext = clean_text(ciphertext)

kasiski_length = kasiski_examination(ciphertext)
print(f"Kasiski Estimated Key Length: {kasiski_length}")


key_length = kasiski_length if kasiski_length else friedman_length
print(f"Using Key Length: {key_length}")

columns = split_text_by_key_length(ciphertext, key_length)
key = frequency_analysis(columns)
print(f"🔑 Extracted Key: {key}")

decrypted_text = vigenere_decrypt(ciphertext, key)
print("\n📝 Decrypted Text:\n", decrypted_text)