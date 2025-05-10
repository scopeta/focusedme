=========
focusedMe
=========


.. image:: https://img.shields.io/pypi/v/focusedme.svg
        :target: https://pypi.python.org/pypi/focusedme

.. image:: https://github.com/scopeta/focusedme/actions/workflows/ci.yml/badge.svg
        :target: https://github.com/scopeta/focusedme/actions/workflows/ci.yml
        :alt: CI Status

.. image:: https://github.com/scopeta/focusedme/actions/workflows/docs.yml/badge.svg
        :target: https://scopeta.github.io/focusedme/
        :alt: Documentation




A minimalist Pomodoro timer that runs in your terminal


* Free software: MIT license
* Documentation: https://focusedme.readthedocs.io.


Installation and usage
----------------------
Install via pip
    $ pip install focusedme

Read instructions
    $ focusedme -h

Common usage (default pomodoro values)
    $ focusedme

.. image:: https://raw.githubusercontent.com/scopeta/focusedme/master/docs/images/UI.png


Overview
--------

Project Background and Description
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The goal of this project is to implement a productivity timer based on `Pomodoro <https://en.wikipedia.org/wiki/Pomodoro_Technique>`_ technique using Python programming language


The *focusedMe* module implements the basic features of a *Pomodoro* timer that runs in a terminal and provide a minimalist text-based interface. The timer provides an easy way to break down work into focused sessions, traditionally 25 minutes in length, separated by short or long breaks. Each session is known as a Pomodoro.

The timer tracks the sessions and notify the user of completion, as well as allow them to control its progress.

Features
~~~~~~~~
The timer currently includes the following features:

- Allows users to initialize the timer with default parameters (25 mins for focused sessions and long breaks, and 5 mins for short breaks)
- Tracks sessions according the *Pomodoro* technique and properly handling short and long breaks
- Updates the user in real time through a text-based interface
- Includes command line help and user options in the screen
- Plays a sound to alert the user when a session is completed and a new one is about to start
- Allows user to skip or pause a session or stop timer
- Allows user to visualize information about progress


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

`JaDogg_: <https://github.com/JaDogg/pydoro>`_ for the in_app_path function in util.py module

`TaylorSMarks: <https://github.com/TaylorSMarks/playsound>`_ for the playsound module
