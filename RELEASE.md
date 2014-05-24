# How to make a new release of `scikit-tracker`

- Update release notes in doc/source/release/
- Update doc/source/new.txt to add new release notes

- Update the version number in:
    - `README.md`
    - `doc/source/_static/docversions.js`
    - `sktracker/version.py` and commit

- Commit

- Pull git submodule to build doc : `make init_submodule`
- Build doc : `make doc`

- Check doc is ok lcoally and then push doc : `make push_doc`

- Add the version number as a tag in git : `git tag v0.X.0`
- Push the new meta-data to github : `git push --tags origin master`

- Create release on Github so zenodo can create and update DOI

- Publish on PyPi :

```sh
   python setup.py register
   python setup.py sdist upload
```

- Increase the version number in `sktracker/version.py` and `dev` suffix.
- Update the development docs for the new version `0.X-dev` just like above
- Push the new dev doc

- Go drink a beer, you deserved it :-)
