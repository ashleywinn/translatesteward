#! /usr/bin/env python3
from flask import Flask, jsonify, abort
import os.path
from cccedictionary import ChineseSimplifiedDictionary

app = Flask(__name__)

resource_dir = os.path.join(os.path.dirname(__file__), '../resources')
cedict_file = os.path.join(resource_dir, 'cedict_1_0_ts_utf-8_mdbg.txt')

cedict = ChineseSimplifiedDictionary(cedict_file)

@app.route('/')
def index():
    return "Hello Y'all"

@app.route('/hi')
def say_hi():
    resp = jsonify({'greeting': "你好"})
    resp.mimetype += "; charset=utf-8"
    print("Mimetype: " + resp.mimetype)
    return resp

@app.route('/translate/v0.1/chinese/tokenize/<phrase>')
def tokenize_chinese_phrase(phrase):
    tokens = [word for word in cedict.break_into_words(phrase)]
    return jsonify({'words': tokens})
    

@app.route('/translate/v0.1/chinese/english/<chin_word>')
def get_english_definition(chin_word):
    dict_entries = [entry.as_hash() for entry 
                    in cedict.lookup_dict_entries(chin_word)]
    return jsonify({'dict_entries': dict_entries})







if __name__ == '__main__':
    app.run(debug=True)
