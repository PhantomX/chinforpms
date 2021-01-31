%undefine _hardened_build

%global commit ba5d206dcfea
%global date 20201203
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{commit}
%endif

Name:           blastem
Version:        0.6.2
Release:        11%{?gver}%{?dist}
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


%description
BlastEm is an open source, higly accurate emulator for the Genesis/Megadrive that
runs on modest hardware.


%prep
%autosetup -n %{name}-%{commit} -p1

rm -rf zlib

sed -e 's|"zlib/zlib.h"|<zlib.h>|g' -i blastem.c event_log.{c,h} png.c zip.c

sed -e 's|./termhelper|%{_bindir}/%{name}-termhelper|g' -i terminal.c

BLASTEM_OPTFLAGS="%{build_cflags} -flto=%{_smp_build_ncpus} -fuse-linker-plugin"
sed \
  -e "/^OPT:=/s|-O2 -flto|$BLASTEM_OPTFLAGS|g" \
  -e 's|$(OPT) $(LDFLAGS)|\0 %{build_ldflags} -Wl,-z,relro -Wl,-z,now|g' \
  -e 's|$(CC)|\0 $(CFLAGS)|g' \
  -i Makefile

icotool -x icons/windows.ico


%build
%make_build \
  CC=gcc \
  DATA_PATH=%{_datadir}/%{name} \
  FONT_PATH=%{_datadir}/fonts/dejavu-sans-fonts/DejaVuSans.ttf \
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
