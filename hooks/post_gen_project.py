import os
import shutil

DIRS = ['src/models']
CWD = os.getcwd()

if '{{ cookiecutter.include_starter_proj|lower }}' == 'n':
    shutil.rmtree(os.path.join(CWD, 'tests'))
    for directory in DIRS:
        files_path = os.path.join(CWD, directory)
        for fin in os.listdir(files_path):
            if fin.endswith('.py'):
                open(os.path.join(CWD, files_path, fin), 
                    'w').close()
