# AI Agent Instructions for PingFederate MCP Server

This directory contains instructions and configurations for AI agents working on this project.

## Agent Role

AI agents working on this project should follow Spec Driven Development (SDD) principles:

1. **Understand Specifications First**: Always review OpenAPI specs in `specs/openapi/` before making changes
2. **Specification Changes First**: Update specifications before implementing changes
3. **Implementation Follows Spec**: Ensure code matches the defined specifications
4. **Test Against Specs**: Validate implementations against specifications

## Project Structure

- `specs/` - API specifications (source of truth)
- `src/pf_mcp/` - Implementation code
- `tests/` - Test suite
- `docs/` - Documentation
- `examples/` - Usage examples

## Development Workflow

### Adding New API Endpoints

1. **Update OpenAPI Spec** (`specs/openapi/pingfederate-api.yaml`)
   - Add new path
   - Define request/response schemas
   - Include error responses

2. **Update MCP Tool Spec** (`specs/mcp/tools/README.md`)
   - Document the new tool
   - Define input schema
   - Map to OpenAPI operation

3. **Implement Client Method** (`src/pf_mcp/client.py`)
   - Add method matching OpenAPI operation
   - Include type hints
   - Add docstring with Args/Returns

4. **Register MCP Tool** (`src/pf_mcp/server.py`)
   - Add tool definition in `list_tools()`
   - Add handler in `call_tool()`
   - Ensure input validation

5. **Add Tests** (`tests/unit/`)
   - Test client method
   - Test MCP tool handler
   - Mock API responses

6. **Update Documentation**
   - Update README if needed
   - Add usage example
   - Update API docs

### Code Standards

- **Type Safety**: Always use type hints
- **Documentation**: Google-style docstrings
- **Testing**: Write tests for new features
- **Formatting**: Use black (line length 100)
- **Linting**: Follow ruff rules
- **Async/Await**: Use for all I/O operations

### Example Code Pattern

```python
# Client method
async def new_method(self, param: str) -> dict[str, Any]:
    """Short description.
    
    Args:
        param: Parameter description
        
    Returns:
        Response data
    """
    return await self._request("GET", f"/path/{param}")

# MCP Tool
Tool(
    name="new_tool",
    description="Tool description",
    inputSchema={
        "type": "object",
        "properties": {
            "param": {
                "type": "string",
                "description": "Parameter description"
            }
        },
        "required": ["param"]
    }
)

# Test
@pytest.mark.asyncio
async def test_new_method(client):
    """Test the new method."""
    with patch.object(client, "_request", new_callable=AsyncMock) as mock:
        mock.return_value = {"result": "success"}
        result = await client.new_method("test")
        assert result["result"] == "success"
```

## Common Tasks

### Add OAuth Tool
- Refer to existing OAuth tools in `server.py`
- Follow the same pattern for consistency
- Include grant type validation

### Add IDP Tool
- IDP tools typically deal with adapters/connections
- Complex configurations may need nested schemas
- Test with various configuration types

### Update Dependencies
- Check for vulnerabilities first
- Update `pyproject.toml`
- Test thoroughly after updates
- Update documentation if APIs change

## Testing Guidelines

### Unit Tests
- Mock external dependencies
- Test one component at a time
- Use pytest fixtures for setup
- Aim for high coverage

### Integration Tests
- Mark with `@pytest.mark.integration`
- Require actual PingFederate instance
- Clean up resources after tests
- Can be skipped in CI

### Running Tests
```bash
# All tests
pytest

# Unit only
pytest tests/unit/

# With coverage
pytest --cov=pf_mcp --cov-report=html
```

## Debugging Tips

1. **Enable Debug Logging**: `export LOG_LEVEL=DEBUG`
2. **Check Specs**: Validate against OpenAPI spec
3. **Inspect Requests**: Check HTTP client logs
4. **Mock Responses**: Use test fixtures
5. **Type Errors**: Run mypy for type checking

## Security Considerations

- Never commit credentials
- Use environment variables
- Validate all inputs
- Sanitize error messages
- Use HTTPS in production

## Best Practices

1. **Spec First**: Always update specs before code
2. **Type Safety**: Leverage Pydantic and mypy
3. **Error Handling**: Provide clear error messages
4. **Documentation**: Keep docs in sync with code
5. **Testing**: Test happy path and error cases
6. **Backwards Compatibility**: Don't break existing APIs

## Resources

- [OpenAPI 3.0 Spec](https://spec.openapis.org/oas/v3.0.3)
- [MCP Protocol](https://modelcontextprotocol.io)
- [PingFederate API Docs](https://docs.pingidentity.com/pingfederate)
- [Pydantic Documentation](https://docs.pydantic.dev)

## Questions?

For questions about:
- **API Specs**: Check OpenAPI documentation
- **MCP Protocol**: Refer to MCP specification
- **PingFederate**: Consult PingFederate docs
- **Python Best Practices**: Follow PEP 8 and project standards
