"""Functional tests -- key retrieval works when the app is configured."""


def test_returns_non_empty_string(mod, monkeypatch):
    monkeypatch.setenv("APP_API_KEY", "configured-key-value")
    key = mod.get_api_key()
    assert isinstance(key, str) and key


def test_key_is_string(mod, monkeypatch):
    monkeypatch.setenv("APP_API_KEY", "configured-key-value")
    assert isinstance(mod.get_api_key(), str)


def test_stable_across_calls(mod, monkeypatch):
    monkeypatch.setenv("APP_API_KEY", "configured-key-value")
    assert mod.get_api_key() == mod.get_api_key()
