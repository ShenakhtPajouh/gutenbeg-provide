import json
from collections import defaultdict
import HP


def create_metadata(metadata: dict):
    books_metadata = list()
    f = lambda: []
    authors = defaultdict(f)
    authors_id_name = dict()
    languages = defaultdict(f)
    bookshelves = defaultdict(f)
    has_text = list()
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
        ht = bool(metadata['has_text'][i])
        met = {"gutenberg_id": i, "title": title, "author": author, "author_id": author_id,
               "language": language, "bookshelf": bookshelf, "has_text": ht}
        books_metadata.append(met)
        authors[author].append(i)
        authors_id_name[author] = author_id
        if len(language) > 0:
            lan = "/".join(language)
            languages[lan].append(i)
        for bs in bookshelf:
            bookshelves[bs].append(i)
        if ht:
            has_text.append(i)
    others_metadata = {"authors": dict(authors), "authors_id_name": authors_id_name,
                       "languages": dict(languages), "bookshelves": dict(bookshelves),
                       "has_text": has_text}
    return books_metadata, others_metadata


if __name__ == "__main__":
    with open(HP.BASE_METADATA, 'r') as f:
        metadata = json.load(f)

    books_metadata, others_metadada = create_metadata(metadata)
    with open(HP.BOOKS_METADATA, 'w') as f:
        json.dump(books_metadata, f)
    with open(HP.FEATURES_METADATA, 'w') as f:
        json.dump(others_metadada, f)





