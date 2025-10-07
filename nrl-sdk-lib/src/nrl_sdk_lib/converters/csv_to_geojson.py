"""Convert CSV data to GeoJSON FeatureCollections."""

import csv
import logging
import sys
import uuid
from pathlib import Path
from typing import IO, Literal

from nrl_sdk_lib.models import (
    Crs,
    CrsProperties,
    Feature,
    FeatureCollection,
    FeatureStatus,
    Høydereferanse,  #noqa: PLC2403
    KomponentReferanse,
    LineString,
    LuftfartsHinderLyssetting,
    LuftfartsHinderMerking,
    LuftspennType,
    MastType,
    NrlLuftspenn,
    NrlMast,
    Point,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(__name__)


def map_luftspenn_type(value: str | None) -> LuftspennType:
    """Map CSV value to LuftspennType."""
    mapping = {
        "Ledning, høyspent": LuftspennType.høgspent,
        "Ledning, lavspent": LuftspennType.lavspent,
        "Ledning, regionalnett": LuftspennType.regional,
    }
    result = mapping.get(value)
    if result is None:
        msg = f"Unknown Luftspenntype: {value}"
        raise ValueError(msg)
    return result

def map_mast_type(value: str | None) -> MastType:
    """Map CSV value to MastType."""
    mapping = {
        "Mast, høyspent": MastType.høgspentmast,
        "Mast, lavspent": MastType.lavspentmast,
        "Mast, regionalnett": MastType.regionalmast,
    }
    result = mapping.get(value)
    if result is None:
        msg = f"Unknown Masttype: {value}"
        raise ValueError(msg)
    return result

def map_feature_status(value: str | None) -> FeatureStatus:
    """Map CSV value to FeatureStatus."""
    mapping = {
        "Eksisterende": FeatureStatus.eksisterende,
        "eksisterende": FeatureStatus.eksisterende,
        "Planlagt oppført": FeatureStatus.planlagt_oppført,
        "planlagtOppført": FeatureStatus.planlagt_oppført,
        "Planlagt fjernet": FeatureStatus.planlagt_fjernet,
        "planlagtFjernet": FeatureStatus.planlagt_fjernet,
        "Fjernet": FeatureStatus.fjernet,
        "fjernet": FeatureStatus.fjernet,
    }
    result = mapping.get(value)
    if result is None:
        msg = f"Unknown Status: {value}"
        raise ValueError(msg)
    return result

def map_lighting_kind(value: str | None) -> LuftfartsHinderLyssetting | None:
    """Map CSV value to LuftfartsHinderLyssetting (optional)."""
    mapping = {
        "Lyssatt": LuftfartsHinderLyssetting.lyssatt,
        "Mellomintensitet, type A": LuftfartsHinderLyssetting.mellomintensitet_type_a,
        "Mellomintensitet, type B": LuftfartsHinderLyssetting.mellomintensitet_type_b,
        "Mellomintensitet, type C": LuftfartsHinderLyssetting.mellomintensitet_type_c,
        "Lavintensitet, type A": LuftfartsHinderLyssetting.lavintensitet_type_a,
        "Lavintensitet, type B": LuftfartsHinderLyssetting.lavintensitet_type_b,
        "Høyintensitet, type A": LuftfartsHinderLyssetting.høyintensitet_type_a,
        "Høyintensitet, type B": LuftfartsHinderLyssetting.høyintensitet_type_b,
    }
    if not value:
        return None
    return mapping.get(value)


def map_marking_kind(value: str | None) -> LuftfartsHinderMerking | None:
    """Map CSV value to LuftfartsHinderMerking (optional)."""
    mapping = {
        "Fargemerking": LuftfartsHinderMerking.fargermerking,
        "Markør": LuftfartsHinderMerking.markør,
    }
    if not value:
        return None
    return mapping.get(value)

def map_location_method(value: str | None) -> Literal["20230101_5-1", "0"]:
    """Map CSV value to location method string."""
    if value == "FOR-2020-10-16-2068, §5(1)":
        return "20230101_5-1"
    return "0"

def csv_to_geojson(file: str | Path | IO[str] | None = None) -> list[FeatureCollection]:
    """Convert CSV file to GeoJSON FeatureCollections grouped by CRS.

    Args:
        file: Can be:
            - None: reads from stdin
            - str or Path: path to CSV file
            - IO[str]: file-like object (already opened file)

    Returns:
        List of FeatureCollections grouped by CRS

    Examples:
        # From file path
        result = csv_to_geojson("data.csv")

        # From stdin
        result = csv_to_geojson()

        # From file object
        with open("data.csv") as f:
            result = csv_to_geojson(f)

    """
    if file is None:
        # Read from stdin
        logger.info("Reading CSV from stdin")
        return _process_csv_file(sys.stdin)
    if isinstance(file, (str, Path)):
        msg = f"Reading CSV from file: {file}"
        logger.info(msg)
        with Path(file).open(newline="", encoding="utf-8-sig") as csvfile:
            return _process_csv_file(csvfile)
    else:
        # Use provided file object
        logger.info("Reading CSV from file object")
        return _process_csv_file(file)


def _process_csv_file(csvfile: IO[str]) -> list[FeatureCollection]:
    """Process CSV file and return FeatureCollections grouped by CRS."""
    feature_by_crs = {}
    reader = csv.DictReader(csvfile, dialect="excel", delimiter=";")

    for row in reader:
        feature, crs = process_row(row)
        crs_name = crs.properties.name
        feature_by_crs.setdefault(crs_name, []).append(feature)

    return [
        FeatureCollection(
            crs=Crs(properties=CrsProperties(name=crs_name)), features=features
        )
        for crs_name, features in feature_by_crs.items()
    ]

def process_row(row: dict[str, str]) -> tuple[Feature, Crs]:
    """Process a single CSV row and return the appropriate feature."""
    table_id = row.get("Tabell ID")

    if table_id == "261":
        return (
            convert_guy_segments_rows(row)
            if row["Betegnelse"] == "Bardunline"
            else convert_ac_linesegments_rows(row)
        )
    if table_id == "109":
        return convert_overhead_structure_rows(row)

    msg = f"Unknown Tabell ID: {table_id}"
    logger.warning(msg)
    raise ValueError(msg)


def get_uuid(row: dict[str, str], *fields: str) -> uuid.UUID:
    """Extract and validate UUID from row fields."""
    for field in fields:
        value = row.get(field)
        if value:
            try:
                return uuid.UUID(value)
            except ValueError:
                continue
    msg = f"No valid UUID found in fields: {fields}"
    raise ValueError(msg)


def parse_float(value: str | None, field_name: str) -> float:
    """Parse float value with error handling."""
    if value is None:
        msg = f"Missing {field_name}"
        raise ValueError(msg)
    try:
        return float(value.replace(",", "."))
    except (ValueError, AttributeError) as e:
        msg = f"{field_name} is not a valid number: {value}"
        raise ValueError(msg) from e


def parse_coordinates(coords: list[str | None]) -> list[float]:
    """Parse and convert coordinate strings to floats."""
    return [
        float(c.replace(",", "."))
        for c in coords if isinstance(c, str) and c != ""]


def create_geometry(
    coordinates: list[list[str | None]], *,is_line: bool = True
) -> tuple[LineString | Point, Crs]:
    """Create LineString or Point geometry with appropriate CRS."""
    has_z = all(coord[2] not in [None, ""] for coord in coordinates)
    len_coordinates_value =2
    if is_line and len(coordinates) != len_coordinates_value:
        msg = "LineString requires exactly 2 points"
        raise ValueError(msg)

    try:
        if has_z:
            if is_line:
                coords = [
                    [
                        parse_float(c[1], "y"),
                        parse_float(c[0], "x"),
                        parse_float(c[2], "z"),
                    ]
                    for c in coordinates
                ]
                geometry = LineString(type="LineString", coordinates=coords)
            else:
                x, y, z = parse_coordinates(coordinates[0])
                geometry = Point(type="Point", coordinates=[y, x, z])
            crs = Crs(properties=CrsProperties(name="EPSG:5972"))
        else:
            if is_line:
                coords = [
                    [parse_float(c[1], "y"), parse_float(c[0], "x")]
                    for c in coordinates
                ]
                geometry = LineString(type="LineString", coordinates=coords)
            else:
                x, y = parse_coordinates(coordinates[0][:2])
                geometry = Point(type="Point", coordinates=[y, x])
            crs = Crs(properties=CrsProperties(name="EPSG:25832"))
    except ValueError as e:
        msg = f"Invalid coordinate values: {e}"
        raise ValueError(msg) from e

    return geometry, crs

def convert_overhead_structure_rows(row: dict[str, str]) -> tuple[Feature, Crs]:
    """Convert overhead structure (mast) rows to NrlMast feature."""
    komponentident = get_uuid(row, "OverheadStructure_uuid", "ID")
    masttype = map_mast_type(row.get("Masttype (NRL)"))
    feature_status = map_feature_status(row.get("Status (NRL)"))
    nøyaktighet = map_location_method(row.get("Verifisert nøyaktighet (NRL)"))

    lyssetting = map_lighting_kind(row.get("Luftfartshinderlyssetting(NRL)"))
    merking = map_marking_kind(row.get("Luftfartshindermerking (NRL)"))

    høydereferanse = None
    if row.get("Hoydereferanse (NRL)"):
        høydereferanse = (
            Høydereferanse.topp
            if row["Hoydereferanse (NRL)"].lower() == "topp"
            else Høydereferanse.fot
            if row["Hoydereferanse (NRL)"].lower() == "fot"
            else None
        )

    max_height = (
        parse_float(row["Vertikalavstand meter (NRL)"], "Vertikalavstand")
        if row.get("Vertikalavstand meter (NRL)")
        else None
    )

    point, crs = create_geometry(
        [[row["x"], row["y"], row.get("z", "")]], is_line=False
    )

    return Feature(
        geometry=point,
        properties=NrlMast(
            komponentident=komponentident,
            status=feature_status,
            verifisert_rapporteringsnøyaktighet=nøyaktighet,
            feature_type="NrlMast",
            mast_type=masttype,
            luftfartshinderlyssetting=lyssetting if lyssetting is not None else None,
            luftfartshindermerking=merking if merking is not None else None,
            høydereferanse=høydereferanse if høydereferanse is not None else None,
            vertikal_avstand=max_height if max_height is not None else None,
        ),
    ), crs


def convert_guy_segments_rows(row: dict[str, str]) -> tuple[Feature, Crs]:
    """Convert guy wire segments to NrlLuftspenn feature."""
    komponentident = get_uuid(row, "Guy_uuid", "ID")
    feature_status = map_feature_status(row.get("Status (NRL)"))
    nøyaktighet = map_location_method(row.get("Vertikalavstand meter (NRL)"))

    linestring, crs = create_geometry(
        [
            [row["x1"], row["y1"], row.get("z1", "")],
            [row["x2"], row["y2"], row.get("z2", "")],
        ]
    )

    komponentreferanse = (
        KomponentReferanse(komponentkodeverdi=row.get("ID", ""))
        if row.get("ID")
        else None
    )

    return Feature(
        geometry=linestring,
        properties=NrlLuftspenn(
            luftspenn_type=LuftspennType.bardun,
            komponentident=komponentident,
            status=feature_status,
            verifisert_rapporteringsnøyaktighet=nøyaktighet,
            feature_type="NrlLuftspenn",
            referanse=komponentreferanse,
        ),
    ), crs


def convert_ac_linesegments_rows(row: dict[str, str]) -> tuple[Feature, Crs]:
    """Convert AC line segments to NrlLuftspenn feature."""
    komponentident = get_uuid(row, "ACLineSegmentSpan_uuid", "ID")
    feature_status = map_feature_status(row.get("Status (NRL)"))
    luftspennstype: LuftspennType = map_luftspenn_type(
        row.get("Luftspenntype (NRL)")
    )

    nøyaktighet: Literal["20230101_5-1","0"] = map_location_method(
            row.get("Verifisert nøyaktighet (NRL)"
        )
    )

    lyssetting: LuftfartsHinderLyssetting | None = map_lighting_kind(
        "Luftfartshinderlyssetting(NRL)"
    )
    merking: LuftfartsHinderMerking | None = map_marking_kind(
        "Luftfartshindermerking(NRL)"
    )

    linestring, crs = create_geometry(
        [
            [row["x1"], row["y1"], row.get("z1", "")],
            [row["x2"], row["y2"], row.get("z2", "")],
        ]
    )

    mast = [
        uuid.UUID(row[f"Mast_{i}_ObjectID"])
        for i in [1, 2]
        if row.get(f"Mast_{i}_ObjectID")
    ]

    komponentreferanse = (
        KomponentReferanse(komponentkodeverdi=row.get("ID", ""))
        if row.get("ID")
        else None
    )
    anleggsbredde = (
        parse_float(row["Anleggsbredde meter (NRL)"], "Anleggsbredde")
        if row.get("Anleggsbredde meter (NRL)")
        else None
    )

    return Feature(
        geometry=linestring,
        properties=NrlLuftspenn(
            luftspenn_type=luftspennstype,
            komponentident=komponentident,
            nrl_mast=mast,
            status=feature_status,
            verifisert_rapporteringsnøyaktighet=nøyaktighet,
            feature_type="NrlLuftspenn",
            referanse=komponentreferanse,
            luftfartshinderlyssetting=lyssetting if lyssetting is not None else None,
            luftfartshindermerking=merking if merking is not None else None,
            anleggsbredde=anleggsbredde if anleggsbredde is not None else None,
        ),
    ), crs
