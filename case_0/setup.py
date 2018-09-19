from distutils.core import setup, Extension

setup(name="fastcopy",
      version="0.0.1",
      py_modules = ["fastcopy.py"],
      ext_modules = [
          Extension("_fastcopy",
                    ["fastcopy.cpp", "fastcopymodule.cpp"])
      ]
)