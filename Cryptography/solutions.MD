# Part A:

## Recovered passwords
a) password for suleman is 63953293
b) password for mazharul is 11232020

## Pseudocode for attack

START
define HASH_SHA256 as the function for calculating the Sha-256 hash of a "{username},{password},{salt}" string
target_hash = T
username = U
salt = S
possible_password_set = the set of all possible passwords based on password length and digit value domain
For password in possible_password_set:
    if HASH_SHA256(username,password,salt) == target_hash:
        # we got the right password. Finished
        return password
    else:
        # Wrong password. continue to crack
        continue
END

## Worst case running time
O(10^n), where n is the maximum length of the possible password.
For example, for my solution, when the maximum length of the possible password is 8, then the worst case will be that the right password is 99999999, and we will check 10^8 times to find it (since we start with "0").

## Discussion merits of current proposal
The proposal is relatively good and makes sense since SHA-256 is currently a strong hash function, and the computational cost of this proposal for encryption and decryption is also pretty low for normal users.

## Suggestions for improvement
I think the password design could be more complex (e.g., involves upper/lower case letters and symbols, longer length), and the SHA-256 hashing operation could be repeated several more times to improve the difficulty for hackers to crack.

## How to run pwcrack.py
python pwcrack.py

# Part B:

## Discussion of the current scheme
The current scheme is not safe. A hacker could easily intercept the message, change the content by modifying the iv and tag part, and then send the "corrupted" message to users.
Simply put, the integrity is not guaranteed in the current scheme.

## Suggestions for improving the scheme
Instead of attaching the sha256 digest of plaintext message, The colleague should use encrypt-then-MAC method to ensure that only user with key can modify the message, which ensure the integrity.

# Extra Credit:

## Recovered password
Wisc0nsin!

## Correct pseudocode

START
define HASH_scrypt as the function for calculating the scrypt hash of a "{username},{password},{salt}" string
target_hash = T
username = U
salt = S
password_list = Crackstation Smaller Wordlist downloaded from Internet (Human Passwords Only, "realhuman_phill.txt")
chunks = Plenty of chunks divided from password_list (for further parallelled calculation)
pool = create multiprocessing pool (for further parallelled calculation. In my computer, I set process num = 32)
For password_chunk in chunks:
    create new process in the pool, and assign a password_chunk to it.
    in each process (parallelled calculation):
        # use HASH_scrypt(username,password,salt) function to find the correct password in the assigned password_chunk
        For password in password_chunk:
            if HASH_scrypt(username,password,salt) == target_hash:
                # we got the right password. Finished
                return password
            else:
                # Wrong password. continue to crack
                continue
END

This parallelled algorithm costs around 30 min to find the correct password.




