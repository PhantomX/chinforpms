# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global _legacy_common_support 1

%global commit 6f3e32e4ac9e47cecb40a3e91e04c054709875f0
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20211108
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname UASM
%global vc_url https://github.com/Terraspace/%{pkgname}

Name:           uasm
Version:        2.53
Release:        2%{?gver}%{?dist}
Summary:        A macro assembler

# Fedora bad licenses
License:        JWasm and Watcom-1.0

URL:            http://www.terraspace.co.uk/uasm.html

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source1:        https://aur.archlinux.org/cgit/aur.git/plain/%{name}-nocolor?h=%{name}&id=4d4e065376da9be6e96de8de201a3b97d4cdc14b#/%{name}-nocolor

Patch0:         0001-Fix-cross-compilation-of-dbgcv.c.patch
Patch1:         %{vc_url}/pull/151.patch#/%{name}-gh-pr151.patch

BuildRequires:  gcc
BuildRequires:  make


%description
UASM is a free MASM-compatible assembler based on JWasm.

%prep
%autosetup -n %{pkgname}-%{?gver:%{commit}}%{!?gver:%{version}} -p1

file=History.txt
iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && touch -r $file $file.new && mv $file.new $file

sed \
  -e 's|$(CPPFLAGS)|\0 $(LDFLAGS)|g' \
  -e 's| -s | |g' \
  -i gccLinux64.mak

cp -p %{S:1} .
sed \
  -e 's|/usr/bin/|exec %{_bindir}/|g' \
  -e 's|$@|"$@"|g' \
  -i %{name}-nocolor


%build
%set_build_flags
%make_build -f gccLinux64.mak


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 GccUnixR/%{name} %{buildroot}%{_bindir}/%{name}

install -pm0755 %{name}-nocolor %{buildroot}%{_bindir}/%{name}-nocolor


%files
%license License.txt
%doc Readme.txt History.txt
%{_bindir}/%{name}
%{_bindir}/%{name}-nocolor


%changelog
* Fri Nov 26 2021 - 2.53-2.20211108git6f3e32e
- Bump

* Sat Jun 19 2021 - 2.53-1.20210601git619259a
- Initial spec
