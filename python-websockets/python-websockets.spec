%global pypi_name websockets

%ifarch x86_64
%bcond_without tests
%endif

Name:           python-%{pypi_name}
Version:        12.0
Release:        100%{?dist}
Summary:        Implementation of the WebSocket Protocol for Python

License:        BSD-3-Clause
URL:            https://github.com/aaugustin/websockets
Source0:        %{url}/archive/%{version}/%{pypi_name}-%{version}.tar.gz

BuildRequires:  gcc

%if %{with tests}
BuildRequires:  python3dist(pytest)
%endif

%global _description %{expand:
websockets is a library for developing WebSocket servers and clients in
Python. It implements RFC 6455 with a focus on correctness and simplicity. It
passes the Autobahn Testsuite.

Built on top of Python’s asynchronous I/O support introduced in PEP 3156, it
provides an API based on coroutines, making it easy to write highly concurrent
applications.}

%description %{_description}

%package -n     python3-%{pypi_name}
Summary:        %{summary}
BuildRequires:  python3-devel

%description -n python3-%{pypi_name} %{_description}

%prep
%autosetup -n %{pypi_name}-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files websockets

%check
%pyproject_check_import

%if %{with tests}
# Skip some tests that require network connectivity and/or a running daemon.
# Investigate: test_server_shuts_down_* tests hang or fail on Python 3.12
%pytest -v --ignore compliance --ignore tests/sync -k "not test_explicit_host_port and not test_server_shuts_down"
%endif


%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst

%changelog
* Thu Jan 04 2024 Phantom X <megaphantomx at hotmail dot com> - 12.0-100
- 12.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 04 2023 Python Maint <python-maint@redhat.com> - 11.0.3-3
- Rebuilt for Python 3.12

* Wed Jun 28 2023 Major Hayden <major@redhat.com> - 11.0.3-2
- Switch to GitHub source to get tests
- Replace tox with pytest
- Add pyproject_check_import

* Wed Jun 28 2023 Major Hayden <major@redhat.com> - 11.0.3-1
- Update to 11.0.3

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 11.0.2-2
- Rebuilt for Python 3.12

* Tue Apr 25 2023 Julien Enselme <jujens@jujens.eu> - 11.0.2-1
- Update to 11.0.2

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 07 2022 Rommel Layco <rj.layco@gmail.com> - 10.4-1
- Update to 10.4

* Fri Aug 12 2022 Julien Enselme <jujens@jujens.eu> - 10.3-3
- Rebuild to update Python bytecode files.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 10.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jul 09 2022 Fabian Affolter <mail@fabian-affolter.ch> - 10.3-1
- Update to latest upstream release 10.3 (closes rhbz#2076066)

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 10.2-2
- Rebuilt for Python 3.11

* Tue Feb 22 2022 Fabian Affolter <mail@fabian-affolter.ch> - 10.2-1
- Update to latest upstream release 10.2 (closes rhbz#2056433)

* Thu Feb 03 2022 Carl George <carl@george.computer> - 10.1-1
- Latest upstream rhbz#2023114
- Only run tests on x86 architectures

* Wed Feb 02 2022 Carl George <carl@george.computer> - 10.0-3
- Convert to pyproject macros
- Run test suite in %%check

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Sep 10 2021 Tomas Hrnciar <thrnciar@redhat.com> - 10.0-1
- Update to 10.0
- Fixes: rhbz#2002542

* Mon Jul 19 2021 Carl George <carl@george.computer> - 9.1-1
- Latest upstream
- Resolves: rhbz#1955976

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 8.1-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 18 2020 Julien Enselme <jujens@jujens.eu> - 8.1-1
- Update to 8.1

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 8.0.2-5
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 8.0.2-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Wed Aug 21 2019 Miro Hrončok <mhroncok@redhat.com> - 8.0.2-2
- Rebuilt for Python 3.8

* Tue Aug 20 2019 Julien Enselme <jujens@jujens> - 8.0.2-1
- Update to 8.0.2

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 8.0-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 13 2019 Julien Enselme <jujens@jujens.eu> - 8.0-2
- Skip tests because it prevents rebuild for Python 3.8. They fail because tests check the number of deprecation warnings and more are raised on Python 3.8.

* Sat Jul 13 2019 Julien Enselme <jujens@jujens.eu> - 8.0-1
- Update to 8.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 20 2018 Julien Enselme <jujens@jujens.eu> - 6.0
- Update to 6.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 5.0.1-2
- Rebuilt for Python 3.7

* Sat Jun 02 2018 Julien Enselme <jujens@jujens.eu> - 5.0.1-1
- Update to 5.0.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 06 2017 Julien Enselme <jujens@jujens.eu> - 4.0.1-1
- Update to 4.0.1

* Mon Aug 21 2017 Julien Enselme <jujens@jujens.eu> - 3.4-2
- Remove tests with timeouts

* Mon Aug 21 2017 Julien Enselme <jujens@jujens.eu> - 3.4-1
- Update to 3.4

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr 05 2017 Julien Enselme <jujens@jujens.eu> - 3.3-1
- Update to 3.3

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.2-3
- Rebuild for Python 3.6

* Sun Sep 18 2016 Julien Enselme <jujens@jujens.eu> - 3.2-2
- Correct tests on Python 3.5.2

* Sun Sep 18 2016 Julien Enselme <jujens@jujens.eu> - 3.2-1
- Update to 3.2

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jun 21 2016 Julien Enselme <jujens@jujens.eu> - 3.1-1
- Update to 3.1

* Sun Feb 14 2016 Julien Enselme <jujens@jujens.eu> - 3.0-1
- Update to 3.0
- Correct build on rawhide

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 22 2015 Julien Enselme <jujens@jujens.eu> - 2.7-1
- Update to 2.7

* Thu Nov 12 2015 Kalev Lember <klember@redhat.com> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Aug 26 2015 Julien Enselme <jujens@jujens.eu> - 2.6-1
- Initial package
