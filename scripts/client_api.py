"""Module python utilisé pour l'intéraction avec l'API """

import requests
import backoff
import logging
from scripts.utils.schemas.authentification import (
    GeneralConfig,
    EndPointConfig,
    AuthConfig,
)


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
request_logger = logging.getLogger(__name__)


class TokenExpired(Exception):
    "Exception pour gérer les expiration de l'access token"


class APIclient:

    def __init__(self, config: GeneralConfig) -> None:
        self.base_url: str = config.access_point
        self.auth_config: AuthConfig = config.auth_config
        self.endpoints: list[EndPointConfig] = config.endpoint_list
        self.access_token: str = None

    @backoff.on_predicate(
        backoff.runtime,
        predicate=lambda r: r is not None and r.status_code == 429,
        value=lambda r: int(r.headers.get("Retry-After")),
        logger=request_logger,
    )
    @backoff.on_exception(
        backoff.expo,
        raise_on_giveup=True,
        exception=TokenExpired,
        max_tries=5,
        logger=request_logger,
    )
    def _get_endpoint_data(self, endpoint: EndPointConfig):

        try:
            response = requests.request(
                method=endpoint.method,
                url=endpoint.complete_url,
                params=endpoint.params,
                headers={"Authorization": f"Bearer {self.access_token}"},
                timeout=30,
            )

            if response.status_code == 401:
                self._retrieve_access_token()
                raise TokenExpired

            response.raise_for_status()

            return response

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code

            error_details = e.response.json()
            error_description = error_details.get(
                "error_description", "No description available"
            )
            error_message = (
                f"HTTPError: Status Code {status_code}. "
                f"Error: {error_details.get('error', 'Unknown')}. "
                f"Description: {error_description}."
            )
            request_logger.error(error_message)
            raise requests.exceptions.HTTPError(error_message)

    @backoff.on_exception(
        backoff.expo,
        raise_on_giveup=True,
        exception=requests.exceptions.Timeout,
        max_time=300,
        logger=request_logger,
    )
    def _retrieve_access_token(self) -> str:
        "fonction utilisé pour générer le token d'accés"

        config = self.auth_config
        try:
            request_logger.info(
                f"Requete : {config.model_dump(exclude=['client_id','client_secret'])}"
            )
            response = requests.post(
                url=self.auth_config.url,
                headers=self.auth_config.headers,
                params=self.auth_config.params,
                data=self.auth_config.payload,
                timeout=30,
            )

            response.raise_for_status()

            request_logger.info(
                f"Access token généré pour les scopes {response.json().get('scope', 'unknown')}! "
                f"Expires dans {response.json().get('expires_in', 'unknown')} seconds."
            )

            self.access_token = response.json()["access_token"]

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            error_details = e.response.json()
            error_description = error_details.get(
                "error_description", "No description available"
            )
            error_message = (
                f"HTTPError: Status Code {status_code}. "
                f"Error: {error_details.get('error', 'Unknown')}. "
                f"Description: {error_description}."
            )
            request_logger.error(error_message)
            raise requests.exceptions.HTTPError(error_message)

    def fetch_and_load(self):
        """Fait un appel pour chaque endpoints lister du fichier de config
        et génére la donnée dans un dossier.
        """

        for endpoint in self.endpoints:
            output_dir = endpoint.output_path
            parser = endpoint.parser(
                data=self._get_endpoint_data(endpoint).json()["resultats"],
                dir_output_path=output_dir,
            )
            parser.run()
