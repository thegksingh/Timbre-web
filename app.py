import streamlit as st
from timbre_module.tts import Tts
import asyncio
from timbre_module.stt import Stt
from timbre_module.polisher import Polisher
from dotenv import load_dotenv
import json

@st.cache_resource
def load_tts_service():
    return Tts()

@st.cache_resource
def load_stt_service(model="small"):
    return Stt(model)

@st.cache_resource
def load_polisher_service(model="gemini-2.5-flash"):
    return Polisher(model) 

@st.cache_data
def load_json():
    #opening json file
    with open("data/voices.json", "r") as f:
        return json.load(f)

#load json file
voices = load_json()

#load environment varibale once
load_dotenv() 

#initializing Polisher class
polisher_service = load_polisher_service()

#initializing Tts class
tts_service = load_tts_service() 

#initializing Stt class 
stt_service = load_stt_service()

def main():
    
    st.set_page_config(page_title = "Timbre",layout = "wide")
    
    st.markdown("<h1 style='color:#00E5FF;'>TIMBRE!</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    **Hi! I'm Gaurav Kumar Singh** – AI & Software Enthusiast. Undergraduate student at BHU.
    I build AI-powered tools for text and audio processing. This project demonstrates my skills.  
    Completed **CS50P**, currently doing **CS50x**.  
    """, unsafe_allow_html=True)
    with st.expander("About Timbre"):
        st.markdown("""
        Timbre is an all-in-one AI-powered audio and text toolkit:  
        - Convert text to speech (TTS)  
        - Transcribe audio to text (STT)  
        - Transform voices (STS)  
        - Translate & enhance text (Text Polisher)  

        **[Project Documentation](https://github.com/thegksingh/timbre-web#readme)** 
        """, unsafe_allow_html=True)

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
        ##created 2 columns
        col1,col2 = st.columns(2)

        with col1:

            #getting all language from json file and after sorting storing them in tts_languages_data variable
            tts_languages_data = sorted({voice['language'] for voice in voices})
    
            #let user select language
            tts_language_selected = st.selectbox(
                "Select language",
                options = tts_languages_data,
                index = None
            )
    
        with col2:

            #gender selection
            gender_selected = st.selectbox(
                "Select gender",
                options=[
                "Male",
                "Female"
                ],
                index = None
            )

        #created 2 more columns
        col3,col4 = st.columns(2)


        with col3:

            #filter voices based on selected language
            filtered_voices_language = [voice for voice in voices if voice['language'] == tts_language_selected]
    
            #sort availabel countries based on select language
            countries = sorted({voice['country'] for voice in filtered_voices_language})

            #country selection
            country_selected = st.selectbox(
            "Select country",
            options=countries,
            index = None
            )

        with col4:

            #filtering  and sort personalities on basis of selected language,gender,country
            filtered_personality = sorted({
            voice['personality']
            for voice in voices
            if voice['language'] == tts_language_selected
            and voice['country'] == country_selected
            and voice['gender'] == gender_selected
            })
    
            #personality selection
            personality_selected = st.selectbox(
                "Select personaliy",
                options = filtered_personality
            )

        #rate and pitch selection with sliders
        col5, col6 = st.columns(2)
        with col5:
            rate_value = st.slider(
                "Select speech rate:",
                min_value = -100,
                max_value = 100,
                value = 0,
                step = 1,
                format = "%d%%",
                key = "tts-rate"
            )
        with col6:
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
            if not tts_language_selected or not country_selected or not gender_selected or not personality_selected:
                st.error("Please select voice input")
                st.stop()
            
            #initialize voice_name
            voice_name = None

            #getting voice name from json
            for voice in voices:
                if(voice['language'] == tts_language_selected
                    and voice['country'] == country_selected
                    and voice['gender'] == gender_selected
                    and voice['personality'] == personality_selected):
                    
                    #retuning vaocie name
                    voice_name = voice['name']
                    break

                    #if no voice found
                    if not voice_name:
                        st.error("Try different combination")
                        st.stop()

            #error handling 
            try:
                #showing spinner while generaitng speech
                with st.spinner("Generating speech, please wait..."):
                    output_audio = asyncio.run(
                        tts_service.generate_tts(
                            text = tts_input_text,
                            voice = voice_name,
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

        #intructions and tips
        st.markdown("<h3 style='color:#00E5FF;'>Instructions & Tips</h3>", unsafe_allow_html=True)
        if users_input == "Text to Speech":
            st.markdown("""
            **How to use TTS:**  
            1. Enter the text to convert.  
            2. Select language, country, gender, personality.  
            3. Adjust speech rate and pitch.  
            4. Click **Generate Speech**.  

            **Note:** If you select a different language than your input text, accent changes according to the language.  
            Example: English input, Spanish voice → reads in Spanish accent.
            """)

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

        #instruction and tips
        st.markdown("""
        **How to use STT:**  
        1. Upload audio (.wav, .mp3, .m4a).  
        2. Whisper model default to small.  
        3. Click **Generate Text**.  

        **Tips:** Clear audio improves transcription.
        """)

    
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

        #instruction and tips
        st.markdown("""
        **How to use Text Polisher:**  
        1. Enter text.  
        2. Choose **Translator** or **Enhancer**.  
        3. For translator, enter target language.  
        4. For enhancer, select style (Professional, Conversational, etc.).  
        5. Click **Translate** or **Enhance**.
        """)

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
            ##created 2 columns
            col1,col2 = st.columns(2)

            with col1:

                #getting all language from json file and after sorting storing them in tts_languages_data variable
                tts_languages_data = sorted({voice['language'] for voice in voices})
    
                #let user select language
                tts_language_selected = st.selectbox(
                   "Select language",
                    options = tts_languages_data,
                    index = None
                )
    
            with col2:

                #gender selection
                gender_selected = st.selectbox(
                    "Select gender",
                    options=[
                        "Male",
                        "Female"
                    ],
                    index = None
                )

            #created 2 more columns
            col3,col4 = st.columns(2)


            with col3:

                #filter voices based on selected language
                filtered_voices_language = [voice for voice in voices if voice['language'] == tts_language_selected]
    
                #sort availabel countries based on select language
                countries = sorted({voice['country'] for voice in filtered_voices_language})

                #country selection
                country_selected = st.selectbox(
                    "Select country",
                    options=countries,
                    index = None
                )

            with col4:

                #filtering  and sort personalities on basis of selected language,gender,country
                filtered_personality = sorted({
                    voice['personality']
                    for voice in voices
                        if voice['language'] == tts_language_selected
                        and voice['country'] == country_selected
                        and voice['gender'] == gender_selected
                    })
    
                #personality selection
                personality_selected = st.selectbox(
                    "Select personaliy",
                    options = filtered_personality
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
                if not tts_language_selected or not country_selected or not gender_selected or not personality_selected:
                   st.error("Please select voice input")
                   st.stop()
                
                #initialize voice_name
                voice_name = None

                #getting voice name from json
                for voice in voices:
                    if(voice['language'] == tts_language_selected
                        and voice['country'] == country_selected
                        and voice['gender'] == gender_selected
                        and voice['personality'] == personality_selected):
                
                        #retuning vaocie name
                        voice_name = voice['name']
                        break
                    
                    #if no voice found
                    if not voice_name:
                        st.error("Try different combination")
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
                                   voice = voice_name,
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
        

        elif choosen == "Cross-language speech translation":
             #storing uploded file into varaible into input_audio
            sts_input_audio_dif = st.file_uploader("Upload audio file:", type=["wav","mp3","m4a"],key="sts-diff-language")

            #target langauge to convert
            sts_target_language = st.text_input(
                label = "Enter language",
                value = "English"
            ) 

            #voice slection with default value 
            ##created 2 columns
            col1,col2 = st.columns(2)

            with col1:

                #getting all language from json file and after sorting storing them in tts_languages_data variable
                tts_languages_data = sorted({voice['language'] for voice in voices})
    
                #let user select language
                tts_language_selected = st.selectbox(
                   "Select language",
                    options = tts_languages_data,
                    index = None
                )
    
            with col2:

                #gender selection
                gender_selected = st.selectbox(
                    "Select gender",
                    options=[
                        "Male",
                        "Female"
                    ],
                    index = None
                )

            #created 2 more columns
            col3,col4 = st.columns(2)


            with col3:

                #filter voices based on selected language
                filtered_voices_language = [voice for voice in voices if voice['language'] == tts_language_selected]
    
                #sort availabel countries based on select language
                countries = sorted({voice['country'] for voice in filtered_voices_language})

                #country selection
                country_selected = st.selectbox(
                    "Select country",
                    options=countries,
                    index = None
                )

            with col4:

                #filtering  and sort personalities on basis of selected language,gender,country
                filtered_personality = sorted({
                    voice['personality']
                    for voice in voices
                        if voice['language'] == tts_language_selected
                        and voice['country'] == country_selected
                        and voice['gender'] == gender_selected
                    })
    
                #personality selection
                personality_selected = st.selectbox(
                    "Select personaliy",
                    options = filtered_personality
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
                if not sts_target_language.strip():
                    st.error("Language can't be empty")
                    st.stop()
                if not tts_language_selected or not country_selected or not gender_selected or not personality_selected:
                    st.error("Please select voice input")
                    st.stop()

                #initialize voice_name
                voice_name = None

                #getting voice name from json
                for voice in voices:
                    if(voice['language'] == tts_language_selected
                        and voice['country'] == country_selected
                        and voice['gender'] == gender_selected
                        and voice['personality'] == personality_selected):
                    
                        #retuning vaocie name
                        voice_name = voice['name']
                        break

                        #if no voice found
                        if not voice_name:
                            st.error("Try different combination")
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
                                        voice = voice_name,
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

        #instruction and tips
        st.markdown("""
        **How to use STS:**  
        1. Upload audio.  
        2. Choose Same-language or Cross-language.  
        3. Select voice (language, country, gender, personality).  
        4. Adjust rate & pitch.  
        5. Click **Generate Speech**.  

        **Tips:** Cross-language converts input text to target language before generating voice.
        """)

if __name__ == "__main__":
    main()