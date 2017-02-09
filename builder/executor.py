class Config(object):
    pass

class Executor(object):
    def __init__(self):
        self.config = Config()

    def execute(self, commands):
        last_command = None
        for c in commands:
            c.set_config(self.config)

            if last_command:
                c.set_input(last_command.get_output())
            last_command = c

            if c.check():
                continue

            try:
                c.execute()
            except BaseException as e:
                try:
                    c.rollback()
                except Exception:
                    pass
                raise
