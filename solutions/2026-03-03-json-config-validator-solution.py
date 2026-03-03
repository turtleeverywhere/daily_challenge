"""
Daily Challenge 2026-03-03 — JSON Config Validator (SOLUTION)
Language: Python | Difficulty: Beginner
"""

def validate_config(config: dict, schema: dict) -> list[str]:
    """
    Validate config against schema, collecting all errors.

    Strategy:
    - Iterate over the schema (not the config) so we always check every
      declared key, even if it's absent from the config.
    - For each schema key, two checks:
        1. Missing required key.
        2. Present key with wrong type (with special-case for bool vs int).
    - Extra keys in config (not in schema) are silently ignored.
    """
    errors = []

    for key, rules in schema.items():
        expected_type = rules["type"]
        required = rules["required"]

        if key not in config:
            # Key is absent from config.
            if required:
                errors.append(f"Missing required key: '{key}'")
            # If optional and absent — no error, move on.
            continue

        # Key is present; now check its type.
        value = config[key]

        # Special case: bool is a subclass of int in Python, so
        # isinstance(True, int) returns True. We want to reject booleans
        # when the schema expects an int, so check for bool first.
        if isinstance(value, bool) and expected_type is not bool:
            # Value is bool but schema doesn't want bool.
            actual_name = type(value).__name__
            errors.append(f"Key '{key}': expected {expected_type.__name__}, got {actual_name}")
        elif not isinstance(value, bool) and expected_type is bool and not isinstance(value, bool):
            # Schema wants bool but value is something else.
            actual_name = type(value).__name__
            errors.append(f"Key '{key}': expected bool, got {actual_name}")
        elif not isinstance(value, expected_type):
            # General type mismatch.
            actual_name = type(value).__name__
            errors.append(f"Key '{key}': expected {expected_type.__name__}, got {actual_name}")

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
    config = {"port": "8080"}
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
    config = {"host": 1234, "debug": "yes"}
    errors = validate_config(config, schema)
    assert len(errors) == 3
    assert "Key 'host': expected str, got int" in errors
    assert "Missing required key: 'port'" in errors
    assert "Key 'debug': expected bool, got str" in errors

def test_extra_keys_ignored():
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
