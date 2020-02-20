%undefine _hardened_build

%global commit 5433252329fb
%global date 20200216
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{commit}
%endif

Name:           blastem
Version:        0.6.2
Release:        3%{?gver}%{?dist}
Summary:        Fast and accurate Sega Genesis/Mega Drive emulator

License:        GPLv3
URL:            https://www.retrodev.com/%{name}/
Source0:        https://www.retrodev.com/repos/%{name}/archive/%{commit}.tar.bz2#/%{name}-%{commit}.tar.bz2

BuildRequires:  icoutils
BuildRequires:  gcc
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(zlib)
Requires:       sdl_gamecontrollerdb
Requires:       hicolor-icon-theme


%description
BlastEm is an open source, higly accurate emulator for the Genesis/Megadrive that
runs on modest hardware.


%prep
%autosetup -n %{name}-%{commit} -p1

rm -rf zlib

sed -e 's|"zlib/zlib.h"|<zlib.h>|g' -i blastem.c png.c zip.c

sed -e 's|./termhelper|%{_bindir}/%{name}-termhelper|g' -i terminal.c

BLASTEM_OPTFLAGS="%(echo %{build_cflags} | sed -e 's/-O2\b/-O3/') -flto=%{_smp_build_ncpus} -fuse-linker-plugin"
sed \
  -e "/^OPT:=/s|-O2 -flto|$BLASTEM_OPTFLAGS|g" \
  -e 's|$(OPT) $(LDFLAGS)|\0 %{build_ldflags}|g' \
  -e 's|$(CC)|\0 $(CFLAGS)|g' \
  -i Makefile

icotool -x icons/windows.ico


%build
%make_build CC=gcc DATA_PATH=%{_datadir}/%{name} HOST_ZLIB=1


%install
mkdir -p %{buildroot}%{_bindir}
install -m0755 %{name} %{buildroot}%{_bindir}/

for i in dis zdis stateview vgmplay termhelper ;do
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
* Wed Feb 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.6.2-3.20200216git5433252329fb
- Bump

* Sun Feb 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.6.2-2.20200109git59a83c21d9d2
- New snapshot

* Mon Nov 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.6.2-1.20191009git179a2ac29f27
- Initial spec
