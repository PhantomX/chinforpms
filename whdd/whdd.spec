%global optflags %{optflags} -D_GNU_SOURCE

Name:           whdd
Version:        3.0.1
Release:        1%{?dist}
Summary:        HDD diagnostic and data recovery tool 

License:        GPL-3.0-only
URL:            https://whdd.github.io

Source0:        https://github.com/%{name}/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

Patch0:         %{name}-cmake-cflags.patch

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  dialog-devel
BuildRequires:  pkgconfig(menuw)
BuildRequires:  pkgconfig(ncursesw)
BuildRequires:  pkgconfig(tinfo)
Requires:       smartmontools

%description
%{summary}.

%prep
%autosetup -p1


%build
%cmake \
  -DDIALOG_INCLUDE_DIR:PATH=/usr/include/dialog \
%{nil}

%cmake_build


%install
%cmake_install


%files
%license COPYING LICENSE
%doc README
%{_sbindir}/%{name}


%changelog
* Tue Nov 09 2021 Phantom X <megaphantomx at bol dot com dot br> - 3.0.1-1
- 3.0.1

* Sat Jan 05 2019 Phantom X <megaphantomx at bol dot com dot br> - 3.0-1
- Initial spec
