from google import genai
import os


class Polisher:
    
    #initialize semini client and model configuration
    def __init__(self,model="gemini-2.5-flash"):
        
        #error handling during api key validation and client initializtion
        try:
            #load api key from environment variables
            api_key = os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("Api key is not set up")
            self.client = genai.Client(api_key=api_key)
            self.model = model

        except Exception as e:
            print(f"Error {e}")
            self.model = None
   

    #prompt template fro translation
    def translator_prompt(self,text,language):
        return f"""
You are an expert, professional, and precise translator.

Strictly adhere to the following instructions:
1.  **Task:** Translate the text provided below into **{language}**.
2.  **Accuracy:** The translation must be as accurate, idiomatic, and contextually appropriate as possible.
3.  **Formatting:** Preserve all original line breaks, paragraph structure, and markdown/HTML elements exactly in the translated text.
4.  **Output Rule:** Provide **only** the translated text. **DO NOT** include any surrounding conversation, explanation, preamble, or any other text.
5.  **Target Language:** The entire output must be in **{language}**.

Text to Translate:
---
{text}
---
""" 

    
    #prompt template for enhancer
    def enhancer_prompt(self, text, style):
        style = style.strip()
        if style:
            instruction =f"Refine the text to conform to a **{style}** style and tone. Ensure the phrasing is accurate, idiomatic, and highly suitable for the requested style."
        else:
            instruction ="Correct all grammar and spelling mistakes. Improve the phrasing to be **clear, natural, and highly accurate** without changing the original tone significantly."
        return f"""
You are an expert editor and style guide. Your task is to polish and refine the provided text.

Strictly adhere to the following instructions:
1.  **Primary Task:** {instruction}
2.  **Correction:** Scrutinize and correct all errors in grammar, spelling, punctuation, and syntax.
3.  **Tone & Audience:** Ensure the refined text is appropriate for its context and maintains coherence.
4.  **Output Rule:** Provide **only** the polished and corrected text. **DO NOT** include any conversation, explanation, or preamble.
5.  **Formatting:** Preserve all original line breaks and paragraph structure.

Text to Enhance:
---
{text}
---
""" 

    #prompt template for language detection
    def detect_language_prompt(self,language):
        return f"""
Is "{language}" a valid human language name?

Rules:
- Answer ONLY "yes" or "no"
- No explanation
"""
    
    #detecting if user input for language is language
    def detect_language(self, language):
       
        #error handling for empty language
        if not language.strip():
            raise ValueError("Input text is empty")

        response = self.client.models.generate_content(
            model=self.model,
            contents=self.detect_language_prompt(language)
        )

        return response.text.strip().lower()

    
    #translate text to target language
    def translator(self,text,language):
        
        #error handling for empty text and language
        if not text.strip():
            raise ValueError("Input text is empty")
        if not language.strip():
            raise ValueError("Choose target language")
        
        #check input language
        is_valid = self.detect_language(language)
        if is_valid == "yes":

            try:
                prompt = self.translator_prompt(text,language)
                response = self.client.models.generate_content(
                    model = self.model,
                    contents = prompt
                )
                return response.text
            
            except Exception as e:
                raise RuntimeError(f"Translation failed: {e}")

    #enhance text by improving grammer and optionally changing writing style
    def enhancer(self,text,style):

        #error handling for empty text
        if not text.strip():
            raise ValueError("Input text is empty")
        
        #error handling
        try:
            prompt = self.enhancer_prompt(text,style)
            response = self.client.models.generate_content(
                model = self.model,
                contents = prompt
            )
        
            return response.text

        except Exception as e:
            raise RuntimeError(f"Enhancement failed: {e}")