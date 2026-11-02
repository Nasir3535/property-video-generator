import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from script_writer import PropertyDetails, build_scenes

def test_copy_uses_only_provided_facts():
    p=PropertyDetails('Maple Homes','Pune','₹70 lakh','2 BHK Apartment',['Balcony','Parking'],'Call 12345')
    text=' '.join(x['voiceover'] for x in build_scenes(p))
    assert 'Pune' in text and '₹70 lakh' in text and 'Balcony' in text
    assert 'swimming pool' not in text.lower()

def test_scene_count():
    p=PropertyDetails('A','B','C','D',['one','two'],'E')
    assert len(build_scenes(p)) == 4
