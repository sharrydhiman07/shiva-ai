import logging
import streamlit as st
from scraper import fetch_scripture
from llm_engine import generate_scripture_answer
from translator import translate_to_hindi
from voice import text_to_speech
import base64
import pathlib

# Set page config - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="SHIVA AI – Divine Wisdom",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize session state for background music
if 'bg_music_volume' not in st.session_state:
    st.session_state.bg_music_volume = 0.3  # Default volume (30%)

# Custom CSS for divine Shiva theme
st.markdown("""
    <style>
    /* Overall theme */
    .main {
        background: linear-gradient(to bottom, #0a192f, #1a1a2e);
        background-image: url('https://raw.githubusercontent.com/sharran-murali/shiva-ai/main/om.png');
        background-repeat: repeat;
        background-size: 200px;
        background-opacity: 0.1;
    }
    
    /* Title and text styling */
    h1 {
        color: #e0e0ff !important;
        text-align: center;
        font-family: 'Sanskrit Text', serif !important;
        text-shadow: 0 0 10px #4a90e2, 0 0 20px #4a90e2, 0 0 30px #4a90e2;
        margin-bottom: 2rem !important;
    }
    
    p {
        color: #b6b6ff !important;
        text-align: center;
        font-size: 1.2em !important;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #000428, #004e92);
        color: white;
        border-radius: 20px;
        height: 3em;
        font-size: 1.1em;
        border: 2px solid #4a90e2;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #004e92, #000428);
        border-color: #87ceeb;
        box-shadow: 0 0 15px #4a90e2;
    }
    
    /* Input field styling */
    .stTextInput>div>div>input {
        font-size: 1.1em;
        border-radius: 15px;
        border: 2px solid #4a90e2;
        background-color: rgba(10, 25, 47, 0.7);
        color: #e0e0ff !important;
        padding: 1em;
    }
    
    /* Audio player styling */
    audio {
        width: 100%;
        height: 50px;
        border-radius: 25px;
        background: linear-gradient(45deg, #000428, #004e92);
        margin: 20px 0;
        border: 2px solid #4a90e2;
    }
    
    /* Background music player styling */
    .bg-music-player {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: rgba(10, 25, 47, 0.9);
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #4a90e2;
        box-shadow: 0 0 15px rgba(74, 144, 226, 0.3);
        z-index: 1000;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        width: 250px;
    }
    
    .bg-music-title {
        color: #e0e0ff;
        font-size: 0.9em;
        text-align: center;
        margin-bottom: 5px;
        text-shadow: 0 0 5px #4a90e2;
    }
    
    .volume-control {
        display: flex;
        align-items: center;
        gap: 10px;
        width: 100%;
        padding: 5px;
        background: rgba(10, 25, 47, 0.5);
        border-radius: 10px;
    }
    
    .volume-icon {
        color: #e0e0ff;
        cursor: pointer;
        font-size: 1.2em;
        width: 24px;
        text-align: center;
    }
    
    .volume-slider {
        flex-grow: 1;
        height: 5px;
        -webkit-appearance: none;
        background: linear-gradient(to right, #4a90e2 var(--volume), #1a1a2e var(--volume));
        border-radius: 5px;
        outline: none;
    }
    
    .volume-slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        width: 15px;
        height: 15px;
        background: #e0e0ff;
        border-radius: 50%;
        cursor: pointer;
        border: 2px solid #4a90e2;
        box-shadow: 0 0 5px #4a90e2;
    }
    
    .volume-value {
        color: #e0e0ff;
        min-width: 40px;
        text-align: right;
        font-size: 0.9em;
    }
    
    .play-pause-btn {
        background: none;
        border: none;
        color: #e0e0ff;
        cursor: pointer;
        font-size: 1.5em;
        padding: 5px;
        transition: all 0.3s ease;
    }
    
    .play-pause-btn:hover {
        text-shadow: 0 0 10px #4a90e2;
    }
    
    /* Shiva icon animation */
    @keyframes divine-glow {
        0% { filter: drop-shadow(0 0 5px #4a90e2); }
        50% { filter: drop-shadow(0 0 25px #4a90e2); }
        100% { filter: drop-shadow(0 0 5px #4a90e2); }
    }
    .shiva-icon {
        animation: divine-glow 3s infinite;
        margin: 20px auto;
        display: block;
    }
    
    /* Loading spinner */
    .stSpinner {
        color: #4a90e2 !important;
    }
    
    /* Custom container for centered content */
    .divine-container {
        background: rgba(10, 25, 47, 0.7);
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid #4a90e2;
        box-shadow: 0 0 20px rgba(74, 144, 226, 0.3);
        margin: 2rem auto;
        max-width: 800px;
    }
    </style>
    """, unsafe_allow_html=True)

