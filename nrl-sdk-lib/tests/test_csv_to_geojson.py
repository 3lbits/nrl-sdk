"""Tests for csv_to_geojson converter."""
import csv
import io
import os
import sys
import tempfile
import uuid
from pathlib import Path
from unittest.mock import patch

import pytest

from nrl_sdk_lib.converters.csv_to_geojson import (
    create_geometry,
    csv_to_geojson,
    get_uuid,
    map_feature_status,
    map_lighting_kind,
    map_location_method,
    parse_float,
)
from nrl_sdk_lib.models import FeatureCollection, Høydereferanse  # noqa:PLC2403


@pytest.mark.anyio
def test_csv_to_geojson_1_mast() -> None:
    """Should create a valid geojson file from csv with 1 mast."""
    input_csv = "tests/files/1_mast.csv"

    actual_content = csv_to_geojson(input_csv)

    assert len(actual_content) == 1
    assert isinstance(actual_content[0], FeatureCollection)
    assert actual_content[0].crs.properties.name == "EPSG:25832"
    assert actual_content[0].features[0].geometry.coordinates == pytest.approx(
        [585243.7955, 6544773.145]
        , rel=1e-6)
    assert actual_content[0].features[0].geometry.type == "Point"
    assert actual_content[0].features[0].properties.feature_type == "NrlMast"
    assert (actual_content[0]
            .features[0]
            .properties
            .høydereferanse
            ) == Høydereferanse.topp
    assert (actual_content[0]
            .features[0]
            .properties
            .komponentident
            ) == uuid.UUID("fa1bf202-345c-49f0-831b-5d5a12103612")
    assert hasattr(actual_content[0].features[0].properties, "mast_type")
    assert actual_content[0].features[0].properties.mast_type == "lavspentmast"
    assert actual_content[0].features[0].properties.status == "planlagtOppført"
    assert actual_content[0].features[0].properties.navn == "LM83700"
    assert hasattr(actual_content[0]
            .features[0]
            .properties
            .referanse, "komponentkodeverdi")
    assert (actual_content[0]
            .features[0]
            .properties
            .referanse.komponentkodeverdi
            ) == "fa1bf202-345c-49f0-831b-5d5a12103612"
    assert (actual_content[0]
            .features[0]
            .properties
            .verifisert_rapporteringsnøyaktighet) == "0"


@pytest.mark.anyio
def test_csv_to_geojson_1_luftspenn() -> None:
    """Should create a valid geojson file from csv with 1 luftspenn."""
    input_csv = "tests/files/1_luftspenn.csv"

    actual_content = csv_to_geojson(input_csv)

    assert len(actual_content) == 1
    assert isinstance(actual_content[0], FeatureCollection)
    assert actual_content[0].crs.properties.name == "EPSG:25832"
    assert actual_content[0].features[0].geometry.coordinates[0] == pytest.approx(
        [582430.5569299466,6544040.344467209]
        , rel=1e-4
    )
    assert actual_content[0].features[0].geometry.coordinates[1] == pytest.approx(
        [582087.7992964027,6544042.579778018]
        , rel=1e-4
    )
    assert actual_content[0].features[0].geometry.type == "LineString"
    assert actual_content[0].features[0].properties.feature_type == "NrlLuftspenn"
    assert (actual_content[0]
            .features[0]
            .properties
            .komponentident
            ) == uuid.UUID("d6716fda-aac4-4229-9e2d-690a32dc5214")
    assert hasattr(actual_content[0].features[0].properties, "luftspenn_type")
    assert actual_content[0].features[0].properties.luftspenn_type == "lavspent"
    assert actual_content[0].features[0].properties.status == "planlagtOppført"
    assert hasattr(
        actual_content[0].features[0].properties.referanse,
        "komponentkodeverdi"
    )
    assert (actual_content[0]
            .features[0]
            .properties
            .referanse
            .komponentkodeverdi
            ) == "d6716fda-aac4-4229-9e2d-690a32dc5214"
    assert actual_content[0].features[0].properties.navn == "Luftnett"
    assert (actual_content[0]
            .features[0]
            .properties
            .verifisert_rapporteringsnøyaktighet
            ) == "0"


