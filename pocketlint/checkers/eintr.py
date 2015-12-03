# Interuptible system call pylint module
#
# Copyright (C) 2014  Red Hat, Inc.
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
# Red Hat Author(s): David Shea <dhsea@redhat.com>
#

import astroid

from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages, safe_infer
from pylint.interfaces import IAstroidChecker

import os

# These are most of the calls listed in PEP 0475 as being interruptible prior
# to Python 3.5.  Ignore time.sleep, since it just returns early instead of
# raising an exception.  For select.*.poll and select.kqueue.control, just hope
# that anyone using them knows what they're getting into because the objects
# returned by the select module cannot be inferred.
interruptible = { "_io": ("open",),
                  "io": ("open",),
                  "faulthandler": ("dump_traceback", "enable", "disable", "is_enabled",
                                   "dump_traceback_later", "cancel_dump_traceback_later",
                                   "register", "unregister"),
                  "os": ("fchdir", "fchmod", "fchown", "fdatasync", "fstat", "fstatvfs",
                         "fsync", "ftruncate", "mkfifo", "mknod", "open", "posix_fadvise",
                         "posix_fallocate", "pread", "pwrite", "read", "readv", "sendfile",
                         "wait3", "wait4", "wait", "waitid", "waitpid", "write", "writev"),
                  "select": ("select",),
                  "socket": ("accept", "connect", "recv", "recvfrom", "recvmsg", "send",
                             "sendall", "sendmsg", "sendto"),
                  "signal": ("sigtimedwait", "sigwaitinfo") }

# These two are slightly different, since they can raise EINTR but should not be retried
ignorable = { "os": ("close", "dup2") }

class EintrChecker(BaseChecker):
    __implements__ = (IAstroidChecker,)
    name = "retry-interruptible"
    msgs = {"W9930" : ("Found interruptible system call %s",
                       "interruptible-system-call",
                       "A system call that may raise EINTR is not wrapped in eintr_retry_call"),
            "W9931" : ( "Found interruptible (ignore) system call %s",
                        "ignorable-system-call",
                        "A system call that may raise EINTR is not wrapped in eintr_ignore"),
           }

    @check_messages("interruptible-system-call", "ignorable-system-call")
    def visit_call(self, node):
        if not isinstance(node, astroid.CallFunc):
            return

        # Try to figure out the module. os redirects most of its
        # content to an OS-dependent module, named os.name, so if the module
        # is that, pretend it's os.
        function_node = safe_infer(node.func)
        if not isinstance(function_node, astroid.Function):
            return

        module_name = function_node.root().name
        if module_name == os.name:
            module_name = "os"

        # Look for the function in the known interruptible functions
        if module_name in interruptible and function_node.name in interruptible[module_name]:
            self.add_message("interruptible-system-call", node=node, args=function_node.name)
        elif module_name in ignorable and function_node.name in ignorable[module_name]:
            self.add_message("ignorable-system-call", node=node, args=function_node.name)

def register(linter):
    """required method to auto register this checker """
    linter.register_checker(EintrChecker(linter))
