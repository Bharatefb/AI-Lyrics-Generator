from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI(
    title="AI Lyrics Generator",
    description="Generate original song lyrics using local Qwen AI",
    version="1.0.0"
)

# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Request Model
# --------------------------------------------------

class LyricsRequest(BaseModel):
    song_name: str
    genre: str = "Pop"
    mood: str = "Happy"
    language: str = "English"
    verses: int = 3


# --------------------------------------------------
# Home Route
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "AI Lyrics Generator API is running",
        "status": "success"
    }


# --------------------------------------------------
# Generate Lyrics
# --------------------------------------------------

@app.post("/generate")
def generate_lyrics(request: LyricsRequest):

    # ----------------------------------------------
    # Language-specific instructions
    # ----------------------------------------------

    language_instruction = ""

    if request.language.lower() == "hindi":

        language_instruction = """
IMPORTANT LANGUAGE REQUIREMENT:

The user selected Hindi.

You MUST write the entire song in Hindi.

Use Devanagari script.

Do NOT write Hindi using English/Roman letters.

Do NOT translate the Hindi lyrics into English.

Do NOT provide an English explanation.

Use natural Hindi vocabulary, grammar, expressions,
rhymes and poetic language.

CORRECT:

"तेरी यादों में खोया सा हूँ
तेरे बिना अधूरा सा हूँ"

INCORRECT:

"Teri yaadon mein khoya sa hoon
Tere bina adhoora sa hoon"

The final lyrics MUST primarily contain Hindi
Devanagari text.
"""

    elif request.language.lower() == "english":

        language_instruction = """
IMPORTANT LANGUAGE REQUIREMENT:

Write the entire song in English.

Do not translate it into another language.
"""

    elif request.language.lower() == "hinglish":

        language_instruction = """
IMPORTANT LANGUAGE REQUIREMENT:

Write the song in natural Hinglish.

Use Hindi words written using English/Roman letters.

Example:

"Teri aankhon mein kuch baat hai
Dil mera tere saath hai"
"""

    else:

        language_instruction = f"""
IMPORTANT LANGUAGE REQUIREMENT:

Write the entire song in {request.language}.

Use the correct native writing system for that language
where applicable.
"""


    # ----------------------------------------------
    # AI Prompt
    # ----------------------------------------------

    prompt = f"""
You are an expert professional songwriter.

Your task is to create completely ORIGINAL song lyrics.

Song name / topic:
{request.song_name}

Genre:
{request.genre}

Mood:
{request.mood}

Language:
{request.language}

Number of verses:
{request.verses}


{language_instruction}


SONG STRUCTURE:

[Verse 1]
4-6 lines

[Pre-Chorus]
2-4 lines

[Chorus]
4-6 lines

[Verse 2]
4-6 lines

[Bridge]
4 lines

[Final Chorus]
4-6 lines


CREATIVE REQUIREMENTS:

1. Write completely original lyrics.

2. Do not reproduce lyrics from existing songs.

3. Do not quote copyrighted lyrics.

4. Do not continue or complete an existing song.

5. Do not copy lyrics from any known artist.

6. Match the requested genre.

7. Match the requested mood.

8. Use natural and meaningful rhymes.

9. Make the chorus memorable.

10. Make the lyrics emotionally engaging.

11. Keep the song coherent from beginning to end.

12. Follow the requested language strictly.

13. Return ONLY the song lyrics.

14. Do not explain your answer.

15. Do not add notes before or after the lyrics.
"""


    # ----------------------------------------------
    # Send request to Ollama
    # ----------------------------------------------

    try:

        response = requests.post(
            "http://localhost:11434/api/chat",

            json={
                "model": "qwen2.5-coder:3b",

                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a professional songwriter "
                            "who creates completely original lyrics."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                "stream": False,

                "options": {
                    "temperature": 0.85,
                    "top_p": 0.9,
                    "num_predict": 1200
                }
            },

            timeout=180
        )


        # ------------------------------------------
        # Check Ollama response
        # ------------------------------------------

        if response.status_code != 200:

            return {
                "error": "Ollama returned an error.",
                "details": response.text
            }


        data = response.json()


        # ------------------------------------------
        # Get generated lyrics
        # ------------------------------------------

        lyrics = data.get("message", {}).get("content", "")


        if not lyrics:

            return {
                "error": "Qwen did not generate any lyrics."
            }


        return {
            "success": True,
            "song_name": request.song_name,
            "genre": request.genre,
            "mood": request.mood,
            "language": request.language,
            "lyrics": lyrics.strip()
        }


    except requests.exceptions.ConnectionError:

        return {
            "error": (
                "Could not connect to Ollama. "
                "Make sure Ollama is running."
            )
        }


    except requests.exceptions.Timeout:

        return {
            "error": (
                "Qwen took too long to generate the lyrics. "
                "Please try again."
            )
        }


    except Exception as e:

        return {
            "error": "Unexpected server error.",
            "details": str(e)
        }
