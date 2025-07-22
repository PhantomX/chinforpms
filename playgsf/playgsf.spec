%undefine _hardened_build

%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%global commit ad37147531e18830678856af44b2ad989e44d9cf
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20211029
%bcond snapshot 1

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           playgsf
Version:        0.7.1
Release:        1%{?dist}
Summary:        Highly Advanced GSF player linux port

License:        GPL-2.0-or-later
URL:            https://projects.raphnet.net/

%if %{with snapshot}
Source0:        https://github.com/yshui/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://projects.raphnet.net/%{name}/%{name}-%{version}.tar.gz
%endif
Source1:        https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

Patch0:         0001-build-system-updates.patch
Patch1:         0001-fix-build.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(ao)
BuildRequires:  pkgconfig(libresample)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(zlib)


%description
This is playgsf, a linux version of gsf input plugin for winamp,
Highly Advanced.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -N -p1

rm -rf libresample

find . \
  -type f \( -name '*.c*' -o -name '*.h*' -o -name '*.txt' \)  \
  -exec sed 's/\r//' -i {} ';'

%autopatch -p1

cp -p %{S:1} COPYING

autoreconf -ivf


%build
%configure \
  --disable-optimisations \
%{nil}

%make_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/


%files
%license COPYING
%doc readme.linux
%{_bindir}/%{name}


%changelog
* Sun Jan 12 2025 Phantom X <megaphantomx at hotmail dot com> - 0.7.1-1.20211029gitad37147
- Initial spec

