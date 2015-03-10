Name:      python3-pocketlint
Version:   0.2
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
* Tue Mar 10 2015 Chris Lumens <clumens@redhat.com> - 0.2-1
- BuildRequires python3-six too. (clumens)
- Fix up Fedora package review problems (#1200119). (clumens)
- Add translatepo from anaconda so the markup checker works. (clumens)

* Mon Mar  9 2015 Chris Lumens <clumens@redhat.com> - 0.1-1
- Initial packaging of pocketlint.
