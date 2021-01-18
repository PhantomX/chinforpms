%global smoothver 0.9.6

%global sanitize 0

%global systemlibs systemlibexpat,systemliburiparser,systemlibxspf,systemzlib

%global ver     %%(echo %{version} | tr '~' '-' | tr '_' '-')

Name:           boca
Version:        1.0.3
Release:        1%{?dist}
Summary:        Component development kit for fre:ac

License:        GPLv2
URL:            http://www.freac.org/

%if 0%{sanitize}
Source0:        https://downloads.sourceforge.net/bonkenc/%{name}-%{ver}.tar.gz
%else
# Use Makefile do download
Source0:        %{name}-%{ver}.tar.xz
%endif
Source1:        Makefile

Patch0:         %{name}-clean.patch
Patch1:         https://github.com/enzo1982/BoCA/commit/4fb9fa91bf8ab3dbeac7ac9349d05cc9c29dd1ff.patch#/%{name}-gh-4fb9fa9.patch

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

for i in aiff au bonk cdrip faad2 fdkaac mac voc wave wma ;do
  rm -rf components/decoder/$i
done
for i in bonk coreaudio coreaudioconnect faac fdkaac voaacenc wave wma ;do
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
