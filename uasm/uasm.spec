# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global _legacy_common_support 1

%global commit 619259a41918f756002226280184fd22d2ba194e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210601
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname UASM
%global vc_url https://github.com/Terraspace/%{pkgname}

Name:           uasm
Version:        2.53
Release:        1%{?gver}%{?dist}
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
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

file=History.txt
iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && touch -r $file $file.new && mv $file.new $file

sed \
  -e 's|$(CPPFLAGS)|\0 $(LDFLAGS)|g' \
  -e 's| -s | |g' \
  -i gccLinux64.mak

cp -p %{S:1} .
sed \
  -e 's|/usr/bin/|exec %{_bindir}/|g' \
  -e 's|@|"@"|g' \
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
* Sat Jun 19 2021 - 2.53-1.20210601git619259a
- Initial spec
