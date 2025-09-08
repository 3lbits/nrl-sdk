"""NRL test data generation functionality."""

import json
import math
import random
import re
import uuid
from datetime import UTC, datetime
from pathlib import Path

import xlsxwriter


def generate_files(  # noqa: PLR0913
    num_elements: int = 2,
    output_prefix: str = "testdata",
    status: str = "planlagtOppført",
    region: str | None = None,
    error_positions: list[int] | None = None,
    error_freq: float | None = None,
    *,
    include_errors: bool = False,
) -> dict:
    """Generate test data files for NRL.

    Args:
        num_elements (int): Number of elements to generate for each type
        output_prefix (str): Prefix for output filenames
        status (str): Status value for the elements
        region (str): Region to generate data in (None for random)
        include_errors (bool): Include error regions in random selection
        error_positions (list): List of positions (1-based) where
            errors should be injected
        error_freq (float): Frequency of error injection (0.0-1.0)

    Returns:
        dict: Information about the generated files

    """
    # Generate random test data
    common_data = generate_random_data(
        num_elements,
        status=status,
        region=region,
        include_errors=include_errors,
        error_positions=error_positions,
        error_freq=error_freq,
    )
    output_type = f"{num_elements * 2}_elements"

    # Add timestamp for unique filenames
    timestamp = datetime.now(tz=UTC).strftime("%Y%m%d_%H%M%S")

    # Define output filenames with better naming
    # Add "_with_errors" suffix if error injection is used
    error_suffix = ""
    if error_positions or error_freq:
        error_suffix = "_with_errors"

    excel_filename = f"{output_prefix}_{output_type}{error_suffix}_{timestamp}.xlsx"
    geojson_filename = (
        f"{output_prefix}_{output_type}{error_suffix}_{timestamp}.geojson"
    )

    # Generate the Excel file
    generate_excel(common_data, excel_filename)

    # Generate the GeoJSON file
    generate_geojson(common_data, geojson_filename)

    # Generate error log file if there are errors
    error_log_file = None
    if common_data.get("error_log"):
        error_log_file = (
            f"{output_prefix}_{output_type}{error_suffix}_{timestamp}_errors.txt"
        )
        error_log_file_path = Path(error_log_file)
        with error_log_file_path.open("w") as f:
            f.writelines(
                f"{entry['position']} {entry['id']} {entry['error_type']} {entry['coordinates'][0]},{entry['coordinates'][1]} {entry['location']} {entry['zone']}\n"  # noqa: E501
                for entry in common_data["error_log"]
            )

    result = {
        "excel_file": excel_filename,
        "geojson_file": geojson_filename,
        "total_elements": len(common_data["mast_points"])
        + len(common_data["trase_lines"]),
        "status": status,
        "region_name": common_data.get("region_name", "Unknown region"),
    }

    if error_log_file:
        result["error_log_file"] = error_log_file

    return result


