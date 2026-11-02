%global srcname wxWidgets
%global pkgname wxGTK
%global gtk3dir bld_gtk3
%global sover 4
%bcond tests 0

%global branch %%(echo %{version} | cut -d. -f-2)
%global branch_clean %%(echo %%{branch} | tr -d '.')
%global srcname_clean %{srcname}%%{branch_clean}
%global wxbasename wxBase%%{branch_clean}

Name:           wxGTK33
Version:        3.3.4
Release:        1%{?dist}
Summary:        GTK port of the wxWidgets GUI library
License:        LGPL-2.0-or-later WITH WxWindows-exception-3.1
URL:            https://www.wxwidgets.org/

Source0:        https://github.com/%{srcname}/%{srcname}/releases/download/v%{version}/%{srcname}-%{version}.tar.bz2
Source10:       wx-config
# https://bugzilla.redhat.com/show_bug.cgi?id=1225148
# remove abort when ABI check fails
# Backport from wxGTK
Patch0:         wxGTK-3.1.6-abicheck.patch

BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  autoconf
BuildRequires:  pkgconfig(webkit2gtk-4.1)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(sdl3)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(gstreamer-plugins-bad-1.0)
BuildRequires:  gettext
BuildRequires:  pkgconfig(cppunit)
BuildRequires:  libmspack-devel
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(ayatana-appindicator3-0.1)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
# For Tests
%if %{with tests}
BuildRequires:  glibc-langpack-en
BuildRequires:  mesa-libEGL
BuildRequires:  xclock
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  python3-httpbin
BuildRequires:  vulkan-loader
%endif

Provides:       %{srcname_clean} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       bundled(scintilla) = 3.7.2
Requires:       %{wxbasename}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-i18n = %{?epoch:%{epoch}:}%{version}-%{release}

%description
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package -n     %{wxbasename}-devel
Summary:        Development files for the wxBase3 library
Requires:       %{wxbasename}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires(post): /usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives

%description -n %{wxbasename}-devel
This package include files needed to link with the wxBase3 library.
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package        devel
Summary:        Development files for the wxGTK library
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-gl = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-media = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-webview = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{wxbasename} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{wxbasename}-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       pkgconfig(gtk+-3.0)
Requires:       pkgconfig(glu)
Provides:       %{srcname_clean}-devel = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
This package include files needed to link with the wxGTK library.
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package        gl
Summary:        OpenGL add-on for the wxWidgets library
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description gl
OpenGL (a 3D graphics API) add-on for the wxWidgets library.
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package        i18n
Summary:        i18n message catalogs for the wxWidgets library
BuildArch:      noarch

%description i18n
i18n message catalogs for the wxWidgets library.
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package        media
Summary:        Multimedia add-on for the wxWidgets library
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description media
Multimedia add-on for the wxWidgets library.
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package        webview
Summary:        WebView add-on for the wxWidgets library
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description webview
WebView add-on for the wxWidgets library.
wxWidgets is the GTK port of the C++ cross-platform wxWidgets
GUI library, offering classes for all common GUI controls as well as a
comprehensive set of helper classes for most common application tasks,
ranging from networking to HTML display and image manipulation.


%package -n     %{wxbasename}
Summary:        Non-GUI support classes from the wxWidgets library

%description -n %{wxbasename}
Every wxWidgets application must link against this library. It contains
mandatory classes that any wxWidgets code depends on (like wxString) and
portability classes that abstract differences between platforms. wxBase can
be used to develop console mode applications -- it does not require any GUI
libraries or the X Window System.


%package        docs
Summary:        Documentation for the wxGTK library
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{srcname_clean}-docs = %{?epoch:%{epoch}:}%{version}-%{release}
BuildArch:      noarch

%description docs
This package provides documentation for the %{srcname_clean} library.


%prep
%autosetup -n %{srcname}-%{version} -p1

# patch some installed files to avoid conflicts with 2.8.*
sed -i -e 's|aclocal)|aclocal/wxwin%{branch_clean}.m4)|' Makefile.in

# fix plugin dir for 64-bit
sed -i -e 's|/usr/lib\b|/usr/%{_lib}|' wx-config.in configure
sed -i -e 's|/lib|/%{_lib}|' src/unix/stdpaths.cpp

# Since we're currently patching configure.in
rm -f configure
./autogen.sh


%build
%global _configure ../configure

mkdir %{gtk3dir}
pushd %{gtk3dir}
%configure \
  --with-gtk=3 \
  --with-opengl \
  --with-sdl \
  --with-libmspack \
  --with-liblzma \
  --enable-intl \
  --disable-rpath \
  --disable-glcanvasegl \
  --enable-ipv6

%make_build
popd

#Docs
WX_SKIP_DOXYGEN_VERSION_CHECK=1 docs/doxygen/regen.sh html
mv docs/doxygen/out/html .

%install
pushd %{gtk3dir}
%make_install
popd

# install our multilib-aware wrapper
##Remove installed
rm %{buildroot}%{_bindir}/wx-config
##Install new and symlink
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_libexecdir}/%{name}/wx-config
sed -i -e 's|=/usr|=%{_prefix}|' %{buildroot}%{_libexecdir}/%{name}/wx-config
ln -s ../..%{_libexecdir}/%{name}/wx-config %{buildroot}%{_bindir}/wx-config-%{branch}
touch %{buildroot}%{_bindir}/wx-config

