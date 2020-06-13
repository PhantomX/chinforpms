Name:           wxmp3gain
Version:        4.0
Release:        1%{?dist}
Summary:        Free front-end for the MP3gain

License:        GPLv3+
URL:            https://%{name}.sourceforge.io

Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.tar.gz


BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  wxGTK3-devel
Requires:       hicolor-icon-theme
Requires:       mp3gain


%description
wxMP3gain is a free front-end for the MP3gain.


%prep
%autosetup -p1

sed -e 's/\r//' -i docs/*

sed \
  -e '/CMAKE_CXX_FLAGS/s| -s\b||' \
  -e '/share\/doc\//d' \
  -i CMakeLists.txt


%build
%cmake . -B %{_target_platform} \
%{nil}

%make_build -C %{_target_platform}


%install
%make_install -C %{_target_platform}

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license docs/COPYING
%doc README.md docs/{AUTHORS,CHANGELOG,TODO}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/%{name}/


%changelog
* Fri Aug 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.0-1
- Initial spec.
