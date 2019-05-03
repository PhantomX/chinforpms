%global smoothver 0.8.74

%global sanitize 0

%global systemlibs systemlibexpat,systemliburiparser,systemlibxspf,systemzlib

Name:           freac-cdk
Version:        1.1~alpha_20190423
Release:        1%{?dist}
Summary:        Component development kit for fre:ac

License:        GPLv2
URL:            http://www.freac.org/

%global ver     %(echo %{version} | tr '~' '-' | tr '_' '-')
%if 0%{sanitize}
Source0:        https://downloads.sourceforge.net/bonkenc/%{name}-%{ver}.tar.gz
%else
Source0:        %{name}-%{ver}.tar.xz
%endif
Source1:        Makefile

Patch0:         %{name}-clean.patch

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libcdio_paranoia)
BuildRequires:  pkgconfig(libpulse)
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
Requires:       smooth-devel%{?_isa} >= %{smoothver}

%description devel
The %{name}-devel package contains the development files needed for 
development with %{name} library.


%prep
%if 0%{sanitize}
%autosetup -n %{name}-%{ver} -p1

for i in aiff au bonk cdrip faad2 fdkaac mac voc wave wma ;do
  rm -rf components/decoder/$i
done
for i in bonk coreaudio coreaudioconnect faac fdkaac voaacenc wave wma ;do
  rm -rf components/encoder/$i
done
%else
%setup -q -n %{name}-%{ver}
%endif

sed -e 's/\r//' -i Readme*

sed -e 's|winegcc|\0-disabled|g' -i Makefile-options

sed \
  -e 's|-L$(prefix)/lib\b||g' \
  -e 's|-L/usr/X11R6/lib -L/usr/local/lib||g' \
  -i Makefile runtime/Makefile Makefile-commands

sed -e 's|/lib/|/%{_lib}/|g' -i runtime/common/utilities.cpp

%build
%set_build_flags

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
* Tue Apr 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.1~alpha_20190423-1
- 1.1-alpha-20190423
- BR: pkgconfig(libpulse)

* Wed Jan 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.1~alpha_20181201-2
- devel: R: smooth-devel
- Clean tarball

* Tue Dec 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1~alpha_20181201-1
- 1.1-alpha-20181201

* Sun Sep 23 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-0.3.alpha.20180913
- 1.1-20180913

* Fri Jul 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-0.2.alpha.20180710
- 1.1-20180710

* Tue May 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-0.1.alpha.20180306
- Initial spec
