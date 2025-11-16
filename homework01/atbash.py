def encrypt_atbash(plaintext):
    result = []

    for char in plaintext:
        code = ord(char)

        if ord("а") <= code <= ord("я"):
            # new_code = start + (end - current)
            result.append(chr(ord("я") - (code - ord("а"))))
        elif ord("А") <= code <= ord("Я"):
            result.append(chr(ord("Я") - (code - ord("А"))))
        elif code == ord("ё"):
            result.append("э")
        elif code == ord("Ё"):
            result.append("Э")
        elif code == ord("э"):
            result.append("ё")
        elif code == ord("Э"):
            result.append("Ё")
        else:
            result.append(char)

    return "".join(result)
