from datetime import datetime
import json


class inJson:
    def __init__(self, file):
        self.file = file

    def new_value(self, value):
        with open(self.file) as f:
            file = json.load(f)
            indexes = []
            for i in file:
                try:
                    index_now = i.split('t')
                    print(index_now)
                    indexes.append(int(index_now[1]))
                except IndexError:
                    indexes.append(int(index_now[0]))
            try:
                index = max(indexes) + 1
            except ValueError:
                index = 1
            finally:
                indexes.clear()
                name = f'result{index}'
            file.update(
                {name: {
                    'date': f'{datetime.now()}',
                    'result': value
                }}
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

        def inner(func):
            with open(self.file) as f:
                file = json.load(f)
            result = Dict(file)
            func(result)

        return inner





