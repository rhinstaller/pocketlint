#!/usr/bin/python3

import sys

from pocketlint import PocketLintConfig, PocketLinter


class PocketLintPocketLintConfig(PocketLintConfig):
    @property
    def pylintPlugins(self):
        retval = super(PocketLintPocketLintConfig, self).pylintPlugins
        # We remove things from the environment, but in a safe way since
        # threads are not involved (yet).
        retval.remove("pocketlint.checkers.environ")
        return retval


if __name__ == "__main__":
    conf = PocketLintPocketLintConfig()
    linter = PocketLinter(conf)
    rc = linter.run()
    sys.exit(rc)
