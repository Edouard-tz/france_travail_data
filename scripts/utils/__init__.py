"ensemble de fonction et class utils"
from scripts.utils.parser.base import Parser
from scripts.utils.parser.offre import SearchParser

PARSER_DICT = {
    "offres": {
        "/search": SearchParser,
    }
}


def get_parser(api_name: str, endpoint: str) -> Parser:
    """Récupère le parser approprié pour un API donné et un endpoint spécifique.

    Cette fonction permet de sélectionner et de retourner le parser adapté
    en fonction du nom de l'API et de l'endpoint spécifié.

    Args:
        api_name (str): Le nom de l'API pour laquelle récupérer un parser.
        endpoint (str): Le chemin ou point d'accès spécifique de l'API.

    Returns:
        Parser: l'objet parser correspondant à l'API et
        l'endpoint fournis.

    Raises:
        ValueError: Si aucun parser correspondant n'est trouvé.

    """

    try:
        parser = PARSER_DICT[api_name][endpoint]
    except KeyError as e:
        raise NotImplementedError(
            f"Mauvais endpoint : {api_name+endpoint} ou le parser n'as pas été encore implémenté"
        ) from e

    return parser
