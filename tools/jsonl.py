import json
import gzip


class JW:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.fp = open(self.path, 'w')
        return self

    def dump(self, obj):
        return self.fp.write(json.dumps(obj) + '\n')

    def __exit__(self, type, value, traceback):
        self.fp.close()


class JR:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.fp = open(self.path, 'r')
        return self._object_yielder()

    def _object_yielder(self):
        for line in self.fp:
            if type(line) == str:
                yield json.loads(line)
            else:
                yield json.loads(line.decode('utf-8'))

    def __exit__(self, type, value, traceback):
        self.fp.close()


class JWZ:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.fp = gzip.open(self.path, 'w')
        return self

    def dump(self, obj):
        return self.fp.write((json.dumps(obj) + '\n').encode('utf-8'))

    def __exit__(self, type, value, traceback):
        self.fp.close()


class JRZ:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        self.fp = gzip.open(self.path, 'r')
        return self._object_yielder()

    def _object_yielder(self):
        for line in self.fp:
            yield json.loads(line.decode('utf-8'))

    def __exit__(self, type, value, traceback):
        self.fp.close()
