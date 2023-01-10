#!/usr/bin/python3

#import the crypter module & import the module which makes you print in color
import crypt 
from termcolor import colored

#mycryptWord = crypt.crypt("testtest","HI")
#print(colored("[i] Le résultat du cryptage de testtest avec Hi est :",'cyan'),end=" ")
#print(colored( mycryptWord,'yellow'))

def crackPass(cryptWord):
    salt = cryptWord[0:2]
    dictionary = open("guessCryptAndSalt_dictionary.txt", 'r')
    #Foreach passwords in the dictionary
    for word in dictionary.readlines():
        word = word.strip('\n')
        cryptPass = crypt.crypt(word, salt)
        #if the Cryptedword is equal to the crypted word,
        # then it means that we found the word that is the pass one
        if (cryptWord == cryptPass):
            return word

def main():
    passFile = open("guessCryptAndSalt_UsersAndHash.txt",'r')
    #Foreach lines in the UsersAndHash file
    for line in passFile.readlines(): 
        if ":" in line:
            #User in the guessCryptAndSalt_UsersAndHash.txt
            user = line.split(':')[0] 
            #Crypted password in the guessCryptAndSalt_UsersAndHash.txt
            cryptWord = line.split(':')[1].strip(' ').strip('\n')
            # password in the guessCryptAndSalt_UsersAndHash.txt
            password = crackPass(cryptWord)
            #Write the User
            print(colored("\n[i] The user is : ",'cyan'),end="")
            print(colored(user,'yellow'))
            if password == None:
                print(colored("[-] Password not found",'red'))
            else:
                print(colored("[+] Password Founded : ",'green'), password)
                #Remove this Break if you want to try with every passwords in the dictionary even if u find the right one
                break
main()
