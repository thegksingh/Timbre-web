import json

#mapping of language code to full language names
language_list = {
    "af": "Afrikaans",
    "am": "Amharic",
    "ar": "Arabic",
    "az": "Azerbaijani",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "ca": "Catalan",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "es": "Spanish",
    "et": "Estonian",
    "fa": "Persian",
    "fi": "Finnish",
    "fil": "Filipino",
    "fr": "French",
    "ga": "Irish",
    "gl": "Galician",
    "gu": "Gujarati",
    "he": "Hebrew",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "id": "Indonesian",
    "is": "Icelandic",
    "it": "Italian",
    "iu": "Inuktitut",
    "ja": "Japanese",
    "jv": "Javanese",
    "ka": "Georgian",
    "kk": "Kazakh",
    "km": "Khmer",
    "kn": "Kannada",
    "ko": "Korean",
    "lo": "Lao",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mn": "Mongolian",
    "mr": "Marathi",
    "ms": "Malay",
    "mt": "Maltese",
    "my": "Burmese",
    "nb": "Norwegian Bokmål",
    "ne": "Nepali",
    "nl": "Dutch",
    "pl": "Polish",
    "ps": "Pashto",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovenian",
    "so": "Somali",
    "sq": "Albanian",
    "sr": "Serbian",
    "su": "Sundanese",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "uz": "Uzbek",
    "vi": "Vietnamese",
    "zh": "Chinese",
    "zu": "Zulu"
}

#mapping of country codes to full country names
country_list = {
    "AE": "United Arab Emirates",
    "AL": "Albania",
    "AR": "Argentina",
    "AT": "Austria",
    "AU": "Australia",
    "AZ": "Azerbaijan",
    "BA": "Bosnia and Herzegovina",
    "BD": "Bangladesh",
    "BE": "Belgium",
    "BG": "Bulgaria",
    "BH": "Bahrain",
    "BO": "Bolivia",
    "BR": "Brazil",
    "CA": "Canada",
    "CH": "Switzerland",
    "CL": "Chile",
    "CN": "China",
    "CO": "Colombia",
    "CR": "Costa Rica",
    "CU": "Cuba",
    "CZ": "Czech Republic",
    "DE": "Germany",
    "DK": "Denmark",
    "DO": "Dominican Republic",
    "DZ": "Algeria",
    "EC": "Ecuador",
    "EE": "Estonia",
    "EG": "Egypt",
    "ES": "Spain",
    "ET": "Ethiopia",
    "FI": "Finland",
    "FR": "France",
    "GB": "United Kingdom",
    "GQ": "Equatorial Guinea",
    "GR": "Greece",
    "GT": "Guatemala",
    "HK": "Hong Kong",
    "HN": "Honduras",
    "HR": "Croatia",
    "HU": "Hungary",
    "ID": "Indonesia",
    "IE": "Ireland",
    "IL": "Israel",
    "IN": "India",
    "IQ": "Iraq",
    "IS": "Iceland",
    "IT": "Italy",
    "JO": "Jordan",
    "JP": "Japan",
    "KE": "Kenya",
    "KH": "Cambodia",
    "KR": "South Korea",
    "KW": "Kuwait",
    "LA": "Laos",
    "LB": "Lebanon",
    "LK": "Sri Lanka",
    "LT": "Lithuania",
    "LV": "Latvia",
    "LY": "Libya",
    "MA": "Morocco",
    "MK": "North Macedonia",
    "ML": "Mali",
    "MM": "Myanmar",
    "MN": "Mongolia",
    "MT": "Malta",
    "MX": "Mexico",
    "MY": "Malaysia",
    "NG": "Nigeria",
    "NI": "Nicaragua",
    "NL": "Netherlands",
    "NO": "Norway",
    "NP": "Nepal",
    "NZ": "New Zealand",
    "OM": "Oman",
    "PA": "Panama",
    "PE": "Peru",
    "PH": "Philippines",
    "PK": "Pakistan",
    "PL": "Poland",
    "PR": "Puerto Rico",
    "PT": "Portugal",
    "PY": "Paraguay",
    "QA": "Qatar",
    "RO": "Romania",
    "RS": "Serbia",
    "RU": "Russia",
    "SA": "Saudi Arabia",
    "SE": "Sweden",
    "SG": "Singapore",
    "SI": "Slovenia",
    "SK": "Slovakia",
    "SO": "Somalia",
    "SV": "El Salvador",
    "SY": "Syria",
    "TH": "Thailand",
    "TN": "Tunisia",
    "TR": "Turkey",
    "TW": "Taiwan",
    "TZ": "Tanzania",
    "UA": "Ukraine",
    "US": "United States",
    "UY": "Uruguay",
    "UZ": "Uzbekistan",
    "VE": "Venezuela",
    "VN": "Vietnam",
    "YE": "Yemen",
    "ZA": "South Africa"
}

