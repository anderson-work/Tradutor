from traceback import print_exc
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

en_text = "Do not meddle in the affairs of wizards, for they are subtle and quick to anger."
#chinese_text = "不要插手巫師的事務, 因為他們是微妙的, 很快就會發怒."
tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M", src_lang="en")
model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M").to("cuda")
encoded_en = tokenizer(en_text, return_tensors="pt").to("cuda")

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

for i, langId in enumerate(Languages):
    print(f'\n{i}. {Languages[langId]}\t', end='')
    try:
        generated_tokens = model.generate(**encoded_en, forced_bos_token_id=tokenizer.get_lang_id(langId))
    except:
        print('error')

        print_exc()

        continue
    s = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    print(s)

