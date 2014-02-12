# How to make a new release of `scikit-tracker`

- Update release notes.

  - To show a list of contributors and changes, run
    `doc/release/contribs.py <tag of prev release>`.

- Update the version number in `setup.py` and commit

- Update the docs:

  - Edit `doc/source/_static/docversions.js` and commit
  - `rm -rf build; make html` in the doc/.
  - Build gh-pages using `python gh-pages`.
  - Push upstream: `git push origin gh-pages` in `doc/gh-pages`.

- Add the version number as a tag in git::

   git tag v0.X.0

- Push the new meta-data to github::

   git push --tags origin master

- Publish on PyPi::

   python setup.py register
   python setup.py sdist upload

- Increase the version number

  - In `setup.py`, set to `0.Xdev`.
  - In `bento.info`, set to `0.X.dev0`.

- Update the web frontpage:
  The webpage is kept in a separate repo: scikit-image-web

  - Sync your branch with the remote repo: `git pull`.
    If you try to `make gh-pages` when your branch is out of sync, it
    creates headaches.
  - Update stable and development version numbers in
    `_templates/sidebar_versions.html`.
  - Add release date to `index.rst` under "Announcements".
  - Add previous stable version documentation path to disallowed paths
    in `robots.txt`
  - Build using `make gh-pages`.
  - Push upstream: `git push origin master` in `gh-pages`.

- Update the development docs for the new version `0.Xdev` just like above

- Post release notes on mailing lists, blog, G+, etc.

  - scikit-image@googlegroups.com
  - scipy-user@scipy.org
  - scikit-learn-general@lists.sourceforge.net
  - pythonvision@googlegroups.com
