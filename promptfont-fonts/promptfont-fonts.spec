%global pkgname promptfont
%global vc_url  https://codeberg.org/shinmera/%{pkgname}

Version:        1.12
Release:        1%{?dist}

URL:            https://shinmera.com/promptfont

%global foundry           PromptFont
%global fontlicense       OFL-1.1
%global fontlicenses      LICENSE.txt
%global fontdocs          README.md

%global archivename %{pkgname}-%{version}

%global fontfamily        PromptFont
%global fontsummary       A font for button prompts
%global fontpkgheader     %{expand:
Requires: jetbrains-mono-fonts
}
%global fonts             %{pkgname}.otf
%global fontappstreams    %{S:31}
%global fontdescription   %{expand:
The PromptFont is a font designed for button prompts in games.
It includes the base alphabet, as well as icons for
modifier and control keys, and gamepad buttons.}

Source0:        %{vc_url}/releases/download/v%{version}/%{pkgname}.zip#/%{archivename}.zip

Source31:       %{fontpkgname}.metainfo.xml

%fontpkg


%prep
%autosetup -c -p1

sed -e 's/\r//' -i LICENSE.txt

%build

%install
%fontinstall

%check
%fontcheck

%fontfiles


%changelog
* Sat Nov 22 2025 Phantom X <megaphantomx at hotmail dot com> - 1.12-1
- Initial spec
