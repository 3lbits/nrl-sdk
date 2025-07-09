"""Test module for feature collection model."""

from uuid import UUID

import pytest
from anyio import open_file
from pydantic import ValidationError

from nrl_sdk_lib.models.feature_collection import (
    FeatureCollection,
    Hoydereferanse,
    KomponentReferanse,
    Kvalitet,
    LineString,
    LuftfartsHinderMerking,
    LuftspennType,
    Materiale,
    NrlFlate,
    NrlLuftspenn,
    Polygon,
)


@pytest.fixture
def anyio_backend() -> str:
    """Use the asyncio backend for the anyio fixture."""
    return "asyncio"


@pytest.mark.anyio
async def test_feature_collection_model() -> None:
    """Example file should deserialize to a FeatureCollection model."""
    testfile_path = "tests/files/Eksempelfil_NRLRapportering-1.0.1.json"
    # Open the file asynchronously
    async with await open_file(testfile_path, mode="r") as f:
        # Read the entire contents
        feature_collection_json = await f.read()
        # Deserialize the JSON string to a FeatureCollection model
        try:
            feature_collection = FeatureCollection.model_validate_json(
                feature_collection_json
            )
        except ValidationError as e:
            pytest.fail(f"Deserialization failed with errors: {e.errors()}")

        # Assert that the deserialized object is an instance of FeatureCollection
        assert isinstance(feature_collection, FeatureCollection)
        # Assert that the type is 'FeatureCollection'
        assert feature_collection.type == "FeatureCollection"
        # Assert that the CRS type is 'name'
        assert feature_collection.crs.type == "name"
        # Assert that the CRS properties name is 'EPSG:5973'
        assert feature_collection.crs.properties.name == "EPSG:5973"
        # Assert that there are features in the collection
        assert len(feature_collection.features) > 0
        # Assert that the first feature's type is 'Feature'
        assert feature_collection.features[0].type == "Feature"
        # Assert that the first feature's geometry type is 'Polygon'
        assert feature_collection.features[0].geometry.type == "Polygon"
        # Assert that the first feature's geometry is of the correct type
        assert type(feature_collection.features[0].geometry) is Polygon
        assert feature_collection.features[0].geometry.coordinates != []
        # Assert that the first feature's geometry coordinates are of the correct type
        assert type(feature_collection.features[0].geometry.coordinates) is list
        # Assert that the first feature's geometry coordinates are a list of lists
        assert all(
            isinstance(coord, list)
            for coord in feature_collection.features[0].geometry.coordinates
        )
        # Assert that the first feature's geometry coordinates is a
        #  list of lists of lists
        assert all(
            isinstance(coord, list)
            for sublist in feature_collection.features[0].geometry.coordinates
            for coord in sublist
        )
        # Assert that the first feature's geometry coordinates are a list of lists of
        #  lists of floats
        assert all(
            isinstance(coord, float)
            for sublist in feature_collection.features[0].geometry.coordinates
            for subsublist in sublist
            for coord in subsublist
        )
        # Assert that the first feature's properties feature_type is 'NRLFlate'
        assert feature_collection.features[0].properties.feature_type == "NrlFlate"
        # Assert that the first feature's properties is of the correct type
        assert type(feature_collection.features[0].properties) is NrlFlate
        # Assert that the first feature's properties komponentident is a UUID
        assert isinstance(
            feature_collection.features[0].properties.komponentident, UUID
        )
        # Assert that the first feature's properties status is 'planlagtFjernet'
        assert feature_collection.features[0].properties.status == "planlagtFjernet"
        # Assert that the first feature's properties luftfartshindermerking is
        #  'fargemerking'
        assert (
            feature_collection.features[0].properties.luftfartshindermerking
            == "fargemerking"
        )
        # Assert that the flate_type is 'NRLFlate'
        assert feature_collection.features[0].properties.flate_type == "kontaktledning"


