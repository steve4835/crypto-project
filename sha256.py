import hashlib
import string
import random

NUM_TRIALS = 25
# using hex digits throughout code instead of binary, for simplicity
# this is the puzzle P, just take different size slices of the same hex value for
# different sizes of B
B_BASE = '7d1a'
ALPHANUMERIC = string.ascii_lowercase + string.ascii_uppercase + string.digits
STR_LEN = 32

print("Using {0} trials for each B".format(NUM_TRIALS))

for b in [1, 2, 3, 4]:
    # Alice creates her puzzle
    B = B_BASE[:b]
    stats = []

    # average number of tries over many trials and store the stats in an array for analysis
    for i in range(NUM_TRIALS):
        tries = 0
        digest = ''
        # Bob tries to find a collision for the last (b * 4) bits
        # while the last b digits of the digest are not equal to B
        while digest[-b:] != B:
            tries += 1
            # create a new sha256 hash object, generate a random string, hash the string,
            # and get the digest in hexadecimal
            hash = hashlib.new('sha256')
            rand_string = ''.join(random.choice(ALPHANUMERIC) for i in range(STR_LEN))
            hash.update(rand_string.encode('utf-8'))
            digest = hash.digest().hex()

        stats.append(tries)

    print("Stats for B={0}: min:{1}  max:{2}  avg:{3}".format(
        b * 4, min(stats), max(stats), sum(stats) / len(stats)))
