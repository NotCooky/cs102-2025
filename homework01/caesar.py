def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    l = list(plaintext)
    for i in range(len(l)):
        newletter_value = ord(l[i]) + shift
        if 97 <= ord(l[i]) <= 122:
            if newletter_value > ord('z'):
                newletter_value = newletter_value - 26
            l[i] = chr(newletter_value)
        elif 65 <= ord(l[i]) <= 90:
            if newletter_value > ord('Z'):
                newletter_value = newletter_value - 26
            l[i] = chr(newletter_value)
        ciphertext += l[i]

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    l = list(ciphertext)
    for i in range(len(l)):
        newletter_value = ord(l[i]) - shift
        if 97 <= ord(l[i]) <= 122:
            if newletter_value < ord('a'):
                newletter_value = newletter_value + 26
            l[i] = chr(newletter_value)
        elif 65 <= ord(l[i]) <= 90:
            if newletter_value < ord('A'):
                newletter_value = newletter_value + 26
            l[i] = chr(newletter_value)
        plaintext += l[i]

    return plaintext








