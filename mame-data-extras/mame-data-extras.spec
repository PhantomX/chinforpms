%global debug_package %{nil}
%global __strip /bin/true

%global cheatver 0264
%global historyver 275
%global infover 0275
%global cheat_url https://www.mamecheat.co.uk
%global history_url https://www.arcade-history.com
%global info_url https://www.mameworld.info/mameinfo

%global samplelink https://www.mameworld.info/samples/wav

Name:           mame-data-extras
Version:        0.275
Release:        1%{?dist}
Summary:        Extra data files for MAME

License:        LicenseRef-Fedora-UltraPermissive
URL:            http://mamedev.org

Source0:       %{cheat_url}/download/cheat%{cheatver}.zip
Source1:       %{history_url}/dats/history%{historyver}.zip
Source2:       %{info_url}/files+/Mameinfo%{infover}.zip

# http://www.mameworld.net/mrdo/mame_art
Source10:       scanlines_apertures.zip
#http://www.mameworld.net/mrdo/mame_artwork_supp.html
Source11:       effect_files.zip

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
#Source238:      #{samplelink}/sharkatt_(full_size).zip
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

BuildRequires:  p7zip
BuildRequires:  p7zip-plugins
BuildRequires:  unzip
Requires:       mame-data

%description
%{summary}.


%prep
%autosetup -cT

# extract DAT files
unzip -q %{SOURCE0}
unzip %{SOURCE1}
unzip -qa %{SOURCE2} -d .
7z x Mameinfo%{infover}.7z
mv docs mameinfo

mkdir effects
unzip -q %{SOURCE10} -d effects/
unzip -q %{SOURCE11} -d effects/

