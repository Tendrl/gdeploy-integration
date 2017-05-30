Name: python-gdeploy
Version: 1.0.0
Release: 1%{?dist}
BuildArch: noarch
Summary: python gdeploy is a python wrapper for gdeploy
Source0: %{name}-%{version}.tar.gz
License: LGPLv2+
URL: https://github.com/Tendrl/python-gdeploy

BuildRequires: python2-devel
BuildRequires: python-mock
BuildRequires: python-setuptools

Requires: gdeploy

%description
Python wrapper for gdeploy

%prep
%setup

# Remove bundled egg-info
rm -rf %{name}.egg-info

%build
%{__python} setup.py build

%install
%{__python} setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%check
py.test -v python_gdeploy/tests || :

%files -f INSTALLED_FILES
%doc README.md
%license LICENSE
%{_sysconfdir}/python-gdeploy/python-gdeploy.conf

%changelog
* Tue Apr 18 2017 Rohan Kanade <rkanade@redhat.com> - 1.0.0-1
- Release python-gdeploy v1.0.0

* Mon Oct 17 2016 Timothy Asir Jeyasingh <tjeyasin@redhat.com> - 0.0.1-1
- Initial build.
