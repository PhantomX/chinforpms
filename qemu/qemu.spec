%ifarch %{ix86}
%global kvm_package   system-x86
# need_qemu_kvm should only ever be used by x86
%global need_qemu_kvm 1
%endif
%ifarch x86_64
%global kvm_package   system-x86
# need_qemu_kvm should only ever be used by x86
%global need_qemu_kvm 1
%endif
%ifarch %{power64}
%global kvm_package   system-ppc
%endif
%ifarch s390x
%global kvm_package   system-s390x
%endif
%ifarch armv7hl
%global kvm_package   system-arm
%endif
%ifarch aarch64
%global kvm_package   system-aarch64
%endif
%ifarch %{mips}
%global kvm_package   system-mips
%endif

%global user_static 1

%global have_kvm 0
%if 0%{?kvm_package:1}
%global have_kvm 1
%endif

# Matches numactl ExcludeArch
%global have_numactl 1
%ifarch %{arm}
%global have_numactl 0
%endif

# Matches spice ExclusiveArch
%global have_spice 0
%ifarch %{ix86} x86_64 %{arm} aarch64
%global have_spice 1
%endif

# Matches xen ExclusiveArch
%global have_xen 0
%if 0%{?fedora}
%ifarch %{ix86} x86_64 armv7hl aarch64
%global have_xen 1
%endif
%endif

%global have_liburing 0
%if 0%{?fedora}
%ifnarch %{arm}
%global have_liburing 1
%endif
%endif

%global have_virgl 0
%if 0%{?fedora}
%global have_virgl 1
%endif

%global have_pmem 0
%ifarch x86_64 %{power64}
%global have_pmem 1
%endif


# Matches edk2.spec ExclusiveArch
%global have_edk2 0
%ifarch %{ix86} x86_64 %{arm} aarch64
%global have_edk2 1
%endif

# If we can run qemu-sanity-check, hostqemu gets defined.
%ifarch %{arm}
%global hostqemu arm-softmmu/qemu-system-arm
%endif
%ifarch aarch64
%global hostqemu aarch64-softmmu/qemu-system-aarch64
%endif
%ifarch %{ix86}
%global hostqemu i386-softmmu/qemu-system-i386
%endif
%ifarch x86_64
%global hostqemu x86_64-softmmu/qemu-system-x86_64
%endif

%global qemu_sanity_check 0
%ifarch x %{?kernel_arches}
%if 0%{?hostqemu:1}
%global qemu_sanity_check 1
%endif
%endif

# QEMU sanity check doesn't know how to pick machine type
# which is needed on ARM as there is no defualt
# https://bugzilla.redhat.com/show_bug.cgi?id=1875763
%ifarch %{arm} aarch64
%global qemu_sanity_check 0
%endif

# All modules should be listed here.
%ifarch %{ix86} %{arm}
%define with_block_rbd 0
%else
%define with_block_rbd 1
%endif
%global with_block_gluster 1

%ifarch %{arm}
%define with_rdma 0
%else
%define with_rdma 1
%endif

%define evr %{epoch}:%{version}-%{release}

%define requires_block_curl Requires: %{name}-block-curl = %{evr}
%define requires_block_dmg Requires: %{name}-block-dmg = %{evr}
%if %{with_block_gluster}
%define requires_block_gluster Requires: %{name}-block-gluster = %{evr}
%define obsoletes_block_gluster %{nil}
%else
%define requires_block_gluster %{nil}
%define obsoletes_block_gluster Obsoletes: %{name}-block-gluster < %{evr}
%endif
%define requires_block_iscsi Requires: %{name}-block-iscsi = %{evr}
%define requires_block_nfs Requires: %{name}-block-nfs = %{evr}
%if %{with_block_rbd}
%define requires_block_rbd Requires: %{name}-block-rbd = %{evr}
%define obsoletes_block_rbd %{nil}
%else
%define requires_block_rbd %{nil}
%define obsoletes_block_rbd Obsoletes: %{name}-block-rbd < %{evr}
%endif
%define requires_block_ssh Requires: %{name}-block-ssh = %{evr}
%define requires_audio_alsa Requires: %{name}-audio-alsa = %{evr}
%define requires_audio_oss Requires: %{name}-audio-oss = %{evr}
%define requires_audio_pa Requires: %{name}-audio-pa = %{evr}
%define requires_audio_sdl Requires: %{name}-audio-sdl = %{evr}
%define requires_char_baum Requires: %{name}-char-baum = %{evr}
%define requires_device_usb_redirect Requires: %{name}-device-usb-redirect = %{evr}
%define requires_device_usb_smartcard Requires: %{name}-device-usb-smartcard = %{evr} 
%define requires_ui_curses Requires: %{name}-ui-curses = %{evr}
%define requires_ui_gtk Requires: %{name}-ui-gtk = %{evr}
%define requires_ui_sdl Requires: %{name}-ui-sdl = %{evr}

%if %{have_spice}
%define requires_ui_spice_app Requires: %{name}-ui-spice-app = %{evr}
%define requires_device_display_qxl Requires: %{name}-device-display-qxl = %{evr}
%else
%define requires_ui_spice_app %{nil}
%define requires_device_display_qxl %{nil}
%endif

%global requires_all_modules \
%{requires_block_curl} \
%{requires_block_dmg} \
%{requires_block_gluster} \
%{requires_block_iscsi} \
%{requires_block_nfs} \
%{requires_block_rbd} \
%{requires_block_ssh} \
%{requires_audio_alsa} \
%{requires_audio_oss} \
%{requires_audio_pa} \
%{requires_audio_sdl} \
%{requires_ui_curses} \
%{requires_ui_gtk} \
%{requires_ui_sdl} \
%{requires_ui_spice_app} \
%{requires_char_baum} \
%{requires_device_display_qxl} \
%{requires_device_usb_redirect} \
%{requires_device_usb_smartcard} \

# Modules which can be conditionally built
%global obsoletes_some_modules \
%{obsoletes_block_gluster} \
%{obsoletes_block_rbd}

%global vc_url https://git.qemu.org/?p=qemu.git;a=patch


Summary: QEMU is a FAST! processor emulator
Name: qemu
# If rc, use "~" instead "-", as ~rc1
Version: 5.1.0
Release: 102%{?dist}
Epoch: 2
License: GPLv2 and BSD and MIT and CC-BY
URL: http://www.qemu.org/

%global ver     %{lua:ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(ver)}
Source0: http://wiki.qemu-project.org/download/%{name}-%{ver}.tar.xz

Patch1: 0001-linux-user-fix-implicit-conversion-from-enumeration-.patch
Patch2: 0002-linux-user-Add-support-for-a-group-of-btrfs-ioctls-u.patch
Patch3: 0003-linux-user-Add-support-for-a-group-of-btrfs-ioctls-u.patch
Patch4: 0004-linux-user-Add-support-for-btrfs-ioctls-used-to-mani.patch
Patch5: 0005-linux-user-Add-support-for-btrfs-ioctls-used-to-get-.patch
Patch6: 0006-linux-user-Add-support-for-a-group-of-btrfs-inode-io.patch
Patch7: 0007-linux-user-Add-support-for-two-btrfs-ioctls-used-for.patch
Patch8: 0008-linux-user-Add-support-for-btrfs-ioctls-used-to-mana.patch
Patch9: 0009-linux-user-Add-support-for-btrfs-ioctls-used-to-scru.patch

# guest agent service
Source10: qemu-guest-agent.service
Source17: qemu-ga.sysconfig
# guest agent udev rules
Source11: 99-qemu-guest-agent.rules
# /etc/qemu/bridge.conf
Source12: bridge.conf
# qemu-kvm back compat wrapper installed as /usr/bin/qemu-kvm
Source13: qemu-kvm.sh
# PR manager service
Source14: qemu-pr-helper.service
Source15: qemu-pr-helper.socket
Source16: %{name}-sysusers.conf
# /etc/modprobe.d/kvm.conf, for x86
Source20: kvm-x86.modprobe.conf
# /etc/security/limits.d/95-kvm-ppc64-memlock.conf
Source21: 95-kvm-ppc64-memlock.conf


BuildRequires: gcc
# documentation deps
BuildRequires: texinfo
# For /usr/bin/pod2man
BuildRequires: perl-podlators
%if %{qemu_sanity_check}
BuildRequires: qemu-sanity-check-nodeps
BuildRequires: kernel
%endif
# For chrpath calls in specfile
BuildRequires: chrpath

