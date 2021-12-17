%global commit 11edb7a785621d507968898a100420072076d71d
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210123
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global vc_url  https://github.com/mupen64plus/%{name}

Name:           mupen64plus-rsp-cxd4
Version:        2.5.9
Release:        5%{?gver}%{?dist}
Summary:        MSP communications simulator plugin for Mupen64Plus

License:        CC0
URL:            http://www.mupen64plus.org/

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/releases/download/%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  mupen64plus-devel
Requires:       mupen64plus%{?_isa} >= 2.5.9

%description
Exemplary MSP communications simulator using a normalized VU.

This is a RSP plugin for Mupen64Plus emulator.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

cat > %{name}-env <<'EOF'
export OPTFLAGS="%{optflags}"
export LDFLAGS="$OPTFLAGS %{build_ldflags}"
export V=1
export LDCONFIG=/bin/true
export PREFIX=/usr
export LIBDIR=%{_libdir}
export INCDIR=%{_includedir}/%{name}
export SHAREDIR=%{_datadir}/%{name}
export MANDIR=%{_mandir}
export PIC=1
export PIE=1
EOF


%build
source ./%{name}-env

# It's safe to build without cleanup, object directory is not the same
%make_build -C projects/unix SSE=SSE2
%make_build -C projects/unix SSE=SSE3


%install
source ./%{name}-env
%make_install -C projects/unix SSE=SSE2 INSTALL="install -p" INSTALL_STRIP_FLAG=
%make_install -C projects/unix SSE=SSE3 INSTALL="install -p" INSTALL_STRIP_FLAG=

chmod +x %{buildroot}%{_libdir}/*/%{name}*.so


%files
%license COPYING
%doc README.md
%{_libdir}/mupen64plus/%{name}.so
%{_libdir}/mupen64plus/%{name}-sse2.so


%changelog
* Mon Jun 07 2021 Phantom X <megaphantomx at hotmail dot com> - 2.5.9-5.20210123git11edb7a
- Bump

* Tue Jan 05 2021 Phantom X <megaphantomx at hotmail dot com> - 2.5.9-4.20201215gitd4adb3d
- Update

* Wed Oct 21 2020 Phantom X <megaphantomx at hotmail dot com> - 2.5.9-3.20200917git094c664
- New snapshot

* Tue Sep 29 2020 Phantom X <megaphantomx at hotmail dot com> - 2.5.9-2.20200528gita961c71
- Use Fedora lto flags

* Thu Jun 25 2020 Phantom X <megaphantomx at hotmail dot com> - 2.5.9-1.20200528gita961c71
- Initial spec
