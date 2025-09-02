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
    """A Geometry model.

    The Geometry model serves as a base class for different geometry types such as Point, Polygon, and LineString.

    Attributes:
        type (Literal["Point", "Polygon", "LineString"]): The type of geometry

    """

    model_config = ConfigDict(
        extra="forbid",  # Forbid extra fields
    )

    type: Literal["Point", "Polygon", "LineString"]


class Point(Geometry):
    """A Point geometry model.

    The Point model represents a single point in a two-dimensional space.

    Attributes:
        coordinates (list[float]): A list of two or three floats representing the x, y and z coordinates of the point.

    """

    coordinates: list[float]


class Polygon(Geometry):
    """A Polygon geometry model.

    The Polygon model represents a polygon defined by a list of linear rings, where each ring is a list of points.

    Attributes:
        coordinates (list[list[list[float]]]): A list of linear rings, where each ring is a list of points,
            and each point is represented by a list of two or three floats (x, y, z).

    """

    coordinates: list[list[list[float]]]


class LineString(Geometry):
    """A LineString geometry model.

    The LineString model represents a sequence of points connected by straight lines.

    Attributes:
        coordinates (list[list[float]]): A list of points, where each point is represented by a list of two or three floats (x, y, z).

    """

    coordinates: list[list[float]]
