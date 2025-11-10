# Architecture

## System Overview

The PingFederate MCP Server is designed using Spec Driven Development principles, where API specifications drive the implementation.

```
┌─────────────────┐
│   AI Assistant  │
│   (e.g., Claude)│
└────────┬────────┘
         │ MCP Protocol
         │
┌────────▼────────┐
│  MCP Server     │
│  (pf-mcp)       │
├─────────────────┤
│ • Tools Layer   │
│ • Client Layer  │
│ • Models Layer  │
└────────┬────────┘
         │ HTTP/REST
         │
┌────────▼────────┐
│  PingFederate   │
│  Admin API      │
└─────────────────┘
```

## Components

### 1. MCP Server (`server.py`)
- Implements the Model Context Protocol
- Registers available tools
- Routes tool calls to appropriate handlers
- Manages server lifecycle

### 2. PingFederate Client (`client.py`)
- Handles HTTP communication with PingFederate
- Implements authentication
- Provides typed API methods
- Manages error handling

### 3. Data Models (`models/`)
- Pydantic models for type safety
- Based on OpenAPI schemas
- Validation and serialization

### 4. Configuration (`config.py`)
- Environment-based configuration
- Settings management
- Credential handling

## Spec Driven Development Flow

1. **Specification Phase**
   - Define API operations in OpenAPI format
   - Document request/response schemas
   - Specify authentication requirements

2. **Code Generation Phase**
   - Generate Pydantic models from OpenAPI schemas
   - Create client method stubs
   - Generate MCP tool definitions

3. **Implementation Phase**
   - Implement client methods
   - Create MCP tool handlers
   - Add business logic

4. **Testing Phase**
   - Generate test cases from specifications
   - Validate against OpenAPI schemas
   - Integration testing

5. **Documentation Phase**
   - Auto-generate API docs from specs
   - Create usage examples
   - Update README

## Design Principles

### 1. Specification as Source of Truth
- OpenAPI specs define the contract
- All code must conform to specs
- Validation against specs in tests

### 2. Separation of Concerns
- Server: MCP protocol handling
- Client: API communication
- Models: Data structures
- Config: Environment settings

### 3. Type Safety
- Pydantic models for runtime validation
- MyPy for static type checking
- JSON Schema for MCP tools

### 4. Error Handling
- Structured error responses
- Clear error messages
- Proper HTTP status codes

### 5. Testability
- Unit tests for each component
- Integration tests with mock API
- Specification-based validation

## Data Flow

```
User Request (AI Assistant)
    ↓
MCP Protocol Message
    ↓
Server.call_tool()
    ↓
Client API Method
    ↓
HTTP Request (httpx)
    ↓
PingFederate Admin API
    ↓
HTTP Response
    ↓
Pydantic Model Validation
    ↓
MCP Response
    ↓
AI Assistant
```

## Security

### Authentication
- HTTP Basic Authentication
- Credentials from environment variables
- No credentials in code

### SSL/TLS
- Configurable SSL verification
- Support for self-signed certificates in dev
- Enforce SSL in production

### Secrets Management
- Environment variables only
- `.env` file for development
- Secret manager for production

## Extensibility

### Adding New Tools

1. Add operation to OpenAPI spec
2. Update client with new method
3. Register tool in server
4. Add tests
5. Update documentation

### Adding New Features

1. Update specifications first
2. Generate/update models
3. Implement changes
4. Validate against specs
5. Update documentation

## Performance Considerations

- Async/await for non-blocking I/O
- Connection pooling (httpx)
- Pagination for large result sets
- Caching where appropriate

## Monitoring & Logging

- Structured logging
- Request/response logging
- Error tracking
- Performance metrics
