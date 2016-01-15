#!/usr/bin/env python3

import simplejson as json

class CpjJsonFormatError(Exception):
    pass

class CpjDataElement:
    def __init__(self, name, value=None, prompt=None):
        self.name   = name
        self.value  = value
        self.prompt = prompt

    def for_json(self):
        my_dict = {'name' : self.name}
        if (self.value is not None):
            my_dict['value'] = self.value
        if (self.prompt is not None):
            my_dict['prompt'] = self.prompt
        return my_dict


class CpjItem:
    def __init__(self, href=None):
        self.href  = href
        self.data  = []
        self.links = []

    def for_json(self):
        my_dict = {'href'   : self.href}
        if len(self.data) > 0:
            my_dict['data'] = self.data 
        if len(self.links) > 0:
            my_dict['links'] = self.links
        return my_dict

    def add_data_from_dict(self, data):
        for (key, value) in data.items():
            self.data.append(CpjDataElement(name=key, value=value))


class CpjQuery:
    def __init__(self, href, rel, name=None, prompt=None, data=[]):
        self.href = href
        self.rel = rel
        self.name = name
        self.prompt = prompt
        self.data = data

    def for_json(self):
        my_dict = {'href' : self.href,
                   'rel'  : self.rel}
        if self.name is not None:
            my_dict['name'] = self.name
        if self.prompt is not None:
            my_dict['prompt'] = self.prompt
        if len(self.data) > 0:
            my_dict['data'] = self.data
        return my_dict


class CpjLink:
    def __init__(self, href, rel, name=None, prompt=None, render=None):
        self.href = href
        self.rel = rel
        self.name = name
        self.prompt = prompt
        self.data = data

    def for_json(self):
        my_dict = {'href' : self.href,
                   'rel'  : self.rel}
        if self.name is not None:
            my_dict['name'] = self.name
        if self.prompt is not None:
            my_dict['prompt'] = self.prompt
        if self.render is not None:
            my_dict['render'] = self.render
        return my_dict


class CpjTemplate:
    def __init__(self, data):
        self.data = data

    def for_json(self):
        my_dict['data'] = self.data
        return my_dict


class CpjError:
    def __init__(self, title=None, code=None, message=None):
        self.title = title
        self.code = code
        self.message = message

    def for_json(self):
        my_dict = {}
        if title is not None:
            my_dict['title'] = self.title
        if code is not None:
            my_dict['code'] = self.code
        if message is not None:
            my_dict['message'] = self.message
        return my_dict


class CollectionPlusJson:
    def __init__(self, href, links=[], items=[], queries=[], template=None, error=None):
        self.version = 1.0
        self.href  = href
        self.links = links
        self.items = items
        self.queries = queries
        self.template = template
        self.error = error

    def as_json(self):
        return json.dumps({'collection': self}, for_json=True)

    def for_json(self):
        my_dict = {'version': self.version,
                   'href'   : self.href}
        if len(self.links) > 0:
            my_dict['links'] = self.links
        if len(self.items) > 0:
            my_dict['items'] = self.items
        if len(self.queries) > 0:
            my_dict['queries'] = self.queries
        if self.template is not None:
            my_dict['template'] = self.template
        if self.error is not None:
            my_dict['error'] = self.error
        return my_dict

if __name__ == '__main__':
    import sys

    first_arg = sys.argv[1]


