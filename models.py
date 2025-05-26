from pydantic import BaseModel
from typing import Optional, List

class OrderRequest(BaseModel):
    order_id: Optional[str]
    customer: str
    items: List[str]
