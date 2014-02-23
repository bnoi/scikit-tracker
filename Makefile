.PHONY: help build clean test coverage push_dev_doc

help:
	@echo "Please use make <target> where <target> is one of"
	@echo "    build          : build extensions (not needed yet)"
	@echo "    clean          : clean current repository"
	@echo "    test           : run tests"
	@echo "    coverage       : run tests and check code coverage"
	@echo "    push_dev_doc   : push dev documentation on internet"

build:
	python setup.py build_ext --inplace

clean:
	find . -name "*.so" -o -name "*.pyc" -o -name "*.pyx.md5" | xargs rm -f

test:
	nosetests sktracker -v

coverage:
	nosetests sktracker --with-coverage --cover-package=sktracker -v

push_dev_doc:
	cd doc/ && make api && make html && python gh-pages.py
	cd doc/gh-pages/ && git push origin gh-pages && cd ../../
