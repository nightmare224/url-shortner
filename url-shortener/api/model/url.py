from dataclasses import dataclass
from model.shorturl import ShortURL

@dataclass
class FullURL:
    full_url: str

@dataclass
class URL(ShortURL, FullURL):
    pass