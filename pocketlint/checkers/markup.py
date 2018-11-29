# Pango markup pylint module
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
from pylint.checkers.utils import check_messages
from pylint.interfaces import IAstroidChecker

import xml.etree.ElementTree as ET

from pocketlint.pangocheck import markup_nodes, is_markup

markupMethods = ["set_markup"]
escapeMethods = ["escape_markup"]

i18n_funcs = ["_", "N_", "P_", "C_", "CN_", "CP_"]
i18n_ctxt_funcs = ["C_", "CN_", "CP_"]


class MarkupChecker(BaseChecker):
    __implements__ = (IAstroidChecker,)
    name = "pango-markup"
    msgs = {"W9920" : ("Found invalid pango markup",
                       "invalid-markup",
                       "Pango markup could not be parsed"),
            "W9921" : ("Found pango markup with invalid element %s",
                       "invalid-markup-element",
                       "Pango markup contains invalid elements"),
            "W9922" : ("Found % in markup with unescaped parameters",
                       "unescaped-markup",
                       "Parameters passed to % in markup not escaped"),
           }

    # Check a parsed markup string for invalid tags
    def _validate_pango_markup(self, node, root):
        if root.tag not in markup_nodes:
            self.add_message("W9921", node=node, args=(root.tag,))
        else:
            for child in root:
                self._validate_pango_markup(node, child)

    # Attempt to parse a markup string as XML
    def _validate_pango_markup_string(self, node, string):
        try:
            # QUIS CUSTODIET IPSOS CUSTODES
            # pylint: disable=unescaped-markup
            tree = ET.fromstring("<markup>%s</markup>" % string)
        except ET.ParseError:
            self.add_message("W9920", node=node)
        else:
            # Check that all of the elements are valid for pango
            self._validate_pango_markup(node, tree)

    def __init__(self, linter=None):
        BaseChecker.__init__(self, linter)

    @check_messages("invalid-markup", "invalid-markup-element", "unescaped-markup", "unnecessary-markup")
    def visit_const(self, node):
        if not isinstance(node.value, (str, bytes)):
            return

        if not is_markup(node.value):
            return

        self._validate_pango_markup_string(node, node.value)

        # Check if this the left side of a % operation
        curr = node
        formatOp = None
        while curr.parent:
            if isinstance(curr.parent, astroid.BinOp) and curr.parent.op == "%" and \
                    curr.parent.left == curr:
                formatOp = curr.parent
                break
            curr = curr.parent

        # Check whether the right side of the % operation is escaped
        if formatOp:
            if isinstance(formatOp.right, astroid.Call):
                if getattr(formatOp.right.func, "name", "") not in escapeMethods:
                    self.add_message("W9922", node=formatOp.right)
            # If a tuple, each item in the tuple must be escaped
            elif isinstance(formatOp.right, astroid.Tuple):
                for elt in formatOp.right.elts:
                    if not isinstance(elt, astroid.Call) or\
                            getattr(elt.func, "name", "") not in escapeMethods:
                        self.add_message("W9922", node=elt)
            # If a dictionary, each value must be escaped
            elif isinstance(formatOp.right, astroid.Dict):
                for item in formatOp.right.items:
                    if not isinstance(item[1], astroid.Call) or\
                            getattr(item[1].func, "name", "") not in escapeMethods:
                        self.add_message("W9922", node=item[1])
            else:
                self.add_message("W9922", node=formatOp)


def register(linter):
    """required method to auto register this checker """
    linter.register_checker(MarkupChecker(linter))
