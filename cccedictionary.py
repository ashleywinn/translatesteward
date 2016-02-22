#!/usr/bin/env python3

import re
import os.path

resource_dir = os.path.join(os.path.dirname(__file__), '../resources')
cedict_file = os.path.join(resource_dir, 'cedict_1_0_ts_utf-8_mdbg_20151013.txt')

class EntryParseError(Exception):
    pass

class DictEntry:
    cedict_re = re.compile(r"""(?P<traditional>[\w・，○]+)\s+
                                (?P<simplified>[\w・，○]+)\s+
                                \[(?P<pinyin>.*)\]\s+
                                /(?P<definitions>.*)/""", re.VERBOSE)

    def __init__(self, simplified, traditional='', pinyin=''):
        self.simplified   = simplified
        self.traditional  = traditional
        self.pinyin       = pinyin
        self.englishdefinitions = []
        self.classifiers  = []
        self.propername   = False

    def as_hash(self):
        return {'simplified'         : self.simplified,
                'traditional'        : self.traditional,
                'pinyin'             : self.pinyin,
                'englishdefinitions' : '; '.join(self.englishdefinitions),
                'classifiers'        : '; '.join(self.classifiers),
                'propername'         : self.propername}
    
    @classmethod
    def parse_entry_line(cls, cedict_line):
        entry = cls('')
        match = cls.cedict_re.match(cedict_line)
        if match is None: 
            raise EntryParseError("unrecognized cc-cedict entry: " + line)
        entry.simplified = match.group('simplified')
        entry.traditional = match.group('traditional')
        entry.pinyin = match.group('pinyin')
        if entry.pinyin.islower():
            entry.propername = False
        else:
            entry.propername = True
        definition_list = match.group('definitions')
        for definition in definition_list.split('/'):
            definition = definition.strip()
            if not definition.startswith('CL:'):
                entry.englishdefinitions.append(definition)
            else:
                entry.classifiers.extend(get_classifiers_from_definition(definition))
        return entry

    @classmethod
    def line_is_entry(cls, cedict_line):
        match = cls.cedict_re.match(cedict_line)
        if match is None: 
            return False
        else:
            return True

            
class ChineseSimplifiedDictionary:
    def __init__(self, dict_file=cedict_file):
        self.dict_file = dict_file

    def get_entries(self, cnt=0, start=0):
        idx = 0 
        for line in open(self.dict_file):
            if (DictEntry.line_is_entry(line)):
                idx += 1
                if (idx > start):
                    yield DictEntry.parse_entry_line(line)
                if (cnt > 0) and (idx >= cnt + start):
                    break

    def get_dict_file_entries(self, simplified):
        simplified  = simplified.strip()
        simplified_re = re.compile(r'[\w・，○]+\s+' + simplified + r'\s+')
        for line in open(self.dict_file):
            if (simplified_re.match(line)):
                yield line

    def break_into_words(self, simp_phrase):
        yield from get_recognized_components(simp_phrase, self.is_a_word, 6)

    def is_a_word(self, simp_word):
        simplified = simp_word.strip()
        simplified_re = re.compile(r'[\w・，○]+\s+' + simplified + r'\s+')
        for line in open(self.dict_file):
            if (simplified_re.match(line)):
                return True
        return False

    def lookup_dict_entries(self, search_word):
        for entry_line in self.get_dict_file_entries(search_word):
            yield DictEntry.parse_entry_line(entry_line)


def get_classifiers_from_definition(definition):
    if not definition.startswith('CL:'):
        return []
    definition = definition[3:]
    classifiers = []
    for desc in definition.split(','):
        m = re.match(r"\s*(?:\w\|)?(\w)", desc)
        if m is None:
            raise ParseError("no classifiers found: {} -> {}".format(definition, desc))
        classifiers.append(str(m.group(1)))
    return classifiers

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


def print_definitions(entry):
    print(" {} ({}):".format(entry.simplified, entry.pinyin))
    for definition in entry.englishdefinitions:
        print("     - " + definition.strip()) 

if __name__ == '__main__':
    import sys

    simp_phrase = sys.argv[1]

    ce_dict = ChineseSimplifiedDictionary()

    for word in ce_dict.break_into_words(simp_phrase):
        for word_entry in ce_dict.lookup_dict_entries(word):
            print_definitions(word_entry)
