# PropMotion AI — AI Property Video Generator

A runnable Streamlit application and CLI that turns real-estate listing details plus 4–8 photos into a vertical MP4 promotional video. It creates an opening scene, feature scenes, and a closing enquiry scene, with readable captions, subtle zoom motion, and cross-fade transitions.

## Features
- Streamlit form for property name, location, price, property type, features, CTA, and image upload.
- 9:16 portrait MP4 export (540 × 960, 15 FPS).
- Deterministic, fact-grounded voice-over script and on-screen captions.
- Handles missing details, fewer than four images, unreadable images, and video-writer failures with clear errors.
- CLI for repeatable generation and a unit test for copy generation.

## Quick start

**Requirements:** Python 3.10+ and FFmpeg available to OpenCV on your operating system.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit, enter listing details, upload 4–8 images, and click **Generate property video**. Preview the result and download the MP4.

## CLI

```bash
python cli.py --images assets/sample_property --output output/sample.mp4 \
  --name "The Cedar Residence" --location "New Town, Kolkata" \
  --price "INR 82 lakh" --type "2 BHK Apartment" \
  --features "2 bedrooms|Modular kitchen|Balcony|Covered parking" \
  --contact "Call +91 98765 43210"
```

## Sample data and output
- `assets/sample_property/`: six synthetic illustrative property images (not a real listing).
- `sample_data.json`: example property input.
- `output/sample_property_promo.mp4`: generated demo video.
- `output/sample_voiceover.txt`: generated script.

## Architecture
1. `app.py` collects and validates user input.
2. `validation.py` checks required fields and image count/readability.
3. `script_writer.py` maps supplied facts to a fixed scene structure. It does not invent amenities, distances, legal status, or investment claims.
4. `video_engine.py` resizes images, applies a slow zoom, draws high-contrast text overlays, adds cross-fades, and writes MP4 using OpenCV.
5. `cli.py` exposes the same renderer without the UI.

## AI/model and external services disclosure
This prototype intentionally uses **template-based content generation**, not a hosted LLM or paid API. The brief explicitly permits a justified rule-based approach. This design makes every factual claim traceable to the submitted property details and avoids hallucinated amenities. Libraries: Streamlit, OpenCV, Pillow, NumPy. No external API, customer database, or credentials are required.

## Validation and tests
```bash
python -m pytest -q
```
The sample video is generated using synthetic illustrative assets. Replace them with authorized property photos before using the app for a real listing.

## Limitations and next steps
- Current narration is supplied as a voice-over script; speech audio is not synthesized.
- Background music is not bundled, avoiding copyright/licensing issues.
- The renderer uses a fixed 9:16 social-video layout and English copy templates.
- A production version could add licensed TTS, multilingual templates, brand presets, and a queue for batch rendering.

## Responsible use
Use only photos and contact details you are authorized to publish. The app does not verify property ownership, pricing, legal approvals, or the accuracy of the supplied listing information.
