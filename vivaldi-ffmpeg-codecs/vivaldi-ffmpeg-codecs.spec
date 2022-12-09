# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global vivaldi_ver 5.6
%global vivaldi_dir %{_libdir}/vivaldi

%ifarch aarch64
%global parch arm64
%global pkgid 628097503
%else
%global parch amd64
%global pkgid 628079667
%endif

%global pkgname chromium-codecs-ffmpeg-extra
%global pkgdistro 0ubuntu9.18.04


Name:           vivaldi-ffmpeg-codecs
Version:        108.0.5327.0
Release:        1%{?dist}
Summary:        Additional support for proprietary codecs for Vivaldi

License:        LGPL2
URL:            https://ffmpeg.org/

Source0:        https://launchpadlibrarian.net/%{pkgid}/%{pkgname}_%{version}-%{pkgdistro}_%{parch}.deb

ExclusiveArch:  x86_64 aarch64

%global __provides_exclude_from ^%{vivaldi_dir}/.*
%global __requires_exclude ^libffmpeg.so.*


%description
%{summary}.


%prep
%setup -c -T

ar p %{S:0} data.tar.xz | tar xJ -C .

%build


%install
mkdir -p %{buildroot}%{vivaldi_dir}
install -pm0755 usr/lib/chromium-browser/libffmpeg.so %{buildroot}%{vivaldi_dir}/libffmpeg.so.%{vivaldi_ver}

%files
%license usr/share/doc/%{pkgname}/copyright
%{vivaldi_dir}/libffmpeg.so.%{vivaldi_ver}


%changelog
* Fri Dec 09 2022 - 108.0.5327.0-1
- 108.0.5327.0

* Mon Oct 31 2022 - 106.0.5249.30-1
- 106.0.5249.30

* Wed Oct 05 2022 - 106.0.5249.12-1
- Initial spec

