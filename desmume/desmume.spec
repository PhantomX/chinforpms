%global commit 0dab5917b689bcbe18b07af3b4ac5105b50c9345
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190116
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global vc_url  https://github.com/TASVideos/%{name}

Name:           desmume
Version:        0.9.12
Release:        0.5%{?gver}%{?dist}
Summary:        A Nintendo DS emulator

Epoch:          1

License:        GPLv2+
URL:            http://desmume.org/
%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
%endif #{?with_snapshot}

# Do not look into builddir
Patch0:         %{name}-dontlookinbuilddir.patch
# Use system tinyxml instead of the embedded copy
Patch1:         %{name}-tinyxml.patch
Patch2:         %{name}-format-security.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(gtkglext-1.0)
BuildRequires:  pkgconfig(libglade-2.0)
BuildRequires:  pkgconfig(lua)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(sdl)
BuildRequires:  pkgconfig(soundtouch) >= 1.5.0
BuildRequires:  pkgconfig(zziplib)
BuildRequires:  libpcap-devel
BuildRequires:  tinyxml-devel
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme


%package glade
Summary:        A Nintendo DS emulator (Glade GUI version)

%package cli
Summary:        A Nintendo DS emulator (CLI version)


%description
DeSmuME is a Nintendo DS emulator running homebrew demos and commercial games.

%description glade
DeSmuME is a Nintendo DS emulator running homebrew demos and commercial games.

This is the GTK/Glade version.

%description cli
DeSmuME is a Nintendo DS emulator running homebrew demos and commercial games.

This is the CLI version.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

mkdir docs

pushd %{name}

# Remove bundled tinyxml
rm -rf src/utils/tinyxml

# Fix end-of-line encoding
sed -i 's/\r//' AUTHORS

# Fix file encoding
for txtfile in ChangeLog AUTHORS
do
  iconv --from=ISO-8859-1 --to=UTF-8 $txtfile > tmp
  touch -r $txtfile tmp
  mv tmp $txtfile
done

cp -p AUTHORS ChangeLog README README.LIN ../docs/

# Fix premissions
chmod 644 COPYING README README.LIN

# Fix glade path
sed -i 's|gladedir = $(datadir)/desmume/glade|gladedir = $(datadir)/%{name}-glade/|g' src/frontend/posix/gtk-glade/Makefile.am

# We need a different icon for desmume-glade
sed -i 's|Icon=DeSmuME|Icon=DeSmuME-glade|g' src/frontend/posix/gtk-glade/%{name}-glade.desktop

# Fix gettext package name
sed -i 's|GETTEXT_PACKAGE=desmume|GETTEXT_PACKAGE=desmume-glade|g' src/frontend/posix/configure.ac

%if 0%{?with_snapshot}
sed -i 's|\$REVISION|%{shortcommit}|g' src/frontend/posix/configure.ac
sed -i \
  -e '/SVN_REV_STR/s|"0"|"%{shortcommit}"|g' \
  src/version.cpp
%endif

pushd src/frontend/posix
autoreconf -ivf
popd

%build
pushd %{name}/src/frontend/posix
%configure \
  --disable-silent-rules \
  --enable-glx \
  --enable-openal \
  --enable-glade \
  --enable-wifi

%make_build

popd

%install
%make_install -C %{name}/src/frontend/posix UPDATEDESKTOP=/usr/bin/true

# Rename desktop files and fix categories
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-edit \
  --remove-key Version \
  --remove-category GNOME \
  --remove-category GTK \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-edit \
  --remove-key Version \
  --remove-category GNOME \
  --remove-category GTK \
  %{buildroot}%{_datadir}/applications/%{name}-glade.desktop

# Remove installed icon
rm -rf %{buildroot}%{_datadir}/pixmaps

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/64x64/apps
install -pm0644 "%{name}/src/frontend/cocoa/images/Icon_DeSmuME_32x32@2x.png" \
  %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/DeSmuME.png
install -pm0644 "%{name}/src/frontend/cocoa/images/Icon_DeSmuME_32x32@2x.png" \
  %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/DeSmuME-glade.png

for res in 16 22 24 32 36 48 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert "%{name}/src/frontend/cocoa/images/Icon_DeSmuME_32x32@2x.png" \
    -filter Lanczos -resize ${res}x${res} ${dir}/DeSmuME.png
  cp -p ${dir}/DeSmuME.png ${dir}/DeSmuME-glade.png
done


%files
%doc docs/*
%license %{name}/COPYING
%{_bindir}/%{name}
%{_datadir}/icons/hicolor/*/apps/DeSmuME.png
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/%{name}.1*


%files glade
%doc docs/*
%license %{name}/COPYING
%{_bindir}/%{name}-glade
%{_datadir}/%{name}-glade
%{_datadir}/icons/hicolor/*/apps/DeSmuME-glade.png
%{_datadir}/applications/%{name}-glade.desktop
%{_mandir}/man1/%{name}-glade.1*


