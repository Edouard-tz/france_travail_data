# pylint: disable=no-self-argument, missing-function-docstring,missing-class-docstring
"""Module utilisé pour lister 
l'enssemble des schémas de validation pour 
les endpoints de l'API offre
"""


from pydantic import field_validator, field_serializer
from scripts.utils.schemas.base import NonNumberBaseModel
from typing import Optional
import hashlib
from uuid import uuid4


def generate_id_from_string(input_string: str) -> str:
    "Permet de générer des ids à partir de string"
    hash_object = hashlib.sha1(input_string.encode())
    unique_id = hash_object.hexdigest()
    return unique_id


class LieuTravail(NonNumberBaseModel):
    libelle: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    codePostal: Optional[str] = None
    commune: Optional[str] = None


class Entreprise(NonNumberBaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None
    logo: Optional[str] = None
    url: Optional[str] = None
    entrepriseAdaptee: bool
    entreprise_id: Optional[str] = None

    @field_serializer("entreprise_id")
    def serialize_entreprise_id(self, value: str) -> str:
        if not self.nom:
            return str(uuid4()).replace("-", "")
        else:
            return generate_id_from_string(self.nom)


class Formation(NonNumberBaseModel):
    codeFormation: Optional[str] = None
    domaineLibelle: Optional[str] = None
    niveauLibelle: Optional[str] = None
    commentaire: Optional[str] = None
    exigence: Optional[str] = None


class Langue(NonNumberBaseModel):
    libelle: Optional[str] = None
    exigence: Optional[str] = None


class Permis(NonNumberBaseModel):
    libelle: Optional[str] = None
    exigence: Optional[str] = None


class Competence(NonNumberBaseModel):
    code: Optional[str] = None
    libelle: Optional[str] = None
    exigence: Optional[str] = None
    competence_id: Optional[str] = None

    @field_serializer("competence_id")
    def serialize_competence_id(self, value: str) -> str:
        if self.code:
            return self.code
        else:
            str_id = str(self.libelle) + "_" + str(self.exigence)
            return generate_id_from_string(str_id)


class Salaire(NonNumberBaseModel):
    libelle: Optional[str] = None
    commentaire: Optional[str] = None
    complement1: Optional[str] = None
    complement2: Optional[str] = None


class Contact(NonNumberBaseModel):
    nom: Optional[str] = None
    coordonnees1: Optional[str] = None
    coordonnees2: Optional[str] = None
    coordonnees3: Optional[str] = None
    telephone: Optional[str] = None
    courriel: Optional[str] = None
    commentaire: Optional[str] = None
    urlRecruteur: Optional[str] = None
    urlPostulation: Optional[str] = None


class Agence(NonNumberBaseModel):
    telephone: Optional[str] = None
    courriel: Optional[str] = None


class QualiteProfessionnelle(NonNumberBaseModel):
    libelle: Optional[str] = None
    description: Optional[str] = None


class Partenaire(NonNumberBaseModel):
    nom: Optional[str] = None
    url: Optional[str] = None
    logo: Optional[str] = None


class OrigineOffre(NonNumberBaseModel):
    origine: Optional[str] = None
    urlOrigine: Optional[str] = None
    partenaires: Optional[list[Partenaire]] = None


class Offre(NonNumberBaseModel):
    id: str
    intitule: str
    description: str
    dateCreation: str
    dateActualisation: str
    lieuTravail: LieuTravail
    romeCode: str
    romeLibelle: str
    appellationlibelle: str
    entreprise: Entreprise
    typeContrat: str
    typeContratLibelle: str
    natureContrat: str
    experienceExige: Optional[str] = None
    experienceLibelle: Optional[str] = None
    experienceCommentaire: Optional[str] = None
    formations: Optional[list[Formation]] = None
    langues: Optional[list[Langue]] = None
    permis: Optional[list[Permis]] = None
    outilsBureautiques: Optional[list[str]] = None
    competences: Optional[list[Competence]] = None
    salaire: Salaire
    dureeTravailLibelle: str
    dureeTravailLibelleConverti: str
    complementExercice: Optional[str] = None
    conditionExercice: Optional[str] = None
    alternance: bool
    contact: Contact
    agence: Agence
    nombrePostes: int
    accessibleTH: bool
    deplacementCode: Optional[str] = None
    deplacementLibelle: Optional[str] = None
    qualificationCode: Optional[str] = None
    qualificationLibelle: str
    codeNAF: str
    secteurActivite: Optional[str] = None
    secteurActiviteLibelle: str
    qualitesProfessionnelles: Optional[list[QualiteProfessionnelle]] = None
    trancheEffectifEtab: Optional[str] = None
    origineOffre: OrigineOffre
    offresManqueCandidats: Optional[bool] = None

    @field_validator(
        "deplacementCode", "qualificationCode", "secteurActivite", mode="before"
    )
    def number_to_string(cls, v) -> str:
        if isinstance(v, int) or isinstance(v, float):
            return str(int(v))

    @field_serializer("competences")
    def serialize_competence_to_id(self, values) -> Optional[list[str]]:
        if values:
            new_list = []
            for competence in values:
                new_list.append(competence.model_dump()["competence_id"])

            return new_list
        else:
            return values

    @field_serializer("entreprise")
    def serialize_entreprise_to_id(self, value: list) -> Optional[str]:

        return value.model_dump()["entreprise_id"]
