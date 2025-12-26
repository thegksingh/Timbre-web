import streamlit as st
from timbre_module.tts import Tts
import asyncio


@st.cache_resource
def load_tts_service():
    return Tts()

#initializing Tts class
speech = load_tts_service() 

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
        
        #error handling for empty text input and voice
        if not tts_input_text.strip():
            st.error("Please enter text to convert.")
            st.stop()
        if not voice.strip():
            st.error("Please enter a voice.")
            st.stop()

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

            try:
                with st.spinner("Generating speech, please wait..."):
                    output_audio = asyncio.run(
                        speech.generate_tts(
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

                    st.success("Speech generated successfully!")

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

if __name__ == "__main__":
    main()