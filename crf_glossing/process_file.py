import re

import crf_glossing.utils as utils


## Process IGT files in the SIGMORPHON Shared Task format
def preprocess_translation(translation_sentence, tilde=False, lower=True):
    '''Preprocess the translation sentence.'''
    new_sentence = translation_sentence.strip()
    if lower: new_sentence = new_sentence.lower()
    new_sentence = re.sub(r'[!?\[\];:"/.(),]', ' ', new_sentence)
    new_sentence = re.sub(r'[=|$¿¡]', ' ', new_sentence) # New
    if tilde: new_sentence = re.sub(r'~', ' ', new_sentence)
    new_sentence = re.sub('--', ' ', new_sentence) # New
    new_sentence = re.sub(' - ', ' ', new_sentence) # New
    # Deal with '
    new_sentence = re.sub(" ' ", ' ', new_sentence)
    new_sentence = re.sub(" '", ' ', new_sentence)
    # Deal with other special characters
    new_sentence = re.sub(r'[\u200e“”\u200b…<>]', ' ', new_sentence) # New
    new_sentence = re.sub(' +', ' ', new_sentence)
    return new_sentence.strip()


class IGT_Corpus:
    '''Processes a corpus in the SIGMORPHON Shared Task format

    Parameters
    ----------
    corpus_file : string
        Raw corpus file
    test : bool
        Indicates whether the corpus is a test dataset or not

    Attributes
    ----------
    split_file : list [sentences (string)]
        List of all sentences in the corpus
    n_sent : int
        Number of sentences in the corpus
    sentences : list [Sentences (object)]
        List of all processed sentences using the Sentence class
    '''
    def __init__(self, corpus_file, test=False):
        self.split_file = re.split('\n\n', corpus_file)
        self.n_sent = len(self.split_file)

        print(f'There are {self.n_sent} sentences.')

        self.test = test
        if self.test:
            print(f'This corpus is a test dataset.')
        else:
            print(f'This corpus is a training dataset.')

        self.sentences = []
        self.split_uncovered()
        

    def split_uncovered(self, tilde=False, lower=True):
        '''Convert the Shared task file into three separate files.

        4 tiers:
        \t: raw source sentence
        \m: morpheme segmented sentence
        \g: gloss
        \l: translation
        If covered, there is no gloss output'''
        
        # corpus = IGT_Corpus(uncovered_file)

        for sentence in self.split_file:
            split_sentence = utils.text_to_line(sentence)
            if len(split_sentence) == 5: # 5 tiers (e.g., Uspanteko)
                #print(split_sentence)
                field_dict = {'m': 1, 'g': 3, 'l': 4}
            elif len(split_sentence) == 4: # 4 tiers
                field_dict = {'m': 1, 'g': 2, 'l': 3}
            elif len(split_sentence) == 3: # 3 tiers (e.g., Nyangbo)
                field_dict = {'m': 1, 'g': 2, 'l': -1}
            else:
                print(f'Number of tiers {len(split_sentence)} for {split_sentence}')
            #utils.check_equality(len(split_sentence), 4) # 4 tiers

            # Source sentence
            source = split_sentence[field_dict['m']].strip()
            utils.check_equality(source[0:3], '\m ')

            # Gloss sentence
            gloss = split_sentence[field_dict['g']].strip()
            if not self.test:
                utils.check_equality(gloss[0:3], '\g ')
            else: # If test dataset, gloss is not available
                gloss = '\g '

            # Translation
            if field_dict['l'] == -1: # If no translation
                translation = '\l '
            else: 
                translation = split_sentence[field_dict['l']].strip()
                utils.check_equality(translation[0:3], '\l ')
                pp_translation = preprocess_translation(translation[3:], tilde=tilde, lower=lower)

            # # Add to lists
            # self.source_list.append(source[3:])
            # self.gloss_list.append(gloss[3:])
            # self.translation_list.append(pp_translation)

            # print(source, gloss)
            self.sentences.append(Sentence(source[3:], gloss[3:], translation[3:], self.test))
        # return source_list, gloss_list, translation_list

    def convert_to_crf_format(self, stem=True, custom_dict=dict()):
        '''Convert the corpus into the CRFsuite format.'''
        return [sentence.to_crf_format(stem=stem, custom_dict=custom_dict) 
                for sentence in self.sentences]
    


