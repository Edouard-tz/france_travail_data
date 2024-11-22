"""Module utilisé pour définir les parser liées aux endpoints de l'API offre """

import os
from typing import Any
import logging
import pandas as pd
from scripts.utils.parser.base import Parser
from scripts.utils.schemas.offres import Offre


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class SearchParser(Parser):
    """Classe utilisée pour parser la réponse
    du endpoint /Search
    """

    dir_output_path: str

    def _parse(self, data: Any) -> dict[str, pd.DataFrame]:
        """
        Implémente le parsing de la donnée reçus.
        :return: Une liste d'instance de `Offre`.
        """
        competence_list = []
        offre_list = []
        entreprise_list = []
        for records in data:
            offre = Offre(**records)

            competences = offre.competences
            entreprise = offre.entreprise

            offre_list.append(offre.model_dump())
            entreprise_list.append(entreprise.model_dump())
            if competences:
                competence_list.extend(competences)

        competence_list = [
            competence.model_dump() for competence in competence_list if competence
        ]

        offre_df = pd.DataFrame(offre_list).rename(
            {"entreprise": "entreprise_id", "competences": "competence_id"}, axis=1
        )
        offre_df = offre_df.explode("competence_id")

        logging.info("Parsing terminée !")
        return {
            "offre": offre_df,
            "competence": pd.DataFrame(competence_list).drop_duplicates(),
            "entreprise": pd.DataFrame(entreprise_list).drop_duplicates(),
        }

    def _generate_output(self, parsed_data: dict[str, pd.DataFrame]):
        """
        Génère le/les formats de sortie aprés traitement de la donnée.

        Args:
          parsed_data (dict): Les données parsées issue de la method self.parse().

        Returns:
          None
        """

        os.makedirs(self.dir_output_path, exist_ok=True)

        for name, df in parsed_data.items():
            output_path = os.path.join(self.dir_output_path, name + ".csv")
            df.to_csv(output_path, index=False)

        logging.info(f"Donnée sont chargé dans le dossier {self.dir_output_path} !")
