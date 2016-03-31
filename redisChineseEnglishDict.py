#!/usr/bin/env python3

import redis 

class RedisChineseEnglishDict:

    @staticmethod
    def key_word2logograph_set(pinyin):
        return 'word:{}:chi:logographs'.format(pinyin)
    
    @staticmethod
    def key_word2language_set(simplified):
        return 'word:{}:language'.format(simplified)
    
    @staticmethod
    def key_word2pinyin_set(simplified):
        return 'word:{}:chi:pinyin'.format(simplified)
    
    @staticmethod
    def key_word2alldefinitions_set(simplified):
        return 'word:{}:chi:definitions'.format(simplified)
    
    @staticmethod
    def key_word2posdefinitions_set(simplified, pos):
        return 'word:{}:chi:{}:eng:definitions'.format(simplified, pos)
    
    @staticmethod
    def key_word2pos_set(simplified):
        return 'word:{}:chi:partsofspeech'.format(simplified)
    
    def __init__(self, *args, **kwargs):
        self.db = redis.StrictRedis(*args, **kwargs)
        self.default_pinyin_score = 100
        self.default_logograph_score = 100
        self.default_pos_score = 100
        self.default_definition_score = 100

    def db_sadd(self, *args):
        self.db.sadd(*args)
    
    def db_zadd(self, *args):
        self.db.zadd(*args)
    
    def is_a_word(self, simp_word):
        return self.db.exists(self.key_word2language_set(simp_word))

    def lookup_entries(self, search_word):
        yield None

    def add_word_language(self, word, language):
        self.db_sadd(self.key_word2language_set(word), language)

    def add_word_pinyin(self, word, pinyin):
        self.db_zadd(self.key_word2pinyin_set(word),
                     self.default_pinyin_score, pinyin)

    def add_word_logograph(self, pinyin, simplified):
        self.db_zadd(self.key_word2logograph_set(pinyin),
                     self.default_logograph_score, simplified)

    def add_word_definition(self, simplified, pos, definition):
        self.db_zadd(self.key_word2alldefinitions_set(simplified),
                     self.default_pos_score,
                     self.key_word2posdefinitions_set(simplified, pos))
        self.db_zadd(self.key_word2posdefinitions_set(simplified, pos),
                     self.default_definition_score,
                     definition)

    def add_word_partofspeech(self, word, pos):
        self.db_sadd(self.key_word2pos_set(word), pos)

    def add_definition(self, simplified, pinyin, definition, pos='na'):
        toneless_pinyin = pinyin.translate(str.maketrans('','','12345'))
        self.add_word_language(simplified, 'chi')
        self.add_word_language(pinyin, 'chi')
        self.add_word_language(toneless_pinyin, 'chi')
        self.add_word_pinyin(simplified, pinyin)
        self.add_word_logograph(pinyin, simplified)
        self.add_word_logograph(toneless_pinyin, simplified)
        self.add_word_definition(simplified, pos, definition)
        self.add_word_partofspeech(simplified, pos)

    def definitions(self, simplified):
        if (not self.is_a_word(simplified)):
            return []
        return [definition.decode("utf-8")
                for def_type in self.db.zrange(
                        self.key_word2alldefinitions_set(simplified), 0, -1) 
                for definition in self.db.zrange(def_type, 0, -1)]

    def pinyin(self, simplified):
        if (not self.is_a_word(simplified)):
            return []
        return [pinyin.decode("utf-8")
                for pinyin in self.db.zrange(
                        self.key_word2pinyin_set(simplified), 0, -1)]
        
    
                
        

class DictEntry:
    def __init__(self, simplified, traditional='', pinyin=''):
        self.simplified   = simplified
        self.traditional  = traditional
        self.pinyin       = pinyin
        self.englishdefinitions = []
        self.classifiers  = []
        self.propername   = False
        self.part_of_speech = ''

    def as_hash(self):
        return {'simplified'         : self.simplified,
                'traditional'        : self.traditional,
                'pinyin'             : self.pinyin,
                'englishdefinitions' : '; '.join(self.englishdefinitions),
                'classifiers'        : '; '.join(self.classifiers),
                'propername'         : self.propername}

    
