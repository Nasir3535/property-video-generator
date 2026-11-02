# 90-second evaluator demo

1. **Problem (10 sec):** A property sales team repeats the same editing work for every listing. PropMotion turns the listing facts and photos into a vertical social video.
2. **Input (20 sec):** Open the Streamlit app, enter the property name, location, price, type, features and enquiry CTA. Upload the six sample photos.
3. **Generate (20 sec):** Click **Generate property video**. The app validates required fields and image count, builds a fact-grounded scene script, then renders the MP4 with motion, overlays and transitions.
4. **Output (20 sec):** Preview the video, download the MP4, and expand the voice-over script. Show the included `output/sample_property_promo.mp4` as a pre-generated example.
5. **Engineering decisions (15 sec):** The brief permits template logic. This version uses deterministic templates rather than an external LLM, so every claim comes from the submitted facts. It also avoids API keys and paid services.
6. **Limitations (5 sec):** Voice-over is supplied as a script rather than synthesized audio; music and multilingual copy are future extensions.

## Suggested evaluator test
Try uploading only two images. The app should show a clear validation message rather than crash. Then upload four or more images and generate the video.
