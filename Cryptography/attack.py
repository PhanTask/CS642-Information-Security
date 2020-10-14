# /usr/bin/env python3

# CS 642 University of Wisconsin
#
# usage: python3 attack.py ciphertext
# Outputs a modified ciphertext and tag

import sys
import hashlib

# Grab ciphertext from first argument
ciphertextWithTag = bytes.fromhex(sys.argv[1])

if len(ciphertextWithTag) < 16+16+32:
  print("Ciphertext is too short!")
  sys.exit(0)

iv = ciphertextWithTag[:16]
ciphertext = ciphertextWithTag[16:len(ciphertextWithTag)-32] # without iv

# Modify the input so the transfer amount is more lucrative to the recipient
message = \
"""AMOUNT: $  99.00
Originating Acc Holder: Badger
Orgininating Acc #82123-098370

I authorized the above amount to be transferred to the account #38108-443280
held by a Wisc student at the National Bank of the Cayman Islands.
"""

iv = iv[:11] + bytes([iv[11] + 8]) + bytes([iv[12] + 9]) + iv[13:]
tag = hashlib.sha256(message.encode()).hexdigest()

# Print the new encrypted message
# you can change the print content if necessary
print(iv.hex() + ciphertext.hex() + tag)
