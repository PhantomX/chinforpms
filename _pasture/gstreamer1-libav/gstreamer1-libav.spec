# gstreamer1.prov is broken and hangs, workarround it
%global __gstreamer1_provides %{nil}

%global src_name gst-libav

Name:           gstreamer1-libav
Epoch:          1
Version:        1.20.0
Release:        100%{?dist}
Summary:        GStreamer 1.0 libav-based plug-ins

License:        LGPLv2+
URL:            https://gstreamer.freedesktop.org

Source0:        %{url}/src/%{src_name}/%{src_name}-%{version}.tar.xz

Patch0:         0001-gstavviddec-remove-stupid-check-for-VC1.patch

BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  gstreamer1-devel >= %{version}
BuildRequires:  gstreamer1-plugins-base-devel >= %{version}
BuildRequires:  orc-devel
BuildRequires:  bzip2-devel
BuildRequires:  zlib-devel
BuildRequires:  ffmpeg-devel

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new 
plugins.

This package provides libav-based GStreamer plug-ins.

%if 0
# gstreamer1 uses hotdoc which isn't provided yet
%package devel-docs
Summary: Development documentation for the libav GStreamer plug-in
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description devel-docs
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the development documentation for the libav GStreamer
plug-in.
%endif


%prep
%autosetup -n %{src_name}-%{version} -p1

%build
%meson  \
    -D package-name='chinforpms GStreamer-plugins-ugly package' \
    -D package-origin='https://copr.fedorainfracloud.org/coprs/phantomx/chinforpms' \
    -D doc=disabled

%meson_build

%install
%meson_install


%files
%doc AUTHORS ChangeLog NEWS README.md
%license COPYING
%{_libdir}/gstreamer-1.0/libgstlibav.so

%if 0
%files devel-docs
# Take the dir and everything below it for proper dir ownership
%doc %{_datadir}/gtk-doc
%endif

%changelog
* Sun Apr 03 2022 Phantom X <megaphantomx at hotmail dot com> - 1:1.20.1-100
- Fix crash with wmv videos

* Sun Feb 06 2022 Sérgio Basto <sergio@serjux.com> - 1:1.20.0-1
- Update gstreamer1-libav to 1.20.0

* Mon Nov 15 2021 Sérgio Basto <sergio@serjux.com> - 1:1.19.3-2
- Rebuilt for new ffmpeg snapshot

* Mon Nov 15 2021 Sérgio Basto <sergio@serjux.com> - 1:1.19.3-1
- Update gstreamer1-libav to 1.19.3

* Thu Nov 11 2021 Leigh Scott <leigh123linux@gmail.com> - 1:1.19.2-2
- Rebuilt for new ffmpeg snapshot

* Sat Oct 09 2021 Sérgio Basto <sergio@serjux.com> - 1:1.19.2-1
- Update gstreamer1-libav to 1.19.2

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1:1.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
- gstreamer1.prov is broken and hangs, workarround it

* Tue Jun 08 2021 Leigh Scott <leigh123linux@gmail.com> - 1.19.1-1
- Update

* Wed Mar 24 2021 Leigh Scott <leigh123linux@gmail.com> - 1.18.4-2
- Drop patch

* Wed Mar 17 2021 Leigh Scott <leigh123linux@gmail.com> - 1.18.4-1
- 1.18.4

* Sun Feb 28 2021 Leigh Scott <leigh123linux@gmail.com> - 1.18.2-4
- Add patch for ffmpeg-4.4

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.18.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 31 2020 Leigh Scott <leigh123linux@gmail.com> - 1.18.2-2
- Rebuilt for new ffmpeg snapshot

* Sun Dec 13 2020 Leigh Scott <leigh123linux@gmail.com> - 1.18.2-1
- 1.18.2

* Sun Nov  1 2020 Leigh Scott <leigh123linux@gmail.com> - 1.18.1-1
- 1.18.1

* Wed Sep  9 2020 Leigh Scott <leigh123linux@gmail.com> - 1.18.0-1
- 1.18.0

* Sun Aug 23 2020 Leigh Scott <leigh123linux@gmail.com> - 1.17.90-1
- 1.17.90

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 08 2020 Leigh Scott <leigh123linux@gmail.com> - 1.17.2-1
- 1.17.2

* Mon Jun 22 2020 Leigh Scott <leigh123linux@gmail.com> - 1.17.1-1
- 1.17.1

* Thu Mar 12 2020 Leigh Scott <leigh123linux@gmail.com> - 1.16.2-3
- Rebuilt for i686

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Feb 01 2020 Leigh Scott <leigh123linux@googlemail.com> - 1.16.2-1
- 1.16.2

* Wed Sep 25 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.16.1-1
- 1.16.1

* Wed Aug 07 2019 Leigh Scott <leigh123linux@gmail.com> - 1.16.0-2
- Rebuild for new ffmpeg version

* Wed Apr 24 2019 Leigh Scott <leigh123linux@gmail.com> - 1.16.0-1
- 1.16.0

* Tue Mar 19 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.15.2-1
- 1.15.2

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Feb 09 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.15.1-1
- 1.15.1

* Tue Oct 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.14.4-1
- 1.14.4

* Tue Sep 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.14.3-1
- 1.14.3

* Sat Aug 18 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.14.2-1
- 1.14.2

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 31 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.14.1-1
- 1.14.1

* Thu Mar 22 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.14.0-1
- Update to 1.14.0

* Sun Mar 04 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.13.1-2
- Use bundled libav for F28 as it doesn't build with ffmpeg git

