%global commit 33834a2ccffe665a264b45afd1d7f39c85e5f454
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220619
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

# Set to 0 after bootstrap
%global bootstrap 0

%undefine _debugsource_packages

%ifarch x86_64
%global platform 64
%endif

Name:           asmc
Version:        2.34
Release:        1%{?gver}%{?dist}
Summary:        Asmc Macro Assembler

License:        GPLv2
URL:            https://github.com/nidud/asmc

ExclusiveArch:  %{ix86} x86_64

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

%if !0%{?bootstrap}
BuildRequires:  asmc
%endif
BuildRequires:  gcc

%description
%{summary}.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

rm -f bin/*.exe

%if 0%{?bootstrap}
  chmod +x bin/%{name}{,64}
  sed -e '/CC =/s|asmc64|%{name}%{platform}|' -i source/%{name}/gcc/makefile
%else
  rm -f bin/%{name}{,64}
  sed -e '/chmod/d' -i source/%{name}/gcc/makefile
  sed -e 's|^CC =.*|CC = %{name}%{platform}|' -i source/%{name}/gcc/makefile
%endif

sed \
  -e 's|,-pie,-z,now,|,|g' \
  -e 's|gcc |\0$(CFLAGS) |' \
  -e '/gcc/s| -s | |' \
  -e '/gcc/s|$@|\0 $(LDFLAGS)|' \
  -i source/%{name}/gcc/makefile

%build
%set_build_flags
make -C source/%{name}/gcc -f ./makefile %{name}
make -C source/%{name}/gcc -f ./makefile %{name}64

%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 source/%{name}/gcc/%{name} %{buildroot}%{_bindir}/
install -pm0755 source/%{name}/gcc/%{name}64 %{buildroot}%{_bindir}/


%files
%license LICENSE
%doc readme.md doc
%{_bindir}/%{name}
%{_bindir}/%{name}64


%changelog
* Mon Jun 20 2022 Phantom X <megaphantomx at hotmail dot com> - 2.34-1.20220619git33834a2
- Initial spec

