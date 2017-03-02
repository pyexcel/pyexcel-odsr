pip freeze
nosetests --with-cov --cover-package pyexcel_odsr --cover-package tests --with-doctest --doctest-extension=.rst README.rst tests docs/source pyexcel_odsr && flake8 . --exclude=.moban.d --builtins=unicode,xrange,long
