from cx_Freeze import setup, Executable

addtional_mods = ['numpy.core._methods', 'numpy.lib.format']
setup(name = "ProjectScarberry" ,
      version = "0.1" ,
      description = "" ,
      options = {'build_exe': {'includes': addtional_mods}},
      executables = [Executable("Main.py",
                        icon="butterflybrown-64.ico")])