# -display sdl support
BuildRequires: SDL2-devel
# used in various places for compression
BuildRequires: zlib-devel
# used in various places for crypto
BuildRequires: gnutls-devel
# VNC sasl auth support
BuildRequires: cyrus-sasl-devel
# aio implementation for block drivers
BuildRequires: libaio-devel
# pulseaudio audio output
BuildRequires: pulseaudio-libs-devel
# alsa audio output
BuildRequires: alsa-lib-devel
# qemu-pr-helper multipath support (requires libudev too)
BuildRequires: device-mapper-multipath-devel
BuildRequires: systemd-devel
# iscsi drive support
BuildRequires: libiscsi-devel
# NFS drive support
BuildRequires: libnfs-devel
# snappy compression for memory dump
BuildRequires: snappy-devel
# lzo compression for memory dump
BuildRequires: lzo-devel
# needed for -display curses
BuildRequires: ncurses-devel
# used by 9pfs
BuildRequires: libattr-devel
# used by qemu-bridge-helper and qemu-pr-helper
BuildRequires: libcap-ng-devel
# spice usb redirection support
BuildRequires: usbredir-devel >= 0.5.2
%if %{have_spice}
# spice graphics support
BuildRequires: spice-protocol >= 0.12.2
BuildRequires: spice-server-devel >= 0.12.0
%endif
# seccomp containment support
BuildRequires: libseccomp-devel >= 2.3.0
# For network block driver
BuildRequires: libcurl-devel
%if %{with_block_rbd}
# For rbd block driver
BuildRequires: librados2-devel
BuildRequires: librbd1-devel
%endif
# We need both because the 'stap' binary is probed for by configure
BuildRequires: systemtap
BuildRequires: systemtap-sdt-devel
# For VNC JPEG support
BuildRequires: libjpeg-devel
# For VNC PNG support
BuildRequires: libpng-devel
# For Braille device support
BuildRequires: brlapi-devel
# For FDT device tree support
BuildRequires: libfdt-devel
# Hard requirement for version >= 1.3
BuildRequires: pixman-devel
%if %{with_block_gluster}
# For gluster support
BuildRequires: glusterfs-devel >= 3.4.0
BuildRequires: glusterfs-api-devel >= 3.4.0
%endif
# Needed for usb passthrough for qemu >= 1.5
BuildRequires: libusbx-devel
# SSH block driver
BuildRequires: libssh-devel
# GTK frontend
BuildRequires: gtk3-devel
BuildRequires: vte291-devel
# GTK translations
BuildRequires: gettext
# RDMA migration
%if %{with_rdma}
BuildRequires: rdma-core-devel
%endif
%if %{have_xen}
# Xen support
BuildRequires: xen-devel
%endif
%if %{have_numactl}
# qemu 2.1: needed for memdev hostmem backend
BuildRequires: numactl-devel
%endif
# qemu 2.3: reading bzip2 compressed dmg images
BuildRequires: bzip2-devel
# qemu 2.4: needed for opengl bits
BuildRequires: libepoxy-devel
# qemu 2.5: needed for TLS test suite
BuildRequires: libtasn1-devel
# qemu 2.5: libcacard is it's own project now
BuildRequires: libcacard-devel >= 2.5.0
%if %{have_virgl}
# qemu 2.5: virgl 3d support
BuildRequires: virglrenderer-devel
%endif
# qemu 2.6: Needed for gtk GL support, vhost-user-gpu
BuildRequires: mesa-libgbm-devel
# qemu 2.11: preferred disassembler for TCG
BuildRequires: capstone-devel
# qemu 2.12: parallels disk images require libxml2 now
BuildRequires: libxml2-devel
%if %{have_pmem}
# qemu 3.1: Used for nvdimm
BuildRequires: libpmem-devel
%endif
# qemu 3.1: Used for qemu-ga
BuildRequires: libudev-devel
# qemu 4.0: Use for qauth infrastructure
BuildRequires: pam-devel
# qemu 4.0: user-mode networking
BuildRequires: libslirp-devel
# qemu 4.0: sphinx-build used for some docs
BuildRequires: python3-sphinx
# qemu 4.0: Used by test suite ./scripts/tap-driver.pl
BuildRequires: perl-Test-Harness
# Required for making python shebangs versioned
BuildRequires: /usr/bin/pathfix.py
BuildRequires: python3-devel
%if %{have_liburing}
# qemu 5.0 liburing support. Library isn't built for arm
BuildRequires: liburing-devel
%endif
# qemu 5.0 zstd compression support
BuildRequires: libzstd-devel
# `hostname` used by test suite
BuildRequires: hostname 
# Used for nvdimm dax
BuildRequires: daxctl-devel 

BuildRequires: glibc-static pcre-static glib2-static zlib-static


Requires: %{name}-user = %{epoch}:%{version}-%{release}
Requires: %{name}-system-aarch64 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-alpha = %{epoch}:%{version}-%{release}
Requires: %{name}-system-arm = %{epoch}:%{version}-%{release}
Requires: %{name}-system-avr = %{epoch}:%{version}-%{release}
Requires: %{name}-system-cris = %{epoch}:%{version}-%{release}
Requires: %{name}-system-lm32 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-m68k = %{epoch}:%{version}-%{release}
Requires: %{name}-system-microblaze = %{epoch}:%{version}-%{release}
Requires: %{name}-system-mips = %{epoch}:%{version}-%{release}
Requires: %{name}-system-moxie = %{epoch}:%{version}-%{release}
Requires: %{name}-system-nios2 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-or1k = %{epoch}:%{version}-%{release}
Requires: %{name}-system-ppc = %{epoch}:%{version}-%{release}
Requires: %{name}-system-riscv = %{epoch}:%{version}-%{release}
Requires: %{name}-system-rx = %{epoch}:%{version}-%{release}
Requires: %{name}-system-s390x = %{epoch}:%{version}-%{release}
Requires: %{name}-system-sh4 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-sparc = %{epoch}:%{version}-%{release}
Requires: %{name}-system-tricore = %{epoch}:%{version}-%{release}
Requires: %{name}-system-unicore32 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-x86 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-xtensa = %{epoch}:%{version}-%{release}
Requires: %{name}-img = %{epoch}:%{version}-%{release}


%description
QEMU is a generic and open source processor emulator which achieves a good
emulation speed by using dynamic translation. QEMU has two operating modes:

 * Full system emulation. In this mode, QEMU emulates a full system (for
   example a PC), including a processor and various peripherials. It can be
   used to launch different Operating Systems without rebooting the PC or
   to debug system code.
 * User mode emulation. In this mode, QEMU can launch Linux processes compiled
   for one CPU on another CPU.

As QEMU requires no host kernel patches to run, it is safe and easy to use.


%package  common
Summary: QEMU common files needed by all QEMU targets
Requires: ipxe-roms-qemu
Requires(post): /usr/bin/getent
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/useradd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%{obsoletes_some_modules}
%description common
This package provides the common files needed by all QEMU targets


%package guest-agent
Summary: QEMU guest agent
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%description guest-agent
This package provides an agent to run inside guests, which communicates
with the host over a virtio-serial channel named "org.qemu.guest_agent.0"

This package does not need to be installed on the host OS.


%package  img
Summary: QEMU command line tool for manipulating disk images
%description img
This package provides a command line tool for manipulating disk images


%package -n ivshmem-tools
Summary: Client and server for QEMU ivshmem device
%description -n ivshmem-tools
This package provides client and server tools for QEMU's ivshmem device.


%package  block-curl
Summary: QEMU CURL block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-curl
This package provides the additional CURL block driver for QEMU.

Install this package if you want to access remote disks over
http, https, ftp and other transports provided by the CURL library.


%package  block-dmg
Summary: QEMU block driver for DMG disk images
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-dmg
This package provides the additional DMG block driver for QEMU.

Install this package if you want to open '.dmg' files.


%if %{with_block_gluster}
%package  block-gluster
Summary: QEMU Gluster block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-gluster
This package provides the additional Gluster block driver for QEMU.

Install this package if you want to access remote Gluster storage.
%endif


%package  block-iscsi
Summary: QEMU iSCSI block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-iscsi
This package provides the additional iSCSI block driver for QEMU.

Install this package if you want to access iSCSI volumes.


%package  block-nfs
Summary: QEMU NFS block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-nfs
This package provides the additional NFS block driver for QEMU.

Install this package if you want to access remote NFS storage.


%if %{with_block_rbd}
%package  block-rbd
Summary: QEMU Ceph/RBD block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-rbd
This package provides the additional Ceph/RBD block driver for QEMU.

Install this package if you want to access remote Ceph volumes
using the rbd protocol.
%endif

%package  block-ssh
Summary: QEMU SSH block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-ssh
This package provides the additional SSH block driver for QEMU.

Install this package if you want to access remote disks using
the Secure Shell (SSH) protocol.


%package  audio-alsa
Summary: QEMU ALSA audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-alsa
This package provides the additional ALSA audio driver for QEMU.

%package  audio-oss
Summary: QEMU OSS audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-oss
This package provides the additional OSS audio driver for QEMU.

%package  audio-pa
Summary: QEMU PulseAudio audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-pa
This package provides the additional PulseAudi audio driver for QEMU.

%package  audio-sdl
Summary: QEMU SDL audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-sdl
This package provides the additional SDL audio driver for QEMU.


%package  ui-curses
Summary: QEMU curses UI driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-curses
This package provides the additional curses UI for QEMU.

%package  ui-gtk
Summary: QEMU GTK UI driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-gtk
This package provides the additional GTK UI for QEMU.

%package  ui-sdl
Summary: QEMU SDL UI driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-sdl
This package provides the additional SDL UI for QEMU.

%if %{have_spice}
%package  ui-spice-app
Summary: QEMU spice-app UI driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-spice-app
This package provides the additional spice-app UI for QEMU.
%endif


%package  char-baum
Summary: QEMU Baum chardev driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description char-baum
This package provides the Baum chardev driver for QEMU.


%if %{have_spice}
%package device-display-qxl
Summary: QEMU QXL display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-qxl
This package provides the QXL display device for QEMU.
%endif

%package device-usb-redirect
Summary: QEMU usbredir device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-usb-redirect
This package provides the usbredir device for QEMU.

%package device-usb-smartcard
Summary: QEMU USB smartcard device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-usb-smartcard
This package provides the USB smartcard device for QEMU. 


%if %{have_kvm}
%package kvm
Summary: QEMU metapackage for KVM support
Requires: qemu-%{kvm_package} = %{epoch}:%{version}-%{release}
%description kvm
This is a meta-package that provides a qemu-system-<arch> package for native
architectures where kvm can be enabled. For example, in an x86 system, this
will install qemu-system-x86


