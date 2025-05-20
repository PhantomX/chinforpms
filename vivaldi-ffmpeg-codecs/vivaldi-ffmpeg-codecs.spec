# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%bcond_without snap

%global vivaldi_dir %{_libdir}/vivaldi

%ifarch aarch64
%global parch arm64
%global pkgid 660838579
%global snaprev 67
%else
%global parch amd64
%global pkgid 660647727
%global snapid XXzVIXswXKHqlUATPqGCj2w2l7BxosS8
%global snaprev 76
%endif

%global pkgname chromium-codecs-ffmpeg-extra
%global pkgdistro 0ubuntu0.18.04.1
%global ffmpeg_ver %%(echo %{version} | cut -d. -f3)
%global vivaldi_ver %%(echo %{version} | cut -d. -f-2)

Name:           vivaldi-ffmpeg-codecs
Version:        7.4.119605
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
Source0:        https://launchpadlibrarian.net/%{pkgid}/%{pkgname}_%{ffmpeg_ver}-%{pkgdistro}_%{parch}.deb
ExclusiveArch:  x86_64 aarch64
%endif

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
ar p %{S:0} data.tar.xz | tar xJ -C .
mv usr/lib/chromium-browser/libffmpeg.so .
mv usr/share/doc/%{pkgname}/copyright .
%endif

RVER="$(grep -aom1 'N-[0-9]\+-' libffmpeg.so | cut -d- -f2)"
if [ "${RVER}" != "%{ffmpeg_ver}" ] ;then
  echo "Version mismatch. You have ${RVER} in %{S:0} instead %{ffmpeg_ver} "
  echo "Edit Version and try again"
  exit 1
fi

%build


%install
mkdir -p %{buildroot}%{vivaldi_dir}
install -pm0755 libffmpeg.so %{buildroot}%{vivaldi_dir}/libffmpeg.so.%{vivaldi_ver}

%files
%license copyright
%{vivaldi_dir}/libffmpeg.so.%{vivaldi_ver}


%changelog
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

