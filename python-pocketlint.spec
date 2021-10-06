%global srcname pocketlint

Name:      python-%{srcname}
Version:   0.22
Release:   1%{?dist}
Summary:   Support for running pylint against projects

License:   GPLv2+
Url:       https://github.com/rhinstaller/%{srcname}
Source0:   https://github.com/rhinstaller/%{srcname}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch: noarch

%description
Addon pylint modules and configuration settings for checking the validity of
Python-based source projects.

%package -n python3-%{srcname}
Summary: Support for running pylint against projects (Python 3 version)
%{?python_provide:%python_provide python3-%{srcname}}

BuildRequires: make
BuildRequires: python3-devel
BuildRequires: python3-pylint
BuildRequires: python3-setuptools

Requires: python3-polib
Requires: python3-pylint

%description -n python3-%{srcname}
Addon pylint modules and configuration settings for checking the validity of
Python-based source projects.

%prep
%autosetup -n %{srcname}-%{version} -p1

%build
make PYTHON=%{__python3}

%install
make DESTDIR=%{buildroot} PYTHON=%{__python3} install

%check
make PYTHON=%{__python3} check

%files -n python3-%{srcname}
%license COPYING
%{python3_sitelib}/%{srcname}*egg*
%{python3_sitelib}/%{srcname}/

%changelog
* Wed Oct 06 2021 Vojtech Trefny <vtrefny@redhat.com> - 0.22-1
- Specify encoding for open() (vtrefny)
- Do not use Fedora container to GH checkout action (jkonecny)
- Sync spec with downstream (vtrefny)

* Tue Apr 20 2021 Vojtech Trefny <vtrefny@redhat.com> - 0.21-1
- spec: Remove Python 2 and make Python 3 non-optional (vtrefny)
- tests: Fix pocketlint use of removed pylint messages (bcl)
- Run tests in GitHub workflow (martin)
- Add build dependency on python3-setuptools (vtrefny)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 24 2020 Vojtech Trefny <vtrefny@redhat.com> - 0.20-5
- Add build dependency on python3-setuptools

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.20-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.20-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 30 2019 Jiri Konecny <jkonecny@redhat.com> - 0.20-1
- Fix reading pylint version (vtrefny)
- Add API to enable all C extensions (jkonecny)

* Fri Aug 30 2019 Jiri Konecny <jkonecny@redhat.com> - 0.19-6
- Replace temporary by something what will change only build not usage

* Wed Aug 28 2019 Vojtech Trefny <vtrefny@redhat.com> - 0.19-5
- Temporary mark E1121 (too-many-function-args) as false positive

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.19-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 29 2018 Jiri Konecny <jkonecny@redhat.com> - 0.19-1
- Make code more pep8 (jkonecny)
- Adapt to the new LoggingChecker class (jkonecny)
- Make bumpver lang independent (jkonecny)
- Backport spec file from dist-git (jkonecny)
- Spec file changelog date must be English (jkonecny)

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
