import hashlib

def sha256(data):
    """TODO: Helper function to compute SHA-256 hash."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def compute_merkle_root(transactions):
    """TODO: Compute the Merkle Root for a list of transactions."""
    "https://www.youtube.com/watch?time_continue=2&v=fB41w3JcR7U&embeds_referring_euri=https%3A%2F%2Flearn.scu.edu.au%2F&source_ve_path=Mjg2NjY"

    if len(transactions) % 2 != 0:
        transactions.append(transactions[-1])

    root = hash_transactions(transactions)

    return root

def hash_transactions(transactions):
    hashes = []
    if len(transactions) == 1:
        return transactions

    for i, transaction in enumerate(transactions):
        if i + 1 > len(transactions) - 1:
            break
        first_hash = str(sha256(transaction))
        print(first_hash)
        second_hash = str(sha256(transactions[i + 1]))
        hashes.append(f"{first_hash}{second_hash}")

    print('running recursion')
    root = hash_transactions(hashes.copy())
    return root


# Example Usage
tnx = [
    "Transaction A",
    "Transaction B",
    "Transaction C",
    "Transaction D"
]

merkle_root = compute_merkle_root(tnx)
print("Merkle Root:", merkle_root)