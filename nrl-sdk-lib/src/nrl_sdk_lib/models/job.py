"""Module for job model."""

from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class OperationType(str, Enum):
    """Enum for operation types.

    This enum defines the types of operations that can be performed on a job.
    """

    VALIDATE = "validate"
    """Operation for validating data."""

    REPORT = "report"
    """Operation for reporting data."""


class Job(BaseModel):
    """A job model.

    The job model represents a processing task that can be validated or reported.

    Attributes:
        id (UUID): Unique identifier for the job.
        status (str): Current status of the job.
        content_type (str): Type of content being processed in the job.
        operation (OperationType): Type of operation being performed in the job.
        data_id (UUID): Identifier for the data associated with the job.
        created_at (datetime): Timestamp when the job was created.
        created_by_user (str): Username of the user who created the job.
        created_for_org (str): Organization for which the job was created.
        completed_at (datetime | None): Timestamp when the job was completed, if applicable.

    """

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    status: str
    content_type: str
    operation: OperationType
    data_id: UUID
    created_at: datetime
    created_by_user: str
    created_for_org: str
    completed_at: datetime | None = None
    id: UUID | None = Field(default_factory=uuid4)
