# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%bcond_without snap

%global vivaldi_ver 6.6
%global vivaldi_dir %{_libdir}/vivaldi

%ifarch aarch64
%global parch arm64
%global pkgid 660838579
%else
%global parch amd64
%global pkgid 660647727
%global snapid XXzVIXswXKHqlUATPqGCj2w2l7BxosS8
%global snaprev 37
%endif

%global pkgname chromium-codecs-ffmpeg-extra
%global pkgdistro 0ubuntu0.18.04.1
%global ffmpeg_ver 114023

Name:           vivaldi-ffmpeg-codecs
Version:        114023
Release:        1%{?dist}
Summary:        Additional support for proprietary codecs for Vivaldi

License:        LGPL-2.1-only
URL:            https://ffmpeg.org/

%if %{with snap}
Source0:        https://api.snapcraft.io/api/v1/snaps/download/%{snapid}_%{snaprev}.snap#/%{name}-%{version}.snap
Source1:        copyright
ExclusiveArch:  x86_64
BuildRequires:  squashfs-tools
%else
Source0:        https://launchpadlibrarian.net/%{pkgid}/%{pkgname}_%{version}-%{pkgdistro}_%{parch}.deb
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
mv %{name}/chromium-ffmpeg-%{version}/chromium-ffmpeg/libffmpeg.so .
%else
ar p %{S:0} data.tar.xz | tar xJ -C .
mv usr/lib/chromium-browser/libffmpeg.so .
mv usr/share/doc/%{pkgname}/copyright .
%endif

RVER="$(grep -aom1 'N-[0-9]\+-' libffmpeg.so | cut -d- -f2)"
if [ "${RVER}" != "%{version}" ] ;then
  echo "Version mismatch. You have ${RVER} in %{S:0} instead %{version} "
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
* Mon Mar 04 2024 Phantom X <megaphantomx at hotmail dot com> - 114023-1
- 114023, vivaldir_ver 6.6

* Sun Dec 24 2023 Phantom X <megaphantomx at hotmail dot com> - 112.0.5615.49-4
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

