import HP
import json
import numpy as np
from collections import defaultdict


def get_books_metadata(books_id=None):
    """

    Args:
        books_id: A list of integers, if it is not None, then it will return metadata of only these ids

    """
    with open(HP.BOOKS_METADATA, 'r') as f:
        metadata = json.load(f)
    if books_id is not None:
        metadata = {i: metadata[i-1] for i in books_id}
    else:
        metadata = {i+1: met for i, met in enumerate(metadata)}
    return metadata


def get_books(author=None, language=None, bookshelf=None, has_text=True):
    with open(HP.FEATURES_METADATA, 'r') as f:
        features_metadata = json.load(f)
    if has_text:
        books = features_metadata["has_text"]
    else:
        with open(HP.BOOKS_METADATA, 'r') as f:
            books = json.load(f)
            books = [gut["gutenberg_id"] for gut in books]
    books = set(books)

    x = author
    name_x = "authors"
    if x is not None:
        if isinstance(x, str):
            x = [x]
        x = [y for y in x if y in features_metadata[name_x]]
        bb = [features_metadata[name_x][ent] for ent in x]
        bb = sum(bb, [])
        bb = set(bb)
        books = books & bb

    x = bookshelf
    name_x = "bookshelves"
    if x is not None:
        if isinstance(x, str):
            x = [x]
        x = [y for y in x if y in features_metadata[name_x]]
        bb = [features_metadata[name_x][ent] for ent in x]
        bb = sum(bb, [])
        bb = set(bb)
        books = books & bb

    languages = features_metadata['languages']
    lans = []
    if language is not None:
        if isinstance(language, str):
            language = {language}
        else:
            language = set(language)
        for lan1 in language:
            if lan1 in languages:
                lans.append(lan1)
            for lan2 in language - {lan1}:
                l = lan1 + '/' + lan2
                if l in languages:
                    lans.append(l)
        bb = [languages[ent] for ent in lans]
        bb = sum(bb, [])
        bb = set(bb)
        books = books & bb
    return list(books)


def get_keys(feature):
    with open(HP.FEATURES_METADATA, 'r') as f:
        features_metadata = json.load(f)
    return list(features_metadata[feature].keys())


def get_features():
    with open(HP.FEATURES_METADATA, 'r') as f:
        features_metadata = json.load(f)
    return list(features_metadata.keys())


def get_keys():
    return HP.keys.copy()

def get_paragraphs_metadata(par_ids = None):
    metadata = np.loadtxt(HP.PARAGRAPH_METADATA, dtype=int)
    if par_ids is not None:
        par_ids = np.array(par_ids) - 1
        metadata = metadata[par_ids]
    return metadata


def get_paragraphs_id(books=None, is_analysed=True, sents_num=None, words_num=None,
                      tokens_num=None, has_dialogue=None, whole_dialogue=None, output_local_id=True):
    metadata = np.loadtxt(HP.PARAGRAPH_METADATA, dtype=np.int16)
    keys = get_keys()
    keys = dict(zip(keys, range(len(keys))))

    x = is_analysed
    x_name = "is_analysed"
    if x:
        vec = metadata[:, keys[x_name]]
        vec = vec == 1
        metadata = metadata[vec]

    if books is not None:
        vec = metadata[:, keys["book_id"]]
        vec = np.expand_dims(vec, 1)
        bks = np.array(books, dtype=int)
        if bks.ndim != 1:
            raise AttributeError("books must be a list of integers")
        vec = vec == bks
        vec = np.any(vec, 1)
        metadata = metadata[vec]
        bks = None

    x = sents_num
    x_name = "sents_num"
    if x is not None:
        vec = books[:, keys[x_name]]
        if isinstance(x, int):
            vec = vec == x
        elif len(x) == 2:
            if not isinstance(x[0], int) and isinstance(x[1], int):
                raise ValueError(x_name + " must be a positive integer or tuple of two positive integers")
            vec = np.logical_and(x[0] <= vec, x[1] >= vec)
        else:
            raise ValueError(x_name + " must be a positive integer or tuple of two positive integers")
        metadata = metadata[vec]

    x = words_num
    x_name = "words_num"
    if x is not None:
        vec = books[:, keys[x_name]]
        if isinstance(x, int):
            vec = vec == x
        elif len(x) == 2:
            if not isinstance(x[0], int) and isinstance(x[1], int):
                raise ValueError(x_name + " must be a positive integer or tuple of two positive integers")
            vec = np.logical_and(x[0] <= vec, x[1] >= vec)
        else:
            raise ValueError(x_name + " must be a positive integer or tuple of two positive integers")
        metadata = metadata[vec]

    x = tokens_num
    x_name = "tokens_num"
    if x is not None:
        vec = books[:, keys[x_name]]
        if isinstance(x, int):
            vec = vec == x
        elif len(x) == 2:
            if not isinstance(x[0], int) and isinstance(x[1], int):
                raise ValueError(x_name + " must be a positive integer or tuple of two positive integers")
            vec = np.logical_and(x[0] <= vec, x[1] >= vec)
        else:
            raise ValueError(x_name + " must be a positive integer or tuple of two positive integers")
        metadata = metadata[vec]

    x = has_dialogue
    x_name = "has_dialogue"
    if x is not None:
        vec = books[: keys[x_name]]
        vec = vec == bool(x)
        metadata = metadata[vec]

    x = whole_dialogue
    x_name = "whole_dialogue"
    if x is not None:
        vec = books[: keys[x_name]]
        vec = vec == bool(x)
        metadata = metadata[vec]

    vec = metadata[:, keys["book_id"]]
    books = list(vec)
    books = set(books)
    books = sorted(list(books))
    if output_local_id:
        x_name = "local_id"
    else:
        x_name = "global_id"
    output = metadata[:, keys[x_name]]
    output = {book: list(output[vec == book]) for book in books}
    return output


