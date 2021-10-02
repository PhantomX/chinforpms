%global pkgname SDL

Name:           SDL1
Version:        1.2.15
Release:        1%{?dist}
Summary:        A cross-platform multimedia library

URL:            https://www.libsdl.org/
# The license of the file src/video/fbcon/riva_mmio.h is bad, but the contents
# of the file has been relicensed to MIT in 2008 by Nvidia for the 
# xf86_video-nv driver, therefore it can be considered ok.
# The license in the file src/stdlib/SDL_qsort.c is bad, but author relicensed
# it to zlib on 2016-02-21,
# <https://www.mccaughan.org.uk/software/qsort.c-1.14>, bug #1381888.
License:       LGPLv2+

# Source: %%{url}/release/%%{pkgname}-%%{version}.tar.gz
# To create the repackaged archive use ./repackage.sh %%{version}
Source0:        https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{pkgname}/%{pkgname}-%{version}_repackaged.tar.gz/cf222b5e323b5d0aa972b5d267badb07/%{pkgname}-%{version}_repackaged.tar.gz


Source1:        %{url}/release/%{pkgname}-%{version}.tar.gz.sig
Source2:        https://slouken.libsdl.org/slouken-pubkey.asc
Source3:        README.sdl1
Source4:        repackage.sh

# Rejected by upstream as sdl1155, rh480065
Patch1:         SDL-1.2.10-GrabNotViewable.patch
# Proposded to upstream as sdl1769
Patch2:         SDL-1.2.15-const_XData32.patch
# sdl-config(1) manual from Debian, rh948864
Patch3:         SDL-1.2.15-add_sdl_config_man.patch
# Upstream fix for sdl1486, rh990677
Patch4:         SDL-1.2.15-ignore_insane_joystick_axis.patch
# Do not use backing store by default, sdl2383, rh1073057, rejected by
# upstream
Patch5:         SDL-1.2.15-no-default-backing-store.patch
# Fix processing keyboard events if SDL_EnableUNICODE() is enabled, sdl2325,
# rh1126136, in upstream after 1.2.15
Patch6:         SDL-1.2.15-SDL_EnableUNICODE_drops_keyboard_events.patch
# Fix vec_perm() usage on little-endian 64-bit PowerPC, bug #1392465
Patch7:         SDL-1.2.15-vec_perm-ppc64le.patch
# Use system glext.h to prevent from clashing on a GL_GLEXT_VERSION definition,
# rh1662778
Patch8:         SDL-1.2.15-Use-system-glext.h.patch
# Fix CVE-2019-7577 (a buffer overread in MS_ADPCM_decode), bug #1676510,
# upstream bug #4492, in upstream after 1.2.15
Patch9:         SDL-1.2.15-CVE-2019-7577-Fix-a-buffer-overread-in-MS_ADPCM_deco.patch
# Fix CVE-2019-7575 (a buffer overwrite in MS_ADPCM_decode), bug #1676744,
# upstream bug #4493, in upstream after 1.2.15
Patch10:        SDL-1.2.15-CVE-2019-7575-Fix-a-buffer-overwrite-in-MS_ADPCM_dec.patch
# Fix CVE-2019-7574 (a buffer overread in IMA_ADPCM_decode), bug #1676750,
# upstream bug #4496, in upstream after 1.2.15
Patch11:        SDL-1.2.15-CVE-2019-7574-Fix-a-buffer-overread-in-IMA_ADPCM_dec.patch
# Fix CVE-2019-7572 (a buffer overread in IMA_ADPCM_nibble), bug #1676754,
# upstream bug #4495, in upstream after 1.2.15
Patch12:        SDL-1.2.15-CVE-2019-7572-Fix-a-buffer-overread-in-IMA_ADPCM_nib.patch
# Fix CVE-2019-7572 (a buffer overwrite in IMA_ADPCM_nibble), bug #1676754,
# upstream bug #4495, in upstream after 1.2.15
Patch13:        SDL-1.2.15-CVE-2019-7572-Fix-a-buffer-overwrite-in-IMA_ADPCM_de.patch
# Fix CVE-2019-7573, CVE-2019-7576 (buffer overreads in InitMS_ADPCM),
# bugs #1676752, #1676756, upstream bugs #4491, #4490,
# in upstream after 1.2.15
Patch14:        SDL-1.2.15-CVE-2019-7573-CVE-2019-7576-Fix-buffer-overreads-in-.patch
# Fix CVE-2019-7578, (a buffer overread in InitIMA_ADPCM), bug #1676782,
# upstream bug #4491, in upstream after 1.2.15
Patch15:        SDL-1.2.15-CVE-2019-7578-Fix-a-buffer-overread-in-InitIMA_ADPCM.patch
# Fix CVE-2019-7638, CVE-2019-7636 (buffer overflows when processing BMP
# images with too high number of colors), bugs #1677144, #1677157,
# upstream bugs #4500, #4499, in upstream after 1.2.15
Patch16:        SDL-1.2.15-CVE-2019-7638-CVE-2019-7636-Refuse-loading-BMP-image.patch
# Fix CVE-2019-7637 (an integer overflow in SDL_CalculatePitch), bug #1677152,
# upstream bug #4497, in upstream after 1.2.15
Patch17:        SDL-1.2.15-CVE-2019-7637-Fix-in-integer-overflow-in-SDL_Calcula.patch
# Fix CVE-2019-7635 (a buffer overread when blitting a BMP image with pixel
# colors out the palette), bug #1677159, upstream bug #4498,
# in upstream after 1.2.15
Patch18:        SDL-1.2.15-CVE-2019-7635-Reject-BMP-images-with-pixel-colors-ou.patch
# Reject 2, 3, 5, 6, 7-bpp BMP images (related to CVE-2019-7635),
# bug #1677159, upstream bug #4498, in upstream after 1.2.15
Patch19:        SDL-1.2.15-Reject-2-3-5-6-7-bpp-BMP-images.patch
# Fix CVE-2019-7577 (Fix a buffer overread in MS_ADPCM_nibble and
# MS_ADPCM_decode on an invalid predictor), bug #1676510, upstream bug #4492,
# in upstream after 1.2.15
Patch20:        SDL-1.2.15-CVE-2019-7577-Fix-a-buffer-overread-in-MS_ADPCM_nibb.patch
# Fix retrieving an error code after stopping and resuming a CD-ROM playback,
# upstream bug #4108, in upstream after 1.2.15
Patch21:        SDL-1.2.15-Fixed-bug-4108-Missing-break-statements-in-SDL_CDRes.patch
# Fix SDL_Surface reference counter initialization and a possible crash when
# opening a mouse device when using a framebuffer video output, bug #1602687
Patch22:        SDL-1.2.15-fix-small-errors-detected-by-coverity.patch
# Fix Windows drivers broken with a patch for CVE-2019-7637, bug #1677152,
# upstream bug #4497, in upstream after 1.2.15
Patch23:        SDL-1.2.15-fix_copy_paste_mistakes_in_commit_9b0e5c555c0f.patch
# Fix CVE-2019-13616 (a heap buffer over-read in BlitNtoN), bug #1747237,
# upstream bug #4538, in upstream after 1.2.15
Patch24:        SDL-1.2.15-CVE-2019-13616-validate_image_size_when_loading_BMP_files.patch

