"""
Module for Speech-to-text conversion using OpenAI's Whisper model
"""
import whisper
import tempfile
import os

class Stt:
   
    #Using small model to reduce memory (RAM) usage, suitable for deployment on streamlit cloud
    
    def __init__(self, model = "small"):
        #loading the whisper model once during class initialization to avoid reloading for every stt request
        self.model = whisper.load_model(model)

    def generate(self,uploaded_file):
        #creating a temporary file to store the uploaded audio file because whisper need a file path
        with tempfile.NamedTemporaryFile(delete = False,suffix = ".wav") as tmp_file:
            #read entire audio file as bytes and write to temp file
            tmp_file.write(uploaded_file.getvalue())
            #tmp_file.name store full path of the temporary file later passed to model.transcribe(tmp_path)
            tmp_path = tmp_file.name   

        try:
            #performing stt
            result = self.model.transcribe(tmp_path)

            #returning only the transcribed text from the result dictionary
            return(result["text"])

        finally:
            #deleting file after transcribing
            if os.path.exists(tmp_path):
                os.remove(tmp_path)