.PHONY: help init build clean test coverage doc push_doc

help:
	@echo "Please use make <target> where <target> is one of"
	@echo "    init           : init and pull all submodules"
	@echo "    build          : build extensions (not needed yet)"
	@echo "    clean          : clean current repository"
	@echo "    test           : run tests"
	@echo "    coverage       : run tests and check code coverage"
	@echo "    doc            : build dev documentation"
	@echo "    push_doc       : push dev documentation to http://bnoi.github.io/scikit-tracker/dev/"

init:
	git submodule update --init

build:
	python setup.py build_ext --inplace

clean:
	find . -name "*.so" -o -name "*.pyc" -o -name "*.pyx.md5" -o -name "__pycache__" -exec rm -rf {} \;
	rm -rf build/ dist/ scikit_tracker.egg-info/

test:
	nosetests sktracker -v

coverage:
	nosetests sktracker --with-coverage --cover-package=sktracker -v

doc:
	cd doc/ && make clean && make api && make html

push_doc:
	cd doc/ && make clean && make api && make html
	cd doc/ && python gh-pages.py
	cd doc/gh-pages/ && git push origin gh-pages && cd ../../
