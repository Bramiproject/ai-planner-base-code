from pydantic import BaseModel, Field
from typing import List, Optional

class FreightRateSummary(BaseModel):
    """Ringkasan data untuk tarif pengiriman."""
    index_name: str = Field(description="Nama indeks, cth: SCFI atau Drewry")
    change_description: str = Field(description="Deskripsi perubahan tarif, termasuk persentase jika ada.")
    source: str = Field(description="Sumber data untuk indeks ini.")