"""Module for a simplified feature collection model."""

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Parent(BaseModel):
    """A base model for all other models."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",  # Forbid extra fields
    )


class CrsProperties(Parent):
    """A CRS properties model.

    The CrsProperties model represents the properties of a Coordinate Reference System (CRS).

    Attributes:
        name (str): The name of the CRS.

    """

    name: str


class Crs(Parent):
    """A CRS model.

    The Crs model represents a Coordinate Reference System (CRS) with its properties.

    Attributes:
        type (str): The type of CRS, typically "name".
        properties (CrsProperties): The properties of the CRS.

    """

    model_config = ConfigDict(
        extra="forbid",  # Forbid extra fields
    )

    type: str = "name"
    properties: CrsProperties
