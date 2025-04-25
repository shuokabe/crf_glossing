import sklearn_crfsuite


# Default CRF features (from CRF suite documentation) + additional features for glossing
def morph2features(sentence, i):
    morph = sentence[i][0]

    def is_boundary(morpheme):
        '''Outputs whether the morpheme is a morpheme boundary or not.'''
        return morpheme in ['-', '=']

    features = {
        'bias': 1.0,
        'morph.lower()': morph.lower(), # the morpheme itself
        'morph.isupper()': morph.isupper(), 
        'morph.istitle()': morph.istitle(), # Is the morpheme in title case?
        'morph.isdigit()': morph.isdigit(), # Is the morpheme only digits?
        'morph.length': len(morph), # the morpheme length
        'morph.is_boundary': is_boundary(morph), # Is it a morpheme boundary?
    }

    # Previous morpheme
    if i > 0:
        prev_morph = sentence[i - 1][0]
        features.update({
            '-1:morph.lower()': prev_morph.lower(), # the previous morpheme
            '-1:morph.length': len(prev_morph), # the length of the previous morpheme
        })
    else:
        features['BOS'] = True # beginning of the sentence

    # Next morpheme
    if i < len(sentence) - 1:
        next_morph = sentence[i + 1][0]
        features.update({
            '+1:morph.lower()': next_morph.lower(), # the next morpheme
            '+1:morph.length': len(next_morph), # the length of the next morpheme
            #'+1:morph.is_boundary': is_boundary(next_morph), # the next element is a morpheme boundary?
        })
    else:
        features['EOS'] = True # end of the sentence

    return features


def sent2features(sentence):
    return [morph2features(sentence, i) for i in range(len(sentence))]

def sent2labels(sentence):
    return [label for token, label in sentence]

def sent2tokens(sentence):
    return [token for token, label in sentence]
