%undefine _hardened_build

%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%global commit 31fc1186ffbb
%global date 20221030
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}hg%{commit}
%endif

Name:           blastem
Version:        0.6.3
Release:        0.12%{?gver}%{?dist}
Summary:        Fast and accurate Sega Genesis/Mega Drive emulator

License:        GPLv3
URL:            https://www.retrodev.com/%{name}/
Source0:        https://www.retrodev.com/repos/%{name}/archive/%{commit}.tar.bz2#/%{name}-%{commit}.tar.bz2


BuildRequires:  icoutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(zlib)
Requires:       sdl_gamecontrollerdb
Requires:       dejavu-sans-fonts
Requires:       hicolor-icon-theme
Recommends:     %{name}-bindata >= %{version}


%description
BlastEm is an open source, higly accurate emulator for the Genesis/Megadrive
that runs on modest hardware.

TMMS support and menu.bin is not included.


%prep
%autosetup -n %{name}-%{commit} -p1

rm -rf zlib android

sed -e 's|"zlib/zlib.h"|<zlib.h>|g' -i blastem.c event_log.{c,h} png.c vgmplay.c zip.c

sed -e 's|./termhelper|%{_bindir}/%{name}-termhelper|g' -i terminal.c

sed \
  -e '/^CFLAGS:=$(OPT) $(CFLAGS)/d' \
  -e '/^LDFLAGS:=$(OPT) $(LDFLAGS)/d' \
  -e 's|^CFLAGS:=|CFLAGS+=|g' \
  -e 's|^LDFLAGS:=|LDFLAGS+=|g' \
  -e 's|$(OPT)|$(LDFLAGS)|g' \
  -e '/^CFLAGS+=/s| $(CFLAGS)||g' \
  -i Makefile

icotool -x icons/windows.ico


%build
%set_build_flags
%make_build \
  DATA_PATH=/usr/share/blastem \
  FONT_PATH=/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf \
  HOST_ZLIB=1


%install
mkdir -p %{buildroot}%{_bindir}
install -m0755 %{name} %{buildroot}%{_bindir}/

for i in dis zdis vgmplay termhelper ;do
  install -pm0755 $i %{buildroot}%{_bindir}/%{name}-$i
done

mkdir -p %{buildroot}%{_datadir}/%{name}/{images,shaders}
install -pm0644 rom.db default.cfg systems.cfg %{buildroot}%{_datadir}/%{name}/
install -pm0644 images/*.png %{buildroot}%{_datadir}/%{name}/images/
install -pm0644 shaders/*.glsl %{buildroot}%{_datadir}/%{name}/shaders/

ln -sf ../SDL_GameControllerDB/gamecontrollerdb.txt %{buildroot}%{_datadir}/%{name}/

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<'EOF'
[Desktop Entry]
Name=BlastEm
Comment=Genesis/MegaDrive emulator
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;Emulator;
EOF

for res in 16 32 48 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 windows_*_${res}x${res}x*.png \
    ${dir}/%{name}.png
done


%files
%license COPYING
%doc README
%{_bindir}/%{name}
%{_bindir}/%{name}-*
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png


%changelog
* Fri Jun 17 2022 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-0.10.20220611hg0bf077df45c3
- Bump

* Mon Apr 11 2022 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-0.9.20220407hg6f58af5bd6fa
- Bump

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-0.8.20220326hg9209858b2f74
- New snapshot
- Fix for package_note_file

* Mon Feb 14 2022 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-0.7.20220213hg0013362c320c
- Update

* Sun Jan 09 2022 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-0.6.20220101hg3748a2a8a4b7
- Bump

* Wed Oct 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-0.5.20210921hg460e14497120
- Update to proper branch
- Do not build vasm files (menu.bin and tmss.md moved to -bindata extra package)

* Sat Aug 14 2021 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-0.4.20210805git804954731e3f
- Bump

* Sat Mar 27 2021 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-0.3.20210309gita61b47d5489e
- Build menu.bin and tmss.md
- BR: xcftools vasm python3-pillow

* Wed Mar 24 2021 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-0.2.20210309gita61b47d5489e
- Update

* Fri Feb 19 2021 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-0.1.20210215git1e7a63f0ccf4
- 0.6.3-pre

* Sat Dec  5 2020 Phantom X <megaphantomx at hotmail dot com> - 0.6.2-11.20201203gitba5d206dcfea
- Bump

* Fri Nov 06 2020 Phantom X <megaphantomx at hotmail dot com> - 0.6.2-10.20201104git8a64d86cc362
- Update

* Sat Jul 25 2020 Phantom X <megaphantomx at hotmail dot com> - 0.6.2-9.20200719git4c418ee9a9d8
- Bump

* Sat Jun 20 2020 Phantom X <megaphantomx at hotmail dot com> - 0.6.2-8.20200618gite35b00626b3e
- New snapshot

* Mon May 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.6.2-7.20200516gita042e046f7f2
- Bump

* Wed Apr 29 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.6.2-6.20200426git357878be8be6
- New snapshot
- R: dejavu-sans-fonts

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.6.2-5.20200226git1ec6931d0a49
- gcc 10 fix

* Sun Mar 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.6.2-4.20200226git1ec6931d0a49
- New snapshot

* Wed Feb 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.6.2-3.20200216git5433252329fb
- Bump

* Sun Feb 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.6.2-2.20200109git59a83c21d9d2
- New snapshot

* Mon Nov 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.6.2-1.20191009git179a2ac29f27
- Initial spec
