"""Module for response message model."""

from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class ResultError(BaseModel):
    """A result error model.

    The result error model represents an error encountered during a validation or reporting process.

    Attributes:
        reason (str): A description of the error encountered.
        komponent_id (UUID | None): An optional identifier for the component associated with the error.
        id (UUID | None): A unique identifier for the error, automatically generated if not provided

    """

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    reason: str
    komponent_id: UUID | None = None
    id: UUID | None = Field(default_factory=uuid4)


class Result(BaseModel):
    """A result model.

    The result model represents the outcome of a validation or reporting process.

    Attributes:
        status (str): The status of the result, e.g., "success" or "
        stage (int): The stage of the process, typically an integer indicating the step in the workflow.
        job_id (UUID): The unique identifier of the job associated with this result.
        type (str | None): The type of result, if applicable.
        errors (list[ResultError] | None): A list of errors encountered during the process
            or an empty list if there are no errors.
        id (UUID | None): A unique identifier for the result, automatically generated if not provided

    """

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    status: str
    stage: int  # Should be enum.
    job_id: UUID
    type: str | None = None
    errors: list[ResultError] | None = Field(default_factory=list)
    id: UUID | None = Field(default_factory=uuid4)
