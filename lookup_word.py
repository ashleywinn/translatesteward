#!/usr/bin/env python3

import re
import os.path

resource_dir = os.path.join(os.path.dirname(__file__), 'resources')
cedict_file = os.path.join(resource_dir, 'cedict_1_0_ts_utf-8_mdbg.txt')


def is_a_word(simp_word):
    simplified = simp_word.strip()
    simplified_re = re.compile(r'[\w・，○]+\s+' + simplified + r'\s+')
    for line in open(cedict_file):
        if (simplified_re.match(line)):
            return True
    return False

def get_recognized_components(text, recognizer, max_len=100):
    while len(text) > 1:
        for i in range(len(text), 0, -1):
            if i >= max_len: continue
            if i == 1:
                yield text[0]
                text = text[1:]
                break
            if recognizer(text[0:i]):
                yield text[0:i]
                text = text[i:]
                break
    if len(text):
        yield text

        
def phrase_to_words(simp_phrase):
    yield from get_recognized_components(simp_phrase, is_a_word, 6)
    

def find_simplified_entries(simp_word):
    simplified  = simp_word.strip()

    simp_word_re = re.compile(r"""(?P<traditional>[\w・，○]+)\s+""" + 
                              simplified + r'\s+' +
                              r"""\[(?P<pinyin>.*)\]\s+/(?P<english>.*)/""", 
                              re.VERBOSE)

    for line in open(cedict_file):
        if line.startswith('#'): continue
        match = simp_word_re.match(line)
        if match is None: continue

        traditional = match.group('traditional')
        pinyin      = match.group('pinyin')
        english     = match.group('english')
        definitions = english.split('/')

        yield (simplified, traditional, pinyin, definitions)


def parse_cedict_file(filename):
    chinese_re = re.compile(r"""(?P<traditional>[\w・，○]+)\s+
                                (?P<simplified>[\w・，○]+)\s+
                                \[(?P<pinyin>.*)\]\s+
                                /(?P<english>.*)/""", re.VERBOSE)

    for line in open(filename):
        if line.startswith('#'): continue
        match = chinese_re.match(line)
        if match is None: continue

        traditional = match.group('traditional')
        simplified  = match.group('simplified')
        pinyin      = match.group('pinyin')
        english     = match.group('english')
        definitions = english.split('/')

        yield (simplified, traditional, pinyin, definitions)


def print_definitions(simp_word):
    found = False
    for dict_entry in find_simplified_entries(simp_word):
        found = True
        print(" {} ({}):".format(simp_word, dict_entry[2]))
        for definition in dict_entry[3]:
            print("     - " + definition.strip()) 
    if not found:
        print(" {} not found".format(simp_word))

if __name__ == '__main__':
    import sys

    simp_phrase = sys.argv[1]

    for word in phrase_to_words(simp_phrase):
        print_definitions(word)