chmod 0644 mameinfo/*.txt
chmod 0755 mameinfo
sed 's/\r//' cheat.txt -i mameinfo/*


%build


%install

mkdir -p %{buildroot}%{_datadir}/mame

# Install DAT files
install -pm 644 history/history.xml mameinfo.dat \
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

# Empty dirs
for file in cab icons roms snap ;do
  mkdir -p %{buildroot}%{_datadir}/mame/${file}
  touch %{buildroot}%{_datadir}/mame/${file}/dummy.txt
done


%files
%doc cheat.txt mameinfo
%{_datadir}/mame/*.dat
%{_datadir}/mame/*.xml
%dir %{_datadir}/mame/cab
%{_datadir}/mame/cab/*
%dir %{_datadir}/mame/cheat
%{_datadir}/mame/cheat/*.7z
%{_datadir}/mame/effects/*
%dir %{_datadir}/mame/icons
%{_datadir}/mame/icons/*
%dir %{_datadir}/mame/roms
%{_datadir}/mame/roms/*
%{_datadir}/mame/samples/*.zip
%dir %{_datadir}/mame/snap
%{_datadir}/mame/snap/*


%changelog
* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 0.275-1
- 0.275

* Wed Dec 04 2024 Phantom X <megaphantomx at hotmail dot com> - 0.272-1
- 0.272

* Sat Sep 28 2024 Phantom X <megaphantomx at hotmail dot com> - 0.270-1
- 0.270

* Sat Aug 31 2024 Phantom X <megaphantomx at hotmail dot com> - 0.269-1
- 0.269

* Tue Jul 09 2024 Phantom X <megaphantomx at hotmail dot com> - 0.267-1
- 0.267

* Sun Jun 02 2024 Phantom X <megaphantomx at hotmail dot com> - 0.266-1
- 0.266

* Sat Apr 27 2024 Phantom X <megaphantomx at hotmail dot com> - 0.265-1
- 0.265

* Thu Mar 28 2024 Phantom X <megaphantomx at hotmail dot com> - 0.258-1
- 0.264

* Wed Aug 30 2023 Phantom X <megaphantomx at hotmail dot com> - 0.258-1
- 0.258

* Sat Jul 29 2023 Phantom X <megaphantomx at hotmail dot com> - 0.257-1
- 0.257

* Thu Jun 29 2023 Phantom X <megaphantomx at hotmail dot com> - 0.256-1
- 0.256

* Thu Jun 01 2023 Phantom X <megaphantomx at hotmail dot com> - 0.255-1
- 0.255

* Sun Apr 30 2023 Phantom X <megaphantomx at hotmail dot com> - 0.254-1
- 0.254

* Mon Apr 03 2023 Phantom X <megaphantomx at hotmail dot com> - 0.253-1
- 0.253

* Sat Feb 25 2023 Phantom X <megaphantomx at hotmail dot com> - 0.252-1
- 0.252

* Mon Jan 02 2023 Phantom X <megaphantomx at hotmail dot com> - 0.251-1
- 0.251

* Sat Dec 03 2022 Phantom X <megaphantomx at hotmail dot com> - 0.250-1
- 0.250

* Sat Nov 05 2022 Phantom X <megaphantomx at hotmail dot com> - 0.249-1
- 0.249

* Sat Oct 01 2022 Phantom X <megaphantomx at hotmail dot com> - 0.248-1
- Mameinfo 0.248
- History 2.48

* Mon Sep 05 2022 Phantom X <megaphantomx at hotmail dot com> - 0.247-1
- Mameinfo 0.247
- History 2.47

* Mon Aug 01 2022 Phantom X <megaphantomx at hotmail dot com> - 0.246-1
- Mameinfo 0.246
- History 2.46

* Sun Jul 03 2022 Phantom X <megaphantomx at hotmail dot com> - 0.245-1
- 0.245

* Fri May 27 2022 Phantom X <megaphantomx at hotmail dot com> - 0.244-1
- Mameinfo 0.244
- History 2.44

* Mon May 02 2022 Phantom X <megaphantomx at hotmail dot com> - 0.243-1
- Mameinfo 0.243
- History 2.43

* Sun Apr 03 2022 Phantom X <megaphantomx at hotmail dot com> - 0.242-1
- Mameinfo 0.242
- History 2.42

* Fri Feb 25 2022 Phantom X <megaphantomx at hotmail dot com> - 0.241-1
- Mameinfo 0.241
- History 2.41

* Tue Feb 01 2022 Phantom X <megaphantomx at hotmail dot com> - 0.240-1
- Mameinfo 0.240
- History 2.40

* Thu Dec 30 2021 Phantom X <megaphantomx at hotmail dot com> - 0.239-1
- Mameinfo 0.239
- History 2.39

* Fri Nov 26 2021 Phantom X <megaphantomx at hotmail dot com> - 0.238-1
- Mameinfo 0.238
- History 2.38

* Thu Oct 28 2021 Phantom X <megaphantomx at hotmail dot com> - 0.237-1
- Mameinfo 0.237
- History 2.37

* Sat Oct 02 2021 Phantom X <megaphantomx at hotmail dot com> - 0.236-1
- Mameinfo 0.236
- History 235a

* Sun Aug 29 2021 Phantom X <megaphantomx at hotmail dot com> - 0.235-1
- Mameinfo 0.235
- History 235

* Wed Aug 04 2021 Phantom X <megaphantomx at hotmail dot com> - 0.234-1
- Mameinfo 0.234
- History 234

* Sat Jul 03 2021 Phantom X <megaphantomx at hotmail dot com> - 0.233-1
- Mameinfo 0.233
- History 233

* Sat May 29 2021 Phantom X <megaphantomx at hotmail dot com> - 0.232-1
- Mameinfo 0.232
- History 232
- Drop icons and roms from this package

* Sat May 01 2021 Phantom X <megaphantomx at hotmail dot com> - 0.231-1
- Mameinfo 0.231
- History 231

* Sat Apr 03 2021 Phantom X <megaphantomx at hotmail dot com> - 0.230-1
- Mameinfo 0.230
- History 230

* Thu Jan 28 2021 Phantom X <megaphantomx at hotmail dot com> - 0.228-1
- Mameinfo 0.228
- History 228, xml

* Sat Jan 02 2021 Phantom X <megaphantomx at hotmail dot com> - 0.227-1
- Mameinfo 0.227
- History 227

* Sat Oct 31 2020 Phantom X <megaphantomx at hotmail dot com> - 0.226-1
- Mameinfo 0.226
- History 226

* Fri Oct  2 2020 Phantom X <megaphantomx at hotmail dot com> - 0.225-1
- Mameinfo 0.225
- History 225
- Optimize png files

* Sun Aug 30 2020 Phantom X <megaphantomx at hotmail dot com> - 0.224-1
- Mameinfo 0.224
- History 224

* Fri Aug 14 2020 Phantom X <megaphantomx at hotmail dot com> - 0.223-1
- Mameinfo 0.223
- History 223

* Mon Jun 29 2020 Phantom X <megaphantomx at hotmail dot com> - 0.222-1
- Mameinfo 0.222
- History 222
- Pugsy's Cheats 0.221

* Thu May 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.221-1
- Mameinfo 0.221
- History 221

* Sun Apr 12 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.220-1
- Mameinfo 0.220
- History 220

* Sun Mar 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.219-1
- Mameinfo 0.219
- History 219

* Mon Feb 03 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.218-1
- Mameinfo 0.218
- History 218

* Fri Jan 03 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.217-1
- Mameinfo 0.217
- History 217

* Mon Dec 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.216-1
- Mameinfo 0.216
- History 216

* Sun Nov 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.215-1
- Mameinfo 0.215

* Sun Sep 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.214-1
- Mameinfo 0.214

* Sat Sep 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.213-1
- Mameinfo 0.213
- History 212

* Thu Aug 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.212-1
- Mameinfo 0.212

* Fri Jun 28 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.211-1
- 0.211

* Tue Jun 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.210-1
- 0.210

* Thu Apr 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.209-1
- 0.209

* Fri Mar 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.208-1
- 0.208

* Sun Mar 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.207-1
- 0.207
- Pugsy's Cheats to 0.206

* Sat Feb 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.206-1
- 0.206

* Sun Dec 30 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.205-1
- Mameinfo 0.205

* Fri Nov 30 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.204-1
- 0.204

* Sat Nov 03 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.203-1
- 0.203
- Pugsy's Cheats to 0.200

* Fri Sep 28 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.202-1
- 0.202

* Sun Jul 29 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.200-1
- 0.200

* Mon Jul 02 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.199-1
- 0.199

* Fri Jun 01 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.198-1
- 0.198

* Fri Apr 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.197-1
- 0.197

* Sun Apr 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.196-1
- new version

* Sat Mar 10 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.195-1
- 0.195

* Wed Feb 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.194-1
- 0.194

* Mon Jan 01 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.193-1
- 0.193

* Mon Dec 04 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.192-1
- 0.192

* Sun Oct 29 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.191-1
- 0.191

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
