"""Utilities for extracting and selecting Planton Cloud resource IDs.

This module is intentionally resilient: it attempts to load valid ID prefixes
from the Planton Cloud API Resource Kind enum if present on the PYTHONPATH.
If those stubs are not available locally, it gracefully falls back to pure
regex-based extraction without prefix validation.
"""

from __future__ import annotations

import importlib
import re
from collections.abc import Sequence

# ID tokens look like: <prefix>_<rest>, where prefix is alphanumeric (lowercase)
# and the rest is a slug. We normalize dashes to underscores.
ID_TOKEN_RE = re.compile(r"\b([a-z][a-z0-9]{1,31})_([a-z0-9][a-z0-9_-]{1,127})\b")


def load_valid_prefixes() -> set[str]:
    """Best-effort retrieval of allowed ID prefixes from API Resource Kind enum.

    Returns a set of known prefixes. If the Planton Cloud stubs are not
    importable, returns an empty set to indicate "no filtering by prefix".
    """
    prefixes: set[str] = set()
    try:
        # Attempt to import generated stubs that include id_prefix metadata
        kinds = importlib.import_module(
            "planton_cloud.cloud.planton.apis.commons.apiresource.apiresourcekind.api_resource_kind_pb2"
        )

        enum_desc = getattr(kinds, "_APIRESOURCEKIND", None)
        ext = getattr(kinds, "kind_meta", None)
        kind_type_enum = getattr(kinds, "ApiResourceKindType", None)
        if enum_desc is None or ext is None or kind_type_enum is None:
            return prefixes
        
        try:
            CLOUD_RESOURCE_KIND = kind_type_enum.Value("cloud_resource_kind")
        except Exception:
            CLOUD_RESOURCE_KIND = None

        values = getattr(enum_desc, "values", [])
        for value in values:
            try:
                meta = value.GetOptions().Extensions[ext]
                # Only include prefixes for cloud_resource_kind types
                kind_type_val = getattr(meta, "kind_type", None)
                id_prefix: str | None = getattr(meta, "id_prefix", None)
                if (
                    id_prefix
                    and CLOUD_RESOURCE_KIND is not None
                    and kind_type_val == CLOUD_RESOURCE_KIND
                ):
                    prefixes.add(id_prefix)
            except Exception:
                # Missing or unreadable metadata for this enum value
                continue
    except Exception:
        # Stubs not available – operate without a prefix allowlist
        return prefixes

    return prefixes


def extract_candidate_ids(
    text: str, allowed_prefixes: set[str] | None = None
) -> list[str]:
    """Extract candidate resource IDs from free-form text.

    - Performs a case-insensitive regex scan for tokens matching the ID shape
      and normalizes hyphens in the suffix to underscores.
    - If ``allowed_prefixes`` is provided and non-empty, filters candidates to
      only those whose prefix appears in the allowlist.
    """
    if not text:
        return []

    text_lc = text.lower()
    candidates: list[str] = []
    seen: set[str] = set()

    for match in ID_TOKEN_RE.finditer(text_lc):
        prefix, rest = match.group(1), match.group(2)
        if allowed_prefixes:
            if prefix not in allowed_prefixes:
                continue
        token = f"{prefix}_{rest.replace('-', '_')}"
        if token not in seen and "_" in token:
            seen.add(token)
            candidates.append(token)

    return candidates


def select_resource_ids(
    messages: Sequence[dict[str, object]], candidates: Sequence[str], max_ids: int = 50
) -> list[str]:
    """Heuristically select a subset of candidate IDs.

    This is a placeholder for a future LLM-based selector. For now, it returns
    de-duplicated candidates up to ``max_ids``.
    """
    selected: list[str] = []
    seen: set[str] = set()
    for cid in candidates:
        if cid in seen:
            continue
        seen.add(cid)
        selected.append(cid)
        if len(selected) >= max_ids:
            break
    return selected


