# How to make a new release of `scikit-tracker`

- Update release notes.

  - To show a list of contributors and changes, run
    `doc/release/contribs.py <tag of prev release>`.

- Update the version number in `setup.py` and commit

- Update the docs:

  - Edit `doc/source/_static/docversions.js` and commit
  - `rm -rf build; make html` in the doc/.
  - Build gh-pages using `python gh-pages`.
  - Push upstream:
    - `cd gh-pages/ && git push origin gh-pages`.

- Add the version number as a tag in git::

   git tag v0.X.0

- Push the new meta-data to github::

   git push --tags origin master

- Publish on PyPi::

   python setup.py register
   python setup.py sdist upload

- Increase the version number

  - In `setup.py`, set to `dev`.

- Update the development docs for the new version `0.X-dev` just like above
