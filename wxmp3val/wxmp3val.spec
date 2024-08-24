%global commit 3992f7e93e11ea5417d7a2847cec5b3b3ef49ba7
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230401
%bcond_with snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           wxmp3val
Version:        4.2
Release:        1%{?dist}
Summary:        Free front-end for the MP3val

License:        GPL-3.0-or-later
URL:            https://github.com/cfgnunes/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif


BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  wxGTK-devel >= 3.2
Requires:       hicolor-icon-theme
Requires:       mp3val


%description
wxMP3val is a free front-end for the MP3val.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

sed -e 's/\r//' -i doc/*.md doc/COPYING
mv doc/README.{md,disabled}

sed \
  -e '/CMAKE_CXX_FLAGS/s| -s\b||' \
  -e '/CMAKE_DOC_DIR/d' \
  -i CMakeLists.txt

sed -e 's|/usr/share/|%{_datadir}/|g' -i src/Constants.hpp*


%build
%cmake \
%{nil}

%cmake_build


%install
%cmake_install

desktop-file-edit \
  --remove-key="Encoding" \
  %{buildroot}%{_datadir}/applications/%{name}.desktop


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license doc/COPYING
%doc README.md doc/*.{md,png}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/%{name}/


%changelog
* Thu Aug 22 2024 Phantom X <megaphantomx at hotmail dot com> - 4.2-1
- 4.2

* Thu May 18 2023 Phantom X <megaphantomx at hotmail dot com> - 4.1-0.1.20230401git3992f7e
- Snapshot
- wxGTK 3.2
- Update URLs

* Fri Aug 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 4.0-1
- Initial spec.
