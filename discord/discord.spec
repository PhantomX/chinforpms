%global debug_package %{nil}
%global __strip /bin/true

%global use_canary 0

%if 0%{?use_canary}
%global execname DiscordCanary
%else
%global execname Discord
%endif

Name:           discord
Version:        0.0.2
Release:        2%{?dist}
Epoch:          1
Summary:        Voice and text chat messenger

License:        Proprietary
URL:            https://discordapp.com/
%if 0%{?use_canary}
Source0:        https://discordapp.com/api/download/canary?platform=linux&format=tar.gz#/%{name}-canary-%{version}.tar.gz
%else
Source0:        https://discordapp.com/api/download?platform=linux&format=tar.gz#/%{name}-%{version}.tar.gz
%endif

ExclusiveArch:  x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
Requires:       libcxx%{?_isa}
Requires:       libXScrnSaver%{?_isa}
Requires:       hicolor-icon-theme

%if 0%{?use_canary}
Provides:       %{name}-canary = %{version}-%{release}
Conflicts:      %{name}-canary < %{version}
Conflicts:      %{name} < %{version}
%endif

%global __provides_exclude_from ^%{_libdir}/%{name}/.*


%global __requires_exclude ^libffmpeg.so
%global __requires_exclude %__requires_exclude|^libnode.so

%description
All-in-one voice and text chat for gamers that’s free, secure, and works on
both your desktop and phone.

%prep
%autosetup -n %{execname}

chmod +x *.so

chrpath --delete %{execname}

mv %{name}-canary.desktop %{name}.desktop ||:

%build


%install

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<'EOF'
#!/usr/bin/sh
LD_LIBRARY_PATH="%{_libdir}/%{name}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec %{_libdir}/%{name}/%{execname} "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_libdir}/%{name}
cp -rp %{execname} *.bin *.dat *.pak *.so locales resources \
  %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-name="Discord" \
  --set-icon="%{name}" \
  --set-key="Exec" \
  --set-value="%{name}" \
  %{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
install -pm0644 %{name}.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/

for res in 16 22 24 32 48 64 72 96 128 192 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert %{name}.png -filter Lanczos -resize ${res}x${res}  \
    ${dir}/%{name}.png
done

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png


%changelog
* Thu Sep 14 2017 Phantom X <megaphantomx at bol dot com dot br> - 1:0.0.2-2
- Exclude provides

* Thu Aug 24 2017 Phantom X <megaphantomx at bol dot com dot br> - 1:0.0.2-1
- 0.0.2

* Tue Feb 07 2017 Phantom X <megaphantomx at bol dot com dot br> - 1:0.0.1-1
- 0.0.1, not canary

* Thu Jan 26 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.0.15-1
- 0.0.15

* Sun Jan  8 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.1.13-1
- Initial spec
