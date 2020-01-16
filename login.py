
import getpass
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

username = input("Username: ").encode("utf-8")
password = getpass.getpass().encode("utf-8")

cipher_text_un = cipher_suite.encrypt(username)
cipher_text_pw = cipher_suite.encrypt(password)

################ Configs -Decrypt imported file


username = cipher_suite.decrypt(cipher_text_un).decode("utf-8", "strict")
_这不是密码 = cipher_suite.decrypt(cipher_text_pw).decode("utf-8", "strict")

def getCipherText():
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    username = input("Username: ").encode("utf-8")
    password = getpass.getpass().encode("utf-8")

    cipher_text_un = cipher_suite.encrypt(username)
    cipher_text_pw = cipher_suite.encrypt(password)

    encryption_list = [key.decode("utf-8"), cipher_text_un.decode("utf-8"), cipher_text_pw.decode("utf-8")]

    file = filepath  # Put full filepath here where you want encrypted password to be stored
    out_file = open(file, "w")

    for line in encryption_list:
        out_file.write(line)
        out_file.write("\n")
    out_file.close()

    
options = {
    'server': 'https://jira.arbfund.com'
    }
jira = JIRA(options, basic_auth = (username, password))
