"""Command-line interface for the NRL test data generator."""

import sys

import click

from . import nrl_generator


@click.command()
@click.version_option(message=("nrl-test-data-generator, %(version)s"))
@click.option(
    "-n",
    "--num-elements",
    type=int,
    default=2,
    show_default=True,
    help=(
        "Number of elements to generate for each type "
        "(will create n mast points AND n trase lines, totaling 2*n elements)"
    ),
)
@click.option(
    "-t",
    "--total-elements",
    type=int,
    help=(
        "Total number of elements to generate (divided equally between "
        "mast points and trase lines)"
    ),
)
@click.option(
    "-o",
    "--output-prefix",
    type=str,
    default="testdata",
    show_default=True,
    help="Prefix for output filenames",
)
@click.option(
    "-s",
    "--status",
    type=click.Choice(
        ["eksisterende", "fjernet", "planlagtFjernet", "planlagtOppført"]
    ),
    default="planlagtOppført",
    help='Set the "Status (NRL)" value for all elements',
)
@click.option(
    "-r",
    "--region",
    type=click.Choice(
        [
            "Oslo_area",
            "Larvik_area",
            "Bergen_area",
            "Stavanger_area",
            "Kristiansand_area",
            "Trondheim_area",
            "Hjorring_Denmark",
            "Gothenburg_Sweden",
        ]
    ),
    help=(
        "Specify the region for data generation (default: random Norwegian region). "
        "Error regions available for testing."
    ),
)
@click.option(
    "--include-errors/--exclude-errors",
    default=False,
    show_default=True,
    help="Include error regions (outside Norway) when randomly selecting regions",
)
@click.option(
    "--error-pos",
    type=str,
    help=(
        "Comma-separated list of positions (1-based) where "
        "errors should be injected (e.g., 2,5,7,21)"
    ),
)
@click.option(
    "--error-freq",
    type=float,
    help="Frequency of error injection (0.0-1.0, e.g., 0.2 for 20%% errors)",
)
def cli(  # noqa: PLR0913
    num_elements: int,
    total_elements: int,
    output_prefix: str,
    status: str,
    region: str,
    error_pos: str,
    error_freq: float,
    *,
    include_errors: bool,
) -> int:
    """Generate test data for NRL (Nasjonalt Register over Luftfartshindre)."""
    # If total-elements is specified, use that instead of num-elements
    # Divide by 2 and round up to ensure we get the exact total
    num_each = (total_elements + 1) // 2 if total_elements else num_elements

    if region:
        click.echo(f"Generating NRL test data in the {region} region...")
    elif include_errors:
        click.echo(
            "Generating NRL test data with randomly selected regions "
            "(including error regions outside Norway)..."
        )
    else:
        click.echo(
            "Generating NRL test data with randomly selected regions across Norway..."
        )
        click.echo(
            "This ensures a lower chance of resubmitting data for the same location."
        )

    # Parse error positions if provided
    error_positions = None
    if error_pos:
        try:
            error_positions = [int(x.strip()) for x in error_pos.split(",")]
        except ValueError:
            msg = (
                "Error: Invalid error positions format. "
                "Use comma-separated integers (e.g., 2,5,7,21)"
            )
            raise click.Abort(msg) from None

    # Validate error frequency if provided
    if error_freq is not None and not 0.0 <= error_freq <= 1.0:
        msg = "Error: Error frequency must be between 0.0 and 1.0"
        raise click.Abort(msg) from None

    try:
        # Generate NRL test data
        result = nrl_generator.generate_files(
            num_elements=num_each,
            output_prefix=output_prefix,
            status=status,
            region=region,
            include_errors=include_errors,
            error_positions=error_positions,
            error_freq=error_freq,
        )

        # Extract the region name if available
        region_name = result.get("region_name", "Random region")

        click.echo("Files generated successfully:")
        click.echo(f"  - Excel: {result['excel_file']}")
        click.echo(f"  - GeoJSON: {result['geojson_file']}")
        if "error_log_file" in result:
            click.echo(f"  - Error log: {result['error_log_file']}")
        click.echo(f"  - Total elements: {result['total_elements']}")
        click.echo(f"  - Status (NRL): {result['status']}")
        click.echo(f"  - Generated in region: {region_name}")

    except Exception as e:  # pragma: no cover
        click.echo(f"Error generating test data: {e}", file=sys.stderr)
        raise click.Abort(e) from e

    return 0
