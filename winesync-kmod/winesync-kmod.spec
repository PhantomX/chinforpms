# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%global buildforkernels akmod

%global debug_package %{nil}

%define repo chinforpms

%global commit 9ac10c6e711ec096274ecc676ae83a7cf2a1213f
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220513

%global gver .%{date}git%{shortcommit}

%global vc_url https://repo.or.cz/linux/zf.git/blob_plain

Name:           winesync-kmod
Version:        5.16.20
Release:        2%{?gver}%{?dist}
Summary:        Wine synchronization primitive driver

License:        GPLv2
URL:            https://repo.or.cz/linux/zf.git/shortlog/refs/heads/winesync4

Source0:        %{vc_url}/%{commit}:/drivers/misc/winesync.c#/winesync.c_%{shortcommit}
Source1:        %{vc_url}/%{commit}:/include/uapi/linux/winesync.h#/winesync.h_%{shortcommit}
Source2:        Makefile
Source3:        winesync-kmod-excludekernel-filter.txt

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  %{_bindir}/kmodtool
BuildRequires:  %{_bindir}/make
%dnl BuildRequires:  %{_bindir}/patch
%{!?kernels:BuildRequires: buildsys-build-%{repo}-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo %{repo} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} --filterfile %{SOURCE3} 2>/dev/null) }

%description
%{summary}.

This package provides kernel module for kernel %{kversion}.


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo %{repo} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T

for kernel_version in %{?kernel_versions} ; do
  mkdir -p _kmod_build_${kernel_version%%___*}/include/uapi/linux/
  cp -p %{SOURCE0} _kmod_build_${kernel_version%%___*}/winesync.c
  cp -p %{SOURCE1} _kmod_build_${kernel_version%%___*}/include/uapi/linux/winesync.h
  cp -p %{SOURCE2} _kmod_build_${kernel_version%%___*}/Makefile
%dnl  patch -p1 -s --fuzz=0 --no-backup-if-mismatch -f -d _kmod_build_${kernel_version%%___*}/ -i %{SOURCE4}
done

%build
for kernel_version in %{?kernel_versions}; do
  make %{?_smp_mflags} -C "${kernel_version##*___}" M=${PWD}/_kmod_build_${kernel_version%%___*} modules
done

%install
for kernel_version in %{?kernel_versions}; do
  install -D -m 0755 _kmod_build_${kernel_version%%___*}/winesync.ko %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/winesync.ko
done
%{?akmod_install}


%changelog
* Wed Jun 29 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.20-2.20220513git9ac10c6
- Bump

* Tue May 03 2022 Phantom X <megaphantomx at hotmail dot com> - 5.16.20-1.20220421git50ed00e
- 5.16.20

* Mon Dec 06 2021 Phantom X <megaphantomx at hotmail dot com> - 5.15.5-1.20211202gitee18b22
- 5.15.5

* Mon Aug 30 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12.10-1.20210610gitf12fad2
- 5.12.10

* Sat May 22 2021 Phantom X <megaphantomx at hotmail dot com> - 5.12-1.20210507git73f1881
- Initial spec
