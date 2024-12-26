%global sanitize 0

%bcond_without asm
# Select the assembler (asmc or uasm)
# asmc can be used with Fedora
%global asmopt asmc

%global platform %{nil}
%if %{with asm}
%ifarch %{ix86}
%global platform x86
%global isx86 1
%endif
%ifarch x86_64
%global platform x64
%global isx64 1
%endif
%ifarch arm
%global platform arm64
%global isarm64 1
%endif
%endif

%global ver     %%(echo %{version} | tr -d '.')

Name:           7zip
Version:        24.09
Release:        2%{?dist}
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

Patch1:         0001-set-plugins-path.patch

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

Obsoletes:      p7zip < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       p7zip = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       p7zip%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


%description
7-Zip is a file archiver with a very high compression ratio.

This build do not have RAR support.


%package plugins
Summary:        Additional plugins for 7zip
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      p7zip-plugins < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       p7zip-plugins = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       p7zip-plugins%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description plugins
Additional plugins that can be used with 7zip to extend its abilities.


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
  -e 's| -z noexecstack| -Wl,-z,noexecstack|g' \
  -e '/LDFLAGS/s| -s | |g' \
  -e '/^AFLAGS_ABI =/s|-elf64|\0 -DASMC64|g' \
  -e '/^AFLAGS =/s|-nologo|\0 -c -fpic|g' \
  -i CPP/7zip/7zip_gcc.mak

sed \
  -e 's|_RPMLIBEXECDIR_|%{_libexecdir}/%{name}|g' \
  -i CPP/7zip/UI/Console/Main.cpp CPP/7zip/UI/Client7z/Client7z.cpp

for i in 7za 7zz 7z ;do
cat > ${i}.wrapper <<EOF
#!/usr/bin/sh
exec "%{_libexecdir}/%{name}/${i}" "\$@"
EOF
done


%build
export DISABLE_RAR=1

for build in Bundles/{Alone,Alone2,Format7zF,SFXCon} UI/Console; do
  %make_build -C CPP/7zip/${build} -f ../../cmpl_gcc.mak LFLAGS_STRIP= \
    PLATFORM=%{platform} IS_X86=%{?isx86} IS_X64=%{?isx64} IS_ARM64=%{?isarm64} \
    %{?with_asm:USE_ASM=1 MY_ASM=%{asmopt}}
done


%install
mkdir -p %{buildroot}%{_bindir}
for i in 7za 7zz 7z ;do
  install -pm0755 ${i}.wrapper %{buildroot}%{_bindir}/${i}
done

mkdir -p %{buildroot}%{_libexecdir}/%{name}
install -pm0755 CPP/7zip/Bundles/Alone/b/g/7za %{buildroot}%{_libexecdir}/%{name}/
install -pm0755 CPP/7zip/Bundles/Alone2/b/g/7zz %{buildroot}%{_libexecdir}/%{name}/
install -pm0755 CPP/7zip/Bundles/Format7zF/b/g/7z.so %{buildroot}%{_libexecdir}/%{name}/
install -pm0755 CPP/7zip/UI/Console/b/g/7z %{buildroot}%{_libexecdir}/%{name}/
install -pm0755 CPP/7zip/Bundles/SFXCon/b/g/7zCon %{buildroot}%{_libexecdir}/%{name}/7zCon.sfx

ln -s %{name} %{buildroot}%{_libexecdir}/p7zip


%pretrans -p <lua>
-- Define the path to directory being replaced below.
-- DO NOT add a trailing slash at the end.
path = "%{_libexecdir}/p7zip"
st = posix.stat(path)
if st and st.type == "directory" then
  status = os.rename(path, path .. ".rpmmoved")
  if not status then
    suffix = 0
    while not status do
      suffix = suffix + 1
      status = os.rename(path .. ".rpmmoved", path .. ".rpmmoved." .. suffix)
    end
    os.rename(path, path .. ".rpmmoved")
  end
end


%files
%license copying.txt License.txt
%doc DOC/*.txt
%{_bindir}/7za
%{_bindir}/7zz
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/7za
%{_libexecdir}/%{name}/7zz
%{_libexecdir}/%{name}/7zCon.sfx
%{_libexecdir}/p7zip

%files plugins
%{_bindir}/7z
%{_libexecdir}/%{name}/7z
%{_libexecdir}/%{name}/7z.so


%changelog
* Wed Dec 25 2024 Phantom X <megaphantomx at hotmail dot com> - 24.09-2
- Rewrite to replace p7zip

* Fri Dec 20 2024 Phantom X <megaphantomx at hotmail dot com> - 24.09-1
- 24.09

* Sun Aug 18 2024 Phantom X <megaphantomx at hotmail dot com> - 24.08-1
- 24.08

* Sat Jun 29 2024 Phantom X <megaphantomx at hotmail dot com> - 24.07-1
- 24.07

* Fri May 31 2024 Phantom X <megaphantomx at hotmail dot com> - 24.06-1
- 24.06

* Sun May 19 2024 Phantom X <megaphantomx at hotmail dot com> - 24.05-1
- 24.05

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
