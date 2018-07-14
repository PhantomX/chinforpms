%global date 20180710
%global prerel 1

%global smoothver 0.8.74

%if 0%{?prerel}
%global prereltag .alpha.%{date}
%global prereltarball -alpha-%{date}
%endif

%global systemlibs systemlibexpat,systemliburiparser,systemlibxspf,systemzlib

Name:           freac-cdk
Version:        1.1
Release:        0.2%{prereltag}%{?dist}
Summary:        Component development kit for fre:ac

License:        GPLv2
URL:            http://www.freac.org/
Source0:        https://downloads.sourceforge.net/bonkenc/%{name}-%{version}%{?prereltarball}.tar.gz

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
%autosetup -n %{name}-%{version}%{?prereltarball}

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
* Fri Jul 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-0.2.alpha.20180710
- 1.1-20180710

* Tue May 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-0.1.alpha.20180306
- Initial spec