# Convert audio file to base64
audio_file = pathlib.Path("D:/ai_website/Shiv Tandav Stotram.mp3").read_bytes()
audio_base64 = base64.b64encode(audio_file).decode()

# Background Music Player with base64 encoded audio
bg_music_html = f"""
<div class="bg-music-player" id="bgMusicPlayer">
    <div class="bg-music-title">
        🔱 शिव तांडव स्तोत्रम् 🔱
    </div>
    <audio id="bg-music" loop>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
    </audio>
    <div class="volume-control">
        <button class="play-pause-btn" id="playPauseBtn" title="Play/Pause">▶️</button>
        <span class="volume-icon" id="volumeIcon" title="Mute/Unmute">🔊</span>
        <input type="range" id="volume-slider" class="volume-slider" 
               min="0" max="100" value="{int(st.session_state.bg_music_volume * 100)}"
               style="--volume: {st.session_state.bg_music_volume * 100}%">
        <span class="volume-value" id="volumeValue">{int(st.session_state.bg_music_volume * 100)}%</span>
    </div>
</div>

<script>
    const bgMusic = document.getElementById('bg-music');
    const volumeSlider = document.getElementById('volume-slider');
    const volumeIcon = document.getElementById('volumeIcon');
    const volumeValue = document.getElementById('volumeValue');
    const playPauseBtn = document.getElementById('playPauseBtn');
    let isPlaying = false;
    
    // Initialize audio
    bgMusic.volume = {st.session_state.bg_music_volume};
    
    // Function to update volume display
    function updateVolumeDisplay(value) {{
        const percentage = Math.round(value * 100);
        volumeValue.textContent = `${{percentage}}%`;
        volumeSlider.style.setProperty('--volume', `${{percentage}}%`);
        
        // Update volume icon based on level
        if (value === 0) {{
            volumeIcon.textContent = '🔇';
        }} else if (value < 0.3) {{
            volumeIcon.textContent = '🔈';
        }} else if (value < 0.7) {{
            volumeIcon.textContent = '🔉';
        }} else {{
            volumeIcon.textContent = '🔊';
        }}
    }}
    
    // Function to toggle play/pause
    function togglePlayPause() {{
        if (bgMusic.paused) {{
            bgMusic.play();
            playPauseBtn.textContent = '⏸️';
            isPlaying = true;
        }} else {{
            bgMusic.pause();
            playPauseBtn.textContent = '▶️';
            isPlaying = false;
        }}
    }}
    
    // Play/Pause button click handler
    playPauseBtn.addEventListener('click', togglePlayPause);
    
    // Volume slider change handler
    volumeSlider.addEventListener('input', function() {{
        const value = this.value / 100;
        bgMusic.volume = value;
        updateVolumeDisplay(value);
    }});
    
    // Mute/Unmute handler
    let lastVolume = {st.session_state.bg_music_volume};
    volumeIcon.addEventListener('click', function() {{
        if (bgMusic.volume > 0) {{
            lastVolume = bgMusic.volume;
            bgMusic.volume = 0;
            volumeSlider.value = 0;
        }} else {{
            bgMusic.volume = lastVolume;
            volumeSlider.value = lastVolume * 100;
        }}
        updateVolumeDisplay(bgMusic.volume);
    }});
    
    // Keyboard controls
    document.addEventListener('keydown', function(e) {{
        if (e.key === 'ArrowUp' || e.key === 'ArrowRight') {{
            const newVal = Math.min(100, parseInt(volumeSlider.value) + 10);
            volumeSlider.value = newVal;
            bgMusic.volume = newVal / 100;
            updateVolumeDisplay(bgMusic.volume);
        }} else if (e.key === 'ArrowDown' || e.key === 'ArrowLeft') {{
            const newVal = Math.max(0, parseInt(volumeSlider.value) - 10);
            volumeSlider.value = newVal;
            bgMusic.volume = newVal / 100;
            updateVolumeDisplay(bgMusic.volume);
        }} else if (e.key === 'm') {{
            volumeIcon.click();
        }} else if (e.key === ' ') {{
            e.preventDefault();
            togglePlayPause();
        }}
    }});
    
    // Auto-play with user interaction
    document.addEventListener('click', function initAudio() {{
        if (!isPlaying) {{
            togglePlayPause();
            document.removeEventListener('click', initAudio);
        }}
    }}, {{once: true}});
    
    // Update volume display initially
    updateVolumeDisplay({st.session_state.bg_music_volume});
</script>
"""