%package kvm-core
Summary: QEMU metapackage for KVM support
Requires: qemu-%{kvm_package}-core = %{epoch}:%{version}-%{release}
%description kvm-core
This is a meta-package that provides a qemu-system-<arch>-core package
for native architectures where kvm can be enabled. For example, in an
x86 system, this will install qemu-system-x86-core
%endif


%package user
Summary: QEMU user mode emulation of qemu targets
Requires: %{name}-common = %{epoch}:%{version}-%{release}
# On upgrade, make qemu-user get replaced with qemu-user + qemu-user-binfmt
Obsoletes: %{name}-user < 2:2.6.0-5%{?dist}
%description user
This package provides the user mode emulation of qemu targets


%package user-binfmt
Summary: QEMU user mode emulation of qemu targets
Requires: %{name}-user = %{epoch}:%{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units
# qemu-user-binfmt + qemu-user-static both provide binfmt rules
Conflicts: %{name}-user-static
# On upgrade, make qemu-user get replaced with qemu-user + qemu-user-binfmt
Obsoletes: %{name}-user < 2:2.6.0-5%{?dist}
%description user-binfmt
This package provides the user mode emulation of qemu targets

%if %{user_static}
%package user-static
Summary: QEMU user mode emulation of qemu targets static build
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units
# qemu-user-binfmt + qemu-user-static both provide binfmt rules
Conflicts: %{name}-user-binfmt
Provides: %{name}-user-binfmt
%description user-static
This package provides the user mode emulation of qemu targets built as
static binaries
%endif


%package system-aarch64
Summary: QEMU system emulator for AArch64
Requires: %{name}-system-aarch64-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-aarch64
This package provides the QEMU system emulator for AArch64.

%package system-aarch64-core
Summary: QEMU system emulator for AArch64
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%if %{have_edk2}
Requires: edk2-aarch64
%endif
%description system-aarch64-core
This package provides the QEMU system emulator for AArch64.


%package system-alpha
Summary: QEMU system emulator for Alpha
Requires: %{name}-system-alpha-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-alpha
This package provides the QEMU system emulator for Alpha systems.

%package system-alpha-core
Summary: QEMU system emulator for Alpha
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-alpha-core
This package provides the QEMU system emulator for Alpha systems.


%package system-arm
Summary: QEMU system emulator for ARM
Requires: %{name}-system-arm-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-arm
This package provides the QEMU system emulator for ARM systems.

%package system-arm-core
Summary: QEMU system emulator for ARM
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-arm-core
This package provides the QEMU system emulator for ARM boards.


%package system-avr
Summary: QEMU system emulator for AVR
Requires: %{name}-system-avr-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-avr
This package provides the QEMU system emulator for AVR systems.

%package system-avr-core
Summary: QEMU system emulator for AVR
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-avr-core
This package provides the QEMU system emulator for AVR systems. 


%package system-cris
Summary: QEMU system emulator for CRIS
Requires: %{name}-system-cris-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-cris
This package provides the system emulator for CRIS systems.

%package system-cris-core
Summary: QEMU system emulator for CRIS
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-cris-core
This package provides the system emulator for CRIS boards.


%package system-hppa
Summary: QEMU system emulator for HPPA
Requires: %{name}-system-hppa-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-hppa
This package provides the QEMU system emulator for HPPA.

%package system-hppa-core
Summary: QEMU system emulator for hppa
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-hppa-core
This package provides the QEMU system emulator for HPPA.


%package system-lm32
Summary: QEMU system emulator for LatticeMico32
Requires: %{name}-system-lm32-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-lm32
This package provides the QEMU system emulator for LatticeMico32 boards.

%package system-lm32-core
Summary: QEMU system emulator for LatticsMico32
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-lm32-core
This package provides the QEMU system emulator for LatticeMico32 boards.


%package system-m68k
Summary: QEMU system emulator for ColdFire (m68k)
Requires: %{name}-system-m68k-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-m68k
This package provides the QEMU system emulator for ColdFire boards.

%package system-m68k-core
Summary: QEMU system emulator for ColdFire (m68k)
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-m68k-core
This package provides the QEMU system emulator for ColdFire boards.


%package system-microblaze
Summary: QEMU system emulator for Microblaze
Requires: %{name}-system-microblaze-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-microblaze
This package provides the QEMU system emulator for Microblaze boards.

%package system-microblaze-core
Summary: QEMU system emulator for Microblaze
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-microblaze-core
This package provides the QEMU system emulator for Microblaze boards.


%package system-mips
Summary: QEMU system emulator for MIPS
Requires: %{name}-system-mips-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-mips
This package provides the QEMU system emulator for MIPS systems.

%package system-mips-core
Summary: QEMU system emulator for MIPS
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-mips-core
This package provides the QEMU system emulator for MIPS systems.


%package system-moxie
Summary: QEMU system emulator for Moxie
Requires: %{name}-system-moxie-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-moxie
This package provides the QEMU system emulator for Moxie boards.

%package system-moxie-core
Summary: QEMU system emulator for Moxie
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-moxie-core
This package provides the QEMU system emulator for Moxie boards.


%package system-nios2
Summary: QEMU system emulator for nios2
Requires: %{name}-system-nios2-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-nios2
This package provides the QEMU system emulator for NIOS2.

%package system-nios2-core
Summary: QEMU system emulator for nios2
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-nios2-core
This package provides the QEMU system emulator for NIOS2.


%package system-or1k
Summary: QEMU system emulator for OpenRisc32
Requires: %{name}-system-or1k-core = %{epoch}:%{version}-%{release}
Obsoletes: %{name}-system-or32 < 2:2.9.0
%{requires_all_modules}
%description system-or1k
This package provides the QEMU system emulator for OpenRisc32 boards.

%package system-or1k-core
Summary: QEMU system emulator for OpenRisc32
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Obsoletes: %{name}-system-or32-core < 2:2.9.0
%description system-or1k-core
This package provides the QEMU system emulator for OpenRisc32 boards.


%package system-ppc
Summary: QEMU system emulator for PPC
Requires: %{name}-system-ppc-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-ppc
This package provides the QEMU system emulator for PPC and PPC64 systems.

%package system-ppc-core
Summary: QEMU system emulator for PPC
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: openbios
Requires: SLOF
Requires: seavgabios-bin
%description system-ppc-core
This package provides the QEMU system emulator for PPC and PPC64 systems.


%package system-riscv
Summary: QEMU system emulator for RISC-V
Requires: %{name}-system-riscv-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-riscv
This package provides the QEMU system emulator for RISC-V systems.

%package system-riscv-core
Summary: QEMU system emulator for RISC-V
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-riscv-core
This package provides the QEMU system emulator for RISC-V systems.


%package system-rx
Summary: QEMU system emulator for RX
Requires: %{name}-system-rx-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-rx
This package provides the QEMU system emulator for RX systems.

%package system-rx-core
Summary: QEMU system emulator for RX
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-rx-core
This package provides the QEMU system emulator for RX systems.


%package system-s390x
Summary: QEMU system emulator for S390
Requires: %{name}-system-s390x-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-s390x
This package provides the QEMU system emulator for S390 systems.

%package system-s390x-core
Summary: QEMU system emulator for S390
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-s390x-core
This package provides the QEMU system emulator for S390 systems.


%package system-sh4
Summary: QEMU system emulator for SH4
Requires: %{name}-system-sh4-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-sh4
This package provides the QEMU system emulator for SH4 boards.

%package system-sh4-core
Summary: QEMU system emulator for SH4
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-sh4-core
This package provides the QEMU system emulator for SH4 boards.


%package system-sparc
Summary: QEMU system emulator for SPARC
Requires: %{name}-system-sparc-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-sparc
This package provides the QEMU system emulator for SPARC and SPARC64 systems.

%package system-sparc-core
Summary: QEMU system emulator for SPARC
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: openbios
%description system-sparc-core
This package provides the QEMU system emulator for SPARC and SPARC64 systems.


%package system-tricore
Summary: QEMU system emulator for tricore
Requires: %{name}-system-tricore-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-tricore
This package provides the QEMU system emulator for Tricore.

%package system-tricore-core
Summary: QEMU system emulator for tricore
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-tricore-core
This package provides the QEMU system emulator for Tricore.


%package system-unicore32
Summary: QEMU system emulator for Unicore32
Requires: %{name}-system-unicore32-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-unicore32
This package provides the QEMU system emulator for Unicore32 boards.

%package system-unicore32-core
Summary: QEMU system emulator for Unicore32
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-unicore32-core
This package provides the QEMU system emulator for Unicore32 boards.


%package system-x86
Summary: QEMU system emulator for x86
Requires: %{name}-system-x86-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-x86
This package provides the QEMU system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.

%package system-x86-core
Summary: QEMU system emulator for x86
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: seabios-bin
Requires: sgabios-bin
Requires: seavgabios-bin
%if %{have_edk2}
Requires: edk2-ovmf
%endif
%description system-x86-core
This package provides the QEMU system emulator for x86. When being run in a x86
machine that supports it, this package also provides the KVM virtualization
platform.


%package system-xtensa
Summary: QEMU system emulator for Xtensa
Requires: %{name}-system-xtensa-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-xtensa
This package provides the QEMU system emulator for Xtensa boards.

%package system-xtensa-core
Summary: QEMU system emulator for Xtensa
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-xtensa-core
This package provides the QEMU system emulator for Xtensa boards.


%prep
%setup -q -n qemu-%{ver}
%autopatch -p1

# https://fedoraproject.org/wiki/Changes/Make_ambiguous_python_shebangs_error
# Fix all Python shebangs recursively in .
# -p preserves timestamps
# -n prevents creating ~backup files
# -i specifies the interpreter for the shebang
# Need to list files that do not match ^[a-zA-Z0-9_]+\.py$ explicitly!
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" scripts/qemu-trace-stap


%build
# Disable LTO since it caused lots of strange assert failures.
%define _lto_cflags %{nil}

# OOM killer breaks builds with parallel make on s390(x)
%ifarch s390x
%global _smp_mflags %{nil}
%endif

# --build-id option is used for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

# As of qemu 2.1, --enable-trace-backends supports multiple backends,
# but there's a performance impact for non-dtrace so we don't use them
tracebackends="dtrace"

# 2020-08-17: tracing disabled, breaks modules on f33+
# https://bugzilla.redhat.com/show_bug.cgi?id=1869339
tracebackends="log"

%if %{have_spice}
    %global spiceflag --enable-spice
%else
    %global spiceflag --disable-spice
%endif


run_configure() {
    # Base configure call with standard shared options
    ../configure \
        --prefix=%{_prefix} \
        --libdir=%{_libdir} \
        --sysconfdir=%{_sysconfdir} \
        --localstatedir=%{_localstatedir} \
        --libexecdir=%{_libexecdir} \
        --interp-prefix=%{_prefix}/qemu-%%M \
        --with-pkgversion=%{name}-%{version}-%{release} \
        --extra-ldflags="$extraldflags -Wl,-z,relro -Wl,-z,now" \
        --extra-cflags="%{optflags}" \
        --python=%{__python3} \
        --disable-strip \
        --disable-werror \
        --tls-priority=@QEMU,SYSTEM \
        --enable-trace-backend=$tracebackends \
        "$@" || cat config.log
}

run_configure_disable_everything() {
    # Disable every qemu feature. Callers can --enable-X the bits they need
    run_configure \
        --audio-drv-list= \
        --disable-attr \
        --disable-auth-pam \
        --disable-avx2 \
        --disable-avx512f \
        --disable-blobs \
        --disable-bochs \
        --disable-brlapi \
        --disable-bsd-user \
        --disable-bzip2 \
        --disable-cap-ng \
        --disable-capstone \
        --disable-cloop \
        --disable-cocoa \
        --disable-coroutine-pool \
        --disable-crypto-afalg \
        --disable-curl \
        --disable-curses \
        --disable-debug-info \
        --disable-debug-mutex \
        --disable-debug-tcg \
        --disable-dmg \
        --disable-docs \
        --disable-fdt \
        --disable-gcrypt \
        --disable-glusterfs \
        --disable-gnutls \
        --disable-gtk \
        --disable-guest-agent \
        --disable-guest-agent-msi \
        --disable-hax \
        --disable-hvf \
        --disable-iconv \
        --disable-jemalloc \
        --disable-keyring \
        --disable-kvm \
        --disable-libdaxctl \
        --disable-libiscsi \
        --disable-libnfs \
        --disable-libpmem \
        --disable-libssh \
        --disable-libusb \
        --disable-libxml2 \
        --disable-linux-aio \
        --disable-linux-io-uring \
        --disable-linux-user \
        --disable-live-block-migration \
        --disable-lzfse \
        --disable-lzo \
        --disable-membarrier \
        --disable-modules \
        --disable-mpath \
        --disable-netmap \
        --disable-nettle \
        --disable-numa \
        --disable-opengl \
        --disable-parallels \
        --disable-pie \
        --disable-pvrdma \
        --disable-qcow1 \
        --disable-qed \
        --disable-qom-cast-debug \
        --disable-rbd \
        --disable-rdma \
        --disable-replication \
        --disable-rng-none \
        --disable-sdl \
        --disable-sdl-image \
        --disable-seccomp \
        --disable-sheepdog \
        --disable-slirp \
        --disable-smartcard \
        --disable-snappy \
        --disable-sparse \
        --disable-spice \
        --disable-system \
        --disable-tcg \
        --disable-tcmalloc \
        --disable-tools \
        --disable-tpm \
        --disable-usb-redir \
        --disable-user \
        --disable-vde \
        --disable-vdi \
        --disable-vhost-crypto \
        --disable-vhost-kernel \
        --disable-vhost-net \
        --disable-vhost-scsi \
        --disable-vhost-user \
        --disable-vhost-vdpa \
        --disable-vhost-vsock \
        --disable-virglrenderer \
        --disable-virtfs \
        --disable-vnc \
        --disable-vnc-jpeg \
        --disable-vnc-png \
        --disable-vnc-sasl \
        --disable-vte \
        --disable-vvfat \
        --disable-whpx \
        --disable-xen \
        --disable-xen-pci-passthrough \
        --disable-xfsctl \
        --disable-zstd \
        --without-default-devices \
        "$@"
}



# Build for qemu-user-static
%if %{user_static}
mkdir build-static
pushd build-static

run_configure_disable_everything \
    --disable-pie \
    --enable-attr \
    --enable-linux-user \
    --enable-tcg \
    --static

make V=1 %{?_smp_mflags} $buildldflags

popd
%endif



# Build for non-static qemu-*
mkdir build-dynamic
pushd build-dynamic

run_configure \
    --audio-drv-list=pa,sdl,alsa,oss \
    --enable-kvm \
    --enable-system \
    --enable-tcg \
    --enable-linux-user \
    --enable-pie \
    --enable-modules \
    --enable-mpath \
    %{spiceflag} \
    --enable-slirp=system \
%{nil}

echo "config-host.mak contents:"
echo "==="
cat config-host.mak
echo "==="

make V=1 %{?_smp_mflags} $buildldflags

popd


%install

%global _udevdir /lib/udev/rules.d
%global qemudocdir %{_docdir}/%{name}


# Install rules to use the bridge helper with libvirt's virbr0
install -D -m 0644 %{_sourcedir}/bridge.conf %{buildroot}%{_sysconfdir}/qemu/bridge.conf


# Install qemu-guest-agent service and udev rules
install -D -p -m 0644 %{_sourcedir}/qemu-guest-agent.service %{buildroot}%{_unitdir}/qemu-guest-agent.service
install -D -p -m 0644 %{_sourcedir}/qemu-ga.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/qemu-ga
install -D -m 0644 %{_sourcedir}/99-qemu-guest-agent.rules %{buildroot}%{_udevdir}/99-qemu-guest-agent.rules


# Install qemu-ga fsfreeze bits
mkdir -p %{buildroot}%{_sysconfdir}/qemu-ga/fsfreeze-hook.d
install -p -m 0755 scripts/qemu-guest-agent/fsfreeze-hook %{buildroot}%{_sysconfdir}/qemu-ga
install -p -m 0644 scripts/qemu-guest-agent/fsfreeze-hook.d/*.sample %{buildroot}%{_sysconfdir}/qemu-ga/fsfreeze-hook.d/
mkdir -p %{buildroot}%{_localstatedir}/log
touch %{buildroot}%{_localstatedir}/log/qga-fsfreeze-hook.log


# Install qemu-pr-helper service
install -m 0644 %{_sourcedir}/qemu-pr-helper.service %{buildroot}%{_unitdir}
install -m 0644 %{_sourcedir}/qemu-pr-helper.socket %{buildroot}%{_unitdir}


# Install ppc64 memlock
%ifarch %{power64}
install -d %{buildroot}%{_sysconfdir}/security/limits.d
install -m 0644 %{_sourcedir}/95-kvm-ppc64-memlock.conf %{buildroot}%{_sysconfdir}/security/limits.d
%endif


# Install qemu-user-static tree
mkdir -p %{buildroot}%{_bindir}
%if %{user_static}
pushd build-static
make DESTDIR=%{buildroot} install

# Rename all QEMU user emulators to have a -static suffix
for src in %{buildroot}%{_bindir}/qemu-*
do
  mv $src $src-static
done

# Rename trace files to match -static suffix
for src in %{buildroot}%{_datadir}/systemtap/tapset/qemu-*.stp
do
  dst=`echo $src | sed -e 's/.stp/-static.stp/'`
  #mv $src $dst
  #perl -i -p -e 's/(qemu-\w+)/$1-static/g; s/(qemu\.user\.\w+)/$1.static/g' $dst
done

popd
%endif

# Install main qemu-system-* tree
pushd build-dynamic
make DESTDIR=%{buildroot} install
popd
%find_lang %{name}

# Copy some static data into place
install -D -p -m 0644 -t %{buildroot}%{qemudocdir} Changelog README.rst COPYING COPYING.LIB LICENSE
install -D -p -m 0644 qemu.sasl %{buildroot}%{_sysconfdir}/sasl2/qemu.conf

# Generate qemu-system-* man pages
chmod -x %{buildroot}%{_mandir}/man1/*
for emu in %{buildroot}%{_bindir}/qemu-system-*; do
    ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/$(basename $emu).1.gz
done

# Install kvm specific source bits, and qemu-kvm manpage
%if 0%{?need_qemu_kvm}
ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/qemu-kvm.1.gz
install -m 0755 %{_sourcedir}/qemu-kvm.sh %{buildroot}%{_bindir}/qemu-kvm
install -D -p -m 0644 %{_sourcedir}/kvm-x86.modprobe.conf %{buildroot}%{_sysconfdir}/modprobe.d/kvm.conf
%endif


# Install binfmt
%global binfmt_dir %{buildroot}%{_exec_prefix}/lib/binfmt.d
mkdir -p %{binfmt_dir}

./scripts/qemu-binfmt-conf.sh --systemd ALL --exportdir %{binfmt_dir} --qemu-path %{_bindir}
for i in %{binfmt_dir}/*; do
    mv $i $(echo $i | sed 's/.conf/-dynamic.conf/')
done

%if %{user_static}
for regularfmt in %{binfmt_dir}/*; do
  staticfmt="$(echo $regularfmt | sed 's/-dynamic/-static/g')"
  cat $regularfmt | tr -d '\n' | sed "s/:$/-static:F/" > $staticfmt
done
%endif


# XXX With qemu 2.11 we can probably drop this symlinking with use of
# configure --firmwarepath, see qemu git 3d5eecab4

# Provided by package openbios
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-ppc
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc32
rm -rf %{buildroot}%{_datadir}/%{name}/openbios-sparc64
# Provided by package SLOF
rm -rf %{buildroot}%{_datadir}/%{name}/slof.bin
# Provided by package ipxe
rm -rf %{buildroot}%{_datadir}/%{name}/pxe*rom
rm -rf %{buildroot}%{_datadir}/%{name}/efi*rom
# Provided by package seavgabios
rm -rf %{buildroot}%{_datadir}/%{name}/vgabios*bin
# Provided by package seabios
rm -rf %{buildroot}%{_datadir}/%{name}/bios.bin
rm -rf %{buildroot}%{_datadir}/%{name}/bios-256k.bin
# Provided by package sgabios
rm -rf %{buildroot}%{_datadir}/%{name}/sgabios.bin
# Provided by package edk2
rm -rf %{buildroot}%{_datadir}/%{name}/edk2*
rm -rf %{buildroot}%{_datadir}/%{name}/firmware/*edk2*.json

pxe_link() {
  ln -s ../ipxe/$2.rom %{buildroot}%{_datadir}/%{name}/pxe-$1.rom
  ln -s ../ipxe.efi/$2.rom %{buildroot}%{_datadir}/%{name}/efi-$1.rom
}

pxe_link e1000 8086100e
pxe_link ne2k_pci 10ec8029
pxe_link pcnet 10222000
pxe_link rtl8139 10ec8139
pxe_link virtio 1af41000
pxe_link eepro100 80861209
pxe_link e1000e 808610d3
pxe_link vmxnet3 15ad07b0

rom_link() {
    ln -s $1 %{buildroot}%{_datadir}/%{name}/$2
}

rom_link ../seavgabios/vgabios-isavga.bin vgabios.bin
rom_link ../seavgabios/vgabios-cirrus.bin vgabios-cirrus.bin
rom_link ../seavgabios/vgabios-qxl.bin vgabios-qxl.bin
rom_link ../seavgabios/vgabios-stdvga.bin vgabios-stdvga.bin
rom_link ../seavgabios/vgabios-vmware.bin vgabios-vmware.bin
rom_link ../seavgabios/vgabios-virtio.bin vgabios-virtio.bin
rom_link ../seavgabios/vgabios-ramfb.bin vgabios-ramfb.bin
rom_link ../seavgabios/vgabios-bochs-display.bin vgabios-bochs-display.bin
rom_link ../seavgabios/vgabios-ati.bin vgabios-ati.bin
rom_link ../seabios/bios.bin bios.bin
rom_link ../seabios/bios-256k.bin bios-256k.bin
rom_link ../sgabios/sgabios.bin sgabios.bin


# When building using 'rpmbuild' or 'fedpkg local', RPATHs can be left in
# the binaries and libraries (although this doesn't occur when
# building in Koji, for some unknown reason). Some discussion here:
#
# https://lists.fedoraproject.org/pipermail/devel/2013-November/192553.html
#
# In any case it should always be safe to remove RPATHs from
# the final binaries:
for f in %{buildroot}%{_bindir}/* %{buildroot}%{_libdir}/* \
         %{buildroot}%{_libexecdir}/*; do
  if file $f | grep -q ELF | grep -q -i shared; then chrpath --delete $f; fi
done

# We need to make the modules executable else
# RPM won't pick up their dependencies.
chmod +x %{buildroot}%{_libdir}/qemu/*.so

mkdir -p %{buildroot}%{_localstatedir}/lib/qemu/

install -Dpm 644 %{SOURCE16} %{buildroot}%{_sysusersdir}/%{name}.conf


%check
%global tests_skip 0
# Enable this temporarily if tests are broken
%global tests_nofail 0

# 2020-08-31: tests passing, but s390x fails due to
# spurious warning breaking an iotest case
# https://lists.gnu.org/archive/html/qemu-devel/2020-08/msg03279.html
%global tests_nofail 1

pushd build-dynamic
%if !%{tests_skip}
%if %{tests_nofail}
 make check V=1 || :
%else
 make check V=1
%endif

# Check the binary runs (see eg RHBZ#998722).
b="./x86_64-softmmu/qemu-system-x86_64"
if [ -x "$b" ]; then "$b" -help; fi

%if %{qemu_sanity_check}
# Sanity-check current kernel can boot on this qemu.
KERNEL=`find /lib/modules -name vmlinuz | head -1`
echo "Trying to boot kernel $KERNEL with %{?hostqemu}"
qemu-sanity-check --qemu=%{?hostqemu} --kernel=$KERNEL
%endif

%endif
popd


%post common
%sysusers_create_package %{name} %{SOURCE16}


%post user-binfmt
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-binfmt
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%if %{user_static}
%post user-static
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%endif

%post guest-agent
%systemd_post qemu-guest-agent.service
%preun guest-agent
%systemd_preun qemu-guest-agent.service
%postun guest-agent
%systemd_postun_with_restart qemu-guest-agent.service



%files
# Deliberately empty


%files common -f %{name}.lang
%dir %{qemudocdir}
%doc %{qemudocdir}/Changelog
%doc %{qemudocdir}/README.rst
%doc %{qemudocdir}/index.html
%doc %{qemudocdir}/interop
%doc %{qemudocdir}/specs
%doc %{qemudocdir}/system
%doc %{qemudocdir}/tools
%doc %{qemudocdir}/user
%license %{qemudocdir}/COPYING
%license %{qemudocdir}/COPYING.LIB
%license %{qemudocdir}/LICENSE
%dir %{_datadir}/%{name}/
%{_datadir}/applications/qemu.desktop
%{_datadir}/icons/hicolor/*/apps/*
%exclude %{_datadir}/%{name}/qemu-nsis.bmp
%{_datadir}/%{name}/keymaps/
%{_datadir}/%{name}/trace-events-all
%{_datadir}/%{name}/vgabios.bin
%{_datadir}/%{name}/vgabios-cirrus.bin
%{_datadir}/%{name}/vgabios-qxl.bin
%{_datadir}/%{name}/vgabios-stdvga.bin
%{_datadir}/%{name}/vgabios-vmware.bin
%{_datadir}/%{name}/vgabios-virtio.bin
%{_datadir}/%{name}/vgabios-ramfb.bin
%{_datadir}/%{name}/vgabios-bochs-display.bin
%{_datadir}/%{name}/vgabios-ati.bin
%{_datadir}/%{name}/pxe-e1000.rom
%{_datadir}/%{name}/efi-e1000.rom
%{_datadir}/%{name}/pxe-e1000e.rom
%{_datadir}/%{name}/efi-e1000e.rom
%{_datadir}/%{name}/pxe-eepro100.rom
%{_datadir}/%{name}/efi-eepro100.rom
%{_datadir}/%{name}/pxe-ne2k_pci.rom
%{_datadir}/%{name}/efi-ne2k_pci.rom
%{_datadir}/%{name}/pxe-pcnet.rom
%{_datadir}/%{name}/efi-pcnet.rom
%{_datadir}/%{name}/pxe-rtl8139.rom
%{_datadir}/%{name}/efi-rtl8139.rom
%{_datadir}/%{name}/pxe-virtio.rom
%{_datadir}/%{name}/efi-virtio.rom
%{_datadir}/%{name}/pxe-vmxnet3.rom
%{_datadir}/%{name}/efi-vmxnet3.rom
%{_datadir}/%{name}/vhost-user/50-qemu-virtiofsd.json
%{_mandir}/man1/qemu.1*
#{_mandir}/man1/qemu-trace-stap.1*
%{_mandir}/man1/virtfs-proxy-helper.1*
%{_mandir}/man1/virtiofsd.1*
%{_mandir}/man7/qemu-block-drivers.7*
%{_mandir}/man7/qemu-cpu-models.7*
%{_mandir}/man7/qemu-qmp-ref.7*
%{_mandir}/man7/qemu-ga-ref.7*
%{_bindir}/elf2dmp
%{_bindir}/qemu-edid
%{_bindir}/qemu-keymap
%{_bindir}/qemu-storage-daemon
#{_bindir}/qemu-trace-stap
%{_sysusersdir}/%{name}.conf
%{_unitdir}/qemu-pr-helper.service
%{_unitdir}/qemu-pr-helper.socket
%attr(4755, root, root) %{_libexecdir}/qemu-bridge-helper
%{_libexecdir}/qemu-pr-helper
%{_libexecdir}/virtfs-proxy-helper
%{_libexecdir}/virtiofsd
%config(noreplace) %{_sysconfdir}/sasl2/qemu.conf
%dir %{_sysconfdir}/qemu
%config(noreplace) %{_sysconfdir}/qemu/bridge.conf
%dir %{_libdir}/qemu
%dir %attr(0751, qemu, qemu) %{_localstatedir}/lib/qemu/
%if %{have_virgl}
%{_datadir}/%{name}/vhost-user/50-qemu-gpu.json
%{_libexecdir}/vhost-user-gpu
%endif


%files guest-agent
%{_bindir}/qemu-ga
%{_mandir}/man8/qemu-ga.8*
%{_unitdir}/qemu-guest-agent.service
%{_udevdir}/99-qemu-guest-agent.rules
%config(noreplace) %{_sysconfdir}/sysconfig/qemu-ga
%{_sysconfdir}/qemu-ga
%ghost %{_localstatedir}/log/qga-fsfreeze-hook.log


%files img
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*


%files block-curl
%{_libdir}/qemu/block-curl.so
%files block-dmg
%{_libdir}/qemu/block-dmg-bz2.so
%if %{with_block_gluster}
%files block-gluster
%{_libdir}/qemu/block-gluster.so
%endif
%files block-iscsi
%{_libdir}/qemu/block-iscsi.so
%files block-nfs
%{_libdir}/qemu/block-nfs.so
%if %{with_block_rbd}
%files block-rbd
%{_libdir}/qemu/block-rbd.so
%endif
%files block-ssh
%{_libdir}/qemu/block-ssh.so


%files audio-alsa
%{_libdir}/qemu/audio-alsa.so
%files audio-oss
%{_libdir}/qemu/audio-oss.so
%files audio-pa
%{_libdir}/qemu/audio-pa.so
%files audio-sdl
%{_libdir}/qemu/audio-sdl.so


%files ui-curses
%{_libdir}/qemu/ui-curses.so
%files ui-gtk
%{_libdir}/qemu/ui-gtk.so
%files ui-sdl
%{_libdir}/qemu/ui-sdl.so
%if %{have_spice}
%files ui-spice-app
%{_libdir}/qemu/ui-spice-app.so
%endif

%files char-baum
%{_libdir}/qemu/chardev-baum.so

%if %{have_spice}
%files device-display-qxl
%{_libdir}/qemu/hw-display-qxl.so
%endif

%files device-usb-redirect
%{_libdir}/qemu/hw-usb-redirect.so
%files device-usb-smartcard
%{_libdir}/qemu/hw-usb-smartcard.so 


%files -n ivshmem-tools
%{_bindir}/ivshmem-client
%{_bindir}/ivshmem-server


%if %{have_kvm}
%files kvm
# Deliberately empty

%files kvm-core
# Deliberately empty
%endif


%files user
%{_bindir}/qemu-i386
%{_bindir}/qemu-x86_64
%{_bindir}/qemu-aarch64
%{_bindir}/qemu-aarch64_be
%{_bindir}/qemu-alpha
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-cris
%{_bindir}/qemu-hppa
%{_bindir}/qemu-m68k
%{_bindir}/qemu-microblaze
%{_bindir}/qemu-microblazeel
%{_bindir}/qemu-mips
%{_bindir}/qemu-mipsel
%{_bindir}/qemu-mips64
%{_bindir}/qemu-mips64el
%{_bindir}/qemu-mipsn32
%{_bindir}/qemu-mipsn32el
%{_bindir}/qemu-nios2
%{_bindir}/qemu-or1k
%{_bindir}/qemu-ppc
%{_bindir}/qemu-ppc64
%{_bindir}/qemu-ppc64abi32
%{_bindir}/qemu-ppc64le
%{_bindir}/qemu-riscv32
%{_bindir}/qemu-riscv64
%{_bindir}/qemu-s390x
%{_bindir}/qemu-sh4
%{_bindir}/qemu-sh4eb
%{_bindir}/qemu-sparc
%{_bindir}/qemu-sparc32plus
%{_bindir}/qemu-sparc64
%{_bindir}/qemu-tilegx
%{_bindir}/qemu-xtensa
%{_bindir}/qemu-xtensaeb

#{_datadir}/systemtap/tapset/qemu-i386*.stp
#{_datadir}/systemtap/tapset/qemu-x86_64*.stp
#{_datadir}/systemtap/tapset/qemu-aarch64*.stp
#{_datadir}/systemtap/tapset/qemu-alpha*.stp
#{_datadir}/systemtap/tapset/qemu-arm*.stp
#{_datadir}/systemtap/tapset/qemu-cris*.stp
#{_datadir}/systemtap/tapset/qemu-hppa*.stp
#{_datadir}/systemtap/tapset/qemu-m68k*.stp
#{_datadir}/systemtap/tapset/qemu-microblaze*.stp
#{_datadir}/systemtap/tapset/qemu-mips*.stp
#{_datadir}/systemtap/tapset/qemu-nios2*.stp
#{_datadir}/systemtap/tapset/qemu-or1k*.stp
#{_datadir}/systemtap/tapset/qemu-ppc*.stp
#{_datadir}/systemtap/tapset/qemu-riscv*.stp
#{_datadir}/systemtap/tapset/qemu-s390x*.stp
#{_datadir}/systemtap/tapset/qemu-sh4*.stp
#{_datadir}/systemtap/tapset/qemu-sparc*.stp
#{_datadir}/systemtap/tapset/qemu-tilegx*.stp
#{_datadir}/systemtap/tapset/qemu-xtensa*.stp

%files user-binfmt
%{_exec_prefix}/lib/binfmt.d/qemu-*-dynamic.conf

%if %{user_static}
%files user-static
# Just use wildcard matches here: we will catch any new/missing files
# in the qemu-user filelists
%{_exec_prefix}/lib/binfmt.d/qemu-*-static.conf
%{_bindir}/qemu-*-static
#{_datadir}/systemtap/tapset/qemu-*-static.stp
%endif


%files system-aarch64
%files system-aarch64-core
%{_bindir}/qemu-system-aarch64
#{_datadir}/systemtap/tapset/qemu-system-aarch64*.stp
%{_mandir}/man1/qemu-system-aarch64.1*


%files system-alpha
%files system-alpha-core
%{_bindir}/qemu-system-alpha
#{_datadir}/systemtap/tapset/qemu-system-alpha*.stp
%{_mandir}/man1/qemu-system-alpha.1*
%{_datadir}/%{name}/palcode-clipper


%files system-arm
%files system-arm-core
%{_bindir}/qemu-system-arm
#{_datadir}/systemtap/tapset/qemu-system-arm*.stp
%{_mandir}/man1/qemu-system-arm.1*


%files system-avr
%files system-avr-core
%{_bindir}/qemu-system-avr
#{_datadir}/systemtap/tapset/qemu-system-avr*.stp
%{_mandir}/man1/qemu-system-avr.1* 


%files system-cris
%files system-cris-core
%{_bindir}/qemu-system-cris
#{_datadir}/systemtap/tapset/qemu-system-cris*.stp
%{_mandir}/man1/qemu-system-cris.1*


%files system-hppa
%files system-hppa-core
%{_bindir}/qemu-system-hppa
#{_datadir}/systemtap/tapset/qemu-system-hppa*.stp
%{_mandir}/man1/qemu-system-hppa.1*
%{_datadir}/%{name}/hppa-firmware.img


%files system-lm32
%files system-lm32-core
%{_bindir}/qemu-system-lm32
#{_datadir}/systemtap/tapset/qemu-system-lm32*.stp
%{_mandir}/man1/qemu-system-lm32.1*


%files system-m68k
%files system-m68k-core
%{_bindir}/qemu-system-m68k
#{_datadir}/systemtap/tapset/qemu-system-m68k*.stp
%{_mandir}/man1/qemu-system-m68k.1*


%files system-microblaze
%files system-microblaze-core
%{_bindir}/qemu-system-microblaze
%{_bindir}/qemu-system-microblazeel
#{_datadir}/systemtap/tapset/qemu-system-microblaze*.stp
%{_mandir}/man1/qemu-system-microblaze.1*
%{_mandir}/man1/qemu-system-microblazeel.1*
%{_datadir}/%{name}/petalogix*.dtb


%files system-mips
%files system-mips-core
%{_bindir}/qemu-system-mips
%{_bindir}/qemu-system-mipsel
%{_bindir}/qemu-system-mips64
%{_bindir}/qemu-system-mips64el
#{_datadir}/systemtap/tapset/qemu-system-mips*.stp
%{_mandir}/man1/qemu-system-mips.1*
%{_mandir}/man1/qemu-system-mipsel.1*
%{_mandir}/man1/qemu-system-mips64el.1*
%{_mandir}/man1/qemu-system-mips64.1*


%files system-moxie
%files system-moxie-core
%{_bindir}/qemu-system-moxie
#{_datadir}/systemtap/tapset/qemu-system-moxie*.stp
%{_mandir}/man1/qemu-system-moxie.1*


%files system-nios2
%files system-nios2-core
%{_bindir}/qemu-system-nios2
#{_datadir}/systemtap/tapset/qemu-system-nios2*.stp
%{_mandir}/man1/qemu-system-nios2.1*


%files system-or1k
%files system-or1k-core
%{_bindir}/qemu-system-or1k
#{_datadir}/systemtap/tapset/qemu-system-or1k*.stp
%{_mandir}/man1/qemu-system-or1k.1*


%files system-ppc
%files system-ppc-core
%{_bindir}/qemu-system-ppc
%{_bindir}/qemu-system-ppc64
#{_datadir}/systemtap/tapset/qemu-system-ppc*.stp
%{_mandir}/man1/qemu-system-ppc.1*
%{_mandir}/man1/qemu-system-ppc64.1*
%{_datadir}/%{name}/bamboo.dtb
%{_datadir}/%{name}/canyonlands.dtb
%{_datadir}/%{name}/qemu_vga.ndrv
%{_datadir}/%{name}/skiboot.lid
%{_datadir}/%{name}/u-boot.e500
%{_datadir}/%{name}/u-boot-sam460-20100605.bin
%ifarch %{power64}
%{_sysconfdir}/security/limits.d/95-kvm-ppc64-memlock.conf
%endif


%files system-riscv
%files system-riscv-core
%{_bindir}/qemu-system-riscv32
%{_bindir}/qemu-system-riscv64
%{_datadir}/%{name}/opensbi-riscv*.bin
#{_datadir}/systemtap/tapset/qemu-system-riscv*.stp
%{_mandir}/man1/qemu-system-riscv*.1*


%files system-rx
%files system-rx-core
%{_bindir}/qemu-system-rx
#{_datadir}/systemtap/tapset/qemu-system-rx*.stp
%{_mandir}/man1/qemu-system-rx.1*


%files system-s390x
%files system-s390x-core
%{_bindir}/qemu-system-s390x
#{_datadir}/systemtap/tapset/qemu-system-s390x*.stp
%{_mandir}/man1/qemu-system-s390x.1*
%{_datadir}/%{name}/s390-ccw.img
%{_datadir}/%{name}/s390-netboot.img


%files system-sh4
%files system-sh4-core
%{_bindir}/qemu-system-sh4
%{_bindir}/qemu-system-sh4eb
#{_datadir}/systemtap/tapset/qemu-system-sh4*.stp
%{_mandir}/man1/qemu-system-sh4.1*
%{_mandir}/man1/qemu-system-sh4eb.1*


%files system-sparc
%files system-sparc-core
%{_bindir}/qemu-system-sparc
%{_bindir}/qemu-system-sparc64
#{_datadir}/systemtap/tapset/qemu-system-sparc*.stp
%{_mandir}/man1/qemu-system-sparc.1*
%{_mandir}/man1/qemu-system-sparc64.1*
%{_datadir}/%{name}/QEMU,tcx.bin
%{_datadir}/%{name}/QEMU,cgthree.bin


%files system-tricore
%files system-tricore-core
%{_bindir}/qemu-system-tricore
#{_datadir}/systemtap/tapset/qemu-system-tricore*.stp
%{_mandir}/man1/qemu-system-tricore.1*


%files system-unicore32
%files system-unicore32-core
%{_bindir}/qemu-system-unicore32
#{_datadir}/systemtap/tapset/qemu-system-unicore32*.stp
%{_mandir}/man1/qemu-system-unicore32.1*


%files system-x86
%files system-x86-core
%{_bindir}/qemu-system-i386
%{_bindir}/qemu-system-x86_64
#{_datadir}/systemtap/tapset/qemu-system-i386*.stp
#{_datadir}/systemtap/tapset/qemu-system-x86_64*.stp
%{_mandir}/man1/qemu-system-i386.1*
%{_mandir}/man1/qemu-system-x86_64.1*
%{_datadir}/%{name}/bios.bin
%{_datadir}/%{name}/bios-256k.bin
%{_datadir}/%{name}/bios-microvm.bin
%{_datadir}/%{name}/kvmvapic.bin
%{_datadir}/%{name}/linuxboot.bin
%{_datadir}/%{name}/linuxboot_dma.bin
%{_datadir}/%{name}/multiboot.bin
%{_datadir}/%{name}/pvh.bin
%{_datadir}/%{name}/sgabios.bin
%if 0%{?need_qemu_kvm}
%{_bindir}/qemu-kvm
%{_mandir}/man1/qemu-kvm.1*
%config(noreplace) %{_sysconfdir}/modprobe.d/kvm.conf
%endif


%files system-xtensa
%files system-xtensa-core
%{_bindir}/qemu-system-xtensa
%{_bindir}/qemu-system-xtensaeb
#{_datadir}/systemtap/tapset/qemu-system-xtensa*.stp
%{_mandir}/man1/qemu-system-xtensa.1*
%{_mandir}/man1/qemu-system-xtensaeb.1*


%changelog
* Wed Oct 07 2020 Phantom X <megaphantomx at hotmail dot com> - 2:5.1.0-102
- Rawhide sync

* Thu Sep 17 2020 Phantom X <megaphantomx at hotmail dot com> - 2:5.1.0-101
- Rawhide sync

* Tue Aug 11 2020 Phantom X <megaphantomx at bol dot com dot br> - 2:5.1.0-100
- 5.1.0
- Rawhide sync

* Wed May 27 2020 Phantom X <megaphantomx at bol dot com dot br> - 2:5.0.0-101
- f33 sync

* Tue Apr 28 2020 Phantom X <megaphantomx at bol dot com dot br> - 2:5.0.0-100
- 5.0.0

* Mon Apr 13 2020 Phantom X <megaphantomx at bol dot com dot br> - 2:5.0.0~rc2-100
- 5.0.0-rc2
- f33 sync

* Thu Apr 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 2: 5.0.0~rc1-100
- 5.0.0-rc1
- f33 sync

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 2:4.2.0-101
- f33 sync

* Thu Dec 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:4.2.0-100
- 4.2.0

* Tue Dec 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:4.2.0~rc4-100
- 4.2.0-rc4

* Fri Nov 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:4.2.0~rc3-100
- 4.2.0-rc3

* Wed Nov 20 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:4.2.0~rc2-100
- 4.2.0-rc2
- Rawhide sync

* Thu Nov 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:4.2.0~rc1-100
- 4.2.0-rc1
- Rawhide sync

* Sat Nov 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:4.1.0-101
- Rawhide sync
- Change rc versioning to "~" system

* Sat Nov 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:4.1.0-100.1
- rebuilt

* Fri Aug 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:4.1.0-100
- 4.1.0
- Rawhide sync

* Mon May 20 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:4.0.0-101
- Rawhide sync, md-clear-bit patch

* Tue Apr 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 2:4.0.0-100
- 4.0.0
- %%{_localstatedir}/lib/qemu as user directory

* Tue Apr 16 2019 Cole Robinson <crobinso@redhat.com> - 2:4.0.0-0.7.rc3
- Don't block migration with nested VMX (bz #1697997)
- Update to qemu-4.0.0-rc3

* Sat Apr 06 2019 Richard W.M. Jones <rjones@redhat.com> - 2:4.0.0-0.6.rc2
- Rebuild against xen 4.12.

* Wed Apr 03 2019 Cole Robinson <aintdiscole@gmail.com> - 2:4.0.0-0.5.rc2
- Update to 4.0.0-rc2

* Wed Mar 27 2019 Cole Robinson <aintdiscole@gmail.com> - 2:4.0.0-0.4.rc1
- Update to 4.0.0-rc1

* Mon Mar 25 2019 Adam Williamson <awilliam@redhat.com> - 2:4.0.0-0.3.rc0
- Backport patch to fix 3D crasher bug (bz #1692323)

* Thu Mar 21 2019 Cole Robinson <aintdiscole@gmail.com> - 2:4.0.0-0.2.rc0
- Fix python paths for qemu-trace-stap

* Wed Mar 20 2019 Cole Robinson <aintdiscole@gmail.com> - 2:4.0.0-0.2.rc0
- Update to 4.0.0-rc0

* Wed Mar 20 2019 Daniel P. Berrangé <berrange@redhat.com> - 2:3.1.0-5
- Fix compat with latest glibc which has gettid func

* Sun Mar 03 2019 Cole Robinson <aintdiscole@gmail.com> - 2:3.1.0-4.3
- Temporarily disable glusterfs (bz #1684298)

* Thu Feb 28 2019 Cole Robinson <aintdiscole@gmail.com> - 2:3.1.0-4.2
- Rebuild for brltty soname bump

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:3.1.0-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 12 2019 Richard W.M. Jones <rjones@redhat.com> - 2:3.1.0-4
- Remove temporary patch and rebuild against fixed capstone.

* Fri Jan 11 2019 Richard W.M. Jones <rjones@redhat.com> - 2:3.1.0-3
- Rebuild for unannounced libcapstone soname bump from 3 to 4.
- Add a temporary patch to fix capstone header location.

* Tue Dec 18 2018 Adam Williamson <awilliam@redhat.com> - 2:3.1.0-1.1
- Restore patch to drop phantom 86 key from en-us keymap (bz #1658676)

* Tue Dec 11 2018 Cole Robinson <crobinso@redhat.com> - 2:3.1.0-1
- Rebase to qemu-3.1.0 GA

* Mon Dec 10 2018 Daniel P. Berrangé <berrange@redhat.com> - 2:3.1.0-0.2.rc1
- Disable RBD on 32-bit arches

* Thu Nov 15 2018 Cole Robinson <crobinso@redhat.com> - 2:3.1.0-0.1.rc1
- Rebase to qemu-3.1.0-rc1

* Wed Aug 15 2018 Cole Robinson <crobinso@redhat.com> - 2:3.0.0-1
- Rebase to qemu-3.0.0 GA

* Mon Aug 13 2018 Cole Robinson <crobinso@redhat.com> - 2:3.0.0-0.2.rc3
- Drop ksm package, moved to ksmtuned srpm

* Tue Jul 31 2018 Cole Robinson <crobinso@redhat.com> - 2:3.0.0-0.1.rc3
- Rebase to qemu-3.0.0-rc3
- Drop now unneeded s390x conf (bz #1609706)
- Only install modprobe kvm.conf on x86 (bz #1517989)

* Fri Jul 13 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2:2.12.0-4
- Rebuild for Xen 4.11

* Mon Jun 18 2018 Daniel P. Berrangé <berrange@redhat.com> - 2:2.12.0-3
- New CPU features for speculative store bypass (CVE-2018-3639)

* Tue Jun 05 2018 Cole Robinson <crobinso@redhat.com> - 2:2.12.0-2
- Fix qxl memslot_get_virt crashes (bz #1565354)

* Mon Apr 30 2018 Cole Robinson <crobinso@redhat.com> - 2:2.12.0-1
- Update to qemu-2.12.0 GA

* Mon Apr 16 2018 Richard W.M. Jones <rjones@redhat.com> - 2:2.12.0-0.7.rc3
- Update to qemu-2.12.0-rc3
- Remove upstream patch.
- Fixes issues with partition / LV minimum alignment (RHBZ#1565714).

* Thu Apr 05 2018 Cole Robinson <crobinso@redhat.com> - 2:2.12.0-0.6.rc2
- Update to qemu-2.12.0-rc2

* Wed Mar 28 2018 Cole Robinson <crobinso@redhat.com> - 2:2.12.0-0.5.rc1
- Update to qemu-2.12.0-rc1

* Mon Mar 26 2018 Cole Robinson <crobinso@redhat.com> - 2:2.12.0-0.4.rc0
- Enable missing tilegx, xtensa* qemu-user targets

* Sun Mar 25 2018 Cole Robinson <crobinso@redhat.com> - 2:2.12.0-0.3.rc0
- Generate binfmt configs with qemu-binfmt-conf.sh

* Fri Mar 23 2018 Cole Robinson <crobinso@redhat.com> - 2:2.12.0-0.2.rc0
- Fix audio and ui module RPM deps
- Drop some arch restrictions for rdma, spice, xen, numactl
- Fix hppa firmware packaging

* Thu Mar 22 2018 Cole Robinson <crobinso@redhat.com> - 2:2.12.0-0.1.rc0
- Rebase to qemu-2.12.0-rc0
- Add hppa and riscv32/64 targets
- Add audio and ui modules

* Mon Mar 19 2018 Daniel P. Berrangé <berrange@redhat.com> - 2:2.11.1-2
- Re-enable normal hardened build macros to fix ksmctl.c hardening
- Don't strip _FORTIFY_SOURCE from compiler flags
- Don't pass -pie as an extra ldflags when we use --enable-pie

* Wed Feb 28 2018 Cole Robinson <crobinso@redhat.com> - 2:2.11.1-1
- Rebase to qemu 2.11.1 bugfix release

* Tue Feb 27 2018 Daniel P. Berrange <berrange@redhat.com> - 2:2.11.0-5
- Improve License tag
- Honour CC/LD flags for ksmctl
- Fix non-deterministic test failure
- Use explicit "python2" binary to avoid "python" brokeness (rhbz#1550010)
- Avoid breakage in TLS tests due to stricter crypto policies

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.11.0-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 21 2017 Daniel P. Berrange <berrange@redhat.com> - 2:2.11.0-4
- Re-enable RBD on arm/ppc (rhbz #1528378)

* Wed Dec 20 2017 Adam Williamson <awilliam@redhat.com> - 2:2.11.0-3
- Fix problem with typing some characters via VNC (LP#1738283)

* Wed Dec 20 2017 Cole Robinson <crobinso@redhat.com> - 2:2.11.0-2
- Rebuild for xen 4.10

* Mon Dec 18 2017 Cole Robinson <crobinso@redhat.com> - 2:2.11.0-1
- Rebase to 2.11.0 GA

* Mon Dec 04 2017 Cole Robinson <crobinso@redhat.com> - 2:2.11.0-0.3-rc3
- Rebase to 2.11.0-rc3

* Tue Nov 28 2017 Paolo Bonzini <pbonzini@redhat.com> - 2:2.11.0-0.2.rc2
- Fix compilation
- Upgrade qemu-ga packaging based on RHEL 7

* Mon Nov 20 2017 Cole Robinson <crobinso@redhat.com> - 2:2.11.0-0.1.rc1
- Rebase to 2.11.0-rc1

* Thu Oct 19 2017 Cole Robinson <crobinso@redhat.com> - 2:2.10.1-1
- Fix ppc64 KVM failure (bz #1501936)
- CVE-2017-15038: 9p: information disclosure when reading extended
  attributes (bz #1499111)
- CVE-2017-15268: potential memory exhaustion via websock connection to VNC
  (bz #1496882)

* Tue Oct 17 2017 Paolo Bonzini <pbonzini@redhat.com> - 2:2.10.0-7
- Update patch 1014 for new libmultipath/libmpathpersist API
- Force build to fail if multipath is not available
- Tighten permissions on the qemu-pr-helper socket

* Mon Oct  9 2017 Daniel P. Berrange <berrange@redhat.com> - 2:2.10.0-6
- Rebuild for libiscsi changed soname again

* Tue Oct 03 2017 Paolo Bonzini <pbonzini@redhat.com> - 2:2.10.0-5
- Rebuild with new libiscsi for iSER support

* Thu Sep 28 2017 Paolo Bonzini <pbonzini@redhat.com> - 2:2.10.0-4
- Stop using tcmalloc, glibc got faster

* Fri Sep 22 2017 Paolo Bonzini <pbonzini@redhat.com> - 2:2.10.0-3
- Backport persistent reservation manager in preparation for SELinux work
- Fix previous patch

* Mon Sep 18 2017 Nathaniel McCallum <npmccallum@redhat.com> - 2:2.10.0-2
- Fix endianness of e_type in the ppc64le binfmt

* Thu Sep 07 2017 Cole Robinson <crobinso@redhat.com> - 2:2.10.0-1
- Rebase to 2.10.0 GA

* Tue Aug 29 2017 Nathaniel McCallum <npmccallum@redhat.com> - 2:2.10.0-0.5.rc4
- Fix incorrect byte order in e_machine field in ppc64le binfmt (#1486379)

* Fri Aug 25 2017 Cole Robinson <crobinso@redhat.com> - 2:2.10.0-0.4.rc4
- Rebase to 2.10.0-rc4

* Tue Aug 22 2017 Adam Williamson <awilliam@redhat.com> - 2:2.10.0-0.3.rc3
- Don't build against rdma on 32-bit ARM (#1484155)

* Wed Aug 16 2017 Cole Robinson <crobinso@redhat.com> - 2:2.10.0-0.2.rc3
- Rebase to 2.10.0-rc3

* Thu Aug 03 2017 Cole Robinson <crobinso@redhat.com> - 2:2.10.0-0.1.rc1
- Rebase to 2.10.0-rc1

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 2:2.9.0-9
- Rebuild with binutils fix for ppc64le (#1475636)

* Tue Jul 25 2017 Daniel Berrange <berrange@redhat.com> - 2:2.9.0-8
- Disabled RBD on arm & ppc64 (rhbz #1474743)

* Thu Jul 20 2017 Nathaniel McCallum <npmccallum@redhat.com> - 2:2.9.0-7
- Fix binfmt dependencies and post scriptlets
- Add binfmt for ppc64le

* Wed Jul 19 2017 Daniel Berrange <berrange@redhat.com> - 2:2.9.0-6
- Fixes for compat with Xen 4.9

* Tue Jul 18 2017 Nathaniel McCallum <npmccallum@redhat.com> - 2:2.9.0-5
- Fix ucontext_t references

* Tue Jul 18 2017 Daniel P. Berrange <berrange@redhat.com> - 2:2.9.0-4
- Rebuild for changed Xen sonames

* Wed Jul 12 2017 Cole Robinson <crobinso@redhat.com> - 2:2.9.0-3
- CVE-2017-8112: vmw_pvscsi: infinite loop in pvscsi_log2 (bz #1445622)
- CVE-2017-8309: audio: host memory lekage via capture buffer (bz #1446520)
- CVE-2017-8379: input: host memory lekage via keyboard events (bz #1446560)
- CVE-2017-8380: scsi: megasas: out-of-bounds read in megasas_mmio_write (bz
  #1446578)
- CVE-2017-7493: 9pfs: guest privilege escalation in virtfs mapped-file mode
  (bz #1451711)
- CVE-2017-9503: megasas: null pointer dereference while processing megasas
  command (bz #1459478)
- CVE-2017-10806: usb-redirect: stack buffer overflow in debug logging (bz
  #1468497)
- CVE-2017-9524: nbd: segfault due to client non-negotiation (bz #1460172)
- CVE-2017-10664: qemu-nbd: server breaks with SIGPIPE upon client abort (bz
  #1466192)

* Mon May 22 2017 Richard W.M. Jones <rjones@redhat.com> - 2:2.9.0-2
- Bump release and rebuild to try to fix _ZdlPvm symbol (see RHBZ#1452813).

* Tue Apr 25 2017 Cole Robinson <crobinso@redhat.com> - 2:2.9.0-1
- Rebase to qemu-2.9.0 GA

* Thu Apr 13 2017 Cole Robinson <crobinso@redhat.com> - 2:2.9.0-0.2-rc4
- Rebase to qemu-2.9.0-rc4
- Fix ipxe rom links for aarch64

* Sat Apr 08 2017 Richard W.M. Jones <rjones@redhat.com> - 2:2.9.0-0.2-rc3
- Backport upstream fix for assertion when copy-on-read=true (RHBZ#1439922).

* Tue Apr 04 2017 Cole Robinson <crobinso@redhat.com> - 2:2.9.0-0.1-rc3
- Rebase to qemu-2.9.0-rc3

* Wed Mar 29 2017 Cole Robinson <crobinso@redhat.com> - 2:2.9.0-0.1-rc2
- Rebase to qemu-2.9.0-rc2
- Add Obsoletes for or32-or1k rename (bz 1435016)
- spec: Pull in vga and pxe roms for ppc64 (bz 1431403)

* Tue Mar 21 2017 Cole Robinson <crobinso@redhat.com> - 2:2.9.0-0.1-rc1
- Rebase to qemu-2.9.0-rc1

* Wed Mar 15 2017 Cole Robinson <crobinso@redhat.com> - 2:2.9.0-0.1-rc0
* Rebase to qemu-2.9.0-rc0

* Mon Feb 20 2017 Daniel Berrange <berrange@redhat.com> - 2:2.8.0-2
- Drop texi2html BR, since QEMU switched to using makeinfo back in 2010

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.8.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
