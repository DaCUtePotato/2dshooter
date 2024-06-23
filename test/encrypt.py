# Unconventional and fun encryption methods

def reverse_string(input_string):
    return input_string[::-1]

def caesar_cipher(input_string, shift):
    result = []
    for char in input_string:
        if char.isalpha():
            shift_base = ord('a') if char.islower() else ord('A')
            result.append(chr((ord(char) - shift_base + shift) % 26 + shift_base))
        else:
            result.append(char)
    return ''.join(result)

def rot13(input_string):
    return caesar_cipher(input_string, 13)

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
    'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
    'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-',
    'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '0': '-----', ', ': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-',
    '(': '-.--.', ')': '-.--.-', ' ': '/'
}

def morse_code(input_string):
    return ' '.join(MORSE_CODE_DICT[char.upper()] if char.upper() in MORSE_CODE_DICT else char for char in input_string)

EMOJI_DICT = {
    'a': '😀', 'b': '😁', 'c': '😂', 'd': '🤣', 'e': '😃', 'f': '😄', 'g': '😅', 'h': '😆',
    'i': '😉', 'j': '😊', 'k': '😋', 'l': '😎', 'm': '😍', 'n': '😘', 'o': '😗', 'p': '😙',
    'q': '😚', 'r': '☺️', 's': '🙂', 't': '🤗', 'u': '🤩', 'v': '🤔', 'w': '🤨', 'x': '😐',
    'y': '😑', 'z': '😶', 'A': '😇', 'B': '🥰', 'C': '😋', 'D': '😎', 'E': '😍', 'F': '😘',
    'G': '😗', 'H': '😙', 'I': '😚', 'J': '☺️', 'K': '🙂', 'L': '🤗', 'M': '🤩', 'N': '🤔',
    'O': '🤨', 'P': '😐', 'Q': '😑', 'R': '😶', 'S': '😇', 'T': '🥰', 'U': '😋', 'V': '😎',
    'W': '😍', 'X': '😘', 'Y': '😗', 'Z': '😙', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣',
    '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣', '0': '0️⃣', ' ': '⬜'
}

def emoji_encrypt(input_string):
    return ''.join(EMOJI_DICT[char] if char in EMOJI_DICT else char for char in input_string)

def main():
    input_string = "Hello, World! 123"
    shift = 3

    print(f"Original string: {input_string}")

    # Reverse String
    reversed_string = reverse_string(input_string)
    print(f"Reversed string: {reversed_string}")

    # Caesar Cipher
    caesar_encrypted = caesar_cipher(input_string, shift)
    print(f"Caesar Cipher (shift {shift}): {caesar_encrypted}")

    # ROT13
    rot13_encrypted = rot13(input_string)
    print(f"ROT13: {rot13_encrypted}")

    # Morse Code
    morse_encoded = morse_code(input_string)
    print(f"Morse Code: {morse_encoded}")

    # Emoji Encryption
    emoji_encrypted = emoji_encrypt(input_string)
    print(f"Emoji Encrypted: {emoji_encrypted}")

if __name__ == "__main__":
    main()
