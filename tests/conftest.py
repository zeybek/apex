# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Ahmet Zeybek and the Apex contributors
"""Make the standard-library validators in scripts/ importable from tests."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
