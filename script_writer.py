"""Fact-grounded promotional copy generation; no unsupported property claims."""
from dataclasses import dataclass
from typing import List

@dataclass
class PropertyDetails:
    name: str
    location: str
    price: str
    property_type: str
    features: List[str]
    contact: str


def build_scenes(p: PropertyDetails):
    """Create short scenes using only user-provided facts."""
    features = [x.strip() for x in p.features if x and x.strip()]
    scenes = [{
        "title": p.name,
        "caption": f"{p.property_type} | {p.location}",
        "voiceover": f"Discover {p.name}, a {p.property_type} in {p.location}.",
    }]
    for feature in features[:5]:
        scenes.append({"title": feature, "caption": feature,
                       "voiceover": f"A featured highlight: {feature}."})
    scenes.append({"title": p.price, "caption": f"Enquire: {p.contact}",
                   "voiceover": f"Listed at {p.price}. For enquiries, contact {p.contact}."})
    return scenes


def build_full_script(p: PropertyDetails) -> str:
    return "\n".join(s["voiceover"] for s in build_scenes(p))
