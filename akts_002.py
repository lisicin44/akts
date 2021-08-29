import re as re
import numpy as np
import pandas as pd
import argparse

app_version = 'AktsApp v 0.0.2 (22.08.2021)'

def main():
    #define the logic of exe file
    app_help = InteractiveHelp()

    commands = {
        'help': app_help.gethelp,
        'quit': quit
    }

    while True:
        command_response = Command(input('Please, enter the command...\n'))
        if (command_response.user_command != None) and (command_response.user_command_args != None):
            try:
                commands[command_response.user_command](*command_response.user_command_args)
            except KeyError:
                print('WARNING! '+ command_response.user_command +' is unknown command')
                app_help.gethelp()
        elif command_response.user_command != None:
            try:
                commands[command_response.user_command]()
            except KeyError:
                print('WARNING! '+ command_response.user_command +' is unknown command')
                app_help.gethelp()
        else:
            app_help.gethelp()
        
    #with pd.ExcelFile(side_A_filepath) as xls:
    #    side_A_df_dict = pd.read_excel(xls, sheet_name=None)
    #with pd.ExcelFile(side_B_filepath) as xls:
    #    side_B_df_dict = pd.read_excel(xls, sheet_name=None)

def cli_arg_parsing():
    cli_parser = argparse.ArgumentParser(name=app_version)

class InteractiveHelp:

    def __init__(self):
        self.default = 'Try using \'help\' or \'help command\' for more info'
        self.foo = 'This text describes the use of foo function'
        self.help_dict = {
                            'default' : self.default,
                            'foo' : self.foo
                                                }

    def gethelp(self, key='default'):
        print(self.help_dict.get(key, self.help_dict['default']))


class Command:
    """Создает объект для работы с введенными командами
    Принимает строку с командами.
    Атрибуты:
    user_command - основная команда (первое слово в строке)
    user_command_args - аргументы команды (кортеж)
    user_command_args_n - количество аргументов
    """
    def __init__(self, inputstring):
        self.user_command = None
        self.user_command_args = None
        self.user_command_args_n = None
        if inputstring:
            self.inputlist = inputstring.split(sep=' ')
            self.user_command = self.inputlist[0]
            if len(self.inputlist) > 1:
                self.user_command_args = tuple(self.inputlist[1:])
                self.user_command_args_n = len(self.user_command_args)


if __name__ == '__main__':    
    main()