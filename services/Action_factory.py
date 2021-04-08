from .actions.Add_action import Add_action
from .actions.Set_status_action import Set_status_action
from .actions.Show_action import Show_action
from .actions.Help_action import Help_action


class Action_factory:

    def __init__(self, bot, bd):
        self.actions = {
            "/add": Add_action,
            "/set_status": Set_status_action,
            "/show":  Show_action,
            "/help": Help_action
         }
        self.bot = bot
        self.bd = bd

    def create_action(self, cmd):
        try:
            current_class = self.actions[cmd]
        except KeyError:
            current_class = None
        return current_class(self.bot, self.bd) if current_class is not None else None


