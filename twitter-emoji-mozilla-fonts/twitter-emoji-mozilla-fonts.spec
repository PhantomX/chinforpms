%global src_url https://github.com/PCSX2/pcsx2
%global src_id ed796ee3dbb3b873c4ab0af0c2b6a578cbf50288

Version:        17.0.2
Release:        1%{?dist}

URL:            https://github.com/mozilla/twemoji-colr

%global pkgname Twemoji.Mozilla
%global fontconfname twemoji-color

%global foundry           twitter
# Artwork: CC-BY-4.0
# Source Code: ASL-2.0
# Twitter Emoji for Everyone: CC-BY-4.0
%global fontlicense       CC-BY-4.0 AND ASL-2.0
%global fontlicenses      Twemoji.Mozilla-license

%global fontfamily        Twitter Emoji Mozilla
%global fontsummary       Twitter Unicode emoji COLRv0 font
%global fonts             %{pkgname}.ttf
%global fontdescription   %{expand:
A color and B&W emoji COLRv0 font by Mozilla with support for ZWJ, skin
tone modifiers and country flags.}

Source0:        %{src_url}/raw/%{src_id}/bin/resources/fonts/%{pkgname}.ttf#/%{pkgname}-%{version}.ttf
Source1:        %{src_url}/raw/%{src_id}/bin/resources/fonts/Twemoji.Mozilla-license
Source31:       %{fontpkgname}.metainfo.xml

%fontpkg


%prep
%autosetup -c -T
install -pm0644 %{S:0} %{pkgname}.ttf
install -pm0644 %{S:1} .


%build

%install
%fontinstall

%check
%fontcheck

%fontfiles


%changelog
* Mon Apr 20 2026 Phantom X <megaphantomx at hotmail dot com> - 17.0.2-1
- Initial spec

