"""
Daily Challenge 2026-03-03 — JSON Config Validator
Language: Python | Difficulty: Beginner

=== Background ===
Configuration files are everywhere — web apps, CLI tools, game settings.
Most use JSON because it's readable and widely supported. But loading a JSON
file doesn't mean the *contents* are valid — missing keys, wrong types, and
bad values can cause confusing crashes deep in your code.

Today you'll write a validator that checks a config dict against a schema,
and produces clear, human-friendly error messages.

=== Your Task ===
Implement `validate_config(config: dict, schema: dict) -> list[str]`.

The schema describes what keys are required and what type each value must be:

    schema = {
        "host":    {"type": str,  "required": True},
        "port":    {"type": int,  "required": True},
        "debug":   {"type": bool, "required": False},
        "timeout": {"type": float, "required": False},
    }

Rules:
1. Every key marked `"required": True` must be present in config.
2. If a key is present, its value must be an instance of the given type.
   (Note: in Python, `bool` is a subclass of `int`. If the schema says `int`
    but the value is `True` or `False`, that should be treated as a TYPE ERROR
    — a bool is not a valid int for our purposes.)
3. Collect ALL errors (don't stop at the first one).
4. Return a list of error strings. Return an empty list if config is valid.

Error message format (use these exactly):
  - Missing required key:   "Missing required key: 'host'"
  - Wrong type:             "Key 'port': expected int, got str"

=== Hints ===
- Use `isinstance(value, expected_type)` for type checking.
- Remember the special bool/int case — check for `bool` first!
- Iterate over the schema, not the config, so you catch missing keys.

=== Examples ===

Example 1 — valid config:
    config = {"host": "localhost", "port": 8080, "debug": True}
    schema = {
        "host":  {"type": str,  "required": True},
        "port":  {"type": int,  "required": True},
        "debug": {"type": bool, "required": False},
    }
    validate_config(config, schema)  # → []

Example 2 — multiple errors:
    config = {"host": 1234, "debug": "yes"}
    schema = {
        "host":  {"type": str,  "required": True},
        "port":  {"type": int,  "required": True},
        "debug": {"type": bool, "required": False},
    }
    validate_config(config, schema)
    # → ["Key 'host': expected str, got int",
    #    "Missing required key: 'port'",
    #    "Key 'debug': expected bool, got str"]

=== Starter Code ===
"""

def validate_config(config: dict, schema: dict) -> list[str]:
    """
    Validate config against schema.

    Args:
        config: The configuration dict to validate.
        schema: A dict mapping key names to {"type": <type>, "required": <bool>}.

    Returns:
        A list of error strings (empty list = valid).
    """
    errors = []

    # TODO: Iterate over the schema entries
    # For each key, check:
    #   1. Is it required but missing from config?
    #   2. Is it present but has the wrong type?

    return errors


# ─── Tests ───────────────────────────────────────────────────────────────────

def test_valid_config():
    schema = {
        "host":    {"type": str,   "required": True},
        "port":    {"type": int,   "required": True},
        "debug":   {"type": bool,  "required": False},
        "timeout": {"type": float, "required": False},
    }
    config = {"host": "localhost", "port": 8080, "debug": False, "timeout": 30.0}
    assert validate_config(config, schema) == [], "Expected no errors for valid config"

def test_missing_required():
    schema = {
        "host": {"type": str, "required": True},
        "port": {"type": int, "required": True},
    }
    config = {"host": "localhost"}
    errors = validate_config(config, schema)
    assert "Missing required key: 'port'" in errors

def test_missing_optional_ok():
    schema = {
        "host":  {"type": str,  "required": True},
        "debug": {"type": bool, "required": False},
    }
    config = {"host": "example.com"}
    errors = validate_config(config, schema)
    assert errors == [], "Optional missing keys should not cause errors"

def test_wrong_type():
    schema = {"port": {"type": int, "required": True}}
    config = {"port": "8080"}  # string instead of int
    errors = validate_config(config, schema)
    assert "Key 'port': expected int, got str" in errors

def test_bool_not_valid_int():
    """bool is a subclass of int in Python — we treat it as a type error."""
    schema = {"port": {"type": int, "required": True}}
    config = {"port": True}
    errors = validate_config(config, schema)
    assert "Key 'port': expected int, got bool" in errors, \
        "True/False should not be accepted as int values"

def test_multiple_errors():
    schema = {
        "host":  {"type": str,  "required": True},
        "port":  {"type": int,  "required": True},
        "debug": {"type": bool, "required": False},
    }
    config = {"host": 1234, "debug": "yes"}  # host wrong type, port missing, debug wrong type
    errors = validate_config(config, schema)
    assert len(errors) == 3
    assert "Key 'host': expected str, got int" in errors
    assert "Missing required key: 'port'" in errors
    assert "Key 'debug': expected bool, got str" in errors

def test_extra_keys_ignored():
    """Keys in config that aren't in schema should be silently ignored."""
    schema = {"host": {"type": str, "required": True}}
    config = {"host": "localhost", "extra_setting": 42}
    errors = validate_config(config, schema)
    assert errors == [], "Extra keys should be ignored"


if __name__ == "__main__":
    tests = [
        test_valid_config,
        test_missing_required,
        test_missing_optional_ok,
        test_wrong_type,
        test_bool_not_valid_int,
        test_multiple_errors,
        test_extra_keys_ignored,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {t.__name__}: {e}")
        except Exception as e:
            print(f"  ✗ {t.__name__}: unexpected error — {e}")

    print(f"\n{passed}/{len(tests)} tests passed")
