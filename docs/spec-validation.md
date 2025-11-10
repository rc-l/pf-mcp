# Specification Validation

This document describes how to validate implementations against specifications.

## Overview

Spec Driven Development requires that implementations match their specifications. This document outlines validation strategies.

## OpenAPI Specification Validation

### Validating the Spec Itself

```bash
# Install OpenAPI validator
pip install openapi-spec-validator

# Validate the spec
openapi-spec-validator specs/openapi/pingfederate-api.yaml
```

### Validating Requests/Responses

```python
from openapi_core import Spec
from openapi_core.validation.request import openapi_request_validator
from openapi_core.validation.response import openapi_response_validator

# Load spec
spec = Spec.from_file_path('specs/openapi/pingfederate-api.yaml')

# Validate request
result = openapi_request_validator.validate(spec, request)

# Validate response
result = openapi_response_validator.validate(spec, request, response)
```

## MCP Tool Validation

### JSON Schema Validation

```python
import jsonschema

# Tool input schema
schema = {
    "type": "object",
    "properties": {
        "clientId": {"type": "string"}
    },
    "required": ["clientId"]
}

# Validate input
jsonschema.validate(instance={"clientId": "test"}, schema=schema)
```

## Test-Based Validation

### Schema Compliance Tests

```python
@pytest.mark.asyncio
async def test_list_oauth_clients_schema(client):
    """Test that list_oauth_clients returns correct schema."""
    result = await client.list_oauth_clients()
    
    # Validate response structure
    assert "items" in result
    assert isinstance(result["items"], list)
    
    # Validate each item
    for item in result["items"]:
        assert "clientId" in item
        assert "name" in item
        assert isinstance(item["clientId"], str)
        assert isinstance(item["name"], str)
```

### Integration Tests with Spec Validation

```python
@pytest.mark.integration
async def test_create_oauth_client_matches_spec(client):
    """Test OAuth client creation matches OpenAPI spec."""
    # Create client according to spec
    client_data = {
        "clientId": "test-client",
        "name": "Test Client",
        "grantTypes": ["authorization_code"]
    }
    
    result = await client.create_oauth_client(client_data)
    
    # Validate response matches spec
    assert "clientId" in result
    assert result["clientId"] == "test-client"
    assert "name" in result
    assert result["name"] == "Test Client"
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
name: Spec Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate OpenAPI Spec
        run: |
          pip install openapi-spec-validator
          openapi-spec-validator specs/openapi/pingfederate-api.yaml
      
      - name: Run Spec Compliance Tests
        run: |
          pytest tests/unit/ -k schema
```

## Best Practices

1. **Validate Early**: Check specs during development
2. **Automate**: Include validation in CI/CD
3. **Test Coverage**: Test all schema fields
4. **Version Control**: Keep specs in sync with code
5. **Documentation**: Document any deviations

## Tools

### OpenAPI Validation
- `openapi-spec-validator` - Spec validation
- `openapi-core` - Request/response validation
- `prance` - Spec parsing and validation

### JSON Schema
- `jsonschema` - Schema validation
- `fastjsonschema` - Fast validation

### Code Generation
- `datamodel-code-generator` - Generate Pydantic models
- `openapi-python-client` - Generate API client

## Continuous Validation

```python
# Add to tests/conftest.py
import pytest
from openapi_spec_validator import validate_spec

@pytest.fixture(scope="session")
def openapi_spec():
    """Load and validate OpenAPI spec."""
    spec_path = "specs/openapi/pingfederate-api.yaml"
    validate_spec(spec_path)
    return spec_path
```

## Validation Checklist

- [ ] OpenAPI spec is valid YAML
- [ ] All references ($ref) resolve correctly
- [ ] Request schemas match implementation
- [ ] Response schemas match implementation
- [ ] Error responses are documented
- [ ] Required fields are enforced
- [ ] Data types are correct
- [ ] Enums match allowed values
- [ ] Examples are valid
- [ ] Security schemes are defined

## Resources

- [OpenAPI Specification](https://spec.openapis.org/)
- [JSON Schema](https://json-schema.org/)
- [OpenAPI Generator](https://openapi-generator.tech/)
