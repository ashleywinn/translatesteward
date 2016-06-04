#!/usr/bin/env python3

import sys
from os import environ
from utils import split_into_lines
from redisChineseEnglishDict import RedisChineseEnglishDict

wide_space = '\N{IDEOGRAPHIC SPACE}'

if len(sys.argv) > 1:
    phrase = ' '.join(sys.argv[1:])
else:
    phrase = '太棒'

redis_db = environ.get('CEDICT_DB_HOST', default='localhost')

try:
    (host, port, db, *j) = redis_db.split(':')
    cedict = RedisChineseEnglishDict(host=host, port=port, db=db)
except ValueError:
    try:
        (host, port) = redis_db.split(':')
        cedict = RedisChineseEnglishDict(host=host, port=port)
    except ValueError:
        cedict = RedisChineseEnglishDict(host=redis_db)

print('\n' + phrase + '\n')
for word in cedict.break_into_words(phrase):
    if not cedict.is_a_word(word):
        print(word)
        continue
    definition_lines = [line for line in
                        split_into_lines('; '.join(cedict.definitions(word)), 60)]
    print('{}{} {:<12} {}'.format(word, wide_space * (5 - len(word)),
                                  cedict.pinyin(word)[0],
                                  definition_lines[0]))
    for line in definition_lines[1:]:
        print('{}{} {}'.format(wide_space * 5,' ' * 13, line))

    

