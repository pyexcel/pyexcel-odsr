#/bin/bash
pip freeze
nosetests --with-coverage --cover-package pyexcel_odsr --cover-package tests tests --with-doctest --doctest-extension=.rst README.rst docs/source pyexcel_odsr
