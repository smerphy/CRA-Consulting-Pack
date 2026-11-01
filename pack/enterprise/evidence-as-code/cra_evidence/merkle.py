"""Append-only Merkle log over evidence-record entries (RFC 9162 hashing).

Leaf hash  = SHA-256(0x00 || canonical JSON of the log entry)
Node hash  = SHA-256(0x01 || left || right)

The tree is the RFC 9162 (Certificate Transparency v2) Merkle tree, the
same construction Rekor uses, so the inclusion-proof verifier in
``transparency.py`` is reused. On top of the hash chain the store already
keeps, the Merkle log adds two properties that do not depend on the storage
layer:

- inclusion: anyone holding a signed checkpoint (tree size + root hash) can
  check that a given record entry is in the log with an O(log n) proof;
- consistency: a later checkpoint can be proved to extend an earlier one, so
  rewriting or truncating history is detectable by anyone who kept an old
  checkpoint (an auditor, a notified body, a witness).

``CompactTree`` keeps only the right-edge "frontier" (O(log n) hashes) for
appends and roots; proofs are computed from the stored leaf hashes.
"""

import hashlib

from .transparency import TlogError, root_from_inclusion_proof


def _h(b):
    return hashlib.sha256(b).digest()


def leaf_hash(data):
    return _h(b"\x00" + data)


def node_hash(left, right):
    return _h(b"\x01" + left + right)


EMPTY_ROOT = _h(b"")


def _split(n):
    """Largest power of two strictly less than n (n >= 2)."""
    k = 1
    while k << 1 < n:
        k <<= 1
    return k


def mth(leaves):
    """Merkle Tree Hash of a list of leaf hashes (RFC 9162 2.1.1)."""
    n = len(leaves)
    if n == 0:
        return EMPTY_ROOT
    if n == 1:
        return leaves[0]
    k = _split(n)
    return node_hash(mth(leaves[:k]), mth(leaves[k:]))


def inclusion_proof(index, leaves):
    """Audit path for leaf ``index`` in the tree over ``leaves`` (RFC 9162 2.1.3.1)."""
    n = len(leaves)
    if not 0 <= index < n:
        raise TlogError("index %d outside tree of size %d" % (index, n))
    if n == 1:
        return []
    k = _split(n)
    if index < k:
        return inclusion_proof(index, leaves[:k]) + [mth(leaves[k:])]
    return inclusion_proof(index - k, leaves[k:]) + [mth(leaves[:k])]


def verify_inclusion(index, size, leaf, proof, root):
    return root_from_inclusion_proof(index, size, leaf, proof) == root


def _subproof(m, leaves, complete):
    n = len(leaves)
    if m == n:
        return [] if complete else [mth(leaves)]
    k = _split(n)
    if m <= k:
        return _subproof(m, leaves[:k], complete) + [mth(leaves[k:])]
    return _subproof(m - k, leaves[k:], False) + [mth(leaves[:k])]


def consistency_proof(m, leaves):
    """Proof that the tree of size m is a prefix of the tree over ``leaves`` (RFC 9162 2.1.4.1)."""
    n = len(leaves)
    if not 0 < m <= n:
        raise TlogError("consistency proof needs 0 < m <= n (m=%d, n=%d)" % (m, n))
    if m == n:
        return []
    return _subproof(m, leaves, True)


def verify_consistency(m, n, root_m, root_n, proof):
    """RFC 9162 2.1.4.2 verification."""
    if m == n:
        return root_m == root_n and not proof
    if m == 0 or m > n:
        return False
    proof = list(proof)
    if (m & (m - 1)) == 0:          # m is a power of two: root_m is the first node
        proof = [root_m] + proof
    if not proof:
        return False
    fn, sn = m - 1, n - 1
    while fn & 1:
        fn >>= 1
        sn >>= 1
    fr = sr = proof[0]
    for c in proof[1:]:
        if sn == 0:
            return False
        if fn & 1 or fn == sn:
            fr = node_hash(c, fr)
            sr = node_hash(c, sr)
            if not fn & 1:
                while True:
                    fn >>= 1
                    sn >>= 1
                    if fn & 1 or fn == 0:
                        break
        else:
            sr = node_hash(sr, c)
        fn >>= 1
        sn >>= 1
    return sn == 0 and fr == root_m and sr == root_n


class CompactTree:
    """Incremental Merkle tree: O(log n) state for append and root."""

    def __init__(self):
        self.size = 0
        self._frontier = []      # list of (height, hash), heights strictly decreasing
        self.leaves = []         # leaf hashes, kept for proofs

    def append(self, lh):
        self.leaves.append(lh)
        h, node = 0, lh
        while self._frontier and self._frontier[-1][0] == h:
            _, left = self._frontier.pop()
            node = node_hash(left, node)
            h += 1
        self._frontier.append((h, node))
        self.size += 1
        return self.size - 1

    def root(self):
        if not self._frontier:
            return EMPTY_ROOT
        node = self._frontier[-1][1]
        for _, left in reversed(self._frontier[:-1]):
            node = node_hash(left, node)
        return node

    def inclusion_proof(self, index, size=None):
        return inclusion_proof(index, self.leaves[:size or self.size])

    def consistency_proof(self, m, n=None):
        return consistency_proof(m, self.leaves[:n or self.size])
