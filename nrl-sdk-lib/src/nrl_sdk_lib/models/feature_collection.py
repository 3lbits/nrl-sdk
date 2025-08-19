"""Module for a simplified feature collection model."""

from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from .crs import Crs
from .geometry import LineString, Point, Polygon


class Parent(BaseModel):
    """A base model for all other models."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",  # Forbid extra fields
    )


class FeatureStatus(str, Enum):
    """An enumeration for feature property statuses.

    This enumeration defines the possible statuses for feature properties in the NRL.

    Attributes:
        eksisterende (str): Represents an existing feature.
        fjernet (str): Represents a feature that has been removed.
        planlagt_fjernet (str): Represents a feature that is planned to be removed.
        planlagt_oppført (str): Represents a feature that is planned to be constructed.
        erstattet (str): Represents a feature that has been replaced.

    """

    eksisterende = "eksisterende"
    fjernet = "fjernet"
    planlagt_fjernet = "planlagtFjernet"
    planlagt_oppført = "planlagtOppført"
    erstattet = "erstattet"


class LuftfartsHinderMerking(str, Enum):
    """An enumeration for luftfartshindermerking.

    This enumeration defines the possible markings for aviation obstacles.

    Attributes:
        fargermerking (str): Represents color marking.
        markør (str): Represents a marker.

    """

    fargermerking = "fargemerking"
    markør = "markør"


class LuftfartsHinderLyssetting(str, Enum):
    """An enumeration for luftfartshinderlyssetting.

    This enumeration defines the possible lighting settings for aviation obstacles.

    Attributes:
        belyst_med_flomlys (str): Represents lighting with floodlights.
        blinkende_hvitt (str): Represents blinking white lights.
        blinkende_rødt (str): Represents blinking red lights.
        fast_hvitt (str): Represents steady white lights.
        fast_rødt (str): Represents steady red lights.
        høyintensitet_type_a (str): Represents high-intensity type A lighting.
        høyintensitet_type_b (str): Represents high-intensity type B lighting.
        lavintensitet_type_a (str): Represents low-intensity type A lighting.
        lavintensitet_type_b (str): Represents low-intensity type B lighting.
        lyssatt (str): Represents illuminated features.
        mellomintensitet_type_a (str): Represents medium-intensity type A lighting.
        mellomintensitet_type_b (str): Represents medium-intensity type B lighting.
        mellomintensitet_type_c (str): Represents medium-intensity type C lighting.

    """

    belyst_med_flomlys = "belystMedFlomlys"
    blinkende_hvitt = "blinkendeHvitt"
    blinkende_rødt = "blinkendeRødt"
    fast_hvitt = "fastHvitt"
    fast_rødt = "fastRødt"
    høyintensitet_type_a = "høyintensitetTypeA"
    høyintensitet_type_b = "høyintensitetTypeB"
    lavintensitet_type_a = "lavintensitetTypeA"
    lavintensitet_type_b = "lavintensitetTypeB"
    lyssatt = "lyssatt"
    mellomintensitet_type_a = "mellomintensitetTypeA"
    mellomintensitet_type_b = "mellomintensitetTypeB"
    mellomintensitet_type_c = "mellomintensitetTypeC"


class Høydereferanse(str, Enum):
    """An enumeration for height references.

    This enumeration defines the possible height references used in the NRL.

    Attributes:
        fot (str): Represents height at the bottom.
        topp (str): Represents height at the top.

    """

    fot = "fot"
    topp = "topp"


class PunktType(str, Enum):
    """An enumeration for punkt types."""

    annet = "annet"
    """A generic point type."""

    bygning = "bygning"
    """A point representing a building."""

    flaggstang = "flaggstang"
    """A point representing a flagpole."""

    forankret_ballong = "forankretBallong"
    """A point representing an anchored balloon."""

    fornøyelsesparkinnretning = "fornøyelsesparkinnretning"
    """A point representing an amusement park attraction."""

    fyrtårn = "fyrtårn"
    """A point representing a lighthouse."""

    hopptårn = "hopptårn"
    """A point representing a ski jump tower."""

    kjøletårn = "kjøletårn"
    """A point representing a cooling tower."""

    kontrolltårn = "kontrolltårn"
    """A point representing a control tower."""

    kraftverk = "kraftverk"
    """A point representing a power plant."""

    kran = "kran"
    """A point representing a crane."""

    kuppel = "kuppel"
    """A point representing a dome."""

    monument = "monument"
    """A point representing a monument."""

    navigasjonshjelpemiddel = "navigasjonshjelpemiddel"
    """A point representing a navigation aid."""

    petroleumsinnretning = "petroleumsinnretning"
    """A point representing a petroleum installation."""

    pipe = "pipe"
    """A point representing a chimney."""

    raffineri = "raffineri"
    """A point representing a refinery."""

    silo = "silo"
    """A point representing a silo."""

    sprengningstårn = "sprengningstårn"
    """A point representing a blasting tower."""

    tank = "tank"
    """A point representing a tank."""

    tårn = "tårn"
    """A point representing a tower."""

    vanntårn = "vanntårn"
    """A point representing a water tower."""

    vindturbin = "vindturbin"
    """A point representing a wind turbine."""


class Materiale(str, Enum):
    """An enumeration for materials."""

    annet = "annet"
    """Generic material type."""

    betong = "betong"
    """Concrete material."""

    glass = "glass"
    """Glass material."""

    metall = "metall"
    """Metal material."""

    murstein = "murstein"
    """Brick material."""

    stein = "stein"
    """Stone material."""

    trevirke = "trevirke"
    """Wood material."""


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
    """A KomponentReferanse model.

    The KomponentReferanse model represents a reference to a component in the NRL.

    Attributes:
        kodesystemversjon (str | None): Version of the code system.
        komponentkodesystem (str | None): Code system for the component.
        komponentkodeverdi (str | None): Value of the component code.

    """

    kodesystemversjon: str | None = None
    komponentkodesystem: str | None = None
    komponentkodeverdi: str | None = None


class Kvalitet(Parent):
    """A Kvalitet model.

    Attributes:
        datafangstmetode (DatafangsMetode | None): Method of data capture.
        nøyaktighet (int | None): Accuracy of the data capture.
        datafangstmetode_høyde (DatafangsMetode | None): Method of data capture for height.
        nøyaktighet_høyde (int | None): Accuracy of the data capture for height.

    """

    datafangstmetode: DatafangsMetode | None = None
    nøyaktighet: int | None = None
    datafangstmetode_høyde: DatafangsMetode | None = None
    nøyaktighet_høyde: int | None = None


class FeatureProperty(Parent):
    """A FeatureProperty abstract base class model.

    Attributes:
        feature_type (Literal): Type of the feature, e.g., "NrlPunkt
        status (FeatureStatus): Status of the feature.
        komponentident (UUID): Unique identifier for the component.
        verifisert_rapporteringsnøyaktighet (Literal): Verified reporting accuracy.
        referanse (KomponentReferanse | None): Reference to the component, if applicable.
        navn (str | None): Name of the feature, if applicable.
        vertikal_avstand (float | None): Vertical distance, if applicable.
        luftfartshindermerking (LuftfartsHinderMerking | None): Aviation obstacle marking, if applicable.
        luftfartshinderlyssetting (LuftfartsHinderLyssetting | None): Aviation obstacle lighting, if applicable.
        materiale (Materiale | None): Material of the feature, if applicable.
        datafangstdato (str | None): Date of data capture, if applicable.
        kvalitet (Kvalitet | None): Quality of the feature, if applicable.
        informasjon (str | None): Additional information about the feature, if applicable.
        høydereferanse (Høydereferanse | None): Height reference, if applicable.

    """

    feature_type: Literal["NrlPunkt", "NrlMast", "NrlLuftspenn", "NrlLinje", "NrlFlate"]
    status: FeatureStatus
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
    høydereferanse: Høydereferanse | None = None


class FlateType(str, Enum):
    """An enumeration for flate types."""

    kontaktledning = "kontaktledning"
    """Contact line type, typically used for overhead power lines."""

    trafostasjon = "trafostasjon"
    """Transformer station type, typically used for electrical substations."""


class NrlFlate(FeatureProperty):
    """A Nrl Flate model.

    To create a NrlFlate:
    ```python
    >>> from uuid import UUID
    >>>
    >>> from nrl_sdk_lib.models import NrlFlate, FeatureStatus, FlateType
    >>>
    >>> nrl_flate = NrlFlate(
    ... feature_type="NrlFlate",
    ... status=FeatureStatus.eksisterende,
    ... komponentident=UUID("12345678-1234-5678-1234-567812345678"),
    ... verifisert_rapporteringsnøyaktighet="20230101_5-1",
    ... flate_type=FlateType.trafostasjon,
    ... )
    >>> # Do something with nrl_flate, e.g. add it to a feature collection

    ```
    """

    flate_type: FlateType


class NrlLinje(FeatureProperty):
    """A Nrl Linje model.

    Attributes:
        linje_type (str): Type of the line, e.g., "høgspent
        anleggsbredde (float | None): Width of the facility, if applicable.

    """

    linje_type: str
    anleggsbredde: float | None = None


class LuftspennType(str, Enum):
    """An enumeration for luftspenn types."""

    annet = "annet"
    """Generic type for unspecified air spans."""

    bardun = "bardun"
    """Type for guyed spans, typically used for supporting structures."""

    gondolbane = "gondolbane"
    """Type for gondola cable cars, typically used in ski resorts or mountainous areas."""

    ekom = "ekom"
    """Type for communication lines, typically used for telecommunication or data transmission."""

    høgspent = "høgspent"
    """Type for high-voltage power lines, typically used for electrical transmission."""

    kontaktledning = "kontaktledning"
    """Type for contact lines, typically used in railways or tram systems."""

    lavspent = "lavspent"
    """Type for low-voltage power lines, typically used for local electrical distribution."""

    transmisjon = "transmisjon"
    """Type for transmission lines, typically used for long-distance electrical transmission."""

    regional = "regional"
    """Type for regional lines, typically used for medium-voltage electrical distribution."""

    løypestreng = "løypestreng"
    """Type for ski lift lines, typically used in ski resorts."""

    skitrekk = "skitrekk"
    """Type for ski tow lines, typically used in ski resorts."""

    stolheis = "stolheis"
    """Type for chairlift lines, typically used in ski resorts."""

    taubane = "taubane"
    """Type for cable car lines, typically used in ski resorts or mountainous areas."""

    vaier = "vaier"
    """Type for cable lines, typically used for various purposes including ski lifts and gondolas."""

    zipline = "zipline"
    """Type for zip lines, typically used for recreational activities."""


class NrlLuftspenn(FeatureProperty):
    """A Nrl Luftspenn model.

    Attributes:
        luftspenn_type (LuftspennType): Type of the air span.
        anleggsbredde (float | None): Width of the facility, if applicable.
        friseilingshøyde (float | None): Height of the free span,
            if applicable.
        nrl_mast (list[UUID] | None): List of UUIDs for associated Nrl Mast, if applicable.

    """

    luftspenn_type: LuftspennType
    anleggsbredde: float | None = None
    friseilingshøyde: float | None = None
    nrl_mast: list[UUID] | None = None


class MastType(str, Enum):
    """An enumeration for mast types."""

    annet = "annet"
    """Generic type for unspecified masts."""

    belysningsmast = "belysningsmast"
    """Type for lighting masts, typically used for street or area lighting."""

    ekommast = "ekommast"
    """Type for communication masts, typically used for telecommunication or data transmission."""

    høgspentmast = "høgspentmast"
    """Type for high-voltage masts, typically used for electrical transmission."""

    kontaktledningsmast = "kontaktledningsmast"
    """Type for contact line masts, typically used in railways or tram systems."""

    lavspentmast = "lavspentmast"
    """Type for low-voltage masts, typically used for local electrical distribution."""

    transmisjonmast = "transmisjonmast"
    """Type for transmission masts, typically used for long-distance electrical transmission."""

    regionalmast = "regionalmast"
    """Type for regional masts, typically used for medium-voltage electrical distribution."""

    målemast = "målemast"
    """Type for measurement masts, typically used for environmental or structural monitoring."""

    radiomast = "radiomast"
    """Type for radio masts, typically used for broadcasting or communication."""

    taubanemast = "taubanemast"
    """Type for cable car masts, typically used in ski resorts or mountainous areas."""

    telemast = "telemast"
    """Type for telecommunication masts, typically used for mobile or fixed-line communication."""


class NrlMast(FeatureProperty):
    """A Nrl Mast model.

    Attributes:
        mast_type (MastType): Type of the mast.
        horisontal_avstand (float | None): Horizontal distance to the next mast, if applicable.
        nrl_luftspenn (list[UUID] | None): List of UUIDs for associated Nrl Luftspenn, if applicable.

    """

    mast_type: MastType
    horisontal_avstand: float | None = None
    nrl_luftspenn: list[UUID] | None = None


class NrlPunkt(FeatureProperty):
    """A Nrl Punkt model.

    Attributes:
        punkt_type (PunktType): Type of the point.
        horisontal_avstand (float | None): Horizontal distance to the next point, if applicable.

    """

    punkt_type: PunktType
    horisontal_avstand: float | None = None


class Feature(Parent):
    """A Feature model.

    Attributes:
        type (str): The type of the feature, typically "Feature".
        geometry (Point | Polygon | LineString): The geometry of the feature, which can be
            a Point, Polygon, or LineString.

    """

    type: str = "Feature"
    geometry: Point | Polygon | LineString
    properties: NrlPunkt | NrlMast | NrlLuftspenn | NrlLinje | NrlFlate


class FeatureCollection(Parent):
    """A FeatureCollection model.

    The FeatureCollection model represents a collection of geographic features with associated geometries and properties.

    How to create a FeatureCollection from a JSON file:
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

    How to create a FeatureCollection programmatically:
    ```python
    >>> from uuid import UUID
    >>>
    >>> from nrl_sdk_lib.models import (
    ...     CrsProperties,
    ...     Feature,
    ...     Point,
    ...     NrlFlate,
    ...     FeatureStatus,
    ...     FlateType,
    ...     FeatureCollection,
    ...     Crs,
    ...     )
    >>>
    >>> nrl_flate = NrlFlate(
    ...     feature_type="NrlFlate",
    ...     status=FeatureStatus.eksisterende,
    ...     komponentident=UUID("12345678-1234-5678-1234-567812345678"),
    ...     verifisert_rapporteringsnøyaktighet="20230101_5-1",
    ...     flate_type=FlateType.trafostasjon,
    ... )
    >>>
    >>> feature = Feature(
    ...     type="Feature",
    ...     geometry=Point(type="Point", coordinates=[10.0, 59.0]),
    ...     properties=nrl_flate,
    ... )
    >>>
    >>> feature_collection = FeatureCollection(
    ...     crs=Crs(properties=CrsProperties(name="EPSG:4326")),
    ...     features=[feature],
    ... )
    >>>
    >>> # Do something with feature_collection, e.g. serialize it to JSON:
    >>> # print(feature_collection.serialize())
    ```

    Attributes:
        type (str): The type of the collection, typically "FeatureCollection".
        crs (Crs): The coordinate reference system of the features in the collection.
        features (list[Feature]): A list of features in the collection, each with its own geometry and properties.

    Methods:
        serialize: Converts the FeatureCollection instance to a JSON string.

    """

    type: str = "FeatureCollection"
    crs: Crs
    features: list[Feature]

    async def serialize(self) -> str:
        """Serialize the FeatureCollection to a JSON string.

        This method converts the FeatureCollection instance to a JSON string.
        The serialization will exclude any fields that are None, and
        field names in the serialization will be in camelCase.
        """
        return self.model_dump_json(exclude_none=True, by_alias=True)
