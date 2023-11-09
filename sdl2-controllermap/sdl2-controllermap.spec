Name:           sdl2-controllermap
Version:        2.28.5
Release:        1%{?dist}
Summary:        Official tool to create SDL2 Game Controller controller mappings

License:        Zlib AND MIT
URL:            http://www.libsdl.org
Source0:        %{url}/release/SDL2-%{version}.tar.gz

Patch0:         0001-controllermap-set-datadir-to-RPM-packaging.patch

BuildRequires:  gcc
BuildRequires:  pkgconfig(sdl2) >= %{version}
Requires:       SDL2%{_isa} >= %{version}


%description
%{name} is the official tool to create SDL2 Game Controller controller mappings.


%prep
%autosetup -n SDL2-%{version} -p1

sed -e 's|_RPM_DATADIR_|%{_datadir}/%{name}|g' -i test/controllermap.c


%build
%set_build_flags
$CC $CFLAGS %(pkg-config --cflags --libs sdl2) $LDFLAGS \
  test/testutils.c test/controllermap.c -o %{name}


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/%{name}
install -pm0644 test/{axis,button,controllermap*}.bmp \
  %{buildroot}%{_datadir}/%{name}/


%files
%license LICENSE.txt
%doc README-SDL.txt
%{_bindir}/%{name}
%{_datadir}/%{name}


%changelog
* Thu Nov 09 2023 Phantom X <megaphantomx at hotmail dot com> - 2.28.5-1
- 2.28.5

* Sat Sep 16 2023 Phantom X <megaphantomx at hotmail dot com> - 2.26.5-1
- 2.26.5

* Mon Mar 13 2023 Phantom X <megaphantomx at hotmail dot com> - 2.26.3-1
- 2.26.3

* Wed Nov 23 2022 Phantom X <megaphantomx at hotmail dot com> - 2.26.0-1
- 2.26.0

* Tue Sep 13 2022 Phantom X <megaphantomx at hotmail dot com> - 2.24.0-1
- 2.24.0

* Sun Apr 17 2022 Phantom X <megaphantomx at hotmail dot com> - 2.0.20-1
- 2.0.20

* Thu Dec 02 2021 Phantom X <megaphantomx at hotmail dot com> - 2.0.18-1
- 2.0.18

* Wed Aug 11 2021 Phantom X <megaphantomx at hotmail dot com> - 2.0.16-1
- 2.0.16

* Fri Jan 22 2021 Phantom X <megaphantomx at hotmail dot com> - 2.0.14-1
- 2.0.14

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.0.12-1
- 2.0.12

* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.0.10-1
- 2.0.10

* Sun Apr 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.0.9-2
- Reorder linking to fix build with as-needed

* Sat Mar  9 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.0.9-1
- Initial spec
