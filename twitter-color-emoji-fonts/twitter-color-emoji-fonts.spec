# Install fontconfig file
%bcond fontconf 0

Version:        15.1.0
Release:        1%{?dist}

URL:            https://github.com/13rac1/twemoji-color-font

%global pkgname TwitterColorEmoji-SVGinOT
%global priority 46
%global fontconfname twemoji-color

%global foundry           twitter
# Artwork: CC-BY-4.0
# Source Code: MIT
# Twitter Emoji for Everyone: CC-BY-4.0
# Power Symbol: MIT
%global fontlicense       CC-BY-4.0 AND MIT
%global fontlicenses      LICENSE*
%global fontdocs          README.md

%global archivename %{pkgname}-Linux-%{version}

%global fontfamily        Twitter Color Emoji
%global fontsummary       Twitter Unicode emoji color OpenType-SVG font
%if %{with fontconf}
%global fontpkgheader     %{expand:
Requires: bitstream-vera-fonts-all
}
%endif
%global fonts             %{pkgname}.ttf
%if %{with fontconf}
%global fontconfs         fontconfig/%{priority}-%{fontconfname}.conf
%endif
%global fontappstreams    %{S:31}
%global fontdescription   %{expand:
A color and B&W emoji SVG-in-OpenType font by Twitter with support for ZWJ, skin
tone modifiers and country flags.}

Source0:        https://github.com/13rac1/twemoji-color-font/releases/download/v%{version}/%{pkgname}-Linux-%{version}.tar.gz
Source31:       %{fontpkgname}.metainfo.xml

Patch0:         0001-fontconfig-fix-DTD.patch

%fontpkg


%prep
%autosetup -n %{archivename} -p1

%build

%install
%fontinstall

%check
%fontcheck

%fontfiles


%changelog
* Sat Jul 26 2025 Phantom X <megaphantomx at hotmail dot com> - 15.1.0-1
- Initial spec

