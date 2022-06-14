%global commit a38d34f15a3b79ee44b2c6f7c2e168bacdeabe35
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220416
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           nvtop
Version:        2.0.2
Release:        1%{?gver}%{?dist}
Summary:        AMD and NVIDIA GPUs htop like monitoring tool 

License:        GPLv3
URL:            https://github.com/Syllo/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(libdrm) >= 2.4.110
BuildRequires:  pkgconfig(ncursesw)


%description
Nvtop stands for Neat Videocard TOP, a (h)top like task monitor for AMD and
NVIDIA GPUs. It can handle multiple GPUs and print information about them in a
htop familiar way.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1


%build
%cmake \
%{nil}

%cmake_build


%install
%cmake_install


%files
%license COPYING
%doc README.markdown
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Sun Jun 12 2022 Phantom X <megaphantomx at hotmail dot com> - 2.0.2-1
- 2.0.2

* Sat Apr 16 2022 Phantom X <megaphantomx at hotmail dot com> - 2.0.1-1
- Initial spec
