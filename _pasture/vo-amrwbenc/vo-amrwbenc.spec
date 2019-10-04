Name:			vo-amrwbenc
Version:		0.1.3
Release:		10%{?dist}
Summary:		VisualOn AMR-WB encoder library
License:		ASL 2.0
URL:			http://opencore-amr.sourceforge.net/
Source0:		http://downloads.sourceforge.net/opencore-amr/%{name}/%{name}-%{version}.tar.gz

BuildRequires: gcc

%description
This library contains an encoder implementation of the Adaptive 
Multi Rate Wideband (AMR-WB) audio codec. The library is based 
on a codec implementation by VisualOn as part of the Stagefright 
framework from the Google Android project.

%package        devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure --disable-static
%make_build

%install
%make_install
rm %{buildroot}%{_libdir}/libvo-amrwbenc.la


%ldconfig_scriptlets


%files
%license COPYING
%doc README NOTICE
%{_libdir}/libvo-amrwbenc.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/libvo-amrwbenc.so
%{_libdir}/pkgconfig/vo-amrwbenc.pc

%changelog
* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.1.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 25 2018 Nicolas Chauvet <kwizart@gmail.com> - 0.1.3-8
- Add missing cc

* Tue Sep 25 2018 Nicolas Chauvet <kwizart@gmail.com> - 0.1.3-7
- Spec file clean-up

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.1.3-6
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Oct 11 2015 Michael Kuhn <suraia@ikkoku.de> - 0.1.3-1
- Update to 0.1.3.

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Sep 16 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.1.2-1
- New upstream release 0.1.2
- Drop static lib
- Some spec-file cleanups

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed May 04 2011 Prabin Kumar Datta <prabindatta@fedoraproject.org> - 0.1.1-1
- upgraded to new version 0.1.1

* Wed May 04 2011 Prabin Kumar Datta <prabindatta@fedoraproject.org> - 0.1.0-1
- Initial build
