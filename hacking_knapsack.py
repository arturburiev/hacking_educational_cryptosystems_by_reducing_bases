from math import gcd
import basis_reduction.basis_reduction as br

def get_public_key_m_n_knapsack(private_key):
    
    max_elem = max(private_key)
    m = 2 * max_elem + round((2 * max_elem)/3)
    n = 1
    public_key = []
    
    while gcd(m, n) != 1 or n == 1:
        n  += 1

    for el in private_key:
        public_key.append(el*n%m)
        
    print('Private key (r): ', private_key)
    print('A: ', m)
    print('B: ', n)
    print('Public key (M): ', public_key)
        
    return {
        'public_key': public_key,
        'm': m,
        'n': n,
    }
        
            
def encrypt_knapsack(public_key, binary_msg):
    
    assert len(public_key) != 0
    
    def grouper(iterable, n):
        args = [iter(iterable)] * n
        return zip(*args)
    
    binary_msg = str(binary_msg)
    split_msg = [''.join(i) for i in grouper(binary_msg, len(public_key))]
    encr_blocks = []
    encr_block = 0
    
    for block_split_msg in split_msg:
        for i in range(len(block_split_msg)):
            if block_split_msg[i] == '1':
                encr_block += public_key[i]
        encr_blocks.append(encr_block)
        encr_block = 0
        
    print('Plaintext (x): ', binary_msg)
    print('Chiphertext (S): ', encr_block)

    return encr_blocks
      

def decrypt_knapsack_lll(encr_blocks, public_key):
    size_matrix = len(public_key) + 1
    matrix = []
    row = []
    result_x = []
    result_decrypt_msg = ''
    
    for encr_block in encr_blocks:
    
        for i in range(len(public_key)):
            row = [0] * size_matrix
            row[i] = 2 
            row[size_matrix - 1] = public_key[i]
            matrix.append(row)
            row = []
        
        row = [1] * size_matrix
        row[size_matrix - 1] = encr_block
        matrix.append(row)
        
        print('Subset sum matrix: ', matrix)

        if len(matrix) > 0:
            matrix_reduced = br.lll_reduction(matrix, 0.75)
            
            print('Reduced matrix with LLL: ', matrix_reduced)
            
            shortest_vec = br.shortest_vector(matrix_reduced)
            
            print('Shortest vector: ', shortest_vec)
            
            for i in range(len(shortest_vec)):
                if i != len(shortest_vec)-1:
                    if shortest_vec[i] == -1:
                        result_x.append('1')
                    else:
                        result_x.append('0')
                        
            print('Decrypted block of message: ', ''.join(result_x))
                
            result_decrypt_msg += ''.join(result_x)

            print('---\n')
            
            result_x = []
            matrix = []
            row = []
            
    print('Decrypted message: ', result_decrypt_msg)
        
    return result_decrypt_msg
    
public_key = []
public_key = get_public_key_m_n_knapsack([1, 2, 4, 10, 20, 40])['public_key']

msg = '100100111100101110'
encr_blocks = encrypt_knapsack(public_key, msg)

descrypt_msg = decrypt_knapsack_lll(encr_blocks, public_key)

if str(descrypt_msg) == str(msg):
    print('Success! :)')
else:
    print('Fail! :(')
print('Message: ', msg)
print('Result: ', descrypt_msg)