# Copyright (c) Sunlight Labs, 2013 under the BSD-3 terms

all: develop test
	@echo "ready to go."

%:
	./setup.py $@

test:
	nosetests -v
	tox

docs:
	pycco larvae/schemas/*py


.PHONY: test docs install build develop all
