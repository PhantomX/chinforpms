%global pkgname JetBrainsMono
%global vc_url  https://github.com/JetBrains/%{pkgname}
%global vc_id   cd5227bd1f61dff3bbd6c814ceaf7ffd95e947d9

Version:        2.304
Release:        1%{?dist}

URL:            https://jetbrains.com/mono/

%global foundry           JetBrains
%global fontlicense       OFL-1.1
%global fontlicenses      OFL.txt
%global fontdocs          README.md

%global archivename %{pkgname}-%{version}

%global fontfamily        JetBrains Mono VF
%global fontsummary       A mono-space variable font family containing coding ligatures
%global fontpkgheader     %{expand:
Requires: jetbrains-mono-fonts
}
%global fonts             fonts/variable/JetBrainsMono[wght].ttf fonts/variable/%{pkgname}-Italic[wght].ttf 
%global fontappstreams    %{S:31}
%global fontdescription   %{expand:
The JetBrains Mono project publishes developer-oriented font families.

This package contains a variable font family.}

Source0:        %{vc_url}/releases/download/v%{version}/%{archivename}.zip

Source31:       %{fontpkgname}.metainfo.xml
Source32:       %{vc_url}/raw/%{vc_id}/README.md

%fontpkg


%prep
%autosetup -c -p1

cp -p %{S:32} .

%build

%install
%fontinstall

%check
%fontcheck

%fontfiles


%changelog
* Sat Nov 22 2025 Phantom X <megaphantomx at hotmail dot com> - 2.304-1
- Initial spec
