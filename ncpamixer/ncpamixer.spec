%global commit e4bdee13ffa8959a2ba052bf5b2f53e0455f8994
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230820
%bcond snapshot 0

%bcond man 1

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           ncpamixer
Version:        1.3.9
Release:        1%{?dist}
Summary:        ncurses PulseAudio Mixer

License:        MIT
URL:            https://github.com/fulhax/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(menuw)
BuildRequires:  pkgconfig(ncursesw)
BuildRequires:  pkgconfig(libpulse)
%if %{with man}
BuildRequires:  pandoc
%endif
Requires:       pulseaudio-daemon

%description
%{name} is a ncurses mixer for PulseAudio inspired by pavucontrol.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

sed  \
  -e '/MENU_LIBRARY/s|menu|menuw|g' \
  -e 's|"git" "describe" "--tags" "--dirty"|"echo" "%{version}%{?with_snapshot:-%{shortcommit}}"|g' \
  -i src/CMakeLists.txt


%build
%cmake -S src \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DBUILD_MANPAGES:BOOL=OFF \
  -DUSE_WIDE:BOOL=ON \
%{nil}

%cmake_build

%if %{with man}
pandoc -s -t man src/man/%{name}.1.md -o %{name}.1
%endif


%install
%cmake_install

%if %{with man}
mkdir -p %{buildroot}%{_mandir}/man1
install -pm0644 %{name}.1 %{buildroot}%{_mandir}/man1/
%endif


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%if %{with man}
%{_mandir}/man1/%{name}.1*
%endif


%changelog
* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 1.3.9-1
- 1.3.9

* Thu Sep 26 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.7-2
- Upstream patch to fix build

* Tue Oct 10 2023 Phantom X <megaphantomx at bol dot com dot br> - 1.3.7-1
- Initial spec

