# PingFederate MCP Server

A Model Context Protocol (MCP) server for PingFederate, built with Spec Driven Development principles.

## Overview

This MCP server provides AI assistants with the ability to interact with PingFederate administrative APIs, enabling automated identity and access management workflows.

## Features

- 🔧 **Spec Driven Development**: API specifications drive implementation
- 🤖 **AI Agent Ready**: Designed for AI-powered automation
- 📝 **OpenAPI Integration**: Full PingFederate API coverage
- 🧪 **Test Driven**: Comprehensive test suite
- 🔐 **Secure**: Built-in authentication and authorization

## Project Structure

```
pf-mcp/
├── src/pf_mcp/          # Main source code
│   ├── server.py        # MCP server implementation
│   ├── client.py        # PingFederate API client
│   ├── models/          # Data models
│   └── tools/           # MCP tools
├── specs/               # API specifications
│   ├── openapi/         # OpenAPI specs for PingFederate
│   └── mcp/             # MCP tool definitions
├── docs/                # Documentation
│   ├── architecture.md  # System architecture
│   ├── development.md   # Development guide
│   └── api/             # API documentation
├── tests/               # Test suite
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── fixtures/        # Test fixtures
├── examples/            # Example usage
└── .github/             # GitHub configuration
    ├── workflows/       # CI/CD workflows
    └── agents/          # AI agent configurations
```

## Spec Driven Development

This project follows Spec Driven Development (SDD) principles:

1. **Specification First**: Define APIs in OpenAPI format before implementation
2. **Code Generation**: Generate client code from specifications
3. **Validation**: Ensure implementation matches specification
4. **Documentation**: Auto-generate docs from specs
5. **Testing**: Specification-based test generation

### Workflow

```mermaid
graph LR
    A[OpenAPI Spec] --> B[Generate Models]
    B --> C[Implement Tools]
    C --> D[Run Tests]
    D --> E[Validate Against Spec]
    E --> F[Deploy]
```

## Quick Start

### Prerequisites

- Python 3.10 or higher
- PingFederate instance (for testing)
- MCP-compatible client (e.g., Claude Desktop)

### Installation

```bash
# Clone the repository
git clone https://github.com/rc-l/pf-mcp.git
cd pf-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

### Configuration

Create a `.env` file:

```env
PINGFEDERATE_BASE_URL=https://your-pingfederate-instance.com
PINGFEDERATE_USERNAME=administrator
PINGFEDERATE_PASSWORD=your-password
PINGFEDERATE_API_VERSION=11.3
```

### Running the Server

```bash
# Start the MCP server
pf-mcp
```

### MCP Client Configuration

Add to your MCP client configuration (e.g., `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "pingfederate": {
      "command": "python",
      "args": ["-m", "pf_mcp.server"],
      "env": {
        "PINGFEDERATE_BASE_URL": "https://your-instance.com",
        "PINGFEDERATE_USERNAME": "administrator",
        "PINGFEDERATE_PASSWORD": "your-password"
      }
    }
  }
}
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pf_mcp --cov-report=html

# Run specific test file
pytest tests/unit/test_server.py
```

### Linting and Formatting

```bash
# Format code with black
black src/ tests/

# Lint with ruff
ruff check src/ tests/

# Type checking with mypy
mypy src/
```

### Adding New Tools

1. Define the tool in `specs/mcp/tools/`
2. Implement in `src/pf_mcp/tools/`
3. Add tests in `tests/unit/tools/`
4. Update documentation

See [Development Guide](docs/development.md) for details.

## API Specifications

OpenAPI specifications for PingFederate APIs are located in `specs/openapi/`. These specs:

- Define all available endpoints
- Specify request/response schemas
- Include authentication requirements
- Document error responses

## Available Tools

The MCP server provides the following tools:

- `list_oauth_clients` - List OAuth 2.0 clients
- `create_oauth_client` - Create a new OAuth client
- `get_oauth_client` - Get OAuth client details
- `update_oauth_client` - Update OAuth client configuration
- `delete_oauth_client` - Delete an OAuth client
- `list_idp_connections` - List identity provider connections
- `create_idp_connection` - Create IDP connection
- And more...

See [API Documentation](docs/api/) for complete tool reference.

## AI Agent Configuration

AI agent instructions and workflows are located in `.github/agents/`. These configurations:

- Define agent capabilities
- Specify workflow patterns
- Include best practices
- Provide examples

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Process

1. Create a feature branch
2. Update/create specifications
3. Implement changes
4. Add tests
5. Run linters and tests
6. Submit pull request

## Security

- Never commit credentials
- Use environment variables for configuration
- Follow PingFederate security best practices
- Report security issues privately

## License

See [LICENSE](LICENSE) file for details.

## Resources

- [PingFederate Documentation](https://docs.pingidentity.com/pingfederate)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [OpenAPI Specification](https://spec.openapis.org)
- [Spec Driven Development](https://swagger.io/resources/articles/adopting-an-api-first-approach/)

## Support

- GitHub Issues: [Report bugs or request features](https://github.com/rc-l/pf-mcp/issues)
- Discussions: [Ask questions and share ideas](https://github.com/rc-l/pf-mcp/discussions)

## Roadmap

- [x] Initial project structure
- [ ] OpenAPI specification for core PingFederate APIs
- [ ] MCP server implementation
- [ ] OAuth client management tools
- [ ] IDP connection management tools
- [ ] User management tools
- [ ] CI/CD pipeline
- [ ] Comprehensive documentation
- [ ] Example workflows
