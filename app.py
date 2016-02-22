#! /usr/bin/env python3
from flask import Flask, jsonify, abort, make_response
from flask import redirect, url_for
import os.path
from cccedictionary import ChineseSimplifiedDictionary as CeDict
from cccecollection import CcCeCollection

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('chinese_english_dictionary_top'))

@app.route('/api')
def api_top():
    return redirect(url_for('chinese_english_dictionary_top'))

@app.route('/hi')
def say_hi():
    return redirect(url_for('chinese_english_dictionary',
                            chi_word='你好', _external=True))

@app.route('/api/chi/eng/dictionary')
def chinese_english_dictionary_top():
    collection = CcCeCollection([entry for entry 
                                 in CeDict().get_entries(20,50)])
    collection.href = url_for('chinese_english_dictionary_top', _external=True)
    for item in collection.items:
        item.href = url_for('chinese_english_dictionary', 
                            chi_word=item.entry.simplified, _external=True)
    resp = make_response(collection.as_json())
    resp.mimetype = "application/vnd.collection+json"
    return resp

@app.route('/api/chi/eng/dictionary/<chi_word>')
def chinese_english_dictionary(chi_word):
    resp = make_response(CcCeCollection(
            dict_entries=[entry for entry in
                          CeDict().lookup_dict_entries(chi_word)],
            collection_href=url_for('chinese_english_dictionary', 
                                    chi_word=chi_word, _external=True),
            item_href_callback=lambda word: url_for('chinese_english_dictionary', 
                                                    chi_word=word, _external=True)
            ).as_json())
    resp.mimetype = "application/vnd.collection+json"
    return resp

@app.route('/api/chi/eng/tokenize/<phrase>')
def chinese_english_tokenize(phrase):
    resp = make_response(CcCeCollection(
            dict_entries=[entry for word in CeDict().break_into_words(phrase) 
                                for entry in CeDict().lookup_dict_entries(word)], 
            collection_href=url_for('chinese_english_tokenize', 
                                phrase=phrase, _external=True), 
            item_href_callback=lambda word: url_for('chinese_english_dictionary', 
                                                    chi_word=word, _external=True)
            ).as_json())
    resp.mimetype = "application/vnd.collection+json"
    return resp

@app.route('/translate/v0.1/chinese/tokenize/<phrase>')
def tokenize_chinese_phrase(phrase):
    tokens = [word for word in CeDict().break_into_words(phrase)]
    return jsonify({'words': tokens})
    

@app.route('/translate/v0.1/chinese/english/<chin_word>')
def get_english_definition(chin_word):
    dict_entries = [entry.as_hash() for entry 
                    in CeDict().lookup_dict_entries(chin_word)]
    return jsonify({'dict_entries': dict_entries})



if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)
