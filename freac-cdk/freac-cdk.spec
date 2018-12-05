%global smoothver 0.8.74

%global systemlibs systemlibexpat,systemliburiparser,systemlibxspf,systemzlib

Name:           freac-cdk
Version:        1.1~alpha_20181201
Release:        1%{?dist}
Summary:        Component development kit for fre:ac

License:        GPLv2
URL:            http://www.freac.org/

%global ver     %(echo %{version} | tr '~' '-' | tr '_' '-')
Source0:        https://downloads.sourceforge.net/bonkenc/%{name}-%{ver}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libcdio_paranoia)
BuildRequires:  pkgconfig(liburiparser)
BuildRequires:  pkgconfig(xspf)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  smooth-devel >= %{smoothver}

%description
The fre:ac Component Development Kit (CDK) enables software developers
to create custom BoCA components for fre:ac development releases.


%package devel
Summary:        %{summary} development files
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The %{name}-devel package contains the development files needed for 
development with %{name} library.


%prep
%autosetup -n %{name}-%{ver}

sed -e 's/\r//' -i Readme*

sed -e 's|winegcc|\0-disabled|g' -i Makefile-options

sed -e 's|/lib/|/%{_lib}/|g' -i runtime/common/utilities.cpp

%build
export CFLAGS="%{build_cflags}"
export CXXFLAGS="%{build_cxxflags}"
export LDFLAGS="%{build_ldflags}"

%make_build \
  config=%{systemlibs} \
  prefix=/usr libdir=%{_libdir}


%install

%make_install \
  config=%{systemlibs} \
  prefix=/usr libdir=%{_libdir}

chmod +x %{buildroot}%{_libdir}/boca/*.so*


%files
%license COPYING
%doc Readme.md
%{_libdir}/*.so.*
%{_libdir}/boca/*.so*
%{_libdir}/boca/*.xml

%files devel
%{_includedir}/boca/
%{_includedir}/*.h
%{_libdir}/*.so


%changelog
* Tue Dec 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1~alpha_20181201-1
- 1.1-alpha-20181201

* Sun Sep 23 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-0.3.alpha.20180913
- 1.1-20180913

* Fri Jul 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-0.2.alpha.20180710
- 1.1-20180710

* Tue May 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-0.1.alpha.20180306
- Initial spec
