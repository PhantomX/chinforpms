%global debug_package %{nil}
%global __strip /bin/true

%global cheatver 0184
%global historyver 185
%global infover 0185

# Build non redistributable package with free roms
%global with_roms  %{?_with_roms:     1} %{?!_with_roms:     0}
%global romlink http://www.mamedev.org/roms

Name:           mame-data-extras
Version:        0.185
Release:        1%{?dist}
Summary:        Extra data files for MAME

License:        Freely redistributable without restriction
URL:            http://mamedev.org

# http://cheat.retrogames.com/
Source0:       http://cheat.retrogames.com/download/cheat%{cheatver}.zip
# http://www.arcade-history.com/
Source1:       http://www.arcade-history.com/dats/history%{historyver}.7z
# http://mameinfo.mameworld.info/
Source2:       http://www.mameworld.info/mameinfo/download/Mameinfo%{infover}.zip

# Samples from http://www.mame.net/downsamples.html
Source10:       sdlmame-samples.tar

# http://www.mameworld.net/mrdo/mame_art
Source20:       scanlines_apertures.zip
#http://www.mameworld.net/mrdo/mame_artwork_supp.html
Source21:       effect_files.zip

# Icons: Mamu icons from http://icons.mameworld.info/
Source30:       http://icons.mameworld.info/icons.zip/icons.zip

%if %{with_roms}
# Distributable ROM images (non-commercial use)
Source100:      README.roms
Source101:      %{romlink}/alienar/alienar.zip
Source102:      %{romlink}/carpolo/carpolo.zip
Source103:      %{romlink}/crash/crash.zip
Source104:      %{romlink}/circus/circus.zip
Source105:      %{romlink}/fax/fax.zip
Source106:      %{romlink}/fireone/fireone.zip
Source107:      %{romlink}/gridlee/gridlee.zip
Source108:      %{romlink}/hardhat/hardhat.zip
Source109:      %{romlink}/looping/looping.zip
Source110:      %{romlink}/ripcord/ripcord.zip
Source111:      %{romlink}/robby/robby.zip
Source112:      %{romlink}/robotbwl/robotbwl.zip
Source113:      %{romlink}/sidetrac/sidetrac.zip
Source114:      %{romlink}/spectar/spectar.zip
Source115:      %{romlink}/starfire/starfire.zip
Source116:      %{romlink}/supertnk/supertnk.zip
Source117:      %{romlink}/targ/targ.zip
Source118:      %{romlink}/teetert/teetert.zip
Source119:      %{romlink}/topgunnr/topgunnr.zip
Source120:      %{romlink}/victory/victory.zip
%global romfiles %{SOURCE101} %{SOURCE102} %{SOURCE103} %{SOURCE104} %{SOURCE105} %{SOURCE106} %{SOURCE107} %{SOURCE108} %{SOURCE109} %{SOURCE110} %{SOURCE111} %{SOURCE112} %{SOURCE113} %{SOURCE114} %{SOURCE115} %{SOURCE116} %{SOURCE117} %{SOURCE118} %{SOURCE119} %{SOURCE120}
%endif

BuildArch: noarch

BuildRequires:  findutils
BuildRequires:  ImageMagick
BuildRequires:  p7zip
BuildRequires:  unzip
Requires:       mame-data

%description
%{summary}.

%package roms
Summary:        Free no-commercial use and non redistributable roms for mame
License:        Free for no-commercial use and non redistributable

Requires:       %{name}

%description roms
%{summary}.

%prep
%autosetup -cT

%if %{with_roms}
  cp %{SOURCE100} .
for file in %{romfiles} ; do
  basefile="$(basename ${file} .zip)"
  if [ "${basefile}" == "alienar" ] ; then
    unzip -qa ${file} Aareadme.txt -d .
    mv Aareadme.txt README.${basefile}
  elif [ "${basefile}" = "gridlee" ] || [ "${basefile}" = "robby" ]  ; then
    unzip -qa ${file} readme.txt -d .
    mv readme.txt README.${basefile}
  fi
done
%endif

# extract DAT files
unzip %{SOURCE0}
7z x %{SOURCE1}
unzip -qa %{SOURCE2} -d .
7z x Mameinfo%{infover}.7z
mv docs mameinfo

mkdir effects
unzip %{SOURCE20} -d effects/
unzip %{SOURCE21} -d effects/

mkdir -p icons/png
unzip %{SOURCE30} -d icons

# fix permissions and line endings
chmod -R u+w,go+r-w,a-s .

chmod 0644 README.* mameinfo/*.txt
chmod 0755 mameinfo
sed 's/\r//' cheat.txt -i mameinfo/*

sed 's/\r//' icons/*READ.txt > README.icons

%build

pushd icons
  rm -f '('*.ico
  rm -f '!'*.ico
  find -maxdepth 1 -name '*.ico' -print0 | xargs -0 -t -r -I FILE -P %(echo %{?_smp_mflags} | sed -e 's|-j||') convert FILE[1] png/FILE.png
  rename '.ico' '' png/*.png
popd

%install

%if %{with_roms}
# Install ROMs
mkdir -p %{buildroot}%{_datadir}/mame/roms
install -pm0644 %{romfiles} \
  %{buildroot}%{_datadir}/mame/roms/
%endif

# Install DAT files
install -pm 644 history/history.dat mameinfo.dat \
  %{buildroot}%{_datadir}/mame/

# Install cheat files
mkdir -p %{buildroot}%{_datadir}/mame/cheat
install -pm0644 cheat.7z %{buildroot}%{_datadir}/mame/cheat/

# Install Samples
mkdir -p %{buildroot}%{_datadir}/mame/samples
tar --extract --directory %{buildroot}%{_datadir}/mame/samples/ \
  --file %{SOURCE10}

# Install Artwork
mkdir -p %{buildroot}%{_datadir}/mame/effects
install -pm0644 effects/*.png %{buildroot}%{_datadir}/mame/effects/

# Install Icons
mkdir -p %{buildroot}%{_datadir}/mame/icons
install -pm0644 icons/png/*.png %{buildroot}%{_datadir}/mame/icons/

# Empty dirs
for file in cab snap ;do
  mkdir -p %{buildroot}%{_datadir}/mame/${file}
  touch %{buildroot}%{_datadir}/mame/${file}/dummy.txt
done


%files
%doc cheat.txt mameinfo
%{_datadir}/mame/*.dat
%dir %{_datadir}/mame/cab
%{_datadir}/mame/cab/*
%dir %{_datadir}/mame/cheat
%{_datadir}/mame/cheat/*.7z
%{_datadir}/mame/effects/*
%dir %{_datadir}/mame/icons
%{_datadir}/mame/icons/*.png
%{_datadir}/mame/samples/*.zip
%dir %{_datadir}/mame/snap
%{_datadir}/mame/snap/*


%if %{with_roms}
%files roms
%doc README.alienar README.gridlee README.robby README.icons
%{_datadir}/mame/roms/*.zip
%endif


%changelog
* Sat Apr 29 2017 Phantom X - 0.185-1
- 0.185
- Pugsy's Cheats to 0.184

* Sat Apr 01 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.184-1
- 0.184

* Thu Feb 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.183-1
- 0.183
- Use proper spec file sessions
- Icon conversion speedup with find and xargs, removing unneeded parallel dependency
- Own some directories

* Wed Feb 08 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.182-1
- 0.182

* Thu Jan 12 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.181-1
- Initial spec
