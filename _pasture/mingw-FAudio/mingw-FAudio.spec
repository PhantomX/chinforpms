%{?mingw_package_header}

%global commit 7eca833536c3e938a67f35bae57d7436c00f0875
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210707
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname FAudio
%global vc_url  https://github.com/FNA-XNA/%{pkgname}

Name:           mingw-%{pkgname}
Version:        21.12
Release:        1%{?gver}%{?dist}
Summary:        MinGW Windows Accuracy-focused XAudio reimplementation

License:        zlib
URL:            https://fna-xna.github.io/

%global vc_url  https://github.com/FNA-XNA/%{pkgname}
%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-binutils


%description
%{summary}.

# Win32
%package -n mingw32-%{pkgname}
Summary:        MinGW Windows Accuracy-focused XAudio reimplementation
Requires:       pkgconfig

%description -n mingw32-%{pkgname}
MinGW Windows Accuracy-focused XAudio reimplementation.

# Win64
%package -n mingw64-%{pkgname}
Summary:        MinGW Windows Accuracy-focused XAudio reimplementation
Requires:       pkgconfig

%description -n mingw64-%{pkgname}
MinGW Windows Accuracy-focused XAudio reimplementation.


%{?mingw_debug_package}


%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

sed -e '/FAudio_INSTALL_INCLUDEDIR/s| include| ${CMAKE_INSTALL_INCLUDEDIR}|g' \
  -i CMakeLists.txt


%build
%mingw_cmake \
  -DCMAKE_INSTALL_INCLUDEDIR:PATH=include/%{pkgname} \
  -DPLATFORM_WIN32:BOOL=ON \
%{nil}

%mingw_make_build


%install
%mingw_make_install

ln -sf %{pkgname}.pc %{buildroot}%{mingw32_libdir}/pkgconfig/faudio.pc
ln -sf %{pkgname}.pc %{buildroot}%{mingw64_libdir}/pkgconfig/faudio.pc


%files -n mingw32-%{pkgname}
%license LICENSE
%doc README
%{mingw32_bindir}/%{pkgname}.dll
%{mingw32_libdir}/lib%{pkgname}.dll.a
%{mingw32_libdir}/cmake/%{pkgname}/
%{mingw32_libdir}/pkgconfig/*.pc
%{mingw32_includedir}/%{pkgname}/

%files -n mingw64-%{pkgname}
%license LICENSE
%doc README
%{mingw64_bindir}/%{pkgname}.dll
%{mingw64_libdir}/lib%{pkgname}.dll.a
%{mingw64_libdir}/cmake/%{pkgname}/
%{mingw64_libdir}/pkgconfig/*.pc
%{mingw64_includedir}/%{pkgname}/


%changelog
* Sat Dec 04 2021 Phantom X <megaphantomx at hotmail dot com> - 21.12-1
- Initial spec
