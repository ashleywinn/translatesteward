#! /usr/bin/env python3

import sys

def gen_redis_proto(*cmd):
    print("*{}".format(len(cmd)), end='\r\n')
    for part in cmd:
        print("${}".format(len(str(part).encode())), end='\r\n')
        print(str(part), end='\r\n')

def set(key, value):
    gen_redis_proto("SET", key, value)

def zadd(name, *args):
    gen_redis_proto("ZADD", name, *args)

def sadd(name, *args):
    gen_redis_proto("SADD", name, *args)

if __name__ == '__main__':
    import sys
    set(sys.argv[1], sys.argv[2])
