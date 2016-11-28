from cmd import Cmd


class UserInput(Cmd):

    intro = 'Welcome to log monitor shell.   Type help or ? to list commands.\n'
    prompt = '# '
    file = None

    def do_print(self, arg):
        print(arg)
