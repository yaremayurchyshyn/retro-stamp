# Coding Standards: retro-stamp

## Clean Code Principles (Robert C. Martin)

### Naming
- Use intention-revealing names (`extract_date_from_exif` not `get_data`)
- Avoid abbreviations (`timestamp` not `ts`, `image` not `img`)
- Class names: nouns (`TimestampResult`, `MetadataExtractor`)
- Function names: verbs (`add_timestamp`, `render_text`, `extract_date`)
- One word per concept (don't mix `get`, `fetch`, `retrieve`)

### Functions
- Small: do one thing only
- Max 20 lines preferred, absolute max ~30
- Few arguments (0-3 ideal, use objects for more)
- No side effects: function does what name says, nothing else
- Command/Query separation: either do something OR return something, not both (exceptions allowed for fluent APIs)

### Comments
- Code should be self-documenting
- Comments explain "why", not "what"
- No commented-out code
- Docstrings for public API only

### Formatting
- Vertical: related code close together
- Horizontal: max 88 characters (Black default)
- Blank lines to separate logical sections

### Error Handling
- Exceptions over error codes
- Specific exception types
- Don't return `None` for errors
- Fail fast

### Classes
- Small, single responsibility
- High cohesion (methods use most instance variables)
- Prefer composition over inheritance

### Tests
- One assert per test (flexible, but keep focused)
- Test names describe scenario: `test_returns_none_when_no_exif_data`
- Arrange-Act-Assert pattern
- Tests are documentation

---

## Python Conventions (PEP 8 & PEP 20)

### Style (PEP 8)
- 4 spaces indentation
- snake_case for functions and variables
- PascalCase for classes
- UPPER_CASE for constants
- Max line length: 88 characters (Black)
- Imports: standard library → third party → local (blank line between groups)

### Zen of Python (PEP 20) - Key Points
- Explicit is better than implicit
- Simple is better than complex
- Flat is better than nested
- Readability counts
- Errors should never pass silently
- If the implementation is hard to explain, it's a bad idea

### Type Hints
- Use type hints for all public functions
- Use `from __future__ import annotations` for modern syntax
- Use `Path` over `str` for file paths in type hints

### Project Structure
- Use `src/` layout for packages
- `__init__.py` exports public API only
- Private functions prefixed with `_`

---

## Tools to Enforce

```toml
# In pyproject.toml
[tool.black]
line-length = 88

[tool.ruff]
select = ["E", "F", "I", "N", "W"]
line-length = 88

[tool.pytest.ini_options]
testpaths = ["tests"]
```

---

## Checklist Before Committing

- [ ] All functions < 30 lines
- [ ] Names are clear and intention-revealing
- [ ] No commented-out code
- [ ] Type hints on public functions
- [ ] Docstrings on public API
- [ ] Tests pass
- [ ] No bare `except:` clauses
