from typing import List, Sequence
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer


device = "cuda"
model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M").to(device)
tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M", src_lang="en")


class Translator:
    def __init__(self, source_lang: str, dest_lang: str) -> None:
        self.source_lang = get_language_description(source_lang)
        self.target_lang = get_language_description(dest_lang)
        self.forced_bos_token_id = tokenizer.get_lang_id(dest_lang)

    def __call__(self, text: str) -> str:
        encoded_en = tokenizer(text, return_tensors="pt").to(device)
        generated_tokens = model.generate(**encoded_en, forced_bos_token_id=self.forced_bos_token_id)
        return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

Languages = {
    "ar": "Arabic",
    "cs": "Czech",
    "de": "German",
    "en": "English",
    "es": "Spanish",
    "et": "Estonian",
    "fi": "Finnish",
    "fr": "French",
#    "gu": "Gujarati",
    "he": "Hebrew",
    "hi": "Hindi",
    "hu": "Hungarian",
    "it": "Italian",
    "ja": "Japanese",
#    "kk": "Kazakh",
    "ko": "Korean",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mk": "Macedonian",
    "mn": "Mongolian",
    "mr": "Marathi",
    "my": "Burmese",
    "ne": "Nepali",
    "nl": "Dutch",
    "no": "Norwegian",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovenian",
    "sq": "Albanian",
    "sv": "Swedish",
    "ta": "Tamil",
#    "te": "Telugu",
    "th": "Thai",
    "tl": "Tagalog",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "xh": "Xhosa",
    "zh": "Chinese",
    "af": "Afrikaans",
#    "am": "Amharic",
    "az": "Azerbaijani",
    "be": "Belarusian",
    "bg": "Bulgarian",
    "bn": "Bengali"
}

def get_language_codes() -> List[str]:
    return list(Languages.keys())

def get_language_description(code:str) -> str:
    return Languages[code]

if __name__=='__main__':
    marian_ru_en = Translator('pt', 'eo')
    s = marian_ru_en.translate(['Realmente não sei o que fazer. Não sei o que fazer. Realmente. Vamos ver no que dá isso.'])
    print(s)


