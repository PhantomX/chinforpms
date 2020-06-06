%global commit e178184cfd86f3fce0882a24ec425c163ac5964b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180519
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           cmdpack
Version:        1.06
Release:        1%{?gver}%{?dist}
Summary:        Collection of command line utilities, most for emulation or disk images

License:        GPLv3
URL:            https://github.com/chungy/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  asciidoc
BuildRequires:  gcc


%description
%{name} is a collection of command line utilities, most for emulation or disk
images.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

sed \
  -e '/^VERSION =/s|=.*$|= %{version}|' \
  -e '/^target=/s|$(prefix)||' \
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
* Fri Jun 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.06-1.20180519gite178184
- Initial spec