class Sentence:
    '''Object to handle one sentence and its annotations.

    Parameters
    ----------
    source : string
        Sentence in the studied language (segmentation in words and morphemes)
    gloss : string
        Glossed sentence with the same number of units as the source
    translation : string
        Translation of the source sentence (raw, neither processed nor tokenised)
    test : bool
        If it is a sentence from the test dataset or not.

    Attributes
    ----------
    split_source : list [morphemes (string)]
        Source sentence split into morphemes
    split_gloss : list [glosses (string)]
        Glosses split at the morpheme level
    split_translation : list [words (string)]
        Translation split into a list of words
    n_morph : int
        Number of morphemes in the source sentence (or number of glosses)
    '''
    def __init__(self, source, gloss, translation, test=False):
        tilde=False 
        lower=True
        
        self.source = source
        self.gloss = gloss
        self.raw_translation = translation
        self.pp_translation = preprocess_translation(translation, tilde=tilde, lower=lower)
        self.test = test

        # Handle hyphen as punctuation mark
        if (' - ' in self.source) and (self.test or (' - ' in self.gloss)):
            self.source = self.source.replace(' - ', ' $$$ ')
            if not self.test:
                self.gloss = self.gloss.replace(' - ', ' $$$ ')
        if (self.source[0:2] == '- ') and (self.test or (self.gloss[0:2] == '- ')):
            self.source = '$$$' + self.source[1:]
            if not self.test:
                self.gloss = '$$$' + self.gloss[1:]

        # Split according to morpheme boundaries
        equal = True
        if equal: # Treat equal signs differently than hyphens
            split_pattern = '(-|=)' #'[ -=]'
        else:
            split_pattern = '(-)' #'[ -]'
            self.source = self.source.replace('=', '-')
            self.gloss = self.gloss.replace('=', '-')
        
        # print(self.source, self.gloss)
        split_source = [re.split(split_pattern, word) for word in self.source.split(' ')]
        self.split_source = utils.flatten_2D(split_source)
        split_gloss = [re.split(split_pattern, word) for word in self.gloss.split(' ')]
        self.split_gloss = utils.flatten_2D(split_gloss)
        self.split_translation = utils.line_to_word(self.pp_translation)

        if equal: # Treat equal signs differently than hyphens
            new_split_pattern = r'[ =-]' 
        else:
            new_split_pattern = '[ -]'
        self.morph_list = re.split(new_split_pattern, self.source)
        self.gloss_list = re.split(new_split_pattern, self.gloss)
        self.n_morph = len(self.morph_list)
        # print(self.split_source, self.split_gloss)
        # print(self.morph_list, self.gloss_list)
        if not self.test: utils.check_equality(self.n_morph, len(self.gloss_list))
    

    def to_crf_format(self, stem=False, custom_dict=dict()):
        '''Convert the sentence into the CRFsuite format.
        
        stem: indicates whether lexical glosses should be replaced by the stem label.
        custom_dict: keeps certain tags in the label set.'''
        morph_gloss_list = []
        n_unit = len(self.split_source) # Number of units (with hyphens)
        for i in range(n_unit): #self.n_morph):
            source_morph = self.split_source[i]
            if not self.test:
                gloss = self.split_gloss[i]
                # if source_morph == 'ke' and custom_dict != dict():
                #     print(source_morph, gloss, custom_dict[source_morph], custom_dict[source_morph] == gloss)
                if gloss in ['-', '=']:
                    pp_gloss = gloss
                elif gloss.isupper(): # Grammatical label (reference)
                    pp_gloss = gloss
                elif custom_dict != dict() and \
                    (source_morph in custom_dict and custom_dict[source_morph] == gloss):
                    print('Custom dictionary', source_morph, gloss)
                    pp_gloss = gloss
                else: # Lexical label
                    # if source_morph == 'ke' and custom_dict != dict():
                    #     print(custom_dict)
                    #     print(source_morph, gloss, custom_dict[source_morph])
                    if stem:
                        pp_gloss = 'stem'
                    else:
                        pp_gloss = gloss
            else:
                pp_gloss = ''
            morph_gloss_list.append((source_morph, pp_gloss))
        return morph_gloss_list


# Conversion of the output into IGT format
def convert_to_igt_format(pred_list):
        '''Convert the list of predicted labels into a list of sentences.'''
        sent_pred_list = [pred_to_igt_format(sent_list) for sent_list in pred_list]
        return sent_pred_list

def pred_to_igt_format(pred_list):
    '''Convert a list of labels (prediction) into a sentence.'''
    str_pred = re.sub(' - ', '-', ' '.join(pred_list))
    str_pred = re.sub(' = ', '=', str_pred)
    return str_pred