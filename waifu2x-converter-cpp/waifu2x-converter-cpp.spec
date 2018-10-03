%global gitcommitid 0529f441b7e13831ebcef3e90b1a96c58272a31e
%global shortcommit %(c=%{gitcommitid}; echo ${c:0:7})
%global date 20180401
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global libname libw2xc

Name:           waifu2x-converter-cpp
Version:        5.2
Release:        1%{?gver}%{?dist}
Summary:        C++ Image Super-Resolution for Anime-Style Art

License:        MIT
URL:            https://github.com/DeadSix27/waifu2x-converter-cpp

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{gitcommitid}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

Patch0:         %{name}-soversion.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(opencl-utils)
BuildRequires:  pkgconfig(opencv) >= 3.0.0
BuildRequires:  picojson-devel
BuildRequires:  tclap
Requires:       libw2xc%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description
Image Super-Resolution for Anime-style art using Deep Convolutional
Neural Networks.
This is a reimplementation of waifu2x (original) converter function,
in C++, using OpenCV.


%package -n     %{libname}
Summary:        %{summary} library

%description -n %{libname}
The %{libname} package contains the dynamic libraries needed for %{name}.


%package -n     %{libname}-devel
Summary:        %{summary} development files
Requires:       %{libname}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n %{libname}-devel
The %{libname}-devel package contains the development files libraries needed for 
%{libname} application support.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{gitcommitid} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

rm -rf include/picojson*
rm -rf include/tclap

%build
mkdir builddir
pushd builddir
%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON \
  -DINSTALL_MODELS:BOOL=ON

%make_build

popd


%install
%make_install -C builddir


%files
%license LICENSE OpenCV_LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}

%files -n %{libname}
%license LICENSE
%{_libdir}/%{libname}.so.*

%files -n %{libname}-devel
%license LICENSE
%{_includedir}/*.h
%{_libdir}/%{libname}.so


%changelog
* Tue Oct 02 2018 Phantom X<megaphantomx at bol dot com dot br> - 5.2-1
- Initial spec