@pytest.mark.anyio
def test_csv_to_geojson_1_bardun() -> None:
    """Should create a valid geojson file from csv with 1 bardun."""
    input_csv = "tests/files/1_bardun.csv"

    actual_content = csv_to_geojson(input_csv)

    assert len(actual_content) == 1
    assert isinstance(actual_content[0], FeatureCollection)
    assert actual_content[0].crs.properties.name == "EPSG:5972"
    assert actual_content[0].features[0].geometry.coordinates[0] == pytest.approx(
        [559404.7227,6539567.9961,0.0]
        ,rel=1e-4
    )
    assert actual_content[0].features[0].geometry.coordinates[1] == pytest.approx(
        [559419.7617,6539579.2813,0.0]
        , rel=1e-4
    )
    assert actual_content[0].features[0].geometry.type == "LineString"
    assert actual_content[0].features[0].properties.feature_type == "NrlLuftspenn"
    assert hasattr(actual_content[0].features[0].properties, "luftspenn_type")
    assert actual_content[0].features[0].properties.luftspenn_type == "bardun"
    assert actual_content[0].features[0].properties.status == "eksisterende"
    assert hasattr(
        actual_content[0].features[0].properties.referanse,
        "komponentkodeverdi"
    )
    assert (actual_content[0]
            .features[0]
            .properties
            .komponentident) == uuid.UUID(
        "0291c89b-8294-4c5c-9061-445149e68330"
    )
    assert (actual_content[0]
            .features[0]
            .properties
            .referanse.komponentkodeverdi) == "188488519"
    assert actual_content[0].features[0].properties.navn == "Bardunline"
    assert (actual_content[0]
            .features[0]
            .properties
            .verifisert_rapporteringsnøyaktighet) == "0"


def test_csv_to_geojson_file_object() -> None:
    """Should read from file-like object."""
    gen_uuid = uuid.uuid4()
    csv_content = ("Tabell ID;"
                   "x;"
                   "y;"
                   "z;"
                   "OverheadStructure_uuid;"
                   "Masttype (NRL);"
                   "Status (NRL)\n"
                   f"109;100;200;10;{gen_uuid};Mast, lavspent;Eksisterende\n")
    file_obj = io.StringIO(csv_content)
    result = csv_to_geojson(file_obj)
    assert len(result) > 0
    assert result[0].features[0].properties.feature_type == "NrlMast"

def test_csv_to_geojson_reads_from_stdin() -> None:
    """Should read from stdin if no filename is given."""
    gen_uuid = uuid.uuid4()
    csv_content = ("Tabell ID;"
                   "x;"
                   "y;"
                   "z;"
                   "OverheadStructure_uuid;"
                   "Masttype (NRL);"
                   "Status (NRL)\n"
                   f"109;100;200;10;{gen_uuid};Mast, lavspent;Eksisterende\n")
    fake_stdin = io.StringIO(csv_content)
    with patch.object(sys, "stdin", fake_stdin):
        result = csv_to_geojson(None)
        assert len(result) > 0
        assert result[0].features[0].properties.feature_type == "NrlMast"

def test_get_uuid_valid() -> None:
    """Test UUID extraction with valid UUID."""
    row = {"field1": "550e8400-e29b-41d4-a716-446655440000", "field2": "other"}
    result = get_uuid(row, "field1", "field2")
    assert str(result) == "550e8400-e29b-41d4-a716-446655440000"


def test_get_uuid_fallback() -> None:
    """Test UUID extraction with fallback field."""
    row = {"field1": "invalid", "field2": "550e8400-e29b-41d4-a716-446655440000"}
    result = get_uuid(row, "field1", "field2")
    assert str(result) == "550e8400-e29b-41d4-a716-446655440000"


def test_get_uuid_missing() -> None:
    """Test UUID extraction when no valid UUID exists."""
    row = {"field1": "invalid", "field2": "also-invalid"}
    with pytest.raises(ValueError, match="No valid UUID found"):
        get_uuid(row, "field1", "field2")


def test_parse_float_valid() -> None:
    """Test parsing valid float."""
    assert parse_float("123.45", "test_field") == 123.45


def test_parse_float_comma_decimal() -> None:
    """Test parsing float with comma as decimal separator."""
    assert parse_float("123,45", "test_field") == 123.45


def test_parse_float_invalid() -> None:
    """Test parsing invalid float."""
    with pytest.raises(ValueError, match="not a valid number"):
        parse_float("not_a_number", "test_field")


def test_create_geometry_line_with_z() -> None:
    """Test creating LineString with z coordinates."""
    coords = [["100", "200", "10"], ["300", "400", "20"]]
    geometry, crs = create_geometry(coords, is_line=True)

    assert geometry.type == "LineString"
    assert isinstance(geometry.coordinates[0], list)
    assert len(geometry.coordinates) == 2
    assert len(geometry.coordinates[0]) == 3  # Has z
    assert crs.properties.name == "EPSG:5972"


