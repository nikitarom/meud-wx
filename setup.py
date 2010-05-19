"""
Created on 17.02.2010

@author: jupp
"""
from distutils.core import setup
import py2exe
               
setup(name             = "meud",
      version          = "0.0.1",
      author           = "Nikita Romashkin",
      author_email     = "romashkin.nikita@gmail.com",
      description      = "Python package for formal concept analysis",
      keywords         = ["FCA", "Concept mining", "Mathematics", "lattice theory"],
      license          = "LGPL",
      platforms        = ["Linux", "Mac OSX", "Windows XP/2000/NT"],
      windows          = ['meud.py']
      )