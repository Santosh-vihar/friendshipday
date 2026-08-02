"""Friendship Day Celebration App for Vihar."""

import shutil
import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))

from modules.database import check_visitor, init_db, save_visitor, update_visitor_video
from modules.helpers import generate_id
from modules.ui import (
    celebration_page,
    landing_header,
    load_css,
    photo_question_ui,
    show_balloons_html,
    show_confetti,
    video_preview_page,
    welcome_back_page,
)
from modules.video_generator import create_slideshow

st.set_page_config(
    page_title="Friendship Day - Vihar",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_css()
init_db()

defaults = {
    "step": 1,
    "first_name": "",
    "surname": "",
    "full_name": "",
    "existing_user": False,
    "photo_choice": None,
    "uploaded_photos": [],
    "video_path": None,
    "generation_done": False,
}
for key, value in defaults.items():
    st.session_state.setdefault(key, value)

if st.session_state.step == 1 and not st.session_state.existing_user:
    landing_header()
    show_balloons_html()
    show_confetti()

    with st.container():
        _, col2, _ = st.columns([1, 2, 1])
        with col2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("## Enter Your Name")
            with st.form("name_form"):
                first = st.text_input("First Name", placeholder="e.g., Rahul")
                surname = st.text_input("Surname", placeholder="e.g., Sharma")
                submitted = st.form_submit_button("Celebrate Now")

                if submitted:
                    if not first.strip() or not surname.strip():
                        st.error("Please enter both your first name and surname.")
                    else:
                        first_name = first.strip().title()
                        surname_value = surname.strip().title()
                        full_name = f"{first_name} {surname_value}"
                        exists, _ = check_visitor(first_name, surname_value)

                        if exists:
                            st.session_state.existing_user = True
                            st.session_state.full_name = full_name
                            st.session_state.first_name = first_name
                            st.session_state.surname = surname_value
                            st.rerun()
                        else:
                            save_visitor(
                                first_name,
                                surname_value,
                                full_name,
                                datetime.now().isoformat(),
                                False,
                                "",
                            )
                            st.session_state.first_name = first_name
                            st.session_state.surname = surname_value
                            st.session_state.full_name = full_name
                            st.session_state.step = 2
                            st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.existing_user:
    welcome_back_page(st.session_state.full_name)
    st.stop()

if st.session_state.step == 2:
    photo_question_ui()

if st.session_state.step == 3:
    st.markdown(f"## Upload Memorable Photos with Vihar, {st.session_state.first_name}")
    st.markdown("### Please upload between 3 and 5 photos (JPG, PNG, JPEG)")

    uploaded = st.file_uploader(
        "Choose photos",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="photo_uploader",
    )

    if uploaded:
        st.session_state.uploaded_photos = uploaded
        count = len(uploaded)
        if count < 3:
            st.warning(f"You have uploaded {count} photo(s). Please upload at least 3.")
        elif count > 5:
            st.warning("You can upload a maximum of 5 photos. Please remove some.")
        else:
            st.success(f"{count} photos uploaded! Ready to create your Friendship Day video.")
            if st.button("Generate My Friendship Day Video", type="primary", use_container_width=True):
                with st.spinner("Creating your beautiful video... This may take a moment."):
                    temp_dir = Path("database/temp_photos") / generate_id()
                    temp_dir.mkdir(parents=True, exist_ok=True)
                    saved_paths = []

                    for index, image_file in enumerate(st.session_state.uploaded_photos):
                        extension = Path(image_file.name).suffix
                        safe_name = f"photo_{index + 1}{extension}"
                        destination = temp_dir / safe_name
                        with open(destination, "wb") as file_handle:
                            file_handle.write(image_file.getbuffer())
                        saved_paths.append(str(destination))

                    output_dir = Path("database/generated_videos")
                    output_dir.mkdir(parents=True, exist_ok=True)
                    video_name = f"{st.session_state.full_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
                    output_path = output_dir / video_name

                    try:
                        create_slideshow(
                            image_paths=saved_paths,
                            name=st.session_state.full_name,
                            output_path=str(output_path),
                        )
                        update_visitor_video(st.session_state.first_name, st.session_state.surname, video_name)
                        st.session_state.video_path = str(output_path)
                        st.session_state.generation_done = True
                        st.session_state.step = 5
                        shutil.rmtree(temp_dir, ignore_errors=True)
                        st.rerun()
                    except Exception as error:
                        st.error(f"An error occurred while generating the video: {error}")
                        shutil.rmtree(temp_dir, ignore_errors=True)

if st.session_state.step == 4:
    celebration_page(st.session_state.full_name)

if st.session_state.step == 5 and st.session_state.video_path:
    video_preview_page(st.session_state.full_name, st.session_state.video_path)
