"""Configuration"""
# -*- coding: utf-8 -*-

import os.path
import configparser
import os

DIR = ".pymemo"
FILENAME = "config"

default_config = {
  "Main": {
    "WORK_DIR": "~/pymemo_wk",
    "BASE_ENCODE":"utf-8",
    "FILE_SIZE":"32000"
  },

  "Window": {
    "LCOLOR":"blue",
    "LCOLOR2":"green"
  }

}

CONFIG_OBJECT = None


class _Config(configparser.ConfigParser):
    """Configuration file handler"""
    def __init__(self):
        configparser.ConfigParser.__init__(self)
        # Determine config file path.
        home_dir = os.path.expanduser("~")
        dir = os.path.join(home_dir, DIR)
        self.filename = os.path.join(dir, FILENAME)
        if (not os.path.exists(dir)) or (not os.path.isdir(dir)):
            self.create_dir(dir)
        # Default.
        for section in default_config.keys():
            options = default_config[section]
            self.add_section(section)
            for key in options:
                configparser.ConfigParser.set(self, section, key, options[key])
        # Read.
        self.read([self.filename])

    def get(self, section, option):
        try:
            val = configparser.ConfigParser.get(self, section, option, raw=True)
        except configparser.NoOptionError:
            val = None
        if val=="0" or val=="1":
            val = int(val)
        return val

    def set(self, section, option, value):
        configparser.ConfigParser.set(self,section,option,str(value))
        fout = open(self.filename, "w")
        self.write(fout)
        fout.close()

    def create_dir(self, dir):
        if not os.path.isdir(dir):
            os.rename(dir, "%s.bak"%dir)
        os.mkdir(dir)


def Config():
    """Return configparser sub-object

    Only 1 instance of Config class is availabe as singleton.
    You don't need to save configuration on file, since _Conifg object's
    destructor save the info.
    """
    global CONFIG_OBJECT
    if CONFIG_OBJECT:
        return CONFIG_OBJECT
    else:
        CONFIG_OBJECT = _Config()
        return CONFIG_OBJECT


def get(section, option):
    """Return option's value"""
    return Config().get(section, option)

def set(Section, option, value):
    """Set option's value"""
    Config().set(Section, option, value)

# EOF
