# Preprocessing
import re
import unicodedata
from sacremoses import MosesPunctNormalizer

import crf_glossing.utils as utils


# Punctuation normalisation
mpn = MosesPunctNormalizer(lang='en')
mpn.substitutions = [
    (re.compile(r), sub) for r, sub in mpn.substitutions
]

def punctuation_normalisation(sent):
    return mpn.normalize(sent) #.strip()

# Encoding normalisation
def encoding_normalisation(string):
    '''Normalise the encoding.'''
    return unicodedata.normalize('NFC', string)

# Cutom preprocessing
def custom_preprocessing(text):
    '''Apply preprocessing on the original text.'''
    new_text = punctuation_normalisation(text)
    new_text = encoding_normalisation(new_text)
    new_text = utils.remove_excessive_whitespace(new_text)
    return new_text.strip()

# Miscellaneous preprocessing
def remove_quote_mark(string):
    '''Remove quote marks from the translation.'''
    return re.sub('"', '', string)

def remove_space_after_hyphen(string):
    '''Remove space after hyphen.'''
    pp_string = re.sub('= ', '=', string)
    return re.sub('- ', '-', pp_string)

def remove_new_line(string):
    '''Remove new lines in sentence.'''
    return utils.remove_excessive_whitespace(re.sub('\n', ' ', string))