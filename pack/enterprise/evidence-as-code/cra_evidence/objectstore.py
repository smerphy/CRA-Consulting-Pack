"""Storage backends for the evidence store: write-once objects with a retain-until date.

Interface (``StorageBackend``)
  put(key, data, retain_until, content_type, if_absent=True) -> dict
      Write a new object locked until ``retain_until`` (a date; the lock runs
      to the end of that day UTC). With ``if_absent`` an existing key is an
      error (``WriteOnceError``) rather than a new version.
  get(key) -> bytes ; exists(key) -> bool ; list(prefix) -> [key]
  retention(key) -> {"mode", "retain_until"}
  extend_retention(key, retain_until)  only ever lengthens
  delete(key, version_id=None)         must fail while the lock is in force

Backends
- ``LocalBackend``: the module's existing local, write-once directory store
  generalised to this interface. Files are created exclusively and made
  read-only, and retention is kept in a sidecar. It models the contract; a
  privileged local user can still delete files, which the signed Merkle log
  detects but cannot prevent.
- ``S3ObjectLockBackend``: any S3-compatible service with Object Lock. Each
  PUT carries ``ObjectLockMode=COMPLIANCE``, ``ObjectLockRetainUntilDate``,
  ``ChecksumAlgorithm=SHA256`` and ``If-None-Match: *`` (no silent
  overwrite); the returned checksum and the stored lock are read back and
  checked. Tested against moto's S3 server over HTTP; see the paper's
  appendix for which guarantees moto enforces and which only AWS does.
"""

import base64
import datetime as _dt
import hashlib
import json
import os
import stat


class StorageError(RuntimeError):
    pass


class WriteOnceError(StorageError):
    """Key already exists (write-once violation)."""


class ObjectLockedError(StorageError):
    """Delete, overwrite or retention shortening refused while the lock is in force."""


def _as_date(d):
    if isinstance(d, _dt.datetime):
        return d.date()
    if isinstance(d, _dt.date):
        return d
    return _dt.date.fromisoformat(str(d)[:10])


def lock_until(retain_until):
    """End of the retain-until day, UTC (the lock covers the whole date)."""
    d = _as_date(retain_until) + _dt.timedelta(days=1)
    return _dt.datetime(d.year, d.month, d.day, tzinfo=_dt.timezone.utc)


def sha256_b64(data):
    return base64.b64encode(hashlib.sha256(data).digest()).decode("ascii")


class StorageBackend:
    name = "abstract"
    mode = None

    def put(self, key, data, retain_until, content_type="application/octet-stream", if_absent=True):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def exists(self, key):
        raise NotImplementedError

    def list(self, prefix=""):
        raise NotImplementedError

    def retention(self, key):
        raise NotImplementedError

    def extend_retention(self, key, retain_until):
        raise NotImplementedError

    def delete(self, key, version_id=None):
        raise NotImplementedError

    def put_dedup(self, key, data, retain_until, content_type="application/octet-stream"):
        """Content-addressed write: if the key exists with the same bytes, extend its lock if needed."""
        try:
            return self.put(key, data, retain_until, content_type, if_absent=True)
        except WriteOnceError:
            existing = self.retention(key)
            if existing.get("sha256_b64") and existing["sha256_b64"] != sha256_b64(data):
                raise StorageError("content-addressed key %s holds different bytes" % key)
            if _as_date(existing["retain_until"]) < _as_date(retain_until):
                self.extend_retention(key, retain_until)
            return {"key": key, "deduplicated": True, "retain_until": str(_as_date(retain_until))}


