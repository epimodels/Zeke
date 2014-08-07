Deploying Zeke: Local Development Server - Mac OS X and Linux
=================================

The easiest way to deploy *Zeke* for testing and prototyping is using Django's built in webserver, which while only single threaded should be sufficient for most testing, evaluation and development purposes.

Setting Up Your Environment
-----
* Configure a virtual environment using virtualenv, conda, or another tool.
* Install SciPy. We recommend using distribution such as Enthough's *Canopy*, or Continuum's *Anaconda* for ease of installation.

Set A Secret Key
-------
Django requires a "secret key", and for security reasons, this is not hard coded and accessible within the GitHub repository. Instead, *Zeke* looks for an environmental variable called <code>SECRET\_KEY</code> and assigns that value to be the Django secret key. In the appropriate bash config file (for example, .bash\_profile) and enter the following:

	export SECRET_KEY='abcdefg'

Replacing abcdefg with something more appropriate. Restart your shell.

Install Requirements and Launch Django Server
------
With your virtual environment activated, and in the appropriate directory, enter the following commands while in the shell:

	pip install -r requirements.txt
	django-admin.py syncdb --settings=zeke.settings.dev
	
Note this step will fail if you have not appropriately set <code>SECRET\_KEY</code>. If you have not previously created a database for Zeke, it will ask to make one. Follow the prompts. Finally, type

	django-admin.py runserver --settings=zeke.settings.dev

In the shell. You should now have a server running at localhost on port 8000. Note that, even for local development, you'll want to be connected to the internet, as much of the UI, as well as MathJax support, pulls from remote resources.