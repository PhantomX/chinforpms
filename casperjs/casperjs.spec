Name:           casperjs
Version:        1.1.4_2
Release:        3%{?dist}
Summary:        Open source navigation scripting & testing utility

License:        MIT
URL:            http://casperjs.org/

%global rversion %(c=%{version}; echo ${c//_/-})
Source0:        https://github.com/%{name}/%{name}/archive/%{rversion}/%{name}-%{version}.tar.gz
Patch0:         %{name}-path.patch

BuildArch:      noarch

BuildRequires:  python3-devel
Requires:       python3
BuildRequires:  /usr/bin/pathfix.py
Requires:       phantomjs


%description
CasperJS is an open source navigation scripting & testing utility written
in Javascript and based on PhantomJS.  It eases the process of defining a
full navigation scenario and provides useful high-level functions, methods
& syntactic sugar for doing common tasks

%prep
%autosetup -n %{name}-%{rversion} -p1

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" bin/%{name}

sed \
  -e 's|_RPM_DATADIR_|%{_datadir}|g' \
  -i bin/%{name}

%build

%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 bin/%{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/%{name}/{bin,modules,tests}
install -pm0644 package.json %{buildroot}%{_datadir}/%{name}/
install -pm0644 bin/bootstrap.js bin/usage.txt %{buildroot}%{_datadir}/%{name}/
install -pm0644 modules/*.js %{buildroot}%{_datadir}/%{name}/modules/
cp -pr tests/* %{buildroot}%{_datadir}/%{name}/tests/

%files
%license LICENSE.md
%doc CONTRIBUTORS.md README.md samples
%{_bindir}/%{name}
%{_datadir}/%{name}/package.json
%{_datadir}/%{name}/bootstrap.js
%{_datadir}/%{name}/usage.txt
%{_datadir}/%{name}/modules/*.js
%{_datadir}/%{name}/tests/*


%changelog
* Sun Jun 21 2020 Phantom X <megaphantomx at hotmail dot com> - 1.1.4_2-3
- Python3 fixes

* Mon Jan 28 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.1.4_2-2
- Fix usage.txt path

* Fri Dec 29 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.1.4_2-1
- Initial spec
