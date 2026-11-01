"""Schema loading and validation.

Uses ``jsonschema`` (Draft 2020-12, with format checking) when installed.
Otherwise falls back to a small validator covering the keywords the record
schema uses: type, enum, const, required, properties, additionalProperties
(false), items, minItems, minimum, minLength, pattern, format (date,
date-time), allOf and local $ref.
"""

import datetime as _dt
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.normpath(os.path.join(HERE, "..", "spec", "cra-evidence-record.v1.0.0.schema.json"))


def load_schema(path=SCHEMA_PATH):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def have_jsonschema():
    try:
        import jsonschema  # noqa: F401
        return True
    except ImportError:
        return False


def validate(instance, schema=None, force_fallback=False):
    """Return a list of error strings (empty when valid)."""
    schema = schema or load_schema()
    if not force_fallback and have_jsonschema():
        import jsonschema
        cls = jsonschema.Draft202012Validator
        v = cls(schema, format_checker=cls.FORMAT_CHECKER)
        errs = sorted(v.iter_errors(instance), key=lambda e: list(e.absolute_path))
        return ["%s: %s" % ("/" + "/".join(str(p) for p in e.absolute_path), e.message) for e in errs]
    return MiniValidator(schema).errors(instance)


_TYPES = {
    "object": dict, "array": list, "string": str, "boolean": bool,
    "null": type(None),
}


def _is_type(value, t):
    if t == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if t == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, _TYPES[t])


def _check_format(fmt, value):
    if not isinstance(value, str):
        return True
    try:
        if fmt == "date":
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                return False
            _dt.date.fromisoformat(value)
        elif fmt == "date-time":
            _dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


class MiniValidator:
    def __init__(self, root):
        self.root = root

    def _resolve(self, ref):
        if not ref.startswith("#/"):
            raise ValueError("only local $ref supported: %s" % ref)
        node = self.root
        for part in ref[2:].split("/"):
            node = node[part]
        return node

    def errors(self, instance):
        out = []
        self._v(instance, self.root, "", out)
        return out

    def _v(self, x, s, path, out):
        if "$ref" in s:
            self._v(x, self._resolve(s["$ref"]), path, out)
        for sub in s.get("allOf", []):
            self._v(x, sub, path, out)
        if "const" in s and x != s["const"]:
            out.append("%s: %r is not %r" % (path or "/", x, s["const"]))
        if "enum" in s and x not in s["enum"]:
            out.append("%s: %r is not one of %r" % (path or "/", x, s["enum"]))
        if "type" in s:
            types = s["type"] if isinstance(s["type"], list) else [s["type"]]
            if not any(_is_type(x, t) for t in types):
                out.append("%s: %r is not of type %s" % (path or "/", x, "/".join(types)))
                return
        if isinstance(x, str):
            if "minLength" in s and len(x) < s["minLength"]:
                out.append("%s: shorter than %d" % (path, s["minLength"]))
            if "pattern" in s and not re.search(s["pattern"], x):
                out.append("%s: %r does not match %r" % (path, x, s["pattern"]))
            if "format" in s and not _check_format(s["format"], x):
                out.append("%s: %r is not a valid %s" % (path, x, s["format"]))
        if isinstance(x, (int, float)) and not isinstance(x, bool):
            if "minimum" in s and x < s["minimum"]:
                out.append("%s: %r is less than %r" % (path, x, s["minimum"]))
        if isinstance(x, list):
            if "minItems" in s and len(x) < s["minItems"]:
                out.append("%s: fewer than %d items" % (path, s["minItems"]))
            if "items" in s:
                for i, item in enumerate(x):
                    self._v(item, s["items"], "%s/%d" % (path, i), out)
        if isinstance(x, dict):
            for req in s.get("required", []):
                if req not in x:
                    out.append("%s: %r is a required property" % (path or "/", req))
            props = s.get("properties", {})
            for k, val in x.items():
                if k in props:
                    self._v(val, props[k], "%s/%s" % (path, k), out)
                elif s.get("additionalProperties") is False:
                    out.append("%s: additional property %r not allowed" % (path or "/", k))