%files cli
%doc docs/*
%license %{name}/COPYING
%{_bindir}/%{name}-cli
%{_mandir}/man1/%{name}-cli.1*


%changelog
* Thu Jan 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.9.12-0.5.20190116git0dab591
- New snapshot

* Wed Jan 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.9.12-0.4.20190102git21a3fae
- New snapshot

* Sun Dec 23 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.9.12-0.3.20181222git022cf3c
- New snapshot

* Wed Dec 05 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.9.12-0.2.20181205git35e834f
- New snapshot

* Sat Nov 10 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.9.12-0.1.20181108git5d85ac2.chinfo
- chinforpms cleanup
- Build from snapshot

* Wed Feb 28 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.9.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct 08 2017 Sérgio Basto <sergio@serjux.com> - 0.9.11-6
- Rebuild for soundtouch 2.0.0

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.9.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 19 2017 Andrea Musuruane <musuruan@gmail.com> - 0.9.11-4
- Fixed FTBFS
- Added soundtouch-devel and libpcap-devel to BR

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.9.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 28 2016 Leigh Scott <leigh123linux@googlemail.com> - 0.9.11-2
- fix gcc6 compile issue
- quick spec file clean up

* Thu May 14 2015 Andrea Musuruane <musuruan@gmail.com> - 0.9.11-1
- Updated to upstream version 0.9.11
- Spec file cleanup

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Dec 01 2013 Andrea Musuruane <musuruan@gmail.com> - 0.9.10-1
- Updated to upstream version 0.9.10
- Added a patch to use system tinyxml
- Built with compat-lua for F20+
- Dropped cleaning at the beginning of %%install
- Updated desktop database because desmume desktop entry has MimeType key

* Wed May 01 2013 Andrea Musuruane <musuruan@gmail.com> - 0.9.9-1
- Updated to upstream version 0.9.9
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- Dropped desktop vendor tag for F19+

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.9.8-2
- Mass rebuilt for Fedora 19 Features

* Thu Apr 26 2012 Andrea Musuruane <musuruan@gmail.com> 0.9.8-1
- Updated to upstream version 0.9.8

* Sun Apr 15 2012 Andrea Musuruane <musuruan@gmail.com> 0.9.7-5
- Fixed microphone support (BZ #2231)
- Enabled LUA engine

* Sat Mar 17 2012 Andrea Musuruane <musuruan@gmail.com> 0.9.7-4
- Fixed FTBFS for F17+

* Sat Mar 17 2012 Andrea Musuruane <musuruan@gmail.com> 0.9.7-3
- Fixed an error in desmume-glade.desktop (BZ #2229)

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.9.7-2
- Rebuilt for c++ ABI breakage

* Sun Feb 06 2011 Andrea Musuruane <musuruan@gmail.com> 0.9.7-1
- Updated to upstream version 0.9.7

* Sun Jun 06 2010 Andrea Musuruane <musuruan@gmail.com> 0.9.6-1
- Updated to upstream version 0.9.6-1
- Fixed Source0 URL

* Sun Dec 06 2009 Andrea Musuruane <musuruan@gmail.com> 0.9.5-2
- Added a patch from upstream to compile on big endian systems (SF #2909694)

* Sun Dec 06 2009 Andrea Musuruane <musuruan@gmail.com> 0.9.5-1
- Updated to upstream version 0.9.5
- Updated icon cache scriptlets

* Fri Jul 24 2009 Andrea Musuruane <musuruan@gmail.com> 0.9.4-1
- Updated to upstream version 0.9.4
- Added a fix to compile under gcc 4.4 (SF #2819176)
- Removed no longer needed patches
- Removed no longer needed Debian man pages
- Cosmetic changes

* Thu Apr 30 2009 Andrea Musuruane <musuruan@gmail.com> 0.9.2-2
- Added a patch from upstream to fix IO Regs menu crash (SF #2781065)

* Sun Apr 19 2009 Andrea Musuruane <musuruan@gmail.com> 0.9.2-1
- Updated to upstream version 0.9.2
- Removed no longer needed patch to compile with gcc 4.4
- Added a patch from upstream to compile on 64 bit systems (SF #2755952)

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.9.1-3
- rebuild for new F11 features

* Sat Feb 14 2009 Andrea Musuruane <musuruan@gmail.com> 0.9.1-2
- Made a patch to compile with gcc 4.4 (SF #2599049)

* Fri Feb 13 2009 Andrea Musuruane <musuruan@gmail.com> 0.9.1-1
- Updated to upstream version 0.9.1

* Sun Jan 04 2009 Andrea Musuruane <musuruan@gmail.com> 0.9-1
- Updated to upstream version 0.9

* Wed Jul 30 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.8-2
- rebuild for buildsys cflags issue

* Wed Apr 23 2008 Andrea Musuruane <musuruan@gmail.com> 0.8-1
- Updated to upstream version 0.8

* Sat Sep 08 2007 Andrea Musuruane <musuruan@gmail.com> 0.7.3-4
- Using debian sources because many things were missing from upstream
- Removed no longer needed automake and autoconf from BR
- Updated icon cache scriptlets to be compliant to new guidelines

* Tue Aug 21 2007 Andrea Musuruane <musuruan@gmail.com> 0.7.3-3
- Added missing automake libtool to BR

* Mon Aug 20 2007 Andrea Musuruane <musuruan@gmail.com> 0.7.3-2
- Added missing autoconf to BR

* Sat Aug 18 2007 Andrea Musuruane <musuruan@gmail.com> 0.7.3-1
- Updated to upstream version 0.7.3
- Added man pages from Debian
- Updated License tag from GPL to GPLv2+
- Removed %%{?dist} tag from changelog

* Sun Jun 24 2007 Andrea Musuruane <musuruan@gmail.com> 0.7.1-1
- Updated to upstream version 0.7.1
- Updated icon cache scriptlets to be compliant to new guidelines

* Thu Jun 07 2007 Andrea Musuruane <musuruan@gmail.com> 0.7.0-2
- Added a patch from Ian Chapman to remove the buggy tools menu which 
  only contains IO regs which frequently crashes desmume on x86_64
- Added a patch from Ian Chapman to make desmume-glade ONLY look in the 
  installed location for it's .glade files and not to use the "uninstalled" 
  location
- Shortened description
- Better use of %%{name} macro

* Fri May 25 2007 Andrea Musuruane <musuruan@gmail.com> 0.7.0-1
- Updated to upstrem version 0.7.0

* Sun Mar 25 2007 Andrea Musuruane <musuruan@gmail.com> 0.6.0-1
- Initial release for Dribble

