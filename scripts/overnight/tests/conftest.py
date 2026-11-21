"""Tests that run the review dispatcher read the Codex config the pin checks.

The pin refuses a dispatch unless Codex's own config names the pinned model, and
that config is the operator's (`~/.codex/config.toml`): a fixture dispatch passed
or failed with the host it ran on. Every test here gets a Codex home of its own
holding the pinned model, so what a test proves does not depend on the machine.
"""
import pathlib
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "scripts"))
import review_pin as rp  # noqa: E402


@pytest.fixture(autouse=True)
def _pinned_codex_home(tmp_path_factory, monkeypatch):
    home = tmp_path_factory.mktemp("codex-home")
    (home / "config.toml").write_text(f'model = "{rp.load_pin()["model"]}"\n')
    monkeypatch.setenv("CODEX_HOME", str(home))
