from commands.command import MuxCommand

class CmdAbilities(MuxCommand):
    """
    List of abilities

    Usage:
      abilities

    Displays a list of your current abilities.
    """
    key = "abilities"
    aliases = ["able"]
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        "executes command"
        abilities = [
            "STR: %i" % self.caller.str(),
            "INT: %i" % self.caller.int(),
            "WIL: %i" % self.caller.wil(),
            "AGL: %i" % self.caller.agl(),
            "SPD: %i" % self.caller.spd(),
            "END: %i" % self.caller.end(),
            "PER: %i" % self.caller.per(),
            "LCK: %i" % self.caller.lck()
        ]
        self.caller.msg(", ".join(abilities))
