%global commit 8864e433baf07e995e7047e840d8f94d8f1b2496
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20191205
%global with_snapshot 0

%global branch classic

%global freebsd_rev 20191102
%global freebsd_root %{name}-FreeBSD-patches-%{freebsd_rev}

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

ExcludeArch: armv7hl

%global verbose_build     0
%if 0%{?verbose_build}
%global verbose_mach     -v
%endif

%global alsa_backend      1
%global system_nss        1
%global system_hunspell   1
%global system_libevent   1
%global system_sqlite     1
%global system_ffi        1
%global system_cairo      0
%global system_harfbuzz   1
# libvpx is too new for Waterfox 56
%if 0%{?fedora} < 30
%global system_libvpx     1
%else
%global system_libvpx     0
%endif
%global system_webp       1
%global system_libicu     0
%global system_jpeg       1

%global run_tests         0

%global hardened_build    1

%global build_with_clang  0
%ifnarch %{ix86} ppc64 s390x
%global build_with_pgo    1
%endif

%ifarch x86_64
%global build_with_lto    1
%endif

# Big endian platforms
%ifarch ppc64 s390x
%global big_endian        1
%endif

%if 0%{?build_with_pgo}
%global use_xvfb          1
%global build_tests       1
%endif

%if !0%{?run_tests}
%global use_xvfb          1
%global build_tests       1
%endif

%global debug_build       0

%global disable_elfhack   0

%global build_stylo       0
%global build_rust_simd   1
# Set to build with pinned rust version
# This enables stylo build when default rust version is not supported
# and a downgraded rust package exists
%global build_with_pinned_rust 0
%global rust_build_min_ver 1.35
%global rust_build_min_nover 1.38

%global default_bookmarks_file  %{_datadir}/bookmarks/default-bookmarks.html
%global waterfox_app_id  \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
# Minimal required versions
%global cairo_version 1.13.1
%global freetype_version 2.1.9
%if 0%{?system_harfbuzz}
%global graphite2_version 1.3.10
%global harfbuzz_version 1.4.7
%endif
%if 0%{?system_libevent}
%global libevent_version 2.1.8
%endif
%global libnotify_version 0.7.0
%if 0%{?system_libvpx}
%global libvpx_version 1.4.0
%endif
%if 0%{?system_webp}
%global webp_version 1.0.0
%endif

%if 0%{?system_nss}
%global nspr_version 4.17.0
# NSS/NSPR quite often ends in build override, so as requirement the version
# we're building against could bring us some broken dependencies from time to time.
%global nspr_build_version %{nspr_version}
%global nss_version 3.34
%global nss_build_version %{nss_version}
%endif

%if 0%{?system_sqlite}
%global sqlite_version 3.8.4.2
# The actual sqlite version (see #480989):
%global sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo 65536)
%endif

%if %{branch} == "classic"
%global channel Classic
%else
%global channel Current
%endif

%global mozappdir     %{_libdir}/%{name}
%global mozappdirdev  %{_libdir}/%{name}-devel-%{version}
%global langpackdir   %{mozappdir}/langpacks

%global build_langpacks         1

Summary:        Waterfox Web browser
Name:           waterfox
Version:        2019.12
Release:        1.%{branch}%{?gver}%{?dist}
URL:            https://www.waterfox.net
License:        MPLv1.1 or GPLv2+ or LGPLv2+

%global vc_url  https://github.com/MrAlex94/Waterfox
%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}-%{branch}/%{name}-%{version}-%{branch}.tar.gz
%endif

# FreeBSD patches
# https://www.freshports.org/www/waterfox
# rev=revision ./waterfox-FreeBSD-patches-snapshot.sh
# https://github.com/MrAlex94/Waterfox/issues/1220
Source600:      https://dl.bintray.com/phantomx/tarballs/%{freebsd_root}.tar.xz

Source10:       waterfox-mozconfig
Source12:       waterfox-chinfo-default-prefs.js
Source20:       waterfox.desktop
Source21:       waterfox.sh.in
Source23:       waterfox.1
Source26:       distribution.ini

