%global commit 7011a97f7071282fccaee58ba1c4eb7d166150fb
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180510
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pname   Cows-Revenge

Name:           cowsrevenge
Version:        1.0.2
Release:        1%{?gver}%{?dist}
Summary:        Indie Platformer Pixel Art Game

License:        GPLv3 and CC-BY-ND-SA
URL:            https://pipoypipagames.itch.io/cows-revenge
%if 0%{?with_snapshot}
Source0:        https://github.com/Dariasteam/%{pname}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/Dariasteam/%{pname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

# Fix joystick buttons to match Xbox360
Patch0:         %{name}-xbox360.patch

BuildArch:      noarch

BuildRequires:  desktop-file-utils
Requires:       godot2-runner >= 2.1.5
Requires:       hicolor-icon-theme


%description
You are a cow abducted and genetically improved by aliens which now have the
opportunity to rebel against livestock industry by freeing the encaged hens and
killing butchers. You used to be a regular cow raised as a dairy cow, but you
ain't that anymore. You have become better. You are... THE COWEST.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{pname}-%{commit} -p1
%else
%autosetup -n %{pname}-%{version} -p1
%endif

%build


%install
mkdir -p %{buildroot}%{_datadir}/%{name}

for dir in Fonts Locales Misc Music Scenes Sound Sprites ;do
  cp -rp ${dir} %{buildroot}%{_datadir}/%{name}/
done

install -pm0644 engine.cfg *.png *.tscn %{buildroot}%{_datadir}/%{name}/

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<'EOF'
#!/bin/sh
exec %{_bindir}/godot2-runner -path %{_datadir}/%{name} "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install --mode 0644 \
  --dir %{buildroot}%{_datadir}/applications \
  --add-category="ActionGame" \
  linux_build/com.github.dariasteam.%{name}.desktop

for res in 64 128 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 linux_build/%{name}_icon_${res}.png \
    ${dir}/com.github.dariasteam.%{name}.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 linux_build/*.appdata.xml %{buildroot}%{_metainfodir}/


%files
%license LICENSE_*
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_metainfodir}/*.xml


%changelog
* Fri May 25 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.0.2-1.20180510git7011a97
- Initial spec
