%global         majorminor      1.0
%global     __python %{__python3}

%if 0%{?fedora}
%bcond_without unwind
%else
%bcond_with unwind
%endif 

#global gitrel     140
#global gitcommit  a70055b58568f7304ba46bd8742232337013487b
#global shortcommit %%(c=%{gitcommit}; echo ${c:0:5})

%global         _glib2                  2.32.0
%global         _libxml2                2.4.0
%global         _gobject_introspection  1.31.1

Name:           gstreamer1
Version:        1.22.11
Release:        100%{?gitcommit:.git%{shortcommit}}%{?dist}
Summary:        GStreamer streaming media framework runtime

License:        LGPL-2.1-or-later
URL:            http://gstreamer.freedesktop.org/
%if 0%{?gitrel}
# git clone git://anongit.freedesktop.org/gstreamer/gstreamer
# cd gstreamer; git reset --hard %{gitcommit}; ./autogen.sh; make; make distcheck
Source0:        gstreamer-%{version}.tar.xz
%else
Source0:        http://gstreamer.freedesktop.org/src/gstreamer/gstreamer-%{version}.tar.xz
%endif
## For GStreamer RPM provides
Patch0:         gstreamer-inspect-rpm-format.patch
Source1:        gstreamer1.prov
Source2:        gstreamer1.attr

BuildRequires:  meson >= 0.48.0
BuildRequires:  gcc
BuildRequires:  glib2-devel >= %{_glib2}
BuildRequires:  libxml2-devel >= %{_libxml2}
BuildRequires:  gobject-introspection-devel >= %{_gobject_introspection}
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  check-devel
BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  libcap-devel
%if %{with unwind}
BuildRequires:  libunwind-devel
%endif
BuildRequires:  elfutils-devel
BuildRequires:  bash-completion


%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new 
plugins.


%package devel
Summary:        Libraries/include files for GStreamer streaming media framework
Requires:       %{name}%{?isa} = %{version}-%{release}
Requires:       glib2-devel%{?_isa} >= %{_glib2}
Requires:       libxml2-devel%{?_isa} >= %{_libxml2}
Requires:       check-devel
# file /usr/include/gstreamer-1.0/gst/base/gstaggregator.h conflicts between attempted installs of gstreamer1-plugins-bad-free-devel-1.12.4-3.fc28.x86_64 and gstreamer1-devel-1.13.1-1.fc29.x86_64
Conflicts:      gstreamer1-plugins-bad-free-devel < 1.13

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%if 0
%package devel-docs
Summary:         Developer documentation for GStreamer streaming media framework
Requires:        %{name} = %{version}-%{release}
BuildArch:       noarch


%description devel-docs
This %{name}-devel-docs contains developer documentation for the
GStreamer streaming media framework.
%endif

%prep
%autosetup -p1 -n gstreamer-%{version}

# Dirty multilib fix
sed -e "/GST_PLUGIN_SCANNER_INSTALLED/s|, 'gst-plugin-scanner|\0-%{__isa_bits}|g" \
  -i meson.build
sed -e '/EXESUFFIX/s| "gst-plugin-scanner|\0-%{__isa_bits}|g' \
  -i gst/gstpluginloader.c


%build
%meson \
  -D package-name='chinforpms GStreamer package' \
  -D package-origin='https://copr.fedorainfracloud.org/coprs/phantomx/chinforpms' \
  -D tests=disabled -D examples=disabled \
  -D ptp-helper-permissions=capabilities \
  %{!?with_unwind:-D libunwind=disabled -D libdw=disabled } \
  -D dbghelp=disabled \
  -D doc=disabled
%meson_build


%install
%meson_install

# Dirty multilib fix
mv %{buildroot}%{_libexecdir}/gstreamer-%{majorminor}/gst-plugin-scanner{,-%{__isa_bits}}

for i in inspect launch stats typefind ;do
  bin=gst-$i-%{majorminor}
  mv %{buildroot}%{_bindir}/$bin{,-%{__isa_bits}}

cat >> %{buildroot}%{_bindir}/$bin <<EOF
#!/usr/bin/sh
host=\$(uname -m)
case "\$host" in
  alpha*|ia64*|ppc64*|powerpc64*|s390x*|x86_64*|aarch64*)
    exec %{_bindir}/$bin-64 "\$@"
    ;;
  *)
    exec %{_bindir}/$bin-32 "\$@"
    ;;
esac
EOF
  chmod 0755 %{buildroot}%{_bindir}/$bin

echo ".so man1/$bin.1" > %{buildroot}%{_mandir}/man1/$bin-%{__isa_bits}.1

done

%find_lang gstreamer-%{majorminor}

