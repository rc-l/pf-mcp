# PingFederate MCP Server

A Model Context Protocol (MCP) server for PingFederate, enabling AI agents to interact with PingFederate's administrative API.

## Quick Links
- **Admin Console**: https://localhost:9999/pingfederate/app#/
- **API Docs**: https://localhost:9999/pf-admin-api/api-docs/

## Repository Structure

```
pf-mcp/
├── .github/
│   └── instructions          # Agent memory structure documentation
├── agent/                    # Agent memory files (living documents)
├── docker/                   # PingFederate test environment
├── src/
│   └── pf_mcp/               # MCP server source code
├── swagger.json              # PingFederate API specification
├── pyproject.toml            # Python project configuration
├── LICENSE
└── README.md
```

## Purpose

This MCP server provides AI agents with the ability to:
- Query and manage PingFederate configurations
- Interact with PingFederate's administrative API
- Use spec-driven approaches for PingFederate automation

The server is designed to be used in other projects that need programmatic access to PingFederate functionality.

## Development Setup

### Prerequisites
- Python 3.12+
- Docker and Docker Compose (for testing with PingFederate)

### Running PingFederate (for testing)
```bash
cd docker
docker compose up
```

PingFederate will be available at:
- Admin Console: https://localhost:9999/pingfederate/app
- API: https://localhost:9999/pf-admin-api

## Agent Memory System

This project uses a structured agent memory system in the `/agent` directory. These files are living documents that reflect the current state of the project. See `.github/instructions` for detailed information on how to maintain these files.