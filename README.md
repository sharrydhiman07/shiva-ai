🕉️ SHIVA AI – Divine Hindu Scripture Q&A Bot
Shiva AI is a divine voice assistant that answers spiritual and philosophical questions using Hindu scriptures like the Bhagavad Gita. It uses LLMs for interpretation, Hindi translation, and voice synthesis for delivering answers in a deep, godly tone inspired by Lord Shiva.

🔮 Features
🧠 Scripture Q&A – Get contextual answers from Hindu texts like Bhagavad Gita.

📜 Dynamic Verse Fetching – Matches user question to relevant Sanskrit shloka with translation.

🗣️ Hindi TTS Voice – Generates deep, divine voice responses using Hugging Face TTS + gTTS fallback.

🌐 LLM-Powered Answers – Uses Qwen 0.5B Chat via Hugging Face Inference API.

💬 English-to-Hindi Translator – Converts generated text to Hindi via MarianMT.

🎧 Background Music – Shiva Tandav plays in the background with custom volume/player.

🌌 Streamlit UI – Fully responsive frontend with animated theme and audio support.

📁 File Structure
File	Purpose
main.py	Streamlit frontend with question input, audio output, and custom UI
scraper.py	Fetches relevant Bhagavad Gita verse based on user's question
llm_engine.py	Sends prompt to LLM (Qwen) and returns generated response
translator.py	Translates English answers into Hindi using Helsinki-NLP
voice.py	Converts Hindi text to audio using TTS API or gTTS fallback
Shiv Tandav Stotram.mp3	Background music loaded and controlled in the app
requirements.txt	Python dependencies to install via pip

🚀 Setup Instructions
Clone the repo


git clone https://github.com/your-username/shiva-ai.git
cd shiva-ai
Install dependencies


pip install -r requirements.txt
Run the app


streamlit run main.py
Optional: Add your HuggingFace token
Replace the placeholder API_TOKEN in llm_engine.py, translator.py, and voice.py with your token.

🎯 Use Cases
Ask questions like:

What is the purpose of life?

How to deal with suffering?

What is karma?

You'll get:

Sanskrit verse + English meaning

AI-generated spiritual interpretation

Divine Hindi voice audio response

🧘 Inspired By
This project is a tribute to Lord Shiva and the spiritual depth of Indian scriptures. Designed to blend ancient wisdom with modern AI.