# Base classes for pocketlint
#
# Copyright (C) 2015  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Chris Lumens <clumens@redhat.com>
#

from __future__ import print_function

import atexit
import concurrent.futures
import os
import re
import shutil
import subprocess
import sys
import tempfile

from distutils.version import LooseVersion


class PocketLintConfig(object):
    """Configuration object that a project should use to tell pylint how
       to operate.  Instance attributes:

       falsePositives -- A list of FalsePositive objects for filtering
                         incorrect pylint error messages.
    """
    def __init__(self):
        self.falsePositives = []

    @property
    def disabledOptions(self):
        """A list of warning and error codes that pylint should ignore
           when checking source code.  The base PocketLintConfig object
           comes with a pretty useful list, but subclasses can feel free
           to add or remove as desired.  This list should strive to be empty,
           though.
        """
        return [ "W0110",           # map/filter on lambda could be replaced by comprehension
                 "W0123",           # Use of eval
                 "W0141",           # Used builtin function %r
                 "W0142",           # Used * or ** magic
                 "W0212",           # Access to a protected member %s of a client class
                 "W0511",           # Used when a warning note as FIXME or XXX is detected
                 "W0603",           # Using the global statement
                 "W0613",           # Unused argument %r
                 "W0614",           # Unused import %s from wildcard import
                 "E0012",           # Bad inline option given to pylint
                 "I0011",           # Locally disabling %s
                 "I0012",           # Locally enabling %s
                 "I0013",           # Ignoring entire file
               ]

    @property
    def extraArgs(self):
        """Extra command line arguments that should be passed to pylint.  These
           arguments will be added after the default ones so they can override
           the base config, but may in turn also be overridden by arguments
           passed to the testing framework on the command line.
        """
        return []

    @property
    def initHook(self):
        """Python code to be run by pylint as part of an init hook.  Most
           projects will not need this.
        """
        return ""

    @property
    def pylintPlugins(self):
        """A list of plugins provided by PocketLint to be added to the set of
           pylink checkers.  Not all of these will be relevant to all projects,
           but they should still be able to run without error.  If necessary,
           projects can modify this list as needed.
        """
        return [ "pocketlint.checkers.environ",
                 "pocketlint.checkers.intl",
                 "pocketlint.checkers.markup",
                 "pocketlint.checkers.pointless-override",
                 "pocketlint.checkers.preconf",
               ]

    @property
    def ignoreNames(self):
        """A set of names to skip when automatically determining the list of
           files to lint. The items in this set could be a particular filename
           to skip or a directory that the linter should not traverse into.
           The items should be just basenames, not paths.
        """
        return set()


class FalsePositive(object):
    """An object used in filtering out incorrect results from pylint.  Pass in
       a regular expression matching a pylint error message that should be
       ignored.  This object can also be used to keep track of how often it is
       used, for auditing that false positives are still useful.
    """
    def __init__(self, regex):
        self.regex = regex
        self.used = 0


