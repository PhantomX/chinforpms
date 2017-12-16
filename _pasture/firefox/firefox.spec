%if 0%{?fedora} < 26
ExcludeArch: armv7hl
%endif

# Use ALSA backend?
%global alsa_backend      1

# Use system nspr/nss?
%global system_nss        1

# Use system hunspell?
%if 0%{?fedora} > 25
%global system_hunspell   1
%else
%global system_hunspell   0
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
%global firefox_app_id  \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
# Minimal required versions
%global cairo_version 1.13.1
%global freetype_version 2.1.9
%global libnotify_version 0.7.0
%if %{?system_libvpx}
%global libvpx_version 1.4.0
%endif

%if %{?system_nss}
%global nspr_version 4.10.10
# NSS/NSPR quite often ends in build override, so as requirement the version
# we're building against could bring us some broken dependencies from time to time.
#%global nspr_build_version %(pkg-config --silence-errors --modversion nspr 2>/dev/null || echo 65536)
%global nspr_build_version %{nspr_version}
%global nss_version 3.32.1
#%global nss_build_version %(pkg-config --silence-errors --modversion nss 2>/dev/null || echo 65536)
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

%global official_branding       1
%global build_langpacks         1

%global enable_mozilla_crashreporter       0
%if !%{debug_build}
%ifarch %{ix86} x86_64
%if 0%{?fedora} < 27
%global enable_mozilla_crashreporter       1
%endif
%endif
%endif

Summary:        Mozilla Firefox Web browser
Name:           firefox
Version:        56.0.2
Release:        1.chinfo%{?pre_tag}%{?dist}
URL:            https://www.mozilla.org/firefox/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Source0:        https://archive.mozilla.org/pub/firefox/releases/%{version}%{?pre_version}/source/firefox-%{version}%{?pre_version}.source.tar.xz
%if %{build_langpacks}
#global langpacks_ver #{version}#{?pre_version}-20170927
%global langpacks_ver 56.0-20170927
%global langpacks_hash e74d85410891b6faa388d37043d764a6c01a2c83479d9912aa3d0b23684ed66ca639eb3cdb579cafef6c3156b0d774a66987a605e0f9e25c2d4eed967ef7b627
Source1:        http://pkgs.fedoraproject.org/repo/pkgs/%{name}/%{name}-langpacks-%{langpacks_ver}.tar.xz/sha512/%{langpacks_hash}/%{name}-langpacks-%{langpacks_ver}.tar.xz
%endif

Source10:       firefox-mozconfig
Source12:       firefox-redhat-default-prefs.js
Source20:       firefox.desktop
Source21:       firefox.sh.in
Source23:       firefox.1
Source24:       mozilla-api-key
Source25:       firefox-symbolic.svg
Source26:       distribution.ini
Source27:       google-api-key

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
Patch34:        build-cubeb-pulse-arm.patch
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
Patch229:        firefox-nss-version.patch
Patch230:        rhbz-1497932.patch

# Upstream patches
Patch402:        mozilla-1196777.patch
Patch406:        mozilla-256180.patch
Patch407:        mozilla-1348576.patch
Patch410:        mozilla-1321521.patch
Patch411:        mozilla-1321521-2.patch
Patch412:        mozilla-1337988.patch
Patch413:        mozilla-1353817.patch
Patch415:        mozilla-1405267.patch

# Better compatibility with NSS sql database format, rhbz#1496563
Patch481:        sqlcompat-ff57-1-backport-730495

# Debian patches
Patch500:        mozilla-440908.patch

# OpenSUSE patches
# http://www.rosenauer.org/hg/mozilla/
Patch600:        http://www.rosenauer.org/hg/mozilla/raw-file/bfa8722a06ad/firefox-branded-icons.patch
Patch601:        http://www.rosenauer.org/hg/mozilla/raw-file/bfa8722a06ad/mozilla-nongnome-proxies.patch

# Chinforinfula patches
Patch700:        firefox-nosocial.patch

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
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(xrender)
%if %{?system_hunspell}
BuildRequires:  pkgconfig(hunspell)
%endif
BuildRequires:  pkgconfig(libstartup-notification-1.0)
%if %{?alsa_backend}
BuildRequires:  pkgconfig(alsa)
%endif
BuildRequires:  pkgconfig(libnotify) >= %{libnotify_version}
BuildRequires:  pkgconfig(dri)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  dbus-glib-devel
%if %{?system_libvpx}
BuildRequires:  libvpx-devel >= %{libvpx_version}
%endif
BuildRequires:  autoconf213
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(gconf-2.0)
BuildRequires:  yasm
BuildRequires:  llvm
BuildRequires:  llvm-devel
BuildRequires:  clang
BuildRequires:  clang-libs

