"""Module for a simplified feature collection model."""

from typing import Literal

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Parent(BaseModel):
    """A base model for all other models."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",  # Forbid extra fields
    )


class Geometry(Parent):
    """A Geometry model."""

    model_config = ConfigDict(
        extra="forbid",  # Forbid extra fields
    )

    type: Literal["Point", "Polygon", "LineString"]


class Point(Geometry):
    """A Point geometry model."""

    coordinates: list[float]


class Polygon(Geometry):
    """A Polygon geometry model."""

    coordinates: list[list[list[float]]]


class LineString(Geometry):
    """A LineString geometry model."""

    coordinates: list[list[float]]
