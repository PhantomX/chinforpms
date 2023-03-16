%global commit 2c8b59595174a77b6c027ddf0558b151a6c42997
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20141207
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global vermm %%(echo %{version} | cut -d. -f-2)

%global vc_url https://github.com/DaveDavenport/%{name}

Summary:        Music Player Daemon Library
Name:           libmpd
Version:        11.8.90
Release:        100%{?gver}%{?dist}

License:        GPL-2.0-or-later
Url:            http://gmpc.wikia.com/wiki/Gnome_Music_Player_Client

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        http://download.sarine.nl/Programs/gmpc/%{vermm}/%{name}-%{version}.tar.gz
%endif

Patch0:         libmpd-11.8.17-strndup.patch

BuildRequires:  gcc
BuildRequires:  pkgconfig(glib-2.0) >= 2.16
BuildRequires:  make
%if 0%{?with_snapshot}
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
%endif

%package devel
Summary:        Header files for developing programs with libmpd
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       pkgconfig

%description
libmpd is an abstraction around libmpdclient. It provides an easy and
reliable callback based interface to mpd.

%description devel
libmpd-devel is a sub-package which contains header files and static libraries
for developing program with libmpd.

%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

%{?gver:NOCONFIGURE=1 ./autogen.sh}


%build
%configure \
  --disable-static

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install

find %{buildroot} -name '*.la' -delete


%files
%doc ChangeLog COPYING README
%{_libdir}/libmpd.so.1*

%files devel
%{_libdir}/libmpd.so
%{_libdir}/pkgconfig/libmpd.pc
%{_includedir}/libmpd-1.0

%changelog
* Thu Apr 22 2021 Phantom X <megaphantomx at hotmail dot com> - 11.8.90-100.20141207git2c8b595
- 11.8.90

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.17-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.17-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.17-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.17-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.17-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.17-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.17-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.17-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Yaakov Selkowitz <yselkowi@redhat.com> - 11.8.17-6
- Fix build for http://fedoraproject.org/wiki/Changes/Harden_All_Packages

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.8.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.8.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.8.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.8.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 25 2013 Adrian Reber <adrian@lisas.de> - 11.8.17-1
- updated to 11.8.17

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 Adrian Reber <adrian@lisas.de> - 0.20.0-1
- updated to 0.20.0

* Wed Nov 25 2009 Adrian Reber <adrian@lisas.de> - 0.19.0-2
- updated to 0.19.0

* Mon Aug 03 2009 Adrian Reber <adrian@lisas.de> - 0.18.0-3
- added versioned BR for glib2-devel >= 2.16 (#514565)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 08 2009 Adrian Reber <adrian@lisas.de> - 0.18.0-1
- updated to 0.18.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 27 2008 Adrian Reber <adrian@lisas.de> - 0.16.1-1
- updated to 0.16.1

* Mon Feb 25 2008 Adrian Reber <adrian@lisas.de> - 0.15.0-3
- added patch to remove a few inline statements from
  functions which are actually not inline'd

* Fri Feb 15 2008 Adrian Reber <adrian@lisas.de> - 0.15.0-2
- rebuilt for gcc43

* Sun Dec 23 2007 Adrian Reber <adrian@lisas.de> - 0.15.0-1
- update to 0.15.0
- added BR glib2-devel

* Sun Nov 11 2007 Adrian Reber <adrian@lisas.de> - 0.14.0-1
- update to 0.14.0

* Sun Aug 26 2007 Adrian Reber <adrian@lisas.de> - 0.13.0-2
- rebuilt

* Sun Mar 25 2007 Adrian Reber <adrian@lisas.de> - 0.13.0-1
- update to 0.13.0

* Sat Nov 25 2006 Adrian Reber <adrian@lisas.de> - 0.12.0-3
- added requires pkgconfig to -devel package

* Sat Nov 25 2006 Adrian Reber <adrian@lisas.de> - 0.12.0-2
- small changes for FE submission

* Mon Mar 27 2006 Jan "Yenya" Kasprzak <kas@fi.muni.cz> 0.12.0-1
- initial build
