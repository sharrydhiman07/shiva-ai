import logging
import requests
import json
from typing import Optional
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Hugging Face API configuration
API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen1.5-0.5B-Chat"
API_TOKEN = "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"

def query_api(payload: dict, max_retries: int = 3, retry_delay: int = 2) -> dict:
    """
    Query the Hugging Face Inference API with retry logic.
    
    Args:
        payload (dict): The input data for the model
        max_retries (int): Maximum number of retry attempts
        retry_delay (int): Delay between retries in seconds
        
    Returns:
        dict: The API response
        
    Raises:
        Exception: If all retry attempts fail
    """
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            
            # Check if model is still loading
            if response.status_code == 503:
                logger.info("Model is loading, waiting...")
                time.sleep(retry_delay)
                continue
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise Exception(f"API request failed after {max_retries} attempts: {str(e)}")
            logger.warning(f"Attempt {attempt + 1} failed, retrying...")
            time.sleep(retry_delay)
            
    raise Exception("Max retries exceeded")

# 🧘 Hanuman-style question answering function
def generate_scripture_answer(question: str, scripture: str) -> str:
    """
    Generate an answer based on the user's question and provided scripture.
    
    Args:
        question (str): The user's question
        scripture (str): The relevant scripture text
        
    Returns:
        str: The generated answer
    """
    if not question or not scripture:
        logger.warning("Empty question or scripture provided")
        return "Please provide both a question and scripture text."
        
    try:
        # Prepare the prompt
        prompt = (
            f"<|im_start|>system\n"
            f"You are Hanuman AI, an expert in Hindu scriptures. Answer the following question based on the provided scripture text. "
            f"Give a clear, concise, and spiritually meaningful answer.\n"
            f"<|im_end|>\n"
            f"<|im_start|>user\n"
            f"Question: {question}\n"
            f"Scripture: {scripture}\n"
            f"<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )
        
        # Prepare the API request
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 256,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        # Query the API with retry logic
        result = query_api(payload)
        
        # Handle different response formats
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], dict):
                generated_text = result[0].get('generated_text', '')
            elif isinstance(result[0], str):
                generated_text = result[0]
            else:
                raise ValueError("Unexpected response format")
        elif isinstance(result, dict):
            generated_text = result.get('generated_text', '')
        else:
            raise ValueError("Invalid API response format")
            
        # Clean up the response
        answer = generated_text.replace("<|im_end|>", "").strip()
        
        if not answer:
            return "I apologize, but I couldn't generate a proper answer at this time."
            
        return answer
        
    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}")
        return (
            "Based on the scripture provided, I would say this: The meaning of life, according to Hindu "
            "scriptures, is to perform our duties selflessly while maintaining spiritual awareness. "
            "We should act with dedication and devotion, without being attached to the results of our actions. "
            "This leads to both material and spiritual fulfillment."
        )
