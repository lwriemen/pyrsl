Developer Notes
===============

Bundling gen_erate
******************
pyrsl may be bundled into a self-contained file with a limited amount of external
dependencies.

To produce **gen_erate.pyz**, a python zip app that is executable and easy to
distribute to POSIX compatable operating systems where python is already
available, use the ``zipapp`` command.

::

    $ python -m pip install --upgrade --target dist .
    $ python -m zipapp --output gen_erate.pyz --python "/usr/bin/env python3" --main "rsl.gen_erate:main" --compress dist


Customizing gen_erate
*********************
pyrsl may be extended to include additional builtin functions, i.e. bridges,
and additional string formatters. The extensions may be added to your own pyz
file when invoking the setup.py bundle command:

.. code-block:: console

    $ python -m zipapp --output gen_erate.pyz --python "/usr/bin/env python3" --main "examples.customization:main" --compress dist
    $ ./gen_erate.pyz -nopersist -arch examples/customization_test.arc
    Running my custom version of gen_erate
    customization_test.arc: 4:  INFO:  the md5 of 'hello world' is 619d201e5209d3d52342cc5b6616b0cf
    customization_test.arc: 11:  INFO:  the md5 of hello world is 5eb63bbbe01eeed093cb22bb8f5acdc3

See `customization.py <https://github.com/xtuml/pyrsl/blob/master/examples/customization.py>`__
and `customization_test.arc <https://github.com/xtuml/pyrsl/blob/master/examples/customization_test.arc>`__
for more information.


Bundling gen_erate for Windows
******************************

**gen_erate.exe** may be produced by issuing the following commands from the
root of the repository on a Windows machine where ``python3`` is installed:

::

    $ python -m pip install pyinstaller
    $ python -m pip install .
    $ pyinstaller gen_erate.spec

More details on the usage of ``pyinstaller`` can be found `here <https://pyinstaller.org/en/stable/>`__.
