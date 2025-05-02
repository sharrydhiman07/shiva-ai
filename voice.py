import logging
import requests
import os
import time
from typing import Optional
from gtts import gTTS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Hugging Face TTS API configuration - Using a deep male voice model
API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-hin"
API_TOKEN = "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"

def query_api(payload: dict, max_retries: int = 3, retry_delay: int = 2) -> Optional[bytes]:
    """
    Query the Hugging Face Inference API with retry logic.
    
    Args:
        payload (dict): The input data for the model
        max_retries (int): Maximum number of retry attempts
        retry_delay (int): Delay between retries in seconds
        
    Returns:
        Optional[bytes]: The audio data if successful, None if failed
    """
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Add voice parameters for a deep, resonant, divine voice
    payload["parameters"] = {
        "speaker_embeddings": None,  # Use default male voice
        "speed": 0.75,  # Slower for divine gravitas
        "pitch": 0.8,   # Deeper voice for Shiva-like presence
        "energy": 1.2   # More powerful voice
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            
            # Check if model is still loading
            if response.status_code == 503:
                logger.info("Divine voice is manifesting, please wait...")
                time.sleep(retry_delay)
                continue
                
            response.raise_for_status()
            return response.content
            
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                logger.error(f"Divine voice manifestation failed after {max_retries} attempts: {str(e)}")
                return None
            logger.warning(f"Divine voice attempt {attempt + 1} failed, retrying...")
            time.sleep(retry_delay)
    
    return None

def use_gtts_fallback(hindi_text: str, out_path: str) -> bool:
    """
    Use Google Text-to-Speech as a fallback TTS engine.
    
    Args:
        hindi_text (str): The Hindi text to convert to speech
        out_path (str): Path to save the audio file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Use slower speech rate for divine presence
        tts = gTTS(text=hindi_text, lang='hi', slow=True)
        tts.save(out_path)
        return True
    except Exception as e:
        logger.error(f"Fallback voice manifestation failed: {str(e)}")
        return False

def text_to_speech(hindi_text: str, out_path: str = "output.wav") -> str:
    """
    Convert Hindi text to divine speech using multiple TTS engines.
    
    Args:
        hindi_text (str): The Hindi text to convert to speech
        out_path (str): Path to save the audio file
        
    Returns:
        str: Path to the generated audio file or error message
    """
    if not hindi_text or not isinstance(hindi_text, str):
        logger.warning("Invalid input for divine voice")
        return "TTS failed: Invalid input text"
        
    try:
        # Add sacred pauses and Om
        hindi_text_with_pauses = f"ॐ {hindi_text.replace('।', '। ॐ').replace('॥', '॥ ॐ')}"
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        
        # Try primary TTS service (Hugging Face)
        logger.info("Manifesting divine voice...")
        payload = {
            "inputs": hindi_text_with_pauses
        }
        
        audio_data = query_api(payload)
        
        if audio_data:
            # Save the audio file
            with open(out_path, "wb") as f:
                f.write(audio_data)
                
            if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                logger.info("Divine voice successfully manifested")
                return out_path
        
        # Try fallback TTS service (gTTS)
        logger.info("Primary manifestation failed, attempting alternate path...")
        if use_gtts_fallback(hindi_text_with_pauses, out_path):
            logger.info("Divine voice manifested through alternate path")
            return out_path
            
        logger.error("Divine voice manifestation failed")
        return "TTS failed: Service unavailable"
        
    except Exception as e:
        logger.error(f"Divine voice error: {str(e)}")
        return "TTS failed: Please try again"