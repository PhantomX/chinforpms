%global commit e178184cfd86f3fce0882a24ec425c163ac5964b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180519
%bcond_without snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           cmdpack
Version:        1.06
Release:        2%{?dist}
Summary:        Collection of command line utilities, most for emulation or disk images

License:        GPL-3.0-only
URL:            https://github.com/chungy/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif
# https://www.romhacking.net/utilities/1264/
Source1:        error_recalc.c
Source2:        error_recalc.txt

BuildRequires:  asciidoc
BuildRequires:  gcc
BuildRequires:  make


%description
%{name} is a collection of command line utilities, most for emulation or disk
images.

%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

cp -p %{S:1} %{S:2} .

sed \
  -e '/^VERSION =/s|=.*$|= %{version}|' \
  -e '/^target=/s|$(prefix)||' \
  -e '/^PROGS/s|=|\0 error_recalc|g' \
  -e '/^install:/s|:|\0 install-error_recalc|' \
  -i Makefile

%build
%set_build_flags
%make_build


%install
%make_install prefix=%{_prefix} bindir=%{_bindir} mandir=%{_mandir}

rm -f %{buildroot}%{_mandir}/man1/ecm2bin.1
echo '.so man1/bin2ecm.1' > %{buildroot}%{_mandir}/man1/ecm2bin.1


%files
%license COPYING
%doc README.adoc
%{_bindir}/*
%{_mandir}/man1/*.1*


%changelog
* Sun Aug 09 2020 Phantom X <megaphantomx at hotmail dot com> - 1.06-2.20180519gite178184
- Add error_recalc utility

* Fri Jun 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.06-1.20180519gite178184
- Initial spec
