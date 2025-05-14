.. highlight:: shell

============
Installation
============


Stable release
--------------

To install focusedMe, run this command in your terminal:

.. code-block:: console

    $ pip install focusedme

This is the preferred method to install focusedMe, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

Platform-specific notes
-----------------------

Windows
~~~~~~~

FocusedMe on Windows uses the built-in ``winsound`` module for audio notifications, with no additional dependencies required!

macOS
~~~~~

On macOS, FocusedMe uses the built-in ``afplay`` command for audio notifications, so no additional dependencies are required.

Linux
~~~~~

On Linux systems, FocusedMe uses the ``simpleaudio`` library, which may require additional system dependencies depending on your distribution.


From sources
------------

The sources for focusedMe can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/scopeta/focusedme

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/scopeta/focusedme/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ poetry install

Alternatively, install in editable mode with pip:

.. code-block:: console

    $ pip install -e .


.. _Github repo: https://github.com/scopeta/focusedme
.. _tarball: https://github.com/scopeta/focusedme/tarball/master
