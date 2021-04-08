from .Abstract_action import Abstract_action

class Show_action(Abstract_action):

    def handler(self, *args):
        self.bd.show(args[0])
