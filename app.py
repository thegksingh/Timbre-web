import streamlit as st
from timbre_module.tts import Tts
import asyncio
from timbre_module.stt import Stt

@st.cache_resource
def load_tts_service():
    return Tts()

def load_stt_service(model="small"):
    return Stt(model)
    

#initializing Tts class
tts_service = load_tts_service() 

#initializing Stt class 
stt_service = load_stt_service()

def main():
    
    st.markdown("<h1 style='color:#00E5FF;'>TIMBRE!</h1>", unsafe_allow_html=True)

    #letting user choose the service
    users_input = st.selectbox(
        "Choose a processing service:",
        options=[
            "Text to Speech",
            "Speech to Speech",
            "Speech to Text",
            "Text Polisher"
       ]
   )

    #handling user choice

    #Text-to-speech
    if users_input == "Text to Speech":
        st.markdown("<h3 style='color:#00E5FF;'>Text to speech service</h3>", unsafe_allow_html=True)

        #text to convert
        tts_input_text = st.text_area(
            "Enter text to convert to speech:",
            max_chars = 5000,
            value = "Welcome to TIMBRE, your all-in-one AI-powered audio and text processing platform!"
        )
        #voice slection with default value 
        #TODO: better selection for all voices
        voice = st.text_input(
            "Enter voice:",
            value = "en-AU-NatashaNeural"
        )

        #rate and pitch selection with sliders
        col1, col2 = st.columns(2)
        with col1:
            rate_value = st.slider(
                "Select speech rate:",
                min_value = -100,
                max_value = 100,
                value = 0,
                step = 1,
                format = "%d%%"
            )
        with col2:
            pitch_value = st.slider(
                "Select speech pitch:",
                min_value = -100,
                max_value = 100,
                value = 0,
                step = 1,
                format = "%dHz"
            )

        #converting rate_value and pitch_value to string 
        rate = f"{rate_value:+d}%"
        pitch = f"{pitch_value:+d}Hz"
    
        #output filename
        output_audio_filename = st.text_input(
            "Output audio filename:",
            value = "Result"
        )
        
        #generate button and handling generation
        if st.button(
            "Generate Speech",
            type = "primary",
            width = "stretch"
        ):  
            #error handling for empty text input and voice
            if not tts_input_text.strip():
                st.error("Please enter text to convert.")
                st.stop()
            if not voice.strip():
                st.error("Please enter a voice.")
                st.stop()
            
            #error handling 
            try:
                #showing spinner while generaitng speech
                with st.spinner("Generating speech, please wait..."):
                    output_audio = asyncio.run(
                        tts_service.generate_tts(
                            text = tts_input_text,
                            voice = voice,
                            rate = rate,
                            pitch = pitch
                        )
                    )
        
                if output_audio:
                    st.audio(
                       output_audio,
                       format = "audio/wav"
                    )
                    
                    #success message
                    st.success("Speech generated successfully!")
                    
                    #celebrate TTS succss using ballons
                    st.balloons()

                    #download button
                    st.download_button(
                        label = "Download Audio",
                        data = output_audio,
                        file_name = f"{output_audio_filename}.wav",
                        mime = "audio/wav",
                        type = "primary",
                        width = "stretch"
                    )
            except Exception as e:
                st.error(f"An error occurred during speech generation: {e}")
    
   
    #speech to text
    if users_input == "Speech to Text":

        st.markdown("<h3 style='color:#00E5FF;'>Speech to text service</h3>", unsafe_allow_html=True)
        
        #storing uploded file into varaible into input_audio
        input_audio = st.file_uploader("Upload audio file:", type=["wav","mp3","m4a"])
        
        #generate button and handling generation
        if st.button(
                "Generate Text",
                type = "primary",
                width = "stretch"
            ):

            #error handling for empty file upload
            if not input_audio:
                st.error("Please upload an audio file.")
                st.stop()
 
            #error handling
            try:
                
                #showing spinner while generating text
                with st.spinner("Generating text, please wait..."):
                    stt_output_text = stt_service.generate(input_audio)

                    if stt_output_text:
                        st.text_area(
                            "Transcribed Text:",
                            value = stt_output_text,
                            height = 200
                        )
                    
                        #success message
                        st.success("Text generated successfully!")

                        #celebrating STT success using snow
                        st.snow()

            except Exception as e:
                st.error(f"An error occurred during text generation: {e}")


if __name__ == "__main__":
    main()