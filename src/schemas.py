from pydantic import BaseModel, Field, ConfigDict


class ProductCreateSchema(BaseModel):
    name: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)


class ProductUpdateSchema(BaseModel):
    name: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)


class ProductResponseSchema(BaseModel):
    id: int
    name: str
    category: str

    model_config = ConfigDict(
        from_attributes=True,
    )