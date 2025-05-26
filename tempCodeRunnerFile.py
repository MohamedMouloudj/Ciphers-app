from collections import Counter

def split_text_by_key_length(text, key_length):
    """Divise le texte en key_length sous-textes"""
    groups = ['' for _ in range(key_length)]
    for i, letter in enumerate(text):
        groups[i % key_length] += letter
    return groups

def frequency_analysis(groups):
    """Analyse de fréquence pour chaque groupe"""
    for i, group in enumerate(groups):
        counter = Counter(group)
        total = len(group)
        print(f"\nFréquence des lettres pour le groupe {i + 1}:")
        for letter, count in counter.most_common():
            print(f"{letter}: {count / total:.4f}")

def get_key(groups):
    """Trouve la clé probable en comparant la lettre la plus fréquente à 'E'"""
    key = ''
    for group in groups:
        most_common_letter = Counter(group).most_common(1)[0][0]  # Lettre la plus fréquente
        shift = (ord(most_common_letter) - ord('E')) % 26  # Décalage par rapport à 'E'
        key += chr(ord('A') + shift)  # Convertit en lettre majuscule
    return key

def decrypt_vigenere(text, key):
    """Déchiffre un texte Vigenère avec une clé donnée"""
    decrypted_text = ''
    key_length = len(key)
    
    for i, letter in enumerate(text):
        shift = ord(key[i % key_length]) - ord('A')
        decrypted_letter = chr(((ord(letter) - ord('A') - shift) % 26) + ord('A'))
        decrypted_text += decrypted_letter
    
    return decrypted_text

# Message chiffré et longueur supposée de la clé
message = "NLWBPZVLWRTVCUGUPZGZVQDCNAEZELWUIHTWNHXUZVFLPMNWPMMPPVVPEXTBGKIEOWPUIQDXGBZQYBGAVQAITAMOFTKLVQXMPATDPWEJYBLVVLWQYXNBWPPAEVYFDLKYIOEANPIELTCYIBLZCAMAYLGZWKDBGTIENWOWVAXQUSIEPVVYIBCQULWPZQXLRFQIKYIRLKGHHQDIOLRPPATLKXPUGUXMTZGZIFLLGZJDLQUQYDTLKXYQDIUZSOTMUKIBWCUSEBPZVLHQNWPMMMYKGKIENTKLRFDAWPXQLCPPROTLGUXPPAGJYDTBGWIGEMPAVMTVGYYZPLKTMZFBKVRETOPPJUNIVPZQOMUYIHPVWZGQCBCPRECIRWSDEAKUHUBCCUXCFCPLIZEZGWVUDMRLYFDCDPVGYMDHMEDMFLZUYOVWSGCKGUXPPAQUGTTNHYIPLNHHMDPAFHREWMUTSUDAWPZMYBWUXQWQPJMPPVV"
key_length = 6  # Supposée

# Étape 1 : Découpage du texte
groups = split_text_by_key_length(message, key_length)

# Étape 2 : Analyse des fréquences
frequency_analysis(groups)

# Étape 3 : Trouver la clé
probable_key = get_key(groups)
print(f"\nClé probable : {probable_key}")

# Étape 4 : Décryptage du message
decrypted_message = decrypt_vigenere(message, probable_key)
print(f"\nTexte clair : {decrypted_message}")