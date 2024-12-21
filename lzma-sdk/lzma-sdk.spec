%bcond_without asm

%global ver     %%(echo %{version} | tr -d '.')
%global vermajor %%(echo %{version} | cut -d. -f2)
%global verminor %%(echo %{version} | cut -d. -f1)
# Enable to build versioned package
#global packver %%{ver}

%global sisong_url https://github.com/sisong/lzma

Name:           lzma-sdk%{?packver}
Version:        24.09
Release:        100%{?dist}
Summary:        SDK for lzma compression

License:        LGPL-2.1-only
URL:            https://www.7-zip.org

Source0:        %{url}/a/lzma%{ver}.7z
Source1:        lzma-sdk-LICENSE.fedora

Patch0:         0001-Build-shared-library.patch
Patch1:         0001-MtDec.h-fix-struct.patch

Patch10:        %{name}-sisong-e0b2bff.patch
Patch11:        %{name}-sisong-af82ecb.patch

%if %{with asm}
ExclusiveArch:  x86_64
BuildRequires:  asmc
%endif

BuildRequires:  7zip
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++


%description
LZMA SDK provides the documentation, samples, header files, libraries,
and tools you need to develop applications that use LZMA compression.

LZMA is default and general compression method of 7z format
in 7-Zip compression program (www.7-zip.org). LZMA provides high
compression ratio and very fast decompression.

LZMA is an improved version of famous LZ77 compression algorithm. 
It was improved in way of maximum increasing of compression ratio,
keeping high decompression speed and low memory requirements for
decompressing.

