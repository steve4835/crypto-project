import hashlib
import string
import random

NUM_TRIALS = 50
#using hex digits througout code instead of binary, for simplicity
#this is our puzzle P, we just take different size slices of the same hex value
B_BASE = '3d0a'
ALPHANUMERIC = string.ascii_lowercase + string.ascii_uppercase + string.digits
STR_LEN = 32

print("Using {0} trials for each B".format(NUM_TRIALS))

for b in [1, 2, 3, 4]:
    B = B_BASE[:b]
    stats = []
    for i in range(0, NUM_TRIALS):
        tries = 0
        digest = ''
        while digest[-b:] != B:
            tries += 1
            hash = hashlib.new('sha256')
            rand_string = ''.join(random.choice(ALPHANUMERIC) for i in range(STR_LEN))
            hash.update(rand_string.encode('utf-8'))
            digest = hash.digest().hex()
        stats.append(tries)
        mn = min(stats)
        mx = max(stats)
        avg = sum(stats)/len(stats)

    print("Stats for B={0}: min:{1}  max:{2}  avg:{3}".format(b*4, mn, mx, avg))
