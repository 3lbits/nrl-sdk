"""Generate GeoJSON file with test data in NRL v2 format."""

from pathlib import Path

import anyio
from nrl_sdk_lib.models import (
    Crs,
    CrsProperties,
    Feature,
    FeatureCollection,
    KomponentReferanse,
    LineString,
    NrlLuftspenn,
    NrlMast,
    Point,
)


async def generate_geojson_v2(data: dict, filename: str) -> None:
    """Generate GeoJSON file with test data.

    Args:
        data (dict): Data structure with mast points and trase lines
        filename (str): Output GeoJSON filename

    """
    # Determine CRS based on the region zone used
    utm_zone = data.get("utm_zone", 32)  # Default to zone 32
    if utm_zone == 32:
        epsg_code = "EPSG:25832"
    elif utm_zone == 33:
        epsg_code = "EPSG:25833"
    else:
        epsg_code = "EPSG:25832"  # Default to zone 32

    # Create GeoJSON structure
    crs: Crs = Crs(type="name", properties=CrsProperties(name=epsg_code))
    geojson: FeatureCollection = FeatureCollection(
        type="FeatureCollection",
        crs=crs,
        features=[],
    )

    # Add line features (Trase Elements)
    for line in data["trase_lines"]:
        # Make sure coordinates are 2D only (no height)
        coordinates = [line["coordinates"][0], line["coordinates"][1]]

        line_string: LineString = LineString(type="LineString", coordinates=coordinates)

        nrl_luftspenn: NrlLuftspenn = NrlLuftspenn(
            feature_type="NrlLuftspenn",
            status=line["status"],
            komponentident=line["id"],
            verifisert_rapporteringsnøyaktighet="20230101_5-1",  # Set to verified
            referanse=KomponentReferanse(komponentkodeverdi=line["komponentident"]),
            luftspenn_type=line["luftspennType"],
        )

        line_feature: Feature = Feature(
            type="Feature", geometry=line_string, properties=nrl_luftspenn
        )

        geojson.features.append(line_feature)

    # Add point features (Masts)
    for point in data["mast_points"]:
        coordinates = point["coordinates"]

        nrl_point: Point = Point(type="Point", coordinates=coordinates)

        nrl_mast: NrlMast = NrlMast(
            feature_type="NrlMast",
            status=point["status"],
            komponentident=point["id"],
            verifisert_rapporteringsnøyaktighet="20230101_5-1",
            referanse=KomponentReferanse(komponentkodeverdi=point["komponentident"]),
            mast_type=point["mastType"],
        )
        point_feature: Feature = Feature(
            type="Feature", geometry=nrl_point, properties=nrl_mast
        )
        geojson.features.append(point_feature)

    # Write to file
    file_path = Path(filename)
    async with await anyio.open_file(file_path, "w", encoding="utf-8") as f:
        await f.write(await geojson.serialize())
