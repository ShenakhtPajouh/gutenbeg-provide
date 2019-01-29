import json
import re

BOOKS_PATH='/mnt/storage1/Data/gutenberg/gutenberg/'

def clear_book(text):
    text = text.split('\n')
    j = 0
    for i, sent in enumerate(text):
        if re.match("^\\*\\*\\* START OF THIS PROJECT GUTENBERG(.)*\\*\\*\\*$", sent):
            j = i
            break
    text = "\n".join(text[j+1:])
    return text

with open('paths/paths.json', 'r') as f:
    files = json.load(f)
    
for gut_id, book_paths in files.items():
    if int(gut_id) > 70000:
        continue
    path = book_paths[0]
    with open(BOOKS_PATH + path, 'r', encoding='latin1') as f:
        text = f.read()
    text = clear_book(text)
    with open('books/' + str(gut_id) + '.txt', 'w', encoding='utf-8') as f:
        f.write(text)