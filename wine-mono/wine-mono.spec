# Disable LTO
%global _lto_cflags %{nil}

%undefine _auto_set_build_flags
%undefine _hardened_build
%undefine _package_note_file

%?mingw_package_header

%bcond_without bin
#Set to 1 to download sources from github
%global with_gh 1

%if %{with bin}
%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true
%global __objdump /bin/true
%global __debug_install_post /bin/true
%endif

%global vc_url  https://github.com/madewokherd/wine-mono

Name:           wine-mono
Version:        7.4.1
Release:        100%{?dist}
Summary:        Mono library required for Wine

License:        GPL-2.0-only AND LGPL-2.0-only and MIT AND BSD-1-Clause AND MS-PL AND MPL-1.1 AND Zlib
URL:            http://wiki.winehq.org/Mono

%if 0%{?with_gh}
%global dl_url  %{vc_url}/releases/download/%{name}-%{version}
%else
%global dl_url  https://dl.winehq.org/wine/%{name}/%{version}
%endif
%if %{with bin}
Source0:        %{dl_url}/%{name}-%{version}-x86.tar.xz
%else
Source0:        %{dl_url}/%{name}-%{version}-src.tar.xz
%endif
Source1:        %{vc_url}/%{name}/raw/master/COPYING
Source2:        %{vc_url}/%{name}/raw/master/README

# to statically link in winpthreads
Patch0:         %{name}-build-static.patch


BuildArch:      noarch
ExcludeArch:    %{power64} s390x s390

%if %{with bin}
BuildRequires:  mingw-filesystem-base
%else
# 64
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-headers
BuildRequires:  mingw64-cpp
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-llvm
BuildRequires:  mingw64-crt
BuildRequires:  mingw64-winpthreads-static
# 32
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-headers
BuildRequires:  mingw32-cpp
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-llvm
BuildRequires:  mingw32-crt
BuildRequires:  mingw32-winpthreads-static

BuildRequires:  autoconf automake
BuildRequires:  bc
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  gettext
BuildRequires:  libgdiplus
BuildRequires:  zip
BuildRequires:  wine-core
BuildRequires:  mono-core
BuildRequires:  /usr/bin/pathfix.py
%endif

Requires: wine-filesystem

# Bundles FAudio, libtheorafile, libmojoshader, SDL2, SDL2_image


%description
Windows Mono library required for Wine.

%global mingw_build_win64 0
%global mingw_build_win32 0
%{?mingw_debug_package}

%prep
%setup -q
%if %{with bin}
cp -p %{S:1} %{S:2} .

tar xvf %{S:0}
chmod -R g-w %{name}-%{version}

%else

%patch -P 0 -p1 -b.static


# Fix all Python shebangs
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" .
sed -i 's/GENMDESC_PRG=python/GENMDESC_PRG=python3/' mono/mono/mini/Makefile.am.in
sed -i 's/CP_R=python /CP_R=python3 /' GNUmakefile

