# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

Name:           mame-data-icons
Version:        0.145~u4
Release:        1%{?dist}
Summary:        MAMU_'s icon set for MAME front-ends

License:        Non-redistributable
URL:            https://icons.mameworld.info/

# Download it at https://icons.mameworld.info/
Source0:        icons.zip

BuildArch:      noarch

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
mv *READ.txt $i
iconv -f utf-16 $i -t utf-8 -o $i.new && mv -f $i.new $i
sed 's/\r//' -i README


%build
mkdir -p png
rm -f '('*.ico
rm -f '!'*.ico
find -maxdepth 1 -name '*.ico' -print0 | xargs -0 -r -I FILE -P %{_smp_build_ncpus} magick FILE[1] png/FILE.png
rename '.ico' '' png/*.png
find png -maxdepth 1 -name '*.png' -print0 | xargs -0 -r -I FILE -P %{_smp_build_ncpus} optipng -quiet -preserve FILE


%install
mkdir -p %{buildroot}%{_datadir}/mame/icons
install -pm0644 png/*.png %{buildroot}%{_datadir}/mame/icons/

%files
%doc README
%{_datadir}/mame/icons/*.png


%changelog
* Sat May 29 2021 - 0.145u4-1
- Initial spec
