#!/usr/bin/env python3

import collectionplusjson
import cccedictionary


class CcCeItem(collectionplusjson.CpjItem):
    def __init__(self, entry, href_callback=None):
        href = ''
        if href_callback is not None:
            href=href_callback(entry.simplified)
        collectionplusjson.CpjItem.__init__(self, href=href)
        self.entry = entry
        self.data = [collectionplusjson.CpjDataElement(key, value) for key, value 
                     in self.entry.as_hash().items()]

class CcCeCollection(collectionplusjson.CollectionPlusJson):
    def __init__(self, dict_entries=[], collection_href='', item_href_callback=None):
        collectionplusjson.CollectionPlusJson.__init__(self, href=collection_href)
        self.items = [CcCeItem(entry, item_href_callback) for entry in dict_entries]


if __name__ == '__main__':
    cedict = cccedictionary.ChineseSimplifiedDictionary()
    entries = [entry for entry in cedict.get_entries(5, 15)]
    collection = CcCeCollection(entries)
    print(collection.as_json())
        
        
