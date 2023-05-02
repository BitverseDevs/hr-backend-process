# A B C D E F G H I J K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z  
# 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
#  ! " # $ % & ' ( ) * + , - . / : ; < = > ? @ [ \ ] ^ _ ` { | } ~

special_characters = [' ', '!', '"', '#', '$', '%', '&', '\'', '\(', '\)', '*', '+', ',', 
                      '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '\[', '\]', '\\', 
                      '^', '_', '\`', '\{', '\}', '\|', '\~']

class Hash:
    def __init__(self, key_code):
        self.key_code = key_code

    def encrypt(self, password):
        encrypted_text = []
        counter = 0

        for letter in password.upper():
            if counter == len(self.key_code):
                counter = 0

            if letter in special_characters:
                encrypted_text.append(letter)

            number = ord(letter) + self.key_code[counter]
            if number > 90:
                number -= 26

            encrypted_text.append(chr(number))
            counter += 1

        msg = ""
        return msg.join(encrypted_text)
    
    def decrypt(self, ciphered_text):
        decrypted_text = []
        counter = 0

        for letter in ciphered_text:
            if counter == len(self.key_code):
                counter = 0

            if letter in special_characters:
                decrypted_text.append(letter)

            number = ord(letter) - self.key_code[counter]
            if number < 65:
                number += 26
            
            decrypted_text.append(chr(number))
            counter +=1

        msg = ""
        return msg.join(decrypted_text)