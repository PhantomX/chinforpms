%global commit 8864091a01f1fbbce361d654a4bae96ad20e2211
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180419
%global with_snapshot 1

%global freebsd_rev 467805

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

# Use ALSA backend?
%global alsa_backend      1

# Use system nspr/nss?
%global system_nss        1

# Use system hunspell?
%global system_hunspell   1

# Use system libevent?
%if 0%{?fedora} > 27
%global system_libevent   1
%else
%global system_libevent     0
%endif

# Use system sqlite?
%if 0%{?fedora} > 27
%global system_sqlite     1
%else
%global system_sqlite     0
%endif
%global system_ffi        1

# Use system cairo?
%global system_cairo      0

# Use system graphite2/harfbuzz?
%if 0%{?fedora} > 27
%global system_harfbuzz   1
%else
%global system_harfbuzz   0
%endif

# Use system libvpx?
%global system_libvpx     1

# Use system libicu?
%if 0%{?fedora} > 27
%global system_libicu     0
%else
%global system_libicu     0
%endif

# Big endian platforms
%ifarch ppc64 s390x
# Javascript Intl API is not supported on big endian platforms right now:
# https://bugzilla.mozilla.org/show_bug.cgi?id=1322212
%global big_endian        1
%endif

# Hardened build?
%global hardened_build    1

%global system_jpeg       1

%ifarch %{ix86} x86_64
%global run_tests         0
%else
%global run_tests         0
%endif

# Build as a debug package?
%global debug_build       0

%global default_bookmarks_file  %{_datadir}/bookmarks/default-bookmarks.html
%global waterfox_app_id  \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
# Minimal required versions
%global cairo_version 1.13.1
%global freetype_version 2.1.9
%if %{?system_harfbuzz}
%global graphite2_version 1.3.10
%global harfbuzz_version 1.4.7
%endif
%if %{?system_libevent}
%global libevent_version 2.1.8
%endif
%global libnotify_version 0.7.0
%if %{?system_libvpx}
%global libvpx_version 1.4.0
%endif

%if %{?system_nss}
%global nspr_version 4.17.0
# NSS/NSPR quite often ends in build override, so as requirement the version
# we're building against could bring us some broken dependencies from time to time.
%global nspr_build_version %{nspr_version}
%global nss_version 3.34
%global nss_build_version %{nss_version}
%endif

%if %{?system_sqlite}
%global sqlite_version 3.8.4.2
# The actual sqlite version (see #480989):
%global sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo 65536)
%endif

%global mozappdir     %{_libdir}/%{name}
%global mozappdirdev  %{_libdir}/%{name}-devel-%{version}
%global langpackdir   %{mozappdir}/langpacks

%global build_langpacks         1

Summary:        Waterfox Web browser
Name:           waterfox
Version:        56.1.0
Release:        3%{?gver}%{?dist}
URL:            https://www.waterfoxproject.org
License:        MPLv1.1 or GPLv2+ or LGPLv2+
%if 0%{?with_snapshot}
Source0:        https://github.com/MrAlex94/%{name}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/MrAlex94/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

# FreeBSD patches
# https://www.freshports.org/www/waterfox
# rev=revision ./waterfox-FreeBSD-patches-snapshot.sh
Source600:      http://dl.bintray.com/phantomx/tarballs/%{name}-FreeBSD-patches-r%{freebsd_rev}.tar.xz

Source10:       waterfox-mozconfig
Source12:       waterfox-chinfo-default-prefs.js
Source20:       waterfox.desktop
Source21:       waterfox.sh.in
Source23:       waterfox.1
Source26:       distribution.ini

# Build patches
Patch0:         firefox-install-dir.patch
Patch3:         mozilla-build-arm.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=814879#c3
Patch18:        xulrunner-24.0-jemalloc-ppc.patch
Patch20:        firefox-build-prbool.patch
Patch25:        rhbz-1219542-s390-build.patch
Patch26:        build-icu-big-endian.patch
Patch27:        mozilla-1335250.patch
# Also fixes s390x: https://bugzilla.mozilla.org/show_bug.cgi?id=1376268
Patch29:        build-big-endian.patch
Patch30:        fedora-build.patch
Patch31:        build-ppc64-s390x-curl.patch
Patch32:        build-rust-ppc64le.patch
Patch35:        build-ppc-jit.patch
Patch36:        build-missing-xlocale-h.patch
# Always feel lucky for unsupported platforms:
# https://bugzilla.mozilla.org/show_bug.cgi?id=1347128
Patch37:        build-jit-atomic-always-lucky.patch
# Fixing missing cacheFlush when JS_CODEGEN_NONE is used (s390x)
Patch38:        build-cacheFlush-missing.patch

