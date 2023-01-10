%global commit a38d34f15a3b79ee44b2c6f7c2e168bacdeabe35
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220416
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           nvtop
Version:        3.0.1
Release:        1%{?gver}%{?dist}
Summary:        AMD and NVIDIA GPUs htop like monitoring tool 

License:        GPL-3.0-only
URL:            https://github.com/Syllo/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  make
BuildRequires:  pkgconfig(libdrm) >= 2.4.110
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(ncursesw)
Requires:       hicolor-icon-theme


%description
Nvtop stands for Neat Videocard TOP, a (h)top like task monitor for AMD and
NVIDIA GPUs. It can handle multiple GPUs and print information about them in a
htop familiar way.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

sed -e '/icon/s| type="stock"||g' -i desktop/%{name}.metainfo.xml.in


%build
%cmake \
%{nil}

%cmake_build


%install
%cmake_install

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
mv %{buildroot}%{_datadir}/icons/%{name}.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/


%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license COPYING
%doc README.markdown
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/%{name}.svg
%{_mandir}/man1/%{name}.1*
%{_metainfodir}/%{name}.metainfo.xml


%changelog
* Tue Jan 10 2023 Phantom X <megaphantomx at hotmail dot com> - 3.0.1-1
- 3.0.1

* Sun Jun 12 2022 Phantom X <megaphantomx at hotmail dot com> - 2.0.2-1
- 2.0.2

* Sat Apr 16 2022 Phantom X <megaphantomx at hotmail dot com> - 2.0.1-1
- Initial spec
