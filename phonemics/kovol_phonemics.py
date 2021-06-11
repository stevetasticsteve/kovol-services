#! /usr/bin/python3

import re

consonants = [
    'p', 't', 'k', 'ʔ',
    'b', 'd', 'g',
    'm', 'n', 'ŋ',
    'β', 's',
    'r', 'l',
    'w', 'j'
]

# include both ɑ and a to catch spelling inconsistencies
vowels = [
    'i', 'ɪ', 'e', 'ɛ',
    'u', 'o', 'ɔ', 'ɑ', 'a'
]

glides = ['ɑⁱ', 'aⁱ', 'eⁱ', 'oᵘ']

other_valid_characters = [' ']

valid_characters = consonants + vowels + glides + other_valid_characters
vv = re.compile('[{v}][{v}]'.format(v=''.join(vowels)))

ccc = re.compile('[{c}][{c}][{c}]'.format(c=''.join(consonants)))


def check_phonetic_inventory(string):
    """checks to make sure no unexpected characters are fed into the program"""
    for i, character in enumerate(string):
        # if it's a glide include the base character
        if character == 'ⁱ' or character == 'ᵘ':
            character = string[i - 1] + character
        if character not in valid_characters:
            raise ValueError(
                'Unexpected character: "{c}" in {s}'.format(
                    c=character, s=string))
        if ccc.search(string):
            raise ValueError(
                'A CCC cluster was found in "{word}"'.format(word=string))


def insert_epenthetic_semivowels(string):
    """insert either i or u in CC clusters involving a semi vowel"""
    sv_cluster = [re.compile('[{c}][jw]'.format(c=''.join(consonants))),  # SV intial
                  re.compile('[jw][{c}]'.format(c=''.join(consonants)))]  # SV final

    for cluster in sv_cluster:
        while cluster.search(string):
            match = cluster.search(string)
            match_pos = match.end()  # Identify index of match

            # pick the right epenthetic vowel
            if 'j' in match.group():
                epenthetic_vowel = 'i'
            elif 'w' in match.group():
                epenthetic_vowel = 'u'
            else:  # no SV
                raise ValueError

            # Insert epenthetic vowel
            string = string[:match_pos - 1] + \
                epenthetic_vowel + string[match_pos - 1:]

    return string


def interpret_phonetics(string):
    """Apply the interpretive decisions made in our phonemic write up to a
    target string."""
    string = string.strip('[]')
    check_phonetic_inventory(string)

    # check for VV clusters
    while vv.search(string):
        match = vv.search(string)
        match_pos = match.end()  # Identify index of match
        # sanity check that we are in fact dealing with iV clusters
        if match.group()[0] != 'i':
            raise ValueError('VV cluster not starting with [i]')
        # Insert Semivowel
        string = string[:match_pos - 2] + 'j' + string[match_pos - 1:]

    # check for glides, remove any resulting CCC clusters
    if 'eⁱ' in string:
        string = string.replace('eⁱ', 'ej')
        while ccc.search(string):
            match = ccc.search(string)
            string = string[:match.end() - 2] + 'i' + string[match.end() - 2:]
    if 'oᵘ' in string:
        string = string.replace('oᵘ', 'ow')
        while ccc.search(string):
            match = ccc.search(string)
            string = string[:match.end() - 2] + 'u' + string[match.end() - 2:]

    # insert epenthetic SVs
    # string = insert_epenthetic_semivowels(string)

    return string


def replace_characters(replacement_tuple, string):
    for i, o in replacement_tuple:
        string = string.replace(i, o)
    return string


def analyse_phonetics(string):
    """Apply analytical decisions to interpreted phonetic string"""
    replacements = (('r', 'l'), ('k', 'ʔ'), ('ɔ', 'o'), ('ɪ', 'i'))

    return replace_characters(replacements, string)


def use_orthography(string):
    """Change phonemic text into orthographic"""
    replacements = (('ɑ', 'a'), ('ⁱ', 'i'), ('ɛ', 'ə'),
                    ('β', 'v'), ('ʔ', 'k'),
                    # catch funky clusters resulting from replace
                    ('ŋ', 'ng'), ('nng', 'ng'), ('ngg', 'ng'),
                    ('j', 'y'))

    return replace_characters(replacements, string)


def phonetics_to_orthography(string):
    """Go all the way from phonetics to orthography"""
    inter = interpret_phonetics(string)
    analy = analyse_phonetics(inter)
    orth = use_orthography(analy)

    return orth
    