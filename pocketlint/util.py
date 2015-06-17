#
# Copyright (C) 2015  Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Chris Lumens <clumens@redhat.com>

import errno

# Copied from python's subprocess.py
def eintr_retry_call(func, *args):
    """Retry an interruptible system call if interrupted."""
    while True:
        try:
            return func(*args)
        except (OSError, IOError) as e:
            if e.errno == errno.EINTR:
                continue
            raise
