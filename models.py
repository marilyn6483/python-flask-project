import json
from utils import log


def save(data, path):
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


def load(path):
    log.log("load ", path)
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log.log('load: s', s)
        if s:
            return json.loads(s)


class Model:

    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = '{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        # 对象实例
        return m

    @classmethod
    def all(cls):
        path = cls.db_path()
        log.log("all, path", path)
        models = load(path)
        log.log(models)

        # if models:
        #     ms = [cls.new(m) for m in models]
        #     log.log('ms: ', ms)
        #     return ms
        # return []
        if models:
            return models
        else:
            return []

    def save(self):
        models = self.all()
        models.append(self.__dict__)
        # data = [m.__dict__ for m in models]
        # log.log('data: ', data)
        path = self.db_path()
        save(models, path)

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} > \n'.format(classname, s)


class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    # def new(self, form):
    #     self.username = form.get('username', '')
    #     self.password = form.get('password', '')

    def __repr__(self):
        return '<{} name:{} passwd:{}>'.format(self.__class__.__name__, self.username, self.password)

    def validate_login(self):
        return self.username == 'gua' and self.password == '123'

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2