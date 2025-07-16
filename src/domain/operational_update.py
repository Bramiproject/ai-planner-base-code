from pydantic import BaseModel, Field
from typing import List, Optional

class OperationalUpdate(BaseModel):
    """Ringkasan data untuk pembaruan operasional."""
    location: str = Field(description="Lokasi terdampak, cth: Pelabuhan Hamburg.")
    update_description: str = Field(description="Deskripsi gangguan, cth: kemacetan atau penundaan.")
    source: str = Field(description="Sumber informasi, cth: Hapag-Lloyd atau MarineTraffic.")