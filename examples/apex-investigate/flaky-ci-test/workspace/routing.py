"""Routing selection with an intentional ordering defect."""

from __future__ import annotations


def select_primary(healthy_regions: set[str]) -> str:
    if not healthy_regions:
        raise ValueError("at least one healthy region is required")
    return next(iter(healthy_regions))
