Name:           wxmp3val
Version:        4.0
Release:        1%{?dist}
Summary:        Free front-end for the MP3val

License:        GPLv3+
URL:            https://%{name}.sourceforge.io

Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.tar.gz


BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  wxGTK3-devel
Requires:       hicolor-icon-theme
Requires:       mp3val


%description
wxMP3val is a free front-end for the MP3val.


%prep
%autosetup -p1

sed -e 's/\r//' -i docs/*

sed \
  -e '/CMAKE_CXX_FLAGS/s| -s\b||' \
  -e '/share\/doc\//d' \
  -i CMakeLists.txt


%build
%cmake \
  -B %{__cmake_builddir} \
%{nil}

%cmake_build


%install
%cmake_install

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
