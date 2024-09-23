# Lattice-Based Threshold Signature Schemes (TSS)

This repository showcases two implementations of **Threshold Signature Schemes (TSS)** based on **lattice cryptography**. Lattice-based cryptography is a promising area for building post-quantum secure cryptographic schemes. These implementations demonstrate how lattice-based techniques can be used for distributed key generation and signing operations in TSS.

## Overview

In cryptography, **Threshold Signature Schemes (TSS)** allow multiple parties to collaborate on generating a digital signature without any single party holding the entire private key. The signature is only valid when enough parties (the threshold) work together to generate it. This repository focuses on two lattice-based TSS implementations:

1. **Lattice-Based TSS using a Random Matrix**: This implementation uses lattice-based operations for generating key shares and distributed signing.
2. **Simple Crystals-Dilithium-Based TSS**: A TSS scheme inspired by the Crystals-Dilithium lattice-based signature scheme, incorporating Shamir’s Secret Sharing to distribute keys.

## Implementations

### 1. `lattice_tss.py` - Lattice-Based TSS Using a Random Matrix

This implementation demonstrates how lattice-based operations can be used to distribute key shares and perform distributed signing. It involves the following steps:

- **Matrix Generation**: Generate a random matrix `A` used in the key generation.
- **Secret and Error Sampling**: Sample a secret vector `s` and error vector `e` to compute the public key `t`.
- **Shamir’s Secret Sharing**: Distribute the secret `s` into shares using Shamir's Secret Sharing.
- **Signing**: Each party uses its secret share to sign a message, and the individual signatures are combined into a final signature.
- **Share Refreshment**: Refresh the shares to protect against long-term attacks.

### 2. `simple_crystals_dilithium_scheme.py` - Crystals-Dilithium-Based TSS

This implementation builds upon the **Crystals-Dilithium** scheme, one of the most prominent lattice-based signature schemes, and integrates Shamir's Secret Sharing to create a distributed signature process. It involves:

- **Key Generation**: Generate lattice-based public and private keys using polynomial multiplication and modular operations.
- **Secret Sharing**: Use Shamir’s Secret Sharing to distribute the secret key.
- **Signing**: Each party generates a partial signature using its secret share.
- **Combining Signatures**: The partial signatures are combined using Lagrange interpolation.
- **Verification**: The combined signature is verified against the public key using lattice-based polynomial operations.

## Key Features

- **Post-Quantum Security**: Lattice-based cryptographic schemes are believed to be resistant to attacks by quantum computers, making them a promising approach for future-proof cryptographic systems.
- **Threshold Cryptography**: These schemes enable secure collaboration between multiple parties to create signatures, ensuring no single entity has complete control over the signing process.
- **Shamir's Secret Sharing**: Both implementations use Shamir’s Secret Sharing to distribute the secret key among multiple parties, ensuring security and fault tolerance.

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/rosemary-crypto/lattice-based-tss.git
cd lattice-based-tss
```

### 2. Install Dependencies

Ensure you have Python 3.x installed. Install the necessary dependencies using `pip`:

```bash
pip install numpy
```

### 3. Running the Lattice-Based TSS

You can run the `lattice_tss.py` implementation using the following command:

```bash
python lattice_tss.py
```

This will:
- Generate a random matrix `A` and public key `t`.
- Generate and distribute secret key shares.
- Refresh the secret shares.
- Perform distributed signing and combine the signatures.

Sample Output:
```bash
Matrix A: [[  7161  1717 ...]]
Public key t: [ 2105 2121 ...]
Secret shares: [(1, array([....])), (2, array([....]))]
Final signature: ...
Distributed signature: ...
```

### 4. Running the Crystals-Dilithium-Based TSS

You can run the `simple_crystals_dilithium_scheme.py` implementation using the following command:

```bash
python simple_crystals_dilithium_scheme.py
```

This will:
- Generate lattice-based public and private keys.
- Generate key shares using Shamir’s Secret Sharing.
- Perform partial signing with the distributed secret shares.
- Combine the partial signatures into a final signature and verify its validity.

Sample Output:
```bash
Is the signature valid? True
```

## Understanding the Implementations

### Lattice-Based TSS Using a Random Matrix (`lattice_tss.py`)

This implementation demonstrates a simple form of lattice-based TSS using matrix operations. Key steps include:

- **Key Generation**: A random matrix `A` is generated, and a secret vector `s` is sampled. The public key `t` is computed as \( t = As + e \), where `e` is a small error vector.
- **Distributed Signing**: Each party signs the message with its secret share, and the partial signatures are combined into a final signature.

### Crystals-Dilithium-Based TSS (`simple_crystals_dilithium_scheme.py`)

This implementation uses concepts from the Crystals-Dilithium signature scheme. Key steps include:

- **Polynomial Arithmetic**: Polynomials are multiplied using modular arithmetic and the Number Theoretic Transform (NTT) to achieve efficient lattice-based computations.
- **Key Sharing and Signing**: Secret keys are shared using Shamir’s Secret Sharing, and partial signatures are combined using Lagrange interpolation.