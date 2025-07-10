# nrl-sdk-lib

The nrl-sdk-lib provides models and code snippets for working with the NRL SDK. It includes various models such as `FeatureCollection`, `Feature`, and `Geometry`, as well as utility functions for handling these models.

## Development

To set up the development environment, you need to install the required dependencies:.
```bash
uv sync
```

To upgrade the dependencies, you can run:
```bash
uv sync --upgrade
```

To run the pipeline, you can use the following command:
```bash
uv run poe release
```

To see the docs, run:
```bash
uv run poe create-docs
uv run poe serve-docs
```
