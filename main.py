from os import walk, makedirs
from os.path import join, split, isfile, isdir
from traceback import format_exc
import json

def translate_json(data, parent_key='', translate=False):
    if isinstance(data, dict):
        translate = 'code' in data and data['code'] in [101, 102, 401, 402]
        for key, value in data.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            translate_json(value, new_key, translate)
    elif isinstance(data, list):
        translate = 'parameters' in parent_key
        for index, item in enumerate(data):
            new_key = f"{parent_key}[{index}]" if parent_key else f"[{index}]"
            x = translate_json(item, new_key, translate)
            if x:
                data[index] = x
    else:
        if translate: # tem que ser string
            translate = isinstance(data, str)
#        if translate: # não pode ser um número
#            try:
#                _ = float(data)
#                translate = False
#            except: 
#                pass
        if translate: # não pode ter um caracter só
            translate = len(data.strip()) > 1
        if translate: # não pode ter _
            translate = not data.split('_')[1:]
        if translate:
            translated_data = translator(data)
            print(f"{parent_key}: {data} -> {translated_data}")
            return translated_data


if __name__=='__main__':
    from translator import Translator, Languages
    
    INPUT_DIR = '/home/anderson/Tradutor/data'

    for lang in Languages:
        try:
            translator = Translator('en', lang)
        except:
            print(f'Error creating translator for {lang}')
            print(format_exc())
            continue

        print(f'Processing {lang}: {translator.target_lang}')
        OUTPUT_DIR = f'{INPUT_DIR}_{lang}_({translator.target_lang})'
        if not isdir(OUTPUT_DIR):
            makedirs(OUTPUT_DIR)
        for root, dirs, files in walk(INPUT_DIR):
            for file in files:
                if file.lower().endswith('.json'):
                    try:
                        with open(join(root, file)) as f:
                            parsed = json.load(f)
                        if file.lower().startswith('map'):
                            translate_json(parsed)
                        with open(join(root.replace(INPUT_DIR, OUTPUT_DIR), file), 'w') as f:
                            json.dump(parsed, f)
                    except:
                        print(f'Error processing {file}')
                        print(format_exc())
                        continue