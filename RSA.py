import math

class RSA(object):
    @staticmethod
    def is_prime(n):
        if n == 2:
            return True
        for x in range(2, max(n // 2, 3)):
            if n % x == 0:
                return False
        return True

    @staticmethod
    def prime_range(n, m):
        return [x for x in range(n, m) if RSA.is_prime(x)]

    @staticmethod
    def factorize(n):
        pass

    @staticmethod
    def generate_keypair(min, max):
        first = 10
        second = 19

        #generate public key
        primes = RSA.prime_range(min, max)
        p = primes[first - 1]
        q = primes[second - 1]
        n = p * q
        totient = (p - 1) * (q - 1)

        for e in range(3, totient):
            if math.gcd(e, totient) == 1:
               break

        #generate private key
        d = RSA.table_method(totient, e)

        return dict(pub=[e,n], priv=[d, n])

    @staticmethod
    def table_method(totient, e):
        #euler's exended algo from youtube video
        #https://youtu.be/Z8M2BTscoD4?t=660

        t = [[totient, totient], [e, 1]]

        while t[1][0] != 1:
            a = t[0][0] // t[1][0]
            t.append([t[1][0] * a, t[1][1] * a])
            t[2] = [t[0][0] - t[2][0], t[0][1] - t[2][1]]
            if t[2][1] < 0:
                t[2][1] %= totient
            t.pop(0)

        return t[1][1]


    def __init__(self, m):
        self.encrypted = False
        self.message = []
        m = m.lower()
        self.message = [ord(char) - 97 for char in m]

    def get_message(self):
        if self.encrypted:
            return 'gobbledygook'
        return "".join([chr(a + 97) for a in self.message])

    def encrypt(self, pub):
        if self.encrypted:
            return
        e = pub[0]
        n = pub[1]
        self.message = [pow(m, e, n) for m in self.message]
        self.encrypted = True

    def decrypt(self, priv):
        if not self.encrypted:
            return
        d = priv[0]
        n = priv[1]
        self.message = [pow(m, d, n) for m in self.message]
        self.encrypted = False

if __name__ == "__main__":
    message = input("Type message to be encrypted: ")
    m = RSA(message)
    print("plaintext message: ", m.get_message(), "\n", m.message)
    keys = RSA.generate_keypair(1000, 10000)
    print("keys: ", keys)
    m.encrypt(keys['pub'])
    print("encrypted message: ", m.get_message(), "\n", m.message)
    m.decrypt(keys['priv'])
    print("decrypted message: ", m.get_message(), "\n", m.message)