%package devel
Summary:        Development libraries and headers for %{name}
Requires:       %{?epoch:%{epoch}:}%{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for %{name}.

%prep
%autosetup -cTN
7zz x -bso0 %{S:0}
%_fixperms .

rm -f lzma.exe

for f in .h .c .cpp .dsw .dsp .java .cs .txt makefile; do
   find . -iname "*$f" | xargs chmod -x
done

# correct end-of-line encoding
find . \
  -type f \( -name '*.c*' -o -name '*.h*' -o -name '*.gcc' -o -name '*.txt' -o -name '*.mak' \) \
  -exec sed 's/\r//' -i {} ';'

%autopatch -p1

# Modify booleans to prevent conflict
find . \
  -type f \( -name '*.c*' -o -name '*.h*' -o -name '*.cpp' \) \
  -exec sed 's|False\b|False7z|g;s|True\b|True7z|g' -i {} ';'


install -p -m 0644 %{SOURCE1} .

sed \
  -e 's|_RPM_PACKVER_|%{?packver}|g' \
  -e 's|_RPM_MINOR_|%{verminor}|g' \
  -e 's|_RPM_MAJOR_|%{vermajor}|g' \
  -i C/Util/Lzma/makefile.gcc

sed \
  -e 's|-O2 ||g' \
  -e 's|-Wall -Werror -Wextra ||g' \
  -e 's|CFLAGS =|CFLAGS +=|' \
  -e 's|CXXFLAGS =|CXXFLAGS +=|' \
  -e '/^AFLAGS_ABI =/s|-elf64|\0 -DASMC64|g' \
  -e 's|^AFLAGS =|\0 -nologo -c -fpic|g' \
  -i C/7zip_gcc_c.mak

cat > lzmasdk-c.pc <<'EOF'
prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: lzmasdk%{?packver}
Description: Standalone library for lzma compression - C wrapper
Version: %{version}
Libs: -L${libdir} -llzmasdk%{?packver}
Cflags: -I${includedir}/lzmasdk%{?packver}/C
EOF

cat > lzmasdk-cpp.pc <<'EOF'
prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: lzmasdk%{?packver}
Description: Standalone library for lzma compression - C++ wrapper
Version: %{version}
Libs: -L${libdir} -llzmasdk%{?packver}
Cflags: -I${includedir}/lzmasdk%{?packver}/CPP
EOF


%build
%if %{with asm}
export USE_ASM=1
export IS_X64=1
%endif

%make_build -C C/Util/Lzma -f makefile.gcc clean LFLAGS_STRIP=
mkdir -p C/Util/Lzma/_o
%make_build -C C/Util/Lzma -f makefile.gcc all LFLAGS_STRIP=

%install
mkdir -p %{buildroot}%{_libdir}
install -m0755 C/Util/Lzma/liblzmasdk%{?packver}.so.%{verminor}.%{vermajor} %{buildroot}%{_libdir}/
ln -sf liblzmasdk%{?packver}.so.%{verminor}.%{vermajor} %{buildroot}%{_libdir}/liblzmasdk%{?packver}.so.%{verminor}
ln -sf liblzmasdk%{?packver}.so.%{verminor} %{buildroot}%{_libdir}/liblzmasdk%{?packver}.so

mkdir -p %{buildroot}%{_includedir}/lzmasdk%{?packver}/
find -iname '*.h' | xargs -I {} install -m0644 -D {} %{buildroot}/%{_includedir}/lzmasdk%{?packver}/{}

mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -pm0644 *.pc %{buildroot}%{_libdir}/pkgconfig/


%files
%doc DOC/lzma{,-history}.txt lzma-sdk-LICENSE.fedora
%{_libdir}/liblzmasdk%{?packver}.so.*

%files devel
%doc DOC/{7z*,Methods}.txt
%{_includedir}/lzmasdk%{?packver}/
%{_libdir}/liblzmasdk%{?packver}.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sat Dec 21 2024 Phantom X <megaphantomx at hotmail dot com> - 24.09-100
- 24.09

* Sun Aug 18 2024 Phantom X <megaphantomx at hotmail dot com> - 24.08-100
- 24.08

* Sat Jun 29 2024 Phantom X <megaphantomx at hotmail dot com> - 24.07-100
- 24.07

* Fri May 31 2024 Phantom X <megaphantomx at hotmail dot com> - 24.06-100
- 24.06

* Sun May 19 2024 Phantom X <megaphantomx at hotmail dot com> - 24.05-100
- 24.05

* Wed Apr 17 2024 Phantom X <megaphantomx at hotmail dot com> - 23.01-102
- Add missing XZ symbols to library

* Thu Jun 29 2023 Phantom X <megaphantomx at hotmail dot com> - 23.01-101
- Header fix

* Thu Jun 29 2023 Phantom X <megaphantomx at hotmail dot com> - 23.01-100
- 23.01

* Fri Mar 17 2023 Phantom X <megaphantomx at hotmail dot com> - 22.01-103
- Add sisong additions for HDiffPatch

* Wed Mar 15 2023 Phantom X <megaphantomx at hotmail dot com> - 22.01-102
- Add XZ symbols

* Tue Sep 13 2022 Phantom X <megaphantomx at hotmail dot com> - 22.01-101
- Modify booleans to prevent conflict

* Wed Aug 31 2022 Phantom X <megaphantomx at hotmail dot com> - 22.01-100
- 22.01

* Tue Jun 21 2022 Phantom X <megaphantomx at hotmail dot com> - 22.00-100
- 22.00
- asmc support

* Fri Jan 07 2022 Phantom X <megaphantomx at hotmail dot com> - 21.07-100
- 21.07

* Fri Nov 26 2021 Phantom X <megaphantomx at hotmail dot com> - 21.06-100
- 21.06

* Fri May 07 2021 Phantom X <megaphantomx at hotmail dot com> - 21.02-100
- 21.02

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 19.00-102
- Add missing symbols to library

* Fri Sep 11 2020 Phantom X <megaphantomx at hotmail dot com> - 19.00-101
- Add missing symbols to library

* Sat Aug 08 2020 Phantom X <megaphantomx at hotmail dot com> - 19.00-100
- 19.00
- Add pkgconfig files

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.5-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.5-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.5-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.5-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.5-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.5-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.5-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.5-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.5-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.5-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Aug 14 2015 Adam Jackson <ajax@redhat.com> 4.6.5-16
- Pass ldflags to make so hardening works

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 4.6.5-14
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 10 2014 Jon Ciesla <limburgher@gmail.com> - 4.6.5-11
- Fix format-security FTBFS, BZ 1037188.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Jon Ciesla <limb@jcomserv.net> - 4.6.5-6
- Changed first gcc on make line to g++ to silence rpmlint.

* Tue Aug  9 2011 Tom Callaway <spot@fedoraproject.org> - 4.6.5-5
- rework package to be more normal

* Wed Apr 27 2011 Jon Ciesla <limb@jcomserv.net> - 4.6.5-4
- Additional provides macro.

* Mon Apr 11 2011 Jon Ciesla <limb@jcomserv.net> - 4.6.5-3
- Stripped perl(SevenZip) provides.

* Tue Apr 05 2011 Jon Ciesla <limb@jcomserv.net> - 4.6.5-2
- Licensing clarification.

* Wed May 26 2010 Jon Ciesla <limb@jcomserv.net> - 4.6.5-1
- Initial build
