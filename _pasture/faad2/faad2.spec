%if 0%{?fedora} || 0%{?el7}
%global _with_xmms 1
%global	xmmsinputplugindir %(xmms-config --input-plugin-dir 2>/dev/null)
%endif

Summary:	Library and frontend for decoding MPEG2/4 AAC
Name:		faad2
Epoch:		1
Version:	2.8.8
Release:	7%{?dist}
License:	GPLv2+
URL:		http://www.audiocoding.com/faad2.html
Source:		http://downloads.sourceforge.net/sourceforge/faac/%{name}-%{version}.tar.gz
# fix non-PIC objects in libmp4ff.a
Patch0:		%{name}-pic.patch
Patch1:		fix_undefined_version.patch
# Security issue from videolan contribs
Patch2:         faad2-fix-overflows.patch

BuildRequires:	gcc-c++
BuildRequires:	libsysfs-devel
%{?_with_xmms:
BuildRequires: id3lib-devel
BuildRequires: xmms-devel
}
BuildRequires:	zlib-devel

%{!?_with_xmms:
Obsoletes:	%{name}-xmms < %{version}-%{release}
}

%description
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder, completely
written from scratch.

%package libs
Summary:	Shared libraries of the FAAD 2 AAC decoder
Obsoletes:	%{name} < 1:2.6.1-3

%description libs
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder, completely
written from scratch.

This package contains libfaad.

%package devel
Summary:	Development libraries of the FAAD 2 AAC decoder
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder, completely
written from scratch.

This package contains development files and documentation for libfaad.

%{?_with_xmms:
%package -n xmms-%{name}
Summary:	AAC XMMS Input Plugin
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Provides:	xmms-aac%{?_isa} = %{version}-%{release}
Obsoletes:	xmms-aac < 2.6.1

%description -n xmms-%{name}
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder, completely
written from scratch.

This package contains an input plugin for xmms.
}

%prep
%autosetup -p1

%build
%configure \
    --disable-static \
    %{?_with_xmms:--with-xmms}

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install

#Remove libtool archives.
find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f


%ldconfig_scriptlets libs


%files
%doc AUTHORS ChangeLog NEWS README*
%license COPYING
%{_bindir}/faad
%{_mandir}/man1/faad.1*

%files libs
%{_libdir}/libfaad*.so.*

%files devel
%doc TODO
%{_includedir}/faad.h
%{_includedir}/neaacdec.h
%{_libdir}/libfaad*.so

%{?_with_xmms:
%files -n xmms-%{name}
%doc plugins/xmms/{AUTHORS,NEWS,ChangeLog,README,TODO}
%{xmmsinputplugindir}/libmp4.so
}

%changelog
* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1:2.8.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 07 2019 Nicolas Chauvet <kwizart@gmail.com> - 1:2.8.8-6
- Fix overflows
- Conditionalize xmms

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1:2.8.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Feb 26 2019 Nicolas Chauvet <kwizart@gmail.com> - 1:2.8.8-4
- Group Clean-up

* Tue Jan 29 2019 Nicolas Chauvet <kwizart@gmail.com> - 1:2.8.8-3
- Drop autoreconf

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1:2.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Apr 14 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.8-1
- Update to 2.8.8

* Wed Feb 28 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1:2.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1:2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 28 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:2.8.1-1
- update to 2.8.1

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1:2.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 23 2016 Nicolas Chauvet <nicolas.chauvet@kwizart.fr> - 1:2.7-8
- Bump for dist

* Thu Aug 18 2016 Sérgio Basto <sergio@serjux.com> - 1:2.7-7
- Clean spec, Vascom patches series, rfbz #4200, add license tag

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 1:2.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Dec 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:2.7-5
- Rebuilt for F-20

* Wed Mar 27 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:2.7-4
- Change the escaping space hack - rhbz#928110

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:2.7-3
- Mass rebuilt for Fedora 19 Features

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Mar 13 2009 Dominik Mierzejewski <dominik [AT] greysector [DOT] net> 1:2.7-1
- update to 2.7
- don't install internal libmp4ff
- include manpage
- fix build on x86_64 (non-PIC objects in libmp4ff.a)
- fix rpaths
- make xmms plugin depend on -libs, not the frontend
- preserve docs timestamps

* Mon Nov 10 2008 Dominik Mierzejewski <dominik [AT] greysector [DOT] net> 1:2.6.1-6
- fix CVE-2008-4201

* Sat Oct 18 2008 Dominik Mierzejewski <dominik [AT] greysector [DOT] net> 1:2.6.1-5
- add Obsoletes: for xmms-aac to ensure smooth upgrade from Freshrpms
- add some additional docs for xmms-faad2

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1:2.6.1-4
- rebuild

* Sun Jan 13 2008 Dominik Mierzejewski <dominik [AT] greysector [DOT] net> 1:2.6.1-3
- split off libs to avoid multilib conflicts

* Sun Nov 11 2007 Dominik Mierzejewski <dominik [AT] greysector [DOT] net> 1:2.6.1-2
- bring back the XMMS plugin
- move EOL fixup to prep
- fix URLs