# Add the provides script
install -m0755 -D %{SOURCE1} %{buildroot}%{_rpmconfigdir}/gstreamer1.prov
# Add the gstreamer plugin file attribute entry (rpm >= 4.9.0)
install -m0644 -D %{SOURCE2} %{buildroot}%{_rpmconfigdir}/fileattrs/gstreamer1.attr


%files -f gstreamer-%{majorminor}.lang
%license COPYING
%doc AUTHORS NEWS README.md README.static-linking RELEASE
%{_libdir}/libgstreamer-%{majorminor}.so.*
%{_libdir}/libgstbase-%{majorminor}.so.*
%{_libdir}/libgstcheck-%{majorminor}.so.*
%{_libdir}/libgstcontroller-%{majorminor}.so.*
%{_libdir}/libgstnet-%{majorminor}.so.*

%{_libexecdir}/gstreamer-%{majorminor}/

%dir %{_libdir}/gstreamer-%{majorminor}
%{_libdir}/gstreamer-%{majorminor}/libgstcoreelements.so
%{_libdir}/gstreamer-%{majorminor}/libgstcoretracers.so

%{_libdir}/girepository-1.0/Gst-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstBase-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstCheck-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstController-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstNet-%{majorminor}.typelib

%{_bindir}/gst-inspect-%{majorminor}*
%{_bindir}/gst-launch-%{majorminor}*
%{_bindir}/gst-stats-%{majorminor}*
%{_bindir}/gst-typefind-%{majorminor}*

%{_rpmconfigdir}/gstreamer1.prov
%{_rpmconfigdir}/fileattrs/gstreamer1.attr

%doc %{_mandir}/man1/gst-inspect-%{majorminor}*.*
%doc %{_mandir}/man1/gst-launch-%{majorminor}*.*
%doc %{_mandir}/man1/gst-stats-%{majorminor}*.*
%doc %{_mandir}/man1/gst-typefind-%{majorminor}*.*

%{_datadir}/bash-completion/completions/gst-inspect-1.0
%{_datadir}/bash-completion/completions/gst-launch-1.0
%{_datadir}/bash-completion/helpers/gst

