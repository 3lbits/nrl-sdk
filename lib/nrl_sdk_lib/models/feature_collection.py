"""Module for a simplified feature collection model."""

from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Parent(BaseModel):
    """A base model for all other models."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",  # Forbid extra fields
    )


class Geometry(Parent):
    """A Geometry model."""

    model_config = ConfigDict(
        extra="forbid",  # Forbid extra fields
    )

    type: Literal["Point", "Polygon", "LineString"]


class Point(Geometry):
    """A Point geometry model."""

    coordinates: list[float]


class Polygon(Geometry):
    """A Polygon geometry model."""

    coordinates: list[list[list[float]]]


class LineString(Geometry):
    """A LineString geometry model."""

    coordinates: list[list[float]]


class CrsProperties(Parent):
    """A CRS properties model."""

    name: str


class Crs(Parent):
    """A CRS model."""

    model_config = ConfigDict(
        extra="forbid",  # Forbid extra fields
    )

    type: str
    properties: CrsProperties


class FeaturePropertyStatus(str, Enum):
    """An enumeration for feature property statuses."""

    eksisterende = "eksisterende"
    fjernet = "fjernet"
    planlagt_fjernet = "planlagtFjernet"
    planlagt_oppfort = "planlagtOppført"
    erstattet = "erstattet"


class LuftfartsHinderMerking(str, Enum):
    """An enumeration for luftfartshindermerking."""

    fargermerking = "fargemerking"
    markor = "markør"


class LuftfartsHinderLyssetting(str, Enum):
    """An enumeration for luftfartshinderlyssetting."""

    belyst_med_flomlys = "belystMedFlomlys"
    blinkende_hvitt = "blinkendeHvitt"
    blinkende_rodt = "blinkendeRødt"
    fast_hvitt = "fastHvitt"
    fast_rodt = "fastRødt"
    høyintensitet_type_a = "høyintensitetTypeA"
    høyintensitet_type_b = "høyintensitetTypeB"
    lavintensitet_type_a = "lavintensitetTypeA"
    lavintensitet_type_b = "lavintensitetTypeB"
    lyssatt = "lyssatt"
    mellomintensitet_type_a = "mellomintensitetTypeA"
    mellomintensitet_type_b = "mellomintensitetTypeB"
    mellomintensitet_type_c = "mellomintensitetTypeC"


class Hoydereferanse(str, Enum):
    """An enumeration for height references."""

    fot = "fot"
    topp = "topp"


class PunktType(str, Enum):
    """An enumeration for punkt types."""

    annet = "annet"
    bygning = "bygning"
    flaggstang = "flaggstang"
    forankret_ballong = "forankretBallong"
    fornøyelsesparkinnretning = "fornøyelsesparkinnretning"
    fyrtårn = "fyrtårn"
    hopptårn = "hopptårn"
    kjøletårn = "kjøletårn"
    kontrolltårn = "kontrolltårn"
    kraftverk = "kraftverk"
    kran = "kran"
    kuppel = "kuppel"
    monument = "monument"
    navigasjonshjelpemiddel = "navigasjonshjelpemiddel"
    petroleumsinnretning = "petroleumsinnretning"
    pipe = "pipe"
    raffineri = "raffineri"
    silo = "silo"
    sprengningstårn = "sprengningstårn"
    tank = "tank"
    tårn = "tårn"
    vanntårn = "vanntårn"
    vindturbin = "vindturbin"


class Materiale(str, Enum):
    """An enumeration for materials."""

    annet = "annet"
    betong = "betong"
    glass = "glass"
    metall = "metall"
    murstein = "murstein"
    stein = "stein"
    trevirke = "trevirke"


class DatafangsMetode(str, Enum):
    """An enumeration for data capture methods."""

    dig = "dig"
    fot = "fot"
    gen = "gen"
    lan = "lan"
    pla = "pla"
    sat = "sat"
    byg = "byg"
    ukj = "ukj"


class KomponentReferanse(Parent):
    """A KomponentReferanse model."""

    kodesystemversjon: str | None = None
    komponentkodesystem: str | None = None
    komponentkodeverdi: str | None = None


class Kvalitet(Parent):
    """A Kvalitet model."""

    datafangstmetode: DatafangsMetode | None = None
    nøyaktighet: float | None = None
    datafangstmetode_høyde: DatafangsMetode | None = None
    nøyaktighet_høyde: float | None = None


class FeatureProperty(Parent):
    """A FeatureProperty model."""

    feature_type: Literal["NrlPunkt", "NrlMast", "NrlLuftspenn", "NrlLinje", "NrlFlate"]
    status: FeaturePropertyStatus
    komponentident: UUID
    verifisert_rapporteringsnøyaktighet: Literal["20230101_5-1", "0"]
    referanse: KomponentReferanse | None = None
    navn: str | None = None
    vertikal_avstand: float | None = None
    luftfartshindermerking: LuftfartsHinderMerking | None = None
    luftfartshinderlyssetting: LuftfartsHinderLyssetting | None = None
    materiale: Materiale | None = None
    datafangstdato: str | None = None
    kvalitet: Kvalitet | None = None
    informasjon: str | None = None
    høydereferanse: Hoydereferanse | None = None


class FlateType(str, Enum):
    """An enumeration for flate types."""

    kontaktledning = "kontaktledning"
    trafostasjon = "trafostasjon"


class NrlFlate(FeatureProperty):
    """A Nrl Flate model."""

    flate_type: FlateType


class NrlLinje(FeatureProperty):
    """A Nrl Linje model."""

    linje_type: str
    anleggsbredde: float | None = None


class LuftspennType(str, Enum):
    """An enumeration for luftspenn types."""

    annet = "annet"
    bardun = "bardun"
    gondolbane = "gondolbane"
    ekom = "ekom"
    hogspent = "høgspent"
    kontaktledning = "kontaktledning"
    lavspent = "lavspent"
    transmisjon = "transmisjon"
    regional = "regional"
    loypestreng = "løypestreng"
    skitrekk = "skitrekk"
    stolheis = "stolheis"
    taubane = "taubane"
    vaier = "vaier"
    zipline = "zipline"


class NrlLuftspenn(FeatureProperty):
    """A Nrl Luftspenn model."""

    luftspenn_type: LuftspennType
    anleggsbredde: float | None = None
    friseilingshøyde: float | None = None
    nrl_mast: list[UUID] | None = None


class NrlMast(FeatureProperty):
    """A Nrl Mast model."""

    mast_type: str
    horisontal_avstand: float | None = None
    nrl_luftspenn: list[UUID] | None = None


class NrlPunkt(FeatureProperty):
    """A Nrl Punkt model."""

    punkt_type: PunktType
    horisontal_avstand: float | None = None


class Feature(Parent):
    """A Feature model."""

    type: str
    geometry: Point | Polygon | LineString
    properties: NrlPunkt | NrlMast | NrlLuftspenn | NrlLinje | NrlFlate


class FeatureCollection(Parent):
    """A FeatureCollection model.

    Example usage:
    ```python
    >>> from pydantic import ValidationError
    >>> from nrl_sdk_lib.models import FeatureCollection
    >>>
    >>> testfile_path = "tests/files/Eksempelfil_NRLRapportering-1.0.1.json"
    >>> with open(testfile_path) as file:
    ...     data = file.read()
    >>>
    >>> try:
    ...     feature_collection = FeatureCollection.model_validate_json(data)
    ... except ValidationError as e:
    ...     print(e.errors())

    ```
    """

    type: str
    crs: Crs
    features: list[Feature]
    id: UUID | None = None
