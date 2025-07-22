# prevent library files from being installed
%global cargo_install_lib 0

# Use vendor tarball
%bcond vendor 1

%global vendor_hash ba5dbe61204970d8da85234f34c32e84

%global appname com.mtkennerly.%{name}

Name:           ludusavi
Version:        0.29.1
Release:        1%{?dist}
Summary:        Game save backup tool

License:        MIT
URL:            https://github.com/mtkennerly/%{name}

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%if %{with vendor}
# rust2rpm -t fedora -V auto --no-rpmautospec --ignore-missing-license-files --path %%{name}-%%{version}
Source1:        https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{name}/%{name}-%{version}-vendor.tar.xz/%{vendor_hash}/%{name}-%{version}-vendor.tar.xz
%endif

ExclusiveArch:  %{rust_arches}

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  librsvg2-tools
BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  rust-packaging
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
Requires:       hicolor-icon-theme

%description
Ludusavi is a tool for backing up your PC video game save data.


%prep
%autosetup -p1 %{?with_vendor:-a1}

find -name '*.rs' -exec chmod -x {} ';'

%if %{with vendor}
# Dirty fix shebang error
sed -e'1i //placeholder' -i vendor/typed-path-*/src/lib.rs
typedpath_hash="$(sha256sum vendor/typed-path-*/src/lib.rs 2>&1 |cut -d" " -f1)"
sed \
  -e 's|"src/lib.rs":"[^"]*"|"src/lib.rs":"'${typedpath_hash}'"|' \
  -i vendor/typed-path-*/.cargo-checksum.json

%cargo_prep -v vendor

%else
%generate_buildrequires
%cargo_generate_buildrequires
%endif


%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%if %{with vendor}
%{cargo_vendor_manifest}
%endif


%install
%cargo_install

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --remove-key=Encoding \
  assets/linux/%{appname}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
ln -sf assets/icon.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{appname}.svg

for res in 16 22 24 32 36 48 64 72 96 128 192 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  rsvg-convert assets/icon.svg -h ${res} -w ${res} \
    -o ${dir}/%{appname}.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 assets/linux/%{appname}.metainfo.xml %{buildroot}%{_metainfodir}/


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml


%files
%license LICENSE
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/*/%{appname}*
%{_metainfodir}/%{appname}.metainfo.xml


%changelog
* Wed Jun 04 2025 Phantom X <megaphantomx at hotmail dot com> - 0.29.1-1
- Initial spec