#raw vocie ouput from edge tts
#you can get this list by running "edge-tts --list voices"
#this data will be parsed into structed json
data = """
Name                               Gender    ContentCategories      VoicePersonalities
---------------------------------  --------  ---------------------  --------------------------------------
af-ZA-AdriNeural                   Female    General                Friendly, Positive
af-ZA-WillemNeural                 Male      General                Friendly, Positive
am-ET-AmehaNeural                  Male      General                Friendly, Positive
am-ET-MekdesNeural                 Female    General                Friendly, Positive
ar-AE-FatimaNeural                 Female    General                Friendly, Positive
ar-AE-HamdanNeural                 Male      General                Friendly, Positive
ar-BH-AliNeural                    Male      General                Friendly, Positive
ar-BH-LailaNeural                  Female    General                Friendly, Positive
ar-DZ-AminaNeural                  Female    General                Friendly, Positive
ar-DZ-IsmaelNeural                 Male      General                Friendly, Positive
ar-EG-SalmaNeural                  Female    General                Friendly, Positive
ar-EG-ShakirNeural                 Male      General                Friendly, Positive
ar-IQ-BasselNeural                 Male      General                Friendly, Positive
ar-IQ-RanaNeural                   Female    General                Friendly, Positive
ar-JO-SanaNeural                   Female    General                Friendly, Positive
ar-JO-TaimNeural                   Male      General                Friendly, Positive
ar-KW-FahedNeural                  Male      General                Friendly, Positive
ar-KW-NouraNeural                  Female    General                Friendly, Positive
ar-LB-LaylaNeural                  Female    General                Friendly, Positive
ar-LB-RamiNeural                   Male      General                Friendly, Positive
ar-LY-ImanNeural                   Female    General                Friendly, Positive
ar-LY-OmarNeural                   Male      General                Friendly, Positive
ar-MA-JamalNeural                  Male      General                Friendly, Positive
ar-MA-MounaNeural                  Female    General                Friendly, Positive
ar-OM-AbdullahNeural               Male      General                Friendly, Positive
ar-OM-AyshaNeural                  Female    General                Friendly, Positive
ar-QA-AmalNeural                   Female    General                Friendly, Positive
ar-QA-MoazNeural                   Male      General                Friendly, Positive
ar-SA-HamedNeural                  Male      General                Friendly, Positive
ar-SA-ZariyahNeural                Female    General                Friendly, Positive
ar-SY-AmanyNeural                  Female    General                Friendly, Positive
ar-SY-LaithNeural                  Male      General                Friendly, Positive
ar-TN-HediNeural                   Male      General                Friendly, Positive
ar-TN-ReemNeural                   Female    General                Friendly, Positive
ar-YE-MaryamNeural                 Female    General                Friendly, Positive
ar-YE-SalehNeural                  Male      General                Friendly, Positive
az-AZ-BabekNeural                  Male      General                Friendly, Positive
az-AZ-BanuNeural                   Female    General                Friendly, Positive
bg-BG-BorislavNeural               Male      General                Friendly, Positive
bg-BG-KalinaNeural                 Female    General                Friendly, Positive
bn-BD-NabanitaNeural               Female    General                Friendly, Positive
bn-BD-PradeepNeural                Male      General                Friendly, Positive
bn-IN-BashkarNeural                Male      General                Friendly, Positive
bn-IN-TanishaaNeural               Female    General                Friendly, Positive
bs-BA-GoranNeural                  Male      General                Friendly, Positive
bs-BA-VesnaNeural                  Female    General                Friendly, Positive
ca-ES-EnricNeural                  Male      General                Friendly, Positive
ca-ES-JoanaNeural                  Female    General                Friendly, Positive
cs-CZ-AntoninNeural                Male      General                Friendly, Positive
cs-CZ-VlastaNeural                 Female    General                Friendly, Positive
cy-GB-AledNeural                   Male      General                Friendly, Positive
cy-GB-NiaNeural                    Female    General                Friendly, Positive
da-DK-ChristelNeural               Female    General                Friendly, Positive
da-DK-JeppeNeural                  Male      General                Friendly, Positive
de-AT-IngridNeural                 Female    General                Friendly, Positive
de-AT-JonasNeural                  Male      General                Friendly, Positive
de-CH-JanNeural                    Male      General                Friendly, Positive
de-CH-LeniNeural                   Female    General                Friendly, Positive
de-DE-AmalaNeural                  Female    General                Friendly, Positive
de-DE-ConradNeural                 Male      General                Friendly, Positive
de-DE-FlorianMultilingualNeural    Male      General                Friendly, Positive
de-DE-KatjaNeural                  Female    General                Friendly, Positive
de-DE-KillianNeural                Male      General                Friendly, Positive
de-DE-SeraphinaMultilingualNeural  Female    General                Friendly, Positive
el-GR-AthinaNeural                 Female    General                Friendly, Positive
el-GR-NestorasNeural               Male      General                Friendly, Positive
en-AU-NatashaNeural                Female    General                Friendly, Positive
en-AU-WilliamMultilingualNeural    Male      General                Friendly, Positive
en-CA-ClaraNeural                  Female    General                Friendly, Positive
en-CA-LiamNeural                   Male      General                Friendly, Positive
en-GB-LibbyNeural                  Female    General                Friendly, Positive
en-GB-MaisieNeural                 Female    General                Friendly, Positive
en-GB-RyanNeural                   Male      General                Friendly, Positive
en-GB-SoniaNeural                  Female    General                Friendly, Positive
en-GB-ThomasNeural                 Male      General                Friendly, Positive
en-HK-SamNeural                    Male      General                Friendly, Positive
en-HK-YanNeural                    Female    General                Friendly, Positive
en-IE-ConnorNeural                 Male      General                Friendly, Positive
en-IE-EmilyNeural                  Female    General                Friendly, Positive
en-IN-NeerjaExpressiveNeural       Female    General                Friendly, Positive
en-IN-NeerjaNeural                 Female    General                Friendly, Positive
en-IN-PrabhatNeural                Male      General                Friendly, Positive
en-KE-AsiliaNeural                 Female    General                Friendly, Positive
en-KE-ChilembaNeural               Male      General                Friendly, Positive
en-NG-AbeoNeural                   Male      General                Friendly, Positive
en-NG-EzinneNeural                 Female    General                Friendly, Positive
en-NZ-MitchellNeural               Male      General                Friendly, Positive
en-NZ-MollyNeural                  Female    General                Friendly, Positive
en-PH-JamesNeural                  Male      General                Friendly, Positive
en-PH-RosaNeural                   Female    General                Friendly, Positive
en-SG-LunaNeural                   Female    General                Friendly, Positive
en-SG-WayneNeural                  Male      General                Friendly, Positive
en-TZ-ElimuNeural                  Male      General                Friendly, Positive
en-TZ-ImaniNeural                  Female    General                Friendly, Positive
en-US-AnaNeural                    Female    Cartoon, Conversation  Cute
en-US-AndrewMultilingualNeural     Male      Conversation, Copilot  Warm, Confident, Authentic, Honest
en-US-AndrewNeural                 Male      Conversation, Copilot  Warm, Confident, Authentic, Honest
en-US-AriaNeural                   Female    News, Novel            Positive, Confident
en-US-AvaMultilingualNeural        Female    Conversation, Copilot  Expressive, Caring, Pleasant, Friendly
en-US-AvaNeural                    Female    Conversation, Copilot  Expressive, Caring, Pleasant, Friendly
en-US-BrianMultilingualNeural      Male      Conversation, Copilot  Approachable, Casual, Sincere
en-US-BrianNeural                  Male      Conversation, Copilot  Approachable, Casual, Sincere
en-US-ChristopherNeural            Male      News, Novel            Reliable, Authority
en-US-EmmaMultilingualNeural       Female    Conversation, Copilot  Cheerful, Clear, Conversational
en-US-EmmaNeural                   Female    Conversation, Copilot  Cheerful, Clear, Conversational
en-US-EricNeural                   Male      News, Novel            Rational
en-US-GuyNeural                    Male      News, Novel            Passion
en-US-JennyNeural                  Female    General                Friendly, Considerate, Comfort
en-US-MichelleNeural               Female    News, Novel            Friendly, Pleasant
en-US-RogerNeural                  Male      News, Novel            Lively
en-US-SteffanNeural                Male      News, Novel            Rational
en-ZA-LeahNeural                   Female    General                Friendly, Positive
en-ZA-LukeNeural                   Male      General                Friendly, Positive
es-AR-ElenaNeural                  Female    General                Friendly, Positive
es-AR-TomasNeural                  Male      General                Friendly, Positive
es-BO-MarceloNeural                Male      General                Friendly, Positive
es-BO-SofiaNeural                  Female    General                Friendly, Positive
es-CL-CatalinaNeural               Female    General                Friendly, Positive
es-CL-LorenzoNeural                Male      General                Friendly, Positive
es-CO-GonzaloNeural                Male      General                Friendly, Positive
es-CO-SalomeNeural                 Female    General                Friendly, Positive
es-CR-JuanNeural                   Male      General                Friendly, Positive
es-CR-MariaNeural                  Female    General                Friendly, Positive
es-CU-BelkysNeural                 Female    General                Friendly, Positive
es-CU-ManuelNeural                 Male      General                Friendly, Positive
es-DO-EmilioNeural                 Male      General                Friendly, Positive
es-DO-RamonaNeural                 Female    General                Friendly, Positive
es-EC-AndreaNeural                 Female    General                Friendly, Positive
es-EC-LuisNeural                   Male      General                Friendly, Positive
es-ES-AlvaroNeural                 Male      General                Friendly, Positive
es-ES-ElviraNeural                 Female    General                Friendly, Positive
es-ES-XimenaNeural                 Female    General                Friendly, Positive
es-GQ-JavierNeural                 Male      General                Friendly, Positive
es-GQ-TeresaNeural                 Female    General                Friendly, Positive
es-GT-AndresNeural                 Male      General                Friendly, Positive
es-GT-MartaNeural                  Female    General                Friendly, Positive
es-HN-CarlosNeural                 Male      General                Friendly, Positive
es-HN-KarlaNeural                  Female    General                Friendly, Positive
es-MX-DaliaNeural                  Female    General                Friendly, Positive
es-MX-JorgeNeural                  Male      General                Friendly, Positive
es-NI-FedericoNeural               Male      General                Friendly, Positive
es-NI-YolandaNeural                Female    General                Friendly, Positive
es-PA-MargaritaNeural              Female    General                Friendly, Positive
es-PA-RobertoNeural                Male      General                Friendly, Positive
es-PE-AlexNeural                   Male      General                Friendly, Positive
es-PE-CamilaNeural                 Female    General                Friendly, Positive
es-PR-KarinaNeural                 Female    General                Friendly, Positive
es-PR-VictorNeural                 Male      General                Friendly, Positive
es-PY-MarioNeural                  Male      General                Friendly, Positive
es-PY-TaniaNeural                  Female    General                Friendly, Positive
es-SV-LorenaNeural                 Female    General                Friendly, Positive
es-SV-RodrigoNeural                Male      General                Friendly, Positive
es-US-AlonsoNeural                 Male      General                Friendly, Positive
es-US-PalomaNeural                 Female    General                Friendly, Positive
es-UY-MateoNeural                  Male      General                Friendly, Positive
es-UY-ValentinaNeural              Female    General                Friendly, Positive
es-VE-PaolaNeural                  Female    General                Friendly, Positive
es-VE-SebastianNeural              Male      General                Friendly, Positive
et-EE-AnuNeural                    Female    General                Friendly, Positive
et-EE-KertNeural                   Male      General                Friendly, Positive
fa-IR-DilaraNeural                 Female    General                Friendly, Positive
fa-IR-FaridNeural                  Male      General                Friendly, Positive
fi-FI-HarriNeural                  Male      General                Friendly, Positive
fi-FI-NooraNeural                  Female    General                Friendly, Positive
fil-PH-AngeloNeural                Male      General                Friendly, Positive
fil-PH-BlessicaNeural              Female    General                Friendly, Positive
fr-BE-CharlineNeural               Female    General                Friendly, Positive
fr-BE-GerardNeural                 Male      General                Friendly, Positive
fr-CA-AntoineNeural                Male      General                Friendly, Positive
fr-CA-JeanNeural                   Male      General                Friendly, Positive
fr-CA-SylvieNeural                 Female    General                Friendly, Positive
fr-CA-ThierryNeural                Male      General                Friendly, Positive
fr-CH-ArianeNeural                 Female    General                Friendly, Positive
fr-CH-FabriceNeural                Male      General                Friendly, Positive
fr-FR-DeniseNeural                 Female    General                Friendly, Positive
fr-FR-EloiseNeural                 Female    General                Friendly, Positive
fr-FR-HenriNeural                  Male      General                Friendly, Positive
fr-FR-RemyMultilingualNeural       Male      General                Friendly, Positive
fr-FR-VivienneMultilingualNeural   Female    General                Friendly, Positive
ga-IE-ColmNeural                   Male      General                Friendly, Positive
ga-IE-OrlaNeural                   Female    General                Friendly, Positive
gl-ES-RoiNeural                    Male      General                Friendly, Positive
gl-ES-SabelaNeural                 Female    General                Friendly, Positive
gu-IN-DhwaniNeural                 Female    General                Friendly, Positive
gu-IN-NiranjanNeural               Male      General                Friendly, Positive
he-IL-AvriNeural                   Male      General                Friendly, Positive
he-IL-HilaNeural                   Female    General                Friendly, Positive
hi-IN-MadhurNeural                 Male      General                Friendly, Positive
hi-IN-SwaraNeural                  Female    General                Friendly, Positive
hr-HR-GabrijelaNeural              Female    General                Friendly, Positive
hr-HR-SreckoNeural                 Male      General                Friendly, Positive
hu-HU-NoemiNeural                  Female    General                Friendly, Positive
hu-HU-TamasNeural                  Male      General                Friendly, Positive
id-ID-ArdiNeural                   Male      General                Friendly, Positive
id-ID-GadisNeural                  Female    General                Friendly, Positive
is-IS-GudrunNeural                 Female    General                Friendly, Positive
is-IS-GunnarNeural                 Male      General                Friendly, Positive
it-IT-DiegoNeural                  Male      General                Friendly, Positive
it-IT-ElsaNeural                   Female    General                Friendly, Positive
it-IT-GiuseppeMultilingualNeural   Male      General                Friendly, Positive
it-IT-IsabellaNeural               Female    General                Friendly, Positive
iu-Cans-CA-SiqiniqNeural           Female    General                Friendly, Positive
iu-Cans-CA-TaqqiqNeural            Male      General                Friendly, Positive
iu-Latn-CA-SiqiniqNeural           Female    General                Friendly, Positive
iu-Latn-CA-TaqqiqNeural            Male      General                Friendly, Positive
ja-JP-KeitaNeural                  Male      General                Friendly, Positive
ja-JP-NanamiNeural                 Female    General                Friendly, Positive
jv-ID-DimasNeural                  Male      General                Friendly, Positive
jv-ID-SitiNeural                   Female    General                Friendly, Positive
ka-GE-EkaNeural                    Female    General                Friendly, Positive
ka-GE-GiorgiNeural                 Male      General                Friendly, Positive
kk-KZ-AigulNeural                  Female    General                Friendly, Positive
kk-KZ-DauletNeural                 Male      General                Friendly, Positive
km-KH-PisethNeural                 Male      General                Friendly, Positive
km-KH-SreymomNeural                Female    General                Friendly, Positive
kn-IN-GaganNeural                  Male      General                Friendly, Positive
kn-IN-SapnaNeural                  Female    General                Friendly, Positive
ko-KR-HyunsuMultilingualNeural     Male      General                Friendly, Positive
ko-KR-InJoonNeural                 Male      General                Friendly, Positive
ko-KR-SunHiNeural                  Female    General                Friendly, Positive
lo-LA-ChanthavongNeural            Male      General                Friendly, Positive
lo-LA-KeomanyNeural                Female    General                Friendly, Positive
lt-LT-LeonasNeural                 Male      General                Friendly, Positive
lt-LT-OnaNeural                    Female    General                Friendly, Positive
lv-LV-EveritaNeural                Female    General                Friendly, Positive
lv-LV-NilsNeural                   Male      General                Friendly, Positive
mk-MK-AleksandarNeural             Male      General                Friendly, Positive
mk-MK-MarijaNeural                 Female    General                Friendly, Positive
ml-IN-MidhunNeural                 Male      General                Friendly, Positive
ml-IN-SobhanaNeural                Female    General                Friendly, Positive
mn-MN-BataaNeural                  Male      General                Friendly, Positive
mn-MN-YesuiNeural                  Female    General                Friendly, Positive
mr-IN-AarohiNeural                 Female    General                Friendly, Positive
mr-IN-ManoharNeural                Male      General                Friendly, Positive
ms-MY-OsmanNeural                  Male      General                Friendly, Positive
ms-MY-YasminNeural                 Female    General                Friendly, Positive
mt-MT-GraceNeural                  Female    General                Friendly, Positive
mt-MT-JosephNeural                 Male      General                Friendly, Positive
my-MM-NilarNeural                  Female    General                Friendly, Positive
my-MM-ThihaNeural                  Male      General                Friendly, Positive
nb-NO-FinnNeural                   Male      General                Friendly, Positive
nb-NO-PernilleNeural               Female    General                Friendly, Positive
ne-NP-HemkalaNeural                Female    General                Friendly, Positive
ne-NP-SagarNeural                  Male      General                Friendly, Positive
nl-BE-ArnaudNeural                 Male      General                Friendly, Positive
nl-BE-DenaNeural                   Female    General                Friendly, Positive
nl-NL-ColetteNeural                Female    General                Friendly, Positive
nl-NL-FennaNeural                  Female    General                Friendly, Positive
nl-NL-MaartenNeural                Male      General                Friendly, Positive
pl-PL-MarekNeural                  Male      General                Friendly, Positive
pl-PL-ZofiaNeural                  Female    General                Friendly, Positive
ps-AF-GulNawazNeural               Male      General                Friendly, Positive
ps-AF-LatifaNeural                 Female    General                Friendly, Positive
pt-BR-AntonioNeural                Male      General                Friendly, Positive
pt-BR-FranciscaNeural              Female    General                Friendly, Positive
pt-BR-ThalitaMultilingualNeural    Female    General                Friendly, Positive
pt-PT-DuarteNeural                 Male      General                Friendly, Positive
pt-PT-RaquelNeural                 Female    General                Friendly, Positive
ro-RO-AlinaNeural                  Female    General                Friendly, Positive
ro-RO-EmilNeural                   Male      General                Friendly, Positive
ru-RU-DmitryNeural                 Male      General                Friendly, Positive
ru-RU-SvetlanaNeural               Female    General                Friendly, Positive
si-LK-SameeraNeural                Male      General                Friendly, Positive
si-LK-ThiliniNeural                Female    General                Friendly, Positive
sk-SK-LukasNeural                  Male      General                Friendly, Positive
sk-SK-ViktoriaNeural               Female    General                Friendly, Positive
sl-SI-PetraNeural                  Female    General                Friendly, Positive
sl-SI-RokNeural                    Male      General                Friendly, Positive
so-SO-MuuseNeural                  Male      General                Friendly, Positive
so-SO-UbaxNeural                   Female    General                Friendly, Positive
sq-AL-AnilaNeural                  Female    General                Friendly, Positive
sq-AL-IlirNeural                   Male      General                Friendly, Positive
sr-RS-NicholasNeural               Male      General                Friendly, Positive
sr-RS-SophieNeural                 Female    General                Friendly, Positive
su-ID-JajangNeural                 Male      General                Friendly, Positive
su-ID-TutiNeural                   Female    General                Friendly, Positive
sv-SE-MattiasNeural                Male      General                Friendly, Positive
sv-SE-SofieNeural                  Female    General                Friendly, Positive
sw-KE-RafikiNeural                 Male      General                Friendly, Positive
sw-KE-ZuriNeural                   Female    General                Friendly, Positive
sw-TZ-DaudiNeural                  Male      General                Friendly, Positive
sw-TZ-RehemaNeural                 Female    General                Friendly, Positive
ta-IN-PallaviNeural                Female    General                Friendly, Positive
ta-IN-ValluvarNeural               Male      General                Friendly, Positive
uz-UZ-MadinaNeural                 Female    General                Friendly, Positive
uz-UZ-SardorNeural                 Male      General                Friendly, Positive
vi-VN-HoaiMyNeural                 Female    General                Friendly, Positive
vi-VN-NamMinhNeural                Male      General                Friendly, Positive
zh-CN-XiaoxiaoNeural               Female    News, Novel            Warm
zh-CN-XiaoyiNeural                 Female    Cartoon, Novel         Lively
zh-CN-YunjianNeural                Male      Sports,  Novel         Passion
zh-CN-YunxiNeural                  Male      Novel                  Lively, Sunshine
zh-CN-YunxiaNeural                 Male      Cartoon, Novel         Cute
zh-CN-YunyangNeural                Male      News                   Professional, Reliable
zh-CN-liaoning-XiaobeiNeural       Female    Dialect                Humorous
zh-CN-shaanxi-XiaoniNeural         Female    Dialect                Bright
zh-HK-HiuGaaiNeural                Female    General                Friendly, Positive
zh-HK-HiuMaanNeural                Female    General                Friendly, Positive
zh-HK-WanLungNeural                Male      General                Friendly, Positive
zh-TW-HsiaoChenNeural              Female    General                Friendly, Positive
zh-TW-HsiaoYuNeural                Female    General                Friendly, Positive
zh-TW-YunJheNeural                 Male      General                Friendly, Positive
zu-ZA-ThandoNeural                 Female    General                Friendly, Positive
zu-ZA-ThembaNeural                 Male      General                Friendly, Positive
"""

