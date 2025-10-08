"""Module for job model."""

from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class Status(str, Enum):
    """Enum for status types.

    This enum defines the possible statuses for a job or a batch.
    """

    PENDING = "pending"
    """It is pending and has not yet started."""

    JOB_DATA_SPLITTING_DONE = "job_data_splitting_done"
    """Job is pending and has not yet started."""

    IN_PROGRESS = "in_progress"
    """It is currently being processed."""

    COMPLETED = "completed"
    """It has been completed successfully."""

    FAILED = "failed"
    """It has failed during processing."""


class BatchData(BaseModel):
    """A batch data model for storing the data related to a batch.

    The batch data model represents the data associated with a batch, including its content type and the actual content.

    Attributes:
        batch_number (int): The sequence number of the batch.
        status (Status): Current status of the batch.
        content_type (str): Type of content being stored (e.g., "application/json").
        job_id (UUID): Identifier for the job associated with this batch.
        content (bytes): The actual content data in bytes.
        created_at (datetime): Timestamp when the batch was created.
        started_at (datetime | None): Timestamp when the batch became in progress.
        finished_at (datetime | None): Timestamp when the batch finished.
        number_of_features (int | None): Number of features in the batch.
        id (UUID): Unique identifier for the batch data.

    """

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    batch_number: int
    status: Status
    content_type: str
    job_id: UUID
    created_at: datetime
    content: dict | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    number_of_features: int | None = None
    id: UUID | None = Field(default_factory=uuid4)


class JobOperation(str, Enum):
    """Enum for operation types.

    This enum defines the types of operations that can be performed on a job.
    """

    VALIDATE = "validate"
    """Operation for validating data."""

    REPORT = "report"
    """Operation for reporting data."""


class JobDataType(str, Enum):
    """Enum for job data types.

    This enum defines the possible types of job data.
    """

    GEOJSON = "geojson"
    """Job data type for GeoJSON data."""

    CIM = "cim"
    """Job data type for CIM data."""


class JobData(BaseModel):
    """A job data model for storing the data related to the job .

    The job data model represents the data associated with a job, including its content type and the actual content.

    Attributes:
        type (JobDataType): Type of job data (e.g., "geojson" or "cim").
        content_type (str): Type of content being stored (e.g., "application/json").
        job_id (UUID): Identifier for the job associated with this data.
        content (bytes): The actual content data in bytes.
        id (UUID): Unique identifier for the job data.

    """

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    type: JobDataType
    content_type: str
    job_id: UUID
    content: bytes | None = None
    id: UUID | None = Field(default_factory=uuid4)


class Job(BaseModel):
    """A job model.

    The job model represents a processing task that can be validated or reported.

    Attributes:
        id (UUID): Unique identifier for the job.
        status (Status): Current status of the job.
        content_type (str): Type of content being processed in the job.
        operation (JobOperation): Type of operation being performed in the job.
        created_at (datetime): Timestamp when the job was created.
        started_at (datetime | None): Timestamp when the job became in progress.
        created_for_org (str): Organization for which the job was created.
        job_data (list[JobData] | None): List of data associated with the job.
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

    status: Status
    content_type: str
    operation: JobOperation
    created_at: datetime
    created_for_org: str
    job_data: list[JobData] | None = None
    created_by_user: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    number_of_features: int | None = None
    number_of_batches: int | None = None
    batch_size: int | None = None
    id: UUID | None = Field(default_factory=uuid4)
