%?mingw_package_header

%global with_bin 1

%global msiname wine-gecko
%global vc_url  https://sourceforge.net/p/wine/wine-gecko

Name:           mingw-wine-gecko
Version:        2.47.2
Release:        100%{?dist}
Summary:        Gecko library required for Wine

License:        MPLv1.1 or GPLv2+ or LGPLv2+
URL:            http://wiki.winehq.org/Gecko
%if 0%{?with_bin}
Source0:        https://dl.winehq.org/wine/wine-gecko/%{version}/%{msiname}-%{version}-x86_64.tar.xz
Source1:        https://dl.winehq.org/wine/wine-gecko/%{version}/%{msiname}-%{version}-x86.tar.xz
%else
Source0:        http://dl.winehq.org/wine/wine-gecko/%{version}/%{msiname}-%{version}-src.tar.xz
%endif
Source2:        %{vc_url}/ci/master/tree/LICENSE?format=raw#/LICENSE
Source3:        %{vc_url}/ci/master/tree/LEGAL?format=raw#/LEGAL
Source4:        %{vc_url}/ci/master/tree/README.txt?format=raw#/README.txt


Patch0:         %{name}-mozconfig.patch

BuildArch:      noarch

# This project is only useful with wine, and wine doesn't support PPC.
# We will adopt the same arch support that wine does.
ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64

%if 0%{?with_bin}
BuildRequires:  mingw-filesystem-base
%else
# 64
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-headers
BuildRequires:  mingw64-cpp
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-crt
BuildRequires:  mingw64-winpthreads-static
# 32
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-headers
BuildRequires:  mingw32-cpp
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-crt
BuildRequires:  mingw32-winpthreads-static

BuildRequires:  autoconf213
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  pkgconfig
BuildRequires:  python3
BuildRequires:  perl-Getopt-Long
BuildRequires:  yasm
BuildRequires:  zip
BuildRequires:  wine-core wine-wow
BuildRequires:  wine-devel
%endif


%description
Windows Gecko library required for Wine.

%package -n mingw32-%{msiname}
Summary:       Gecko library for 32bit wine
Requires:      wine-common

%description -n mingw32-%{msiname}
Windows Gecko library required for Wine.

%package -n mingw64-%{msiname}
Summary:       Gecko library for 64bit wine
Requires:      wine-common

%description -n mingw64-%{msiname}
Windows Gecko library required for Wine.

%prep
%if 0%{?with_bin}
%setup -q -T -c -n %{name}-%{version}

mkdir -p %{msiname}-%{version}-{x86,x86_64}/dist/
tar xf %{S:0} -C %{msiname}-%{version}-x86_64/dist/
tar xf %{S:1} -C %{msiname}-%{version}-x86/dist/

mkdir %{msiname}-%{version}
cp -p %{S:2} %{S:3} %{S:4} %{msiname}-%{version}/

%else

%setup -q -c -n %{msiname}-%{version}
cd %{msiname}-%{version}

%patch0 -p1 -b.mozconfig

# fix nsprpub cross compile detection
sed -i 's,cross_compiling=.*$,cross_compiling=yes,' nsprpub/configure

# remove blank includes
rm -f media/libstagefright/ports/win32/include/pthread.h

# fix wine cabinet tool
sed -i 's,$WINE cabarc.exe -r -m mszip N $cabfile msi/files,$WINE cabarc.exe -r -m mszip N $cabfile msi/files/*,' wine/make_package

%endif


%build
# Disable LTO
%global _lto_cflags %{nil}

%if !0%{?with_bin}
cd %{msiname}-%{version}
# setup build options...
echo "mk_add_options MOZ_MAKE_FLAGS=%{_smp_mflags}" >> wine/mozconfig-common
echo "export CFLAGS=\"-DWINE_GECKO_SRC\"" >> wine/mozconfig-common
echo "export CXXFLAGS=\"\$CFLAGS -fpermissive -mxsave\"" >> wine/mozconfig-common

cp wine/mozconfig-common wine/mozconfig-common.build

# ... and build
TOOLCHAIN_PREFIX=i686-w64-mingw32- MAKEOPTS="%{_smp_mflags}" ./wine/make_package --no-package -win32

TOOLCHAIN_PREFIX=x86_64-w64-mingw32- MAKEOPTS="%{_smp_mflags}" ./wine/make_package --no-package -win64
%endif


