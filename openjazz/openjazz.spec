%global commit af172ec9c7c0b4c5243bff5c24a800a7240c1c2d
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180219
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           openjazz
Version:        20171024
Release:        1%{?gver}%{?dist}
Summary:        A re-implemetantion of a known platform game engine

License:        GPLv2+
URL:            http://www.alister.eu/jazz/oj/
%if 0%{?with_snapshot}
Source0:        https://github.com/AlisterT/%{name}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/AlisterT/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif
Source1:        http://www.alister.eu/jazz/oj/ojlogo.png

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(libmodplug)
BuildRequires:  pkgconfig(sdl)
BuildRequires:  pkgconfig(zlib)
%if 0%{?with_snapshot}
BuildRequires:  autoconf
BuildRequires:  automake
%endif
Requires:       hicolor-icon-theme

%description
%{summary}.

%prep
%autosetup -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p0

sed -e 's|"/."|"/.local/share/%{name}/"|' -i src/main.cpp

cp -p %{S:1} .
convert \
  ojlogo.png -resize 96x96 \
  -background transparent -gravity center -extent 96x96 %{name}.png

cat > %{name}.wrapper <<'EOF'
#!/usr/bin/sh
set -e
mkdir -p ${HOME}/.local/share/%{name}
cd ${HOME}/.local/share/%{name}
exec %{_bindir}/%{name}.bin "$@"
EOF

%if 0%{?with_snapshot}
autoreconf -ivf
%endif

%build
export CPPFLAGS="-DDATAPATH=\\\"%{_datadir}/%{name}/\\\" -DHOMEDIR"
%configure \
  --disable-silent-rules
%make_build


%install
%make_install

mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_bindir}/%{name}.bin
install -pm0755 %{name}.wrapper %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=OpenJazz
Comment=Platform game engine
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;ActionGame;
EOF

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/96x96/apps
install -pm0644 %{name}.png %{buildroot}%{_datadir}/icons/hicolor/96x96/apps/

for res in 16 22 24 32 48 64 72 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert %{name}.png -filter Lanczos -resize ${res}x${res}  \
    ${dir}/%{name}.png
done

%files
%license gpl.txt licenses.txt
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}.bin
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/%{name}/%{name}.000

%changelog
* Mon Mar 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 20171024-1.20180219gitaf172ec
- Initial spec
