from pydantic import BaseModel, Field
from typing import List, Optional

class GeopoliticalImpact(BaseModel):
    """Ringkasan data untuk dampak geopolitik."""
    region: str = Field(description="Wilayah geopolitik yang relevan, cth: Laut Merah.")
    impact_description: str = Field(description="Deskripsi dampak terhadap pengiriman.")
    source: str = Field(description="Sumber berita atau analisis.")