%install
mkdir -p %{buildroot}%{_datadir}/wine/gecko
cp -rp %{msiname}-%{version}-x86/dist/%{msiname}-%{version}-x86 \
   %{buildroot}%{_datadir}/wine/gecko/
cp -rp %{msiname}-%{version}-x86_64/dist/%{msiname}-%{version}-x86_64 \
   %{buildroot}%{_datadir}/wine/gecko/

%files -n mingw32-%{msiname}
%license %{msiname}-%{version}/LICENSE
%doc %{msiname}-%{version}/LEGAL
%doc %{msiname}-%{version}/README.txt
%{_datadir}/wine/gecko/%{msiname}-%{version}-x86/

%files -n mingw64-%{msiname}
%license %{msiname}-%{version}/LICENSE
%doc %{msiname}-%{version}/LEGAL
%doc %{msiname}-%{version}/README.txt
%{_datadir}/wine/gecko/%{msiname}-%{version}-x86_64/


%changelog
* Thu Dec 03 2020 Phantom X <megaphantomx at hotmail dot com> - 2.47.2-100
- 2.47.2

* Wed Sep 30 2020 Phantom X <megaphantomx at hotmail dot com> - 2.47.1-103
- bin, source is failing to build on Fedora 33

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.47.1-102
- f33 sync (python 3.8)

* Sat Dec 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.47.1-101
- Global location

* Thu Dec 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.47.1-100
- 2.47.1

* Mon Nov 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.47-100
- bin package support

* Fri Sep 13 2019 Michael Cronenworth <mike@cchtml.com> - 2.47-9
- Fix FTBFS (RHBZ#1675390)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.47-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.47-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.47-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.47-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.47-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Nov 24 2016 Michael Cronenworth <mike@cchtml.com> - 2.47-2
- Adopt ExclusiveArch from wine package

* Fri Jul 01 2016 Michael Cronenworth <mike@cchtml.com> - 2.47-1
- version upgrade, final

* Tue May 24 2016 Michael Cronenworth <mike@cchtml.com> - 2.47-0.1
- version upgrade, beta1

* Fri Feb 05 2016 Michael Cronenworth <mike@cchtml.com> - 2.44-1
- version upgrade, final

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.44-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Michael Cronenworth <mike@cchtml.com> - 2.44-0.1
- version upgrade, beta 1

* Fri Aug 14 2015 Michael Cronenworth <mike@cchtml.com> - 2.40-1
- version upgrade, final

* Thu Aug 06 2015 Michael Cronenworth <mike@cchtml.com> - 2.40-0.1
- version upgrade, beta 1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 06 2015 Michael Cronenworth <mike@cchtml.com> - 2.36-1
- version upgrade

* Tue Jan 06 2015 Michael Cronenworth <mike@cchtml.com> - 2.34-2
- Pass toolchain prefix during build
- Link statically to eliminate winpthreads dep (mozilla bz 1116777)

* Tue Dec 09 2014 Michael Cronenworth <mike@cchtml.com> - 2.34-1
- version upgrade

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 28 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.24-1
- version upgrade

* Thu Sep 12 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.21-4
- Fix FTBFS when winpthreads is available (Mozilla bug #893444)

* Sun Aug 18 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.21-3
- add BR python
- build with -static-gcc (rhbz#977039)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 30 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.21-1
- version upgrade

* Sat Jan 19 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.9-1
- version upgrade

* Mon Oct 15 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.8-1
- version upgrade

* Tue Jul 31 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7-1
- version upgrade

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 24 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.6-1
- version upgrade

* Tue Jun 19 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.0-3
- BR mingw{32,64}-filesystem >= 95

* Wed Mar 21 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.0-2
- further spec cleanup

* Mon Mar 19 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.0-1
- version upgrade
- spec cleanup

* Tue Jun 21 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2.0-3
- add suggestions from #577951c21

* Mon Jun 20 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2.0-2
- rework to mingw framework

* Fri Mar 25 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2.0-1
- version upgrade
- switch to cross framework

* Mon Mar 29 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0.0-3
- adjust path for latest wine
- requires wine-common for /usr/share/wine

* Tue Nov 24 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0.0-2
- include version in install dir

* Tue Nov 17 2009 Erik van Pienbroek <epienbro@fedoraproject.org>
- 1.0.0-1
- Initial release