BuildRequires:  pkgconfig(alsa)
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  glibc-common
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  make
%ifarch %{ix86}
BuildRequires:  nasm
%endif
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  sed
# Autotools
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool


%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device.

This is the old official release, but only to be used with a wrapper, when some
application is failing with sdl12-compat.


%prep
%setup -q -n %{pkgname}-%{version} -b0
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
for F in CREDITS; do 
    iconv -f iso8859-1 -t utf-8 < "$F" > "${F}.utf"
    touch --reference "$F" "${F}.utf"
    mv "${F}.utf" "$F"
done
# Compilation without ESD
sed -i -e 's/.*AM_PATH_ESD.*//' configure.in

cp -p %{S:3} .

cat > sdl1.sh <<'EOF'
#!/usr/bin/sh
# Launch things with old official SDL

SDL_LIB=libSDL-1.2.so.0
LD_PRELOAD="/usr/\${LIB}/%{name}/${SDL_LIB}${LD_PRELOAD:+:$LD_PRELOAD}"

exec env LD_PRELOAD="${LD_PRELOAD}" "$@"
EOF

aclocal
libtoolize
autoconf


%build
%configure \
  --enable-video-opengl \
  --disable-video-svga \
  --disable-video-ggi \
  --disable-video-aalib \
  --enable-sdl-dlopen \
  --disable-arts \
  --disable-esd \
  --disable-nas \
  --enable-pulseaudio-shared \
  --enable-alsa \
  --disable-video-ps3 \
  --disable-rpath \
%{nil}

%make_build

%install
%make_install

rm -f %{buildroot}%{_bindir}/*

install -pm0755 sdl1.sh %{buildroot}%{_bindir}/sdl1

mkdir -p %{buildroot}%{_libdir}/%{name}
mv %{buildroot}%{_libdir}/*.so.* %{buildroot}%{_libdir}/%{name}/

# remove libtool .la file
rm -f %{buildroot}%{_libdir}/*.la

rm -f %{buildroot}%{_libdir}/*.{a,so}
rm -rf %{buildroot}%{_libdir}/pkgconfig
rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_datadir}
rm -rf %{buildroot}%{_mandir}


%files
%license COPYING
%doc BUGS CREDITS README-SDL.txt README.sdl1
%{_bindir}/sdl1
%{_libdir}/%{name}/libSDL-1.2.so.*


%changelog
* Sat Oct 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.15-1
- Initial spec, modified from old Fedora spec file

# end of file
