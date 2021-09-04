#coding: utf-8
import os

class Env:
    def __init__(self):
        self.env_file = os.path.join(os.path.dirname(__file__), '.env')
        self.env_dict = self.read_env()

    def read_env(self):
        o = {}

        with open(self.env_file, 'r') as f:
            for line in f.readlines():
                for i, c in enumerate(line.strip()):
                    if c == "=":
                        o[ line[:i] ] = line[ (i+2) : (len(line)-2) ]
                        break
        return o

    def get(self,key):
        try:
            return self.env_dict[key]
        except KeyError:
            raise KeyError('"' + key + '"' + " not found in .env.")

getenv = Env
