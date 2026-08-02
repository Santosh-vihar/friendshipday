import streamlit as st
from pathlib import Path


def load_css():
    css_file = Path(__file__).parent.parent / "styles" / "style.css"
    if css_file.exists():
        with open(css_file, encoding="utf-8") as file_handle:
            st.markdown(f"<style>{file_handle.read()}</style>", unsafe_allow_html=True)
    st.markdown(
        '<link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600&family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">',
        unsafe_allow_html=True,
    )


def landing_header():
    st.markdown(
        '<div class="landing-header"><h1 class="title">Happy Friendship Day</h1><p class="subtitle">Celebrate the bond of friendship with <span class="highlight">Vihar</span></p></div>',
        unsafe_allow_html=True,
    )


def show_balloons_html():
    balloons_html = "".join(
        [f'<div class="balloon" style="left: {index * 12}%; animation-delay: {index * 0.3}s;"></div>' for index in range(8)]
    )
    st.markdown(f'<div class="balloon-container">{balloons_html}</div>', unsafe_allow_html=True)


def show_confetti():
    st.markdown(
        '<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script><script>setTimeout(() => { confetti({ particleCount: 200, spread: 80, origin: { y: 0.5 } }); }, 500);</script>',
        unsafe_allow_html=True,
    )


def photo_question_ui():
    st.markdown(f"## Hi {st.session_state.first_name}!")
    st.markdown("### Do you have memorable photos with Vihar?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes", use_container_width=True, key="btn_yes"):
            st.session_state.photo_choice = True
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("No", use_container_width=True, key="btn_no"):
            st.session_state.photo_choice = False
            st.session_state.step = 4
            st.rerun()


def celebration_page(name):
    show_balloons_html()
    show_confetti()
    st.balloons()
    st.markdown(
        f'<div class="celebration-card"><h1>Happy Friendship Day, {name}</h1><div class="hearts-container"><span class="floating-heart">❤️</span><span class="floating-heart">💖</span><span class="floating-heart">💕</span><span class="floating-heart">💝</span><span class="floating-heart">💗</span></div><p class="quote">"True friendship isn't about being inseparable. It's about being apart and nothing changes."</p><p class="author">- Unknown</p></div>',
        unsafe_allow_html=True,
    )


def video_preview_page(name, video_path):
    show_confetti()
    st.balloons()
    st.markdown(f"## Your Friendship Day Video, {name}!")
    st.video(video_path)
    with open(video_path, "rb") as file_handle:
        video_bytes = file_handle.read()
    st.download_button(
        label="Download Video",
        data=video_bytes,
        file_name=f"Friendship_Day_{name.replace(' ', '_')}.mp4",
        mime="video/mp4",
        use_container_width=True,
    )
    st.success("Thank you for celebrating with Vihar!")


def welcome_back_page(name):
    show_balloons_html()
    show_confetti()
    st.balloons()
    st.markdown(
        f'<div class="welcome-back-card"><h1>Welcome back, {name}!</h1><p class="welcome-msg">You are already a friend of Vihar and have already celebrated Friendship Day here.</p><p class="friend-emoji">❤️✨💫</p></div>',
        unsafe_allow_html=True,
    )
