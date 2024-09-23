import numpy as np
from numpy.polynomial import polynomial as poly

# Parameters
n = 256  # Lattice dimension
q = 8380417  # Modulus
d = 13  # Bit length of challenge
tau = 60  # Number of +-1's in the challenge
eta = 2  # Coefficient range for secret key

def ntt(a):
    """Number Theoretic Transform (simplified)"""
    return np.fft.rfft(a)

def intt(a):
    """Inverse Number Theoretic Transform (simplified)"""
    return np.fft.irfft(a, n=n).real.astype(np.int32)

def mod_q(x):
    """Modulo q operation that works with arrays"""
    return np.mod(x.astype(np.int64), q).astype(np.int32)

def poly_mul_mod(a, b):
    """Polynomial multiplication modulo x^n + 1 and q"""
    c = poly.polymul(a, b)
    c_padded = np.pad(c, (0, 2*n - len(c)))  # Pad to length 2n
    return mod_q(c_padded[:n] - c_padded[n:2*n])

def generate_keypair():
    """Generate a key pair"""
    s = np.random.randint(-eta, eta+1, size=n, dtype=np.int32)
    a = np.random.randint(0, q, size=n, dtype=np.int32)
    t = mod_q(poly_mul_mod(a, s) + np.random.randint(-eta, eta+1, size=n, dtype=np.int32))
    return (s, a), t

def generate_key_shares(t, num_shares, threshold):
    """Generate key shares using Shamir's Secret Sharing"""
    coeffs = np.random.randint(0, q, size=(threshold-1, n), dtype=np.int32)
    coeffs = np.vstack([t, coeffs])
    
    shares = []
    for i in range(1, num_shares + 1):
        share = np.zeros(n, dtype=np.int32)
        for j in range(threshold):
            share = mod_q(share + coeffs[j] * (i ** j))
        shares.append((i, share))
    
    return shares

def sign_partial(s, message, a):
    """Generate a partial signature"""
    y = np.random.randint(-2**d, 2**d, size=n, dtype=np.int32)
    w = mod_q(ntt(poly_mul_mod(a, y)))
    c = np.random.choice([-1, 0, 1], size=n, p=[1/(2*tau), 1-1/tau, 1/(2*tau)])
    z = mod_q(y + poly_mul_mod(s, c))
    return z, c

def combine_signatures(partial_sigs, indices, t):
    """Combine partial signatures"""
    lambda_i = lagrange_interpolation(indices, 0, q)
    z = np.zeros(n, dtype=np.int32)
    for (i, partial_z), l in zip(partial_sigs, lambda_i):
        z = mod_q(z + l * partial_z)
    return z

def verify_signature(t, message, z, c, a):
    """Verify the signature"""
    w1 = mod_q(ntt(poly_mul_mod(a, z)))
    w2 = mod_q(ntt(poly_mul_mod(t, c)))
    return np.allclose(mod_q(w1 - w2), mod_q(ntt(poly_mul_mod(a, z) - poly_mul_mod(t, c))))

def lagrange_interpolation(indices, x, prime):
    """Lagrange interpolation for Shamir's Secret Sharing"""
    result = []
    for i in indices:
        numerator, denominator = 1, 1
        for j in indices:
            if i != j:
                numerator = (numerator * (x - j)) % prime
                denominator = (denominator * (i - j)) % prime
        result.append((numerator * pow(denominator, -1, prime)) % prime)
    return result

# Example usage
threshold = 3
num_shares = 5

# Key generation
(s, a), t = generate_keypair()
shares = generate_key_shares(t, num_shares, threshold)

# Signing
message = b"Hello, threshold signature!"
partial_sigs = []
for i in range(threshold):
    z, c = sign_partial(shares[i][1], message, a)
    partial_sigs.append((shares[i][0], z))

# Combining signatures
indices = [share[0] for share in shares[:threshold]]
combined_z = combine_signatures(partial_sigs, indices, t)

# Verification
is_valid = verify_signature(t, message, combined_z, c, a)

print("Is the signature valid?", is_valid)