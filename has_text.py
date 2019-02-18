import API
import HP
import json
import os


if __name__ == "__main__":
    with open(HP.BOOKS_METADATA, 'r') as f:
        books_metadata = json.load(f)
    with open(HP.FEATURES_METADATA, 'r') as f:
        features_metadata = json.load(f)

    new_has_text = []
    for met in books_metadata:
        if os.path.isfile(HP.BOOKS_DIR + str(met['gutenberg_id']) + ".txt"):
            with open(HP.BOOKS_DIR + str(met['gutenberg_id']) + ".txt", 'r', encoding="UTF-8") as f:
                text = f.read()
            if text != "":
                met['has_text'] = True
                new_has_text.append(met['gutenberg_id'])
            else:
                met['has_text'] = False
        else:
            met['has_text'] = False

    features_metadata['has_text'] = new_has_text
    with open(HP.BOOKS_METADATA, 'w') as f:
        json.dump(books_metadata, f)
    with open(HP.FEATURES_METADATA, 'w') as f:
        json.dump(features_metadata, f)