def test_create_geometry_line_without_z() -> None:
    """Test creating LineString without z coordinates."""
    coords = [["100", "200", ""], ["300", "400", ""]]
    geometry, crs = create_geometry(coords, is_line=True)

    assert geometry.type == "LineString"
    assert isinstance(geometry.coordinates[0], list)
    assert len(geometry.coordinates) == 2
    assert len(geometry.coordinates[0]) == 2  # No z
    assert crs.properties.name == "EPSG:25832"


def test_create_geometry_point_with_z() -> None:
    """Test creating Point with z coordinate."""
    coords = [["100", "200", "10"]]
    geometry, crs = create_geometry(coords, is_line=False)

    assert geometry.type == "Point"
    assert len(geometry.coordinates) == 3  # Has z
    assert crs.properties.name == "EPSG:5972"


def test_create_geometry_point_without_z() -> None:
    """Test creating Point without z coordinate."""
    coords = [["100", "200", ""]]
    geometry, crs = create_geometry(coords, is_line=False)

    assert geometry.type == "Point"
    assert len(geometry.coordinates) == 2  # No z
    assert crs.properties.name == "EPSG:25832"


def test_create_geometry_invalid_coords() -> None:
    """Test creating geometry with invalid coordinates."""
    coords = [["not", "numbers", "10"], ["300", "400", "20"]]
    with pytest.raises(ValueError, match="Invalid coordinate values"):
        create_geometry(coords, is_line=True)


def test_map_feature_status_valid() -> None:
    """Test mapping valid value."""
    result = map_feature_status("Eksisterende")
    assert result is not None

def test_map_feature_status_missing() -> None:
    """Test mapping with missing value."""
    with pytest.raises(ValueError, match="Unknown Status"):
        map_feature_status("")

def test_map_feature_status_unknown() -> None:
    """Test mapping with unknown value."""
    with pytest.raises(ValueError, match="Unknown Status"):
        map_feature_status("InvalidStatus")

def test_map_lighting_kind_allow_none() -> None:
    """Test mapping with allow_none (returns None for empty value)."""
    result = map_lighting_kind("")
    assert result is None

def test_map_location_kind() -> None:
    """Test both location kinds."""
    result = map_location_method("FOR-2020-10-16-2068, §5(1)")
    assert result == "20230101_5-1"
    result = map_location_method("Some other value")
    assert result == "0"

def create_test_csv(content: list[dict], filename: str | None) -> str | None:
    """Create a temporary CSV file."""
    if filename is None:
        fd, filename = tempfile.mkstemp(suffix=".csv")
        os.close(fd)

    with Path(filename).open("w", newline="", encoding="utf-8-sig") as f:
        if content:
            writer = csv.DictWriter(f, fieldnames=content[0].keys(), delimiter=";")
            writer.writeheader()
            writer.writerows(content)

    return filename


def test_csv_invalid_mast_type() -> None:
    """Test handling invalid mast type."""
    content = [
        {
            "Tabell ID": "109",
            "OverheadStructure_uuid": "550e8400-e29b-41d4-a716-446655440000",
            "Masttype (NRL)": "InvalidType",
            "Status (NRL)": "Eksisterende",
            "x": "100",
            "y": "200",
            "z": "10",
        }
    ]

    filename = create_test_csv(content, filename=None)

    with pytest.raises(ValueError, match="Unknown Masttype"):
        csv_to_geojson(filename)


def test_csv_missing_status() -> None:
    """Test handling missing status field."""
    content = [
        {
            "Tabell ID": "109",
            "OverheadStructure_uuid": "550e8400-e29b-41d4-a716-446655440000",
            "Masttype (NRL)": "Mast, høyspent",
            "Status (NRL)": "",
            "x": "100",
            "y": "200",
            "z": "10",
        }
    ]

    filename = create_test_csv(content, filename=None)

    with pytest.raises(ValueError, match="Unknown Status:"):
        csv_to_geojson(filename)

def test_no_tabell_id() -> None:
    """Test handling missing Tabell ID."""
    content = [
        {
            "OverheadStructure_uuid": "550e8400-e29b-41d4-a716-446655440000",
            "Masttype (NRL)": "Mast, høyspent",
            "Status (NRL)": "Eksisterende",
            "x": "100",
            "y": "200",
            "z": "10",
        }
    ]

    filename = create_test_csv(content, filename=None)

    with pytest.raises(ValueError, match="Unknown Tabell ID:"):
        csv_to_geojson(filename)

