%global sanitize 0

%global ver     %%(echo %{version} | tr -d '.')

Name:           7zip
Version:        21.02
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

BuildRequires:  gcc-c++
BuildRequires:  make
#BuildRequires:  asmc


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
  -e 's|$(LDFLAGS)|\0 %{build_ldflags}|g' \
  -e '/LDFLAGS/s| -s | |g' \
  -i CPP/7zip/7zip_gcc.mak


%build
pushd CPP/7zip/Bundles/Alone2
%make_build -f ../../cmpl_gcc.mak
popd

%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 CPP/7zip/Bundles/Alone2/b/g/7zz %{buildroot}%{_bindir}/


%files
%license copying.txt License.txt
%doc DOC/*.txt
%{_bindir}/7zz


%changelog
* Fri May 07 2021 Phantom X <megaphantomx at hotmail dot com> - 21.02-1
- Initial spec
