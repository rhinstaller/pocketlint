Name:      python3-pocketlint
Version:   0.13
Release:   1%{?dist}
Summary:   Support for running pylint against projects

License:   GPLv2+
Url:       https://github.com/rhinstaller/pocketlint
Source0:   https://github.com/rhinstaller/pocketlint/archive/%{version}/pocketlint-%{version}.tar.gz

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-pylint
BuildRequires: python3-six

Requires: python3-polib
Requires: python3-pylint
Requires: python3-six

%description
Addon pylint modules and configuration settings for checking the validity of
Python-based source projects.

%prep
%setup -q -n pocketlint-%{version}

%build
make %{?_smp_mflags}

%install
%make_install

%check
make check

%files
%license COPYING
%{python3_sitelib}/pocketlint*egg*
%{python3_sitelib}/pocketlint/

%changelog
* Mon Apr 18 2016 Chris Lumens <clumens@redhat.com> - 0.13-1
- E1103 is hiding common errors (#13) (bcl)

* Thu Feb 04 2016 Chris Lumens <clumens@redhat.com> - 0.12-1
- Remove the checks for interruptible system calls. (dshea)
- Ignore E0012 messages. (clumens)

* Mon Dec 14 2015 Chris Lumens <clumens@redhat.com> - 0.11-1
- pylint changed visit_callfunc to visit_call (bcl)

* Fri Dec 04 2015 Chris Lumens <clumens@redhat.com> - 0.10-1
- Add a config property to ignore paths. (dshea)
- Remove the translated markup checks (dshea)
- Remove the commented-out markup_necessary check. (dshea)

* Thu Nov 05 2015 Chris Lumens <clumens@redhat.com> - 0.9-1
- Don't modify the locale to load translations. (dshea)

* Mon Oct 19 2015 Chris Lumens <clumens@redhat.com> - 0.8-1
- Don't bomb out on non-utf8 byte strings (dshea)

* Mon Aug 10 2015 Chris Lumens <clumens@redhat.com> - 0.7-1
- Use sys.exit instead of os._exit. (clumens)
- Add a new makefile target that does everything needed for jenkins. (clumens)

* Tue Jun 30 2015 Chris Lumens <clumens@redhat.com> - 0.6-1
- Add back checks for os.close and os.dup2 (dshea)
- Add kwargs to eintr_retry_call (dshea)
- open is an interruptable call, so wrap it with eintr_retry_call. (clumens)
- Expand the EINTR checker to a bunch more functions (dshea)
- Clean up some new pylint warnings about type vs. isinstance (bcl)

* Mon Apr 27 2015 Chris Lumens <clumens@redhat.com> - 0.5-1
- If we can't open a file to read, skip it. (clumens)

* Fri Apr 24 2015 Chris Lumens <clumens@redhat.com> - 0.4-1
- Add symbolic names of messages to the output (vpodzime)
- If we filtered out all errors as false positives, return 0. (clumens)
- Fix two instances where check_equal() returned True incorrectly. (amulhern)

* Tue Mar 17 2015 Chris Lumens <clumens@redhat.com> - 0.3-1
- Updates to pointless-override.py. (amulhern)
- Use re.search instead of re.match. (clumens)

* Tue Mar 10 2015 Chris Lumens <clumens@redhat.com> - 0.2-1
- BuildRequires python3-six too. (clumens)
- Fix up Fedora package review problems (#1200119). (clumens)
- Add translatepo from anaconda so the markup checker works. (clumens)

* Mon Mar  9 2015 Chris Lumens <clumens@redhat.com> - 0.1-1
- Initial packaging of pocketlint.
