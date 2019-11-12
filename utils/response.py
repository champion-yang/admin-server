# -*- coding:utf-8 -*-


class Response(object):
    def __init__(self, code="", message="", result=""):
        self.Code = code
        self.Message = message
        self.Result = result

    def object_to_dict(self):
        return self.__dict__

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__.get(item)
        else:
            return None

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__.get(item)
        else:
            return None


if __name__ == '__main__':
    res = Response()
    print(res.object_to_dict())
