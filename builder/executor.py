class Config(object):
    pass

class Executor(object):
    def __init__(self):
        self.config = Config()

    def execute(self, commands):
        for c in commands:
            c.set_config(self.config)
            if c.check():
                continue
            try:
                c.execute()
            except BaseException as e:
                c.rollback()
                raise
