from pydantic import BaseModel, Field
from typing import List, Optional
from .freight_rate_summary import FreightRateSummary
from .fuel_price_trend import FuelPriceTrend
from .operational_update import OperationalUpdate
from .geopolitical_impact import GeopoliticalImpact

class MarketAnalysis(BaseModel):
    """Model data terstruktur untuk hasil analisis pasar."""
    freight_rates: List[FreightRateSummary]
    fuel_trends: List[FuelPriceTrend]
    operational_updates: List[OperationalUpdate]
    geopolitical_impacts: List[GeopoliticalImpact]