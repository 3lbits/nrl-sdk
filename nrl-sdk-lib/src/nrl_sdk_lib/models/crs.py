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
    """A CRS properties model."""

    name: str


class Crs(Parent):
    """A CRS model."""

    model_config = ConfigDict(
        extra="forbid",  # Forbid extra fields
    )

    type: str = "name"
    properties: CrsProperties
