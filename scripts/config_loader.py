import os
import yaml
from dotenv import load_dotenv
from scripts.utils import get_parser
from scripts.utils.schemas.authentification import (
    AuthConfig,
    GeneralConfig,
    EndPointConfig,
)

# charger les variables d'environnement
load_dotenv("../config/.env")

YAML_PATH = "../config/config.yaml"
with open(YAML_PATH, "r") as file:
    yaml_config = yaml.safe_load(file)


def get_outputs_path(config_path: str, relative_output_path: str) -> str:
    """Fonction permettant de créer un chemin absolue à partir du
    chemin du fichier de config et le chemin relatif souahité.

    Args:
        config_path (str) : chemin du fichier de configuration
        relative_output_path (str): chemin relatif indiquant le dossier d'extract

    Returns:
        le chemin absolue

    """
    yaml_dir = os.path.dirname(os.path.abspath(config_path))
    absolute_path = os.path.abspath(os.path.join(yaml_dir, relative_output_path))

    return absolute_path


def load_config() -> GeneralConfig:
    "Fonction permettant de charger les paramètre de configuration"

    auth_infos = yaml_config["auth"]
    api_infos = yaml_config["api"]

    relative_path = yaml_config["outputs"]["csv_path"]

    auth_config = AuthConfig(
        url=auth_infos["url"],
        params=auth_infos["params"],
        headers=auth_infos["headers"],
        grant_type=auth_infos["payload"]["grant_type"],
        scopes=" ".join(auth_infos["payload"]["scopes"]),
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
    )

    endpoint_list = []
    for api in api_infos["api_list"]:
        for endpoint in api["endpoints"]:

            complete_url = api_infos["access_point"] + api["path"] + endpoint["value"]
            endpoint_config = EndPointConfig(
                api_name=api["name"],
                complete_url=complete_url,
                value=endpoint["value"],
                params=endpoint.get("params"),
                method=endpoint["method"],
                output_path=get_outputs_path(YAML_PATH, relative_path),
                parser=get_parser(api["name"], endpoint["value"]),
            )

            endpoint_list.append(endpoint_config)

    return GeneralConfig(
        access_point=api_infos["access_point"],
        endpoint_list=endpoint_list,
        auth_config=auth_config,
    )
