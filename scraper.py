import logging
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pre-loaded Bhagavad Gita verses for common life questions
GITA_VERSES = {
    "life": [
        {
            "verse": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन।\nमा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि॥",
            "translation": "You have a right to perform your prescribed duties, but you are not entitled to the fruits of your actions. Never consider yourself to be the cause of the results of your activities, nor be attached to inaction.",
            "chapter": 2,
            "verse_number": 47
        },
        {
            "verse": "योगस्थः कुरु कर्माणि सङ्गं त्यक्त्वा धनञ्जय।\nसिद्ध्यसिद्ध्योः समो भूत्वा समत्वं योग उच्यते॥",
            "translation": "Perform your duty equipoised, O Arjuna, abandoning all attachment to success or failure. Such equanimity is called yoga.",
            "chapter": 2,
            "verse_number": 48
        }
    ],
    "purpose": [
        {
            "verse": "श्रेयान्स्वधर्मो विगुणः परधर्मात्स्वनुष्ठितात्।\nस्वधर्मे निधनं श्रेयः परधर्मो भयावहः॥",
            "translation": "It is better to perform one's own duties imperfectly than to master the duties of another. By fulfilling the obligations he is born with, a person never comes to grief.",
            "chapter": 3,
            "verse_number": 35
        }
    ],
    "happiness": [
        {
            "verse": "सुखदुःखे समे कृत्वा लाभालाभौ जयाजयौ।\nततो युद्धाय युज्यस्व नैवं पापमवाप्स्यसि॥",
            "translation": "Fight for the sake of duty, treating alike happiness and distress, loss and gain, victory and defeat. Fulfilling your responsibility in this way, you will never incur sin.",
            "chapter": 2,
            "verse_number": 38
        }
    ],
    "default": [
        {
            "verse": "यदा यदा हि धर्मस्य ग्लानिर्भवति भारत।\nअभ्युत्थानमधर्मस्य तदात्मानं सृजाम्यहम्॥",
            "translation": "Whenever there is a decline in righteousness and an increase in unrighteousness, O Arjuna, at that time I manifest myself on earth.",
            "chapter": 4,
            "verse_number": 7
        }
    ]
}

def get_relevant_category(question: str) -> str:
    """
    Determine the most relevant category based on the question.
    
    Args:
        question (str): The user's question
        
    Returns:
        str: The relevant category key
    """
    question = question.lower()
    if any(word in question for word in ["life", "live", "living", "exist", "existence"]):
        return "life"
    elif any(word in question for word in ["purpose", "goal", "meaning", "why"]):
        return "purpose"
    elif any(word in question for word in ["happy", "happiness", "joy", "peace"]):
        return "happiness"
    return "default"

def fetch_scripture(question: str) -> str:
    """
    Fetch relevant scripture based on the user's question.
    
    Args:
        question (str): The user's question
        
    Returns:
        str: The relevant scripture with translation
    """
    try:
        # Get relevant category
        category = get_relevant_category(question)
        verses = GITA_VERSES.get(category, GITA_VERSES["default"])
        
        # Select a random verse from the category
        selected_verse = random.choice(verses)
        
        # Format the response
        response = (
            f"Bhagavad Gita Chapter {selected_verse['chapter']}, "
            f"Verse {selected_verse['verse_number']}\n\n"
            f"Sanskrit:\n{selected_verse['verse']}\n\n"
            f"Translation:\n{selected_verse['translation']}"
        )
        
        logger.info(f"Successfully fetched scripture for category: {category}")
        return response
        
    except Exception as e:
        logger.error(f"Error fetching scripture: {str(e)}")
        # Return a default verse if something goes wrong
        default_verse = GITA_VERSES["default"][0]
        return (
            f"Bhagavad Gita Chapter {default_verse['chapter']}, "
            f"Verse {default_verse['verse_number']}\n\n"
            f"Sanskrit:\n{default_verse['verse']}\n\n"
            f"Translation:\n{default_verse['translation']}"
        )