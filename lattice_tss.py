import numpy as np
from hashlib import sha256

# Constants
q = 12289  # Prime modulus
k, l = 4, 4  # Dimensions of the matrices
eta = 2  # Coefficient bound
N = 16  # Degree of polynomials

# Generate a random matrix A
def generate_matrix(k, l, q):
    return np.random.randint(0, q, size=(k, l))

# Sample a secret key vector
def sample_secret(l, eta, q):
    return np.random.randint(-eta, eta + 1, size=l) % q

# Sample an error vector
def sample_error(k, eta, q):
    return np.random.randint(-eta, eta + 1, size=k) % q

# Lattice multiplication (for demonstration purposes)
def lattice_multiply(A, s, q):
    return np.dot(A, s) % q

# Helper functions for Shamir's Secret Sharing
def shamir_share(secret, threshold, num_shares):
    # Ensure the secret is a scalar
    if isinstance(secret, np.ndarray):
        secret = secret[0]
    # Generate random coefficients for a polynomial of degree (threshold - 1)
    coeffs = [secret] + [np.random.randint(0, q) for _ in range(threshold - 1)]
    shares = [(i, np.polyval(coeffs, i) % q) for i in range(1, num_shares + 1)]
    return shares

def shamir_reconstruct(shares, q):
    def lagrange_basis(i, x, x_s):
        basis = 1
        for j, x_j in enumerate(x_s):
            if j != i:
                basis *= (x - x_j) * pow(x_i - x_j, -1, q) % q
        return basis

    x_s, y_s = zip(*shares)
    secret = sum(yi * lagrange_basis(i, 0, x_s) for i, yi in enumerate(y_s)) % q
    return secret

# Distributed key generation (DKeyGen)
def distributed_key_generation(num_parties, threshold):
    A = generate_matrix(k, l, q)  # Generate a random matrix A
    s = sample_secret(l, eta, q)  # Sample a secret key vector
    e = sample_error(k, eta, q)  # Sample an error vector

    t = (np.dot(A, s) + e) % q  # Compute t = As + e

    # Shamir's Secret Sharing
    secret_shares = shamir_share(s, threshold, num_parties)
    return A, t, secret_shares

# Share Refreshment
### This protocol refreshes the secret shares to prevent an attacker from gathering information over time
def refresh_shares(secret_shares, q):
    # Generate fresh shares of zero and add to the existing shares
    zero_shares = shamir_share(0, len(secret_shares), len(secret_shares))
    refreshed_shares = [(x, (y + y_zero) % q) for (x, y), (_, y_zero) in zip(secret_shares, zero_shares)]
    return refreshed_shares

def hash_message(message):
    # Hash the message to create a challenge
    return int(sha256(message.encode()).hexdigest(), 16) % q

def sign_message(secret_share, message, q):
    # Sign a message with a secret share
    challenge = hash_message(message)
    signature = (secret_share[1] + challenge) % q
    return signature

def combine_signatures(signatures, q):
    # Combine individual signatures into a final signature
    final_signature = sum(signatures) % q
    return final_signature

# Distributed Signing (DSign)
def distributed_signing(secret_shares, message, q):
    # Step 1: Generate individual shares of random values used in the signature process
    random_shares = [np.random.randint(0, q) for _ in secret_shares]

    # Step 2: Compute a commitment and a challenge using a hash function
    commitment = sum(random_shares) % q
    challenge = hash_message(message + str(commitment))

    # Step 3: Generate individual parts of the signature using the challenge and secret key shares
    partial_signatures = [(share[1] + challenge * random_share) % q for share, random_share in zip(secret_shares, random_shares)]

    # Step 4: Combine the individual parts into a single signature
    final_signature = combine_signatures(partial_signatures, q)
    return final_signature

# Example
A, t, shares = distributed_key_generation(num_parties=5, threshold=3)
print("Matrix A:", A)
print("Public key t:", t)
print("Secret shares:", shares)

refreshed_shares = refresh_shares(shares, q)
print("Refreshed shares:", refreshed_shares)

message = "Test message"
signatures = [sign_message(share, message, q) for share in refreshed_shares]
final_signature = combine_signatures(signatures, q)
print("Final signature:", final_signature)

# Distributed Signing Example
distributed_signature = distributed_signing(refreshed_shares, message, q)
print("Distributed signature:", distributed_signature)