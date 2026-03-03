# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

BuildArch:      noarch

# Speep up packaging, no rpaths to search here
%global __brp_check_rpaths %{nil}

%global fullset 258
%global update %%(echo %{version} | cut -d. -f2)

Name:           mame-data-icons
Version:        0.269
Release:        1%{?dist}
Summary:        MAMU_'s icon set for MAME front-ends

License:        Non-redistributable
%dnl URL:            https://icons.mameworld.info/
URL:            https://www.progettosnaps.net/icons/

# Download it at https://icons.mameworld.info/
%dnl Source0:        icons.zip
Source0:        https://www.progettosnaps.net/download/?tipo=icons&file=/icons/packs/pS_icons_fullset_%{fullset}.zip
%if 0%{?update}
Source1:        https://www.progettosnaps.net/download/?tipo=icons&file=/icons/packs/pS_icons_upd_%{update}.zip
%endif

BuildRequires:  7zip-standalone
BuildRequires:  findutils
BuildRequires:  ImageMagick
BuildRequires:  optipng
BuildRequires:  unzip
Requires:       mame-data-extras >= 0.232

%description
%{summary}.


%prep
%autosetup -c



i=README
mv ReadMe_Icons.txt $i
sed 's/\r//' -i $i
iconv -f utf-8 $i -t utf-8 -o $i.new && mv -f $i.new $i

7za x -oico icons.7z
%if 0%{?update}
unzip %{S:1} -d update
mv -f update/icons/*.ico ico/
%endif


%build
mkdir -p png
rm -f ico/'('*.ico
rm -f ico/'!'*.ico
pushd ico
find -maxdepth 1 -name '*.ico' -print0 | xargs -0 -r -I FILE -P %{_smp_build_ncpus} magick FILE[1] ../png/FILE.png
popd
rename '.ico' '' png/*.png
find png -maxdepth 1 -name '*.png' -print0 | xargs -0 -r -I FILE -P %{_smp_build_ncpus} optipng -quiet -preserve FILE


%install
mkdir -p %{buildroot}%{_datadir}/mame/icons
install -pm0644 png/*.png %{buildroot}%{_datadir}/mame/icons/

%files
%doc README
%{_datadir}/mame/icons/*.png


%changelog
* Mon Mar 02 2026 - 0.269-1
- 0.269

* Sat May 29 2021 - 0.145u4-1
- Initial spec
