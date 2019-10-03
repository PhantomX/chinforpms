Summary: DTS Coherent Acoustics decoder library
Name: libdca
Version: 0.0.6
Release: 5%{?dist}
License: GPLv2+
URL: https://code.videolan.org/videolan/libdca
Source: http://download.videolan.org/pub/videolan/%{name}/%{version}/%{name}-%{version}.tar.bz2
BuildRequires: gcc

%description
libdca is a free library for decoding DTS Coherent Acoustics streams. It is
released under the terms of the GPL license. The DTS Coherent Acoustics
standard is used in a variety of applications, including DVD, DTS audio CD and
radio broadcasting.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for %{name}.

Install %{name}-devel if you wish to develop or compile
applications that use %{name}.

%package tools
Summary: Various tools for use with %{name}

%description tools
Various tools that use %{name}.

%prep
%setup -q

iconv -f ISO8859-1 -t UTF-8 AUTHORS > tmp; mv tmp AUTHORS

%build
%configure --disable-static
# Get rid of the /usr/lib64 RPATH on 64bit (as of 0.0.5)
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install

#Remove libtool archives.
find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f

%ldconfig_scriptlets

%files
%doc AUTHORS ChangeLog NEWS README
%license COPYING
%{_libdir}/%{name}.so.*

%files tools
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%doc TODO doc/%{name}.txt
%{_libdir}/pkgconfig/libd??.pc
%{_includedir}/d??.h
%{_libdir}/%{name}.so

%changelog
* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 28 2019 Nicolas Chauvet <kwizart@gmail.com> - 0.0.6-4
- Few fixes - fixed upstream url

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 15 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.0.6-1
- Update to 0.0.6 release

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.0.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.0.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.0.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu May 28 2015 Nicolas Chauvet <kwizart@gmail.com> - 0.0.5-9
- Fix build with rawhide - rfbz#3674
- Spec file clean-up

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.5-7
- Mass rebuilt for Fedora 19 Features

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 17 2009 kwizart < kwizart at gmail.com > - 0.0.5-5
- Rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.5-4
- rebuild for new F11 features

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.0.5-3
- rebuild

* Fri Nov  2 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.0.5-2
- Merge freshrpms spec into livna spec for rpmfusion:
- Update to latest upstream releae 0.0.5 as used by freshrpms
- Set release to 2 to be higher as both livna and freshrpms latest release
- Drop x86_64 patch (not needed since we override OPT_CFLAGS anyways)
- Drop visibility patch, this should be done upstream
- Drop upstream integrated libtool patch
- No longer regenerate the autoxxx scripts as this is no longer needed
- Port strict aliasing patch to 0.0.5 release
- Add relative symlink creation patch from freshrpms
- Update license tag in accordance with new license tag guidelines

* Sat Nov 25 2006 Dominik Mierzejewski <rpm@greysector.net> 0.0.2-3
- added patches from gentoo (shared build, strict aliasing and visibility)

* Sat Oct 28 2006 Dominik Mierzejewski <rpm@greysector.net> 0.0.2-2
- renamed to libdca
- added Obsoletes/Provides
- simplified autotools call

* Mon Aug 07 2006 Dominik Mierzejewski <rpm@greysector.net> 0.0.2-1
- stop pretending we have a newer version

* Sat Apr 16 2005 Dominik Mierzejewski <rpm@greysector.net> 0.0.3-0.20040725.1
- adapted ArkLinux specfile
- x86_64 portability patch

* Sun Jul 25 2004 Bernhard Rosenkraenzer <bero@arklinux.org> 0.0.3-0.20040725.1ark
- Force -fPIC
- Update

* Wed Jul 07 2004 Bernhard Rosenkraenzer <bero@arklinux.org> 0.0.3-0.20040707.1ark
- initial RPM
