# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%global buildforkernels akmod

%global debug_package %{nil}

%define repo chinforpms

%global commit 67ecf76b95fcaf9a70e54b0d25b485f4e135e439
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240214

%global dist .%{date}git%{shortcommit}%{?dist}

%global vc_url https://repo.or.cz/linux/zf.git/blob_plain

Name:           ntsync-kmod
Version:        6.8~rc3
Release:        1%{?dist}
Summary:        NT synchronization primitive driver

License:        GPL-2.0-only
URL:            https://repo.or.cz/linux/zf.git/shortlog/refs/heads/ntsync5

Source0:        %{vc_url}/%{commit}:/drivers/misc/ntsync.c#/ntsync.c_%{shortcommit}
Source1:        %{vc_url}/%{commit}:/include/uapi/linux/ntsync.h#/ntsync.h_%{shortcommit}
Source2:        Makefile
Source3:        ntsync-kmod-excludekernel-filter.txt

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
  cp -p %{SOURCE0} _kmod_build_${kernel_version%%___*}/ntsync.c
  cp -p %{SOURCE1} _kmod_build_${kernel_version%%___*}/include/uapi/linux/ntsync.h
  cp -p %{SOURCE2} _kmod_build_${kernel_version%%___*}/Makefile
%dnl  patch -p1 -s --fuzz=0 --no-backup-if-mismatch -f -d _kmod_build_${kernel_version%%___*}/ -i %{SOURCE4}
done

%build
for kernel_version in %{?kernel_versions}; do
  make %{?_smp_mflags} -C "${kernel_version##*___}" M=${PWD}/_kmod_build_${kernel_version%%___*} modules
done

%install
for kernel_version in %{?kernel_versions}; do
  install -D -m 0755 _kmod_build_${kernel_version%%___*}/ntsync.ko %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/ntsync.ko
done
%{?akmod_install}


%changelog
* Wed Feb 21 2024 Phantom X <megaphantomx at hotmail dot com> - 6.8~rc3-1.20240214git67ecf76
- Initial spec

