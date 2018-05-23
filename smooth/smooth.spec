%global prerel 1

%if 0%{?prerel}
%global prereltag .pre%{prerel}
%global prereltarball -pre%{prerel}
%endif

Name:           smooth
Version:        0.8.74.0
Release:        0.1%{?prereltag}%{?dist}
Summary:        An object oriented C++ class library

License:        Artistic 2.0
URL:            http://www.smooth-project.org/
Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}%{?prereltarball}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(fribidi)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(xmu)
#Requires:       

Provides:       %{name}-libs = %{?epoch:%{epoch}:}%{version}-%{release}

%description
%{name} is an object oriented C++ class library. It provides basic
functionality and platform support for applications and libraries.


%package devel
Summary:        %{summary} development files
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The %{name}-devel package contains the development files needed for 
development with %{name} library.


%prep
%autosetup -n %{name}-%{version}%{?prereltarball}

sed -e 's/\r//' -i Readme Copying doc/reference/dtds/*.dtd

%build
export CFLAGS="%{build_cflags}"
export CXXFLAGS="%{build_cxxflags}"
export LDFLAGS="%{build_ldflags}"

%make_build prefix=/usr libdir=%{_libdir}


%install
%make_install prefix=/usr libdir=%{_libdir}

chmod +x %{buildroot}%{_libdir}/*.so.*


%files
%license Copying
%doc Readme
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%doc doc/reference/*
%{_includedir}/smooth/
%{_includedir}/*.h
%{_libdir}/*.so


%changelog
* Tue May 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.8.74.0-0.1.pre1
- Initial spec
