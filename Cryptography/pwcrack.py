import hashlib
import itertools

# Hash function using SHA-256
def hash_sha256(params):
    return hashlib.sha256(params.encode()).hexdigest()

# Cracking function
def crack_password(user_dict):
    return next(pw for pw in itertools.count() if hash_sha256(user_dict['name']+','+str(pw)+','+user_dict['salt']) == user_dict['target_sha256'])

if __name__ == "__main__":
    # You can directly run this .py file like: python pwcrack.py
    suleman = {'name':'suleman',
               'salt':'20202293',
               'target_sha256':"53b8da235e6ab04edfe2d73dfd976d4ab26e2bf4e356840ca8104c24a22af139"
               }

    mazharul = {'name':'mazharul',
               'salt':'20193833',
               'target_sha256':"c9808f6d88ffb8089d44b903aed1e09be2d7432be46db8c06c273ca65a0e6fe7"
               }

    suleman_pw = crack_password(suleman)
    print("password for suleman is", suleman_pw)
    mazharul_pw = crack_password(mazharul)
    print("password for mazharul is", mazharul_pw)
