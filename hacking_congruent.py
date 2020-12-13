from random import randint
from random import uniform
import basis_reduction.basis_reduction as br


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)
 
# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n
    
def generate_and_get_public_key_congruential():
    q = randint(100000000000, 999000000000)
    f = 0
    g = 0
    
    while gcd(f, q*g) != 1:
        f = randint(round(sqrt(q/3)), round(sqrt(q/2)))
        g = randint(round(sqrt(q/4)),round(sqrt(q/2)))
        
#     q = 122430513841
#     f = 231231
#     g = 195698
        
    h = (mulinv(f,q) * g) % q
    
    print('Large integer module (q): ', q)
    print('First secret integer (f): ', f)
    print('Second secret integer (g): ', g)
    print('(f^-1 * g) mod q (h): ', h)
    print(f"public key: ({q}, {h})")
    
    return (q,h)

def encrypt_congruential(qh, m):
    assert len(qh) == 2
    q = qh[0]
    h = qh[1]
    assert 0 < m < sqrt(q/4)
    
#     r = 101010
    r = randint(0, round(sqrt(q/2)))

    e = (r*h + m)%q
    
    print('Random value for chipher (r): ', r)
    print('Plaintext: ', m)
    print('Chiphertext: ', e)
    
    return e

def decrypt_congruential_gaussian(public_key, encr_msg):
    assert len(public_key) == 2
    
    q = public_key[0]
    h = public_key[1]
    
    reduction_basis = br.gaussian_reduction([1, h], [0, q])
    shortest_vec = br.shortest_vector(reduction_basis)
    
    F = shortest_vec[0]
    G = shortest_vec[1]
    
    a = (F * encr_msg) % q
    
    res = (mulinv(F,G) * a) % G
    
    print(f"Lattice basis [(1,h), (0, q)]: [(1, {h}), (0, {q})]")
    print('Reduction basis after Gaussian reduction: ', reduction_basis)
    print('Shortest vector (F, G): ', shortest_vec)
    print('Decrypted message: ', res)
    
    return res
    
public_key_congruential = generate_and_get_public_key_congruential()

msg = 123456

encr_msg_congruential = encrypt_congruential(public_key_congruential, msg)

decrypt_congruential_gaussian_res = decrypt_congruential_gaussian(public_key_congruential, encr_msg_congruential)

if str(decrypt_congruential_gaussian_res) == str(msg):
    print('Success! :)')
else:
    print('Fail! :(')
print('Message: ', msg)
print('Result: ', decrypt_congruential_gaussian_res)