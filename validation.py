from pathlib import Path

REQUIRED = ['name', 'location', 'price', 'property_type', 'contact']

def validate_details(data):
    missing = [key for key in REQUIRED if not str(data.get(key, '')).strip()]
    if missing:
        raise ValueError('Please fill in: ' + ', '.join(missing))
    features = [x.strip() for x in data.get('features', []) if str(x).strip()]
    if not features:
        raise ValueError('Add at least one property feature so the video has useful content.')
    return features

def validate_images(files):
    valid = [Path(x) for x in files if Path(x).exists()]
    if len(valid) < 4:
        raise ValueError(f'Upload at least 4 images. Currently available: {len(valid)}.')
    return valid