def generate_random_data(  # noqa: C901, PLR0912, PLR0913, PLR0915
    num_elements: int,
    status: str = "planlagtOppført",
    region: str | None = None,
    error_positions: list[int] | None = None,
    error_freq: float | None = None,
    *,
    include_errors: bool = False,
) -> dict:
    """Generate random data for NRL test files with a wider geographical area.

    Args:
        num_elements (int): Number of elements of each type to generate
        status (str): Status value for the elements
        region (str): Region to generate data in (None for random)
        include_errors (bool): Include error regions in random selection
        error_positions (list): List of positions (1-based) where errors
            should be injected
        error_freq (float): Frequency of error injection (0.0-1.0)

    Returns:
        dict: Generated data with mast points and trase lines

    """
    # Define Norwegian data elements
    norwegian_areas = [
        "Larvik",
        "Oslo",
        "Tønsberg",
        "Sandefjord",
        "Drammen",
        "Fredrikstad",
        "Moss",
        "Halden",
        "Ski",
        "Asker",
        "Bærum",
        "Lillestrøm",
        "Gjøvik",
        "Kongsberg",
        "Horten",
        "Trondheim",
        "Bergen",
        "Stavanger",
        "Tromsø",
        "Kristiansand",
        "Ålesund",
        "Bodø",
        "Haugesund",
        "Molde",
        "Hamar",
        "Lillehammer",
        "Narvik",
        "Mo i Rana",
        "Steinkjer",
        "Namsos",
    ]

    norwegian_users = [
        "MABJ2",
        "OLAR1",
        "ANNAK",
        "PERSN",
        "KARIA",
        "JENSH",
        "MARIS",
        "OLEJ2",
        "SOFIE",
        "THORH",
        "INGEB",
        "NILSB",
        "EVAO",
        "JOHNK",
        "HELGA",
        "SVENN",
    ]

    impregnering_types = ["Kreosot", "Salt", "CCA", "Kobber", "Ubehandlet"]
    fundament_types = [
        "Stolpe på fjell",
        "Stolpe i jord",
        "Fundament",
        "Betongfundament",
    ]

    # Define regions within NRL coverage area with UTM zones
    # Western and central Norway (Bergen, Stavanger, Oslo, Trondheim etc.) uses UTM zone 32 # noqa: E501
    # Eastern/northeastern Norway (near Swedish/Finnish borders) would use UTM zone 33
    # https://no.wikipedia.org/wiki/UTM-koordinater
    regions = {
        "Oslo_area": {
            "center": [598500, 6642000],  # Oslo area in UTM 32N coordinates
            "radius": 10000,  # Reduced from 15km to 10km - Oslo is close to Swedish border # noqa: E501
            "zone": 32,
        },
        "Larvik_area": {
            "center": [582000, 6554000],  # Larvik area in UTM 32N coordinates
            "radius": 10000,  # Keep at 10km - safe distance from border
            "zone": 32,
        },
        "Bergen_area": {
            "center": [297000, 6700000],  # Bergen area in UTM 32N coordinates
            "radius": 25000,  # Keep at 25km - west coast, far from Sweden
            "zone": 32,
        },
        "Stavanger_area": {
            "center": [308000, 6550000],  # Stavanger area in UTM 32N coordinates
            "radius": 20000,  # Keep at 20km - southwest, safe from Sweden
            "zone": 32,
        },
        "Kristiansand_area": {
            "center": [437000, 6450000],  # Kristiansand area in UTM 32N coordinates
            "radius": 15000,  # Keep at 15km - reasonably safe distance
            "zone": 32,
        },
        "Trondheim_area": {
            "center": [570000, 7030000],  # Trondheim area in UTM 32N coordinates
            "radius": 15000,  # Reduced from 20km to 15km - most risky due to narrow country width # noqa: E501
            "zone": 32,
        },
    }

    # Error regions - locations outside Norway for testing error handling
    error_regions = {
        "Hjorring_Denmark": {
            "center": [565000, 6340000],  # Hjørring, Denmark in UTM 32N
            "radius": 10000,
            "zone": 32,
        },
        "Gothenburg_Sweden": {
            "center": [320000, 6400000],  # Göteborg, Sweden in UTM 32N
            "radius": 15000,
            "zone": 32,
        },
    }

    # Combine all regions
    all_regions = {**regions, **error_regions}

    # Choose region based on parameter or random
    if region and region in all_regions:
        region_name = region
    # Choose from all regions or just Norwegian regions based on include_errors flag
    elif include_errors:
        region_name = random.choice(list(all_regions.keys()))
    else:
        region_name = random.choice(
            list(regions.keys())
        )  # Only choose from valid regions by default
    region_data = all_regions[region_name]

    # Generate coordinates within the selected region
    coordinates = []
    error_log = []  # Track elements with errors
    # Define Hjørring error region for error injection
    hjorring_region = error_regions["Hjorring_Denmark"]

    for i in range(num_elements):
        # Determine if this position should be an error
        is_error_position = False

        # Check if this position should have an error based on error_positions
        if (error_positions and (i + 1) in error_positions) or (
            error_freq is not None and random.random() < error_freq
        ):
            is_error_position = True

        if is_error_position:
            # Generate error coordinates around Hjørring with
            # tighter radius for inland points
            angle = random.uniform(0, 2 * math.pi)
            # Use smaller radius (5km) to ensure points are inland
            distance = random.uniform(0, 1) ** 0.5 * 5000

            x_offset = distance * math.cos(angle)
            y_offset = distance * math.sin(angle)

            x = hjorring_region["center"][0] + x_offset
            y = hjorring_region["center"][1] + y_offset

            # Track this error for logging (position is 1-based)
            error_info = {
                "position": i + 1,
                "error_type": "position",
                "coordinates": [x, y],
                "location": "Hjorring_Denmark",
                "zone": hjorring_region["zone"],
            }
            error_log.append(error_info)
        else:
            # Generate normal coordinates within the selected region
            angle = random.uniform(0, 2 * math.pi)
            # Use square root to get more uniform distribution across the circle area
            distance = random.uniform(0, 1) ** 0.5 * region_data["radius"]

            # Calculate the offset from the center
            x_offset = distance * math.cos(angle)
            y_offset = distance * math.sin(angle)

            # Get the final coordinates
            x = region_data["center"][0] + x_offset
            y = region_data["center"][1] + y_offset

        coordinates.append([x, y])

    # Create mast points from our coordinates
    mast_points = []
    error_positions_set = set()  # Track which positions are errors

    for i in range(num_elements):
        point_id = str(uuid.uuid4())

        mast_point = {
            "id": point_id,
            "coordinates": coordinates[i],  # Using only [easting, northing]
            "status": status,
            "komponentident": f"LM{80000 + random.randint(1000, 9999)}",
            "mastType": "Mast, lavspent",
        }
        mast_points.append(mast_point)

        # Update error log with actual ID if this was an error position
        for error_entry in error_log:
            if error_entry["position"] == i + 1 and "id" not in error_entry:
                error_entry["id"] = point_id
                error_positions_set.add(i)  # Track this position as an error
                break

    # Create random trase lines connecting mast points
    trase_lines = []

    # Separate mast points into valid and error groups
    valid_masts = []
    error_masts = []

    for i, mast in enumerate(mast_points):
        if i in error_positions_set:
            error_masts.append(mast)
        else:
            valid_masts.append(mast)

    # Sort both groups to make connections more logical
    valid_masts_sorted = (
        sorted(valid_masts, key=lambda x: (x["coordinates"][1], x["coordinates"][0]))
        if valid_masts
        else []
    )

    error_masts_sorted = (
        sorted(error_masts, key=lambda x: (x["coordinates"][1], x["coordinates"][0]))
        if error_masts
        else []
    )

    # Create trase lines for valid masts
    for i in range(len(valid_masts_sorted)):
        if len(valid_masts_sorted) > 1:
            if i < len(valid_masts_sorted) - 1:
                start_point = valid_masts_sorted[i]
                end_point = valid_masts_sorted[i + 1]
            else:
                # Last point connects to first point
                start_point = valid_masts_sorted[i]
                end_point = valid_masts_sorted[0]

            line_id = str(uuid.uuid4())
            trase_line = {
                "id": line_id,
                "coordinates": [start_point["coordinates"], end_point["coordinates"]],
                "status": status,
                "komponentident": f"LL{70000 + random.randint(1000, 9999)}",
                "luftspennType": "Ledning, lavspent",
            }
            trase_lines.append(trase_line)

    # Create trase lines for error masts (separate network)
    for i in range(len(error_masts_sorted)):
        if len(error_masts_sorted) > 1:
            if i < len(error_masts_sorted) - 1:
                start_point = error_masts_sorted[i]
                end_point = error_masts_sorted[i + 1]
            else:
                # Last point connects to first point
                start_point = error_masts_sorted[i]
                end_point = error_masts_sorted[0]

            line_id = str(uuid.uuid4())
            trase_line = {
                "id": line_id,
                "coordinates": [start_point["coordinates"], end_point["coordinates"]],
                "status": status,
                "komponentident": f"LL{70000 + random.randint(1000, 9999)}",
                "luftspennType": "Ledning, lavspent",
            }
            trase_lines.append(trase_line)

    # If we need more trase lines to match num_elements,
    # create self-loops or short segments
    while len(trase_lines) < num_elements:
        # Use any available mast point to create a short segment
        if mast_points:
            mast = mast_points[len(trase_lines) % len(mast_points)]
            start_coords = mast["coordinates"]
            end_coords = [start_coords[0] + 10, start_coords[1] + 10]  # 10m offset

            line_id = str(uuid.uuid4())
            trase_line = {
                "id": line_id,
                "coordinates": [start_coords, end_coords],
                "status": status,
                "komponentident": f"LL{70000 + random.randint(1000, 9999)}",
                "luftspennType": "Ledning, lavspent",
            }
            trase_lines.append(trase_line)

    # Common data structure with Norwegian elements
    common_data = {
        "mast_points": mast_points,
        "trase_lines": trase_lines,
        "norwegian_areas": norwegian_areas,
        "norwegian_users": norwegian_users,
        "impregnering_types": impregnering_types,
        "fundament_types": fundament_types,
        "region_name": region_name,  # Include the selected region name for reference
        "utm_zone": region_data["zone"],  # Include the UTM zone for CRS generation
    }

    # Add error log if there are any errors
    if error_log:
        common_data["error_log"] = error_log

    return common_data


