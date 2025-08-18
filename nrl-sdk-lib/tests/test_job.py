"""Test module for job model."""

from datetime import UTC, datetime
from uuid import UUID

import pytest

from nrl_sdk_lib.models.job import Job, OperationType


@pytest.fixture
def anyio_backend() -> str:
    """Use the asyncio backend for the anyio fixture."""
    return "asyncio"


@pytest.mark.anyio
async def test_job_model_with_id() -> None:
    """Should create a valid job object."""
    job_data = {
        "id": "1cda28c1-f84c-430f-b2ce-a2297a4262b8",
        "status": "pending",
        "content_type": "application/json",
        "operation": OperationType.VALIDATE,
        "data_id": "7c93f77d-af17-4145-86c8-e3d17a3f1541",
        "created_at": datetime(2023, 10, 1, 12, 0, 0, tzinfo=UTC),
        "created_by_user": "testuser",
        "created_for_org": "testorg",
    }

    job = Job.model_validate(job_data)
    assert job.id == UUID("1cda28c1-f84c-430f-b2ce-a2297a4262b8")
    assert job.status == "pending"
    assert job.content_type == "application/json"
    assert job.operation == OperationType.VALIDATE
    assert job.data_id == UUID("7c93f77d-af17-4145-86c8-e3d17a3f1541")
    assert job.created_at == datetime(2023, 10, 1, 12, 0, 0, tzinfo=UTC)
    assert job.created_by_user == "testuser"
    assert job.created_for_org == "testorg"
    assert job.completed_at is None


@pytest.mark.anyio
async def test_job_model_without_id() -> None:
    """Should create a valid job object with id."""
    job_data = {
        "status": "pending",
        "content_type": "application/json",
        "operation": OperationType.VALIDATE,
        "data_id": "7c93f77d-af17-4145-86c8-e3d17a3f1541",
        "created_at": datetime(2023, 10, 1, 12, 0, 0, tzinfo=UTC),
        "created_by_user": "testuser",
        "created_for_org": "testorg",
    }

    job = Job.model_validate(job_data)

    assert isinstance(job.id, UUID)
    assert job.status == "pending"
    assert job.content_type == "application/json"
    assert job.operation == OperationType.VALIDATE
    assert job.data_id == UUID("7c93f77d-af17-4145-86c8-e3d17a3f1541")
    assert job.created_at == datetime(2023, 10, 1, 12, 0, 0, tzinfo=UTC)
    assert job.created_by_user == "testuser"
    assert job.created_for_org == "testorg"
    assert job.completed_at is None
