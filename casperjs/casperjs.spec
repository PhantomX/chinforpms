Name:           casperjs
Version:        1.1.4_2
Release:        1%{?dist}
Summary:        Open source navigation scripting & testing utility

License:        MIT
URL:            http://casperjs.org/

%global rversion %(c=%{version}; echo ${c//_/-})
Source0:        https://github.com/%{name}/%{name}/archive/%{rversion}/%{name}-%{version}.tar.gz
Patch0:         %{name}-path.patch

BuildArch:      noarch

BuildRequires:  python2-devel
Requires:       python2
Requires:       phantomjs

%description
CasperJS is an open source navigation scripting & testing utility written
in Javascript and based on PhantomJS.  It eases the process of defining a
full navigation scenario and provides useful high-level functions, methods
& syntactic sugar for doing common tasks

%prep
%autosetup -n %{name}-%{rversion} -p1

sed \
  -e 's|/usr/bin/env python|%{__python2}|' \
  -e 's|_RPM_DATADIR_|%{_datadir}|g' \
  -i bin/%{name}

%build

%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 bin/%{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/%{name}/{bin,modules,tests}
install -pm0644 package.json %{buildroot}%{_datadir}/%{name}/
install -pm0644 bin/bootstrap.js bin/usage.txt %{buildroot}%{_datadir}/%{name}/bin/
install -pm0644 modules/*.js %{buildroot}%{_datadir}/%{name}/modules/
cp -pr tests/* %{buildroot}%{_datadir}/%{name}/tests/

%files
%license LICENSE.md
%doc CONTRIBUTORS.md README.md samples
%{_bindir}/%{name}
%{_datadir}/%{name}/package.json
%{_datadir}/%{name}/bin/*
%{_datadir}/%{name}/modules/*.js
%{_datadir}/%{name}/tests/*


%changelog
* Fri Dec 29 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.1.4_2-1
- Initial spec