def generate_excel(data: dict, filename: str) -> None:  # noqa: C901
    """Generate Excel file with test data.

    Args:
        data (dict): Data structure with mast points and trase lines
        filename (str): Output Excel filename

    """
    # Create a workbook and add worksheets
    workbook = xlsxwriter.Workbook(filename)
    mast_sheet = workbook.add_worksheet("Mast")
    trase_sheet = workbook.add_worksheet("Trase Element")

    # Define column headers for Mast sheet
    mast_headers = [
        "ID",
        "Tabell ID",
        "Klasse",
        "Klasse",
        "Father ID",
        "x",
        "y",
        "z",
        "Retning",
        "Tilstand",
        "Betegnelse",
        "Betegnelse x",
        "Betegnelse y",
        "LabelDirection",
        "Planbetegnelse",
        "Brukernavn",
        "Operativt område",
        "Endret",
        "Driftsstatus",
        "Arbeidets ID",
        "Statistic",
        "Datakilde",
        "Status",
        "Planlagt endring",
        "Opprinnelig plan",
        "Område",
        "Eier",
        "Systemoperatør",
        "Ekstern ID",
        "Eksternt område-ID",
        "Konstruksjon ID",
        "Teknisk type-ID",
        "Kombinert bruk",
        "Installasjonsår",
        "HSp-linje",
        "LSp-linje",
        "Totalhøyde (m)",
        "Høyde 2",
        "Stolpeklasse",
        "Synlig høyde (m)",
        "Stolpetype",
        "Impregnering",
        "Fundament-type",
        "Type 1",
        "Materiale 1",
        "Isolator 1",
        "Jordbånddiameter (mm)",
        "Kombinert bruk 1",
        "Kombinert bruk 2",
        "Kombinert bruk 3",
        "Kombinert bruk 4",
        "Kombinert bruk 5",
        "Kombinert bruk 6",
        "Merknad",
        "Masttype (NRL)",
        "Utskiftningsår travers",
        "UUIDv4",
        "Rapportering (NRL)",
        "Hoydereferanse (NRL)",
        "Luftfartshinderlyssetting(NRL)",
        "Luftfartshindermerking (NRL)",
        "Vertikalavstand meter (NRL)",
        "Verifisert nøyaktighet (NRL)",
        "Status (NRL)",
        "Aktør 4",
        "Aktør 5",
        "Aktør 6",
        "Søknads nr Aktør 4",
        "Søknads nr Aktør 5",
        "Søknads nr Aktør 6",
        "Aktør Veilys",
        "Kryssende luftspenn",
        "GPS Longitude",
        "GPS Latitude",
        "UBW-nummer",
        "Regional_Nett",
        "INVKLASSE",
        "SAMMENFØYINGITOPP",
        "Create User",
        "Create Date",
        "Søknadsnr :",
        "Søker  :",
        "Veilys mastnr :",
        "Driftsmerking :",
        "Fellesføring nr :",
        "Avgrening",
        "Hovedlinje",
        "Bardun antall (Stk)",
        "Anleggsbidrag",
        "Grunnforhold fundament",
        "IsolatorType :",
        "Bardun type",
        "Jordelektrode (Type, mm2)",
        "MMS Tekst",
        "Byggeklausulert bredde (m)",
        "Ryddeklausulert bredde (m)",
        "Horisontal faseavstand (m)",
        "Antall isolatorskåler (stk)",
        "Jordbånd dim. (cm)",
        "Samsvarserklæring",
        "Årstall venstrebein",
        "Årstall høyrebein",
        "Årstall mitrebein",
        "KILE_B",
        "Aktør 1",
        "Aktør 2",
        "Aktør 3",
        "Søknads nr Aktør 1",
        "Søknads nr Aktør 2",
        "Søknads nr Aktør 3",
        "PD: Skalltykkelse(mm)",
        "PD: Min frisk diameter(mm)",
        "PD: Min diameter(mm)",
        "Stagtvinge bardun",
        "Til plan (MMS)",
        "PD: Underdimisjonert",
        "PD: Råtten/Byttes",
        "Avgang",
        "Stasjon",
        "Id på gml. erstattet komponent",
        "Risikoindeks",
    ]

    # Define column headers for Trase Element sheet
    trase_headers = [
        "ID",
        "Tabell ID",
        "Klasse",
        "Klasse",
        "Father ID",
        "x1",
        "y1",
        "z1",
        "x2",
        "y2",
        "z2",
        "Lengde (m)",
        "Bryterens tilstand 1",
        "Bryterens tilstand 2",
        "Betegnelse",
        "Betegnelse x",
        "Betegnelse y",
        "LabelDirection",
        "Planbetegnelse",
        "Brukernavn",
        "Operativt område",
        "Endret",
        "Driftsstatus",
        "Arbeidets ID",
        "Statistic",
        "Datakilde",
        "Status",
        "Planlagt endring",
        "Opprinnelig plan",
        "Systemoperatør",
        "Ekstern ID",
        "Eksternt område-ID",
        "Konstruksjon ID",
        "Teknisk type-ID",
        "CutId",
        "Område",
        "Eier",
        "Miljø",
        "Dybde (cm)",
        "Tverrsnitt-ID",
        "Merknad",
        "Luftspenntype (NRL)",
        "Rapportering (NRL)",
        "Hoydereferanse (NRL)",
        "Vertikalavstand meter (NRL)",
        "Verifisert nøyaktighet (NRL)",
        "Status (NRL)",
        "ObjektID (Lidar)",
        "Kvalitet (Lidar)",
        "NRL Datavask merknad Lede",
        "NRL Datavask  kommentar Lede",
        "NRL Datavask Komponentident",
        "NRL Datavask - Kommentar Kartv",
        "NRL Datavask -  Eiermatch",
        "UUIDv4",
        "Anleggsbredde meter (NRL)",
        "Luftfartshinderlyssetting(NRL)",
        "Luftfartshindermerking (NRL)",
        "Typebetegnelse Fiber rør",
        "Prosjektansvarlig selskap",
        "Stikkledning",
        "Stedfestingsarsak",
        "Datafangstdato",
        "Vertikalniva",
        "Maks avvik horisontalt (cm)",
        "Maks avvik vertikalt (cm)",
        "Hoydereferanse",
        "Stedfestingsforhold",
        "Noyaktighet hoyde (cm)",
        "Malemetode hoyde (cm)",
        "Malemetode",
        "Hovedbruk",
        "NRL_Eiermatch",
        "Ytre hoyde (cm)",
        "Ytre bredde (cm)",
        "Regional_Nett",
        "UBW-nummer",
        "Typebetegnelse",
        "Tverrsnitt",
        "Create User",
        "Create Date",
        "Noyaktighet",
        "Id på gml. erstattet komponent",
    ]

    # Write headers to both sheets
    for col_idx, header in enumerate(mast_headers):
        mast_sheet.write(0, col_idx, header)

    for col_idx, header in enumerate(trase_headers):
        trase_sheet.write(0, col_idx, header)

    # If Norwegian data is provided in common_data, use it
    norwegian_areas = data.get("norwegian_areas", ["Larvik"])
    norwegian_users = data.get("norwegian_users", ["MABJ2"])
    impregnering_types = data.get("impregnering_types", ["Kreosot", "Salt"])
    fundament_types = data.get("fundament_types", ["Stolpe på fjell", "Stolpe i jord"])

    # Generate data for mast rows
    mast_rows = []
    for _idx, mast in enumerate(data["mast_points"]):
        # Derive random but realistic values for the mast
        betegnelse = f"LM{80000 + random.randint(1000, 9999)}"
        area = random.choice(norwegian_areas)
        username = random.choice(norwegian_users)
        installationYear = random.randint(1960, 2020)  # noqa: N806
        visible_height = random.randint(5, 15)
        impregnering = random.choice(impregnering_types)
        fundament_type = random.choice(fundament_types)
        jordbånddiameter = random.choice([160, 180, 200, 220, 230, 250])
        jordbånd_dim = str(int(jordbånddiameter / 10))

        # Create row with all required data
        mast_row = {
            "ID": mast["id"],
            "Tabell ID": 109,
            "Klasse": 650,
            "Klasse_text": "LS Stolpe",
            "Father ID": 0,
            "x": mast["coordinates"][1],  # Northing (UTM y)
            "y": mast["coordinates"][0],  # Easting (UTM x)
            "z": None,  # No height data provided
            "Retning": random.randint(0, 359),
            "Tilstand": 0,
            "Betegnelse": betegnelse,
            "Betegnelse x": 0,
            "Betegnelse y": 0,
            "LabelDirection": 0,
            "Planbetegnelse": "MABJLIDARNRL",
            "Brukernavn": username,
            "Operativt område": 70564885,
            "Endret": "25.02.2025",
            "Driftsstatus": "I bruk",
            "Arbeidets ID": 0,
            "Statistic": 0,
            "Datakilde": "8501",
            "Status": 64,
            "Planlagt endring": 0,
            "Opprinnelig plan": "",
            "Område": area,
            "Eier": "Lede AS",
            "Systemoperatør": "Lede AS",
            "Ekstern ID": 0,
            "Eksternt område-ID": 0,
            "Konstruksjon ID": 0,
            "Teknisk type-ID": 0,
            "Kombinert bruk": "Nei",
            "Installasjonsår": installationYear,
            "HSp-linje": 0,
            "LSp-linje": 650,
            "Totalhøyde (m)": 0,
            "Høyde 2": 0,
            "Stolpeklasse": 0,
            "Synlig høyde (m)": visible_height,
            "Stolpetype": "Tre",
            "Impregnering": impregnering,
            "Fundament-type": fundament_type,
            "Type 1": None,
            "Materiale 1": None,
            "Isolator 1": None,
            "Jordbånddiameter (mm)": jordbånddiameter,
            "Kombinert bruk 1": "Udefinert",
            "Kombinert bruk 2": "Udefinert",
            "Kombinert bruk 3": "Udefinert",
            "Kombinert bruk 4": "Udefinert",
            "Kombinert bruk 5": "Udefinert",
            "Kombinert bruk 6": "Udefinert",
            "Merknad": None,
            "Masttype (NRL)": "Mast, lavspent",
            "Utskiftningsår travers": None,
            "UUIDv4": None,
            "Rapportering (NRL)": "Rapportering NRL utført",
            "Hoydereferanse (NRL)": "topp",  # Explicitly set height reference
            "Luftfartshinderlyssetting(NRL)": None,
            "Luftfartshindermerking (NRL)": None,
            "Vertikalavstand meter (NRL)": None,
            "Verifisert nøyaktighet (NRL)": "1",  # Verified
            "Status (NRL)": mast["status"],
            "Aktør 4": None,
            "Aktør 5": None,
            "Aktør 6": None,
            "Søknads nr Aktør 4": None,
            "Søknads nr Aktør 5": None,
            "Søknads nr Aktør 6": None,
            "Aktør Veilys": None,
            "Kryssende luftspenn": None,
            "GPS Longitude": f"{10 + random.randint(0, 10) + random.random():.5f}",
            "GPS Latitude": f"{59 + random.randint(0, 10) + random.random():.5f}",
            "UBW-nummer": None,
            "Regional_Nett": None,
            "INVKLASSE": None,
            "SAMMENFØYINGITOPP": None,
            "Create User": None,
            "Create Date": None,
            "Søknadsnr :": None,
            "Søker  :": None,
            "Veilys mastnr :": None,
            "Driftsmerking :": None,
            "Fellesføring nr :": None,
            "Avgrening": None,
            "Hovedlinje": None,
            "Bardun antall (Stk)": None,
            "Anleggsbidrag": None,
            "Grunnforhold fundament": None,
            "IsolatorType :": None,
            "Bardun type": None,
            "Jordelektrode (Type, mm2)": None,
            "MMS Tekst": None,
            "Byggeklausulert bredde (m)": None,
            "Ryddeklausulert bredde (m)": None,
            "Horisontal faseavstand (m)": None,
            "Antall isolatorskåler (stk)": None,
            "Jordbånd dim. (cm)": jordbånd_dim,
            "Samsvarserklæring": None,
            "Årstall venstrebein": None,
            "Årstall høyrebein": None,
            "Årstall mitrebein": None,
            "KILE_B": None,
            "Aktør 1": None,
            "Aktør 2": None,
            "Aktør 3": None,
            "Søknads nr Aktør 1": None,
            "Søknads nr Aktør 2": None,
            "Søknads nr Aktør 3": None,
            "PD: Skalltykkelse(mm)": None,
            "PD: Min frisk diameter(mm)": None,
            "PD: Min diameter(mm)": None,
            "Stagtvinge bardun": None,
            "Til plan (MMS)": None,
            "PD: Underdimisjonert": None,
            "PD: Råtten/Byttes": None,
            "Avgang": None,
            "Stasjon": None,
            "Id på gml. erstattet komponent": None,
            "Risikoindeks": None,
        }
        mast_rows.append(mast_row)

    # Generate random rows for trase lines
    trase_rows = []
    for _idx, trase in enumerate(data["trase_lines"]):
        # Calculate Euclidean distance for length
        start = trase["coordinates"][0]
        end = trase["coordinates"][1]
        # Simple distance calculation (not accurate for geographic coordinates
        #  but reasonable for test data)
        length = (
            (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2
        ) ** 0.5 * 100  # No z component for distance calculation

        betegnelse = random.choice(
            ["Trase", "Luftnett", "Linjetrase", "Forsyning", "Fordelingslinje"]
        )
        area = random.choice(norwegian_areas)
        username = random.choice(norwegian_users)

        # Create row with all required data
        trase_row = {
            "ID": trase["id"],
            "Tabell ID": 261,
            "Klasse": 11011,
            "Klasse_text": "Luftnett LS trase",
            "Father ID": 0,
            "x1": trase["coordinates"][0][1],  # Start northing (UTM y)
            "y1": trase["coordinates"][0][0],  # Start easting (UTM x)
            "z1": None,  # No height data
            "x2": trase["coordinates"][1][1],  # End northing (UTM y)
            "y2": trase["coordinates"][1][0],  # End easting (UTM x)
            "z2": None,  # No height data
            "Lengde (m)": length,
            "Bryterens tilstand 1": 0,
            "Bryterens tilstand 2": 0,
            "Betegnelse": betegnelse,
            "Betegnelse x": 0,
            "Betegnelse y": 0,
            "LabelDirection": 200,
            "Planbetegnelse": "MABJLIDARNRL",
            "Brukernavn": username,
            "Operativt område": 70564885,
            "Endret": "25.02.2025",
            "Driftsstatus": "I bruk",
            "Arbeidets ID": 0,
            "Statistic": 0,
            "Datakilde": "0",
            "Status": 64,
            "Planlagt endring": 0,
            "Opprinnelig plan": "",
            "Systemoperatør": "Lede AS",
            "Ekstern ID": 0,
            "Eksternt område-ID": 0,
            "Konstruksjon ID": 0,
            "Teknisk type-ID": 0,
            "CutId": 0,
            "Område": area,
            "Eier": "Lede AS",
            "Miljø": "Ikke bestemt",
            "Dybde (cm)": 0,
            "Tverrsnitt-ID": 0,
            "Merknad": None,
            "Luftspenntype (NRL)": "Ledning, lavspent",
            "Rapportering (NRL)": "Rapportering NRL utført",
            "Hoydereferanse (NRL)": "topp",  # Explicitly set height reference
            "Vertikalavstand meter (NRL)": None,
            "Verifisert nøyaktighet (NRL)": "1",  # Verified
            "Status (NRL)": trase["status"],
            "ObjektID (Lidar)": None,
            "Kvalitet (Lidar)": None,
            "NRL Datavask merknad Lede": None,
            "NRL Datavask  kommentar Lede": None,
            "NRL Datavask Komponentident": None,
            "NRL Datavask - Kommentar Kartv": None,
            "NRL Datavask -  Eiermatch": None,
            "UUIDv4": None,
            "Anleggsbredde meter (NRL)": None,
            "Luftfartshinderlyssetting(NRL)": None,
            "Luftfartshindermerking (NRL)": None,
            "Typebetegnelse Fiber rør": None,
            "Prosjektansvarlig selskap": None,
            "Stikkledning": None,
            "Stedfestingsarsak": None,
            "Datafangstdato": None,
            "Vertikalniva": None,
            "Maks avvik horisontalt (cm)": None,
            "Maks avvik vertikalt (cm)": None,
            "Hoydereferanse": None,
            "Stedfestingsforhold": None,
            "Noyaktighet hoyde (cm)": None,
            "Malemetode hoyde (cm)": None,
            "Malemetode": None,
            "Hovedbruk": None,
            "NRL_Eiermatch": None,
            "Ytre hoyde (cm)": None,
            "Ytre bredde (cm)": None,
            "Regional_Nett": None,
            "UBW-nummer": None,
            "Typebetegnelse": None,
            "Tverrsnitt": None,
            "Create User": None,
            "Create Date": None,
            "Noyaktighet": None,
            "Id på gml. erstattet komponent": None,
        }
        trase_rows.append(trase_row)

    # Write Mast data to the sheet
    for row_idx, row_data in enumerate(mast_rows):
        for col_idx, header in enumerate(mast_headers):
            # Handle special case for "Klasse" which appears twice
            if header == "Klasse" and col_idx == 3:
                mast_sheet.write(row_idx + 1, col_idx, row_data.get("Klasse_text"))
            else:
                mast_sheet.write(row_idx + 1, col_idx, row_data.get(header))

    # Write Trase Element data to the sheet
    for row_idx, row_data in enumerate(trase_rows):
        for col_idx, header in enumerate(trase_headers):
            # Handle special case for "Klasse" which appears twice
            if header == "Klasse" and col_idx == 3:
                trase_sheet.write(row_idx + 1, col_idx, row_data.get("Klasse_text"))
            else:
                trase_sheet.write(row_idx + 1, col_idx, row_data.get(header))

    # Set column widths for better appearance
    mast_sheet.set_column(16, 16, 15.125)  # Column Q
    mast_sheet.set_column(17, 17, 9.875)  # Column R

    # Close the workbook
    workbook.close()


def generate_geojson(data: dict, filename: str) -> None:
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
    geojson = {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {"name": epsg_code},
        },
        "features": [],
    }

    # Add line features (Trase Elements)
    for line in data["trase_lines"]:
        # Make sure coordinates are 2D only (no height)
        coordinates = [line["coordinates"][0], line["coordinates"][1]]

        feature = {
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": coordinates},
            "properties": {
                "featureType": "NrlLuftspenn",
                "status": line["status"].lower(),  # Use lowercase status
                "komponentident": line["id"],
                "verifisertRapporteringsnøyaktighet": "1",  # Set to verified
                "referanse": {"komponentkodeverdi": line["komponentident"]},
                "luftspennType": from_nrl_luftspenn_type(line["luftspennType"]),
            },
        }
        geojson["features"].append(feature)

    # Add point features (Masts)
    for point in data["mast_points"]:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": point["coordinates"],
            },  # 2D coordinates
            "properties": {
                "featureType": "NrlMast",
                "status": point["status"].lower(),  # Use lowercase status
                "komponentident": point["id"],
                "verifisertRapporteringsnøyaktighet": "1",  # Set to verified
                "referanse": {"komponentkodeverdi": point["komponentident"]},
                "mastType": from_nrl_mast_type(point["mastType"]),
            },
        }
        geojson["features"].append(feature)

    # Write to file
    file_path = Path(filename)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)


def from_nrl_luftspenn_type(luftspenn_type: str) -> int:
    """Map NRL luftspennType string to integer code."""
    if re.search(r"regional", luftspenn_type, re.IGNORECASE):
        return 8
    if re.search(r"h[oø]gspent|h[oø]yspent", luftspenn_type, re.IGNORECASE):
        return 4
    if re.search(r"lavspent", luftspenn_type, re.IGNORECASE):
        return 6
    msg = f"Unexpected luftspenn_type: {luftspenn_type}"
    raise ValueError(msg)


def from_nrl_mast_type(mast_type: str) -> int:
    """Map NRL mastType string to integer code."""
    if re.search(r"regional", mast_type, re.IGNORECASE):
        return 8
    if re.search(r"h[oø]gspent|h[oø]yspent", mast_type, re.IGNORECASE):
        return 4
    if re.search(r"lavspent", mast_type, re.IGNORECASE):
        return 6
    msg = f"Unexpected mast_type: {mast_type}"
    raise ValueError(msg)
