%global _lto_cflags %{nil}
%undefine _hardened_build

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%global optflags %{optflags} -Wp,-U_GLIBCXX_ASSERTIONS
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%global commit dec85032ba4f0b37996da26157b6aa0edfc9196c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240314

%global dist .%{date}git%{shortcommit}%{?dist}

%global vc_url  https://github.com/trzy/Supermodel

%global pkgname Supermodel

Name:           supermodel
Version:        0.3~a
Release:        2%{?dist}
Summary:        A Sega Model 3 arcade emulator

License:        GPL-3.0
URL:            https://supermodel3.com/

Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
Source1:        %{name}.sh

Patch0:         0001-fix-build-flags.patch
Patch1:         0001-format-security.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(SDL2_net)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  make
Requires:       findutils


%description
Supermodel emulates Sega's Model 3 arcade platform, allowing you to relive
state-of-the-art 3D arcade gaming as it existed from 1996 through 1999.


%prep
%autosetup -n %{pkgname}-%{commit} -N -p1

rm -rf VS2008

find \( -name '*.c*' -or -name '*.h*' -or -name '*.inc' \) -exec sed -i 's/\r$//' {} \;
find \( -name 'Makefile.*' -or -name '*.txt' -or -name '*.md' \) -exec sed -i 's/\r$//' {} \;
find \( -name '*.ini' -or -name '*.xml' \) -exec sed -i 's/\r$//' {} \;

%autopatch -p1

sed \
  -e 's|eval VERSION.*$|eval VERSION = "%{version}-%{release}")|' \
  -i Makefiles/Rules.inc

cp -a %{S:1} .
sed \
  -e 's|_RPM_DATADIR_|%{_datadir}/%{name}|g' \
  -e 's|_RPM_LIBEXECPATH_|%{_libexecdir}/%{name}|g' \
  -i %{name}.sh

%build
%make_build -f Makefiles/Makefile.UNIX


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name}.sh %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_libexecdir}
install -pm0755 bin/%{name} %{buildroot}%{_libexecdir}/

mkdir -p %{buildroot}%{_datadir}/%{name}/{Assets,Config}
install -pm0644 Assets/*.bmp %{buildroot}%{_datadir}/%{name}/Assets/
install -pm0644 Config/*.{xml,ini} %{buildroot}%{_datadir}/%{name}/Config/


%files
%license Docs/LICENSE.txt
%doc README.md Docs/README.txt
%{_bindir}/%{name}
%{_libexecdir}/%{name}
%{_datadir}/%{name}/


%changelog
* Sun Jan 07 2024 Phantom X <megaphantomx at hotmail dot com> - 0.3~a-1.20231230git620a581
- Initial spec