class PocketLinter(object):
    """Main class that does the hard work of running pylint on a project.
       Pass an instance of PocketLintConfig to a new instance of this class
       and then call its run method.  This is all that should be necessary for
       most projects:

       from pocketlint import PocketLintConfig, PocketLinter

       class FooLintConfig(PocketLintConfig):
          ....

       if __name__ == "__main__":
           conf = FooLintConfig()
           linter = PocketLinter(conf)
           rc = linter.run()
           os._exit(rc)
    """
    def __init__(self, config):
        self._config = config
        self._pylint_log = False

        # If top_srcdir is set, assume this is being run from automake and we don't
        # need to keep a separate log.
        if "top_srcdir" not in os.environ:
            self._pylint_log = True

    def _del_xdg_runtime_dir(self):
        shutil.rmtree(os.environ["XDG_RUNTIME_DIR"])

    @property
    def _files(self):
        retval = []

        srcdir = os.environ.get("top_srcdir", os.getcwd())

        for (root, dirnames, files) in os.walk(srcdir):
            # Filter out the names to ignore
            for i in self._config.ignoreNames:
                if i in dirnames:
                    dirnames.remove(i)
                if i in files:
                    files.remove(i)

            for f in files:
                try:
                    with open(root + "/" + f) as fo:
                        lines = fo.readlines()
                except UnicodeDecodeError:
                    # If we couldn't open this file, just skip it.  It wasn't
                    # going to be valid python anyway.
                    continue

                if "# pylint: skip-file\n" in lines:
                    continue

                # Test any file that either ends in .py or contains #!/usr/bin/python
                # in the first line.
                if f.endswith(".py") or (lines and str(lines[0]).startswith("#!/usr/bin/python")):
                    retval.append(root + "/" + f)

        return retval

    @property
    def _pylint_args(self):
        args = [ "--msg-template='{msg_id}({symbol}):{line:3d},{column}: {obj}: {msg}'",
                 "-r", "n",
                 "--disable", "C,R",
                 "--rcfile", "/dev/null",
                 "--dummy-variables-rgx", "_",
                 "--ignored-classes", "DefaultInstall,Popen,QueueFactory,TransactionSet",
                 "--defining-attr-methods", "__init__,grabObjects,initialize,reset,start,setUp",
                 "--load-plugins", ",".join(self._config.pylintPlugins),
                 "--deprecated-modules", "string,regsub,TERMIOS,Bastion,rexec",
                 "--disable", ",".join(self._config.disabledOptions),
               ]

        if self._config.initHook:
            args += ["--init-hook", self._config.initHook]

        if self._config.extraArgs:
            args += self._config.extraArgs

        # since 1.7 pylint by default prints "score", we need to disable it
        if self._pylint_version >= LooseVersion("1.7.0"):
            args += ["-s", "n"]

        return args

    def _command_exists(self, exc):
        proc = subprocess.Popen(["which", exc],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _out, _err = proc.communicate()
        return proc.returncode == 0

    @property
    def _pylint_executable(self):
        return [sys.executable, "-m", "pylint"]

    @property
    def _pylint_version(self):
        exc = self._pylint_executable
        exc.append("--version")
        proc = subprocess.Popen(exc, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, _stderr) = proc.communicate()
        pattern = re.compile(r"%s (?P<version>[1-9.]+)" % exc)
        match = pattern.search(stdout.decode())
        if match:
            return LooseVersion(match.group("version"))
        else:
            return LooseVersion("0")

    def _parseArgs(self):
        # Really stupid argument processing - strip off the first argument (that's
        # the program name) and then anything starting with a dash is an argument to
        # pylint, and anything else is a file to check.  We don't want this program
        # to have much more in the way of argument processing because the user should
        # do configuration via a LintConfig object.
        args = []
        files = []

        if len(sys.argv) > 1:
            for arg in sys.argv[1:]:
                if arg.startswith("-"):
                    args.append(arg)
                else:
                    files.append(arg)

        return (args, files)

    def _setupEnvironment(self):
        # We need top_builddir to be set so we know where to put the pylint analysis
        # stuff.  Usually this will be set up if we are run via "make test" but if
        # not, hope that we are at least being run out of the right directory.
        builddir = os.environ.get("top_builddir", os.getcwd())

        # XDG_RUNTIME_DIR is "required" to be set, so make one up in case something
        # actually tries to do something with it.
        if "XDG_RUNTIME_DIR" not in os.environ:
            d = tempfile.mkdtemp()
            os.environ["XDG_RUNTIME_DIR"] = d
            atexit.register(self._del_xdg_runtime_dir)

        # Unset TERM so that things that use readline don't output terminal garbage.
        if "TERM" in os.environ:
            os.environ.pop("TERM")

        # Don't try to connect to the accessibility socket.
        os.environ["NO_AT_BRIDGE"] = "1"

        # Force the GDK backend to X11.  Otherwise if no display can be found, Gdk
        # tries every backend type, which includes "broadway", which prints an error
        # and keeps changing the content of said error.
        os.environ["GDK_BACKEND"] = "x11"

        # Save analysis data in the pylint directory.
        os.environ["PYLINTHOME"] = builddir + "/tests/pylint/.pylint.d"
        if not os.path.exists(os.environ["PYLINTHOME"]):
            os.mkdir(os.environ["PYLINTHOME"])

    def _filterFalsePositives(self, filename, lines):
        if not self._config.falsePositives:
            return lines

        retval = []

        for line in lines:
            # This is not an error message.  Ignore it.
            if line.startswith("*****") or line.startswith("Using config file") or not line.strip():
                continue
            else:
                validError = True

                for regex in self._config.falsePositives:
                    if re.search(regex.regex, line):
                        # The false positive was hit, so record that and ignore
                        # the message from pylint.
                        regex.used += 1
                        validError = False
                        break

                # If any false positive matched the error message, it's a valid
                # error from pylint.  Add it to what we're going to return.
                if validError:
                    retval.append(line)

        # If any errors were found, add the header line with the name of the file
        # (instead of the name of the module) and return the list.
        if retval:
            retval.insert(0, "************* Module " + filename)

        return retval

    def _run_one(self, filename, args):
        proc = subprocess.Popen(self._pylint_executable + self._pylint_args + args + [filename],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = proc.communicate()
        output = stdout + stderr

        lines = self._filterFalsePositives(filename, output.decode("utf-8").split("\n"))
        if lines:
            return ("\n".join(lines), proc.returncode)

        return ("", 0)

    def _print(self, s, fo=None):
        print(s)
        sys.stdout.flush()
        if fo:
            print(s, file=fo)
            fo.flush()

    def run(self):
        retval = 0

        self._setupEnvironment()

        (args, files) = self._parseArgs()

        if not files:
            files = self._files

        if self._pylint_log:
            fo = open("pylint-log", "w")
        else:
            fo = None

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            jobs = []
            for f in files:
                jobs.append(executor.submit(self._run_one, f, args))

            for job in concurrent.futures.as_completed(jobs):
                result = job.result()

                output = result[0].strip()
                if output:
                    self._print(output, fo)

                if result[1] > retval:
                    retval = result[1]

        unusedFPs = []

        for fp in self._config.falsePositives:
            if fp.used == 0:
                unusedFPs.append(fp.regex)

        if unusedFPs:
            self._print("************* Unused False Positives Found:", fo)

            for fp in unusedFPs:
                self._print(fp, fo)

        return retval
