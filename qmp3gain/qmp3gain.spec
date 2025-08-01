%global commit ecf61ec0e13023c22e8e277311486ec4e6e72b28
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240427
%bcond snapshot 1

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           qmp3gain
Version:        0.9.4
Release:        0.1%{?dist}
Summary:        MP3Gain GUI front end

License:        GPL-3.0-only
URL:            http://sourceforge.net/projects/qmp3gain/

%if %{with snapshot}
# To regenerate a snapshot:
# Use your regular webbrowser to open https://sourceforge.net/p/qmp3gain/code/ci/%%{commit}/tarball

# This triggers the SourceForge instructure to generate a snapshot
# After that you can pull in the archive with:
# spectool -g qmp3gain.spec
Source0:        https://sourceforge.net/code-snapshots/git/q/qm/%{name}/code.git/%{name}-code-%{commit}.zip#/%{name}-%{shortcommit}.zip
%else
Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
%endif


BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Help)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  qt5-linguist
# For qhelpgenerator
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
Requires:       mp3gain


%description
Graphical user interface front end supporting MP3Gain engine which analyzes and
losslessly adjusts mp3 files to a specified target volume.

%prep
%autosetup %{?with_snapshot:-n %{name}-code-%{commit}}%{!?with_snapshot:-c} -p1

sed \
  -e 's/^QHPQCH.commands =/\0 xvfb-run/g' \
  -e 's/^QHCPQHC.commands =/\0 xvfb-run/g' \
  -i help/help.pro


%build
%qmake_qt5 %{name}.pro


# Fix build error
%make_build || %make_build 


%install
make install INSTALL_ROOT=%{buildroot}

desktop-file-edit \
  --remove-category="Application" \
  --add-mime-type="audio/mpeg" \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name} --with-qt


%files -f %{name}.lang
%doc README.md
%license LICENSE.txt
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/help/
%{_datadir}/%{name}/resources/


%changelog
* Sun Oct 20 2024 Phantom X <megaphantomx at hotmail dot com> - 0.9.4-0.1.20240427gitecf61ec
- 0.9.4 release candidate

* Tue Sep 13 2022 Phantom X <megaphantomx at hotmail dot com> - 0.9.3-0.2.2020727git499c2b1
- Bump

* Mon Jul 11 2022 Phantom X <megaphantomx at bol dot com dot br> - 0.9.3-0.1.20120321git9ba4b11
- Return to official

* Tue Apr 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.9.0-3.20180213git05fa4cf
- Change to Luigi Baldoni Qt5 port snapshot

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.0-2
- BR: desktop-file-utils

* Thu Jan  5 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.0-1
- Initial spec.