#Alternatives setup with wxrc
mv %{buildroot}%{_bindir}/wxrc* %{buildroot}%{_libexecdir}/%{name}
ln -s ../..%{_libexecdir}/%{name}/wxrc-%{branch} %{buildroot}%{_bindir}/wxrc-%{branch}
touch %{buildroot}%{_bindir}/wxrc

# move bakefiles to avoid conflicts with 2.8.*
mkdir %{buildroot}%{_datadir}/bakefile/presets/wx%{branch_clean}
mv %{buildroot}%{_datadir}/bakefile/presets/*.* %{buildroot}%{_datadir}/bakefile/presets/wx%{branch_clean}

%find_lang wxstd-%{branch}

%check
%if %{with tests}
pushd %{gtk3dir}/tests
make %{?_smp_mflags}
python3 -m httpbin.core &
LD_LIBRARY_PATH=%{buildroot}%{_libdir} TZ=UTC wxUSE_XVFB=1 \
  WX_TEST_WEBREQUEST_URL="http://localhost:5000" xvfb-run -a ./test ~[.] \
%ifarch s390x
  ~wxTextFile::Special ~wxFile::Special \
%endif
%ifarch riscv64
  ~wxTextFile::Special ~wxFile::Special ~URLTestCase::GetInputStream ~WebRequest::SSL::Error \
%endif
  ~WebRequest::SSL::Ignore ~wxFileName::GetSizeSpecial
LD_LIBRARY_PATH=%{buildroot}%{_libdir} wxUSE_XVFB=1 xvfb-run -a \
  ./test_gui ~[.] \
%ifarch i686
  ~ImageTestCase \
%endif
%ifarch ppc64le
  ~VirtListCtrlTestCase \
%endif
%ifarch s390x
  ~WebView \
%endif
%ifarch riscv64
  ~TreeCtrlTestCase ~WebView ~wxImage::Paste \
%endif
%ifarch loongarch64
  ~WebView \
%endif
  ~wxHtmlPrintout::Pagination
popd
%endif

%post -n %{wxbasename}-devel
if [ -f %{_bindir}/wx-config ] && [ ! -h %{_bindir}/wx-config ] ; then
  rm %{_bindir}/wx-config
fi
/usr/sbin/update-alternatives --install %{_bindir}/wx-config \
  wx-config %{_libexecdir}/%{name}/wx-config 26
/usr/sbin/update-alternatives --install %{_bindir}/wxrc \
  wxrc %{_libexecdir}/%{name}/wxrc 26

%postun -n %{wxbasename}-devel
if [ $1 -eq 0 ] ; then
  /usr/sbin/update-alternatives --remove wx-config %{_libexecdir}/%{name}/wx-config
  /usr/sbin/update-alternatives --remove wxrc %{_libexecdir}/%{name}/wxrc
fi

%files
%doc docs/changes.txt docs/readme.txt
%license docs/gpl.txt docs/lgpl.txt docs/licence.txt docs/licendoc.txt
%license docs/preamble.txt
%{_libdir}/libwx_gtk3u_adv-*.so.%{sover}*
%{_libdir}/libwx_gtk3u_aui-*.so.%{sover}*
%{_libdir}/libwx_gtk3u_core-*.so.%{sover}*
%{_libdir}/libwx_gtk3u_html-*.so.%{sover}*
%{_libdir}/libwx_gtk3u_propgrid-*.so.%{sover}*
%{_libdir}/libwx_gtk3u_qa-*.so.%{sover}*
%{_libdir}/libwx_gtk3u_ribbon-*.so.%{sover}*
%{_libdir}/libwx_gtk3u_richtext-*.so.%{sover}*
%{_libdir}/libwx_gtk3u_stc-*.so.%{sover}*
%{_libdir}/libwx_gtk3u_xrc-*.so.%{sover}*

%files -n %{wxbasename}-devel
%ghost %{_bindir}/wx-config
%ghost %{_bindir}/wxrc
%{_bindir}/wxrc-%{branch}
%{_bindir}/wx-config-%{branch}
%{_includedir}/wx-%{branch}
%{_libdir}/libwx_baseu*.so
%dir %{_libdir}/wx
%dir %{_libdir}/wx/config
%dir %{_libdir}/wx/include
%{_datadir}/aclocal/wxwin%{branch_clean}.m4
%{_datadir}/bakefile/presets/wx%{branch_clean}
%{_libexecdir}/%{name}

%files devel
%{_libdir}/libwx_gtk3u_*.so
%{_libdir}/wx/config/gtk3-unicode-%{branch}
%{_libdir}/wx/include/gtk3-unicode-%{branch}

%files gl
%{_libdir}/libwx_gtk3u_gl-*.so.%{sover}*

%files i18n -f wxstd-%{branch}.lang

%files media
%{_libdir}/libwx_gtk3u_media-*.so.%{sover}*

%files webview
%{_libdir}/libwx_gtk3u_webview-*.so.%{sover}*
%dir %{_libdir}/wx
%{_libdir}/wx/%{version}

%files -n %{wxbasename}
%doc docs/changes.txt docs/readme.txt
%license docs/gpl.txt docs/lgpl.txt docs/licence.txt docs/licendoc.txt
%license docs/preamble.txt
%{_libdir}/libwx_baseu-*.so.*
%{_libdir}/libwx_baseu_net-*.so.%{sover}*
%{_libdir}/libwx_baseu_xml-*.so.%{sover}*

%files docs
%doc html

%changelog
* Mon Nov 02 2026 Phantom X <megaphantomx at hotmail dot com> - 3.3.4-1
- Initial spec
