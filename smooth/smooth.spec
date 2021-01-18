%global ver     %%{lua:ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(ver)}

Name:           smooth
Version:        0.9.6
Release:        2%{?dist}
Summary:        An object oriented C++ class library

License:        Artistic 2.0
URL:            http://www.smooth-project.org/

Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{ver}.tar.gz

Patch0:         0001-Support-ld.so.conf.d-and-fix-library-loading-order.patch

BuildRequires:  make
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
%autosetup -n %{name}-%{ver} -p1

sed -e 's/\r//' -i Readme.md Copying doc/reference/dtds/*.dtd

sed \
  -e 's|"/usr/lib"|"%{_libdir}"|g' \
  -e 's|"/usr/local/lib"|"/usr/local/%{_lib}"|g' \
  -i classes/system/dynamicloader.cpp


%build
%set_build_flags

%make_build prefix=/usr libdir=%{_libdir}


%install
%make_install prefix=/usr libdir=%{_libdir}

chmod +x %{buildroot}%{_libdir}/*.so.*


%files
%license Copying
%doc Readme.md
%{_bindir}/*
%{_libdir}/*.so.*

%files devel
%doc doc/reference/*
%{_includedir}/smooth/
%{_includedir}/*.h
%{_libdir}/*.so


%changelog
* Sat Dec 12 2020 Phantom X <megaphantomx at hotmail dot com> - 0.9.6-2
- Patch to fix library loading issues

* Mon Nov 30 2020 Phantom X <megaphantomx at hotmail dot com> - 0.9.6-1
- 0.9.6

* Sat Jul 04 2020 Phantom X <megaphantomx at hotmail dot com> - 0.9.5-1
- 0.9.5

* Tue Mar 31 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.9.4-1
- 0.9.4

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.9.3-1
- 0.9.3

* Sat Feb 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.9.2-1
- 0.9.2

* Mon Dec 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.9.0-1
- 0.9.0

* Tue Apr 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.8.74.0~pre6-1
- 0.8.74.0-pre6

* Tue Dec 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.8.74.0~pre5-1
- 0.8.74.0-pre5

* Sun Sep 23 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.8.74.0-0.3.pre4
- 0.8.74.0-pre4

* Fri Jul 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.8.74.0-0.2.pre2
- 0.8.74.0-pre2

* Tue May 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.8.74.0-0.1.pre1
- Initial spec
