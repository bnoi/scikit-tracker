.PHONY: help init-submodule update-submodule build clean flake8 test coverage doc push-doc open-doc

help:
	@echo "Please use make <target> where <target> is one of"
	@echo "    init-submodule   : init and pull all submodules"
	@echo "    update-submodule : update all submodules"
	@echo "    build            : build extensions (not needed yet)"
	@echo "    clean            : clean current repository"
	@echo "    flake8           : run flake8 to check PEP8"
	@echo "    test             : run tests"
	@echo "    coverage         : run tests and check code coverage"
	@echo "    doc              : build dev documentation"
	@echo "    push-doc         : push dev documentation to http://scikit-tracker.org/dev/"

init-submodule:
	git submodule update --init --recursive

update-submodule:
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

doc-execute-notebook:
	cd doc/ && make clean && make api && make notebooks-execute && make html

push-doc:
	cd doc/ && python gh-pages.py
	cd doc/gh-pages/ && git push origin gh-pages && cd ../../

open-doc:
	xdg-open doc/build/html/index.html
