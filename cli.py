"""CLI example: python cli.py --images assets/sample_property --output output/sample.mp4"""
import argparse
from pathlib import Path
from script_writer import PropertyDetails
from video_engine import render_video

p=argparse.ArgumentParser(description='Generate a property promo MP4')
p.add_argument('--images',required=True,help='Folder containing 4–8 image files')
p.add_argument('--output',default='output/property_promo.mp4')
p.add_argument('--name',default='The Cedar Residence')
p.add_argument('--location',default='New Town, Kolkata')
p.add_argument('--price',default='₹82 lakh')
p.add_argument('--type',dest='property_type',default='2 BHK Apartment')
p.add_argument('--features',default='2 bedrooms|Modular kitchen|Balcony|Covered parking|24-hour security')
p.add_argument('--contact',default='Call +91 98765 43210')
a=p.parse_args()
imgs=sorted([str(x) for x in Path(a.images).glob('*') if x.suffix.lower() in ['.jpg','.jpeg','.png','.webp']])
d=PropertyDetails(a.name,a.location,a.price,a.property_type,a.features.split('|'),a.contact)
print('Saved:',render_video(imgs,d,a.output))
