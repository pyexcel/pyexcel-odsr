isort $(find pyexcel_odsr -name "*.py"|xargs echo) $(find tests -name "*.py"|xargs echo)
black -l 79 pyexcel_odsr
black -l 79 tests