class LocalBackend(StorageBackend):
    name = "local"
    mode = "local-write-once"

    def __init__(self, root, clock=None):
        self.root = os.path.abspath(root)
        self.clock = clock or (lambda: _dt.datetime.now(_dt.timezone.utc))
        os.makedirs(self.root, exist_ok=True)

    def _path(self, key):
        p = os.path.normpath(os.path.join(self.root, key))
        if not p.startswith(self.root + os.sep):
            raise StorageError("key escapes the store: %s" % key)
        return p

    def _meta(self, key):
        return self._path(os.path.join(".meta", key + ".json"))

    def put(self, key, data, retain_until, content_type="application/octet-stream", if_absent=True):
        p = self._path(key)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        try:
            fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o444)
        except FileExistsError:
            raise WriteOnceError("%s already exists; objects are write-once" % key)
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
        meta = {"key": key, "sha256_b64": sha256_b64(data), "size": len(data), "content_type": content_type,
                "mode": "COMPLIANCE", "retain_until": str(_as_date(retain_until)),
                "stored_at": self.clock().isoformat().replace("+00:00", "Z")}
        mp = self._meta(key)
        os.makedirs(os.path.dirname(mp), exist_ok=True)
        with open(mp, "w", encoding="utf-8") as fh:
            json.dump(meta, fh)
        os.chmod(mp, stat.S_IRUSR | stat.S_IWUSR)
        return {"key": key, "version_id": None, "checksum_sha256": meta["sha256_b64"],
                "retain_until": meta["retain_until"], "mode": "COMPLIANCE"}

    def get(self, key):
        with open(self._path(key), "rb") as fh:
            return fh.read()

    def exists(self, key):
        return os.path.isfile(self._path(key))

    def list(self, prefix=""):
        out = []
        base = self._path(prefix) if prefix else self.root
        start = base if os.path.isdir(base) else os.path.dirname(base)
        if not os.path.isdir(start):
            return out
        for dp, dns, fns in os.walk(start):
            dns[:] = sorted(d for d in dns if d != ".meta")
            for fn in sorted(fns):
                k = os.path.relpath(os.path.join(dp, fn), self.root).replace(os.sep, "/")
                if k.startswith(prefix) and not k.startswith(".meta/"):
                    out.append(k)
        return sorted(out)

    def retention(self, key):
        try:
            with open(self._meta(key), "r", encoding="utf-8") as fh:
                return json.load(fh)
        except FileNotFoundError:
            return {"mode": None, "retain_until": "1970-01-01"}

    def extend_retention(self, key, retain_until):
        meta = self.retention(key)
        if _as_date(retain_until) < _as_date(meta["retain_until"]):
            raise ObjectLockedError("retention of %s cannot be shortened" % key)
        meta["retain_until"] = str(_as_date(retain_until))
        mp = self._meta(key)
        with open(mp, "w", encoding="utf-8") as fh:
            json.dump(meta, fh)

    def delete(self, key, version_id=None):
        meta = self.retention(key)
        if self.clock() < lock_until(meta["retain_until"]):
            raise ObjectLockedError("%s is locked until %s" % (key, meta["retain_until"]))
        p = self._path(key)
        os.chmod(p, stat.S_IRUSR | stat.S_IWUSR)
        os.remove(p)


