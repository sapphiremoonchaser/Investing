from pydantic import (
    BaseModel,
    Field,
)

class SymbolResult(BaseModel):
    profit: float = Field(default=0.0)
    stock_qty: float = Field(default=0.0)
    option_qty: float = Field(default=0.0)