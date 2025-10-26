from operator import index


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    extended_key = ""

    if len(keyword) < len(plaintext):
        for i in range(len(plaintext)):
            extended_key += keyword[i % len(keyword)]
    else:
        extended_key = keyword

    caps = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    lows = list("abcdefghijklmnopqrstuvwxyz")

    for i in range(len(plaintext)):
        char = plaintext[i]
        key_char = extended_key[i]
        if char in caps or char in lows:
            if char in caps:
                new_pos = (caps.index(char) + caps.index(key_char.upper())) % 26
                ciphertext += caps[new_pos]
            elif char in lows:
                new_pos = (lows.index(char) + lows.index(key_char.lower())) % 26
                ciphertext += lows[new_pos]
        else:
            ciphertext += char

    return ciphertext

    return extended_key


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    extended_key = ""

    if len(keyword) < len(ciphertext):
        for i in range(len(ciphertext)):
            extended_key += keyword[i % len(keyword)]
    else:
        extended_key = keyword

    caps = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    lows = list("abcdefghijklmnopqrstuvwxyz")

    for i in range(len(ciphertext)):
        char = ciphertext[i]
        key_char = extended_key[i]
        if char in caps or char in lows:
            if char in caps:
                new_pos = (caps.index(char) - caps.index(key_char.upper())) % 26
                plaintext += caps[new_pos]
            elif char in lows:
                new_pos = (lows.index(char) - lows.index(key_char.lower())) % 26
                plaintext += lows[new_pos]
        else:
            plaintext += char

    return plaintext
