class Model:

    @classmethod
    def db_path(cls):
        pass

    @classmethod
    def new(cls, form):
        m = form





class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        return self.username == 'gua' and self.password == '123'

    def validate_login(self):
        return len(self.username) > 2 and len(self.password) > 2