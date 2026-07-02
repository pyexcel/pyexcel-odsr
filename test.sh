#/bin/bash
pip freeze
coverage run -m --source=pyexcel_odsr pytest --doctest-modules && coverage report --show-missing
