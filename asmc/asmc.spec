%global commit 3042bffaceea9f2750ee5d5d6159aaecd6e838a3
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250710
%bcond snapshot 1

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

# Use provided binary for first time bootstrap
# Set to 0 after
%global bootstrap 0

%undefine _debugsource_packages

%global _smp_build_ncpus 1

%ifarch x86_64
%global platform 64
%endif

Name:           asmc
Version:        2.37.15
Release:        1%{?dist}
Summary:        Asmc Macro Assembler

License:        GPL-2.0-only
URL:            https://github.com/nidud/asmc

ExclusiveArch:  %{ix86} x86_64

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%dnl Source0:             https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{name}/%{name}-%{shortcommit}.tar.gz/187e7ff180858e19e20c1ebcc0c5e273/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  binutils
%if !0%{?bootstrap}
BuildRequires:  asmc
%endif

%description
%{summary}.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

sed \
  -e '/^all:/s| clean||g' \
  -e '/link/s| -s$||' \
  -e 's/,-pie//' \
  -e '/chmod/d' \
  -i source/%{name}/makefile


%build

mkdir stage1

%if 0%{?bootstrap}
  chmod +x bin/%{name}{,64}
  bsbin="../../bin/%{name}%{platform}"
%else
  rm -rf bin/*
  bsbin=%{name}
%endif

%make_build -C source/%{name} -f ./makefile clean YACC=1 CC=${bsbin} || :
%make_build -C source/%{name} -f ./makefile %{name}%{platform} CC=${bsbin} YACC=1
mv source/%{name}/%{name}%{platform} stage1/

rm -rf bin/*

mkdir stage2

%make_build -C source/%{name} -f ./makefile clean YACC=1 CC=../../stage1/%{name}%{platform}
%make_build -C source/%{name} -f ./makefile %{name}%{platform} YACC=1 CC=../../stage1/%{name}%{platform}
mv source/%{name}/%{name}%{platform} stage2/

%make_build -C source/%{name} -f ./makefile clean YACC=1 CC=../../stage2/%{name}%{platform}
%make_build -C source/%{name} -f ./makefile %{name}%{platform} YACC=1 CC=../../stage2/%{name}%{platform}


%check
cmp stage2/%{name}%{platform} source/%{name}/%{name}%{platform}


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 source/%{name}/%{name}%{platform} %{buildroot}%{_bindir}/%{name}


%files
%license license.txt
%doc readme.md doc
%{_bindir}/%{name}


%changelog
* Sun Jul 13 2025 Phantom X <megaphantomx at hotmail dot com> - 2.37.15-1.20250710git3042bff
- 2.37.15

* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 2.36.24-1.20250201git512bfcd
- 2.36.24

* Fri Dec 20 2024 Phantom X <megaphantomx at hotmail dot com> - 2.36.12-1.20240913gitde51b34
- 2.36.12

* Thu Sep 19 2024 Phantom X <megaphantomx at hotmail dot com> - 2.35.07-1.20240913gitde51b34
- 2.35.07

* Sun Aug 18 2024 Phantom X <megaphantomx at hotmail dot com> - 2.35.03-1.20240815gitdca011b
- 2.35.03

* Sat Jun 29 2024 Phantom X <megaphantomx at hotmail dot com> - 2.34.70-1.20240628gitdb4a4e6
- 2.34.70

* Sun May 19 2024 Phantom X <megaphantomx at hotmail dot com> - 2.34.59-1.20240510gitf3283c5
- 2.34.59

* Tue Mar 26 2024 Phantom X <megaphantomx at hotmail dot com> - 2.34.49-1.20240326git1254636
- 2.34.49

* Sun Feb 11 2024 Phantom X <megaphantomx at hotmail dot com> - 2.34.39-1.20240202git4935c97
- 2.34.39

* Sat Jan 20 2024 Phantom X <megaphantomx at hotmail dot com> - 2.34.38-1.20240104gita32d99a
- 2.34.38

* Thu Jun 29 2023 Phantom X <megaphantomx at hotmail dot com> - 2.34.37-1.20230605gitdf80e2f
- 2.34.37

* Wed Mar 15 2023 Phantom X <megaphantomx at hotmail dot com> - 2.34.25-1.20230315git3fe11ba
- 2.34.25

* Tue Aug 16 2022 Phantom X <megaphantomx at hotmail dot com> - 2.34.15-1.20220720git1f6ac16
- 2.34.15

* Mon Jun 27 2022 Phantom X <megaphantomx at hotmail dot com> - 2.34.01-1.20220621gite0454b0
- 2.34.01

* Mon Jun 20 2022 Phantom X <megaphantomx at hotmail dot com> - 2.34-1.20220619git33834a2
- Initial spec