Requires:       mozilla-filesystem
Requires:       p11-kit-trust
%if %{?system_nss}
Requires:       nspr >= %{nspr_build_version}
Requires:       nss >= %{nss_build_version}
%endif
BuildRequires:  python2-devel

%if 0%{?fedora} > 25
# For early testing of rhbz#1400293 mozbz#1324096 on F26 and Rawhide,
# temporarily require the specific NSS build with the backports.
# Can be removed after firefox is changed to require NSS 3.30.
BuildRequires:  nss-devel >= 3.29.1-2.1
Requires:       nss >= 3.29.1-2.1
%endif

%if 0%{?fedora} < 26
# Using Conflicts for p11-kit, not Requires, because on multi-arch
# systems p11-kit isn't yet available for secondary arches like
# p11-kit.i686 (fallback to libnssckbi.so from NSS).
# This build contains backports from p11-kit 0.23.4
Conflicts: p11-kit < 0.23.2-3
# Requires build with CKA_NSS_MOZILLA_CA_POLICY attribute
Requires: ca-certificates >= 2017.2.11-1.1
# Requires NSS build with backports from NSS 3.30
BuildRequires:  nss-devel >= 3.29.3-1.1
Requires:       nss >= 3.29.3-1.1
%endif

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
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

%if %{enable_mozilla_crashreporter}
%global moz_debug_prefix %{_prefix}/lib/debug
%global moz_debug_dir %{moz_debug_prefix}%{mozappdir}
%global uname_m %(uname -m)
%global symbols_file_name %{name}-%{version}.en-US.%{_os}-%{uname_m}.crashreporter-symbols.zip
%global symbols_file_path %{moz_debug_dir}/%{symbols_file_name}
%global _find_debuginfo_opts -p %{symbols_file_path} -o debugcrashreporter.list
%global crashreporter_pkg_name mozilla-crashreporter-%{name}-debuginfo
%package -n %{crashreporter_pkg_name}
Summary: Debugging symbols used by Mozilla's crash reporter servers
%description -n %{crashreporter_pkg_name}
This package provides debug information for Firefox, for use by
Mozilla's crash reporter servers.  If you are trying to locally
debug %{name}, you want to install %{name}-debuginfo instead.
%files -n %{crashreporter_pkg_name} -f debugcrashreporter.list
%endif

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
%setup -q

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
# don't need that %patch34 -p1 -b .cubeb-pulse-arm
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
%ifarch %{arm}
%if 0%{?fedora} < 26
# Workaround for mozbz#1337988
%patch412 -p1 -b .1337988
%endif
%endif
%patch413 -p1 -b .1353817
%patch415 -p1 -b .1405267

%if 0%{?fedora} > 27
%patch481 -p1 -b .sqlcompat-1
%endif

# Debian extension patch
%patch500 -p1 -b .440908

# More icons sizes
%patch600 -p1 -b .brandedicons
# Do not use gconf proxies if not running within Gnome
%patch601 -p1 -b .nognomeproxies

%patch700 -p1 -b .nosocial

# Patch for big endian platforms only
%if 0%{?big_endian}
%patch26 -p1 -b .icu
%patch36 -p2 -b .xlocale
%endif

rm -f .mozconfig
cp %{SOURCE10} .mozconfig
%if %{official_branding}
echo "ac_add_options --enable-official-branding" >> .mozconfig
%endif
cp %{SOURCE24} mozilla-api-key
cp %{SOURCE27} google-api-key

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

%if %{?debug_build}
echo "ac_add_options --enable-debug" >> .mozconfig
echo "ac_add_options --disable-optimize" >> .mozconfig
%else
%global optimize_flags "none"
# Fedora 26 (gcc7) needs to disable default build flags (mozbz#1342344)
%if 0%{?fedora} > 25
%ifnarch s390 s390x
%global optimize_flags "-g -O2"
%endif
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

