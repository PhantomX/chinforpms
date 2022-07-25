%global srcname pynput

Name:               python-pynput
Version:            1.7.6
Release:            1%{?dist}
Summary:            Sends virtual input commands

License:            LGPLv3
URL:                https://pypi.org/project/pynput

Source0:            %{pypi_source}

BuildArch:          noarch

BuildRequires:      python3-devel
BuildRequires:      python3-setuptools
BuildRequires:      %{py3_dist pytest}

%global _description\
This library allows you to control and monitor input devices.\
\
Currently, mouse and keyboard input and monitoring are supported.\
\
See https://pynput.readthedocs.io/en/latest/ for the full documentation.

%description %_description

%package -n python3-pynput
Summary:            Sends virtual input commands
%{?python_provide:%python_provide python3-pynput}

%description -n python3-pynput
%{_description}


%prep
%setup -q -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install

%pyproject_save_files pynput


%check
%dnl %{__python3} setup.py test

%files -n python3-pynput -f %{pyproject_files}
%doc README.rst
%license COPYING.LGPL


%changelog
* Sun Jul 24 2022 Phantom X <megaphantomx at hotmail dot com> - 1.7.6-1
- Initial spec

