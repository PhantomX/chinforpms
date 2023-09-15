%global _default_patch_fuzz 1

%global commit0 9ae4f4ae4481b1e69d38ed810980d33103544613
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20230803

%global dist .%{date}git%{shortcommit0}%{?dist}

Name:           libbacktrace
Version:        1.0
Release:        2%{?dist}
Summary:        Library to produce symbolic backtraces

License:        BSD-3-Clause
URL:            https://github.com/ianlancetaylor/%{name}

Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
Patch0:         %{url}/commit/e4f3220e535a7bc93730e50d1f10c89ef3996075.patch#/%{name}-gh-e4f3220.patch
Patch1:         %{url}/commit/f75f3eee369686694c379619a134c473982c0951.patch#/%{name}-gh-f75f3ee.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libunwind)
BuildRequires:  pkgconfig(zlib)

%description
%{name} is a C library that may be linked into a C/C++ program to produce
symbolic backtraces.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{commit0} -p1

autoreconf -ivf


%build
%configure \
  --disable-static \
  --enable-shared \
  --with-system-libunwind \
%{nil}

%make_build


%install
%make_install

find %{buildroot} -name '*.la' -delete


%files
%license LICENSE
%doc README.md
%{_libdir}/%{name}.so.*

%files devel
%doc README.md
%{_includedir}/backtrace*.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Tue Jul 18 2023 Phantom X <megaphantomx at hotmail dot com> - 1.0-1.20230328gitcdb64b6
- Initial spec
