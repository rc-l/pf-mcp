"""Data models for PingFederate entities."""

from pydantic import BaseModel


class OAuthClient(BaseModel):
    """OAuth 2.0 client model."""

    clientId: str
    name: str
    description: str | None = None
    enabled: bool = True
    grantTypes: list[str] | None = None
    redirectUris: list[str] | None = None


class IdpAdapter(BaseModel):
    """Identity provider adapter model."""

    id: str
    name: str
    pluginDescriptorRef: dict[str, str]
    configuration: dict[str, any] | None = None
