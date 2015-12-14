from __future__ import print_function
import random

font_colors = {'black'         : 30,
               'red'           : 31,
               'green'         : 32,
               'yellow'        : 33,
               'blue'          : 34,
               'magenta'       : 35,
               'cyan'          : 36,
               'light_grey'    : 37,
               'grey'          : 90,
               'light_red'     : 91,
               'light_green'   : 92,
               'light_yellow'  : 93,
               'light_blue'    : 94,
               'light_magenta' : 95,
               'light_cyan'    : 96,
               'white'         : 97,
               'default'       : 39}

bg_colors = {'black'         : 40,
             'red'           : 41,
             'green'         : 42,
             'yellow'        : 43,
             'blue'          : 44,
             'magenta'       : 45,
             'cyan'          : 46,
             'light_grey'    : 47,
             'grey'          : 100,
             'light_red'     : 101,
             'light_green'   : 102,
             'light_yellow'  : 103,
             'light_blue'    : 104,
             'light_magenta' : 105,
             'light_cyan'    : 106,
             'white'         : 107,
             'default'       : 49}

styles = {'bold'      : 1,
          'underline' : 4,
          'cross_out' : 9,
          'inverse'   : 7,
          'faint'     : 2,
          'default'   : 10}

def format(string, font_col='default', bg_col='default', style='default'):
    if not(font_col in font_colors):
        font_col = 'default'
    if not(bg_col in bg_colors):
        bg_col = 'default'
    ret = string
    ret = '\x1b[%d;%d;%dm' % (font_colors[font_col], bg_colors[bg_col], styles[style]) + \
          string + '\x1b[0m'
    return ret

def black(string):
    return '\x1b[%dm' % font_colors['black'] + string +'\x1b[0m'
def red(string):
    return '\x1b[%dm' % font_colors['red'] + string +'\x1b[0m'
def green(string):
    return '\x1b[%dm' % font_colors['green'] + string +'\x1b[0m'
def yellow(string):
    return '\x1b[%dm' % font_colors['yellow'] + string +'\x1b[0m'
def blue(string):
    return '\x1b[%dm' % font_colors['blue'] + string +'\x1b[0m'
def magenta(string):
    return '\x1b[%dm' % font_colors['magenta'] + string +'\x1b[0m'
def cyan(string):
    return '\x1b[%dm' % font_colors['cyan'] + string +'\x1b[0m'
def light_grey(string):
    return '\x1b[%dm' % font_colors['light_grey'] + string +'\x1b[0m'
def grey(string):
    return '\x1b[%dm' % font_colors['grey'] + string +'\x1b[0m'
def light_red(string):
    return '\x1b[%dm' % font_colors['light_red'] + string +'\x1b[0m'
def light_green(string):
    return '\x1b[%dm' % font_colors['light_green'] + string +'\x1b[0m'
def light_yellow(string):
    return '\x1b[%dm' % font_colors['light_yellow'] + string +'\x1b[0m'
def light_blue(string):
    return '\x1b[%dm' % font_colors['light_blue'] + string +'\x1b[0m'
def light_magenta(string):
    return '\x1b[%dm' % font_colors['light_magenta'] + string +'\x1b[0m'
def light_cyan(string):
    return '\x1b[%dm' % font_colors['light_cyan'] + string +'\x1b[0m'
def white(string):
    return '\x1b[%dm' % font_colors['white'] + string +'\x1b[0m'

def bold(string):
    return '\x1b[%dm' % styles['bold'] + string + '\x1b[0m'
def underline(string):
    return '\x1b[%dm' % styles['underline'] + string + '\x1b[0m'
def cross_out(string):
    return '\x1b[%dm' % styles['cross_out'] + string + '\x1b[0m'
def inverse(string):
    return '\x1b[%dm' % styles['inverse'] + string + '\x1b[0m'
def faint(string):
    return '\x1b[%dm' % styles['faint'] + string + '\x1b[0m'
def default(string):
    return '\x1b[%dm' % styles['default'] + string + '\x1b[0m'

def bg_black(string):
    return '\x1b[%dm' % bg_colors['black'] + string +'\x1b[0m'
def bg_red(string):
    return '\x1b[%dm' % bg_colors['red'] + string +'\x1b[0m'
def bg_green(string):
    return '\x1b[%dm' % bg_colors['green'] + string +'\x1b[0m'
def bg_yellow(string):
    return '\x1b[%dm' % bg_colors['yellow'] + string +'\x1b[0m'
def bg_blue(string):
    return '\x1b[%dm' % bg_colors['blue'] + string +'\x1b[0m'
def bg_magenta(string):
    return '\x1b[%dm' % bg_colors['magenta'] + string +'\x1b[0m'
def bg_cyan(string):
    return '\x1b[%dm' % bg_colors['cyan'] + string +'\x1b[0m'
def bg_light_grey(string):
    return '\x1b[%dm' % bg_colors['light_grey'] + string +'\x1b[0m'
def bg_grey(string):
    return '\x1b[%dm' % bg_colors['grey'] + string +'\x1b[0m'
def bg_light_red(string):
    return '\x1b[%dm' % bg_colors['light_red'] + string +'\x1b[0m'
def bg_light_green(string):
    return '\x1b[%dm' % bg_colors['light_green'] + string +'\x1b[0m'
def bg_light_yellow(string):
    return '\x1b[%dm' % bg_colors['light_yellow'] + string +'\x1b[0m'
def bg_light_blue(string):
    return '\x1b[%dm' % bg_colors['light_blue'] + string +'\x1b[0m'
def bg_light_magenta(string):
    return '\x1b[%dm' % bg_colors['light_magent'] + string +'\x1b[0m'
def bg_light_cyan(string):
    return '\x1b[%dm' % bg_colors['light_cyan'] + string +'\x1b[0m'
def bg_white(string):
    return '\x1b[%dm' % bg_colors['white'] + string +'\x1b[0m'

def rainbow(string):
    r_col = ['red',
             'yellow',
             'light_yellow',
             'green',
             'light_blue',
             'blue',
             'magenta']
    ret = ''
    for i, char in enumerate(string):
        ret += '\x1b[%dm' % (font_colors[r_col[i % 7]])
        ret += char
    ret += '\x1b[0m'
    return ret

def get_info():
    info = bold('\nCOLORS:\n')
    for color in font_colors.keys():
        s = '%s(\'Text\') -> ' % color
        info += s.rjust(26, ' ')
        info += '\x1b[%dm' % font_colors[color] + 'Text' + '\x1b[0m'

        s = 'bg_%s(\'Text\') -> ' % color
        info += s.rjust(32, ' ')
        info += '\x1b[%dm' % bg_colors[color] + 'Text' + '\x1b[0m\n'

    info += bold('\nSTYLES:\n')
    for style in styles.keys():
        s = '%s(\'Text\') -> ' % style
        info += s.rjust(26, ' ')
        info += '\x1b[%dm' % styles[style] + 'Text' + '\x1b[0m\n'

    info += bold('\nOTHER:\n')
    info += 'format(\'Text\', font_col=\'red\', bg_col=\'yellow\', style=\'cross_out\') -> '
    info += format('Text', font_col='red', bg_col='yellow', style='cross_out')
    info += '\n'
    info += 'rainbow(\'Rainbow_String\') -> '
    info += rainbow('Rainbow_String')
    info += '\n'

    return info

def usage():
    print(get_info())
    
def help():
    print(get_info())

def info():
    print(get_info())

if __name__ == '__main__':
    print(get_info())
