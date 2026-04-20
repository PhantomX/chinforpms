# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%bcond snap 1

%global vivaldi_dir %{_libdir}/vivaldi

%ifarch aarch64
%bcond snap 0
%global parch arm64
%global snaprev 110
%global snap_ffmpeg_hash 7500c6d0cc44031221b0d89f735b32766ad817f7ac94ad0e193d2981ad31c47e
%else
%global parch amd64
%global zipver 0.103.1
%global snapid XXzVIXswXKHqlUATPqGCj2w2l7BxosS8
%global snaprev 109
%global snap_ffmpeg_hash f374eccea0196a1f6bae9f34bbacac7af67a5bf2191c8a3f60307b1c176f926c
%global snap_ffmpeg_ver git-2026-02-09
%global zip_ffmpeg_hash d7633f6fb36313b78545fe09dfea03960ce58bcfa2577c77020262a9ddbe9246
%global zip_ffmpeg_ver %%(echo %{version} | cut -d. -f3)
%endif
%if %{with snap}
%global ffmpeg_hash %{snap_ffmpeg_hash}
%global ffmpeg_ver %{snap_ffmpeg_ver}
%else
%global ffmpeg_hash %{zip_ffmpeg_hash}
%global ffmpeg_ver %{zip_ffmpeg_ver}
%endif

%global pkgname chromium-codecs-ffmpeg-extra
%global pkgdistro 0ubuntu0.18.04.1
%global vivaldi_ver %%(echo %{version} | cut -d. -f-2)

Name:           vivaldi-ffmpeg-codecs
Version:        7.9.121586
Release:        1%{?dist}
Summary:        Additional support for proprietary codecs for Vivaldi

License:        LGPL-2.1-only
URL:            https://ffmpeg.org/

%if %{with snap}
Source0:        https://api.snapcraft.io/api/v1/snaps/download/%{snapid}_%{snaprev}.snap#/%{name}-%{ffmpeg_ver}.snap
Source1:        copyright
ExclusiveArch:  x86_64
BuildRequires:  squashfs-tools
%else
Source0:        https://github.com/nwjs-ffmpeg-prebuilt/nwjs-ffmpeg-prebuilt/releases/download/%{zipver}/%{zipver}-linux-x64-gn.zip#/%{name}-%{ffmpeg_ver}-x64.zip
BuildRequires:  unzip
%endif
BuildRequires:  gawk
BuildRequires:  coreutils

ExclusiveArch:  x86_64 aarch64

%global __provides_exclude_from ^%{vivaldi_dir}/.*
%global __requires_exclude ^libffmpeg.so.*


%description
%{summary}.


%prep
%setup -c -T

%if %{with snap}
unsquashfs -n -d %{name} %{S:0}

cp %{S:1} .
mv %{name}/chromium-ffmpeg-%{ffmpeg_ver}/chromium-ffmpeg/libffmpeg.so .
%else
unzip %{S:0}
%endif

%dnl RVER="$(grep -aom1 'N-[0-9]\+-' libffmpeg.so | cut -d- -f2)"
%dnl if [ "${RVER}" != "%{ffmpeg_ver}" ] ;then
%dnl   echo "Version mismatch. You have ${RVER} in %{S:0} instead %{ffmpeg_ver} "
%dnl   echo "Edit Version and try again"
%dnl   exit 1
%dnl fi

RHASH="$(sha256sum libffmpeg.so | awk '{print $1}')"
if [ "${RHASH}" != "%{ffmpeg_hash}" ] ;then
  echo "Hash mismatch. You have ${RHASH} in %{S:0} instead %{ffmpeg_hash} "
  echo "Edit ffmpeg_hash and try again"
  exit 1
fi

%build


%install
mkdir -p %{buildroot}%{vivaldi_dir}
install -pm0755 libffmpeg.so %{buildroot}%{vivaldi_dir}/libffmpeg.so.%{vivaldi_ver}

%files
%if %{with snap}
%license copyright
%endif
%{vivaldi_dir}/libffmpeg.so.%{vivaldi_ver}


%changelog
* Thu Apr 16 2026 - 7.9.121586-1
- 121586

* Thu Mar 19 2026 - 7.9.120726-1
- Set vivaldir_ver to 7.9

* Sat Jan 31 2026 - 7.8.120726-1
- Set vivaldir_ver to 7.8

* Fri Nov 14 2025 - 7.7.120726-1
- Set vivaldir_ver to 7.7

* Thu Sep 18 2025 - 7.6.120726-1
- Set vivaldir_ver to 7.6

* Thu Jul 03 2025 - 7.5.120726-1
- 7.5.120726

* Mon May 19 2025 - 7.4.119605-1
- 7.4.119605

* Thu Mar 27 2025 - 7.3.118356-1
- Set vivaldir_ver to 7.3

* Tue Mar 18 2025 - 7.2.118356-1
- Set vivaldir_ver to 7.2

* Thu Jan 23 2025 - 7.1.118356-1
- 7.1.118356

* Thu Oct 24 2024 - 7.0.115541-1
- Set vivaldir_ver to 7.0
- Rework version tag

* Fri Aug 30 2024 - 115541-2
- Set vivaldir_ver to 6.9

* Thu Jun 20 2024 - 115541-1
- 115541

* Fri Apr 26 2024 - 114023-2
-  Set vivaldir_ver to 6.7

* Mon Mar 04 2024 - 114023-1
- 114023, vivaldir_ver 6.6

* Sun Dec 24 2023 - 112.0.5615.49-4
- Set vivaldir_ver to 6.5

* Thu Oct 26 2023 - 112.0.5615.49-3
- Set vivaldir_ver to 6.4

* Fri Sep 01 2023 - 112.0.5615.49-2
- Set vivaldir_ver to 6.2

* Mon Jul 17 2023 - 112.0.5615.49-1
- 112.0.5615.49

* Thu Mar 16 2023 - 110.0.5481.100-1
- 110.0.5481.100

* Fri Dec 09 2022 - 108.0.5327.0-1
- 108.0.5327.0

* Mon Oct 31 2022 - 106.0.5249.30-1
- 106.0.5249.30

* Wed Oct 05 2022 - 106.0.5249.12-1
- Initial spec

