Name:           opencore-amr
Version:        0.1.5
Release:        8%{?dist}
Summary:        OpenCORE Adaptive Multi Rate Narrowband and Wideband speech lib
License:        ASL 2.0
URL:            http://sourceforge.net/projects/opencore-amr/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         opencore-amr-0.1.3-fix_pc.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++


%description
Library of OpenCORE Framework implementation of Adaptive Multi Rate Narrowband
and Wideband speech codec.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -b .fix
mv opencore/README opencore/README.opencore


%build
%configure --disable-static
%make_build V=1


%install
%make_install
rm $RPM_BUILD_ROOT%{_libdir}/libopencore-amr??.la


%ldconfig_scriptlets


%files
%doc README opencore/ChangeLog opencore/NOTICE opencore/README.opencore
%license LICENSE
%{_libdir}/libopencore-amr??.so.*

%files devel
%{_includedir}/opencore-amr??
%{_libdir}/libopencore-amr??.so
%{_libdir}/pkgconfig/opencore-amr??.pc

%changelog
* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 11 2018 Nicolas Chauvet <kwizart@gmail.com> - 0.1.5-6
- Spec file clean-up

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.1.5-5
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 20 2017 Leigh Scott <leigh123linux@googlemail.com> - 0.1.5-1
- Update to 0.1.5

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.1.3-3
- Mass rebuilt for Fedora 19 Features

* Fri May 18 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.1.3-2
- Fix pkgconfig include

* Sun May 13 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.1.3-1
- Update to 0.1.3

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.1.2-3
- Rebuilt for c++ ABI breakage

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct  4 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.2-1
- New upstream release 0.1.2

* Thu Jul 30 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.1.1-1
- First version of the RPM Fusion package
