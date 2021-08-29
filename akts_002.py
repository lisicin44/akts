import re as re
import numpy as np
import pandas as pd


#import argparse

app_version = 'AktsApp v 0.0.2 (22.08.2021)'

def main():
    #define the logic of exe file
    app_help = InteractiveHelp()
    A = SideData('SideA')
    B = SideData('SideB')

    commands = {
        'help': app_help.gethelp,
        'quit': quit,
        'load': load,
        'dataheaders': dataheaders
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

def corey_logger(orig_foo):
    import logging
    logging.basicConfig(filename='{}.log'.format(orig_foo.__name__), level=logging.INFO)
    
    def wrapper(*args, **kwargs):
        logging.info('Ran with args: {}, and kwargs: {}'.format(args, kwargs))
        return orig_foo(*args, **kwargs)
    
    return wrapper    

def load(sidename, filepath):
    try:
        SideData.get(sidename).upd_data(filepath)
        print('Data successfully loaded to class instance')
    except KeyError:    #заготовка на будущее
        print('KeyError')

def dataheaders(sidename):
    try:
        SideData.get(sidename).dataheaders()
    except KeyError:    #заготовка на будущее
        print('KeyError')

class InteractiveHelp:
    """
    Объект для вызова интерактивной помощи
    Переменные объекта - текстовые строки помощи
    Словарь - для вызова по имени команды
    """
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
    """Создает объект для работы с введенной командой
    Принимает строку с командами. 
    Атрибуты:
    user_command - основная команда (первое слово в строке)
    user_command_args - аргументы команды (кортеж)
    user_command_args_n - количество аргументов (хз зачем, пусть будет)
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

class SideData:
    """Объект с данными сторон
    попробуем закидывать данные в словарь
    """

    #словарь для хранения инстансов
    sides_dict = {}

    def __init__(self, name):
        self.sidename = name
        self.dataloaded = False
        self.dataframesdict = dict()
        SideData.sides_dict[name] = self #ПЕРЕДЕЛАТЬ ПРОВЕ

    @corey_logger
    def upd_data(self, filepath):
        try:
            self.dataframesdict.update(pd.read_excel(filepath, sheet_name=None))
            self.dataloaded = True
        except KeyError:    #заготовка на будущее
            print('KeyError')

    def dataheaders(self):
        if self.dataloaded:
            for sheet_name, dataframe in self.dataframesdict.items():
                print(dataframe)
        else:
            print('No data loaded')

    @classmethod
    def get(cls, name):
        return cls.sides_dict[name]

    def __repr__(self):
        return 'SideData instance, name: {}, dataloaded: {}'.format(self.sidename, self.dataloaded)

if __name__ == '__main__':    
    main()