class S3ObjectLockBackend(StorageBackend):
    """S3 (or compatible) bucket with Object Lock in compliance mode."""

    name = "s3-object-lock"
    mode = "COMPLIANCE"

    def __init__(self, bucket, client=None, prefix="", endpoint_url=None, region=None, verify_lock=True):
        if client is None:
            import boto3  # lazy: optional dependency
            client = boto3.client("s3", endpoint_url=endpoint_url, region_name=region)
        self.client, self.bucket, self.prefix = client, bucket, prefix
        self.verify_lock = verify_lock
        self._errors()

    def _errors(self):
        from botocore.exceptions import ClientError
        self.ClientError = ClientError

    def _k(self, key):
        return self.prefix + key

    def ensure_bucket(self, create=False, region=None):
        """Check (or create) a bucket with Object Lock enabled; refuse a bucket without it."""
        if create:
            kw = {"Bucket": self.bucket, "ObjectLockEnabledForBucket": True}
            if region and region != "us-east-1":
                kw["CreateBucketConfiguration"] = {"LocationConstraint": region}
            try:
                self.client.create_bucket(**kw)
            except self.ClientError as e:
                if e.response["Error"]["Code"] not in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
                    raise
        cfg = self.client.get_object_lock_configuration(Bucket=self.bucket).get("ObjectLockConfiguration") or {}
        if cfg.get("ObjectLockEnabled") != "Enabled":
            raise StorageError("bucket %s does not have Object Lock enabled" % self.bucket)
        return cfg

    def put(self, key, data, retain_until, content_type="application/octet-stream", if_absent=True):
        until = lock_until(retain_until)
        kw = {"Bucket": self.bucket, "Key": self._k(key), "Body": data, "ContentType": content_type,
              "ObjectLockMode": "COMPLIANCE", "ObjectLockRetainUntilDate": until,
              "ChecksumAlgorithm": "SHA256"}
        if if_absent:
            kw["IfNoneMatch"] = "*"
        try:
            r = self.client.put_object(**kw)
        except self.ClientError as e:
            code = e.response["Error"]["Code"]
            if code in ("PreconditionFailed", "412", "ConditionalRequestConflict"):
                raise WriteOnceError("%s already exists; objects are write-once" % key)
            raise
        want = sha256_b64(data)
        if r.get("ChecksumSHA256") and r["ChecksumSHA256"] != want:
            raise StorageError("store returned checksum %s for %s, expected %s" % (r["ChecksumSHA256"], key, want))
        out = {"key": key, "version_id": r.get("VersionId"), "checksum_sha256": r.get("ChecksumSHA256"),
               "retain_until": str(_as_date(retain_until)), "mode": "COMPLIANCE"}
        if self.verify_lock:
            h = self.client.head_object(Bucket=self.bucket, Key=self._k(key), VersionId=r.get("VersionId")) \
                if r.get("VersionId") else self.client.head_object(Bucket=self.bucket, Key=self._k(key))
            if h.get("ObjectLockMode") != "COMPLIANCE" or h.get("ObjectLockRetainUntilDate") is None or \
                    h["ObjectLockRetainUntilDate"] < until:
                raise StorageError("object %s not locked as requested (mode %s, until %s)"
                                   % (key, h.get("ObjectLockMode"), h.get("ObjectLockRetainUntilDate")))
        return out

    def get(self, key):
        return self.client.get_object(Bucket=self.bucket, Key=self._k(key))["Body"].read()

    def exists(self, key):
        try:
            self.client.head_object(Bucket=self.bucket, Key=self._k(key))
            return True
        except self.ClientError:
            return False

    def list(self, prefix=""):
        out, token = [], None
        while True:
            kw = {"Bucket": self.bucket, "Prefix": self._k(prefix)}
            if token:
                kw["ContinuationToken"] = token
            r = self.client.list_objects_v2(**kw)
            out += [o["Key"][len(self.prefix):] for o in r.get("Contents") or []]
            if not r.get("IsTruncated"):
                break
            token = r.get("NextContinuationToken")
        return sorted(out)

    def retention(self, key):
        h = self.client.head_object(Bucket=self.bucket, Key=self._k(key), ChecksumMode="ENABLED")
        ru = h.get("ObjectLockRetainUntilDate")
        return {"mode": h.get("ObjectLockMode"), "version_id": h.get("VersionId"),
                "retain_until": str((ru - _dt.timedelta(seconds=1)).date()) if ru else None,
                "sha256_b64": h.get("ChecksumSHA256")}

    def extend_retention(self, key, retain_until):
        cur = self.retention(key)
        if cur["retain_until"] and _as_date(retain_until) < _as_date(cur["retain_until"]):
            raise ObjectLockedError("retention of %s cannot be shortened" % key)
        self.client.put_object_retention(Bucket=self.bucket, Key=self._k(key), VersionId=cur["version_id"],
                                         Retention={"Mode": "COMPLIANCE",
                                                    "RetainUntilDate": lock_until(retain_until)})

    def delete(self, key, version_id=None):
        """Attempt a permanent delete of a version; S3 refuses while the lock is in force."""
        kw = {"Bucket": self.bucket, "Key": self._k(key)}
        if version_id:
            kw["VersionId"] = version_id
        try:
            return self.client.delete_object(**kw)
        except self.ClientError as e:
            if e.response["Error"]["Code"] in ("AccessDenied", "403"):
                raise ObjectLockedError("%s: delete refused by Object Lock (%s)" % (key, e.response["Error"]["Code"]))
            raise
