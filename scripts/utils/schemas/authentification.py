"""Module utilisé pour lister l'ensemble des schémas d'authentification"""

from typing import Optional, Any
from pydantic import BaseModel, field_validator

from scripts.utils.parser.base import Parser


class AuthConfig(BaseModel):
    "simple classe pour géré les paramètre d'authentification"
    url: str
    params: dict | None
    headers: dict
    grant_type: str
    scopes: str
    client_id: str
    client_secret: str

    @property
    def payload(self) -> dict:
        "payload utilisé pour la requête d'authentification"
        return {
            "grant_type": self.grant_type,
            "scope": self.scopes,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }


class EndPointConfig(BaseModel):
    """classe permetant de centraliser
    les information lié à un endpoint
    """

    api_name: str
    complete_url: str
    params: Optional[dict] = None
    method: str
    output_path: str
    parser: Any


class GeneralConfig(BaseModel):
    "paramètres généraux"
    access_point: str = "https://api.francetravail.io/partenaire"
    endpoint_list: list[EndPointConfig]
    auth_config: AuthConfig
