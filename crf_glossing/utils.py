import re


# def delete_value_from_vector(vector, value):
#     '''Delete a given value from a vector.

#     To be used only when the value is in the vector.
#     '''
#     if value in vector:
#         vector.remove(value)
#         return vector
#     else:
#         raise ValueError('The asked value is not in the vector.')

# def text_to_line(raw_text):
#     r'''Split a raw text into a list of sentences (string) according to '\n'.'''
#     split_text = re.split('\n', raw_text)
#     if '' in split_text: # To remove empty lines
#         return delete_value_from_vector(split_text, '')
#     else:
#         return split_text

# Splitting functions
def text_to_line(raw_text, empty=True):
    r'''Split a raw text into a list of sentences (string) according to '\n'.'''
    split_text = re.split('\n', raw_text)
    if '' in split_text and empty: # To remove empty lines
        split_text.remove('')
    else:
        pass
    return split_text

def line_to_word(raw_line):
    '''Split a sentence into a list of words (string) according to whitespace.'''
    return re.split(' ', raw_line)

# Checking functions
def check_equality(value_left, value_right):
    '''Check that both given values are equal.'''
    assert (value_left == value_right), ('Both values must be equal; '
                         f'currently {value_left} and {value_right}.')

# Useful functions
def flatten_2D(list_of_list):
    '''Flatten a 2D list (list of list).'''
    return [element for element_list in list_of_list for element in element_list]

# Save text file
def save_file(text, path):
    '''Save a text file in the desired path.'''
    with open(path, 'w', encoding = 'utf8') as out_text:
        out_text.write(text)

# Preprocessing functions
def remove_excessive_whitespace(string):
    '''Remove excessive whitespace.'''
    return re.sub(' +', ' ', string)
