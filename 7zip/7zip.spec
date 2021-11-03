%global sanitize 0

%bcond_with asm

%global platform %{nil}
%if %{with asm}
%ifarch %{ix86}
%global platform _x86
%endif
%ifarch x86_64
%global platform _x64
%endif
%ifarch arm
%global platform _arm64
%endif
%endif
%global makefile cmpl_gcc%{platform}

%global ver     %%(echo %{version} | tr -d '.')

Name:           7zip
Version:        21.04
Release:        1%{?dist}
Summary:        Very high compression ratio file archiver

License:        LGPLv2+ and BSD and Public Domain
URL:            https://www.7-zip.org

%if 0%{sanitize}
Source0:        %{url}/a/7z%{ver}-src.7z
%else
# Use Makefile to download
Source0:        %{name}-free-%{version}.tar.xz
%endif
Source1:        Makefile

Patch0:         0001-make-remove-rar.patch

%if %{with asm}
ExclusiveArch:  %{ix86} x86_64 %{arm}
%endif

BuildRequires:  gcc-c++
BuildRequires:  make
%if %{with asm}
#BuildRequires:  asmc
BuildRequires:  uasm
%endif


%description
7-Zip is a file archiver with a very high compression ratio.

This build do not have RAR support.


%prep
%if 0%{sanitize}
%autosetup -n -c %{name}-%{version} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

%if 0%{sanitize}
  rm -rf CPP/7zip/{Archive,Compress,Crypto}/Rar*
  rm -f DOC/unRarLicense.txt
%endif

# correct end-of-line encoding
find . -type f \( -name "*.cpp" -o -name "*.h" -o -name "*.gcc" -o -name "*.mak" -o -name "*.txt" \) -exec sed 's/\r//' -i {} ';'

# move license files
mv DOC/License.txt DOC/copying.txt .

sed \
  -e 's| -Werror | |g' \
  -e 's|-O2 |%{build_cxxflags} |g' \
  -e 's|$(LDFLAGS)|\0 %{build_ldflags} -Wl,-z,noexecstack|g' \
  -e '/LDFLAGS/s| -s | |g' \
  -e '/^MY_ASM/s|asmc|uasm|g' \
  -i CPP/7zip/7zip_gcc.mak

# https://github.com/justdan96/7zip_static/blob/main/Dockerfile#L27
sed -e \
  '1iOPTION FRAMEPRESERVEFLAGS:ON\nOPTION PROLOGUE:NONE\nOPTION EPILOGUE:NONE' \
  -i Asm/x86/LzFindOpt.asm


%build
pushd CPP/7zip/Bundles/Alone2
%make_build -f ../../%{makefile}.mak
popd

%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 CPP/7zip/Bundles/Alone2/b/g%{platform}/7zz %{buildroot}%{_bindir}/


%files
%license copying.txt License.txt
%doc DOC/*.txt
%{_bindir}/7zz


%changelog
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
