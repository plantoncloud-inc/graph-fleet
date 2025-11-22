"""Manifest validation using protovalidate for AWS RDS instances.

This module validates AWS RDS manifest YAML against proto validation rules
defined in the AwsRdsInstance protobuf message.
"""

from __future__ import annotations

from typing import List, Optional, Tuple, Type, TypeVar

import protovalidate
import yaml
from google.protobuf.json_format import ParseDict
from google.protobuf.message import Message

# Import the AwsRdsInstance proto message
try:
    from org.project_planton.provider.aws.awsrdsinstance.v1.api_pb2 import (
        AwsRdsInstance,
    )
except ImportError:
    # Fallback for development/testing without installed stubs
    AwsRdsInstance = None  # type: ignore

# FieldPath is optional at runtime – import it if the stubs are present.
try:
    from buf.validate.validate_pb2 import FieldPath
except ModuleNotFoundError:  # stubs were not generated / vendored
    FieldPath = None  # type: ignore

T = TypeVar("T", bound=Message)


# --------------------------------------------------------------------------- #
# helpers                                                                     #
# --------------------------------------------------------------------------- #
def _get_attr(obj, name: str):
    """Retrieve *name* from *obj*.

    If absent, fall back to obj.proto.<name>.
    Works with both old (flat) and new (wrapped) Violation objects.
    """
    if hasattr(obj, name):
        return getattr(obj, name)
    proto = getattr(obj, "proto", None)
    if proto is not None and hasattr(proto, name):
        return getattr(proto, name)
    return None


def _fmt_field_path(violation) -> str:
    """Render FieldPath → dotted.path[0] form.

    Falls back to the string in older protovalidate builds.
    """
    fp = _get_attr(violation, "field")
    if fp is None:
        legacy = _get_attr(violation, "field_path")
        return legacy if legacy else "<unknown>"

    # Handle both "real" FieldPath objects and stub‑less message instances.
    if FieldPath is not None and isinstance(fp, FieldPath):
        elems = fp.elements
    else:
        elems = getattr(fp, "elements", None)
        if elems is None:  # not a FieldPath at all
            legacy = _get_attr(violation, "field_path")
            return legacy if legacy else "<unknown>"

    parts: list[str] = []
    for elem in elems:
        # field name or number
        name = elem.field_name or str(elem.field_number)

        # map / repeated subscripts
        sub = elem.WhichOneof("subscript")
        if sub == "index":
            name += f"[{elem.index}]"
        elif sub == "bool_key":
            name += f"[{elem.bool_key}]"
        elif sub == "int_key":
            name += f"[{elem.int_key}]"
        elif sub == "uint_key":  # unsigned‑int map keys
            name += f"[{elem.uint_key}]"
        elif sub == "string_key":
            name += f"['{elem.string_key}']"  # mirror Java
        parts.append(name)

    return ".".join(parts)


def _violation_msg(violation) -> str:
    """Retrieve the human‑readable message.

    Regardless of the exact attribute name used by the generated code.
    """
    for attr in ("message", "message_", "msg", "msg_"):
        val = _get_attr(violation, attr)
        if val:
            return val
    rid = _get_attr(violation, "rule_id")
    return rid if rid else "validation error"


def yaml_to_proto(
    yaml_str: str,
    proto_message_cls: Type[T],
) -> Tuple[Optional[T], List[str]]:
    """Convert YAML text to a Protobuf message instance.

    Args:
        yaml_str: YAML document as a string.
        proto_message_cls: Generated Protobuf message class (e.g. AwsRdsInstance).

    Returns:
        A tuple (message_or_none, errors).
        * On success: (populated_message, [])
        * On failure: (None, ["error message"])
    """
    # YAML → dict --------------------------------------------------------------
    try:
        manifest_dict = yaml.safe_load(yaml_str) or {}
    except yaml.YAMLError as exc:
        return None, [f"invalid YAML: {exc}"]

    # dict → proto -------------------------------------------------------------
    msg = proto_message_cls()
    try:
        ParseDict(manifest_dict, msg, ignore_unknown_fields=False)
    except Exception as exc:
        return None, [f"schema mismatch: {exc}"]

    return msg, []


# --------------------------------------------------------------------------- #
# public API                                                                  #
# --------------------------------------------------------------------------- #
def validate_manifest_yaml(
    manifest_yaml: str,
) -> List[str]:
    """Validate *manifest_yaml* against rules declared on AwsRdsInstance.

    Returns:
        []                 – when the manifest is valid.
        ["field: message"] – one entry per violation when invalid.
    """
    if AwsRdsInstance is None:
        return ["Error: AwsRdsInstance proto stubs not installed"]

    msg, errors = yaml_to_proto(manifest_yaml, AwsRdsInstance)
    if errors:
        return errors

    # proto → validate --------------------------------------------------------
    try:
        protovalidate.validate(msg)  # raises on failure
        return []  # ✅ all good
    except protovalidate.ValidationError as err:
        return [
            f"{_fmt_field_path(v)}: {_violation_msg(v)}" for v in err.violations
        ]