# Build patches
Patch3:         mozilla-build-arm.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=814879#c3
Patch18:        xulrunner-24.0-jemalloc-ppc.patch
Patch20:        firefox-build-prbool.patch
Patch25:        rhbz-1219542-s390-build.patch
Patch26:        build-icu-big-endian.patch
Patch30:        fedora-build.patch
Patch31:        build-ppc64-s390x-curl.patch
Patch32:        build-rust-ppc64le.patch
Patch35:        build-ppc-jit.patch
Patch36:        build-missing-xlocale-h.patch
# Always feel lucky for unsupported platforms:
# https://bugzilla.mozilla.org/show_bug.cgi?id=1347128
Patch37:        build-jit-atomic-always-lucky.patch
Patch39:        mozilla-1494037.patch

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
Patch415:        Bug-1238661---fix-mozillaSignalTrampoline-to-work-.patch
Patch416:        bug1375074-save-restore-x28.patch
Patch417:        mozilla-1436242.patch
Patch418:        https://hg.mozilla.org/integration/autoland/raw-rev/342812d23eb9#/mozilla-1336978.patch
Patch419:        https://hg.mozilla.org/mozilla-central/raw-rev/4723934741c5#/mozilla-1320560.patch
Patch420:        https://hg.mozilla.org/mozilla-central/raw-rev/97dae871389b#/mozilla-1389436.patch

# Upstream updates/PRs/Reverts

#Patch???:      %%{vc_url}/commit/commit.patch#/%%{name}-gh-commit.patch

# Debian patches
Patch500:        mozilla-440908.patch

# PGO/LTO patches
Patch600:        pgo.patch
Patch601:        mozilla-1516081.patch
Patch602:        mozilla-1516803.patch
Patch603:        mozilla-1397365-5.patch
Patch604:        1003_gentoo_specific_pgo.patch

# Chinforinfula patches
Patch700:        %{name}-nolangpacks.patch
# https://github.com/MrAlex94/Waterfox/pull/547.patch, down
Patch701:        %{name}-waterfoxdir-1.patch
Patch702:        %{name}-waterfoxdir-2.patch
Patch703:        %{name}-fix-testing-file.patch

%if 0%{?system_nss}
BuildRequires:  pkgconfig(nspr) >= %{nspr_version}
BuildRequires:  pkgconfig(nss) >= %{nss_version}
BuildRequires:  nss-static >= %{nss_version}
%endif
%if 0%{?system_cairo}
BuildRequires:  pkgconfig(cairo) >= %{cairo_version}
%endif
BuildRequires:  pkgconfig(libpng)
%if 0%{?system_jpeg}
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
%if 0%{?system_harfbuzz}
BuildRequires:  pkgconfig(graphite2) >= %{graphite2_version}
BuildRequires:  pkgconfig(harfbuzz) >= %{harfbuzz_version}
%endif
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(xrender)
%if 0%{?system_hunspell}
BuildRequires:  pkgconfig(hunspell)
%endif
%if 0%{?system_libevent}
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
%if 0%{?system_libvpx}
BuildRequires:  pkgconfig(vpx) >= %{libvpx_version}
%endif
%if 0%{?system_webp}
BuildRequires:  pkgconfig(libwebp) >= %{webp_version}
%endif
BuildRequires:  autoconf213
BuildRequires:  pkgconfig(libpulse)
%if 0%{?system_libicu}
BuildRequires:  pkgconfig(icu-i18n)
%endif
BuildRequires:  yasm
BuildRequires:  llvm
BuildRequires:  llvm-devel
# clang is needed even with gcc
BuildRequires:  clang
BuildRequires:  clang-devel
%if 0%{?build_with_clang}
BuildRequires:  lld
BuildRequires:  libstdc++-static
%if 0%{?build_with_pgo}
BuildRequires:  compiler-rt
%endif
%else
%if 0%{?fedora} > 30
BuildRequires:  binutils-gold
%endif
BuildRequires:  gcc-c++
%endif
BuildRequires:  bash
BuildRequires:  patchutils

