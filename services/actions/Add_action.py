from .Abstract_action import Abstract_action


class Add_action(Abstract_action):

    def handler(self, *args):
        self.bd.save_anime(args[0], args[1], args[2])

