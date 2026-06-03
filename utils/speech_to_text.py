import speech_recognition as sr
import io
import os

def transcribe_audio_bytes(audio_bytes) -> str:
    """
    Transcribes audio bytes (e.g. from Streamlit st.audio_input) using SpeechRecognition.
    """
    recognizer = sr.Recognizer()
    
    # SpeechRecognition expects a file-like object or a filename.
    # Streamlit's st.audio_input returns a BytesIO object (typically in WAV or WEBM format).
    # SpeechRecognition's AudioFile supports WAV, AIFF, AIFF-C, FLAC.
    
    # A temporary file is often the safest way to pass to AudioFile if format is uncertain,
    # but let's try direct AudioFile first, assuming it's WAV.
    # Streamlit audio input is often WAV format.
    
    # Write bytes to a temp file to ensure compatibility
    temp_filename = "temp_audio.wav"
    try:
        with open(temp_filename, "wb") as f:
            f.write(audio_bytes.getvalue())
            
        with sr.AudioFile(temp_filename) as source:
            audio_data = recognizer.record(source)
            # Using Google Web Speech API (free, no key required, requires internet)
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Speech Recognition service; {e}"
    except Exception as e:
        return f"Error during transcription: {str(e)}"
    finally:
        # Cleanup temp file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
