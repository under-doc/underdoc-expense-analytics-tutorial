from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

class MyExpense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(..., description="The date of the expense")
    expense_type: str = Field(..., description="The type of the expense")
    shop_name: str = Field("", description="The name of the shop")
    shop_address: str = Field("", description="The address of the shop")
    expense_category: str = Field(..., description="The category of the expense")
    currency: str = Field(..., description="The currency of the expense")
    total_amount: float = Field(..., description="The total amount of the expense")
    source_file_name: str = Field("", description="The source file name")
