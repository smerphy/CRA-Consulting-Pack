"""Content digests for evidence items."""

import hashlib
import os

MEDIA_TYPES = {
    ".cdx.json": "application/vnd.cyclonedx+json",
    ".spdx.json": "application/spdx+json",
    ".intoto.json": "application/vnd.in-toto+json",
    ".openvex.json": "application/vnd.openvex+json",
    ".csaf.json": "application/csaf+json",
    ".sarif": "application/sarif+json",
    ".sarif.json": "application/sarif+json",
    ".json": "application/json",
    ".md": "text/markdown",
    ".html": "text/html",
    ".pdf": "application/pdf",
    ".bin": "application/octet-stream",
}


def file_digests(path):
    """Return sha256 and sha512 hex digests and size of a file, streamed."""
    h256 = hashlib.sha256()
    h512 = hashlib.sha512()
    size = 0
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h256.update(chunk)
            h512.update(chunk)
            size += len(chunk)
    return {"sha256": h256.hexdigest(), "sha512": h512.hexdigest()}, size


def media_type(path):
    name = os.path.basename(path).lower()
    for suffix in sorted(MEDIA_TYPES, key=len, reverse=True):
        if name.endswith(suffix):
            return MEDIA_TYPES[suffix]
    return "application/octet-stream"


def digested_item(path, uri=None, ref=None):
    """Build a schema 'digestedItem' for a local file."""
    digests, size = file_digests(path)
    item = {
        "uri": uri or path,
        "media_type": media_type(path),
        "size_bytes": size,
        "digests": digests,
    }
    if ref is not None:
        item["ref"] = ref
    return item
