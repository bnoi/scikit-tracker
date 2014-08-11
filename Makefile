.PHONY: help init_submodule update_submodule build clean flake8 test coverage doc push_doc open_doc

help:
	@echo "Please use make <target> where <target> is one of"
	@echo "    init_submodule   : init and pull all submodules"
	@echo "    update_submodule : update all submodules"
	@echo "    build            : build extensions (not needed yet)"
	@echo "    clean            : clean current repository"
	@echo "    flake8           : run flake8 to check PEP8"
	@echo "    test             : run tests"
	@echo "    coverage         : run tests and check code coverage"
	@echo "    doc              : build dev documentation"
	@echo "    push_doc         : push dev documentation to http://scikit-tracker.org/dev/"

init_submodule:
	git submodule update --init --recursive

update_submodule:
	git submodule foreach git pull origin master

build:
	python setup.py build_ext --inplace

clean:
	find . -name "*.so" -exec rm -rf {} \;
	find . -name "*.pyc" -exec rm -rf {} \;
	find . -depth -name "__pycache__" -type d -exec rm -rf '{}' \;
	rm -rf build/ dist/ scikit_tracker.egg-info/

flake8:
	flake8 --exclude "test_*" --max-line-length=100 --count --statistics --exit-zero sktracker/

test:
	nosetests sktracker -v --logging-clear-handlers

coverage:
	nosetests sktracker --with-coverage --cover-package=sktracker -v --logging-clear-handlers

doc:
	cd doc/ && make clean && make api && make notebooks && make html

push_doc:
	cd doc/ && python gh-pages.py
	cd doc/gh-pages/ && git push origin gh-pages && cd ../../

open_doc:
	xdg-open doc/build/html/index.html
