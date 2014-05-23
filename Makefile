.PHONY: help init_submodule update_submodule build clean test coverage doc push_doc

help:
	@echo "Please use make <target> where <target> is one of"
	@echo "    init_submodule   : init and pull all submodules"
	@echo "    update_submodule : update all submodules"
	@echo "    build            : build extensions (not needed yet)"
	@echo "    clean            : clean current repository"
	@echo "    test             : run tests"
	@echo "    coverage         : run tests and check code coverage"
	@echo "    doc              : build dev documentation"
	@echo "    push_doc         : push dev documentation to http://bnoi.github.io/scikit-tracker/dev/"

init_submodule:
	git submodule update --init --recursive

update_submodule:
	git submodule foreach git pull

build:
	python setup.py build_ext --inplace

clean:
	find . -name "*.so" -exec rm -rf {} \;
	find . -name "*.pyc" -exec rm -rf {} \;
	find . -depth -name "__pycache__" -type d -exec rm -rf '{}' \;
	rm -rf build/ dist/ scikit_tracker.egg-info/

test:
	nosetests sktracker -v

coverage:
	nosetests sktracker --with-coverage --cover-package=sktracker -v

doc:
	cd doc/ && make clean && make api && make html

push_doc:
	cd doc/ && python gh-pages.py
	cd doc/gh-pages/ && git push origin gh-pages && cd ../../
