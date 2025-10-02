"""Test module for result model."""

from datetime import UTC, datetime
from uuid import UUID

import pytest

from nrl_sdk_lib.models import (
    Result,
    ResultStage,
    ResultStatus,
    ResultType,
)


@pytest.fixture
def anyio_backend() -> str:
    """Use the asyncio backend for the anyio fixture."""
    return "asyncio"


@pytest.mark.anyio
async def test_result_model_without_errors() -> None:
    """Should create a valid result object."""
    result_data = {
        "status": "success",
        "job_id": "cd0d49f7-c19d-432c-bc8d-bb9c2bd0f325",
        "batch_number": 1,
        "id": "764eff66-2b4b-4283-819f-c7f7cd245a13",
    }

    result = Result.model_validate(result_data)
    assert result.status == ResultStatus.SUCCESS
    assert result.stage is None
    assert result.job_id == UUID("cd0d49f7-c19d-432c-bc8d-bb9c2bd0f325")
    assert result.batch_number == 1
    assert result.type is None
    assert result.errors == []
    assert result.id == UUID("764eff66-2b4b-4283-819f-c7f7cd245a13")
    assert result.start_processing_at is None
    assert result.finished_processing_at is None


@pytest.mark.anyio
async def test_result_model_with_errors() -> None:
    """Should create a valid result object with errors."""
    result_data = {
        "status": "failure",
        "stage": 2,
        "job_id": "e4000512-fa93-4a35-882b-c665a8150a1d",
        "batch_number": 1,
        "type": "ValidationException",
        "errors": [
            {
                "reason": "Invalid data format",
                "komponent_id": "4e2baa5f-80ea-4376-acbd-095054825d11",
            },
            {
                "reason": "Missing required field",
                "komponent_id": "4e2baa5f-80ea-4376-acbd-095054825d11",
            },
        ],
        "start_processing_at": datetime(2023, 10, 1, 12, 0, 0, tzinfo=UTC),
        "finished_processing_at": datetime(2023, 10, 1, 13, 0, 0, tzinfo=UTC),
        "id": "1479de31-ed05-4461-8333-becd76a2254a",
    }

    result = Result.model_validate(result_data)
    assert result.status == ResultStatus.FAILURE
    assert result.type == ResultType.VALIDATION_EXCEPTION
    assert result.stage == ResultStage.OWNERSHIP
    assert result.job_id == UUID("e4000512-fa93-4a35-882b-c665a8150a1d")
    assert result.batch_number == 1
    assert result.errors is not None
    assert len(result.errors) == 2
    assert result.errors[0].reason == "Invalid data format"
    assert result.errors[0].komponent_id == UUID("4e2baa5f-80ea-4376-acbd-095054825d11")
    assert result.errors[1].reason == "Missing required field"
    assert result.errors[1].komponent_id == UUID("4e2baa5f-80ea-4376-acbd-095054825d11")
    # Check the ID
    assert result.id == UUID("1479de31-ed05-4461-8333-becd76a2254a")
    assert result.start_processing_at is not None
    assert result.start_processing_at == datetime(2023, 10, 1, 12, 0, 0, tzinfo=UTC)
    assert result.finished_processing_at is not None
    assert result.finished_processing_at == datetime(2023, 10, 1, 13, 0, 0, tzinfo=UTC)