Requires:       mozilla-filesystem
Requires:       waterfox-filesystem
Requires:       p11-kit-trust
%if 0%{?system_nss}
Requires:       nspr >= %{nspr_build_version}
Requires:       nss >= %{nss_build_version}
%endif
BuildRequires:  perl-interpreter
BuildRequires:  python2-devel
Requires:       u2f-hidraw-policy

BuildRequires:  nss-devel >= 3.29.1-2.1
Requires:       nss >= 3.29.1-2.1

BuildRequires:  desktop-file-utils
BuildRequires:  system-bookmarks
%if 0%{?system_sqlite}
BuildRequires:  pkgconfig(sqlite3) >= %{sqlite_version}
Requires:       sqlite >= %{sqlite_build_version}
%endif

%if 0%{?system_ffi}
BuildRequires:  pkgconfig(libffi)
%endif

%if 0%{?use_xvfb}
BuildRequires:  xorg-x11-server-Xvfb
%endif
%if 0%{?build_with_pgo} || !0%{?run_tests}
BuildRequires:  librsvg2
%endif
%if 0%{?build_with_pinned_rust}
BuildRequires:  (rust >= %{rust_build_min_ver} with rust < %{rust_build_min_nover})
BuildRequires:  (cargo >= %{rust_build_min_ver} with cargo < %{rust_build_min_nover})
%else
BuildRequires:  rust
BuildRequires:  cargo
%endif

Obsoletes:      mozilla <= 37:1.7.13
Provides:       webclient

%description
Waterfox is an open-source web browser, specialised modification of the Mozilla
platform, designed for privacy and user choice in mind.

%if %{run_tests}
%global testsuite_pkg_name %{name}-testresults
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
%setup -q -n Waterfox-%{version}-%{branch} -a 600
%endif

%if %{build_langpacks}
  mkdir waterfox-langpacks
  mv browser/extensions/langpack-*.xpi  waterfox-langpacks/
%else
  rm -f browser/extensions/langpack-*.xpi
%endif

%patch18 -p1 -b .jemalloc-ppc
%patch20 -p1 -b .prbool
%ifarch s390
%patch25 -p1 -b .rhbz-1219542-s390
%endif
%patch30 -p1 -b .fedora-build
%patch31 -p1 -b .ppc64-s390x-curl
%patch32 -p1 -b .rust-ppc64le
%ifarch ppc ppc64 ppc64le
%patch35 -p1 -b .ppc-jit
%endif
%patch37 -p1 -b .jit-atomic-lucky
%patch39 -p1 -b .1494037

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
%ifarch %{arm}
%patch415 -p1 -b .mozilla-1238661
%endif
%patch416 -p1 -b .bug1375074-save-restore-x28
%patch417 -p1 -b .mozilla-1436242
%patch418 -p1 -b .mozilla-1336978
%patch419 -p1 -b .mozilla-1320560
%patch420 -p1 -b .mozilla-1389436

# Debian extension patch
%patch500 -p1 -b .440908

# PGO patches
%patch600 -p1 -b .pgo
%patch601 -p1 -b .1516081
%patch602 -p1 -b .1516803
%patch603 -p1 -b .1397365
%patch604 -p1 -b .gentoo_pgo

# Prepare FreeBSD patches
mkdir _patches
cp -p %{freebsd_root}/patch-{bug,z-bug,revert-bug}* _patches/

filterdiff -x dom/svg/crashtests/crashtests.list %{freebsd_root}/patch-bug1343147 \
  > _patches/patch-bug1343147
filterdiff -x dom/security/test/csp/mochitest.ini %{freebsd_root}/patch-bug1381761 \
  > _patches/patch-bug1381761
  
for i in 1404057 1404324 1404180 1405878 ;do
  filterdiff \
    -x layout/style/crashtests/crashtests.list \
    -x layout/reftests/bugs/reftest.list \
    %{freebsd_root}/patch-bug${i} > _patches/patch-bug${i}
