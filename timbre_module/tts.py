import edge_tts
import asyncio

class Tts:
    def __init__(self):
        pass

    async def generate_tts(
        self,
        tts_input_text,
        voice,
        rate = "+0%",
        pitch = "+0Hz"
    ):
        #initializing egde_tts communnicate object with parameters(text,voice,rate,picth)
        communicate = edge_tts.Communicate(
            text = tts_input_text,
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
            
        #reurning the complete audio_data after all chunks are recieved
        return audio_data
                    