%bcond_with tests

Name:           protontricks
Version:        1.9.2
Release:        1%{?dist}
Summary:        A simple wrapper that does winetricks things for Proton enabled games

License:        GPLv3
URL:            https://github.com/Matoking/protontricks
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

Patch10:        0001-Disable-setuptools_scm-version-check.patch

BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  python3-devel >= 3.5
BuildRequires:  %{py3_dist setuptools}
BuildRequires:  %{py3_dist vdf} >= 3.2
%if %{with tests}
BuildRequires:  %{py3_dist pytest-cov} >= 2.10
BuildRequires:  %{py3_dist pytest} >= 6.0
%endif
Requires:       winetricks

Recommends:     steam
Recommends:     wine
Recommends:     zenity


%description
%{summary}.


%prep
%autosetup -p1

echo "version = '%{version}'" > src/protontricks/_version.py

%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install

%pyproject_save_files %{name}

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-launch.desktop

%if %{with tests}
%check
%{pytest}
%endif


%files -f %{pyproject_files}
%license LICENSE
%doc CONTRIBUTING.md README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-*
%{_datadir}/applications/%{name}*.desktop


%changelog
* Mon Nov 07 2022 Phantom X <megaphantomx at hotmail dot com> - 1.9.2-1
- 1.9.2

* Thu Jun 02 2022 Phantom X <megaphantomx at hotmail dot com> - 1.8.2-1
- 1.8.2

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1.8.1-1
- 1.8.1

* Thu Nov 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1.6.1-1
- 1.6.1

* Sun Sep 05 2021 Phantom X <megaphantomx at hotmail dot com> - 1.6.0-1
- 1.6.0
- Update to best packaging practices

* Thu Jul 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1.5.2-1
- 1.5.2
- Fedora sync

* Mon Dec 28 2020 Phantom X <megaphantomx at hotmail dot com> - 1.4.3-1
- 1.4.3

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.4.1-2
- 1.4.1

* Wed Feb 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.4-1
- 1.4
- Remove git BR

* Sat Nov 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.3-1
- 1.3

* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.2.5-1
- 1.2.5

* Wed Jul 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.2.4-1
- Initial spec