def extract_voice(text):
    #created an empty list
    voices = []
    
    #split text into individual lines
    lines = text.strip().split("\n")

     #iterate through each row of the vocie table 
    for line in lines:

        #skip header,empty lines and seprators
        if line.startswith("-") or "Name" in line or not line.strip():
            continue
        
        #exctract fileds usinf fisex-width column slicing
        #adjust slicing indexes if the table fromat chnages
        name = line[0:35].strip()
        gender = line[35:45].strip()
        category = line[45:68].strip()
        personality = line[68:].strip()

        #extracting language code fron name
        parts = name.split("-")

        lang = f"{parts[0]}-{parts[1]}" if len(parts) > 1 else "Unknown"

        language_code = parts[0]
        
        #for special case
        if len(parts) >= 3 and parts[1] in ("Cans","Latn"):
            country_code = parts[2]
        else:
            country_code = parts[1]
        
        #converting language and country code to names
        language = language_list.get(language_code,language_code)
        country = country_list.get(country_code, country_code)

        #appending data in voice list
        voices.append({
            "name": name,
            "gender": gender,
            "language": language,
            "country": country,
            "category": category,
            "personality": personality
        }) 
        
    return voices

#calling funtion
voice_list = extract_voice(data)

#storing data into json file for streamlit app
with open("voices.json", "w") as f:
    json.dump(voice_list,f,indent=4)
