import tempfile
from pathlib import Path
import streamlit as st
from PIL import Image
from script_writer import PropertyDetails, build_full_script
from video_engine import render_video
from validation import validate_details, validate_images

st.set_page_config(page_title='PropMotion AI', page_icon='🏡', layout='wide')
st.markdown('''<style>
.block-container{max-width:1180px;padding-top:2rem} .hero{padding:28px;border-radius:18px;background:linear-gradient(120deg,#14283b,#31536b);color:white;margin-bottom:22px}
.hero h1{font-size:2.35rem;margin:0}.hero p{color:#dbe7ee;margin:8px 0 0}.stButton>button{background:#c58b4b;color:white;border:0;border-radius:9px;padding:.65rem 1.2rem;font-weight:700}
</style>''', unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>PropMotion AI</h1><p>Turn property photos and verified listing details into a share-ready vertical video.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header('How it works')
    st.markdown('1. Add listing details\n2. Upload 4–8 photos\n3. Generate a video\n4. Preview and download MP4')
    st.caption('Copy is generated from supplied facts only. No invented amenities, distances, or guarantees.')

left, right = st.columns([1,1], gap='large')
with left:
    st.subheader('Property details')
    name = st.text_input('Property name', 'The Cedar Residence')
    location = st.text_input('Location', 'New Town, Kolkata')
    price = st.text_input('Price', '₹82 lakh')
    property_type = st.selectbox('Property type', ['2 BHK Apartment','3 BHK Apartment','Villa','Independent House','Studio Apartment','Commercial Space'])
    features_text = st.text_area('Key features (one per line)', '2 bedrooms\nModular kitchen\nBalcony\nCovered parking\n24-hour security', height=140)
    contact = st.text_input('Contact / CTA', 'Call +91 98765 43210')
with right:
    st.subheader('Property photos')
    uploads = st.file_uploader('Upload 4–8 images', type=['jpg','jpeg','png','webp'], accept_multiple_files=True)
    if uploads:
        if len(uploads) > 8: st.warning('Only the first 8 images will be used.')
        cols = st.columns(2)
        for i, f in enumerate(uploads[:8]):
            try:
                cols[i%2].image(f, caption=f.name, use_container_width=True)
            except Exception:
                st.error(f'Could not read {f.name}')
    st.caption('Use photos you own or are authorized to use. Landscape and portrait images are supported.')

if st.button('Generate property video', type='primary', use_container_width=True):
    try:
        data = {'name':name,'location':location,'price':price,'property_type':property_type,'features':[x for x in features_text.splitlines() if x.strip()],'contact':contact}
        features = validate_details(data)
        if not uploads: raise ValueError('Upload at least 4 property images.')
        if len(uploads) > 8: st.info('Using the first 8 uploaded images.')
        with tempfile.TemporaryDirectory() as tmp:
            paths=[]
            for i, f in enumerate(uploads[:8]):
                p=Path(tmp)/f'image_{i+1}{Path(f.name).suffix.lower()}'
                p.write_bytes(f.getvalue())
                # Verify that the uploaded file is a readable image.
                with Image.open(p) as im: im.verify()
                paths.append(str(p))
            validate_images(paths)
            details=PropertyDetails(name.strip(),location.strip(),price.strip(),property_type,features,contact.strip())
            st.info('Creating scenes and rendering your MP4. This can take a minute.')
            out=Path(tmp)/'property_promo.mp4'
            render_video(paths,details,out)
            video_bytes=out.read_bytes()
            st.session_state['video_bytes']=video_bytes
            st.session_state['script']=build_full_script(details)
            st.session_state['video_name']=name.strip().replace(' ','_')+'_promo.mp4'
    except Exception as e:
        st.error(f'Unable to generate video: {e}')

if st.session_state.get('video_bytes'):
    st.divider(); st.subheader('Your property video')
    st.video(st.session_state['video_bytes'])
    st.download_button('Download MP4', st.session_state['video_bytes'], file_name=st.session_state['video_name'], mime='video/mp4', use_container_width=True)
    with st.expander('View generated voice-over script'):
        st.text(st.session_state['script'])

st.caption('Prototype note: the current version uses deterministic, fact-grounded templates rather than an external generative-AI API. This keeps outputs reproducible and prevents unsupported property claims.')
