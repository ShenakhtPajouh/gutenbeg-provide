BASE_METADATA = "metadata/base_metadata.json"
BOOKS_METADATA = "metadata/books_metadata.json"
FEATURES_METADATA = "metadata/features_metadata.json"
BOOKS_DIR = "/mnt/storage1/Data/gutenberg/books/"
PARAGRAPH_METADATA = "metadata/paragraphs.txt"

pre_keys = ["is_analysed", "sents_num", "words_num", "tokens_num", "has_dialogue", "whole_dialogue"]
keys = ["global_id", "book_id", "local_id"] + pre_keys