done

# 1: unneeded
# 2: no apply
# 3: uncertain
for i in \
  702179 991253 1021761 1144632 1288587 1379148 1393235 1393283 1395486 1433747 1452576 1453127 1466606 \
  1384121 1388744 1413143 \
  1447519
do
  rm -f _patches/patch-bug${i}
done

patchcommand='patch -p0 -s -i'

for i in _patches/patch-{bug{??????,???????},revert-bug*,z-*} ;do
  ${patchcommand} ${i}
done

# Install langpacks other way
%patch700 -p1 -b .nolangpacks
%patch701 -p1 -b .waterfoxdir-1
%patch702 -p1 -b .waterfoxdir-2
%patch703 -p1 -b .fix-testing-file

# Patch for big endian platforms only
%if 0%{?big_endian}
%patch26 -p1 -b .icu
%patch36 -p2 -b .xlocale
%endif

cp %{SOURCE26} .
sed -e 's|_BRANCH_|%{channel}|g' -i distribution.ini

rm -f .mozconfig
cp %{SOURCE10} .mozconfig

echo "ac_add_options --prefix=\"%{_prefix}\"" >> .mozconfig
echo "ac_add_options --libdir=\"%{_libdir}\"" >> .mozconfig

%if 0%{?build_with_pgo}
echo "mk_add_options MOZ_PGO=1" >> .mozconfig
echo "mk_add_options PROFILE_GEN_SCRIPT='EXTRA_TEST_ARGS=10 \$(MAKE) -C \$(MOZ_OBJDIR) pgo-profile-run'" >> .mozconfig
%endif

%if 0%{?system_nss}
echo "ac_add_options --with-system-nspr" >> .mozconfig
echo "ac_add_options --with-system-nss" >> .mozconfig
%else
echo "ac_add_options --without-system-nspr" >> .mozconfig
echo "ac_add_options --without-system-nss" >> .mozconfig
%endif

%if 0%{?system_sqlite}
echo "ac_add_options --enable-system-sqlite" >> .mozconfig
%else
echo "ac_add_options --disable-system-sqlite" >> .mozconfig
%endif

%if 0%{?system_cairo}
echo "ac_add_options --enable-system-cairo" >> .mozconfig
%else
echo "ac_add_options --disable-system-cairo" >> .mozconfig
%endif

%if 0%{?system_harfbuzz}
echo "ac_add_options --enable-system-graphite2" >> .mozconfig
echo "ac_add_options --enable-system-harfbuzz" >> .mozconfig
%else
echo "ac_add_options --disable-system-graphite2" >> .mozconfig
echo "ac_add_options --disable-system-harfbuzz" >> .mozconfig
%endif

%if 0%{?system_ffi}
echo "ac_add_options --enable-system-ffi" >> .mozconfig
%endif

%ifarch %{arm}
echo "ac_add_options --disable-elf-hack" >> .mozconfig
%endif

%if 0%{?disable_elfhack}
echo "ac_add_options --disable-elf-hack" >> .mozconfig
%endif

%if %{?alsa_backend}
echo "ac_add_options --enable-alsa" >> .mozconfig
%endif

%if 0%{?system_hunspell}
echo "ac_add_options --enable-system-hunspell" >> .mozconfig
%else
echo "ac_add_options --disable-system-hunspell" >> .mozconfig
%endif

%if 0%{?system_libevent}
echo "ac_add_options --enable-system-libevent" >> .mozconfig
%else
echo "ac_add_options --disable-system-libevent" >> .mozconfig
%endif

%if 0%{?debug_build}
echo "ac_add_options --enable-debug" >> .mozconfig
echo "ac_add_options --disable-optimize" >> .mozconfig
%else
%global optimize_flags "none"
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

%if %{?build_tests}
echo "ac_add_options --enable-tests" >> .mozconfig
%else
echo "ac_add_options --disable-tests" >> .mozconfig
%endif

%if !0%{?system_jpeg}
echo "ac_add_options --without-system-jpeg" >> .mozconfig
%else
echo "ac_add_options --with-system-jpeg" >> .mozconfig
%endif