* Wed Feb 28 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.13.1-1
- 1.13.1

* Fri Jan 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.12.4-3
- Use bundled libav for F28

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.12.4-2
- Rebuilt for ffmpeg-3.5 git

* Mon Dec 11 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.12.4-1
- Update to 1.12.4
- Remove patch for FFMpeg 3.4 APIs (fixed in ffmpeg-3.4.1)

* Sat Nov 18 2017 Simone Caronni <negativo17@gmail.com> - 1.12.3-3
- Temporary patch for FFMpeg 3.4 APIs.

* Mon Oct 16 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.12.3-2
- Rebuild for ffmpeg update

* Wed Sep 20 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.12.3-1
- Update to 1.12.3

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 18 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.12.2-1
- Update to 1.12.2

* Fri Jun 23 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.12.1-1
- Update to 1.12.1

* Wed May 17 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.12.0-2
- Rebuilt for f26 ffmpeg bump

* Fri May 12 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.12.0-1
- Update to 1.12.0

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.11.90-2
- Rebuild for ffmpeg update

* Tue Apr 18 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.11.90-1
- Update to 1.11.90

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Feb 27 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.11.2-1
- Update to 1.11.2

* Mon Jan 16 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.11.1-1
- Update to 1.11.1

* Wed Nov 30 2016 leigh scott <leigh123linux@googlemail.com> - 1.10.2-1
- Update to 1.10.2

* Fri Nov 11 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 1.10.0-2
- Drop no longer needed ignore_vaapi.patch

* Fri Nov 11 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 1.10.0-1
- Update to 1.10.0

* Fri Nov 11 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.8.2-4
- Add patch to disable ffmpeg hardware acceleration for nvenc and qsv (rfbz#4334)

* Fri Nov 11 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.8.2-3
- Add patch to ignore VAAPI decoders and VAAPI/nvenc encoders (rfbz#4334)

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 1.8.2-2
- Rebuilt for ffmpeg-3.1.1

* Sun Jun 12 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 1.8.2-1
- Update to 1.8.2

* Wed May 18 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 1.8.1-1
- Update to 1.8.1

* Sat Jan 23 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 1.6.3-1
- Update to 1.6.3

* Thu Dec 24 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 1.6.2-1
- Update to 1.6.2

* Sat Oct 31 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 1.6.1-1
- Update to 1.6.1
- Upstream is using ffmpeg instead of libav now, switch to system ffmpeg-libs

* Sat May 16 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 1.4.5-1
- Update to 1.4.5
- Update libav to 10.6

* Wed Oct  1 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.4.3-1
- Update to 1.4.3
- Includes libav 10.5

* Fri Aug 29 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.4.1-1
- Update to 1.4.1 (rf#3343)
- Includes libav 10.4

* Sun Jun 15 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.2.4-1
- Update to 1.2.4 (rf#3269)
- Update libav to 9.13

* Sat Feb 15 2014 Michael Kuhn <suraia@ikkoku.de> - 1.2.3-1
- Update to 1.2.3.
- Update libav to 9.11.

* Sat Jan 04 2014 Michael Kuhn <suraia@ikkoku.de> - 1.2.2-1
- Update to 1.2.2.

* Sat Nov 16 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.2.1-1
- Rebase to 1.2.1

* Sun Oct 13 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.2.0-1
- Rebase to 1.2.0
- Upgrade the buildin libav to 9.10 to get all the security fixes from
  upstream libav
- Switch back to included libav copy again, libav and ffmpeg have
  deviated to much to use a system ffmpeg lib as libav replacement,
  this fixes a bad memory-leak (rpmfusion#2976)

* Mon Sep 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.1.3-4
- Rebuilt

* Tue Aug 27 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.1.3-3
- Rebuild now devel properly points to f20

* Mon Aug 26 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.1.3-2
- Rebuild for ffmpeg-2.0

* Thu Aug  8 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.1.3-1
- Rebase to 1.1.3
- Switch back to using system ffmpeg

* Tue Aug  6 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.9-1
- Rebase to 1.0.9
- This includes an upgrade of the buildin libav to 0.8.8 which includes a
  bunch of security fixes from
- No longer overwrite the included libav, as the bundled one is the latest

* Mon Mar 25 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.6-1
- Rebase to 1.0.6
- Upgrade the buildin libav to 0.8.6 to get all the security fixes from
  upstream libav

* Sun Mar 10 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.5-2
- Add a patch from upstream git to fix h264 decoding artifacts (rf#2710)
- Add a patch from upstream libav to fix miscompilation with gcc-4.8
  (rf#2710, gnome#695166, libav#388)

* Sat Mar  2 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.5-1
- Rebase to 1.0.5 (rf#2688)
- Upgrade the buildin libav to 0.8.5 to get all the security fixes from
  upstream libav

* Sat Nov  3 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.2-2
- Build included libav with the default RPM_OPT_FLAGS (rf#2560, rf#2472)

* Sun Oct 28 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.2-1
- Rebase to 1.0.2
- Included libav copy updated to 0.8.4
- Change the license to LGPLv2+, as the GPL only postproc plugin is no longer
  included
- Replace references to ffmpeg with libav (rf#2472)
- Add COPYING.LIB to %%doc (rf#2472)
- Run make with V=1 (rf#2472)

* Sun Sep 23 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.11.99-1
- New upstream release 0.11.99

* Sun Sep  9 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.11.93-1
- First version of gstreamer1-libav for rpmfusion
