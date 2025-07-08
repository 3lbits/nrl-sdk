#!/usr/bin/env python
"""Command-line interface for the NRL test data generator."""

import argparse
import sys
from . import nrl_generator


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate test data for NRL (Nasjonalt Register over Luftfartshindre)"
    )
    parser.add_argument(
        "-n",
        "--num-elements",
        type=int,
        default=2,
        help="Number of elements to generate for each type (will create n mast points AND n trase lines, totaling 2*n elements)",
    )
    parser.add_argument(
        "-t",
        "--total-elements",
        type=int,
        help="Total number of elements to generate (divided equally between mast points and trase lines)",
    )
    parser.add_argument(
        "-o",
        "--output-prefix",
        type=str,
        default="testdata",
        help="Prefix for output filenames",
    )
    parser.add_argument(
        "-s",
        "--status",
        type=str,
        choices=["eksisterende", "fjernet", "planlagtFjernet", "planlagtOppført"],
        default="planlagtOppført",
        help='Set the "Status (NRL)" value for all elements',
    )
    parser.add_argument(
        "-r",
        "--region",
        type=str,
        choices=[
            "Oslo_area",
            "Larvik_area",
            "Bergen_area",
            "Stavanger_area",
            "Kristiansand_area",
            "Trondheim_area",
            "Hjorring_Denmark",
            "Gothenburg_Sweden",
        ],
        help="Specify the region for data generation (default: random Norwegian region). Error regions available for testing.",
    )
    parser.add_argument(
        "--include-errors",
        action="store_true",
        help="Include error regions (outside Norway) when randomly selecting regions",
    )
    parser.add_argument(
        "--error-pos",
        type=str,
        help="Comma-separated list of positions (1-based) where errors should be injected (e.g., 2,5,7,21)",
    )
    parser.add_argument(
        "--error-freq",
        type=float,
        help="Frequency of error injection (0.0-1.0, e.g., 0.2 for 20%% errors)",
    )

    return parser.parse_args()


def main():
    """Entry point for the command-line application."""
    args = parse_args()

    try:
        # If total-elements is specified, use that instead of num-elements
        if args.total_elements:
            # Divide by 2 and round up to ensure we get the exact total
            num_each = (args.total_elements + 1) // 2
        else:
            num_each = args.num_elements

        if args.region:
            print(f"Generating NRL test data in the {args.region} region...")
        else:
            if args.include_errors:
                print(
                    "Generating NRL test data with randomly selected regions (including error regions outside Norway)..."
                )
            else:
                print(
                    "Generating NRL test data with randomly selected regions across Norway..."
                )
                print(
                    "This ensures a lower chance of resubmitting data for the same location."
                )

        # Parse error positions if provided
        error_positions = None
        if args.error_pos:
            try:
                error_positions = [int(x.strip()) for x in args.error_pos.split(",")]
            except ValueError:
                print(
                    "Error: Invalid error positions format. Use comma-separated integers (e.g., 2,5,7,21)",
                    file=sys.stderr,
                )
                return 1

        # Validate error frequency if provided
        if args.error_freq is not None:
            if not 0.0 <= args.error_freq <= 1.0:
                print(
                    "Error: Error frequency must be between 0.0 and 1.0",
                    file=sys.stderr,
                )
                return 1

        # Generate NRL test data
        result = nrl_generator.generate_files(
            num_elements=num_each,
            output_prefix=args.output_prefix,
            status=args.status,
            region=args.region,
            include_errors=args.include_errors,
            error_positions=error_positions,
            error_freq=args.error_freq,
        )

        # Extract the region name if available
        region_name = result.get("region_name", "Random region")

        print("Files generated successfully:")
        print(f"  - Excel: {result['excel_file']}")
        print(f"  - GeoJSON: {result['geojson_file']}")
        if "error_log_file" in result:
            print(f"  - Error log: {result['error_log_file']}")
        print(f"  - Total elements: {result['total_elements']}")
        print(f"  - Status (NRL): {result['status']}")
        print(f"  - Generated in region: {region_name}")

        return 0
    except Exception as e:
        print(f"Error generating test data: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
