from distutils.core import setup
from Cython.Build import cythonize

setup(
ext_modules = cythonize(["reptileTikTok_startup.py"]), # reptileTikTok_startup.py 为需要打包的文件名，不能包含中文
)