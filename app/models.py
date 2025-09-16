from enum import Enum


from pydantic import BaseModel as PydBaseModel
from pydantic.alias_generators import to_camel


class BaseModel(PydBaseModel):
    class Config:
        alias_generator = to_camel
        validate_by_name = True


class HealthStatus(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class HealthCheckResponse(BaseModel):
    status: HealthStatus = HealthStatus.UNHEALTHY
