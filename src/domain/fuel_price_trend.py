from pydantic import BaseModel, Field
from typing import List, Optional

class FuelPriceTrend(BaseModel):
    """Ringkasan data untuk tren harga bahan bakar."""
    fuel_type: str = Field(description="Jenis bahan bakar, cth: VLSFO.")
    price_change_description: str = Field(description="Deskripsi pergerakan harga, cth: naik $15/MT.")
    average_price: str = Field(description="Harga rata-rata di pelabuhan utama, cth: $680/MT di Singapura.")
    source: str = Field(description="Sumber data, biasanya Ship & Bunker.")