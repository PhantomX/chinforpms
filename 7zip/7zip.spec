%global sanitize 0

%bcond_without asm
# Select the assembler (asmc or uasm)
# asmc can be used with Fedora
%global asmopt asmc

%global platform %{nil}
%if %{with asm}
%ifarch %{ix86}
%global platform _x86
%endif
%ifarch x86_64
%global platform _x64
%global asmc 64
%endif
%ifarch arm
%global platform _arm64
%endif
%endif
%global makefile cmpl_gcc%{platform}

%global ver     %%(echo %{version} | tr -d '.')

Name:           7zip
Version:        23.01
Release:        1%{?dist}
Summary:        Very high compression ratio file archiver

License:        LGPL-2.1-or-later AND BSD-3-Clause AND LicenseRef-Fedora-Public-Domain
URL:            https://www.7-zip.org

%if 0%{sanitize}
Source0:        %{url}/a/7z%{ver}-src.7z
%else
# Use Makefile to download
Source0:        %{name}-free-%{version}.tar.xz
%endif
Source1:        Makefile

Patch1:         0001-set-7zCon.sfx-path.patch

%if %{with asm}
%if "%{asmopt}" == "asmc"
ExclusiveArch:  x86_64
%else
ExclusiveArch:  %{ix86} x86_64 %{arm}
%endif
%endif

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
%if %{with asm}
BuildRequires:  %{asmopt}
%endif


%description
7-Zip is a file archiver with a very high compression ratio.

This build do not have RAR support.


%prep
%if 0%{sanitize}
%autosetup -n -c %{name}-%{version} -N -p1
%else
%autosetup -n %{name}-%{version} -N -p1
%endif

%if 0%{sanitize}
  rm -rf CPP/7zip/{Archive,Compress,Crypto}/Rar*
  rm -f DOC/unRarLicense.txt
%endif

# correct end-of-line encoding
find . -type f \( -name '*.c*' -o -name '*.h*' -o -name '*.gcc' -o -name '*.mak' -o -name '*.txt' \) -exec sed 's/\r//' -i {} ';'

%autopatch -p1

# move license files
mv DOC/License.txt DOC/copying.txt .

sed \
  -e 's| -Werror | |g' \
  -e 's|-O2 | |g' \
  -e 's|^CFLAGS =|CFLAGS +=|g' \
  -e 's|^CXXFLAGS =|CXXFLAGS +=|g' \
  -e 's|^LDFLAGS =|LDFLAGS +=|g' \
  -e 's|$(LDFLAGS)|\0 -Wl,-z,noexecstack|g' \
  -e '/LDFLAGS/s| -s | |g' \
  -e '/^MY_ASM/s|asmc|%{asmopt}%{asmc}|g' \
  -e '/^AFLAGS_ABI =/s|-elf64|\0 -DASMC64|g' \
  -e '/^AFLAGS =/s|-nologo|\0 -fpic|g' \
  -i CPP/7zip/7zip_gcc.mak

sed -e 's|__RPMLIBEXECDIR_|%{_libexecdir}/%{name}|g' -i CPP/7zip/UI/Console/Main.cpp


%build
%if %{with asm}
export USE_ASM=1
%endif
export DISABLE_RAR=1

pushd CPP/7zip/Bundles/Alone2
%make_build -f ../../%{makefile}.mak LFLAGS_STRIP=
popd

pushd CPP/7zip/Bundles/SFXCon
%make_build -f makefile.gcc LFLAGS_STRIP=
popd

%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 CPP/7zip/Bundles/Alone2/b/g%{platform}/7zz %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_libexecdir}/%{name}
install -pm0755 CPP/7zip/Bundles/SFXCon/_o/7zCon %{buildroot}%{_libexecdir}/%{name}/7zCon.sfx


%files
%license copying.txt License.txt
%doc DOC/*.txt
%{_bindir}/7zz
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/7zCon.sfx


%changelog
* Thu Jun 29 2023 Phantom X <megaphantomx at hotmail dot com> - 23.01-1
- 23.01

* Wed Aug 31 2022 Phantom X <megaphantomx at hotmail dot com> - 22.01-1
- 22.01

* Mon Jun 20 2022 Phantom X <megaphantomx at hotmail dot com> - 22.00-1
- 22.00
- Removed NASM patches 
- Build with asmc, now is good

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 21.07-4
- Fix for package_note_file

* Mon Jan 17 2022 Phantom X <megaphantomx at hotmail dot com> - 21.07-3
- Update NASM patches

* Fri Jan 07 2022 Phantom X <megaphantomx at hotmail dot com> - 21.07-2
- Enable experimental NASM support

* Fri Jan 07 2022 Phantom X <megaphantomx at hotmail dot com> - 21.07-1
- 21.07

* Sat Nov 27 2021 Phantom X <megaphantomx at hotmail dot com> - 21.06-2
- Build 7zCon.sfx

* Fri Nov 26 2021 Phantom X <megaphantomx at hotmail dot com> - 21.06-1
- 21.06

* Wed Nov 03 2021 Phantom X <megaphantomx at hotmail dot com> - 21.04-1
- 21.04

* Wed Oct 06 2021 Phantom X <megaphantomx at hotmail dot com> - 21.03-2
- Add fix to uasm do not align the stack when build with ASM support

* Thu Jul 22 2021 Phantom X <megaphantomx at hotmail dot com> - 21.03-1
- 21.03

* Sat Jun 19 2021 Phantom X <megaphantomx at hotmail dot com> - 21.02-2
- ASM support with uasm (disabled by default)

* Fri May 07 2021 Phantom X <megaphantomx at hotmail dot com> - 21.02-1
- Initial spec
