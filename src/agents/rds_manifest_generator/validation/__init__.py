"""Validation module for AWS RDS manifest validation using protovalidate."""

from .manifest_validator import validate_manifest_yaml

__all__ = ["validate_manifest_yaml"]


