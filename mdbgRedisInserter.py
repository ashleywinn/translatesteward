#!/usr/bin/env python3

import mdbgCedict
import redisImporter
import redisChineseEnglishDict

class RedisImporterCedict(redisChineseEnglishDict.RedisChineseEnglishDict):
    def db_set(self, key, value):
        redisImporter.set(key, value)
    
    def db_sadd(self, *args):
        redisImporter.sadd(*args)
    
    def db_zadd(self, *args):
        redisImporter.zadd(*args)
    

def importMdbgFile(filename):
    mdbgdict = mdbgCedict.MdbgCedict(filename)
    redisdict = RedisImporterCedict(host='not_used')
    for line in mdbgdict.get_all_entries():
        entry = mdbgCedict.MdbgDictEntry.parse_entry_line(line)
        for definition in entry.englishdefinitions:
            redisdict.add_definition(simplified=entry.simplified,
                                     pinyin=entry.pinyin,
                                     pos=entry.partofspeech,
                                     definition=definition)

if __name__ == '__main__':
    import sys
    try:
        importMdbgFile(sys.argv[1])
    except (BrokenPipeError, IOError):
        pass
    sys.stderr.close()
