%global optflags %{optflags} -D_GNU_SOURCE

Name:           whdd
Version:        3.0
Release:        1%{?dist}
Summary:        HDD diagnostic and data recovery tool 

License:        GPLv3
URL:            https://whdd.github.io

Source0:        https://github.com/%{name}/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

Patch0:         %{name}-cmake-cflags.patch

BuildRequires:  cmake
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
%cmake . -B %{_target_platform} \
  -DDIALOG_INCLUDE_DIR:PATH=/usr/include/dialog \
%{nil}

%make_build -C %{_target_platform}


%install
%make_install -C %{_target_platform}


%files
%license COPYING LICENSE
%doc README
%{_sbindir}/%{name}


%changelog
* Sat Jan 05 2019 Phantom X <megaphantomx at bol dot com dot br> - 3.0-1
- Initial spec
