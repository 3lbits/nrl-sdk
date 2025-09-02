"""Test module for job model."""

from datetime import UTC, datetime
from uuid import UUID

import pytest

from nrl_sdk_lib.models.job import Job, JobData, JobOperation


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
        "operation": JobOperation.VALIDATE,
        "geojson_data": [
            {
                "id": "7c93f77d-af17-4145-86c8-e3d17a3f1541",
                "content_type": "application/json",
            }
        ],
        "created_at": datetime(2023, 10, 1, 12, 0, 0, tzinfo=UTC),
        "created_by_user": "testuser",
        "created_for_org": "testorg",
    }

    job = Job.model_validate(job_data)
    assert job.id == UUID("1cda28c1-f84c-430f-b2ce-a2297a4262b8")
    assert job.status == "pending"
    assert job.content_type == "application/json"
    assert job.operation == JobOperation.VALIDATE
    assert job.created_at == datetime(2023, 10, 1, 12, 0, 0, tzinfo=UTC)
    assert job.created_by_user == "testuser"
    assert job.created_for_org == "testorg"
    assert job.finished_at is None
    for geojson in job.geojson_data or []:
        assert isinstance(geojson.id, UUID)
        assert geojson.content_type == "application/json"
        assert geojson.content is None


@pytest.mark.anyio
async def test_job_model_without_id() -> None:
    """Should create a valid job object with id."""
    job_data = {
        "status": "pending",
        "content_type": "application/json",
        "operation": JobOperation.VALIDATE,
        "geojson_data": [
            {
                "id": "7c93f77d-af17-4145-86c8-e3d17a3f1541",
                "content_type": "application/json",
            }
        ],
        "created_at": datetime(2023, 10, 1, 12, 0, 0, tzinfo=UTC),
        "created_by_user": "testuser",
        "created_for_org": "testorg",
    }

    job = Job.model_validate(job_data)

    assert isinstance(job.id, UUID)
    assert job.status == "pending"
    assert job.content_type == "application/json"
    assert job.operation == JobOperation.VALIDATE
    assert job.created_at == datetime(2023, 10, 1, 12, 0, 0, tzinfo=UTC)
    assert job.created_by_user == "testuser"
    assert job.created_for_org == "testorg"
    assert job.finished_at is None
    for geojson in job.geojson_data or []:
        assert isinstance(geojson, JobData)
        assert isinstance(geojson.id, UUID)
        assert geojson.content_type == "application/json"
        assert geojson.content is None


@pytest.mark.anyio
async def test_job_model_with_cim() -> None:
    """Should create a valid job object with id."""
    job_data = {
        "status": "pending",
        "content_type": "application/json",
        "operation": JobOperation.VALIDATE,
        "cim_data": {
            "id": "292fdfae-9e3a-4389-b6a8-0bfbd662fff9",
            "content_type": "application/json",
        },
        "created_at": datetime(2023, 10, 1, 12, 0, 0, tzinfo=UTC),
        "created_by_user": "testuser",
        "created_for_org": "testorg",
    }

    job = Job.model_validate(job_data)

    assert isinstance(job.id, UUID)
    assert job.status == "pending"
    assert job.content_type == "application/json"
    assert job.operation == JobOperation.VALIDATE
    assert job.created_at == datetime(2023, 10, 1, 12, 0, 0, tzinfo=UTC)
    assert job.created_by_user == "testuser"
    assert job.created_for_org == "testorg"
    assert job.finished_at is None
    assert isinstance(job.cim_data, JobData)
    assert isinstance(job.cim_data.id, UUID)
    assert job.cim_data.content_type == "application/json"
    assert job.cim_data.content is None


@pytest.mark.anyio
async def test_job_model_with_cim_and_geojson() -> None:
    """Should create a valid job object with id."""
    job_data = {
        "status": "pending",
        "content_type": "application/json",
        "operation": JobOperation.VALIDATE,
        "geojson_data": [
            {
                "id": "7c93f77d-af17-4145-86c8-e3d17a3f1541",
                "content_type": "application/json",
            },
            {
                "id": "64f5c666-e180-4aaa-b3d6-b98921b95bbc",
                "content_type": "application/json",
            },
        ],
        "cim_data": {
            "id": "292fdfae-9e3a-4389-b6a8-0bfbd662fff9",
            "content_type": "application/json",
        },
        "created_at": datetime(2023, 10, 1, 12, 0, 0, tzinfo=UTC),
        "created_by_user": "testuser",
        "created_for_org": "testorg",
    }

    job = Job.model_validate(job_data)

    assert isinstance(job.id, UUID)
    assert job.status == "pending"
    assert job.content_type == "application/json"
    assert job.operation == JobOperation.VALIDATE
    assert job.created_at == datetime(2023, 10, 1, 12, 0, 0, tzinfo=UTC)
    assert job.created_by_user == "testuser"
    assert job.created_for_org == "testorg"
    assert job.finished_at is None
    for geojson in job.geojson_data or []:
        assert isinstance(geojson, JobData)
        assert isinstance(geojson.id, UUID)
        assert geojson.content_type == "application/json"
        assert geojson.content is None
    assert isinstance(job.cim_data, JobData)
    assert isinstance(job.cim_data.id, UUID)
    assert job.cim_data.content_type == "application/json"
    assert job.cim_data.content is None
