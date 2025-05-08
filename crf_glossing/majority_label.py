'''Code from gloss_lost (majority_model.py). Modified.'''
import re

from collections import Counter

# from gloss_lost.to_wapiti import LabelHandler
import crf_glossing.utils as utils


def reshape_counter(counter):
    '''Transform a counter into the following format: morph: [(label, frequency)].'''
    new_counter = dict()
    for ((morph, label), freq) in counter.items():
        if morph in new_counter: # Another label (since counter gives unique pairs)
            new_counter[morph].append((label, freq))
        else: # New morpheme, new pair
            new_counter[morph] = [(label, freq)]
    return new_counter

# Creating a dictionary with the majority label
def create_majority_dict(train_corpus, label=None):
    '''Use training data to create a dictionary of label.
    
    Training data in the IGT_Corpus object.'''
    # split_data = utils.text_to_line(train_data)
    maj_dict_list = []
    # all_morph_list = []
    # for line in split_data:
    for sentence in train_corpus.sentences:
        split_source = sentence.split_source
        split_gloss = sentence.split_gloss
        m = len(split_source)
        assert m == len(split_gloss), f'Lengths do not match: {m} and {len(split_gloss)}.'
        for j in range(m):
            maj_dict_list.append((split_source[j], split_gloss[j])) # 2
        # all_morph_list.append(split_line[0])
    maj_counter = Counter(maj_dict_list)
    # all_morph_set = set(all_morph_list)
    #print(maj_counter)
    
    # Reshape the counter
    resh_counter = reshape_counter(maj_counter)
    #print(resh_counter)

    # Keep the most frequent label only
    new_dict = dict()
    for (morph, lab_list) in resh_counter.items():
        #print(morph, lab_list)
        new_dict[morph] = lab_list[0][0]
        if len(lab_list) == 1: # Only one label
            continue
        else: # Several possible labels -> majority label
            # Initialised with the first element
            current_freq = lab_list[0][1]
            #print(current_freq)
            for j in range(1, len(lab_list)):
                if lab_list[j][1] > current_freq:
                    new_dict[morph] = lab_list[j][0]
                    current_freq = lab_list[j][1]
    return new_dict

# # Apply the majority label to the test dataset
# def majority_labelling(train, test, label_type='base'):
#     '''Apply the majority label in the training data to the test dataset.'''
#     label = LabelHandler(label_type)
#     # Create the majority dictionary from the train dataset
#     maj_dict = create_majority_dict(train, label)
#     # Label the test dataset
#     split_file = utils.text_to_line(test, empty=False)
#     #print(split_file)
#     new_file_list = []
#     count_sent = 0
#     for line in split_file:
#         if line == '': # Blank line
#             new_file_list.append(line)
#             count_sent += 1
#         else:
#             split_line = re.split(' ', line)
#             utils.check_equality(len(split_line), label.label_position) #4) #2)
#             source_morph = split_line[0]
#             if split_line[0] in maj_dict: # Known morpheme
#                 new_file_list.append(f'{line}\t{maj_dict[source_morph]}')
#             else: # Unknown morpheme
#                 new_file_list.append(f'{line}\t?') #UNKNOWN
#     print(f'There are {count_sent + 1} sentences')
#     return '\n'.join(new_file_list)

# Apply the majority label to replace stem labels
def apply_majority_label(prediction_list, majority_dictionary, corpus):
    '''Replace all predicted stem labels with the majority label.'''
    # n = len(prediction_list)
    assert len(prediction_list) == corpus.n_sent, f'Number of sentences do not match: {len(prediction_list)} and {corpus.n_sent}.'
    new_prediction = []
    for i in range(corpus.n_sent):
        sent_label_list = []
        sentence = corpus.sentences[i]
        assert len(prediction_list[i]) == len(sentence.split_source), \
                f'Number of morphemes do not match: {len(prediction_list[i])} and {len(sentence.split_source)}.'
        for j in range(len(prediction_list[i])):
            morpheme = sentence.split_source[j]
            gloss = prediction_list[i][j]
            if gloss == 'stem':
                if morpheme in majority_dictionary: # Known morpheme
                    sent_label_list.append(majority_dictionary[morpheme])
                else: # Unknown morpheme
                    sent_label_list.append('UNK')
            else:
                sent_label_list.append(prediction_list[i][j])
        new_prediction.append(sent_label_list)
    return new_prediction
