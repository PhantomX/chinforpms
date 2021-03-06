%global debug_package %{nil}
%global __strip /bin/true

%global binname Telegram
%global gitlink https://github.com/telegramdesktop/tdesktop
%global gitrawlink %{gitlink}/raw/master
%global use_prerel 0

%ifarch %{ix86}
%global parch 32
%endif

%if 0%{?use_prerel}
%global prerel .alpha
%endif

Name:           telegram
Version:        1.1.7
Release:        1%{?dist}
Summary:        A messenger application

License:        GPLv3
URL:            https://telegram.org/
#Source0:        https://updates.tdesktop.com/tlinux%{?parch}/tsetup%{?parch}.%{version}.tar.xz
Source0:        %{gitlink}/releases/download/v%{version}/tsetup%{?parch}.%{version}%{?prerel}.tar.xz
Source1:        %{gitrawlink}/LICENSE
Source2:        %{gitrawlink}/%{binname}/Resources/art/icon32.png
Source3:        %{gitrawlink}/%{binname}/Resources/art/icon48.png
Source4:        %{gitrawlink}/%{binname}/Resources/art/icon64.png
Source5:        %{gitrawlink}/%{binname}/Resources/art/icon256.png
Source6:        %{gitrawlink}/%{binname}/Resources/art/icon512.png
Source7:        %{gitrawlink}/%{binname}/Resources/art/icon_green.png
Source8:        tg.protocol
Source9:        %{name}.xml

BuildRequires:  chrpath
BuildRequires:  ImageMagick
BuildRequires:  kf5-filesystem
Requires:       dbus
Requires:       hicolor-icon-theme
Requires(post): desktop-file-utils shared-mime-info
Requires(postun): desktop-file-utils gtk-update-icon-cache shared-mime-info
Requires(posttrans): gtk-update-icon-cache shared-mime-info

Provides:       %{binname} = %{version}
Provides:       %{binname}Desktop = %{version}

%description
Telegram is a messaging app with a focus on speed and security, it’s super-fast,
simple and free. You can use Telegram on all your devices at the same time — your
messages sync seamlessly across any number of your phones, tablets or computers.

%prep
%autosetup -n %{binname}

cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} .

chrpath --delete %{binname}

cat> %{binname}.wrapper <<'EOF'
#!/usr/bin/bash
set -e

TGDESKFILE1="${HOME}/.local/share/applications/%{name}desktop.desktop"
TGICON1="${HOME}/.local/share/icons/%{name}.png"
TGDIR="${HOME}/.local/share/%{binname}Desktop"
TGDESKFILE2="${TGDIR}/tdata/%{name}desktop.desktop"

mkdir -p "${TGDIR}"

if [[ -d "${HOME}/.TelegramDesktop" ]] && [[ ! -e "${TGDIR}/tdata/settings1" ]];then
  echo "Moving ${HOME}/.TelegramDesktop to ${TGDIR}..."
  mv "${HOME}/.TelegramDesktop"/* "${TGDIR}"/
  rmdir "${HOME}/.TelegramDesktop"
fi

# Remove unneeded user files
[[ -e "${TGDESKFILE1}" ]] && rm -fv "${TGDESKFILE1}"
[[ -w "${TGDESKFILE2}" ]] && rm -fv "${TGDESKFILE2}"
[[ -w "${TGICON1}" ]] && rm -fv "${TGICON1}"
[[ -w "${TGDIR}"/tupdates ]] && rm -rfv "${TGDIR}"/tupdates
[[ -e "${TGDIR}"/Telegram ]] && rm -fv "${TGDIR}"/Telegram
[[ -e "${TGDIR}"/Updater ]] && rm -fv "${TGDIR}"/Updater

# Fake desktop file
[[ ! -e "${TGDESKFILE2}" ]] && touch "${TGDESKFILE2}"
chmod 0444 "${TGDESKFILE2}"

[[ ! -e "${TGDIR}"/tupdates ]] && mkdir -p "${TGDIR}"/tupdates
chmod 0555 "${TGDIR}"/tupdates

unset TGDESKFILE1
unset TGDESKFILE2
unset TGICON1
unset TGDIR

exec %{binname}.bin "${@}"
EOF

%build


%install

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{binname} %{buildroot}%{_bindir}/%{binname}.bin
install -pm0755 %{binname}.wrapper %{buildroot}%{_bindir}/%{binname}

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/telegramdesktop.desktop <<EOF
[Desktop Entry]
Name=%{binname} Desktop
Comment=Official desktop version of %{binname} messaging app
Exec=%{binname}
Icon=%{name}
Terminal=false
StartupWMClass=%{binname}Desktop
Type=Application
Categories=Qt;Network;InstantMessaging;
MimeType=application/x-xdg-protocol-tg;x-scheme-handler/tg;application/x-tdesktop-theme;
EOF

desktop-file-validate %{buildroot}%{_datadir}/applications/telegramdesktop.desktop

for res in 32 48 64 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 icon${res}.png ${dir}/%{name}.png
done

for res in 16 22 24 48 72 96 128 192 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert icon512.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done

for res in 16 22 24 32 36 48 64 72 96 128 192 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/mimetypes
  mkdir -p ${dir}
  convert icon_green.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}-tdesktop-theme.png
done

mkdir -p %{buildroot}%{_datadir}/kservices5
install -pm0644 %{SOURCE8} %{buildroot}%{_datadir}/kservices5/tg.protocol

mkdir -p %{buildroot}%{_datadir}/mime/packages
install -pm0644 %{SOURCE9} %{buildroot}%{_datadir}/mime/packages/


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &>/dev/null || :
update-desktop-database &>/dev/null ||:
 
%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
  touch --no-create %{_datadir}/mime/packages &>/dev/null || :
  update-mime-database %{_datadir}/mime &>/dev/null || :
fi
update-desktop-database &>/dev/null ||:

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &>/dev/null || :

%files
%license LICENSE
%{_bindir}/%{binname}
%{_bindir}/%{binname}.bin
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/kservices5/*.protocol
%{_datadir}/mime/packages/%{name}.xml

%changelog
* Thu Jun 01 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.1.7-1
- 1.1.7

* Tue May 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.1.2-1
- 1.1.2

* Wed May 17 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.1.0-1
- new version

* Wed Apr 05 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.29-1
- 1.0.28

* Fri Mar 31 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.27-1
- 1.0.27
- StartupWMClass fix
- Theme mimetype and icon

* Tue Feb 21 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.14-1
- 1.0.14
- Update wrapper to move old configuration directory
- Update wrapper to stop desktop file installation in HOME dir
- Update wrapper to stop downloading of application updates
- Add KF5 service protocol

* Tue Jan 31 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.5-1
- 1.0.5
- P: %%{binname} and %%{binname}Desktop
- Add wrapper with dirty HOME dir cleanup

* Fri Jan 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.2-2
- Fix desktop file

* Thu Jan 19 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.2-1
- new version

* Thu Jan 12 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.0-1
- new version

* Thu Jan 12 2017 Phantom X <megaphantomx at bol dot com dot br>
- new version

* Mon Jan  9 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.10.20-1
- Initial spec.
