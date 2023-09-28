Information for generating docs
----------

Install requirements:

    pip install -r requirements.txt

Change directories into the docs folder:

    cd docs

Use [mkdocs](http://www.mkdocs.org/) structure to update the documentation. Test it locally with:

    mkdocs serve

Once the docs look good, publish to `gh-pages` branch with:

    mkdocs gh-deploy --clean

** Note **: Never edit the generated site by hand because using `gh-deploy` blows away the `gh-pages` branch and you'll lose your edits.
