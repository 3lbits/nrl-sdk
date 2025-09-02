"""Module for job model."""

from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class JobOperation(str, Enum):
    """Enum for operation types.

    This enum defines the types of operations that can be performed on a job.
    """

    VALIDATE = "validate"
    """Operation for validating data."""

    REPORT = "report"
    """Operation for reporting data."""


class JobStatus(str, Enum):
    """Enum for job status types.

    This enum defines the possible statuses for a job.
    """

    PENDING = "pending"
    """Job is pending and has not yet started."""

    IN_PROGRESS = "in_progress"
    """Job is currently being processed."""

    COMPLETED = "completed"
    """Job has been completed successfully."""

    FAILED = "failed"
    """Job has failed during processing."""


class JobData(BaseModel):
    """A job data model for storing the data related to the job .

    The job data model represents the data associated with a job, including its content type and the actual content.

    Attributes:
        id (UUID): Unique identifier for the job data.
        content_type (str): Type of content being stored (e.g., "application/json").
        content (bytes): The actual content data in bytes.

    """

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    content_type: str
    content: bytes | None = None
    id: UUID | None = Field(default_factory=uuid4)


class Job(BaseModel):
    """A job model.

    The job model represents a processing task that can be validated or reported.

    Attributes:
        id (UUID): Unique identifier for the job.
        status (JobStatus): Current status of the job.
        content_type (str): Type of content being processed in the job.
        operation (JobOperation): Type of operation being performed in the job.
        created_at (datetime): Timestamp when the job was created.
        started_at (datetime | None): Timestamp when the job became in progress.
        created_for_org (str): Organization for which the job was created.
        geojson_data (list[JobData] | None): List of  geojson data associated with the job.
        cim_data (JobData | None): The cim data associated with the job.
        created_by_user (str): Username of the user who created the job.
        finished_at (datetime | None): Timestamp when the job finished.
        number_of_features (int | None): Number of features processed in the job.
        number_of_batches (int | None): Number of batches processed in the job.
        batch_size (int | None): Size of each batch processed in the job.

    """

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    status: JobStatus
    content_type: str
    operation: JobOperation
    created_at: datetime
    created_for_org: str
    geojson_data: list[JobData] | None = None
    cim_data: JobData | None = None
    created_by_user: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    number_of_features: int | None = None
    number_of_batches: int | None = None
    batch_size: int | None = None
    id: UUID | None = Field(default_factory=uuid4)
