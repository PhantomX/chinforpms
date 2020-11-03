%global commit 009570230398febf5cc531c0091371b40bcc69ac
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20201031
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           libliftoff
Version:        0.0.0
Release:        2%{?gver}%{?dist}
Summary:        Lightweight KMS plane library

License:        MIT
URL:            https://github.com/emersion/libliftoff

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  meson >= 0.52.0
BuildRequires:  gcc
BuildRequires:  pkgconfig(libdrm)


%description
libliftoff eases the use of KMS planes from userspace without standing in your way.
Users create "virtual planes" called layers, set KMS properties on them,
and libliftoff will allocate planes for these layers if possible.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{commit} -p1


%build
%meson
%meson_build


%install
%meson_install


%files
%license LICENSE
%doc README.md
%{_libdir}/%{name}.so.*

%files devel
%{_includedir}/%{name}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Mon Nov 02 2020 Phantom X <megaphantomx at hotmail dot com> - 0.0.0-2.20201031git0095702
- Bump

* Sun Oct  4 2020 Neal Gompa <ngompa13@gmail.com>
- Initial packaging
