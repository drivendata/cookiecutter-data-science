Generating the docs
----------

Install development requirements:

    pip install -r dev-requirements.txt

Change directories into the docs folder:

    cd docs

Use [mkdocs](https://www.mkdocs.org/) structure to update the documentation. Test locally with:

    mkdocs serve

Once the docs look good, publish to `gh-pages` branch with:

    mkdocs gh-deploy --clean

** Note **: Never edit the generated site by hand because using `gh-deploy` blows away the `gh-pages` branch and you'll lose your edits.
