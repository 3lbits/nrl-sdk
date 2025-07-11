# NRL Test Data Generator

A utility for generating test data for the NRL (Nasjonalt Register over Luftfartshindre) project.

## Installation

This project uses `uv` for Python package management. If you haven't installed `uv` yet, you can find instructions at [the uv GitHub repository](https://github.com/astral-sh/uv).

### Setting Up a Development Environment

```bash
# Clone the repository
# Navigate to the project directory

# Create a virtual environment
uv venv

# Activate the environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package in development mode
uv pip install -e .
```

## Usage

Generate Excel and GeoJSON files with NRL-specific data:

```bash
generate-testdata --num-elements 5 --status eksisterende
```

Options:
- `--num-elements`, `-n`: Number of elements of each type to generate (default: 2)
- `--total-elements`, `-t`: Total number of elements to generate (divided equally)
- `--output-prefix`, `-o`: Prefix for output filenames (default: testdata)
- `--status`, `-s`: Status value for elements (choices: eksisterende, fjernet, planlagtFjernet, planlagtOppført; default: planlagtOppført)

### Help

To see all available options:

```bash
generate-testdata --help
```

## Output Files

The tool generates two files:
1. An Excel file (.xlsx) with detailed information about mast points and trase elements
2. A GeoJSON file (.geojson) with geographic features corresponding to the same elements

Both files include:
- Mast points (with properties like height, installation year, material type)
- Trase lines (connections between mast points)

The filenames include the number of elements and a timestamp to ensure uniqueness.

### Note on Coordinates and Heights

To prevent validation errors with the Norwegian National Detailed Height Model (NDH), this tool uses predefined coordinates near Larvik with height=0. This approach ensures the generated data will be accepted by the NRL API, which validates that object heights are consistent with the terrain elevation data.

The fixed coordinates limit geographic variation but allow for creating valid test data that can be used with the NRL system.

## Dependencies

- xlsxwriter: For generating Excel files
- uuid: For generating unique identifiers
