import math
import time

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
    def prime_range(m, n):
        prime = [True for i in range(n+1)]
        p = 2
        prime[0] = False
        prime[1] = False

        while(p**2 < n):
            if prime[p]:
                for i in range(2*p, n+1, p):
                    prime[i] = False
            p += 1

        return [i for i in range(m, len(prime)) if prime[i]]

    @staticmethod
    def factorize(n):
        start = time.time_ns()
        factors = []
        while n % 2 == 0:
            factors.append(2)
            n = n / 2
        i = 3
        while n != 1:
            while n % i== 0:
                factors.append(i)
                n = n / i
            i += 2
        end = time.time_ns()
        factors.append((end - start) / 10**6)
        return factors

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

        e = RSA.find_e(totient)

        #generate private key
        d = RSA.table_method(totient, e)

        return dict(pub=[e,n], priv=[d, p, q])

    @staticmethod
    def find_e(totient):
        for e in range(3, totient):
            if math.gcd(e, totient) == 1:
               return e

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
        n = priv[1] * priv[2]
        self.message = [pow(m, d, n) for m in self.message]
        self.encrypted = False

if __name__ == "__main__":
    print("***RSA implementation demonstration***")
    message = "rsa"
    m = RSA(message)
    print("plaintext message: ", m.get_message(), "\n", m.message)
    keys = RSA.generate_keypair(1000, 10000)
    print("keys: {0}\n".format(keys))
    m.encrypt(keys['pub'])
    print("encrypted message: ", m.get_message(), "\n", m.message, "\n")
    m.decrypt(keys['priv'])
    print("decrypted message: ", m.get_message(), "\n", m.message, "\n\n")

    #routine to test the time complexity of factoring the public key
    print("***Demonstrating time complexity to break RSA***")
    print("Generating list of primes...")
    primes = RSA.prime_range(1, 100000000)
    for i in range(1, 13):
        a = primes[int(10**(i/2))] * primes[int(10**((i+1)/2))]
        factors = RSA.factorize(a)
        print("\nn: {0}\nKey length: {1}".format(
              a,
              len(str(a))))
        print("Factors of n (p and q):", factors[:-1])
        totient = (factors[0] - 1) * (factors[1] - 1)
        print("Totient value for RSA algorithm: {0}".format(totient))
        start = time.time_ns()
        e = RSA.find_e(totient)
        d = RSA.table_method(totient, e)
        end = time.time_ns()
        time_taken = factors[2] + ((end - start) / 10**6)
        print("d:", d)
        print("Total time taken to factorize n and calculate d: {0:.2f}ms".format(time_taken))
