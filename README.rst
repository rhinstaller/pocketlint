Pocketlint is an addon module for pylint.

Checks
------

Pocketlint contains these additional checks:

.. list-table:: Pocketlint checks
   :header-rows: 1

   * - Identifier
     - Description
   * - W9940 / environment-modify
     - Potentially thread-unsafe modification of environment using ``setenv()``
   * - W9901 / found-percent-in-_
     - ``%`` in a call to one of the ``_()`` methods results in incorrect translations
   * - W9902 / found-_-in-module-class
     - Calling ``_()`` at the module or class level results in translations to the wrong language
   * - W9910 / bad-preconf-access 
     - Accessing ``yum.preconf`` outside of ``_resetYum`` will cause tracebacks
   * - W9920 / invalid-markup
     - Pango markup could not be parsed
   * - W9921 / invalid-markup-element
     - Pango markup contains invalid elements
   * - W9922 / unescaped-markup
     - Parameters passed to ``%`` in markup not escaped
   * - W9951 / pointless-class-attribute-override
     - Assignment to class attribute that overrides assignment in ancestor that assigns identical value has no effect.
   * - W9952 / pointless-method-definition-override
     - Overriding empty method definition with another empty method definition has no effect.

Usage
-----

To use Pocketlint, place the ``pocketlint`` module directory into ``PYTHONPATH`` and run Pylint with it:

``pylint (...) --load-plugins pocketlint (...)``