# Fedora specific patches
Patch215:        firefox-enable-addons.patch
Patch219:        rhbz-1173156.patch
Patch221:        firefox-fedora-ua.patch
Patch224:        mozilla-1170092.patch
Patch225:        mozilla-1005640-accept-lang.patch
#ARM run-time patch
Patch226:        rhbz-1354671.patch
Patch230:        rhbz-1497932.patch

# Firefox upstream patches
Patch402:        mozilla-1196777.patch
Patch406:        mozilla-256180.patch
Patch413:        mozilla-1353817.patch
Patch415:        mozilla-1405267.patch
Patch416:        mozilla-1435695.patch

# Upstream updates

%global wf_url https://github.com/MrAlex94/Waterfox/commit
#Patch490: %%{wf_url}/commit.patch#/wf-commit.patch

# Debian patches
Patch500:        mozilla-440908.patch

# Chinforinfula patches
Patch700:        %{name}-nolangpacks.patch
Patch701:        %{name}-waterfoxdir.patch

%if %{?system_nss}
BuildRequires:  pkgconfig(nspr) >= %{nspr_version}
BuildRequires:  pkgconfig(nss) >= %{nss_version}
BuildRequires:  nss-static >= %{nss_version}
%endif
%if %{?system_cairo}
BuildRequires:  pkgconfig(cairo) >= %{cairo_version}
%endif
BuildRequires:  pkgconfig(libpng)
%if %{?system_jpeg}
BuildRequires:  libjpeg-devel
%endif
BuildRequires:  zip
BuildRequires:  bzip2-devel
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libIDL-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(krb5)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(freetype2) >= %{freetype_version}
%if %{?system_harfbuzz}
BuildRequires:  pkgconfig(graphite2) >= %{graphite2_version}
BuildRequires:  pkgconfig(harfbuzz) >= %{harfbuzz_version}
%endif
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(xrender)
%if %{?system_hunspell}
BuildRequires:  pkgconfig(hunspell)
%endif
%if %{?system_libevent}
BuildRequires:  pkgconfig(libevent) >= %{libevent_version}
%endif
BuildRequires:  pkgconfig(libstartup-notification-1.0)
%if %{?alsa_backend}
BuildRequires:  pkgconfig(alsa)
%endif
BuildRequires:  pkgconfig(libnotify) >= %{libnotify_version}
BuildRequires:  pkgconfig(dri)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  dbus-glib-devel
BuildRequires:  pkgconfig(libv4l2)
%if %{?system_libvpx}
BuildRequires:  libvpx-devel >= %{libvpx_version}
%endif
BuildRequires:  autoconf213
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  yasm
BuildRequires:  llvm
BuildRequires:  llvm-devel
BuildRequires:  clang
BuildRequires:  clang-libs
BuildRequires:  gcc-c++

Requires:       mozilla-filesystem
Requires:       waterfox-filesystem
Requires:       p11-kit-trust
%if %{?system_nss}
Requires:       nspr >= %{nspr_build_version}
Requires:       nss >= %{nss_build_version}
%endif
BuildRequires:  python2-devel

BuildRequires:  nss-devel >= 3.29.1-2.1
Requires:       nss >= 3.29.1-2.1

BuildRequires:  desktop-file-utils
BuildRequires:  system-bookmarks
%if %{?system_sqlite}
BuildRequires:  pkgconfig(sqlite3) >= %{sqlite_version}
Requires:       sqlite >= %{sqlite_build_version}
%endif

%if %{?system_ffi}
BuildRequires:  pkgconfig(libffi)
%endif

%if %{?run_tests}
BuildRequires:  xorg-x11-server-Xvfb
%endif
BuildRequires:  rust
BuildRequires:  cargo

Obsoletes:      mozilla <= 37:1.7.13
Provides:       webclient

%description
Waterfox is an open-source web browser, specialised modification of the Mozilla
platform, designed for privacy and user choice in mind.

%if %{run_tests}
%global testsuite_pkg_name mozilla-%{name}-testresults
%package -n %{testsuite_pkg_name}
Summary: Results of testsuite
%description -n %{testsuite_pkg_name}
This package contains results of tests executed during build.
%files -n %{testsuite_pkg_name}
/test_results
%endif

