%global commit a2dcaa2f5d3d23cf121934d5ff0e4d169a8f7a64
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210821
%bcond_with snapshot

BuildArch:      noarch

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           reflac
Version:        2.0.1
Release:        1%{?dist}
Summary:        Shell script to recompress FLAC files

License:        ISC
URL:            https://github.com/chungy/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

Patch0:         0001-Add-option-to-maintain-file-times.patch

BuildRequires:  asciidoc
BuildRequires:  make
Requires:       coreutils
Requires:       findutils
Requires:       flac


%description
%{name} is a script that allows you to recompress FLAC files while preserving
their tags, intended for whole directories and for safety regardless of file
name characters and encoding.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

sed \
  -e '/^prefix?=/abindir?=$(prefix)/bin' \
  -e '/^mandir?=/s|/share/man|$(prefix)/share/man|' \
  -e '/^target=/s|$(prefix)||' \
  -e 's|/bin/|$(bindir)/|' \
  -i Makefile

%build
%make_build


%install
%make_install prefix=%{_prefix} bindir=%{_bindir} mandir=%{_mandir}


%files
%license COPYING
%doc README.adoc
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Tue May 23 2023 Phantom X <megaphantomx at hotmail dot com> - 2.0.1-1
- Initial spec