st.markdown(bg_music_html, unsafe_allow_html=True)

# Create a centered container
st.markdown('<div class="divine-container">', unsafe_allow_html=True)

# Main UI with Shiva icon
st.markdown('''
    <div style="text-align: center;">
        <img src="https://raw.githubusercontent.com/sharran-murali/shiva-ai/main/shiva.png" width="150" class="shiva-icon"/>
        <h1>|| ॐ नमः शिवाय ||<br>SHIVA AI</h1>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("""
    <p>🕉️ Seek divine wisdom through Lord Shiva's grace.<br>
    Ask your question and receive answers through celestial voice.</p>
    """, unsafe_allow_html=True)

# Main input area with divine symbols
user_question = st.text_input(
    "🔱 Your Question (in English):",
    placeholder="What is the true nature of consciousness? What is the path to liberation?",
    key="question_input"
)

if st.button("🕉️ Seek Divine Wisdom", key="ask_button"):
    if not user_question.strip():
        st.warning("🙏 Please enter your question with pure intention.")
    else:
        try:
            with st.spinner("🕉️ Connecting with divine consciousness..."):
                scripture = fetch_scripture(user_question)
                
            with st.spinner("🔱 Channeling Lord Shiva's wisdom..."):
                english_answer = generate_scripture_answer(user_question, scripture)
                
            with st.spinner("📿 Transcending to sacred Sanskrit..."):
                hindi_answer = translate_to_hindi(english_answer)
                
            with st.spinner("🎵 Manifesting divine voice..."):
                audio_path = text_to_speech(hindi_answer)
                
                if not audio_path.startswith("TTS failed"):
                    # Create a container for the audio player
                    audio_container = st.container()
                    with audio_container:
                        try:
                            # Read audio file and autoplay
                            with open(audio_path, "rb") as audio_file:
                                audio_bytes = audio_file.read()
                                audio_base64 = base64.b64encode(audio_bytes).decode()
                                
                                # Custom audio player with autoplay
                                st.markdown(
                                    f'<audio autoplay controls><source src="data:audio/wav;base64,{audio_base64}" type="audio/wav"></audio>',
                                    unsafe_allow_html=True
                                )
                        except Exception as e:
                            logger.error(f"Error playing audio: {str(e)}")
                            st.error("🕉️ Divine message could not manifest. Please try again with pure intention.")
                else:
                    st.error("🕉️ Divine voice could not manifest. Please try again with pure intention.")
                    
        except Exception as e:
            logger.error(f"Unexpected error in main flow: {str(e)}")
            st.error("🕉️ An unexpected disturbance occurred. Please center yourself and try again.")

# Close the divine container
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; padding: 20px; color: #4a90e2;">
        || हर हर महादेव ||
    </div>
    """, unsafe_allow_html=True)