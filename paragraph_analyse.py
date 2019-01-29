import nltk
import re


def analyse(text):
    ret = {"is_analysed": 0, "sents_num": 0, "words_num": 0, "tokens_num": 0, "has_dialogue": 0, "whole_dialogue": 0}
    try:
        sentences = nltk.tokenize.sent_tokenize(text)
        sentences = [sent in sentences for sent in sentences if re.match("\\w+", sent)]
        tokens = nltk.tokenize.word_tokenize(text)
        words = [w for w in tokens if re.match("^\\w+$", w)]
        ret["sents_num"] = len(sentences)
        ret["words_num"] = len(words)
        ret["tokens_num"] = len(tokens)
        if "``" in tokens and "''" in tokens:
            ret["has_dialogue"] = 1
        if tokens[0] == "``" and tokens[-1] == "''" and "''" not in tokens[1:-1]:
            ret["whole_dialogue"] = 1
        ret["is_analysed"] = 1
    except:
        ret = ret
    return ret