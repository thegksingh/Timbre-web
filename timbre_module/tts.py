"""
Module for Text-to-speech conversion using edge-tts
"""


import edge_tts
import asyncio

class Tts:
    def __init__(self):
        pass

    async def generate_tts(
        self,
        text,
        voice,
        rate = "+0%",
        pitch = "+0Hz"
    ):
        
        #basic validation
        if not text.strip():
            raise ValueError("Input text for TTS is empty.")
        if not voice:
            raise ValueError("Voice parameter for TTS is empty.")
        
        #error handling
        try:
            #initializing egde_tts communnicate object with parameters(text,voice,rate,picth)
            communicate = edge_tts.Communicate(
                text = text,
                voice = voice,
                rate = rate,
                pitch = pitch
            )
            
            #b"" is empty binary data that is store audio 
            audio_data = b""

            #recieving audio data in small chunks
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    #appending each chunk to audio_data
                    audio_data += chunk["data"]
            
            #receiving the complete audio_data after all chunks are recieved
            return audio_data
        
        #raise exception when request was succeeded but no audio was received
        except edge_tts.exceptions.NoAudioReceived:
            raise RuntimeError9Edge("TTS failed to generate audio.")

        except Exception as e:
            raise RuntimeError(f"TTS generation failed: {e}")           