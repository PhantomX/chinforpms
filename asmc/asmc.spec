%global commit df80e2f33b61440afe935a2a6a57729800c1073e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230605
%bcond_without snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

# Use provided binary for first time bootstrap
# Set to 0 after
%global bootstrap 0

%undefine _debugsource_packages

%ifarch x86_64
%global platform 64
%endif

Name:           asmc
Version:        2.34.37
Release:        1%{?dist}
Summary:        Asmc Macro Assembler

License:        GPL-2.0-only
URL:            https://github.com/nidud/asmc

ExclusiveArch:  %{ix86} x86_64

%if %{with snapshot}
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
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

sed \
  -e 's|gcc |\0$(CFLAGS) |' \
  -e '/gcc/s| -s | |' \
  -e '/gcc/s|$@|\0 $(LDFLAGS)|' \
  -e '/chmod/d' \
  -i source/%{name}/gcc/makefile


%build
%set_build_flags


mkdir stage1

%if 0%{?bootstrap}
  chmod +x bin/%{name}{,64}
  bsbin="../../../bin/%{name}%{platform}"
%else
  rm -f bin/*
  bsbin=%{name}%{platform}
%endif

for i in %{name}{,64} ;do
  make -C source/%{name}/gcc -f ./makefile ${i} clean CC=${bsbin}
  mv source/%{name}/gcc/${i} stage1/
done

rm -f bin/*

mkdir stage2

for i in %{name}{,64} ;do
  make -C source/%{name}/gcc -f ./makefile ${i} clean CC=../../../stage1/%{name}%{platform}
  mv source/%{name}/gcc/${i} stage2/
done

for i in %{name}{,64} ;do
  make -C source/%{name}/gcc -f ./makefile ${i} clean CC=../../../stage2/%{name}%{platform}
done


%check
for i in %{name}{,64} ;do
  cmp stage2/${i} source/%{name}/gcc/${i}
done


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

