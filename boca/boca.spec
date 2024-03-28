%global smoothver 0.9.9

%global sanitize 0

%global systemlibs systemlibexpat,systemliburiparser,systemlibxspf,systemzlib

%global vc_url https://github.com/enzo1982/BoCA

%global ver     %%(echo %{version} | tr '~' '-' | tr '_' '-')

Name:           boca
Version:        1.0.7
Release:        1%{?dist}
Summary:        Component development kit for fre:ac

License:        GPL-2.0-only
URL:            http://www.freac.org/

%if 0%{sanitize}
Source0:        %{vc_url}/releases/download/v%{version}/%{name}-%{version}.tar.gz
%else
# Use Makefile do download
Source0:        %{name}-free-%{ver}.tar.xz
%endif
Source1:        Makefile

Patch0:         %{name}-clean.patch

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libcdio_paranoia)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(liburiparser)
BuildRequires:  pkgconfig(xspf)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  smooth-devel >= %{smoothver}

Obsoletes:      freac-cdk < 1.2
Provides:       freac-cdk = 1.2


%description
The fre:ac Component Development Kit (CDK) enables software developers
to create custom BoCA components for fre:ac development releases.


%package devel
Summary:        %{summary} development files
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       smooth-devel%{?_isa} >= %{smoothver}
Obsoletes:      freac-cdk-devel < 1.2
Provides:       freac-cdk-devel = 1.2

%description devel
The %{name}-devel package contains the development files needed for 
development with %{name} library.


%prep
%if 0%{sanitize}
%autosetup -n %{name}-%{ver} -p1

for i in aiff alac au bonk cdrip faad2 fdkaac mac mediafoundation twinvq voc wave wma ;do
  rm -rf components/decoder/$i
done
for i in bonk coreaudio coreaudioconnect faac fdkaac mac twinvq voaacenc wave wma ;do
  rm -rf components/encoder/$i
done
%else
%setup -q -n %{name}-%{ver}
%endif

sed -e 's/\r//' -i Readme* components/dsp/rnnoise/boca.dsp.rnnoise/Readme.md

cp -p components/dsp/rnnoise/boca.dsp.rnnoise/Readme.md Readme-rnnoise.md

sed -e 's|winegcc|\0-disabled|g' -i Makefile-options

sed \
  -e 's|-L$(prefix)/lib\b||g' \
  -e 's|-L/usr/X11R6/lib -L/usr/local/lib||g' \
  -i Makefile runtime/Makefile Makefile-commands

sed -e 's|/lib/|/%{_lib}/|g' -i runtime/common/utilities.cpp

%build
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
%doc Readme.md Readme-rnnoise.md
%{_libdir}/*.so.*
%{_libdir}/boca/*.so*
%{_libdir}/boca/*.xml
%{_libdir}/boca/boca.dsp.rnnoise/*.rnnn
%exclude %{_libdir}/boca/boca.dsp.rnnoise/Readme.md

%files devel
%{_includedir}/boca/
%{_includedir}/*.h
%{_libdir}/*.so


%changelog
* Thu Apr 06 2023 Phantom X <megaphantomx at hotmail dot com> - 1.0.7-1
- 1.0.7

* Thu Mar 03 2022 Phantom X <megaphantomx at hotmail dot com> - 1.0.6a-1
- 1.0.6a

* Fri Aug 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1.0.5-1
- 1.0.5

* Mon Mar 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1.0.4-1
- 1.0.4

* Mon Nov 30 2020 Phantom X <megaphantomx at hotmail dot com> - 1.0.3-1
- 1.0.3

* Sat Jul 04 2020 Phantom X <megaphantomx at hotmail dot com> - 1.0.2-1
- 1.0.2

* Wed Apr 29 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.0.1-1
- 1.0.1

* Tue Mar 31 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.0-1
- 1.0

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.0~rc1-1
- 1.0-rc1

* Sat Feb 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.0~beta3-1
- Initial spec
- Replaces freac-cdk