#---------------------------------------------------------------------

%prep
%if 0%{?with_snapshot}
%setup -q -n Waterfox-%{commit} -a 600
%else
%setup -q -n Waterfox-%{version} -a 600
%endif

%if %{build_langpacks}
  mkdir waterfox-langpacks
  mv browser/extensions/langpack-*.xpi  waterfox-langpacks/
%else
  rm -f browser/extensions/langpack-*.xpi
%endif

# Build patches, can't change backup suffix from default because during build
# there is a compare of config and js/config directories and .orig suffix is
# ignored during this compare.
%patch0  -p1


%patch18 -p1 -b .jemalloc-ppc
%patch20 -p1 -b .prbool
%ifarch s390
%patch25 -p1 -b .rhbz-1219542-s390
%endif
%patch29 -p1 -b .big-endian
%patch30 -p1 -b .fedora-build
%patch31 -p1 -b .ppc64-s390x-curl
%patch32 -p1 -b .rust-ppc64le
%ifarch ppc ppc64 ppc64le
%patch35 -p1 -b .ppc-jit
%endif
%patch37 -p1 -b .jit-atomic-lucky

%patch3  -p1 -b .arm

# For branding specific patches.

# Fedora patches
%patch215 -p1 -b .addons
%patch219 -p2 -b .rhbz-1173156
%patch221 -p2 -b .fedora-ua
%patch224 -p1 -b .1170092
%patch225 -p1 -b .1005640-accept-lang
#ARM run-time patch
%ifarch aarch64
%patch226 -p1 -b .1354671
%endif
%patch230 -p1 -b .1497932

%patch402 -p1 -b .1196777
%patch406 -p1 -b .256180
%patch413 -p1 -b .1353817
%patch415 -p1 -b .1405267
%patch416 -p1 -b .1435695

#patch490 -p1

# Debian extension patch
%patch500 -p1 -b .440908