%if !%{enable_mozilla_crashreporter}
echo "ac_add_options --disable-crashreporter" >> .mozconfig
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
# Explicitly force the hardening flags for Firefox so it passes the checksec test;
# See also https://fedoraproject.org/wiki/Changes/Harden_All_Packages
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -Wformat-security -Wformat -Werror=format-security"
%if 0%{?fedora} > 23
# Disable null pointer gcc6 optimization in gcc6 (rhbz#1328045)
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fno-delete-null-pointer-checks"
%endif
# Use hardened build?
%if %{?hardened_build}
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fPIC -Wl,-z,relro -Wl,-z,now"
%endif
%if %{?debug_build}
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-O2//')
%endif
%ifarch s390
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-g/-g1/')
# If MOZ_DEBUG_FLAGS is empty, firefox's build will default it to "-g" which
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

# create debuginfo for crash-stats.mozilla.com
%if %{enable_mozilla_crashreporter}
#cd %{moz_objdir}
make -C objdir buildsymbols
%endif

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

# set up the firefox start script
rm -rf %{buildroot}%{_bindir}/firefox
cat %{SOURCE21} > %{buildroot}%{_bindir}/firefox
chmod 755 %{buildroot}%{_bindir}/firefox

install -p -D -m 644 %{SOURCE23} %{buildroot}%{_mandir}/man1/firefox.1

rm -f %{buildroot}/%{mozappdir}/firefox-config
rm -f %{buildroot}/%{mozappdir}/update-settings.ini

for s in 16 22 24 32 48 256; do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps
    cp -p browser/branding/official/default${s}.png \
               %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/firefox.png
done

# Install hight contrast icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps
cp -p %{SOURCE25} \
           %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps

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
<!--
BugReportURL: https://bugzilla.mozilla.org/show_bug.cgi?id=1071061
SentUpstream: 2014-09-22
-->
<application>
  <id type="desktop">firefox.desktop</id>
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
  <screenshots>
    <screenshot type="default">https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/a.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/b.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/c.png</screenshot>
  </screenshots>
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
   -->
</application>
EOF

echo > %{name}.lang
%if %{build_langpacks}
# Extract langpacks, make any mods needed, repack the langpack, and install it.
mkdir -p %{buildroot}%{langpackdir}
%{__tar} xf %{SOURCE1}
for langpack in `ls firefox-langpacks/*.xpi`; do
  language=`basename $langpack .xpi`
  extensionID=langpack-$language@firefox.mozilla.org
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
rm -rf firefox-langpacks

# Install langpack workaround (see #707100, #821169)
function create_default_langpack() {
language_long=$1
language_short=$2
cd %{buildroot}%{langpackdir}
ln -s langpack-$language_long@firefox.mozilla.org.xpi langpack-$language_short@firefox.mozilla.org.xpi
cd -
echo "%%lang($language_short) %{langpackdir}/langpack-$language_short@firefox.mozilla.org.xpi" >> %{name}.lang
}

# Table of fallbacks for each language
# please file a bug at bugzilla.redhat.com if the assignment is incorrect
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


mkdir -p %{buildroot}/%{mozappdir}/browser/defaults/preferences

# System config dir
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/pref

# System extensions
mkdir -p %{buildroot}%{_datadir}/mozilla/extensions/%{firefox_app_id}
mkdir -p %{buildroot}%{_libdir}/mozilla/extensions/%{firefox_app_id}

# Copy over the LICENSE
install -p -c -m 644 LICENSE %{buildroot}/%{mozappdir}

# Use the system hunspell dictionaries
rm -rf ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell ${RPM_BUILD_ROOT}%{mozappdir}/dictionaries

# Enable crash reporter for Firefox application
%if %{enable_mozilla_crashreporter}
sed -i -e "s/\[Crash Reporter\]/[Crash Reporter]\nEnabled=1/" %{buildroot}/%{mozappdir}/application.ini
# Add debuginfo for crash-stats.mozilla.com
mkdir -p %{buildroot}/%{moz_debug_dir}
cp objdir/dist/%{symbols_file_name} %{buildroot}/%{moz_debug_dir}
%endif

