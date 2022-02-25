%global commit 7c2af65066e8174ca2eec36978213cca7ac61030
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220223
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

# Set to 0 after bootstrap
%global bootstrap 1

%undefine _debugsource_packages
%undefine _hardened_build
%global _lto_cflags %{nil}

%ifarch x86_64
%global platform 64
%endif
%global makefile GccLinux%{?platform}.mak

Name:           asmc
Version:        2.33.44
Release:        0%{?gver}%{?dist}
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
  sed -e '/AFLAGS/s|asmc64|../../bin/\0|' -i source/%{name}/GccLinux64.mak
%else
  rm -f bin/%{name}{,64}
  sed -e '/AFLAGS/s|../../bin/||' -i source/%{name}/GccLinux.mak
%endif

sed \
  -e 's|gcc -o|gcc $(CFLAGS) -o|' \
  -e '/gcc/s|$@|\0 $(LDFLAGS)|' \
  -i source/asmc/%{makefile}

%build
%set_build_flags
%ifarch x86_64
make -C source/asmc -f ./%{makefile}
make -C source/asmc -f ./%{makefile} X64=1
%else
make -C source/asmc -f ./%{makefile}
make -C source/asmc -f ./%{makefile} ASMC64=1
%endif

%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 source/asmc/%{name} %{buildroot}%{_bindir}/
install -pm0755 source/asmc/%{name}64 %{buildroot}%{_bindir}/


%files
%license LICENSE
%doc readme.md doc
%{_bindir}/%{name}
%{_bindir}/%{name}64


%changelog
