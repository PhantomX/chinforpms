%global commit b8bb91495631078fb795ec627bb6286b1041158c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200422
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global binname OpenJazz

Name:           openjazz
Version:        20171024
Release:        4%{?gver}%{?dist}
Summary:        A re-implemetantion of a known platform game engine

License:        GPL-2.0-or-later
URL:            http://www.alister.eu/jazz/oj/

%global vc_url  https://github.com/AlisterT/%{name}
%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  perl-podlators
BuildRequires:  pkgconfig(libmodplug)
BuildRequires:  pkgconfig(sdl)
BuildRequires:  pkgconfig(zlib)
%if 0%{?with_snapshot}
BuildRequires:  autoconf
BuildRequires:  automake
%endif
Requires:       hicolor-icon-theme

%description
%{summary}.


%prep
%autosetup -n %{name}-%{?gver:%{commit}}%{!?gver:%{version}} -p0

pod2man -r "%{binname} %{version}" unix/%{binname}.6.pod > %{binname}.6

sed -e 's|"/."|"/.local/share/%{name}/"|' -i src/main.cpp

cat > %{binname}.wrapper <<'EOF'
#!/usr/bin/sh
set -e
mkdir -p ${HOME}/.local/share/%{name}
cd ${HOME}/.local/share/%{name}
exec %{_bindir}/%{binname}.bin "$@"
EOF

%if 0%{?with_snapshot}
sed -e '/AC_INIT/s|\[0\]|[%{version}]|g' -i configure.ac
autoreconf -ivf
%endif

%build
export CPPFLAGS="-DDATAPATH=\\\"%{_datadir}/%{name}/\\\" -DHOMEDIR"
%configure \
  --disable-silent-rules
%make_build


%install
%make_install

mv %{buildroot}%{_bindir}/%{binname} %{buildroot}%{_bindir}/%{binname}.bin
install -pm0755 %{binname}.wrapper %{buildroot}%{_bindir}/%{binname}

mkdir -p %{buildroot}%{_mandir}/man6
install -pm0644 %{binname}.6 %{buildroot}%{_mandir}/man6/

desktop-file-validate %{buildroot}%{_datadir}/applications/%{binname}.desktop


%files
%license COPYING licenses.txt
%doc README.md
%{_bindir}/%{binname}
%{_bindir}/%{binname}.bin
%{_datadir}/applications/%{binname}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/%{name}/%{name}.000
%{_mandir}/man6/%{binname}.6*


%changelog
* Tue Dec 01 2020 Phantom X <megaphantomx at hotmail dot com> - 20171024-4.20200422gitb8bb914
- Bump

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 20171024-3.20190505git030119c
- Bump

* Thu Nov 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 20171024-2.20180913git61a24c6
- New snapshot
- Drop desktop file, now installed by default
- Add manpage. BR: perl-podlators

* Mon Mar 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 20171024-1.20180219gitaf172ec
- Initial spec