%if 0%{?system_libvpx}
echo "ac_add_options --with-system-libvpx" >> .mozconfig
%else
echo "ac_add_options --without-system-libvpx" >> .mozconfig
%endif

%if 0%{?system_webp}
echo "ac_add_options --with-system-webp" >> .mozconfig
%else
echo "ac_add_options --without-system-webp" >> .mozconfig
%endif

%if 0%{?system_libicu}
echo "ac_add_options --with-system-icu" >> .mozconfig
%else
echo "ac_add_options --without-system-icu" >> .mozconfig
%endif
%ifarch s390 s390x
echo "ac_add_options --disable-ion" >> .mozconfig
%endif

%if 0%{?build_stylo}
echo "ac_add_options --enable-stylo=build" >> .mozconfig
%else
echo "ac_add_options --disable-stylo" >> .mozconfig
%endif

%if 0%{?build_rust_simd}
echo "ac_add_options --enable-rust-simd" >> .mozconfig
%else
echo "ac_add_options --disable-rust-simd" >> .mozconfig
%endif

# Remove executable bit to make brp-mangle-shebangs happy.
chmod -x third_party/rust/itertools/src/lib.rs


#---------------------------------------------------------------------

%build
%if 0%{?system_sqlite}
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

RPM_SMP_MFLAGS_NCPUS=%(echo %{_smp_mflags} | sed 's|-j||')

RPM_NCPUS=1
# On x86 architectures, Mozilla can build up to 4 jobs at once in parallel,
# however builds tend to fail on other arches when building in parallel.
%ifarch %{ix86}
[ "$RPM_SMP_MFLAGS_NCPUS" -ge 2 ] && RPM_NCPUS=2
%endif
%ifarch x86_64 ppc ppc64 ppc64le aarch64
[ "$RPM_SMP_MFLAGS_NCPUS" -ge 2 ] && RPM_NCPUS=2
[ "$RPM_SMP_MFLAGS_NCPUS" -ge 4 ] && RPM_NCPUS=4
[ "$RPM_SMP_MFLAGS_NCPUS" -ge 8 ] && RPM_NCPUS=8
%endif
MOZ_SMP_FLAGS=-j$RPM_NCPUS

%if 0%{?build_with_clang}
echo "ac_add_options --enable-linker=lld" >> .mozconfig
MOZ_OPT_FLAGS="-fuse-ld=lld"
%else
%ifarch %{ix86} x86_64 %{arm}
echo "ac_add_options --enable-linker=gold" >> .mozconfig
MOZ_OPT_FLAGS="-fuse-ld=gold"
%endif
%endif

MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS $(echo "%{optflags}" | sed -e 's/-Wall//')"
#rhbz#1037063
# -Werror=format-security causes build failures when -Wno-format is explicitly given
# for some sources
# Explicitly force the hardening flags for Waterfox so it passes the checksec test;
# See also https://fedoraproject.org/wiki/Changes/Harden_All_Packages
%if 0%{?fedora} < 30
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -Wformat-security -Wformat -Werror=format-security"
%else
# Workaround for mozbz#1531309
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | sed -e 's/-Werror=format-security//')
%endif
%if 0%{?fedora} > 30
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fpermissive"
%endif
%if 0%{?build_with_clang}
# Fedora's default compiler flags conflict with what clang supports
MOZ_OPT_FLAGS="$(echo "$MOZ_OPT_FLAGS" | sed -e 's/-fstack-clash-protection//')"
%else
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -Wno-error=alloc-size-larger-than= -Wno-error=free-nonheap-object"
%endif
%if %{?hardened_build}
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fPIC -Wl,-z,relro -Wl,-z,now"
%endif
%if 0%{?debug_build}
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | sed -e 's/-O2//' -e 's/-O3//')
%else
export MOZ_DEBUG_FLAGS=" "
%endif
%if 0%{?build_with_lto}
MOZ_OPT_FLAGS="$(echo "$MOZ_OPT_FLAGS" | sed -e 's/-O2/-O3/' -e 's/ -g\b/ -g1/')"
%if 0%{?build_with_clang}
RPM_FLTO_FLAGS="-flto=thin -Wl,--thinlto-jobs=$RPM_NCPUS"
%else
RPM_FLTO_FLAGS="-flto=$RPM_NCPUS -fuse-linker-plugin -flifetime-dse=1"
%endif
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS $RPM_FLTO_FLAGS"
MOZ_LINK_FLAGS="$MOZ_OPT_FLAGS"
%endif
%ifarch s390
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | sed -e 's/ -g\b/ -g1/')
# If MOZ_DEBUG_FLAGS is empty, waterfox's build will default it to "-g" which
# overrides the -g1 from line above and breaks building on s390
# (OOM when linking, rhbz#1238225)
export MOZ_DEBUG_FLAGS=" "
%endif
%ifarch %{arm} %{ix86}
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | sed -e 's/ -g\b/-g0 /')
export MOZ_DEBUG_FLAGS=" "
%endif
%if !0%{?build_with_clang}
%ifarch s390 ppc aarch64 %{ix86}
MOZ_LINK_FLAGS="-Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
%endif
%ifarch %{arm}
MOZ_LINK_FLAGS="-Wl,--no-keep-memory"
%endif
%endif

%ifarch %{arm} %{ix86}
echo "export RUSTFLAGS=\"-Cdebuginfo=0"\" >> .mozconfig
%endif

%if 0%{?build_with_clang}
echo "export LLVM_PROFDATA=\"llvm-profdata"\" >> .mozconfig
echo "export CC=clang" >> .mozconfig
echo "export CXX=clang++" >> .mozconfig
echo "export AR=\"llvm-ar\"" >> .mozconfig
echo "export NM=\"llvm-nm\"" >> .mozconfig
echo "export RANLIB=\"llvm-ranlib\"" >> .mozconfig
%else
echo "export CC=gcc" >> .mozconfig
echo "export CXX=g++" >> .mozconfig
echo "export AR=\"gcc-ar\"" >> .mozconfig
echo "export NM=\"gcc-nm\"" >> .mozconfig
echo "export RANLIB=\"gcc-ranlib\"" >> .mozconfig
%endif

echo "export CFLAGS=\"$MOZ_OPT_FLAGS\"" >> .mozconfig
echo "export CXXFLAGS=\"$MOZ_OPT_FLAGS\"" >> .mozconfig
echo "export LDFLAGS=\"$MOZ_LINK_FLAGS\"" >> .mozconfig

echo "export MOZ_MAKE_FLAGS=\"$MOZ_SMP_FLAGS\"" >> .mozconfig
echo "export MOZ_SERVICES_SYNC=1" >> .mozconfig
echo "export MOZ_NOSPAM=1" >> .mozconfig
echo "export STRIP=%{_prefix}/bin/true" >> .mozconfig

%if 0%{?build_with_lto}
TMPDIR="$(pwd)/tmpdir"
echo "export TMPDIR=\"$TMPDIR\"" >> .mozconfig
mkdir -p "$TMPDIR"
%endif

%if 0%{?build_with_pgo}
SHELL=%{_prefix}/bin/bash GDK_BACKEND=x11 xvfb-run ./mach build %{?verbose_mach}
%else
SHELL=%{_prefix}/bin/bash ./mach build %{?verbose_mach}
%endif

%if %{?run_tests}
%if 0%{?system_nss}
ln -s %{_prefix}/bin/certutil objdir/dist/bin/certutil
ln -s %{_prefix}/bin/pk12util objdir/dist/bin/pk12util

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
%if 0%{?system_nss}
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

DESTDIR=%{buildroot} SHELL=/usr/bin/bash MOZ_NOSPAM=1 make -C objdir install

mkdir -p %{buildroot}{%{_libdir},%{_bindir},%{_datadir}/applications}

desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE20}

