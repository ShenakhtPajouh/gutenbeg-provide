import json
from collections import defaultdict
import HP
import os

def create_metadata(metadata: dict):
    books_metadata = list()
    f = lambda: []
    authors = defaultdict(f)
    authors_id_name = dict()
    languages = defaultdict(f)
    bookshelves = defaultdict(f)
    for i in range(1, len(metadata['gutenberg_id'])):
        title = str(metadata['title'][i])
        author = str(metadata['author'][i])
        author_id = metadata['gutenberg_author_id'][i]
        language = str(metadata['language'][i])
        if language == 'nan':
            language = []
        else:
            language = language.split('/')
        bookshelf = str(metadata['gutenberg_bookshelf'][i])
        if bookshelf == 'nan':
            bookshelf = []
        else:
            bookshelf = bookshelf.split('/')
        met = {"gutenberg_id": i, "title": title, "author": author, "author_id": author_id,
               "language": language, "bookshelf": bookshelf}
        books_metadata.append(met)
        authors[author].append(i)
        authors_id_name[author] = author_id
        if len(language) > 0:
            lan = "/".join(language)
            languages[lan].append(i)
        for bs in bookshelf:
            bookshelves[bs].append(i)

    features_metadata = {"authors": dict(authors), "authors_id_name": authors_id_name,
                       "languages": dict(languages), "bookshelves": dict(bookshelves)}
    return books_metadata, features_metadata

def has_text(books_metadata: list, features_metadata: dict):
    ht = []
    for met in books_metadata:
        flag = False
        i = met["gutenberg_id"]
        path = HP.BOOKS_DIR + str(i) + ".txt"
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
            if text != "":
                flag = True
        met["has_text"] = flag
        if flag:
            ht.append(i)
    features_metadata["has_text"] = ht


if __name__ == "__main__":
    with open(HP.BASE_METADATA, 'r') as f:
        metadata = json.load(f)
    books_metadata, features_metadata = create_metadata(metadata)
    has_text(books_metadata, features_metadata)
    with open(HP.BOOKS_METADATA, 'w') as f:
        json.dump(books_metadata, f)
    with open(HP.FEATURES_METADATA, 'w') as f:
        json.dump(features_metadata, f)





