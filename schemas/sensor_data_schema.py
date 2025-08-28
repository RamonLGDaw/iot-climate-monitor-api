from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from datetime import datetime


class SensorDataSchemaCreate(BaseModel):
    temp: float = Field(le=100, ge=-20)
    hum: float = Field(ge=0, le=100)

    model_config = ConfigDict( 
        allow_inf_nan=False,
        json_schema_extra={
            "example": {
                "temp":25,
                "hum":50
                }}
        )
   

class SensorDataSchemaRead(BaseModel):
    id: int
    temp: float = Field(le=100, ge=-20)
    hum: float = Field(ge=0, le=100)
    created_at: AwareDatetime

    model_config = ConfigDict(from_attributes=True,  allow_inf_nan=False)