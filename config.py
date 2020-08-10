import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Windows = Documents\Programming Learning\Coding Temple\Class Work\Week Five\Day1

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess...'
