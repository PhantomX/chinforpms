# --with glinject to build only the inject library (for multilib build speedup)
%ifarch %{ix86}
%if 0%{?fedora} > 30
%global with_glinject_only 1
%endif
%endif

%define shortname ssr
Name:           simplescreenrecorder
Version:        0.3.11
Release:        9%{?dist}
Summary:        Simple Screen Recorder is a screen recorder for Linux

License:        GPLv3
URL:            http://www.maartenbaert.be/simplescreenrecorder/
Source0:        https://github.com/MaartenBaert/ssr/archive/%{version}/%{shortname}-%{version}.tar.gz
Patch0:         0001-Fix-libssr-glinject.so-preload-path.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake3
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(xfixes)
%if !0%{?with_glinject_only}
BuildRequires:  desktop-file-utils
BuildRequires:  ffmpeg-devel
BuildRequires:  pkgconfig(Qt5) >= 5.7.0
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(xi)
BuildRequires:  qt5-linguist
BuildRequires:  libappstream-glib

Requires:       hicolor-icon-theme
%endif
Obsoletes:      %{name}-libs < %{version}

#https://github.com/MaartenBaert/ssr/issues/533
ExcludeArch:    %{power64}

%description
It is a screen recorder for Linux.
Despite the name, this program is actually quite complex.
It's 'simple' in the sense that it's easier to use than ffmpeg/avconv or VLC

%prep
%autosetup -p1 -n %{shortname}-%{version}
# https://github.com/MaartenBaert/ssr/issues/694
sed -i 's|lrelease|lrelease-qt5|' src/translations/CMakeLists.txt


%build
%cmake3 \
  -B %{__cmake_builddir} \
    -DCMAKE_BUILD_TYPE=Release \
    -DWITH_QT5=TRUE \
%ifnarch %{ix86} x86_64
    -DENABLE_X86_ASM=FALSE \
%endif
%ifarch %{arm} aarch64
    -DWITH_GLINJECT=FALSE \
%endif
%if 0%{?with_glinject_only}
    -DWITH_SIMPLESCREENRECORDER:BOOL=FALSE \
%endif
%{nil}

%cmake_build


%install
%cmake_install

rm -f %{buildroot}%{_libdir}/*.la
mkdir -p %{buildroot}%{_libdir}/%{name}
%ifnarch %{arm} aarch64
    mv %{buildroot}%{_libdir}/lib%{shortname}-glinject.so %{buildroot}%{_libdir}/%{name}/lib%{shortname}-glinject.so
%endif

%check
%if !0%{?with_glinject_only}
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/*.appdata.xml
%endif


%files
%doc README.md AUTHORS.md CHANGELOG.md notes.txt todo.txt
%license COPYING
%if !0%{?with_glinject_only}
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}*
%{_bindir}/%{shortname}-glinject
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man1/%{shortname}-glinject.1.*
%{_datadir}/appdata/%{name}.appdata.xml
%endif
%{_libdir}/%{name}


%changelog
* Thu Mar 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.3.11-9
- Rebuilt

* Wed Oct 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.3.11-8
- Fixes for multilib, do not bump

* Wed Aug 07 2019 Leigh Scott <leigh123linux@gmail.com> - 0.3.11-8
- Rebuild for new ffmpeg version

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Feb 21 2019 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.11-6
- Enable translations

* Mon Feb 04 2019 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.11-5
- Added preload patch

* Wed Nov 14 2018 Antonio Trande <sagitter@fedoraproject.org> - 0.3.11-4
- Rebuild for ffmpeg-3.4.5 on el7

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.3.11-3
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 13 2018 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.11-1
- Update to 0.3.11

* Tue Mar 13 2018 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.10-1
- Update to 0.3.10

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.3.9-5
- Rebuilt for new ffmpeg snapshot

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.3.9-3
- Rebuilt for ffmpeg-3.5 git

* Wed Dec 13 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.3.9-2
- Use build requires cmake3 instead of cmake

* Wed Dec 13 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.9-1
- Update to 0.3.9
- Switch to use cmake for build

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.3.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.3.8-4
- Rebuild for ffmpeg update

* Mon Apr 17 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.8-3
- Exclude power64 arches from build

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 08 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.8-1
- Update to 0.3.8

* Tue Oct 18 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.7-1
- Update to 0.3.7

* Wed Oct 12 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.6-7
- Switch to use Qt5

* Wed Sep 21 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.6-6
- Add obsoletes

* Tue Sep 20 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.6-5
- Remove libs subpackage

* Fri Aug 26 2016 Vasiliy N. Glazov <vascom2@gmail.com> - 0.3.6-4
- Clean spec

* Tue Jun 14 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.3.6-3.R
- rebuilt against new ffmpeg

* Sun Nov  8 2015 Ivan Epifanov <isage.dna@gmail.com> - 0.3.6-2.R
- Update icon cache

* Wed Nov  4 2015 Ivan Epifanov <isage.dna@gmail.com> - 0.3.6-1.R
- Update to 0.3.6

* Mon Mar 23 2015 Ivan Epifanov <isage.dna@gmail.com> - 0.3.3-1.R
- Update to 0.3.3

* Tue Dec 16 2014 Ivan Epifanov <isage.dna@gmail.com> - 0.3.1-1.R
- Update to 0.3.1

* Thu Jul  3 2014 Ivan Epifanov <isage.dna@gmail.com> - 0.3.0-2.R
- Move gl-inject library to subdir

* Thu Jul  3 2014 Ivan Epifanov <isage.dna@gmail.com> - 0.3.0-1.R
- Initial spec for fedora
