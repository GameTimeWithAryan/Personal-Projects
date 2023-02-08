# Utility Function to print everything nicely
def print_information(sentence: str, key, plain_text: str, cipher_text: str):
    print(f"Plain Text: {sentence}")
    print(f"Key: {key}")
    print(f"Encrypted Text: {plain_text}")
    print(f"Decrypted Text: {cipher_text}")


def print_info_with_cipher(cipher: str, key, cipher_text: str):
    print(f"Cipher Used: {cipher}")
    print(f"Key: {key}")
    print(f"Cipher Text: {cipher_text}\n")


# Vigenère Cipher
class VigenereCipher:
    def __init__(self, keyword: str, uppercase: bool = True):
        self.keyword = keyword
        self.uppercase = uppercase

    def get_encryption_key(self, length: int):
        # Making keyword string as the same length as the plain_text for encryption
        # Shorter code using list comprehensions
        # encryption_key = "".join([keyword[index % len(keyword)] for index in range(length)])

        # More readable code using string operators
        # keyword_len = len(keyword)
        # repetition = length // keyword_len
        # remainder = length % keyword_len
        # encryption_key = keyword * repetition + keyword[:remainder]

        encryption_key = ""
        for index in range(length):
            encryption_key += self.keyword[index % len(self.keyword)]
        return encryption_key

    def encrypt(self, plain_text: str):
        key_index = 0
        encrypted = []
        plain_text_words = plain_text.lower().split(" ")
        encryption_key = self.get_encryption_key(len(plain_text)).lower()

        for word in plain_text_words:
            encrypted_word = ""
            for char in word:
                char_code = ord(char) - 96 - 1  # to get 0-25 in numbers i.e. A=0, Z=25
                key_code = ord(encryption_key[key_index]) - 96 - 1
                encrypted_word += chr((char_code + key_code) % 26 + 97)  # Encryption
                key_index += 1
            encrypted.append(encrypted_word)
        encrypted_content = " ".join(encrypted)
        if self.uppercase:
            return encrypted_content.upper()
        return encrypted_content

    def decrypt(self, cipher_text: str):
        key_index = 0
        decrypted = []
        cipher_text_words = cipher_text.lower().split(" ")
        encryption_key = self.get_encryption_key(len(cipher_text)).lower()

        for word in cipher_text_words:
            decrypted_word = ""
            for char in word:
                char_code = ord(char) - 96 - 1
                key_code = ord(encryption_key[key_index]) - 96 - 1
                decrypted_word += chr((char_code - key_code) % 26 + 97)
                key_index += 1
            decrypted.append(decrypted_word)
        decrypted_content = " ".join(decrypted)
        if self.uppercase:
            return decrypted_content.upper()
        return decrypted_content


# Caesar Cipher
class CaesarCipher:
    def __init__(self, shift: int, uppercase: bool = True):
        self.shift = shift
        self.uppercase = uppercase

    def encrypt(self, plain_text: str):
        encrypted = []
        plain_text_words = plain_text.lower().split(" ")
        for word in plain_text_words:
            encrypted_word = ""
            for char in word:
                char_code = ord(char) - 97
                encrypted_word += chr((char_code + self.shift) % 26 + 97)
            encrypted.append(encrypted_word)
        encrypted_content = " ".join(encrypted)
        if self.uppercase:
            return encrypted_content.upper()
        return encrypted_content

    def decrypt(self, cipher_text: str):
        decrypted = []
        cipher_text_words = cipher_text.lower().split(" ")
        for word in cipher_text_words:
            decrypted_word = ""
            for char in word:
                char_code = ord(char) - 97
                decrypted_word += chr((char_code - self.shift) % 26 + 97)
            decrypted.append(decrypted_word)
        decrypted_content = " ".join(decrypted)
        if self.uppercase:
            return decrypted_content.upper()
        return decrypted_content


# PlayFair Cipher
class PlayFair:
    def __init__(self, keyword: str):
        self.PADDING = "X"
        self.keyword = keyword
        self.square = self.get_square()

    def print_square(self):
        for row in self.square:
            print(" ".join(row))

    def get_square(self):
        square = []
        square_text = ""
        for char in self.keyword:
            if char not in square_text:
                square_text += char
        for i in range(26):
            char = chr(i + 65)
            if char not in square_text and char != "J":
                square_text += char
        for i in range(0, 25, 5):
            five_group = square_text[i:i + 5]
            square.append([char for char in five_group])
        return square

    def get_pairs(self, text: str):
        pairs = []
        indices = []
        for index, char in enumerate(text):
            if index != 0 and text[index - 1] == text[index]:
                indices.append(index)
        indices.reverse()
        for index in indices:
            text = text[:index] + self.PADDING + text[index:]
        if len(text) % 2 == 1:
            text += self.PADDING
        for i in range(0, len(text), 2):
            pairs.append(text[i:i + 2])
        return pairs

    def get_indices_from_square(self, text: str or list):
        indices = []
        for text_char in text:
            for i, row in enumerate(self.square):
                for j, column_char in enumerate(row):
                    if text_char == column_char:
                        indices.append((i, j))
        return indices

    def encrypt(self, plain_text: str):
        encrypted = ""
        # plain_text will be converted into Pairs which will have Padding letter in the right places
        pairs = self.get_pairs(plain_text)
        for chars in pairs:
            if chars[0] == "J":
                chars[0] = "I"
            if chars[1] == "J":
                chars[1] = "I"
        # Converting paired list back to plain_text with Padding letters
        plain_text = [char for pair in pairs for char in pair]
        # Get indices of letters of plain_text from playfair square
        indices = self.get_indices_from_square(plain_text)

        # Play Fair Encryption
        for i in range(0, len(indices), 2):
            row1, column1 = indices[i]
            row2, column2 = indices[i + 1]
            if row1 == row2:
                encrypted += self.square[row1][(column1 + 1) % 5] + self.square[row1][(column2 + 1) % 5]
            elif column1 == column2:
                encrypted += self.square[(row1 + 1) % 5][column1] + self.square[(row2 + 1) % 5][column1]
            else:
                encrypted += self.square[row1][column2] + self.square[row2][column1]
        return encrypted

    def decrypt(self, cipher_text: str):
        decrypted = ""
        indices = self.get_indices_from_square(cipher_text)

        # Play Fair Decryption
        for i in range(0, len(indices), 2):
            row1, column1 = indices[i]
            row2, column2 = indices[i + 1]
            if row1 == row2:
                decrypted += self.square[row1][(column1 - 1) % 5] + self.square[row1][(column2 - 1) % 5]
            elif column1 == column2:
                decrypted += self.square[(row1 - 1) % 5][column1] + self.square[(row2 - 1) % 5][column1]
            else:
                decrypted += self.square[row1][column2] + self.square[row2][column1]
        return decrypted
