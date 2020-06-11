import numpy as np


def MainMenu():
    print("========== Linear Algebra Program ==========\n"
          "1. Encryption\n"
          "2. Decryption\n"
          "3. Exit\n")
    choice = int(input("Selection: "))
    if(choice == 1):
        print("~~~~~ Encryption Program ~~~~~")
        encryption()
    elif(choice == 2):
        print("~~~~~ Decryption Program ~~~~~")
        decryption()
    elif(choice == 3):
        print("Thank you for using our program")
    else:
        print("Invalid Choice, try again")

def encryption():
    # enter an input with an upper output (ascii from 65-90)
    plain_text = input("Enter message: ").upper()

    # if the message length is odd, append 0 at the end and at the decrypt, remove it
    len_check = 0
    if (len(plain_text) % 2 != 0):
        plain_text += "0"
        len_check = 1

    # plain_text in matrix
    # we use a 2x2 matrices
    # initializing an empty matrix by using np.zeros
    row = 2
    col = int(len(plain_text)/2)
    text2m = np.zeros((row,col), dtype=int)

    itr1 = 0
    itr2 = 0
    for i in range(len(plain_text)):
        if(i % 2 == 0):
            text2m[0][itr1] = int(ord(plain_text[i])-65)
            itr1 += 1
        else:
            text2m[1][itr2] = int(ord(plain_text[i])-65)
            itr2 += 1

    # create a key nxn matrices
    key = input("Enter 4 letter key string: ").upper()

    # initializing an empty key by using np.zeros
    key2m = np.zeros((2,2), dtype=int)
    itr3 = 0
    for i in range(2):
        for j in range(2):
            key2m[i][j] = int(ord(key[itr3]) - 65)
            itr3 += 1


    # checking the validity of the key
    # the key has to be invertible
    # first, find the determinant (ad - bc)
    # 26 is the length of how many alphabets
    determinant = key2m[0][0] * key2m[1][1] - key2m[0][1] * key2m[1][0]
    determinant = determinant % 26

    # find the multiplicative inverse
    multi_inv = -1
    for i in range(26):
        current_inv = determinant * i
        if(current_inv % 26 == 1):
            multi_inv = i
            break
        else:
            continue

    if(multi_inv == -1):
        print("Invalid key, try again")


    # to get the cipher text (key*plaintext)
    encryp_text = ""
    x = int(len(plain_text)/2)
    if(len_check == 0):
        for i in range(x):
            row1 = key2m[0][0] * text2m[0][i] + key2m[0][1] * text2m[1][i]
            encryp_text = encryp_text + chr((row1 % 26) + 65)
            row2 = key2m[1][0] * text2m[0][i] + key2m[1][1] * text2m[1][i]
            encryp_text = encryp_text + chr((row2 % 26) + 65)
    else:
        for i in range(x-1): # we have to subtract it with 1 ro reduce the 0 from the message's length
            row1 = key2m[0][0] * text2m[0][i] + key2m[0][1] * text2m[1][i]
            encryp_text = encryp_text + chr((row1 % 26) + 65)
            row2 = key2m[1][0] * text2m[0][i] + key2m[1][1] * text2m[1][i]
            encryp_text = encryp_text + chr((row2 % 26) + 65)

    print("Encrypted text is: {}".format(encryp_text))

def decryption():
    encryp_text = input("Enter the Encrypted text: ").upper()

    # if the length of the message is odd
    len_check = 0
    if(len(encryp_text) % 2 != 0):
        encryp_text += "0"
        len_check = 1

    # create matrix for encrypted text
    row = 2
    col = int(len(encryp_text)/2)
    text2m = np.zeros((row,col), dtype= int)

    itr1 = 0
    itr2 = 0
    for i in range(len(encryp_text)):
        if(i % 2 == 0):
            text2m[0][itr1] = ord(encryp_text[i]) - 65
            itr1 += 1
        else:
            text2m[1][itr2] = ord(encryp_text[i]) - 65
            itr2 += 1

    # create matrix for inverse key
    # using 2x2 matrices
    invkey = input("Input 4 letter key string: ").upper()

    itr3 = 0
    invkey2m = np.zeros((2,2), dtype= int)
    for i in range(2):
        for j in range(2):
            invkey2m[i][j] = ord(invkey[itr3])-65
            itr3 += 1

    # determinant
    determinant = invkey2m[0][0] * invkey2m[1][1] - invkey2m[0][1] * invkey2m[1][0]
    determinant = determinant % 26

    # multiplicative inverse
    mul_inv = -1
    for i in range(26):
        current_inv = determinant * i
        if(current_inv % 26 == 1):
            mul_inv = i
            break
        else:
            continue

    # key in decryption is already being inversed
    # inverse's rule =
    # [d  -b] * multiplicative inverse
    # [-c  a]
    # find the adjoint
    # swap it first between d and a
    invkey2m[0][0], invkey2m[1][1] = invkey2m[1][1], invkey2m[0][0]

    # give minus to c and b
    invkey2m[0][1] *= -1
    invkey2m[1][0] *= -1

    # multiplying the multiple inverse and the adjoint
    for i in range(2):
        for j in range(2):
            invkey2m[i][j] *= mul_inv
            invkey2m[i][j] = invkey2m[i][j] % 26


    # create decrypted result by inverse*encrypted result
    decryp_text = ""
    x = int(len(encryp_text)/2)
    if(len_check == 0):
        for i in range(x):
            row1 = invkey2m[0][0] * text2m[0][i] + invkey2m[0][1] * text2m[1][i]
            decryp_text = decryp_text + chr((row1 % 26) + 65)
            row2 = invkey2m[1][0] * text2m[0][i] + invkey2m[1][1] * text2m[1][i]
            decryp_text = decryp_text + chr((row2 % 26) + 65)
    else:
        for i in range(x-1): # we have to subtract it with 1 ro reduce the 0 from the message's length
            row1 = invkey2m[0][0] * text2m[0][i] + invkey2m[0][1] * text2m[1][i]
            decryp_text = decryp_text + chr((row1 % 26) + 65)
            row2 = invkey2m[1][0] * text2m[0][i] + invkey2m[1][1] * text2m[1][i]
            decryp_text = decryp_text + chr((row2 % 26) + 65)

    print("Decrypted text is: {}".format(decryp_text))




MainMenu()