# remove shipped compiler
rm -rf llvm-mingw-20200325-ubuntu-18.04/*
sed -i 's/$CPPFLAGS_FOR_BTLS $btls_cflags/$CPPFLAGS_FOR_BTLS -fPIC $btls_cflags/' mono/configure.ac

%endif


%build
%if %{without bin}
export BTLS_CFLAGS="-fPIC"
export CPPFLAGS_FOR_BTLS="-fPIC"
# Disable LLVM compiler as we do not ship a full, updated MinGW environment. Use GCC instead.
echo 'AUTO_LLVM_MINGW=0' >> user-config.make
# Disable WpfGfx as it requires LLVM to compile
echo "ENABLE_DOTNET_CORE_WPFGFX=0" >> user-config.make
%make_build image
%endif

%install
mkdir -p %{buildroot}%{_datadir}/wine/mono/%{name}-%{version}/
%if %{with bin}

cp -r %{name}-%{version}/* %{buildroot}%{_datadir}/wine/mono/%{name}-%{version}/

%else

cp -r image/* %{buildroot}%{_datadir}/wine/mono/%{name}-%{version}/

# prep licenses
cp mono/LICENSE mono-LICENSE
cp mono/COPYING.LIB mono-COPYING.LIB
cp mono/mcs/COPYING mono-mcs-COPYING

pushd mono/mcs

for l in `ls LICENSE*`; do
echo $l
cp $l ../../mono-mcs-$l
done

popd

cp mono-basic/README mono-basic-README
cp mono-basic/LICENSE mono-basic-LICENSE

%endif

chmod -x %{buildroot}%{_datadir}/wine/mono/%{name}-%{version}/lib/mono/*/*.{config,rsp}
chmod -x %{buildroot}%{_datadir}/wine/mono/%{name}-%{version}/lib/mono/msbuild/Current/bin/Roslyn/*.targets


%files
%license COPYING
%doc README
%if %{without bin}
%license mono-LICENSE mono-COPYING.LIB mono-basic-LICENSE mono-mcs*
%doc mono-basic-README
%endif
%{_datadir}/wine/mono/%{name}-%{version}/


%changelog
* Tue Apr 18 2023 Phantom X <megaphantomx at hotmail dot com> - 7.4.1-100
- 7.4.1

* Fri Oct 28 2022 Phantom X <megaphantomx at hotmail dot com> - 7.4.0-100
- 7.4.0

* Sat Jul 16 2022 Phantom X <megaphantomx at hotmail dot com> - 7.3.0-101
- Debug fixes

* Sat Jun 04 2022 Phantom X <megaphantomx at hotmail dot com> - 7.3.0-100
- 7.3.0

* Sat Apr 09 2022 Phantom X <megaphantomx at hotmail dot com> - 7.2.0-100
- 7.2.0

* Sat Feb 26 2022 Phantom X <megaphantomx at hotmail dot com> - 7.1.5-100
- 7.1.5

* Tue Feb 08 2022 Phantom X <megaphantomx at hotmail dot com> - 7.1.2-100
- 7.1.2

* Sat Feb 05 2022 Phantom X <megaphantomx at hotmail dot com> - 7.1.1-100
- 7.1.1

* Sat Nov 13 2021 Phantom X <megaphantomx at hotmail dot com> - 7.0.0-100
- 7.0.0

* Mon Nov 01 2021 Phantom X <megaphantomx at hotmail dot com> - 6.4.1-100
- 6.4.1

* Mon Sep 20 2021 Phantom X <megaphantomx at hotmail dot com> - 6.4.0-100
- 6.4.0

* Tue Jul 27 2021 Phantom X <megaphantomx at hotmail dot com> - 6.3.0-100
- 6.3.0

* Fri Jul 23 2021 Phantom X <megaphantomx at hotmail dot com> - 6.2.2-100
- 6.2.2

* Fri Jul 09 2021 Phantom X <megaphantomx at hotmail dot com> - 6.2.1-100
- 6.2.1

* Sat Jun 05 2021 Phantom X <megaphantomx at hotmail dot com> - 6.2.0-100
- 6.2.0

* Sat Apr 03 2021 Phantom X <megaphantomx at hotmail dot com> - 6.1.1-100
- 6.1.1

* Sat Feb 13 2021 Phantom X <megaphantomx at hotmail dot com> - 6.0.0-100
- 6.0.0

* Sat Oct  3 2020 Phantom X <megaphantomx at hotmail dot com> - 5.1.1-100
- 5.1.1

* Tue Jun 09 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.1.0-100
- 5.1.0 bin

* Tue May 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.0.1-100
- 5.0.1

* Tue Apr 28 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.0.0-101
- Fedora sync

* Mon Apr 20 2020 Phantom X <megaphantomx at bol dot com dot br> - 5.0.0-100
- 5.0.0

* Wed Nov 06 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.9.4-100
- 4.9.4

* Mon Sep 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.9.3-101
- Patch to fix whq#47807

* Fri Sep 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.9.3-100
- 4.9.3

* Fri Aug 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.9.2-100
- 4.9.2

* Wed Jul 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.9.0-101
- Split not compliant debug package

* Fri Jun 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.9.0-100
- 4.9.0

* Fri Apr 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.8.3-100
- 4.8.3

* Thu Apr 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.8.2-100
- 4.8.2

* Sun Apr 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.8.1-101
- Fedora sync

* Sun Apr 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.8.1-100
- 4.8.1
- Shared location instead MSI

* Sun Mar 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.8.0-100
- 4.8.0
- Rawhide sync

* Mon Jan 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.7.5-100
- 4.7.5

* Thu Aug 23 2018 Peter Robinson <pbrobinson@fedoraproject.org> 4.7.3-2
- Don't exclude aarch64

* Sat Jul 21 2018 Michael Cronenworth <mike@cchtml.com> - 4.7.3-1
- version upgrade

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug 08 2017 Michael Cronenworth <mike@cchtml.com> - 4.7.1-1
- version upgrade

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 23 2017 Michael Cronenworth <mike@cchtml.com> - 4.7.0-1
- version upgrade

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 15 2016 Michael Cronenworth <mike@cchtml.com> - 4.6.4-1
- version upgrade

* Thu Oct 13 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.3-2
- mono rebuild for aarch64 support

* Wed Jun 15 2016 Michael Cronenworth <mike@cchtml.com> - 4.6.3-1
- version upgrade

* Sun Apr 17 2016 Michael Cronenworth <mike@cchtml.com> - 4.6.2-1
- version upgrade

* Sun Mar 13 2016 Peter Robinson <pbrobinson@fedoraproject.org> 4.6.0-2
- Fix up the Wine / mono supported arch cross section

* Tue Mar 08 2016 Michael Cronenworth <mike@cchtml.com> - 4.6.0-1
- version upgrade

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 23 2015 Michael Cronenworth <mike@cchtml.com> - 4.5.6-4
- enable optimizations, tls patch

* Mon Apr 20 2015 Michael Cronenworth <mike@cchtml.com> - 4.5.6-3
- statically link DLLs (#1213427)

* Sun Mar 08 2015 Michael Cronenworth <mike@cchtml.com> - 4.5.6-2
- disable optimizations in CLI, workaround for gcc5

* Fri Mar 06 2015 Michael Cronenworth <mike@cchtml.com> - 4.5.6-1
- version upgrade

* Thu Feb 05 2015 Michael Cronenworth <mike@cchtml.com> - 4.5.4-2
- Update bundled valgrind headers (#1141584)

* Fri Nov 14 2014 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 4.5.4-1
- version upgrade

* Tue Jun 24 2014 Michael Cronenworth <mike@cchtml.com> - 4.5.2-4
- Rebuilt to use static libgcc (#1056436)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 14 2013 Michael Cronenworth <mike@cchtml.com>
- 4.5.2-2
- Add ExcludeArch as Mono requires an x86 builder host

* Sun Dec 08 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 4.5.2-1
- version upgrade

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr  4 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.0.8-3
- Fix FTBFS against latest automake
- Added BR: bc

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.8-1
- version upgrade

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 04 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-7
- add mingw-filesystem BR
- fix header macro

* Fri Jun 29 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-6
- rename to wine-mono

* Wed Jun 27 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-5
- add conditional so package builds on x86-64 builders as well

* Tue Jun 26 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-4
- add -e option to echo in build script to fix idt files generation

* Sun Jun 24 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-3
- pull some upstream patches from git

* Tue Jun 12 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-2
- rename msi according to what wine expects

* Mon May 28 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.0.4-1
- Initial release
