"""Proto schema loader for AWS RDS Instance.

This module parses the proto files to extract field definitions, validation rules,
and other metadata needed for intelligent manifest generation.
"""

import os
import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ProtoField:
    """Represents a field in a protobuf message."""

    name: str
    field_type: str
    field_number: int
    required: bool
    description: str
    validation_rules: dict
    foreign_key_info: dict | None = None
    is_repeated: bool = False


class ProtoSchemaLoader:
    """Loads and parses AWS RDS proto schema files."""

    def __init__(self, read_file_func: Callable[[str], str] | None = None):
        """Initialize the schema loader.

        Args:
            read_file_func: Optional function to read files from filesystem.
                If None, reads from local filesystem (backwards compatibility).
                Should accept file_path (str) and return file contents (str).
        """
        self.read_file_func = read_file_func
        self.schema_dir = Path(__file__).parent / "protos"
        self._spec_fields = None

    def _parse_proto_file(self, filename: str) -> str:
        """Read a proto file and return its contents."""
        if self.read_file_func:
            # Use DeepAgent filesystem
            from ..config import FILESYSTEM_PROTO_DIR

            filesystem_path = f"{FILESYSTEM_PROTO_DIR}/{filename}"
            try:
                return self.read_file_func(filesystem_path)
            except Exception as e:
                raise FileNotFoundError(
                    f"Proto file not found in filesystem: {filesystem_path}. "
                    f"Error: {e}"
                ) from e
        else:
            # Fallback to local filesystem (for backwards compatibility)
            filepath = self.schema_dir / filename
            if not filepath.exists():
                raise FileNotFoundError(f"Proto file not found: {filepath}")
            return filepath.read_text()

    def _extract_field_description(self, lines: list[str], field_index: int) -> str:
        """Extract field description from comments above the field."""
        description_lines = []
        # Look backwards from the field line to find comments
        i = field_index - 1
        comment_block_started = False
        
        while i >= 0:
            line = lines[i].strip()
            if line.startswith("//"):
                # Remove the // prefix and leading/trailing whitespace
                desc = line[2:].strip()
                if desc:  # Only add non-empty descriptions
                    description_lines.insert(0, desc)
                    comment_block_started = True
                i -= 1
            elif not line:
                # Empty line - if we haven't seen comments yet, keep looking
                # If we have seen comments, stop (end of comment block)
                if comment_block_started:
                    break
                i -= 1
            else:
                # Non-comment, non-empty line - stop
                break

        return " ".join(description_lines)

    def _parse_validation_rules(self, field_line: str) -> dict:
        """Parse buf.validate rules from a field definition."""
        rules = {}

        # Extract all (buf.validate.field).xxx patterns
        # Handle both single and multiple validations in brackets
        validation_pattern = r"\(buf\.validate\.field\)\.([^,\]]+)"
        matches = re.findall(validation_pattern, field_line)

        for match in matches:
            # Parse different validation types
            if "string.min_len" in match:
                min_len_match = re.search(r"string\.min_len\s*=\s*(\d+)", match)
                if min_len_match:
                    rules["min_len"] = int(min_len_match.group(1))

            if "string.pattern" in match:
                pattern_match = re.search(r'string\.pattern\s*=\s*"([^"]+)"', match)
                if pattern_match:
                    rules["pattern"] = pattern_match.group(1)

            if "string.const" in match:
                const_match = re.search(r'string\.const\s*=\s*"([^"]+)"', match)
                if const_match:
                    rules["const"] = const_match.group(1)

            if "int32.gt" in match:
                gt_match = re.search(r"int32\.gt\s*=\s*(\d+)", match)
                if gt_match:
                    rules["greater_than"] = int(gt_match.group(1))

            if "int32.gte" in match:
                gte_match = re.search(r"int32\.gte\s*=\s*(\d+)", match)
                if gte_match:
                    rules["greater_than_or_equal"] = int(gte_match.group(1))

            if "int32.lte" in match:
                lte_match = re.search(r"int32\.lte\s*=\s*(\d+)", match)
                if lte_match:
                    rules["less_than_or_equal"] = int(lte_match.group(1))

            if "required = true" in match:
                rules["required"] = True

        return rules

    def _parse_foreign_key_info(self, field_line: str) -> dict | None:
        """Parse foreign key annotations from a field definition."""
        fk_info = {}

        # Look for default_kind annotation
        kind_pattern = r"\(project\.planton\.shared\.foreignkey\.v1\.default_kind\)\s*=\s*(\w+)"
        kind_match = re.search(kind_pattern, field_line)
        if kind_match:
            fk_info["default_kind"] = kind_match.group(1)

        # Look for default_kind_field_path annotation
        path_pattern = r'\(project\.planton\.shared\.foreignkey\.v1\.default_kind_field_path\)\s*=\s*"([^"]+)"'
        path_match = re.search(path_pattern, field_line)
        if path_match:
            fk_info["default_field_path"] = path_match.group(1)

        return fk_info if fk_info else None

    def _parse_spec_fields(self) -> list[ProtoField]:
        """Parse the spec.proto file to extract field definitions."""
        spec_content = self._parse_proto_file("spec.proto")
        lines = spec_content.split("\n")
        fields = []

        # Find the AwsRdsInstanceSpec message
        in_message = False
        i = 0
        while i < len(lines):
            line = lines[i]
            
            if "message AwsRdsInstanceSpec" in line:
                in_message = True
                i += 1
                continue

            if in_message:
                # End of message
                if line.strip() == "}":
                    break

                # Skip empty lines and comments
                if not line.strip() or line.strip().startswith("//"):
                    i += 1
                    continue

                # Skip option lines
                if line.strip().startswith("option"):
                    i += 1
                    continue

                # Parse field definition
                # Format: [repeated] type name = number [annotations];
                field_match = re.match(
                    r"\s*(repeated\s+)?(\S+)\s+(\w+)\s*=\s*(\d+)(.*)$", line
                )
                if field_match:
                    is_repeated = bool(field_match.group(1))
                    field_type = field_match.group(2)
                    field_name = field_match.group(3)
                    field_number = int(field_match.group(4))
                    annotations = field_match.group(5)

                    # Collect multi-line field definition
                    # Continue reading lines until we find the closing semicolon or bracket
                    full_field = line
                    j = i + 1
                    while j < len(lines) and '];' not in full_field:
                        next_line = lines[j]
                        # Stop at empty line or new field
                        if not next_line.strip() or re.match(r'\s*(repeated\s+)?\S+\s+\w+\s*=', next_line):
                            break
                        full_field += " " + next_line.strip()
                        j += 1

                    # Get description from comments above
                    description = self._extract_field_description(lines, i)

                    # Parse validation rules from full field definition
                    validation_rules = self._parse_validation_rules(full_field)

                    # Parse foreign key info from full field definition
                    fk_info = self._parse_foreign_key_info(full_field)

                    # Determine if required
                    required = validation_rules.get("required", False)
                    # Also check if min_len is set for strings (indicates required)
                    if not required and "min_len" in validation_rules:
                        required = True

                    field = ProtoField(
                        name=field_name,
                        field_type=field_type,
                        field_number=field_number,
                        required=required,
                        description=description,
                        validation_rules=validation_rules,
                        foreign_key_info=fk_info,
                        is_repeated=is_repeated,
                    )
                    fields.append(field)
            
            i += 1

        return fields

    def load_spec_schema(self) -> list[ProtoField]:
        """Load and return all fields from the spec schema."""
        if self._spec_fields is None:
            self._spec_fields = self._parse_spec_fields()
        return self._spec_fields

    def get_required_fields(self) -> list[ProtoField]:
        """Return only required fields from the spec."""
        all_fields = self.load_spec_schema()
        return [f for f in all_fields if f.required]

    def get_optional_fields(self) -> list[ProtoField]:
        """Return only optional fields from the spec."""
        all_fields = self.load_spec_schema()
        return [f for f in all_fields if not f.required]

    def get_field_by_name(self, field_name: str) -> ProtoField | None:
        """Get a specific field by name."""
        all_fields = self.load_spec_schema()
        for field in all_fields:
            if field.name == field_name:
                return field
        return None


# Global instance for easy access
_loader = None


def get_schema_loader(read_file_func: Callable[[str], str] | None = None) -> ProtoSchemaLoader:
    """Get the global schema loader instance.

    Args:
        read_file_func: Optional function to read files from filesystem.
            If None and loader not yet initialized, creates loader with local filesystem.
            If provided, creates new loader with this function.

    Returns:
        ProtoSchemaLoader instance.
    """
    global _loader
    if _loader is None or read_file_func is not None:
        _loader = ProtoSchemaLoader(read_file_func)
    return _loader


def set_schema_loader(loader: ProtoSchemaLoader) -> None:
    """Set the global schema loader instance.

    Args:
        loader: ProtoSchemaLoader instance to set as global.
    """
    global _loader
    _loader = loader