%if %{run_tests}
# Add debuginfo for crash-stats.mozilla.com
mkdir -p %{buildroot}/test_results
cp test_results/* %{buildroot}/test_results
%endif

# Default
cp %{SOURCE12} ${RPM_BUILD_ROOT}%{mozappdir}/browser/defaults/preferences

# Add distribution.ini
mkdir -p ${RPM_BUILD_ROOT}%{mozappdir}/distribution
cp %{SOURCE26} ${RPM_BUILD_ROOT}%{mozappdir}/distribution

# Remove copied libraries to speed up build
rm -f ${RPM_BUILD_ROOT}%{mozappdirdev}/sdk/lib/libmozjs.so
rm -f ${RPM_BUILD_ROOT}%{mozappdirdev}/sdk/lib/libmozalloc.so
rm -f ${RPM_BUILD_ROOT}%{mozappdirdev}/sdk/lib/libxul.so
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
  rm -rf %{mozappdir}/extensions
  rm -rf %{mozappdir}/plugins
  rm -rf %{langpackdir}
fi

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%{_bindir}/firefox
%{mozappdir}/firefox
%{mozappdir}/firefox-bin
%doc %{_mandir}/man1/*
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/*
%dir %{_datadir}/mozilla/extensions/*
%dir %{_libdir}/mozilla/extensions/*
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/*.desktop
%dir %{mozappdir}
%license %{mozappdir}/LICENSE
%{mozappdir}/browser/chrome
%{mozappdir}/browser/chrome.manifest
%{mozappdir}/browser/defaults/preferences/firefox-redhat-default-prefs.js
%{mozappdir}/browser/features/*.xpi
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
%{mozappdir}/pingsender
%exclude %{mozappdir}/removed-files
%{_datadir}/icons/hicolor/16x16/apps/firefox.png
%{_datadir}/icons/hicolor/22x22/apps/firefox.png
%{_datadir}/icons/hicolor/24x24/apps/firefox.png
%{_datadir}/icons/hicolor/256x256/apps/firefox.png
%{_datadir}/icons/hicolor/32x32/apps/firefox.png
%{_datadir}/icons/hicolor/48x48/apps/firefox.png
%{_datadir}/icons/hicolor/symbolic/apps/firefox-symbolic.svg
%if %{enable_mozilla_crashreporter}
%{mozappdir}/crashreporter
%{mozappdir}/crashreporter.ini
%{mozappdir}/minidump-analyzer
%{mozappdir}/Throbber-small.gif
%{mozappdir}/browser/crashreporter-override.ini
%endif
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
* Thu Oct 26 2017 Phantom X <megaphantomx at bol dot com dot br> - 56.0.2-1.chinfo
- Update to 56.0.2
- OpenSUSE patches
- Disable SocialAPI

* Fri Oct 6 2017 Martin Stransky <stransky@redhat.com> - 56.0-5
- Enable Stylo again.

* Wed Oct 4 2017 Martin Stransky <stransky@redhat.com> - 56.0-4
- Fixed rhbz#1497932 - Plug-Ins for example flash fails
  because of unresolved symbols

* Fri Sep 29 2017 Martin Stransky <stransky@redhat.com> - 56.0-3
- Enabled second arches.

* Mon Sep 25 2017 Martin Stransky <stransky@redhat.com> - 56.0-2
- Update to 56.0 (B6)

* Fri Sep 15 2017 Martin Stransky <stransky@redhat.com> - 55.0.3-4
- Added switch to build mozbz#1399611 and disable it now
  for various regressions.

* Thu Sep 14 2017 Martin Stransky <stransky@redhat.com> - 55.0.3-3
- Added experimental patch for mozbz#1399611

* Thu Sep 14 2017 Ville Skyttä <ville.skytta@iki.fi> - 55.0.3-2
- Own the %%{_sysconfdir}/%%{name} dir

* Fri Sep  1 2017 Jan Horak <jhorak@redhat.com> - 55.0.3-1
- Update to 55.0.3

* Thu Aug 24 2017 Martin Stransky <stransky@redhat.com> - 55.0.2-3
- Enable to build with nspr-4.16.

* Wed Aug 23 2017 Martin Stransky <stransky@redhat.com> - 55.0.2-2
- Rebuilt to remove wrong dependency to nspr-4.16.

* Fri Aug 18 2017 Martin Stransky <stransky@redhat.com> - 55.0.2-1
- Updated to 55.0.2

* Mon Aug 14 2017 Jan Horak <jhorak@redhat.com> - 55.0.1-1
- Update to 55.0.1

* Fri Aug 11 2017 Jan Horak <jhorak@redhat.com> - 55.0-6
- Do not require nss and nspr which we build package against

* Tue Aug 8 2017 Martin Stransky <stransky@redhat.com> - 55.0-5
- Rebuild

* Mon Aug 7 2017 Martin Stransky <stransky@redhat.com> - 55.0-2
- Updated to 55.0 (B3)

* Wed Aug 2 2017 Martin Stransky <stransky@redhat.com> - 55.0-1
- Updated to 55.0 (B1)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 54.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Jan Horak <jhorak@redhat.com> - 54.0.1-1
- Update to 54.0.1

* Tue Jun 13 2017 Jan Horak <jhorak@redhat.com> - 54.0-2
- Update to 54.0 (B3)

* Thu Jun  8 2017 Jan Horak <jhorak@redhat.com> - 54.0-1
- Update to 54.0

* Wed May 31 2017 Jan Horak <jhorak@redhat.com> - 53.0.3-2
- Added patch for big endian platforms
- Do not restrict architectures in older Fedoras

* Fri May 26 2017 Jan Horak <jhorak@redhat.com> - 53.0.3-1
- Update to 53.0.3

* Wed May 24 2017 Martin Stransky <stransky@redhat.com> - 53.0.2-8
- Disabled Rust on ppc64 ppc64le s390x

* Wed May 24 2017 Martin Stransky <stransky@redhat.com> - 53.0.2-7
- Enabled aarch64 on all Fedoras
- Enabled Rust on all arches

* Wed May 24 2017 Martin Stransky <stransky@redhat.com> - 53.0.2-6
- Added aarch64 patch (mozbz#1353817)

* Tue May 16 2017 Martin Stransky <stransky@redhat.com> - 53.0.2-5
- Arm gcc6 build fix (mozbz#1337988)

* Fri May 12 2017 Martin Stransky <stransky@redhat.com> - 53.0.2-4
- Enabled rust on ix86

* Thu May 11 2017 Martin Stransky <stransky@redhat.com> - 53.0.2-3
- Enabled Rust on Arm builds

* Thu May 11 2017 Martin Stransky <stransky@redhat.com> - 53.0.2-2
- Enabled Arm builds

* Fri May  5 2017 Jan Horak <jhorak@redhat.com> - 53.0.2-1
- Update to 53.0.2
- Cannot use disable-skia for any architecture now

* Thu Apr 27 2017 Jan Horak <jhorak@redhat.com> - 53.0-4
- Added patch from rhbz#1400293

* Thu Apr 20 2017 Martin Stransky <stransky@redhat.com> - 53.0-3
- Enabled second arches

* Tue Apr 18 2017 Martin Stransky <stransky@redhat.com> - 53.0-2
- Disable system hunspell library when necessary

* Tue Apr 18 2017 Martin Stransky <stransky@redhat.com> - 53.0-1
- Updated to 53.0 (B6)

* Tue Apr 18 2017 Jan Horak <jhorak@redhat.com> - 52.0.2-3
- Do not use color management until it is fixed for some broken profiles,
  ie. don't set gfx.color_management.enablev4 to true (rhbz#1403970).
- Added distribution.ini file to fix mozbz#1354489

* Fri Mar 31 2017 Martin Stransky <stransky@redhat.com> - 52.0.2-2
- Added patch for mozbz#1348576 - enable e10s by default
- Added patch for mozbz#1158076 - enable dark theme by pref

* Wed Mar 29 2017 Jan Horak <jhorak@redhat.com> - 52.0.2-1
- Update to 52.0.2

* Mon Mar 27 2017 Martin Stransky <stransky@redhat.com> - 52.0-7
- Reverted mozbz#1158076 due to rhbz#1435964

* Wed Mar 22 2017 Martin Stransky <stransky@redhat.com> - 52.0-6
- Added fix for CVE-2017-5428
- Added fix for mozbz#1158076

* Mon Mar 13 2017 Martin Stransky <stransky@redhat.com> - 52.0-5
- Enable ALSA backend behind pref (rhbz#1431371)

* Fri Mar 10 2017 Martin Stransky <stransky@redhat.com> - 52.0-4
- Fixed e10s enablement (rhbz#1398717)

* Tue Mar  7 2017 Jan Horak <jhorak@redhat.com> - 52.0-3
- Added s390x to big endian platforms

* Tue Mar  7 2017 Jan Horak <jhorak@redhat.com> - 52.0-2
- Added fix for libicu on big endian platforms

* Fri Mar 3 2017 Martin Stransky <stransky@redhat.com> - 52.0-1
- Update to 52.0 (B2)

* Thu Mar 02 2017 Kai Engert <kaie@redhat.com> - 51.0.1-11
- Enable upstream fix for rhbz#1400293 mozbz#1324096 on F26 and Rawhide.
  Keep the old workaround on F24/F25, required base packages aren't
  available yet.

* Thu Mar 2 2017 Martin Stransky <stransky@redhat.com> - 51.0.1-10
- Test another ARMv7 build setup (rhbz#1426850)

* Mon Feb 27 2017 Martin Stransky <stransky@redhat.com> - 51.0.1-9
- Disabled ARMv7 due to build failures (rhbz#1426850)

* Mon Feb 27 2017 Martin Stransky <stransky@redhat.com> - 51.0.1-8
- Enabled ARMv7 (rhbz#1426850)

* Mon Feb 27 2017 Martin Stransky <stransky@redhat.com> - 51.0.1-7
- Added fix for rhbz#1414535

* Thu Feb 23 2017 Martin Stransky <stransky@redhat.com> - 51.0.1-6
- Added fix for mozbz#1321579

* Thu Feb 23 2017 Martin Stransky <stransky@redhat.com> - 51.0.1-5
- Disabled -O3 optimization on rawhide to make FF usable (rhbz#1422532)

* Wed Feb 15 2017 Jan Horak <jhorak@redhat.com> - 51.0.1-4
- Fixed bug 1421334 - translations for "New window"

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 51.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 25 2017 Jan Horak <jhorak@redhat.com> - 51.0.1-2
- Update to 51.0.1

* Tue Jan 24 2017 Martin Stransky <stransky@redhat.com> - 51.0-3
- Added fix for aarch64 crashes (rhbz#1354671)

* Thu Jan 19 2017 Martin Stransky <stransky@redhat.com> - 51.0-2
- Update to 51.0 (B2)

* Wed Jan 18 2017 Martin Stransky <stransky@redhat.com> - 51.0-1
- Update to 51.0 (B1)

* Tue Jan 17 2017 Jan Horak <jhorak@redhat.com> - 50.1.0-4
- Enable telemetry (rhbz#1412971)

* Mon Jan 16 2017 Martin Stransky <stransky@redhat.com> - 50.1.0-3
- Added patch for nss 3.28.1 (mozbz#1290037)

* Wed Dec 21 2016 Martin Stransky <stransky@redhat.com> - 50.1.0-2
- Enabled Mozilla crash reporter

* Tue Dec 13 2016 Martin Stransky <stransky@redhat.com> - 50.1.0-1
- Updated to 50.1.0

* Wed Nov 30 2016 Martin Stransky <stransky@redhat.com> - 50.0.2-2
- Added fix for "ABORT: X_ShmAttach: BadAccess" crashes
  (mozbz#1271100)

* Wed Nov 30 2016 Martin Stransky <stransky@redhat.com> - 50.0.2-1
- Update to latest upstream (50.0.2)

* Mon Nov 28 2016 Martin Stransky <stransky@redhat.com> - 50.0.1-1
- Update to latest upstream (50.0.1)

* Thu Nov 24 2016 Martin Stransky <stransky@redhat.com> - 50.0-2
- Rebase Gtk3 widget code to latest trunk to fix
  various rendering problems (rhbz#1397290)

* Thu Nov 10 2016 Martin Stransky <stransky@redhat.com> - 50.0-1
- Update to 50.0

* Mon Oct 31 2016 Jan Horak <jhorak@redhat.com> - 49.0.2-1
- Update to 49.0.2

* Mon Sep 26 2016 Jan Horak <jhorak@redhat.com> - 49.0-3
- Build with rust where possible
- Added fix for wrong accept-language headers when running with non-english locales

* Mon Sep 19 2016 Martin Stransky <stransky@redhat.com> - 49.0-2
- Update to Firefox 49 (B4)

* Tue Sep 6 2016 Martin Stransky <stransky@redhat.com> - 49.0-1
- Update to Firefox 49

* Mon Aug 22 2016 Jan Horak <jhorak@redhat.com> - 48.0.1-2
- Added translations for .desktop file actions

* Fri Aug 19 2016 Martin Stransky <stransky@redhat.com> - 48.0.1-1
- Update to 48.0.1
- Added fix for mozbz#1291700 - Since latest release NTLM/SPNEGO
  no longer works

* Wed Aug 17 2016 Martin Stransky <stransky@redhat.com> - 48.0-6
- Added patch for mozbz#1225044 - gtk3 rendering glitches

* Fri Jul 29 2016 Martin Stransky <stransky@redhat.com> - 48.0-5
- Added fix for mozbz#1250704 - tooltips text color
- Disable system sqlite on F23
- Package in-tree icu file

* Thu Jul 28 2016 Martin Stransky <stransky@redhat.com> - 48.0-4
- Enable dark themes by pref in about:config (Bug 1272332)
- Backported gtk3.20 upstream fixes

* Wed Jul 27 2016 Martin Stransky <stransky@redhat.com> - 48.0-3
- Updated to 48.0 (B2)

* Wed Jul 27 2016 Jan Horak <jhorak@redhat.com> - 48.0-2
- Negotiate authentication is made off the main thread again (mozbz#890908)
- Fixed default prerefences (rhbz#1349489)

* Tue Jul 26 2016 Martin Stransky <stransky@redhat.com> - 48.0-1
- Updated to 48.0

* Fri Jul 22 2016 Tom Callaway <spot@fedoraproject.org> - 47.0.1-3
- rebuild for libvpx 1.6.0

* Mon Jul 11 2016 Martin Stransky <stransky@redhat.com> - 47.0.1-2
- Added fix for mozbz#256180 - gmail paste issues

* Mon Jul 11 2016 Martin Stransky <stransky@redhat.com> - 47.0.1-1
- Updated to 47.0.1

* Wed Jun 22 2016 Martin Stransky <stransky@redhat.com> - 47.0-6
- Updated tooltip patch for 3.20

* Mon Jun  6 2016 Martin Stransky <stransky@redhat.com> - 47.0-4
- Updated to 47.0 (B3)
- Should fix rhbz#1338010 (rebuilt against new astronomy-bookmarks)

* Fri Jun  3 2016 Martin Stransky <stransky@redhat.com> - 47.0-3
- Updated to 47.0 (B2)

* Thu Jun  2 2016 Martin Stransky <stransky@redhat.com> - 47.0-2
- Updated to 47.0
- Backout of negotiate authentication patch

* Thu May 26 2016 Jan Horak <jhorak@redhat.com> - 46.0.1-9
- Negotiate authentication is made off the main thread (mozbz#890908)

* Mon May 23 2016 Martin Stransky <stransky@redhat.com> - 46.0.1-8
- Rebuilt for new bookmarks (rhbz#1338010)
- Fixed build issue in Gtk3.20 patch

* Fri May 20 2016 Martin Stransky <stransky@redhat.com> - 46.0.1-6
- Updated Gtk3.20 patch - fixed tooltips

* Thu May 19 2016 Martin Stransky <stransky@redhat.com> - 46.0.1-5
- Added a fix for mozbz#1245783 - gcc6.1 crashes in JIT

* Thu May 12 2016 Martin Stransky <stransky@redhat.com> - 46.0.1-4
- Added fix for rhbz#1332821 - Crash on "Select" in "Open with" dialog

* Tue May 10 2016 Martin Stransky <stransky@redhat.com> - 46.0.1-3
- Added patch for rhbz#1332875 - new Samba auth reponse

* Thu May 5 2016 Martin Stransky <stransky@redhat.com> - 46.0.1-2
- Disable dark theme until we support it correctly (mozbz#1216658)

* Tue May 3 2016 Martin Stransky <stransky@redhat.com> - 46.0.1-1
- Updated to 46.0.1

* Mon May 2 2016 Martin Stransky <stransky@redhat.com> - 46.0-6
- Removed gstreamer config as it's no longer used.
  See rhbz#1331496 for details.
- Updated Firefox project URL (rhbz#1329014)

* Thu Apr 28 2016 Martin Stransky <stransky@redhat.com> - 46.0-5
- Added fix for rhbz#1322626 - wrong focused window

* Wed Apr 27 2016 Martin Stransky <stransky@redhat.com> - 46.0-4
- Added fix for rhbz#1315225 - ppc64le/aarch64 build fixes

* Wed Apr 27 2016 Martin Stransky <stransky@redhat.com> - 46.0-3
- Fixed missing langpacks

* Tue Apr 26 2016 Martin Stransky <stransky@redhat.com> - 46.0-2
- Disabled system libicu on Fedora 22/23

* Mon Apr 25 2016 Martin Stransky <stransky@redhat.com> - 46.0-1
- Updated to 46.0 (B5)

* Thu Apr 21 2016 Martin Stransky <stransky@redhat.com> - 45.0.2-5
- Added patch for mozbz#1263145

* Wed Apr 20 2016 Martin Stransky <stransky@redhat.com> - 45.0.2-4
- Updated scrollbar code for Gtk 3.20

* Mon Apr 18 2016 Martin Stransky <stransky@redhat.com> - 45.0.2-2
- Disabled gcc6 null this optimization (rhbz#1328045)

* Mon Apr 11 2016 Martin Stransky <stransky@redhat.com> - 45.0.2-1
- New upstream (45.0.2)

* Tue Apr 5 2016 Martin Stransky <stransky@redhat.com> - 45.0.1-6
- Fixed rhbz#1322669 - Flash widgets are not displayed

* Tue Apr 5 2016 Martin Stransky <stransky@redhat.com> - 45.0.1-5
- Polished gcc6 patches

* Tue Mar 22 2016 Martin Stransky <stransky@redhat.com> - 45.0.1-4
- Fixed rhbz#1321355 - broken flash plugin
- Added /etc/firefox/pref dir for easy configuration

* Mon Mar 21 2016 Martin Stransky <stransky@redhat.com> - 45.0.1-3
- Provide system wide config dir (mozbz#1170092)
- Allow lock preferences from .js files (mozbz#440908)

* Mon Mar 21 2016 Martin Stransky <stransky@redhat.com> - 45.0.1-2
- Fixed rhbz#1293874 - use a Debian patch for disabled extension
  signing

* Wed Mar 16 2016 Martin Stransky <stransky@redhat.com> - 45.0.1-1
- Update to 45.0.1

* Tue Mar 15 2016 Martin Stransky <stransky@redhat.com> - 45.0-5
- Updated gtk3.20 patch

* Fri Mar 4 2016 Martin Stransky <stransky@redhat.com> - 45.0-4
- Update to 45.0 (B2)

* Thu Mar 3 2016 Martin Stransky <stransky@redhat.com> - 45.0-3
- Added run-time fix for JIT (mozbz#1253216)

* Wed Mar 2 2016 Martin Stransky <stransky@redhat.com> - 45.0-2
- Disabled system libvpx on Fedora 22 where is 1.3.0

* Wed Mar 2 2016 Martin Stransky <stransky@redhat.com> - 45.0-1
- Update to 45.0

* Thu Feb 11 2016 Martin Stransky <stransky@redhat.com> - 44.0.2-3
- Added patch for mozbz#1205199

* Thu Feb 11 2016 Martin Stransky <stransky@redhat.com> - 44.0.2-2
- Update to 44.0.2 (B3)

* Wed Feb 10 2016 Martin Stransky <stransky@redhat.com> - 44.0.2-1
- Update to 44.0.2 (B2)

* Mon Feb 8 2016 Martin Stransky <stransky@redhat.com> - 44.0.1-2
- Update to 44.0.1 (B2)

* Fri Feb 5 2016 Martin Stransky <stransky@redhat.com> - 44.0.1-1
- Update to 44.0.1

* Thu Feb  4 2016 Jan Horak <jhorak@redhat.com> - 44.0-6
- Workaround for crash when closing application chooser and Fedora 23
  (rhbz#1291190)

* Tue Feb 2 2016 Martin Stransky <stransky@redhat.com> - 44.0-5
- GCC 6.0 build patch
- Disabled mozilla crashreporter to catch Gtk3 crashes

* Mon Feb 1 2016 Martin Stransky <stransky@redhat.com> - 44.0-4
- Removed pulseaudio hard dependency (rhbz#1303620)

* Tue Jan 26 2016 Ralph Giles <giles@mozilla.com> - 44.0-3
- Medadata update, require pulseaudio

* Mon Jan 25 2016 Martin Stransky <stransky@redhat.com> - 44.0-2
- Update to 44.0 B3

* Thu Jan 21 2016 Jan Horak <jhorak@redhat.com> - 44.0-1
- Update to 44.0

* Thu Jan 14 2016 Martin Stransky <stransky@redhat.com> - 43.0.4-2
- Fixed the progress bar rendering

* Thu Jan 14 2016 Martin Stransky <stransky@redhat.com> - 43.0.4-1
- Update to 43.0.4

* Wed Jan 13 2016 Martin Stransky <stransky@redhat.com> - 43.0.3-5
- Updated progress bars rendering for Gtk 3.20

* Thu Jan 7 2016 Martin Stransky <stransky@redhat.com> - 43.0.3-4
- Added fix for mozbz#1234026 - crashes on XWayland

* Tue Jan 05 2016 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 43.0.3-3
- Fix build on AArch64.

* Mon Jan 4 2016 Martin Stransky <stransky@redhat.com> - 43.0.3-2
- Enabled Skia (rhbz#1282134)

