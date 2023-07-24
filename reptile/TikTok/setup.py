from distutils.core import setup
from Cython.Build import cythonize


setup(
    ext_modules=cythonize(["sendData_startup.py", "sendData.py", "reptileTikTok_startup.py", "pop_up_box.py", "reptileTikTok.py"]),  # add.py 为需要打包的文件名，不能包含中文
)