from pydantic import (
    BaseModel,
    Field,
)

class BuyInData(BaseModel):
    total_cost: float = Field(default=0.0)
    total_quantity: float = Field(default=0.0)
    net_option_premiums: float = Field(default=0.0)
    total_dividends: float = Field(default=0.0)