def get_local_ids(pars):
    if isinstance(pars, dict):
        pars = sum([p for p in pars.values()], [])
    metadata = np.loadtxt(HP.PARAGRAPH_METADATA, dtype=int)
    keys = get_keys()
    keys = dict(zip(keys, range(len(keys))))
    pars = np.array(pars, dtype=int) - 1
    metadata = metadata[pars]
    vec = metadata[:, keys["book_id"]]
    books = list(vec)
    books = set(books)
    books = sorted(list(books))
    local_id = metadata[:, keys["local_id"]]
    local_id = {book: list(local_id[vec == book]) for book in books}
    return local_id


def get_global_ids(local_id):
    metadata = np.loadtxt(HP.PARAGRAPH_METADATA, dtype=int)
    keys = get_keys()
    keys = dict(zip(keys, range(len(keys))))
    vec = metadata[:, keys["book_id"]]
    global_ids = metadata[:, keys["global_id"]]
    output = dict()
    for book, pars in local_id.items():
        ids = global_ids[vec == book]
        ids = ids[np.array(pars, dtype=int) - 1]
        ids = list(ids)
        output[book] = ids
    return output


def get_paragraphs_id_n(n: int, books=None, is_analysed=True, sents_num=None, words_num=None,
                        tokens_num=None, has_dialogue=None, whole_dialogue=None):
    assert n >= 1
    local_pars = get_paragraphs_id(books=books, is_analysed=is_analysed, sents_num=sents_num,
                                   words_num=words_num, tokens_num=tokens_num, has_dialogue=has_dialogue,
                                   whole_dialogue=whole_dialogue)
    new_local_pars = []
    for book, pars in local_pars.items():
        new_pars = []
        pars = set(pars)
        for i in pars:
            seq = tuple(i + x for x in range(n))
            if set(seq).issubset(pars):
                new_pars.append(seq)
        if len(new_pars) > 0:
            new_local_pars.append((book, new_pars))
    return dict(new_local_pars)


def get_local_global_dict(books=None):
    if books is None:
        books = get_books()
    result = dict()
    metadata = get_paragraphs_metadata()
    keys = get_keys()
    keys = dict(zip(keys, range(len(keys))))
    features = np.array([keys["global_id"], keys["local_id"], keys["book_id"]])
    metadata = metadata[:, features]
    for book in books:
        met = metadata[:, np.array([1, 0])][metadata[:, 2] == book]
        met = dict(met)
        result[book] = met
    return result

def get_global_local_dict(pars=None):
    metadata = get_paragraphs_metadata()
    keys = get_keys()
    keys = dict(zip(keys, range(len(keys))))
    features = np.array([keys["global_id"], keys["local_id"], keys["book_id"]])
    metadata = metadata[:, features]
    if pars is not None:
        pars = np.array(pars) - 1
        metadata = metadata[:, pars]
    return {par: (book, loc) for par, loc, book in metadata}   



def get_paragraph_text(ids, num_sequential=1):
    local_ids = ids
    paragraphs = list()
    local_global = get_local_global_dict(list(local_ids))
    for book, pars in local_ids.items():
        with open(HP.BOOKS_DIR + str(book) + ".txt", 'r') as f:
            text = f.read()
        text = [p for p in text.split("\n\n") if p != ""]
        if num_sequential == 1:
            pps = set(pars)
        else:
            pps = set(sum([list(p) for p in pars], []))
        text = {p: text[p - 1] for p in pps}
        met = local_global[book]
        paragraphs = paragraphs + [(met[p], text[p]) for p in pps]
    paragraphs = dict(paragraphs)
    return paragraphs, local_global



































