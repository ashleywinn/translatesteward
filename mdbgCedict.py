#!/usr/bin/env python3

import re
import os.path

resource_dir = os.path.join(os.path.dirname(__file__), '../resources')
cedict_file = os.path.join(resource_dir, 'cedict_1_0_ts_utf-8_mdbg_20151013.txt')

class EntryParseError(Exception):
    pass

class MdbgCedict:
    def __init__(self, dict_file=cedict_file):
        self.dict_file = dict_file

    def get_entries_for_simplified(self, simplified):
        for line in self.get_entry_lines_for_simplified(simplified):
            yield MdbgDictEntry.parse_entry_line(line)

    def get_entry_lines_for_simplified(self, simplified):
        simplified  = simplified.strip()
        simplified_re = re.compile(r'[\w・，○]+\s+' + simplified + r'\s+')
        for line in open(self.dict_file):
            if (simplified_re.match(line)):
                yield line

    def get_all_entries(self):
        n_char_re = re.compile(r'[\w・，○]+\s+[\w・，○]+\s+\[')
        for line in open(self.dict_file):
            if (n_char_re.match(line)):
                yield line
                
    def get_n_char_entries(self, num_chars):
        n_char_re = re.compile(r'[\w・，○]+\s+\w{'+ str(num_chars) + r'}\s+')
        for line in open(self.dict_file):
            if (n_char_re.match(line)):
                yield line

    def get_count_of_n_char_entries(self, num_chars):
        cnt = 0
        for line in self.get_n_char_entries(num_chars):
            cnt += 1
        return cnt
                

class MdbgDictEntry:
    cedict_re = re.compile(r"""(?P<traditional>[\w・，○]+)\s+
                                (?P<simplified>[\w・，○]+)\s+
                                \[(?P<pinyin>.*)\]\s+
                                /(?P<definitions>.*)/""", re.VERBOSE)

    def __init__(self, simplified, traditional='', pinyin=''):
        self.simplified   = simplified
        self.traditional  = traditional
        self._pinyin      = pinyin
        self.englishdefinitions = []
        self.classifiers  = []
        self.propername   = False

    @property
    def partofspeech(self):
        if (not self.pinyin.islower()):
            return 'pn'
        else:
            return 'na'

    @property
    def pinyin(self):
        return self._pinyin

    @pinyin.setter
    def pinyin(self, value):
        self._pinyin = value.replace(' ','')

    @property
    def pinyin_no_tones(self):
        return self._pinyin.translate(
            str.maketrans('','','12345'))

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


if __name__ == '__main__':
    import sys

    mdbg = MdbgCedict()

    for n in range(1, 20):
        cnt = mdbg.get_count_of_n_char_entries(n)
        print("For {} character long words there are {} entries".format(n, cnt))
    
