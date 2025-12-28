import streamlit as st
from timbre_module.tts import Tts
import asyncio
from timbre_module.stt import Stt
from timbre_module.polisher import Polisher
from dotenv import load_dotenv

@st.cache_resource
def load_tts_service():
    return Tts()

@st.cache_resource
def load_stt_service(model="small"):
    return Stt(model)

@st.cache_resource
def load_polisher_service(model="gemini-2.5-flash"):
    return Polisher(model) 


#load environment varibale once
load_dotenv() 

#initializing Polisher class
polisher_service = load_polisher_service()

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
       ],
       index = None
   )

    #handling user choice

    #Text-to-speech
    if users_input == "Text to Speech":
        st.markdown("<h3 style='color:#00E5FF;'>Text to speech service</h3>", unsafe_allow_html=True)

        #text to convert
        tts_input_text = st.text_area(
            "Enter text to convert to speech:",
            max_chars = 20000,
            value = "Welcome to TIMBRE, your all-in-one AI-powered audio and text processing platform!",
            key = "tts-input"
        )
        #voice slection with default value 
        #TODO: better selection for all voices
        voice = st.text_input(
            "Enter voice:",
            value = "en-AU-NatashaNeural",
            key = "tts-voice"
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
                format = "%d%%",
                key = "tts-rate"
            )
        with col2:
            pitch_value = st.slider(
                "Select speech pitch:",
                min_value = -100,
                max_value = 100,
                value = 0,
                step = 1,
                format = "%dHz",
                key = "tts-pitch"
            )

        #converting rate_value and pitch_value to string 
        rate = f"{rate_value:+d}%"
        pitch = f"{pitch_value:+d}Hz"
    
        #output filename
        output_audio_filename = st.text_input(
            "Output audio filename:",
            value = "Result",
            key = "tts-audiofile-name"
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
        input_audio = st.file_uploader("Upload audio file:", type=["wav","mp3","m4a"],key="speech-to-text")
        
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
                    
                    #enhancing text to make sure grammer it correct
                    if stt_output_text: 
                        stt_enhancer_result = polisher_service.enhancer(
                            text = stt_output_text,
                            style = ""
                        )

                        #print result
                        if stt_enhancer_result:
                            st.text_area(
                                "Transcribed Text:",
                                value = stt_enhancer_result,
                                height = 200,
                                key = "stt-result"
                            )
                    
                            #success message
                            st.success("Text generated successfully!")

                            #celebrating STT success using snow
                            st.snow()

            except Exception as e:
                st.error(f"An error occurred during text generation: {e}")

    
    #text polisher
    if users_input ==  "Text Polisher":
        
        user_choice = st.selectbox("Choose service:", options=["Translator","Enhancer"],index = None)
        
        #handling user_choice for translator
        if user_choice == "Translator":

            #getting user text
            translation_input_text = st.text_area("Enter text for translation:",key = "input-for-translation")
            
            #getting target language
            target_language = st.text_input("Enter target language:", key = "language-input")

            #generate button and handling translation
            if st.button(
                "Translate",
                type = "primary",
                width = "stretch"
            ):
                #error handling for empty text and language
                if not translation_input_text.strip():
                    st.error("Please enter text for translation")
                    st.stop()
                if not target_language.strip():
                    st.error("Language can't be empty")
                    st.stop()

                #error handling   
                try:

                    #showing spinner while translating text
                    with st.spinner("Translating text, please wait..."):

                        #translating text to target language and detecting valid language
                        translator_result = polisher_service.translator(
                            text = translation_input_text,
                            language = target_language
                        )
                    
                        #print result
                        if translator_result:
                            st.text_area(
                                "Translation result",
                                value = translator_result,
                                height = 200,
                                key = "translation-result"
                            )
                        
                            #success message
                            st.success("Text translated.")
                        
                            #celebrating translation using snow
                            st.snow()

                except Exception as e:
                    st.error(f"An error occured during translaton: {e}")
            
        #handling user_choicce fro enhancer
        elif user_choice == "Enhancer":

            #getting user text
            enhancer_input_text = st.text_area("Enter text for enhacement:", key = "enhancer-input")

            #getting target lstyle
            target_style = st.selectbox(
                "Select style:",
                options = [
                    "Professional",
                    "Conversational",
                    "Clear and Simple",
                    "Concise",
                    "Persuasive",
                     "Storytelling",
                    "Creative",
                    "Empathetic",
                    "Motivational",
                    "Humorous",
                    "Academic",
                    "Technical",
                ],
                index = None
            )
           
           #generate button and handling enhancer
            if st.button(
                "Enhance",
                type = "primary",
                width = "stretch"
            ):
                #ensure style is never None (selectbox returns None if not selected)
                if target_style is None:
                    target_style = ""

                #error handling fro empty text and style
                if not enhancer_input_text.strip():
                    st.error("Please enter text for enhancement")
                    st.stop() 
                
                #error handling
                try:
                    
                    #showing spinner while enhancing text
                    with st.spinner("Enhancing text, please wait..."):

                        #enhancing text 
                        enhancer_result = polisher_service.enhancer(
                            text = enhancer_input_text,
                            style = target_style
                        )
                    
                        #print result
                        if enhancer_result:
                            st.text_area(
                                "Enhanced text",
                                value = enhancer_result,
                                height = 200,
                                key = "enhancer-result"
                            )
                        
                            #success message
                            st.success("Text enhanced.")

                            #celebrating enhancement using balloons
                            st.balloons()

                except Exception as e:
                    st.error(f"An error occured during enhancement: {e}")

    #speech to speech
    if users_input == "Speech to Speech":

        choosen = st.selectbox(
            "",
            options=[
                "Same-language voice conversion",
                "Cross-language speech translation",
            ],
            index = None
        )
        
        if choosen == "Same-language voice conversion":

            #storing uploded file into varaible into input_audio
            sts_input_audio = st.file_uploader("Upload audio file:", type=["wav","mp3","m4a"],key="stp-same-language")

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
                    format = "%d%%",
                    key = "sts-same-lang-rate"
                )
            with col2:
                pitch_value = st.slider(
                    "Select speech pitch:",
                    min_value = -100,
                    max_value = 100,
                    value = 0,
                    step = 1,
                    format = "%dHz",
                    key = "sts-same-lang-pitch"
                )

            #converting rate_value and pitch_value to string 
            rate = f"{rate_value:+d}%"
            pitch = f"{pitch_value:+d}Hz"

            #output filename
            output_audio_filename = st.text_input(
                "Output audio filename:",
                value = "Result",
                key = "sts-same-lang-outfile-name"
            )
        
            #generate button and handling same language speech to speech
            if st.button(
                label = "Generate Speech",
                type = "primary",
                width = "stretch"
            ):
            
                #error handling if no input auido file and voice
                if not sts_input_audio:
                   st.error("Upload audio file")
                   st.stop()
                if not voice.strip():
                   st.error("Please enter a voice.")
                   st.stop()
            
                #error handling
                try:
                
                    #shwoing spinner while converting speech
                    with st.spinner("Generating Speech"):

                        #converting audio file into text
                        sts_output_text = stt_service.generate(sts_input_audio)
                    
                        #enhancing text to ensure grammar is correct
                        if sts_output_text: 
                            sts_enhancer_result = polisher_service.enhancer(
                               text = sts_output_text,
                               style = ""
                            )
                        
                            #converting stt output (text) into selected voice output
                            output_audio = asyncio.run(
                                tts_service.generate_tts(
                                   text = sts_enhancer_result,
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
                                st.snow()

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
                    st.error(f"An error occurred during text generation: {e}")

        if choosen == "Cross-language speech translation":
             #storing uploded file into varaible into input_audio
            sts_input_audio_dif = st.file_uploader("Upload audio file:", type=["wav","mp3","m4a"],key="sts-diff-language")

            #target langauge to convert
            sts_target_language = st.text_input(
                label = "Enter language",
                value = "English"
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
                    format = "%d%%",
                    key = "sts-dif-lang-rate"
                )
            with col2:
                pitch_value = st.slider(
                    "Select speech pitch:",
                    min_value = -100,
                    max_value = 100,
                    value = 0,
                    step = 1,
                    format = "%dHz",
                    key = "sts-dif-lang-pitch"
                )

            #converting rate_value and pitch_value to string 
            rate = f"{rate_value:+d}%"
            pitch = f"{pitch_value:+d}Hz"

            #output filename
            output_audio_filename = st.text_input(
                "Output audio filename:",
                value = "Result",
                key = "sts-dif-lang_outputfile-name"
            )
            
            #generate button and handling different language speech to speech
            if st.button(
                "Translate speech",
                type = "primary",
                width = "stretch"
            ):
                 
                #error handling if no input auido file and voice and language
                if not sts_input_audio_dif:
                   st.error("Upload audio file")
                   st.stop()
                if not voice.strip():
                   st.error("Please enter a voice.")
                   st.stop()
                if not sts_target_language.strip():
                    st.error("Language can't be empty")
                    st.stop()

                #error handling
                try:
                
                    #shwoing spinner while performing stt-translation-enhancement-tts
                    with st.spinner("Generating Speech"):

                        #converting audio file into text
                        sts_dif_output_text = stt_service.generate(sts_input_audio_dif)
                        
                        #translating text to target language and detecting valid language
                        if sts_dif_output_text:
                            sts_translator_result = polisher_service.translator(
                                text = sts_dif_output_text,
                                language = sts_target_language
                            )
                             
                            #enhancing text to ensure grammar is correct
                            if sts_translator_result: 
                                sts_enhancer_result_dif = polisher_service.enhancer(
                                    text = sts_translator_result,
                                    style = ""
                                )

                                #generating audio
                                output_audio = asyncio.run(
                                    tts_service.generate_tts(
                                        text = sts_enhancer_result_dif,
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
                    
                                #celebrate STS succss using snow
                                st.snow()

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
                    st.error(f"An error occurred during text generation: {e}")

if __name__ == "__main__":
    main()