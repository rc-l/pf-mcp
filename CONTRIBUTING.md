# Contributing to PingFederate MCP Server

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

Please be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Submit a pull request

## Development Setup

```bash
# Clone repository
git clone https://github.com/rc-l/pf-mcp.git
cd pf-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Development Process

### 1. Spec Driven Development

This project follows Spec Driven Development (SDD). Always:

1. **Start with the specification**: Update OpenAPI specs first
2. **Implement based on spec**: Code should match specifications
3. **Validate against spec**: Test implementations against specs
4. **Document changes**: Update documentation to reflect specs

### 2. Making Changes

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make changes following SDD principles
# 1. Update specs/openapi/pingfederate-api.yaml
# 2. Update specs/mcp/tools/README.md
# 3. Implement in src/
# 4. Add tests in tests/
# 5. Update documentation

# Run tests
pytest

# Run linters
black src/ tests/
ruff check src/ tests/
mypy src/

# Commit changes
git add .
git commit -m "feat: add new feature"
```

### 3. Commit Messages

Follow conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

Examples:
```
feat: add support for SAML connections
fix: handle missing redirect URI in OAuth clients
docs: update API documentation for new endpoints
test: add integration tests for IDP adapters
```

### 4. Pull Requests

- Write clear PR description
- Reference related issues
- Ensure all tests pass
- Update documentation
- Follow the PR template

## Code Standards

### Python Style

- **Formatting**: Black with 100 character line length
- **Linting**: Ruff with project configuration
- **Type Checking**: MyPy with strict mode
- **Docstrings**: Google style

### Code Quality

- Write unit tests for new code
- Maintain or improve test coverage
- Use type hints everywhere
- Document public APIs
- Handle errors gracefully

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pf_mcp --cov-report=html

# Run specific test file
pytest tests/unit/test_client.py

# Run integration tests
pytest -m integration
```

## Project Structure

```
pf-mcp/
├── specs/              # API specifications (source of truth)
│   ├── openapi/        # OpenAPI specs
│   └── mcp/            # MCP tool definitions
├── src/pf_mcp/         # Source code
│   ├── server.py       # MCP server
│   ├── client.py       # PingFederate client
│   ├── config.py       # Configuration
│   ├── models/         # Data models
│   └── tools/          # MCP tools
├── tests/              # Test suite
│   ├── unit/           # Unit tests
│   └── integration/    # Integration tests
├── docs/               # Documentation
├── examples/           # Usage examples
└── .github/            # GitHub configuration
    ├── workflows/      # CI/CD
    └── agents/         # AI agent instructions
```

## Adding New Features

### New API Endpoint

1. **Update OpenAPI Spec** (`specs/openapi/pingfederate-api.yaml`)
```yaml
/new/endpoint:
  get:
    summary: New endpoint
    operationId: newEndpoint
    responses:
      '200':
        description: Success
```

2. **Document MCP Tool** (`specs/mcp/tools/README.md`)
```markdown
#### new_tool
Description of the tool.
```

3. **Implement Client Method** (`src/pf_mcp/client.py`)
```python
async def new_method(self, param: str) -> dict[str, Any]:
    """Method description."""
    return await self._request("GET", f"/endpoint/{param}")
```

4. **Register MCP Tool** (`src/pf_mcp/server.py`)
```python
Tool(
    name="new_tool",
    description="Tool description",
    inputSchema={...},
)
```

5. **Add Tests** (`tests/unit/test_client.py`)
```python
@pytest.mark.asyncio
async def test_new_method(client):
    """Test new method."""
    # Test implementation
```

6. **Update Documentation**
- README.md
- docs/api/
- Usage examples

## Documentation

- Keep README up to date
- Update architecture docs
- Add API documentation
- Provide usage examples
- Document breaking changes

## Testing

### Unit Tests

- Test individual components
- Mock external dependencies
- Use pytest fixtures
- Aim for high coverage

### Integration Tests

- Test with real API (optional)
- Mark with `@pytest.mark.integration`
- Clean up resources
- Can be skipped in CI

## Security

- Never commit credentials
- Use environment variables
- Review security implications
- Report security issues privately

## Questions?

- Open an issue for bugs
- Use discussions for questions
- Check documentation first
- Be specific and provide context

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
