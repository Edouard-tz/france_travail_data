"""Module qui sert à définir la classe abstraite utilisé comme struture de base pour les parser"""

from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Any, Union


class Parser(ABC, BaseModel):

    data: Union[dict, list]

    @abstractmethod
    def _parse(self, data: dict) -> BaseModel:
        """
        Méthode abstraite pour parser les données.
        Doit retourner une instance d'un modèle Pydantic validé.
        """
        pass

    @abstractmethod
    def _generate_output(self, parsed_data: BaseModel) -> Any:
        """
        Méthode abstraite pour générer une sortie à partir des données parsées.
        """
        pass

    def run(self) -> Any:
        """
        Exécute le parsing et génère la sortie.
        Returns:
             La sortie générée par `generate_output`.
        """
        parsed_data = self._parse(self.data)
        return self._generate_output(parsed_data)
