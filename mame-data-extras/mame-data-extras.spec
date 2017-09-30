%global debug_package %{nil}
%global __strip /bin/true

%global cheatver 0187
%global historyver 190
%global infover 0190

# Build non redistributable package with free roms
%global with_roms  %{?_with_roms:     1} %{?!_with_roms:     0}
%global romlink http://www.mamedev.org/roms
%global samplelink http://samples.mameworld.info/wav

Name:           mame-data-extras
Version:        0.190
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

# http://www.mameworld.net/mrdo/mame_art
Source10:       scanlines_apertures.zip
#http://www.mameworld.net/mrdo/mame_artwork_supp.html
Source11:       effect_files.zip

# Icons: Mamu icons from http://icons.mameworld.info/
Source20:       http://icons.mameworld.info/icons.zip/icons.zip

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


# Samples from http://samples.mameworld.info/
Source200:      %{samplelink}/alphamc07.zip
Source201:      %{samplelink}/aristmk4.zip
Source202:      %{samplelink}/armora.zip
Source203:      %{samplelink}/astrob.zip
Source204:      %{samplelink}/astrof.zip
Source205:      %{samplelink}/barrier.zip
Source206:      %{samplelink}/battles.zip
Source207:      %{samplelink}/blockade.zip
Source208:      %{samplelink}/buckrog.zip
Source209:      %{samplelink}/carnival.zip
Source210:      %{samplelink}/circus.zip
Source211:      %{samplelink}/congo.zip
Source212:      %{samplelink}/cosmica.zip
Source213:      %{samplelink}/cosmicg.zip
Source214:      %{samplelink}/dai3wksi.zip
Source215:      %{samplelink}/depthch.zip
Source216:      %{samplelink}/elim2.zip
Source217:      %{samplelink}/fantasy.zip
Source218:      %{samplelink}/frogs.zip
Source219:      %{samplelink}/gaplus.zip
Source220:      %{samplelink}/gorf.zip
Source221:      %{samplelink}/gorf_older2.zip
Source222:      %{samplelink}/gridlee.zip
Source223:      %{samplelink}/invaders.zip
Source224:      %{samplelink}/invinco.zip
Source225:      %{samplelink}/journey.zip
Source226:      %{samplelink}/lrescue.zip
Source227:      %{samplelink}/monsterb.zip
Source228:      %{samplelink}/natodef.zip
Source229:      %{samplelink}/panic.zip
Source230:      %{samplelink}/pulsar.zip
Source231:      %{samplelink}/qbert.zip
Source232:      %{samplelink}/rallyx.zip
Source233:      %{samplelink}/reactor.zip
Source234:      %{samplelink}/ripoff.zip
Source235:      %{samplelink}/safarir.zip
Source236:      %{samplelink}/sasuke.zip
Source237:      %{samplelink}/seawolf.zip
#Source238:      %{samplelink}/sharkatt_(full_size).zip
Source239:      %{samplelink}/sharkatt.zip
Source240:      %{samplelink}/solarq.zip
Source241:      %{samplelink}/spacefb.zip
Source242:      %{samplelink}/spaceod.zip
Source243:      %{samplelink}/spacfury.zip
Source244:      %{samplelink}/spacewar.zip
Source245:      %{samplelink}/speedfrk.zip
Source246:      %{samplelink}/starcas.zip
Source247:      %{samplelink}/starcrus.zip
Source248:      %{samplelink}/starhawk.zip
Source249:      %{samplelink}/subroc3d.zip
Source250:      %{samplelink}/sundance.zip
Source251:      %{samplelink}/tailg.zip
Source252:      %{samplelink}/tankbatt.zip
Source253:      %{samplelink}/targ.zip
Source254:      %{samplelink}/thehand.zip
Source255:      %{samplelink}/thief.zip
Source256:      %{samplelink}/triplhnt.zip
Source257:      %{samplelink}/turbo.zip
Source258:      %{samplelink}/vanguard.zip
Source259:      %{samplelink}/warrior.zip
Source260:      %{samplelink}/wotw.zip
Source261:      %{samplelink}/wow.zip
Source262:      %{samplelink}/zaxxon.zip
Source263:      %{samplelink}/zektor.zip
%global samplefiles %{SOURCE200} %{SOURCE201} %{SOURCE202} %{SOURCE203} %{SOURCE204} %{SOURCE205} %{SOURCE206} %{SOURCE207} %{SOURCE208} %{SOURCE209} %{SOURCE210} %{SOURCE211} %{SOURCE212} %{SOURCE213} %{SOURCE214} %{SOURCE215} %{SOURCE216} %{SOURCE217} %{SOURCE218} %{SOURCE219} %{SOURCE220} %{SOURCE221} %{SOURCE222} %{SOURCE223} %{SOURCE224} %{SOURCE225} %{SOURCE226} %{SOURCE227} %{SOURCE228} %{SOURCE229} %{SOURCE230} %{SOURCE231} %{SOURCE232} %{SOURCE233} %{SOURCE234} %{SOURCE235} %{SOURCE236} %{SOURCE237} %{SOURCE239} %{SOURCE240} %{SOURCE241} %{SOURCE242} %{SOURCE243} %{SOURCE244} %{SOURCE245} %{SOURCE246} %{SOURCE247} %{SOURCE248} %{SOURCE249} %{SOURCE250} %{SOURCE251} %{SOURCE252} %{SOURCE253} %{SOURCE254} %{SOURCE255} %{SOURCE256} %{SOURCE257} %{SOURCE258} %{SOURCE259} %{SOURCE260} %{SOURCE261} %{SOURCE262} %{SOURCE263}

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
%endif

# extract DAT files
unzip %{SOURCE0}
7z x %{SOURCE1}
unzip -qa %{SOURCE2} -d .
7z x Mameinfo%{infover}.7z
mv docs mameinfo

mkdir effects
unzip %{SOURCE10} -d effects/
unzip %{SOURCE11} -d effects/

mkdir -p icons/png
unzip %{SOURCE20} -d icons

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

mkdir -p %{buildroot}%{_datadir}/mame

%if %{with_roms}
# Install ROMs
mkdir -p %{buildroot}%{_datadir}/mame/roms
install -pm0644 %{romfiles} \
  %{buildroot}%{_datadir}/mame/roms/
%endif

# Install DAT files
install -pm 644 history.dat mameinfo.dat \
  %{buildroot}%{_datadir}/mame/

# Install cheat files
mkdir -p %{buildroot}%{_datadir}/mame/cheat
install -pm0644 cheat.7z %{buildroot}%{_datadir}/mame/cheat/

# Install Samples
mkdir -p %{buildroot}%{_datadir}/mame/samples
install -pm0644 %{samplefiles} \
  %{buildroot}%{_datadir}/mame/samples/

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
%doc cheat.txt mameinfo README.icons
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
%doc README.roms
%files roms
%{_datadir}/mame/roms/*.zip
%endif


%changelog
* Fri Sep 29 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.190-1
- 0.190

* Thu Sep 07 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.189-1
- 0.189
- Fix installation without roms
- Fix sample files

* Sun Aug 13 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.188-1
- 0.188

* Sat Jul 01 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.187-1
- 0.187

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.186-1
- 0.186

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
