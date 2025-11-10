# Development Guide

## Setup

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager
- Git
- PingFederate instance (for testing)

### Initial Setup

```bash
# Clone repository
git clone https://github.com/rc-l/pf-mcp.git
cd pf-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Environment Configuration

Create `.env` file:

```env
# PingFederate Configuration
PINGFEDERATE_BASE_URL=https://localhost:9999
PINGFEDERATE_USERNAME=administrator
PINGFEDERATE_PASSWORD=your-password
PINGFEDERATE_API_VERSION=11.3
PINGFEDERATE_VERIFY_SSL=false

# Logging
LOG_LEVEL=DEBUG
```

## Development Workflow

### 1. Spec-First Development

Always start with the specification:

```bash
# Edit OpenAPI spec
vim specs/openapi/pingfederate-api.yaml

# Validate the spec
openapi-spec-validator specs/openapi/pingfederate-api.yaml
```

### 2. Generate Models (if needed)

```bash
# Use datamodel-code-generator for Pydantic models
datamodel-codegen --input specs/openapi/pingfederate-api.yaml \
  --output src/pf_mcp/models/generated.py
```

### 3. Implement Features

```python
# Update client.py with new methods
async def new_method(self, param: str) -> dict[str, Any]:
    """Method description."""
    return await self._request("GET", f"/endpoint/{param}")

# Update server.py with new tools
Tool(
    name="new_tool",
    description="Tool description",
    inputSchema={...},
)
```

### 4. Add Tests

```python
# tests/unit/test_client.py
async def test_new_method():
    """Test the new method."""
    client = PingFederateClient(settings)
    result = await client.new_method("test")
    assert result is not None
```

### 5. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pf_mcp --cov-report=html

# Run specific test
pytest tests/unit/test_client.py::test_new_method

# Run with verbose output
pytest -v
```

### 6. Lint and Format

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Fix lint issues automatically
ruff check --fix src/ tests/

# Type checking
mypy src/
```

## Testing

### Unit Tests

Located in `tests/unit/`, test individual components in isolation.

```python
import pytest
from pf_mcp.client import PingFederateClient

@pytest.mark.asyncio
async def test_list_oauth_clients():
    """Test listing OAuth clients."""
    # Setup
    client = PingFederateClient(test_settings)
    
    # Execute
    result = await client.list_oauth_clients()
    
    # Assert
    assert "items" in result
```

### Integration Tests

Located in `tests/integration/`, test with real or mock PingFederate API.

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_and_delete_client():
    """Test full lifecycle of OAuth client."""
    client = PingFederateClient(settings)
    
    # Create
    created = await client.create_oauth_client({
        "clientId": "test-client",
        "name": "Test Client"
    })
    
    # Verify
    fetched = await client.get_oauth_client("test-client")
    assert fetched["clientId"] == "test-client"
    
    # Cleanup
    await client.delete_oauth_client("test-client")
```

### Running Tests

```bash
# All tests
pytest

# Only unit tests
pytest tests/unit/

# Only integration tests
pytest -m integration

# Skip integration tests
pytest -m "not integration"

# With coverage
pytest --cov=pf_mcp --cov-report=html
open htmlcov/index.html
```

## Code Style

### Black

Line length: 100 characters

```python
# Good
def long_function_name(
    parameter_one: str,
    parameter_two: int,
    parameter_three: bool = False,
) -> dict[str, Any]:
    """Function with many parameters."""
    pass
```

### Ruff

Follow PEP 8 with project-specific rules in `pyproject.toml`.

### Type Hints

Always use type hints:

```python
from typing import Any

async def method(param: str, optional: int | None = None) -> dict[str, Any]:
    """Method with type hints."""
    result: dict[str, Any] = {}
    return result
```

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def function(param1: str, param2: int) -> bool:
    """Short description.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When validation fails
    """
    pass
```

### API Documentation

Keep `specs/mcp/tools/README.md` updated with new tools.

## Debugging

### Enable Debug Logging

```bash
export LOG_LEVEL=DEBUG
pf-mcp
```

### Python Debugger

```python
import pdb; pdb.set_trace()

# Or with breakpoint() (Python 3.7+)
breakpoint()
```

### VSCode Debug Configuration

`.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: MCP Server",
      "type": "python",
      "request": "launch",
      "module": "pf_mcp.server",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/src",
        "LOG_LEVEL": "DEBUG"
      },
      "console": "integratedTerminal"
    }
  ]
}
```

## CI/CD

### GitHub Actions

Workflows in `.github/workflows/`:

- `ci.yml` - Run tests on push/PR
- `lint.yml` - Code quality checks
- `release.yml` - Build and publish releases

### Pre-commit Hooks

Automatically runs before each commit:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    hooks:
      - id: black
  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff
```

## Troubleshooting

### SSL Certificate Issues

For development with self-signed certificates:

```env
PINGFEDERATE_VERIFY_SSL=false
```

### Connection Refused

Check PingFederate is running:

```bash
curl -k https://localhost:9999/pf-admin-api/v1/version
```

### Import Errors

Ensure package is installed in development mode:

```bash
pip install -e ".[dev]"
```

## Contributing

1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes following this guide
3. Run tests and linters
4. Commit with clear message
5. Push and create PR
6. Address review feedback

## Resources

- [PingFederate API Documentation](https://docs.pingidentity.com/pingfederate)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [Pydantic Documentation](https://docs.pydantic.dev)
- [pytest Documentation](https://docs.pytest.org)