@pytest.mark.anyio
async def test_feature_collection_model_luftspenn() -> None:  # noqa: PLR0915
    """Example file should deserialize to a FeatureCollection model."""
    testfile_path = "tests/files/Eksempelfil_NRLRapportering-1.0.1_1_luftspenn.json"
    # Open the file asynchronously
    async with await open_file(testfile_path, mode="r") as f:
        # Read the entire contents
        feature_collection_json = await f.read()
        # Deserialize the JSON string to a FeatureCollection model
        try:
            feature_collection = FeatureCollection.model_validate_json(
                feature_collection_json
            )
        except ValidationError as e:
            pytest.fail(f"Deserialization failed with errors: {e.errors()}")

        # Assert that the deserialized object is an instance of FeatureCollection
        assert isinstance(feature_collection, FeatureCollection)
        # Assert that the type is 'FeatureCollection'
        assert feature_collection.type == "FeatureCollection"

        # crs:
        # Assert that the CRS type is 'name'
        assert feature_collection.crs.type == "name"
        # Assert that the CRS properties name is 'EPSG:5973'
        assert feature_collection.crs.properties.name == "EPSG:5973"

        # features:
        # Assert that there are features in the collection
        assert len(feature_collection.features) == 1
        # type:
        # Assert that the first feature's type is 'Feature'
        assert feature_collection.features[0].type == "Feature"

        # geometry:
        # Assert that the first feature's geometry type is 'Polygon'
        assert feature_collection.features[0].geometry.type == "LineString"
        # Assert that the first feature's geometry is of the correct type
        assert type(feature_collection.features[0].geometry) is LineString
        assert feature_collection.features[0].geometry.coordinates != []
        # Assert that the first feature's geometry coordinates are of the correct type
        assert type(feature_collection.features[0].geometry.coordinates) is list
        # Assert that the first feature's geometry coordinates are a list of lists
        assert all(
            isinstance(coord, list)
            for coord in feature_collection.features[0].geometry.coordinates
        )
        # Assert that the first feature's geometry coordinates is
        #  a list of lists of lists of floats
        assert all(
            isinstance(coord, float)
            for sublist in feature_collection.features[0].geometry.coordinates
            for subsublist in sublist
            for coord in sublist
        )

        # general properties:
        # Assert that the first feature's properties feature_type is 'NRLFlate'
        assert feature_collection.features[0].properties.feature_type == "NrlLuftspenn"
        # Assert that the first feature's properties is of the correct type
        assert type(feature_collection.features[0].properties) is NrlLuftspenn
        # Assert that the first feature's properties status is 'eksisterende'
        assert feature_collection.features[0].properties.status == "eksisterende"
        # Assert that the first feature's properties komponentident is a UUID
        assert isinstance(
            feature_collection.features[0].properties.komponentident, UUID
        )
        # Assert that the verifisert_rapporteringsnøyaktighet is "20230101_5-1":
        assert (
            feature_collection.features[
                0
            ].properties.verifisert_rapporteringsnøyaktighet
            == "20230101_5-1"
        )
        # Assert that the referanse is of type KomponentReferanse:
        assert (
            type(feature_collection.features[0].properties.referanse)
            is KomponentReferanse
        )
        # Assert that the kodesystemversjon of referanse is "1.0.0":
        assert (
            feature_collection.features[0].properties.referanse.kodesystemversjon
            == "1234"
        )
        # Assert that the komponentkodesystem of referanse is "NIS":
        assert (
            feature_collection.features[0].properties.referanse.komponentkodesystem
            == "NIS"
        )
        # Assert that the komponentkodeverdi of referanse is "88884444":
        assert (
            feature_collection.features[0].properties.referanse.komponentkodeverdi
            == "88884444"
        )
        # Assert that the first feature's properties navn is 'Høgspent fra A til B':
        assert feature_collection.features[0].properties.navn == "Høgspent fra A til B"
        # Assert that the first feature's properties vertikal_avstand is 73:
        assert feature_collection.features[0].properties.vertikal_avstand == 73
        # Assert that the type of luftfartshindermerking is LuftfartsHinderMerking:
        assert (
            type(feature_collection.features[0].properties.luftfartshindermerking)
            is LuftfartsHinderMerking
        )
        # Assert that the first feature's properties luftfartshindermerking is 'markør'
        assert (
            feature_collection.features[0].properties.luftfartshindermerking
            == LuftfartsHinderMerking.markor
        )
        # Assert that the type of materiale is Materiale:
        assert type(feature_collection.features[0].properties.materiale) is Materiale
        # Assert that the materiale is "metall":
        assert feature_collection.features[0].properties.materiale == Materiale.metall
        # Assert that the datafangstdato is "1990-06-29":
        assert feature_collection.features[0].properties.datafangstdato == "1990-06-29"
        # Assert that the kvalitet is of type Kvalitet:
        assert type(feature_collection.features[0].properties.kvalitet) is Kvalitet
        # Assert that the datafangstmetode of kvalitet is "sat":
        assert (
            feature_collection.features[0].properties.kvalitet.datafangstmetode == "sat"
        )
        # Assert that the nøyaktighet of kvalitet is 50:
        assert feature_collection.features[0].properties.kvalitet.nøyaktighet == 50
        # Assert that the datafangstmetodeHøyde of kvalitet is "sat":
        assert (
            feature_collection.features[0].properties.kvalitet.datafangstmetode_høyde
            == "sat"
        )
        # Assert that the nøyaktighet_høyde of kvalitet is 50:
        assert (
            feature_collection.features[0].properties.kvalitet.nøyaktighet_høyde == 50
        )
        # Assert that the verifisert_rapporteringsnøyaktighet is "20230101_5-1":
        assert (
            feature_collection.features[
                0
            ].properties.verifisert_rapporteringsnøyaktighet
            == "20230101_5-1"
        )
        # Assert that the høydereferanse is "topp":
        assert feature_collection.features[0].properties.høydereferanse == "topp"
        # Assert that the informasjon contains "Dette er en test":
        assert feature_collection.features[0].properties.informasjon is not None
        assert (
            "Dette er en test" in feature_collection.features[0].properties.informasjon
        )
        # Assert that høydereferanse is of type Hoydereferanse:
        assert (
            type(feature_collection.features[0].properties.høydereferanse)
            is Hoydereferanse
        )
        # Assert that the høydereferanse is "topp":
        assert (
            feature_collection.features[0].properties.høydereferanse
            == Hoydereferanse.topp
        )

        # specific properties:
        # Assert that the luftspenn_type is of type LuftspennType:
        assert (
            type(feature_collection.features[0].properties.luftspenn_type)
            is LuftspennType
        )
        # Assert that the luftspenn_type is "høgspent":
        assert (
            feature_collection.features[0].properties.luftspenn_type
            == LuftspennType.hogspent
        )
        # Assert that the anleggsbredde is 22:
        assert feature_collection.features[0].properties.anleggsbredde == 22
        # Assert that the friseilingshøyde is 45.3:
        assert feature_collection.features[0].properties.friseilingshøyde == 45.3
        # Assert that the nrl_mast is a list:
        assert isinstance(feature_collection.features[0].properties.nrl_mast, list)
        # Assert that the nrl_mast list has 2 items:
        assert len(feature_collection.features[0].properties.nrl_mast) == 2
        # Assert that the first item in nrl_mast is of type UUID:
        assert isinstance(feature_collection.features[0].properties.nrl_mast[0], UUID)
        # Assert that the second item in nrl_mast is of type UUID:
        assert isinstance(feature_collection.features[0].properties.nrl_mast[1], UUID)
