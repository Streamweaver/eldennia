from commands.command import MuxCommand
from world.rules.rollers import simple_check

"""
Used for defining new local commands.
"""

# General Commands
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
            "DEX: %i" % self.caller.dex(),
            "END: %i" % self.caller.end(),
            "INT: %i" % self.caller.int(),
            "EDU: %i" % self.caller.edu(),
            "SOC: %i" % self.caller.soc()
        ]
        self.caller.msg(", ".join(abilities))

class CmdCheck(MuxCommand):
    """
    Checks against an attirbute:

    Usage:
        check <stat> (ex. 'check str')

    Returns success or failure for an attibute check.
    """
    key = "check"
    aliases = []
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        errmsg = "You must check one of str, dex, end, int, edu, soc"
        try:
            stat = self.args
            stat = stat.lower()
            f = getattr(self.caller, stat)
            val = f()
            msg = "%s(%i) check Failed" % (stat.upper(), val)
            if simple_check(val):
                msg = "%s(%i) check Success!" % (stat.upper(), val)
            self.caller.msg(msg)
            return
        except IndexError:
            self.caller.msg("No attribute provided: " + errmsg)
            return
        except AttributeError:
            self.caller.msg("Did not recognize attribute %s: " % stat + errmsg)
            return


