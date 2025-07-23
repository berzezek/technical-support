from dadata import Dadata
from app.config import settings


dadata = Dadata(settings.DADATA_TOKEN)
result = dadata.suggest(
    "address", "москва хабар", 
    locations_boost=[{
        "kladr_id": "78"
    }])