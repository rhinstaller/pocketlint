%global srcname pocketlint

# python2 is not available on RHEL > 7 and not needed on Fedora > 28
%if 0%{?rhel} > 7 || 0%{?fedora} > 28
%bcond_with python2
%else
%bcond_without python2
%endif

%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_without python3
%else
%bcond_with python3
%endif

Name:      python-%{srcname}
Version:   0.18
Release:   1%{?dist}
Summary:   Support for running pylint against projects

License:   GPLv2+
Url:       https://github.com/rhinstaller/%{srcname}
Source0:   https://github.com/rhinstaller/%{srcname}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch: noarch

%description
Addon pylint modules and configuration settings for checking the validity of
Python-based source projects.

%if %{with python3}
%package -n python3-%{srcname}
Summary: Support for running pylint against projects (Python 3 version)
%{?python_provide:%python_provide python3-%{srcname}}

BuildRequires: python3-devel
BuildRequires: python3-pylint

Requires: python3-polib
Requires: python3-pylint

%description -n python3-%{srcname}
Addon pylint modules and configuration settings for checking the validity of
Python-based source projects.
%endif

%if %{with python2}
%package -n python2-%{srcname}
Summary: Support for running pylint against projects (Python 2 version)
%{?python_provide:%python_provide python2-%{srcname}}

BuildRequires: python2-devel
BuildRequires: python2-six
BuildRequires: python2-futures

%if 0%{?fedora} >= 26
BuildRequires: python2-pylint
%else
BuildRequires: pylint
%endif

Requires: python2-polib
Requires: python2-six
Requires: python2-futures

%if 0%{?fedora} >= 26
Requires: python2-pylint
%else
Requires: pylint
%endif

%description -n python2-%{srcname}
Addon pylint modules and configuration settings for checking the validity of
Python-based source projects.
%endif

%prep
%setup -q -n %{srcname}-%{version}

%build
%if %{with python2}
make PYTHON=%{__python2}
%endif
%if %{with python3}
make PYTHON=%{__python3}
%endif

%install
%if %{with python2}
make DESTDIR=%{buildroot} PYTHON=%{__python2} install
%endif
%if %{with python3}
make DESTDIR=%{buildroot} PYTHON=%{__python3} install
%endif

%check
%if %{with python2}
make PYTHON=%{__python2} check
%endif
%if %{with python3}
make PYTHON=%{__python3} check
%endif

%if %{with python3}
%files -n python3-%{srcname}
%license COPYING
%{python3_sitelib}/%{srcname}*egg*
%{python3_sitelib}/%{srcname}/
%endif

%if %{with python2}
%files -n python2-%{srcname}
%license COPYING
%{python2_sitelib}/%{srcname}*egg*
%{python2_sitelib}/%{srcname}/
%endif

%changelog
* Tue Oct 09 2018 Jiri Konecny <jkonecny@redhat.com> - 0.18-1
- Use pylint from python which starts pocketlint (jkonecny)
- Remove python six package and its usage (jkonecny)
- Add polib to setup.py dependencies (jkonecny)
- Fix requires in setup.py (jkonecny)
- Add release-pypi target to Makefile (jkonecny)
- Add missing parts to setup.py (jkonecny)

* Mon Sep 17 2018 Vojtech Trefny <vtrefny@redhat.com> - 0.17-1
- Ignore config file line printed by pylint (vtrefny)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 0.16-2
- Rebuilt for Python 3.7

* Thu Jun 07 2018 Vojtech Trefny <vtrefny@redhat.com> - 0.16-1
- Use new astroid API (vtrefny)
- Use new astroid class names (miro)
- Remove Python 2 subpackage was RHEL > 7 and Fedora > 28 (vtrefny)
- Add a new pylint executable name to check (vtrefny)
- Define "srcname" in SPEC (vtrefny)
- Fix Python 2 dependencies (vtrefny)

* Mon Apr 23 2018 Vojtech Trefny <vtrefny@redhat.com> - 0.15-4
- Remove Python 2 subpackage for RHEL > 7 and Fedora > 28

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 12 2017 Vojtech Trefny <vtrefny@redhat.com> - 0.15-1
- Add python2-pylint subpackage (vtrefny)
- Make pocketlint python2 compatible (vtrefny)
- Disable printing of score when running pylint (vtrefny)

* Mon Apr 10 2017 Chris Lumens <clumens@redhat.com> - 0.14-1
- Fix pylint name for Fedora 26 and later (#15) (jkonecny)
- Fallback to using pylint in case we didn't install from RPM (#14) (atodorov)

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
