"""Module for response message model."""

from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from nrl_sdk_lib.models import KomponentReferanse


class ResultError(BaseModel):
    """A result error model.

    The result error model represents an error encountered during a validation or reporting process.

    Attributes:
        reason (str): A description of the error encountered.
        komponent_id (UUID | None): An optional identifier for the component associated with the error.
        referanse (KomponentReferanse | None): An optional reference dictionary providing additional context about the error.
        id (UUID | None): A unique identifier for the error, automatically generated if not provided

    """

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    reason: str
    komponent_id: UUID | None = None
    referanse: KomponentReferanse | None = None
    id: UUID | None = Field(default_factory=uuid4)


class ResultStatus(str, Enum):
    """Enumeration for result statuses.

    This enum defines the possible statuses for a result, such as "success" or "failure".

    Attributes:
        SUCCESS (str): Indicates a successful result.
        FAILURE (str): Indicates a failed result.

    """

    SUCCESS = "success"
    FAILURE = "failure"


class ResultType(str, Enum):
    """Enumeration for result types.

    This enum defines the possible types of results, such as "validation" or "reporting".

    Attributes:
        STRUCTURE_VALIDATION_ERRORS (str): Indicates errors related to structure validation.
        VALIDATION_EXCEPTION (str): Indicates a validation exception.
        HTTP_MESSAGE_NOT_READABLE_EXCEPTION (str): Indicates an HTTP message not readable exception.
        AUTHORIZATION_DENIED_EXCEPTION (str): Indicates an authorization denied exception.
        METHOD_ARGUMENT_NOT_VALID_EXCEPTION (str): Indicates a method argument not valid exception.

    """

    STRUCTURE_VALIDATION_ERRORS = "StructureValidationErrors"
    VALIDATION_EXCEPTION = "ValidationException"
    HTTP_MESSAGE_NOT_READABLE_EXCEPTION = "HttpMessageNotReadableException"
    AUTHORIZATION_DENIED_EXCEPTION = "AuthorizationDeniedException"
    METHOD_ARGUMENT_NOT_VALID_EXCEPTION = "MethodArgumentNotValidException"


class ResultStage(int, Enum):
    """Enumeration for result stages.

    This enum defines the possible stages of validation errors.

    Attributes:
        STRUCTURAL (int): Represents the structural validation stage.
        OWNERSHIP (int): Represents the ownership validation stage.
        BASIC_VALUE_VALIDATION (int): Represents the basic value validation stage.
        ADVANCED_VALUE_VALIDATION (int): Represents the advanced value validation stage.

    """

    STRUCTURAL = 1
    OWNERSHIP = 2
    BASIC_VALUE_VALIDATION = 3
    ADVANCED_VALUE_VALIDATION = 4


class Result(BaseModel):
    """A result model.

    The result model represents the outcome of a validation or reporting process.

    Attributes:
        status (str): The status of the result, e.g., "success" or "
        stage (int): The stage of the process, typically an integer indicating the step in the workflow.
        job_id (UUID): The unique identifier of the job associated with this result.
        batch_number (int | None): The batch number if the job was processed in batches.
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

    status: ResultStatus
    job_id: UUID
    batch_number: int | None = None
    type: ResultType | str | None = None
    stage: ResultStage | None = None
    errors: list[ResultError] | None = Field(default_factory=list)
    id: UUID | None = Field(default_factory=uuid4)