# Prepare FreeBSD patches
mkdir _temp
mv %{name}-FreeBSD-patches-r%{freebsd_rev}/patch-{bug*,typos,{a,z}-bug*} _temp/
rm -f %{name}-FreeBSD-patches-r%{freebsd_rev}/*

for i in \
  702179 991253 1021761 1144632 1288587 1341234 \
  1343147 1381761 1386371 \
  1404057 1404324 1404180 \
  1386887 1387811 1388744 1401992 1409680 1413143 \
  1434619 1440717 1444083 1405267 1447519
do
  rm -f _temp/patch-bug${i}
done

%if 0%{?fedora} < 28
  rm -f _temp/patch-bug730495
%endif

mv _temp/* %{name}-FreeBSD-patches-r%{freebsd_rev}/

patchcommand='patch -p0 -s -i'

for i in %{name}-FreeBSD-patches-r%{freebsd_rev}/patch-{a-*,bug{??????,???????},typos,z-*} ;do
  ${patchcommand} ${i}
done

# Install langpacks other way
%patch700 -p1 -b .nolangpacks
%patch701 -p1 -b .waterfoxdir

# Patch for big endian platforms only
%if 0%{?big_endian}
%patch26 -p1 -b .icu
%patch36 -p2 -b .xlocale
%endif

rm -f .mozconfig
cp %{SOURCE10} .mozconfig

%if %{?system_nss}
echo "ac_add_options --with-system-nspr" >> .mozconfig
echo "ac_add_options --with-system-nss" >> .mozconfig
%else
echo "ac_add_options --without-system-nspr" >> .mozconfig
echo "ac_add_options --without-system-nss" >> .mozconfig
%endif

%if %{?system_sqlite}
echo "ac_add_options --enable-system-sqlite" >> .mozconfig
%else
echo "ac_add_options --disable-system-sqlite" >> .mozconfig
%endif

%if %{?system_cairo}
echo "ac_add_options --enable-system-cairo" >> .mozconfig
%else
echo "ac_add_options --disable-system-cairo" >> .mozconfig
%endif

%if %{?system_harfbuzz}
echo "ac_add_options --enable-system-graphite2" >> .mozconfig
echo "ac_add_options --enable-system-harfbuzz" >> .mozconfig
%else
echo "ac_add_options --disable-system-graphite2" >> .mozconfig
echo "ac_add_options --disable-system-harfbuzz" >> .mozconfig
%endif

%if %{?system_ffi}
echo "ac_add_options --enable-system-ffi" >> .mozconfig
%endif

%ifarch %{arm}
echo "ac_add_options --disable-elf-hack" >> .mozconfig
%endif

%if %{?alsa_backend}
echo "ac_add_options --enable-alsa" >> .mozconfig
%endif

%if %{?system_hunspell}
echo "ac_add_options --enable-system-hunspell" >> .mozconfig
%else
echo "ac_add_options --disable-system-hunspell" >> .mozconfig
%endif

%if %{?system_libevent}
echo "ac_add_options --enable-system-libevent" >> .mozconfig
%else
echo "ac_add_options --disable-system-libevent" >> .mozconfig
%endif

%if %{?debug_build}
echo "ac_add_options --enable-debug" >> .mozconfig
echo "ac_add_options --disable-optimize" >> .mozconfig
%else
%global optimize_flags "none"
# Fedora 26 (gcc7) needs to disable default build flags (mozbz#1342344)
%ifnarch s390 s390x
%global optimize_flags "-g -O2"
%endif
%ifarch armv7hl
# ARMv7 need that (rhbz#1426850)
%global optimize_flags "-g -O2 -fno-schedule-insns"
%endif
%ifarch ppc64le aarch64
%global optimize_flags "-g -O2"
%endif
%if %{optimize_flags} != "none"
echo 'ac_add_options --enable-optimize=%{?optimize_flags}' >> .mozconfig
%else
echo 'ac_add_options --enable-optimize' >> .mozconfig
%endif
echo "ac_add_options --disable-debug" >> .mozconfig
%endif

# s390(x) fails to start with jemalloc enabled
%ifarch s390 s390x
echo "ac_add_options --disable-jemalloc" >> .mozconfig
%endif

%ifnarch %{ix86} x86_64
echo "ac_add_options --disable-webrtc" >> .mozconfig
%endif

%if %{?run_tests}
echo "ac_add_options --enable-tests" >> .mozconfig
%endif

%if !%{?system_jpeg}
echo "ac_add_options --without-system-jpeg" >> .mozconfig
%else
echo "ac_add_options --with-system-jpeg" >> .mozconfig
%endif

%if %{?system_libvpx}
echo "ac_add_options --with-system-libvpx" >> .mozconfig
%else
echo "ac_add_options --without-system-libvpx" >> .mozconfig
%endif

%if %{?system_libicu}
echo "ac_add_options --with-system-icu" >> .mozconfig
%else
echo "ac_add_options --without-system-icu" >> .mozconfig
%endif
%ifarch s390 s390x
echo "ac_add_options --disable-ion" >> .mozconfig
%endif


#---------------------------------------------------------------------

%build
%if %{?system_sqlite}
# Do not proceed with build if the sqlite require would be broken:
# make sure the minimum requirement is non-empty, ...
sqlite_version=$(expr "%{sqlite_version}" : '\([0-9]*\.\)[0-9]*\.') || exit 1
# ... and that major number of the computed build-time version matches:
case "%{sqlite_build_version}" in
  "$sqlite_version"*) ;;
  *) exit 1 ;;
esac
%endif

echo "Generate big endian version of config/external/icu/data/icud58l.dat"
%if 0%{?big_endian}
  ./mach python intl/icu_sources_data.py .
  ls -l config/external/icu/data
  rm -f config/external/icu/data/icudt*l.dat
%endif

# Update the various config.guess to upstream release for aarch64 support
find ./ -name config.guess -exec cp /usr/lib/rpm/config.guess {} ';'

# -fpermissive is needed to build with gcc 4.6+ which has become stricter
#
# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
# Disable C++ exceptions since Mozilla code is not exception-safe
#
MOZ_OPT_FLAGS=$(echo "%{optflags}" | %{__sed} -e 's/-Wall//')
#rhbz#1037063
# -Werror=format-security causes build failures when -Wno-format is explicitly given
# for some sources
# Explicitly force the hardening flags for Waterfox so it passes the checksec test;
# See also https://fedoraproject.org/wiki/Changes/Harden_All_Packages
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -Wformat-security -Wformat -Werror=format-security"
# Disable null pointer gcc6 optimization in gcc6 (rhbz#1328045)
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fno-delete-null-pointer-checks"
# Use hardened build?
%if %{?hardened_build}
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fPIC -Wl,-z,relro -Wl,-z,now"
%endif
%if %{?debug_build}
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-O2//')
%endif
%ifarch s390
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-g/-g1/')
# If MOZ_DEBUG_FLAGS is empty, waterfox's build will default it to "-g" which
# overrides the -g1 from line above and breaks building on s390
# (OOM when linking, rhbz#1238225)
export MOZ_DEBUG_FLAGS=" "
%endif
%ifarch s390 %{arm} ppc aarch64
MOZ_LINK_FLAGS="-Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
%endif
export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS
export LDFLAGS=$MOZ_LINK_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1
# On x86 architectures, Mozilla can build up to 4 jobs at once in parallel,
# however builds tend to fail on other arches when building in parallel.
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le aarch64
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
[ "$RPM_BUILD_NCPUS" -ge 8 ] && MOZ_SMP_FLAGS=-j8
%endif

make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS" MOZ_SERVICES_SYNC="1"

%if %{?run_tests}
%if %{?system_nss}
ln -s /usr/bin/certutil objdir/dist/bin/certutil
ln -s /usr/bin/pk12util objdir/dist/bin/pk12util

%endif
mkdir test_results
./mach --log-no-times check-spidermonkey &> test_results/check-spidermonkey || true
./mach --log-no-times check-spidermonkey &> test_results/check-spidermonkey-2nd-run || true
./mach --log-no-times cppunittest &> test_results/cppunittest || true
xvfb-run ./mach --log-no-times crashtest &> test_results/crashtest || true
./mach --log-no-times gtest &> test_results/gtest || true
xvfb-run ./mach --log-no-times jetpack-test &> test_results/jetpack-test || true
# not working right now ./mach marionette-test &> test_results/marionette-test || true
xvfb-run ./mach --log-no-times mochitest-a11y &> test_results/mochitest-a11y || true
xvfb-run ./mach --log-no-times mochitest-browser &> test_results/mochitest-browser || true
xvfb-run ./mach --log-no-times mochitest-chrome &> test_results/mochitest-chrome || true
xvfb-run ./mach --log-no-times mochitest-devtools &> test_results/mochitest-devtools || true
xvfb-run ./mach --log-no-times mochitest-plain &> test_results/mochitest-plain || true
xvfb-run ./mach --log-no-times reftest &> test_results/reftest || true
xvfb-run ./mach --log-no-times webapprt-test-chrome &> test_results/webapprt-test-chrome || true
xvfb-run ./mach --log-no-times webapprt-test-content &> test_results/webapprt-test-content || true
./mach --log-no-times webidl-parser-test &> test_results/webidl-parser-test || true
xvfb-run ./mach --log-no-times xpcshell-test &> test_results/xpcshell-test || true
%if %{?system_nss}
rm -f  objdir/dist/bin/certutil
rm -f  objdir/dist/bin/pk12util
%endif

%endif
#---------------------------------------------------------------------

%install

# set up our default bookmarks
cp -p %{default_bookmarks_file} objdir/dist/bin/browser/chrome/en-US/locale/browser/bookmarks.html

# Make sure locale works for langpacks
cat > objdir/dist/bin/browser/defaults/preferences/firefox-l10n.js << EOF
pref("general.useragent.locale", "chrome://global/locale/intl.properties");
EOF

DESTDIR=%{buildroot} make -C objdir install

mkdir -p %{buildroot}{%{_libdir},%{_bindir},%{_datadir}/applications}

desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE20}

# set up the waterfox start script
rm -rf %{buildroot}%{_bindir}/waterfox
cat %{SOURCE21} > %{buildroot}%{_bindir}/waterfox
chmod 755 %{buildroot}%{_bindir}/waterfox

install -p -D -m 644 %{SOURCE23} %{buildroot}%{_mandir}/man1/waterfox.1

rm -f %{buildroot}/%{mozappdir}/waterfox-config
rm -f %{buildroot}/%{mozappdir}/update-settings.ini

for s in 16 22 24 32 48 256; do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps
  cp -p browser/branding/unofficial/default${s}.png \
    %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/waterfox.png
done

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p %{buildroot}%{_datadir}/appdata
cat > %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<application>
  <id type="desktop">waterfox.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <description>
    <p>
      Bringing together all kinds of awesomeness to make browsing better for you.
      Get to your favorite sites quickly – even if you don’t remember the URLs.
      Type your term into the location bar (aka the Awesome Bar) and the autocomplete
      function will include possible matches from your browsing history, bookmarked
      sites and open tabs.
    </p>
    <!-- FIXME: Needs another couple of paragraphs -->
  </description>
  <url type="homepage">http://www.mozilla.org/</url>
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
   -->
</application>
EOF

echo > %{name}.lang
%if %{build_langpacks}
# Extract langpacks, make any mods needed, repack the langpack, and install it.
mkdir -p %{buildroot}%{langpackdir}
for langpack in `ls waterfox-langpacks/*.xpi`; do
  language=`basename $langpack .xpi | sed -e 's/^langpack-//' -e 's/@waterfox//'`
  extensionID=langpack-$language@waterfox
  mkdir -p $extensionID
  unzip -qq $langpack -d $extensionID
  find $extensionID -type f | xargs chmod 644

  cd $extensionID
  zip -qq -r9mX ../${extensionID}.xpi *
  cd -

  install -m 644 ${extensionID}.xpi %{buildroot}%{langpackdir}
  language=`echo $language | sed -e 's/-/_/g'`
  echo "%%lang($language) %{langpackdir}/${extensionID}.xpi" >> %{name}.lang
done
rm -rf waterfox-langpacks

# Install langpack workaround (see #707100, #821169)
function create_default_langpack() {
language_long=$1
language_short=$2
cd %{buildroot}%{langpackdir}
ln -s langpack-$language_long@waterfox.xpi langpack-$language_short@waterfox.xpi
cd -
echo "%%lang($language_short) %{langpackdir}/langpack-$language_short@waterfox.xpi" >> %{name}.lang
}

# Table of fallbacks for each language
create_default_langpack "bn-IN" "bn"
create_default_langpack "es-AR" "es"
create_default_langpack "fy-NL" "fy"
create_default_langpack "ga-IE" "ga"
create_default_langpack "gu-IN" "gu"
create_default_langpack "hi-IN" "hi"
create_default_langpack "hy-AM" "hy"
create_default_langpack "nb-NO" "nb"
create_default_langpack "nn-NO" "nn"
create_default_langpack "pa-IN" "pa"
create_default_langpack "pt-PT" "pt"
create_default_langpack "sv-SE" "sv"
create_default_langpack "zh-TW" "zh"
%endif # build_langpacks

mkdir -p %{buildroot}/%{mozappdir}/browser/features

mkdir -p %{buildroot}/%{mozappdir}/browser/defaults/preferences

# System config dir
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/pref

# System extensions
mkdir -p %{buildroot}%{_datadir}/waterfox/extensions/%{waterfox_app_id}
mkdir -p %{buildroot}%{_libdir}/waterfox/extensions/%{waterfox_app_id}

# Copy over the LICENSE
install -p -c -m 644 LICENSE %{buildroot}/%{mozappdir}

# Use the system hunspell dictionaries
rm -rf %{buildroot}%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell %{buildroot}%{mozappdir}/dictionaries

%if %{run_tests}
# Add debuginfo for crash-stats.mozilla.com
mkdir -p %{buildroot}/test_results
cp test_results/* %{buildroot}/test_results
%endif

# Default
cp %{SOURCE12} %{buildroot}%{mozappdir}/browser/defaults/preferences

# Add distribution.ini
mkdir -p %{buildroot}%{mozappdir}/distribution
cp %{SOURCE26} %{buildroot}%{mozappdir}/distribution

# Remove copied libraries to speed up build
rm -f %{buildroot}%{mozappdirdev}/sdk/lib/libmozjs.so
rm -f %{buildroot}%{mozappdirdev}/sdk/lib/libmozalloc.so
rm -f %{buildroot}%{mozappdirdev}/sdk/lib/libxul.so
#---------------------------------------------------------------------

# Moves defaults/preferences to browser/defaults/preferences
%pretrans -p <lua>
require 'posix'
require 'os'
if (posix.stat("%{mozappdir}/browser/defaults/preferences", "type") == "link") then
  posix.unlink("%{mozappdir}/browser/defaults/preferences")
  posix.mkdir("%{mozappdir}/browser/defaults/preferences")
  if (posix.stat("%{mozappdir}/defaults/preferences", "type") == "directory") then
    for i,filename in pairs(posix.dir("%{mozappdir}/defaults/preferences")) do
      os.rename("%{mozappdir}/defaults/preferences/"..filename, "%{mozappdir}/browser/defaults/preferences/"..filename)
    end
    f = io.open("%{mozappdir}/defaults/preferences/README","w")
    if f then
      f:write("Content of this directory has been moved to %{mozappdir}/browser/defaults/preferences.")
      f:close()
    end
  end
end


%preun
# is it a final removal?
if [ $1 -eq 0 ]; then
  rm -rf %{mozappdir}/components
  rm -rf %{langpackdir}
fi

%files -f %{name}.lang
%{_bindir}/waterfox
%{mozappdir}/waterfox
%{mozappdir}/waterfox-bin
%doc %{_mandir}/man1/*
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/*
%dir %{_datadir}/waterfox/extensions/*
%dir %{_libdir}/waterfox/extensions/*
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/*.desktop
%dir %{mozappdir}
%license %{mozappdir}/LICENSE
%{mozappdir}/browser/chrome
%{mozappdir}/browser/chrome.manifest
%{mozappdir}/browser/defaults/preferences/waterfox-chinfo-default-prefs.js
%{mozappdir}/browser/features
%{mozappdir}/distribution/distribution.ini
# That's Windows only
%ghost %{mozappdir}/browser/features/aushelper@mozilla.org.xpi
%attr(644, root, root) %{mozappdir}/browser/blocklist.xml
%dir %{mozappdir}/browser/extensions
%{mozappdir}/browser/extensions/*
%if %{build_langpacks}
%dir %{langpackdir}
%endif
%{mozappdir}/browser/omni.ja
%{mozappdir}/browser/icons
%{mozappdir}/chrome.manifest
%{mozappdir}/run-mozilla.sh
%{mozappdir}/application.ini
%exclude %{mozappdir}/removed-files
%{_datadir}/icons/hicolor/16x16/apps/waterfox.png
%{_datadir}/icons/hicolor/22x22/apps/waterfox.png
%{_datadir}/icons/hicolor/24x24/apps/waterfox.png
%{_datadir}/icons/hicolor/256x256/apps/waterfox.png
%{_datadir}/icons/hicolor/32x32/apps/waterfox.png
%{_datadir}/icons/hicolor/48x48/apps/waterfox.png
%{mozappdir}/*.so
%{mozappdir}/gtk2/*.so
%{mozappdir}/defaults/pref/channel-prefs.js
%{mozappdir}/dependentlibs.list
%{mozappdir}/dictionaries
%{mozappdir}/omni.ja
%{mozappdir}/platform.ini
%{mozappdir}/plugin-container
%{mozappdir}/gmp-clearkey
%{mozappdir}/fonts/EmojiOneMozilla.ttf
%if !%{?system_libicu}
%{mozappdir}/icudt*.dat
%endif
%if !%{?system_nss}
%{mozappdir}/libfreeblpriv3.chk
%{mozappdir}/libnssdbm3.chk
%{mozappdir}/libsoftokn3.chk
%exclude %{mozappdir}/libnssckbi.so
%endif

#---------------------------------------------------------------------

%changelog
* Thu Apr 19 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.1.0-3.20180419git8864091
- Apply most of FreeBSD backport patches
- Enable system libevent and harfbuzz

* Sat Apr 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.1.0-2.20180412gita52b5ea
- Build latest snapshot for servo fixes
- Drop unneeded patches
- gcc 8 fix

* Fri Apr 06 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.1.0-1
- 56.1.0

* Fri Feb 02 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.0.4-1
- 56.0.4

* Fri Jan 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.0.3-1
- 56.0.3

* Fri Jan 05 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.0.2-1
- 56.0.2
- Fix release tarball support
- Unused patches cleanup
- Fix man

* Wed Dec 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 56.0.1-4.20171213git388770f
- New patch to ~/.waterfox/{extensions,plugins} and /usr/share/waterfox
- R: waterfox-filesystem

* Tue Dec 26 2017 Phantom X <megaphantomx at bol dot com dot br> - 56.0.1-3.20171213git388770f
- New snapshot
- BR: libevent, disabled, needs new releases
- Patch to use ~/.waterfox/extensions

* Tue Dec 19 2017 Phantom X <megaphantomx at bol dot com dot br> - 56.0.1-2.20171213git7b7aa8b
- Fixes borrowed from FreeBSD
- Enable stylo
- Do not use api keys from Fedora Firefox package
- Build with gold

* Wed Dec 13 2017 Phantom X <megaphantomx at bol dot com dot br> - 56.0.1-1.20171213git7b7aa8b
- First spec, borrowed from Fedora Firefox