# set up the waterfox start script
rm -rf %{buildroot}%{_bindir}/%{name}
sed -e 's,/__PREFIX__,%{_prefix},g' %{SOURCE21} \
  > %{buildroot}%{_bindir}/%{name}
chmod 755 %{buildroot}%{_bindir}/%{name}

install -p -D -m 644 %{SOURCE23} %{buildroot}%{_mandir}/man1/%{name}.1

rm -f %{buildroot}/%{mozappdir}/waterfox-config
rm -f %{buildroot}/%{mozappdir}/update-settings.ini

for s in 16 22 24 32 48 64 128 256; do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps
  cp -p browser/branding/unofficial/default${s}.png \
    %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/%{name}.png
done

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p %{buildroot}%{_metainfodir}
cat > %{buildroot}%{_metainfodir}/%{name}.appdata.xml <<EOF
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
  <url type="homepage">https://www.waterfox.net/</url>
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
%endif

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
cp distribution.ini %{buildroot}%{mozappdir}/distribution

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
%{_bindir}/%{name}
%{mozappdir}/%{name}
%{mozappdir}/%{name}-bin
%doc %{_mandir}/man1/*
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/*
%dir %{_datadir}/%{name}/extensions/*
%dir %{_libdir}/%{name}/extensions/*
%{_metainfodir}/*.appdata.xml
%{_datadir}/applications/*.desktop
%dir %{mozappdir}
%license %{mozappdir}/LICENSE
%{mozappdir}/browser/chrome
%{mozappdir}/browser/chrome.manifest
%{mozappdir}/browser/defaults/preferences/*-default-prefs.js
%{mozappdir}/browser/features
%{mozappdir}/distribution/distribution.ini
# That's Windows only
%ghost %{mozappdir}/browser/features/aushelper@mozilla.org.xpi
%attr(644, root, root) %{mozappdir}/browser/blocklist.xml
%attr(644, root, root) %{mozappdir}/browser/ua-update.json
%dir %{mozappdir}/browser/extensions
%{mozappdir}/browser/extensions/*
%if %{build_langpacks}
%dir %{langpackdir}
%endif
%{mozappdir}/browser/omni.ja
%{mozappdir}/chrome.manifest
%{mozappdir}/run-mozilla.sh
%{mozappdir}/application.ini
%exclude %{mozappdir}/removed-files
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{mozappdir}/*.so
%{mozappdir}/gtk2/*.so
%{mozappdir}/defaults/pref/channel-prefs.js
%{mozappdir}/dependentlibs.list
%{mozappdir}/dictionaries
%{mozappdir}/omni.ja
%{mozappdir}/platform.ini
%{mozappdir}/plugin-container
%{mozappdir}/gmp-clearkey
%{mozappdir}/fonts/TwemojiMozilla.ttf
%if !0%{?system_libicu}
%{mozappdir}/icudt*.dat
%endif
%if !0%{?system_nss}
%{mozappdir}/libfreeblpriv3.chk
%{mozappdir}/libnssdbm3.chk
%{mozappdir}/libsoftokn3.chk
%exclude %{mozappdir}/libnssckbi.so
%endif

#---------------------------------------------------------------------

%changelog
* Tue Dec 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 2019.12-1.classic
- 2019.12
- Disable broken lto for the time
- Update FreeBSD patches. No system ogg/vorbis anymore

* Thu Oct 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 2019.10-4.classic.20191020gitf80144e
- New snapshot
- Add channel to distribution.ini

* Thu Oct 17 2019 Phantom X <megaphantomx at bol dot com dot br> - 2019.10-3.classic.20191016git68014c0
- PR to restore user-agent overrides

* Wed Oct 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 2019.10-2.classic.20191016git68014c0
- Try to fix crash with LTO, reverting some commits

* Wed Oct 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 2019.10-1.classic
- 2019.10-classic
- Enable av1
- Disable stylo, rust 1.38 build error

* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 56.2.14-2.20190916gitd516ab7
- New snapshot

* Wed Sep 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 56.2.14-1
- 5.2.14

* Mon Aug 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 56.2.13-1.20190709gitdc34e4b
- New release/snapshot

* Wed Jul 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 56.2.12-1.20190709git1bc2fb6
- New release/snapshot
- Fix URL
- BR: perl-interpreter
- Reenable elfhack

* Tue Jun 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 56.2.11-2.20190625git63b480e
- New snapshot
- stylo and rust-simd switches

* Fri Jun 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 56.2.11-1.20190621gitaa2e404
- New release/snapshot
- Set ui.use_unity_menubar to false in defaults file

* Fri Jun 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 56.2.10.1-1.20190606git3d73512
- New snapshot

* Sun May 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 56.2.10-1.20190517git9eb36ac
- New release/snapshot

* Fri Apr 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 56.2.8-2.20190411giteeb3b0b
- New snapshot
- Better rust BR version control with build_with_pinned_rust switch

* Thu Mar 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 56.2.8-1.20190313gitfa114d4
- New release/snapshot
- Temporary fix to rust BR, build is failing with 1.33+
- format-security flags changes from Fedora Firefox

* Mon Mar 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 56.2.7.1-3.20190303git61bdb81
- New snapshot
- Rework MOZ_OPT_FLAGS to enable better parallel LTO build support

* Wed Feb 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 56.2.7.1-2.20190201gitf367fd2
- LTO and fixes to build with it

* Mon Feb 04 2019 Phantom X <megaphantomx at bol dot com dot br> - 56.2.7.1-1.20190201gitf367fd2
- New release/snapshot

* Thu Jan 31 2019 Phantom X <megaphantomx at bol dot com dot br> - 56.2.7-1.20190129git3fa3c2a
- New release/snapshot

* Wed Jan 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 56.2.6-2.20181217gitff45971
- PGO and fixes for it to work (from Gentoo and Fedora Firefox)
- Return gcc build

* Wed Dec 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.2.6-1.20181217gitff45971
- New release/snapshot

* Wed Dec 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.2.5-2.20181211git3e2c786
- New snapshot
- Updated spec, more like Fedora Firefox one
- clang build

* Tue Oct 30 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.2.5-1.20181030git475fed0
- New release/snapshot

* Sun Oct 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.2.4-1.20181008git9c2c0e0
- New release/snapshot

* Mon Oct 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.2.3-2.20180911git432b427
- Some spec cleanups adapted from Fedora Firefox
- BR: clang-devel
- Disable elfhack for Fedora 29+
- Remove old gcc 7.2 fix

* Fri Sep 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.2.3-1.20180911git432b427
- New release/snapshot

* Sun Sep 09 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.2.2-4.20180908git2294d45
- New snapshot
- clang only build switch

* Sun Jul 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.2.2-3.20180807git9a88873
- Crash fixes

* Sun Jul 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.2.2-2.20180713giteb9e7d6
- New release

* Thu Jul 05 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.2.2-1.20180618gitb7b9ee7
- New release/snapshot

* Wed Jul 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.2.1-2.20180618git75c40de
- New snapshot

* Tue Jun 19 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.2.1-1.20180618gitff88ad0
- New release/snapshot

* Sat Jun 09 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.2.0-3.20180530gitf435a82
- New release/snapshot

* Tue May 29 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.2.0-2.20180527git01e6727
- New release/snapshot
- Update patchset

* Tue May 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.2.0-1.20180514git4368983
- New release/snapshot
- Update patchset

* Mon May 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.1.0-7.20180514git94abeb3
- New snapshot
- Update patchset
- Rebrand waterfox.sh.in

* Sat May 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.1.0-6.20180511git2bb1a86
- New snapshot
- Update patchset

* Tue May 01 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.1.0-5.20180430gitd5c2541
- New snapshot
- Update patchset
- Enable system webp

* Tue Apr 24 2018 Phantom X <megaphantomx at bol dot com dot br> - 56.1.0-4.20180419git8864091
- Some more FreeBSD backport patches, BR: patchutils
- Enable ogg/vorbis, BR: pkgconfig(vorbis)

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
