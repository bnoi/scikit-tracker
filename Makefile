build:
	python setup.py build_ext --inplace

clean:
	find . -name "*.so" -o -name "*.pyc" -o -name "*.pyx.md5" | xargs rm -f

test:
	nosetests sktracker

coverage:
	nosetests sktracker --with-coverage --cover-package=sktracker

push_dev_doc:
	cd doc/ && make api && make html && python gh-pages.py
	cd doc/gh-pages/ && git push origin gh-pages && cd ../../
