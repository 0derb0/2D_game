import json


class inJson:
    def __init__(self, file):
        self.file = file

    def new_value(self, key, value):
        with open(self.file) as f:
            file = json.load(f)
            file.update(
                {key: value}
            )
        with open(self.file, 'w') as f:
            json.dump(
                file, f,
                indent=4, ensure_ascii=False
            )

    def del_value(self, key):
        with open(self.file) as f:
            file = json.load(f)
            for i in file:
                if i == key:
                    file.pop(key)
                    break
        with open(self.file) as f:
            json.dump(
                file, f,
                indent=4, ensure_ascii=False
            )

    def get_value(self):

        class Dict(dict):
            def __new__(cls, *args, **kwargs):
                self = dict.__new__(cls, *args, **kwargs)
                self.__dict__ = self
                return self

        with open(self.file) as f:
            file = json.load(f)

        return Dict(file)