* Thu Nov 01 2007 Dominik Mierzejewski <dominik [AT] greysector [DOT] net> 1:2.6.1-1
- remerge freshrpms specfile
- update to latest upstream, fixes licensing issues!

* Thu Oct 18 2007 Dominik Mierzejewski <dominik [AT] greysector [DOT] net> 1:2.0-21
- fix missing epochs in dependencies

* Tue Oct 16 2007 Dominik Mierzejewski <dominik [AT] greysector [DOT] net> 1:2.0-20
- revert from 2.5

* Wed Sep 26 2007 Dominik Mierzejewski <dominik [AT] greysector [DOT] net> 2.5-4
- disable drm, fixes playback of many AAC streams (bug #1465)

* Sun Sep 23 2007 Dominik Mierzejewski <dominik [AT] greysector [DOT] net> 2.5-3
- remove redundant BRs
- don't disable backward compatibility (breaks ffmpeg)
- silence tar in setup
- use disttag
- fix source file permissions and other rpmlint warnings

* Sat Sep 15 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 2.5-2
- import faad2 from freshrpms as discussed on on repomerge-list

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 2.0-19
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Ville Skyttä <ville.skytta at iki.fi> - 2.0-18.20050131
- Rebuild.

* Sat Jun 17 2006 Ville Skyttä <ville.skytta at iki.fi> - 2.0-17.20050131
- Let soname based autogenerated deps take care of xmms-libs (#1018).
- Revert x86_64 patch to the correct one again (#1017).

* Thu Jun 15 2006 Noa Resare <noa@resare.com> - 2.0-16.20050131
- reverted to obviously broken x86_64 patch to preserve binary compatibility
  and prevent slow motion bug (#1017)
- fixed xmms-libs regression (#1018)

* Wed May 24 2006 Noa Resare <noa@resare.com> - 2.0-15.20050131
- added patch to fix apple trailer playback problem

* Tue May 23 2006 Noa Resare <noa@resare.com> - 2.0-14.20050131
- reverted to older cvs to avoid a GPL violating extra redistribution
  requirement in README
- changed the bogus uint8_t to correct uin32_t in the x86_64 patch

* Sun May 21 2006 Ville Skyttä <ville.skytta at iki.fi> - 2.0-13.20060505
- Avoid aclocal >= 1.8 warnings.

* Sun May 21 2006 Noa Resare <noa@resare.com> - 2.0-12.20060505
- re-introduce the x86_64 patch to restore binary compatibility

* Sat May 20 2006 Noa Resare <noa@resare.com> - 2.0-10.20060505
- patch the sources to be binary compatible with old faad2
- remove library major version bump
- add symbol versioning script for new symbols

* Fri May 05 2006 Noa Resare <noa@resare.com> - 2.0-9.20060505
- upgrade to cvs version
- mp4v2 is no longer included (now a separate package)
- bump libary major version
- drop static library
- remove mp4ff headers from -devel

* Mon Mar 13 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.0-8
- Drop Epoch completely

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Tue Jan 17 2006 Adrian Reber <adrian@lisas.de> - 2.0-0.lvn.7
- Removed change of ownership to root:root during %%install
- Droped Epoch

* Sat Oct 01 2005 Thorsten Leemhuis <fedora[AT]leemhuis.info - 0:2.0-0.lvn.6
- Add faad2-amd64.patch to fix #510

* Wed Jun 15 2005 Ricahrd June <rjune[AT]bravegnuworld.com> - 0:2.0-0.lvn.5
- Included some hand install lines because make install did not place some required header files

* Wed Apr 27 2005 Dams <anvil[AT]livna.org> - 0:2.0-0.lvn.4
- Fixed gcc4 build

* Fri Nov 12 2004 Dams <anvil[AT]livna.org> 0:2.0-0.lvn.3
- Fixing gcc34 build

* Wed Oct 13 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.0-0.lvn.2
- libsndfile is no longer required since 2.0rc1.

* Wed Mar 10 2004 Dams <anvil[AT]livna.org> 0:2.0-0.lvn.1
- Updated to 2.0 final release
- Added missing defattr
- Added xmms-aac provides to xmms-{name}
- Fixed makefile (patch)

* Sun Sep 28 2003 Dams <anvil[AT]livna.org> 0:2.0-0.fdr.0.1.rc1
- Updated to 2.0 rc1
- Added xmms-faad2 subpackage

* Sun Sep 28 2003 Dams <anvil[AT]livna.org> 0:1.1-0.fdr.4
- Added missing scriplets
- buildroot -> RPM_BUILD_ROOT

* Tue Apr 15 2003 Dams <anvil[AT]livna.org> 0:1.1-0.fdr.3
- turned bootstrap into ./bootstrap to prevent build to fail with
  people who dont have "." in their PATH.

* Sat Apr 12 2003 Dams <anvil[AT]livna.org> 0:1.1-0.fdr.2
- Typo in devel Requires.

* Sat Apr 12 2003 Dams <anvil[AT]livna.org> 
- Initial build.
