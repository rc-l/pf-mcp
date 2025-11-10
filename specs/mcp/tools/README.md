# MCP Tools Specification for PingFederate

This directory contains MCP tool definitions that map OpenAPI operations to MCP tools.

## Tool Definition Format

Each tool is defined with:
- **name**: Unique tool identifier
- **description**: What the tool does
- **inputSchema**: JSON Schema for tool parameters
- **outputSchema**: Expected response format
- **mappings**: Connection to OpenAPI operations

## Available Tools

### OAuth Client Management

#### list_oauth_clients
Lists all OAuth 2.0 clients configured in PingFederate.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "page": {
      "type": "integer",
      "description": "Page number (default: 1)",
      "minimum": 1
    },
    "numberPerPage": {
      "type": "integer",
      "description": "Items per page (default: 10, max: 100)",
      "minimum": 1,
      "maximum": 100
    }
  }
}
```

**OpenAPI Mapping:** `GET /oauth/clients` (listOAuthClients)

---

#### create_oauth_client
Creates a new OAuth 2.0 client.

**Input Schema:**
```json
{
  "type": "object",
  "required": ["clientId", "name"],
  "properties": {
    "clientId": {
      "type": "string",
      "description": "Unique client identifier"
    },
    "name": {
      "type": "string",
      "description": "Client display name"
    },
    "description": {
      "type": "string",
      "description": "Client description"
    },
    "enabled": {
      "type": "boolean",
      "description": "Enable the client",
      "default": true
    },
    "grantTypes": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["authorization_code", "implicit", "resource_owner_credentials", "client_credentials", "refresh_token"]
      },
      "description": "Allowed OAuth grant types"
    },
    "redirectUris": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Allowed redirect URIs"
    }
  }
}
```

**OpenAPI Mapping:** `POST /oauth/clients` (createOAuthClient)

---

#### get_oauth_client
Retrieves details of a specific OAuth 2.0 client.

**Input Schema:**
```json
{
  "type": "object",
  "required": ["clientId"],
  "properties": {
    "clientId": {
      "type": "string",
      "description": "OAuth client ID"
    }
  }
}
```

**OpenAPI Mapping:** `GET /oauth/clients/{clientId}` (getOAuthClient)

---

#### update_oauth_client
Updates an existing OAuth 2.0 client configuration.

**Input Schema:**
```json
{
  "type": "object",
  "required": ["clientId"],
  "properties": {
    "clientId": {
      "type": "string",
      "description": "OAuth client ID to update"
    },
    "name": {
      "type": "string",
      "description": "Updated client name"
    },
    "description": {
      "type": "string",
      "description": "Updated description"
    },
    "enabled": {
      "type": "boolean",
      "description": "Enable/disable the client"
    },
    "grantTypes": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Updated grant types"
    },
    "redirectUris": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Updated redirect URIs"
    }
  }
}
```

**OpenAPI Mapping:** `PUT /oauth/clients/{clientId}` (updateOAuthClient)

---

#### delete_oauth_client
Deletes an OAuth 2.0 client.

**Input Schema:**
```json
{
  "type": "object",
  "required": ["clientId"],
  "properties": {
    "clientId": {
      "type": "string",
      "description": "OAuth client ID to delete"
    }
  }
}
```

**OpenAPI Mapping:** `DELETE /oauth/clients/{clientId}` (deleteOAuthClient)

---

### Identity Provider Management

#### list_idp_adapters
Lists all identity provider adapters.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {}
}
```

**OpenAPI Mapping:** `GET /idp/adapters` (listIdpAdapters)

---

### System

#### get_version
Gets the PingFederate server version.

**Input Schema:**
```json
{
  "type": "object",
  "properties": {}
}
```

**OpenAPI Mapping:** `GET /version` (getVersion)

---

## Tool Implementation Guidelines

1. **Validation**: Always validate inputs against the schema
2. **Error Handling**: Return clear error messages
3. **Authentication**: Include credentials in all API calls
4. **Logging**: Log all operations for debugging
5. **Rate Limiting**: Respect API rate limits

## Adding New Tools

To add a new tool:

1. Define the operation in `specs/openapi/pingfederate-api.yaml`
2. Add tool specification in this directory
3. Implement in `src/pf_mcp/tools/`
4. Add tests in `tests/unit/tools/`
5. Update documentation
