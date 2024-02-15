%global commit 4935c972eb15f170f36412974e6f86a48ee83324
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240202
%bcond_without snapshot

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
Version:        2.34.39
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

%if !0%{?bootstrap}
BuildRequires:  asmc
%endif
BuildRequires:  gcc

%description
%{summary}.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

sed \
  -e '/^all:/s| clean||g' \
  -e 's|gcc |\0$(CFLAGS) |' \
  -e '/gcc/s| -s | |' \
  -e '/gcc/s|$@|\0 $(LDFLAGS)|' \
  -e '/chmod/d' \
  -i source/%{name}/makefile


%build
%set_build_flags


mkdir stage1

%if 0%{?bootstrap}
  chmod +x bin/%{name}{,64}
  bsbin="../../bin/%{name}%{platform}"
%else
  rm -f bin/*
  bsbin=%{name}%{platform}
%endif

for i in %{name}{,64} ;do
  %make_build -C source/%{name} -f ./makefile clean YACC=1 CC=${bsbin} || :
  %make_build -C source/%{name} -f ./makefile ${i} CC=${bsbin} YACC=1
  mv source/%{name}/${i} stage1/
done

rm -f bin/*

mkdir stage2

for i in %{name}{,64} ;do
  %make_build -C source/%{name} -f ./makefile clean YACC=1 CC=../../stage1/%{name}%{platform}
  %make_build -C source/%{name} -f ./makefile ${i} YACC=1 CC=../../stage1/%{name}%{platform}
  mv source/%{name}/${i} stage2/
done

for i in %{name}{,64} ;do
  %make_build -C source/%{name} -f ./makefile clean YACC=1 CC=../../stage2/%{name}%{platform}
  %make_build -C source/%{name} -f ./makefile ${i} YACC=1 CC=../../stage2/%{name}%{platform}
done


%check
for i in %{name}{,64} ;do
  cmp stage2/${i} source/%{name}/${i}
done


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 source/%{name}/%{name} %{buildroot}%{_bindir}/
install -pm0755 source/%{name}/%{name}64 %{buildroot}%{_bindir}/


%files
%license LICENSE
%doc readme.md doc
%{_bindir}/%{name}
%{_bindir}/%{name}64


%changelog
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