def test_parse_float_none_value() -> None:
    """Test parsing None value."""
    with pytest.raises(ValueError, match="Missing test_field"):
        parse_float(None, "test_field")

def test_create_geometry_line_invalid_number_of_points() -> None:
    """Test creating LineString with invalid number of points."""
    coords = [["100", "200", "10"]]
    with pytest.raises(ValueError, match="LineString requires exactly 2 points"):
        create_geometry(coords, is_line=True)

def test_csv_optional_lighting_and_marking() -> None:
    """Test handling optional lighting and marking fields."""
    content = [
        {
            "Tabell ID": "109",
            "OverheadStructure_uuid": "550e8400-e29b-41d4-a716-446655440000",
            "Masttype (NRL)": "Mast, høyspent",
            "Status (NRL)": "Eksisterende",
            "Luftfartshinderlyssetting(NRL)": "Lyssatt",
            "Luftfartshindermerking (NRL)": "Fargemerking",
            "x": "100",
            "y": "200",
            "z": "10",
        }
    ]

    filename = create_test_csv(content, filename=None)
    result = csv_to_geojson(filename)

    assert len(result) > 0
    feature = result[0].features[0]
    assert feature.properties.luftfartshinderlyssetting is not None
    assert feature.properties.luftfartshindermerking is not None


def test_csv_guy_segment_missing_uuid() -> None:
    """Test guy segment with missing UUID."""
    content = [
        {
            "Tabell ID": "261",
            "Betegnelse": "Bardunline",
            "Guy_uuid": "",
            "Status (NRL)": "Eksisterende",
            "x1": "100",
            "y1": "200",
            "z1": "10",
            "x2": "300",
            "y2": "400",
            "z2": "20",
        }
    ]

    filename = create_test_csv(content, filename=None)

    with pytest.raises(ValueError, match="No valid UUID found"):
        csv_to_geojson(filename)


def test_csv_luftspenn_invalid_type() -> None:
    """Test luftspenn with invalid type."""
    content = [
        {
            "Tabell ID": "261",
            "Betegnelse": "Ledning",
            "ACLineSegmentSpan_uuid": "550e8400-e29b-41d4-a716-446655440000",
            "Status (NRL)": "Eksisterende",
            "Luftspenntype (NRL)": "InvalidType",
            "x1": "100",
            "y1": "200",
            "z1": "10",
            "x2": "300",
            "y2": "400",
            "z2": "20",
        }
    ]

    filename = create_test_csv(content, filename=None)

    with pytest.raises(ValueError, match="Unknown Luftspenntype"):
        csv_to_geojson(filename)


def test_csv_multiple_crs() -> None:
    """Test CSV with features in different CRS."""
    content = [
        {
            "Tabell ID": "109",
            "OverheadStructure_uuid": "550e8400-e29b-41d4-a716-446655440000",
            "Masttype (NRL)": "Mast, høyspent",
            "Status (NRL)": "Eksisterende",
            "x": "100",
            "y": "200",
            "z": "10",
        },
        {
            "Tabell ID": "109",
            "OverheadStructure_uuid": "550e8400-e29b-41d4-a716-446655440001",
            "Masttype (NRL)": "Mast, høyspent",
            "Status (NRL)": "Eksisterende",
            "x": "100",
            "y": "200",
            "z": "",  # No z = different CRS
        },
    ]

    filename = create_test_csv(content, filename=None)
    result = csv_to_geojson(filename)

    # Should create 2 FeatureCollections (one per CRS)
    assert len(result) == 2


def test_csv_with_anleggsbredde() -> None:
    """Test luftspenn with anleggsbredde field."""
    content = [
        {
            "Tabell ID": "261",
            "Betegnelse": "Ledning",
            "ACLineSegmentSpan_uuid": "550e8400-e29b-41d4-a716-446655440000",
            "Status (NRL)": "Eksisterende",
            "Luftspenntype (NRL)": "Ledning, høyspent",
            "Anleggsbredde meter (NRL)": "5.5",
            "x1": "100",
            "y1": "200",
            "z1": "10",
            "x2": "300",
            "y2": "400",
            "z2": "20",
        }
    ]

    filename = create_test_csv(content, filename=None)
    result = csv_to_geojson(filename)

    assert len(result) > 0
    feature = result[0].features[0]

    assert hasattr(feature.properties, "anleggsbredde")
    assert feature.properties.anleggsbredde == 5.5