%files devel
%dir %{_includedir}/gstreamer-%{majorminor}/
%dir %{_includedir}/gstreamer-%{majorminor}/gst/
%dir %{_includedir}/gstreamer-%{majorminor}/gst/base/
%dir %{_includedir}/gstreamer-%{majorminor}/gst/check/
%dir %{_includedir}/gstreamer-%{majorminor}/gst/controller/
%dir %{_includedir}/gstreamer-%{majorminor}/gst/net/
%{_includedir}/gstreamer-%{majorminor}/gst/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/base/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/check/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/controller/*.h
%{_includedir}/gstreamer-%{majorminor}/gst/net/*.h

%{_libdir}/libgstreamer-%{majorminor}.so
%{_libdir}/libgstbase-%{majorminor}.so
%{_libdir}/libgstcheck-%{majorminor}.so
%{_libdir}/libgstcontroller-%{majorminor}.so
%{_libdir}/libgstnet-%{majorminor}.so

%{_datadir}/gir-1.0/Gst-%{majorminor}.gir
%{_datadir}/gir-1.0/GstBase-%{majorminor}.gir
%{_datadir}/gir-1.0/GstCheck-%{majorminor}.gir
%{_datadir}/gir-1.0/GstController-%{majorminor}.gir
%{_datadir}/gir-1.0/GstNet-%{majorminor}.gir

%{_datadir}/aclocal/gst-element-check-%{majorminor}.m4

%dir %{_datadir}/gstreamer-%{majorminor}/gdb
%{_datadir}/gstreamer-%{majorminor}/gdb/
%{_datadir}/gdb/auto-load/

%{_libdir}/pkgconfig/gstreamer-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-base-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-controller-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-check-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-net-%{majorminor}.pc

%if 0
%files devel-docs
%doc %{_datadir}/gtk-doc/html/gstreamer-%{majorminor}/
%doc %{_datadir}/gtk-doc/html/gstreamer-libs-%{majorminor}/
%doc %{_datadir}/gtk-doc/html/gstreamer-plugins-%{majorminor}/
%endif


%changelog
* Fri Apr 19 2024 Phantom X <megaphantomx at hotmail dot com> - 1.22.11-100
- 1.22.11

* Fri Jan 26 2024 Phantom X <megaphantomx at hotmail dot com> - 1.22.9-100
- 1.22.9

* Wed Dec 20 2023 Phantom X <megaphantomx at hotmail dot com> - 1.22.8-100
- 1.22.8

* Wed Nov 15 2023 Phantom X <megaphantomx at hotmail dot com> - 1.22.7-100
- 1.22.7

* Fri Sep 22 2023 Phantom X <megaphantomx at hotmail dot com> - 1.22.6-100
- 1.22.6

* Sun Jul 23 2023 Phantom X <megaphantomx at hotmail dot com> - 1.22.5-100
- 1.22.5

* Thu Jun 22 2023 Phantom X <megaphantomx at hotmail dot com> - 1.22.4-100
- 1.22.4

* Fri May 19 2023 Phantom X <megaphantomx at hotmail dot com> - 1.22.3-100
- 1.22.3

* Tue May 02 2023 Phantom X <megaphantomx at hotmail dot com> - 1.22.2-101
- Fix multilib wrappers again

* Fri Apr 14 2023 Phantom X <megaphantomx at hotmail dot com> - 1.22.2-100
- 1.22.2

* Wed Mar 15 2023 Phantom X <megaphantomx at hotmail dot com> - 1.22.1-100
- 1.22.1

* Tue Dec 20 2022 Phantom X <megaphantomx at hotmail dot com> - 1.20.5-100
- 1.20.5

* Sun Oct 16 2022 Phantom X <megaphantomx at hotmail dot com> - 1.20.4-100
- 1.20.4

* Wed Jul 20 2022 Phantom X <megaphantomx at hotmail dot com> - 1.20.3-100
- 1.20.3

* Sat Feb 05 2022 Phantom X <megaphantomx at hotmail dot com> - 1.20.0-100
- 1.20.0

* Fri Nov 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1.19.3-100
- 1.19.3

* Thu Sep 30 2021 Phantom X <megaphantomx at hotmail dot com> - 1.19.2-100
- 1.19.2

* Thu Sep 16 2021 Phantom X <megaphantomx at hotmail dot com> - 1.18.5-100
- 1.18.5

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1.18.4-101
- Rawhide sync

* Wed Mar 17 2021 Phantom X <megaphantomx at hotmail dot com> - 1.18.4-100
- 1.18.4

* Thu Jan 14 2021 Phantom X <megaphantomx at hotmail dot com> - 1.18.3-100
- 1.18.3

* Mon Dec  7 2020 Phantom X <megaphantomx at hotmail dot com> - 1.18.2-100
- 1.18.2

* Tue Oct 27 2020 Phantom X <megaphantomx at hotmail dot com> - 1.18.1-100
- 1.18.1

* Tue Sep 29 2020 Phantom X <megaphantomx at hotmail dot com> - 1.18.0-100
- 1.18.0
- f33 sync

* Wed Dec 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.16.2-100
- 1.16.2

* Wed Oct 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.16.1-101
- f31 sync, libpcap
- Fix multilib wrappers

* Tue Sep 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.16.1-100
- 1.16.1

* Fri Apr 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.16.0-100
- 1.16.0

* Tue Apr 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.15.90-100
- 1.15.90

* Thu Apr 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.15.2-100
- 1.15.2

* Thu Oct 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.14.4-101.chinfo
- Multilib wrappers

* Tue Oct 02 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.14.4-100.chinfo
- 1.14.4

* Mon Sep 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.14.3-100.chinfo
- 1.14.3

* Fri Jul 20 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.14.2-100.chinfo
- 1.14.2

* Sun May 27 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.14.1-101.chinfo
- 1.14.1
- f28 sync (#1581325)

* Thu May 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.14.1-100.chinfo
- 1.14.1

* Sat Apr 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.14.0-100.chinfo
- 1.14.0
- f28 sync

* Thu Dec 07 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.12.4-100.chinfo
- 1.12.4

* Mon Sep 18 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.12.3-100.chinfo
- 1.12.3

* Fri Jul 14 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.12.2-100.chinfo
- 1.12.2

* Fri Jun 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.12.1-101.chinfo
- Multilib fix, dirty, but better

* Tue Jun 20 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.12.1-100.chinfo
- 1.12.1

* Sun Jun 18 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.10.5-100.chinfo
- 1.10.5

* Thu Feb 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.10.4-100.chinfo
- 1.10.4

* Thu Feb 02 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.10.3-100.chinfo
- 1.10.3

* Mon Jan 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.10.2-2
- Set libexecdir to %{_libdir} on ix86 archs

* Mon Dec 05 2016 Wim Taymans <wtaymans@redhat.com> - 1.10.2-1
- Update to 1.10.2

* Mon Nov 28 2016 Wim Taymans <wtaymans@redhat.com> - 1.10.1-1
- Update to 1.10.1

* Thu Nov 3 2016 Wim Taymans <wtaymans@redhat.com> - 1.10.0-1
- Update to 1.10.0

* Fri Sep 30 2016 Wim Taymans <wtaymans@redhat.com> - 1.9.90-1
- Update to 1.9.90
- remove obsolete patches

* Thu Sep  8 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.2-3
- fix build on Power64

* Thu Sep 01 2016 Wim Taymans <wtaymans@redhat.com> - 1.9.2-2
- fix build on s390x

* Thu Sep 01 2016 Wim Taymans <wtaymans@redhat.com> - 1.9.2-1
- Update to 1.9.2
- gstconfig.h was moved to normal include dir

* Thu Jul 07 2016 Wim Taymans <wtaymans@redhat.com> - 1.9.1-1
- Update to 1.9.1

* Thu Jun 09 2016 Wim Taymans <wtaymans@redhat.com> - 1.8.2-1
- Update to 1.8.2

* Thu Apr 21 2016 Wim Taymans <wtaymans@redhat.com> - 1.8.1-1
- Update to 1.8.1

* Thu Mar 24 2016 Wim Taymans <wtaymans@redhat.com> - 1.8.0-1
- Update to 1.8.0

* Wed Mar 16 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.91-1
- Update to 1.7.91

* Wed Mar 02 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.90-1
- Update to 1.7.90

* Fri Feb 19 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.2-1
- Update to 1.7.2

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 4 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.1-1
- Update to 1.7.1
- update rpm inspect patch
- add gst-stats
- add core traces

* Tue Dec 15 2015 Wim Taymans <wtaymans@redhat.com> - 1.6.2-1
- Update to 1.6.2

* Mon Nov 2 2015 Wim Taymans <wtaymans@redhat.com> - 1.6.1-1
- Update to 1.6.1

* Sat Sep 26 2015 Kalev Lember <klember@redhat.com> - 1.6.0-2
- Remove lib64 rpaths from newly added binaries

* Sat Sep 26 2015 Kalev Lember <klember@redhat.com> - 1.6.0-1
- Update to 1.6.0
- Use license macro for COPYING

* Mon Sep 21 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.91-1
- Update to 1.5.91

* Wed Aug 19 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.90-1
- Update to 1.5.90

* Thu Jun 25 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.2-1
- Update to 1.5.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 5 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.1-1
- Update to 1.5.1
- add new bash-completion scripts
- gstconfig.h got moved

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.4.5-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Jan 28 2015 Bastien Nocera <bnocera@redhat.com> 1.4.5-1
- Update to 1.4.5

* Fri Nov 14 2014 Kalev Lember <kalevlember@gmail.com> - 1.4.4-1
- Update to 1.4.4

* Mon Sep 22 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.2-1
- Update to 1.4.2

* Fri Aug 29 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.1-1
- Update to 1.4.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.4.0-2
- Rebuilt for gobject-introspection 1.41.4

* Tue Jul 22 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.0-1
- Update to 1.4.0

* Fri Jul 11 2014 Wim Taymans <wtaymans@redhat.com> - 1.3.91-1
- Update to 1.3.91

* Mon Jun 30 2014 Richard Hughes <rhughes@redhat.com> - 1.3.90-1
- Update to 1.3.90

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Apr 20 2014 Brian Pepple <bpepple@fedoraproject.org> - 1.2.4-1
- Update to 1.2.4.

* Mon Feb 10 2014 Brian Pepple <bpepple@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3.

* Fri Dec 27 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2.

* Mon Nov 11 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1.

* Tue Sep 24 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0.

* Thu Sep 19 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.90-1
- Update to 1.1.90.

* Wed Aug 28 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4.

* Mon Jul 29 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3.

* Fri Jul 12 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2.

* Fri Apr 26 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.7-1
- Update to 1.0.7.

* Wed Mar 27 2013 Adam Jackson <ajax@redhat.com>
- Tweak BRs for RHEL

* Fri Mar 22 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6.
- Remove BR on PyXML.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5.

* Wed Dec 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Wed Nov 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Thu Oct 25 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2.

* Sun Oct  7 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Mon Oct  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.0-2
- Enable verbose build

* Mon Sep 24 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0.

* Wed Sep 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.99-1
- Update to 0.11.99

* Fri Sep 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.94-1
- Update to 0.11.94.

* Sat Sep  8 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.93-2
- Add patch to gst-inspect to generate RPM provides
- Add RPM find-provides script

* Tue Aug 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.93-1
- Update to 0.11.93.
- Bump minimum version of glib2 needed.

* Fri Aug  3 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.92-2
- Use %%global instead of %%define.
- Remove rpath.

* Tue Jul 17 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.92-1
- Initial Fedora spec file.

