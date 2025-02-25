# qemu 9.0.0 errors with:
# RPM build errors:
#     Missing build-id in /tmp/rpmbuild/BUILDROOT/qemu-9.0.0-1.rc2.fc41.x86_64/usr/share/qemu/hppa-firmware.img
#     Missing build-id in /tmp/rpmbuild/BUILDROOT/qemu-9.0.0-1.rc2.fc41.x86_64/usr/share/qemu/hppa-firmware64.img
#     Generating build-id links failed
%global  _missing_build_ids_terminate_build    0

# Provide a way to skip tests via rpmbuild `--without`
# This makes it easier to skip tests in copr repos, where
# the qemu test suite is historically flakey
%bcond_with check

%bcond_without systemtap

%global libfdt_version 1.6.0
%global libseccomp_version 2.4.0
%global libusbx_version 1.0.23
%global meson_version 0.61.3
%global usbredir_version 0.7.1
%global ipxe_version 20200823-5.git4bd064de

%define have_vmsr_helper 0
%global have_memlock_limits 0
%global need_qemu_kvm 0
%ifarch %{ix86}
%global kvm_package   system-x86
# need_qemu_kvm should only ever be used by x86
%global need_qemu_kvm 1
%define have_vmsr_helper 1
%endif
%ifarch x86_64
%global kvm_package   system-x86
# need_qemu_kvm should only ever be used by x86
%global need_qemu_kvm 1
%define have_vmsr_helper 1
%endif
%ifarch %{power64}
%global have_memlock_limits 1
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
%ifarch riscv64
%global kvm_package   system-riscv
%endif

%global modprobe_kvm_conf %{_sourcedir}/kvm.conf
%ifarch s390x
    %global modprobe_kvm_conf %{_sourcedir}/kvm-s390x.conf
%endif
%ifarch %{ix86} x86_64
    %global modprobe_kvm_conf %{_sourcedir}/kvm-x86.conf
%endif

%global tools_only 0

%global user_static 1
%if 0%{?rhel}
# EPEL/RHEL do not have required -static builddeps
%global user_static 0
%endif

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
%global have_spice 1
%ifnarch %{ix86} x86_64 %{arm} aarch64
%global have_spice 0
%endif
%if 0%{?rhel} >= 9
%global have_spice 0
%endif

# Matches xen ExclusiveArch
%global have_xen 0
%if 0%{?fedora}
%ifarch x86_64 aarch64
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
%if 0%{?rhel} >= 10
%global have_pmem 0
%endif

%global have_jack 1
%if 0%{?rhel}
%global have_jack 0
%endif

%global have_dbus_display 1
%if %{defined rhel} && 0%{?rhel} < 9
# RHEL/Centos 8 glib is not new enough
%global have_dbus_display 0
%endif

%global have_libblkio 0
%if 0%{?fedora}
%global have_libblkio 1
%endif

%global have_gvnc_devel %{defined fedora}
%global have_sdl_image %{defined fedora}
%global have_fdt 1
%global have_opengl 1
%global have_usbredir 1
%global enable_werror 0


# Matches edk2.spec ExclusiveArch
%global have_edk2 0
%ifarch %{ix86} x86_64 aarch64 riscv64
%global have_edk2 1
%endif

# All modules should be listed here.
%define have_block_rbd 1
%ifarch %{ix86} %{arm}
%define have_block_rbd 0
%endif

%global have_block_gluster 1
%if 0%{?rhel} >= 9
%global have_block_gluster 0
%endif

%define have_block_nfs 0
%if 0%{?fedora}
%define have_block_nfs 1
%endif

%define have_librdma 1
%ifarch %{arm}
%define have_librdma 0
%endif

%define have_libcacard 1
%if 0%{?rhel} >= 9
%define have_libcacard 0
%endif

%define have_rutabaga_gfx 0
%if 0%{?fedora} >= 40
%ifarch x86_64 aarch64
%define have_rutabaga_gfx 1
%endif
%endif

%define have_qatzip 0
%ifarch x86_64
%define have_qatzip 1
%endif

%global have_libcbor 1
%if 0%{?rhel}
# libcbor missing on centos stream 9
%global have_libcbor 0
%endif

# LTO still has issues with qemu on armv7hl and aarch64
# https://bugzilla.redhat.com/show_bug.cgi?id=1952483
%global _lto_cflags %{nil}

%global firmwaredirs "%{_datadir}/qemu-firmware:%{_datadir}/ipxe/qemu:%{_datadir}/seavgabios:%{_datadir}/seabios"

%global qemudocdir %{_docdir}/%{name}

%define evr %{epoch}:%{version}-%{release}

%if %{have_libblkio}
%define requires_block_blkio Requires: %{name}-block-blkio = %{evr}
%else
%define requires_block_blkio %{nil}
%endif
%define requires_block_curl Requires: %{name}-block-curl = %{evr}
%define requires_block_dmg Requires: %{name}-block-dmg = %{evr}
%if %{have_block_gluster}
%define requires_block_gluster Requires: %{name}-block-gluster = %{evr}
%define obsoletes_block_gluster %{nil}
%else
%define requires_block_gluster %{nil}
%define obsoletes_block_gluster Obsoletes: %{name}-block-gluster < %{evr}
%endif
%define requires_block_iscsi Requires: %{name}-block-iscsi = %{evr}
%if %{have_block_nfs}
%define requires_block_nfs Requires: %{name}-block-nfs = %{evr}
%define obsoletes_block_nfs %{nil}
%else
%define requires_block_nfs %{nil}
%define obsoletes_block_nfs Obsoletes: %{name}-block-nfs < %{evr}
%endif
%if %{have_block_rbd}
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
%define requires_audio_pipewire Requires: %{name}-audio-pipewire = %{evr}
%define requires_audio_sdl Requires: %{name}-audio-sdl = %{evr}
%define requires_char_baum Requires: %{name}-char-baum = %{evr}
%define requires_device_usb_host Requires: %{name}-device-usb-host = %{evr}
%define requires_device_usb_redirect Requires: %{name}-device-usb-redirect = %{evr}
%define requires_ui_curses Requires: %{name}-ui-curses = %{evr}
%define requires_ui_gtk Requires: %{name}-ui-gtk = %{evr}
%define requires_ui_sdl Requires: %{name}-ui-sdl = %{evr}
%define requires_ui_egl_headless Requires: %{name}-ui-egl-headless = %{evr}
%define requires_ui_opengl Requires: %{name}-ui-opengl = %{evr}
%define requires_device_display_virtio_gpu Requires: %{name}-device-display-virtio-gpu = %{evr}
%define requires_device_display_virtio_gpu_pci Requires: %{name}-device-display-virtio-gpu-pci = %{evr}
%define requires_device_display_virtio_gpu_ccw Requires: %{name}-device-display-virtio-gpu-ccw = %{evr}
%define requires_device_display_virtio_vga Requires: %{name}-device-display-virtio-vga = %{evr}
%define requires_package_qemu_pr_helper Requires: qemu-pr-helper
%ifnarch %{ix86}
%if 0%{?fedora} || 0%{?rhel} > 9
%define requires_package_virtiofsd Requires: vhostuser-backend(fs)
%else
%define requires_package_virtiofsd Requires: virtiofsd
%endif
%define obsoletes_package_virtiofsd %{nil}
%else
%define requires_package_virtiofsd %{nil}
%define obsoletes_package_virtiofsd Obsoletes: %{name}-virtiofsd < %{evr}
%endif

%if %{have_virgl}
%define requires_device_display_vhost_user_gpu Requires: %{name}-device-display-vhost-user-gpu = %{evr}
%define requires_device_display_virtio_gpu_gl Requires: %{name}-device-display-virtio-gpu-gl = %{evr}
%define requires_device_display_virtio_gpu_pci_gl Requires: %{name}-device-display-virtio-gpu-pci-gl = %{evr}
%define requires_device_display_virtio_vga_gl Requires: %{name}-device-display-virtio-vga-gl = %{evr}
%else
%define requires_device_display_vhost_user_gpu %{nil}
%define requires_device_display_virtio_gpu_gl %{nil}
%define requires_device_display_virtio_gpu_pci_gl %{nil}
%define requires_device_display_virtio_vga_gl %{nil}
%endif

%if %{have_rutabaga_gfx}
%define requires_device_display_virtio_gpu_rutabaga Requires: %{name}-device-display-virtio-gpu-rutabaga = %{evr}
%define requires_device_display_virtio_gpu_pci_rutabaga Requires: %{name}-device-display-virtio-gpu-pci-rutabaga = %{evr}
%define requires_device_display_virtio_vga_rutabaga Requires: %{name}-device-display-virtio-vga-rutabaga = %{evr}
%else
%define requires_device_display_virtio_gpu_rutabaga %{nil}
%define requires_device_display_virtio_gpu_pci_rutabaga %{nil}
%define requires_device_display_virtio_vga_rutabaga %{nil}
%endif

%if %{have_jack}
%define jack_drv jack,
%define requires_audio_jack Requires: %{name}-audio-jack = %{evr}
%else
%define requires_audio_jack %{nil}
%endif

%if %{have_dbus_display}
%define requires_audio_dbus Requires: %{name}-audio-dbus = %{evr}
%define requires_ui_dbus Requires: %{name}-ui-dbus = %{evr}
%else
%define requires_audio_dbus %{nil}
%define requires_ui_dbus %{nil}
%endif

%if %{have_spice}
%define requires_ui_spice_app Requires: %{name}-ui-spice-app = %{evr}
%define requires_ui_spice_core Requires: %{name}-ui-spice-core = %{evr}
%define requires_device_display_qxl Requires: %{name}-device-display-qxl = %{evr}
%define requires_audio_spice Requires: %{name}-audio-spice = %{evr}
%define requires_char_spice Requires: %{name}-char-spice = %{evr}
%else
%define requires_ui_spice_app %{nil}
%define requires_ui_spice_core %{nil}
%define requires_device_display_qxl %{nil}
%define requires_audio_spice %{nil}
%define requires_char_spice %{nil}
%endif

%if %{have_libcacard}
%define requires_device_usb_smartcard Requires: %{name}-device-usb-smartcard = %{evr}
%else
%define requires_device_usb_smartcard %{nil}
%endif

%global requires_all_modules \
%{requires_block_blkio} \
%{requires_block_curl} \
%{requires_block_dmg} \
%{requires_block_gluster} \
%{requires_block_iscsi} \
%{requires_block_nfs} \
%{requires_block_rbd} \
%{requires_block_ssh} \
%{requires_audio_alsa} \
%{requires_audio_dbus} \
%{requires_audio_oss} \
%{requires_audio_pa} \
%{requires_audio_pipewire} \
%{requires_audio_sdl} \
%{requires_audio_jack} \
%{requires_audio_spice} \
%{requires_ui_curses} \
%{requires_ui_gtk} \
%{requires_ui_sdl} \
%{requires_ui_egl_headless} \
%{requires_ui_opengl} \
%{requires_ui_spice_app} \
%{requires_ui_spice_core} \
%{requires_char_baum} \
%{requires_char_spice} \
%{requires_device_display_qxl} \
%{requires_device_display_vhost_user_gpu} \
%{requires_device_display_virtio_gpu} \
%{requires_device_display_virtio_gpu_ccw} \
%{requires_device_display_virtio_gpu_gl} \
%{requires_device_display_virtio_gpu_rutabaga} \
%{requires_device_display_virtio_gpu_pci} \
%{requires_device_display_virtio_gpu_pci_gl} \
%{requires_device_display_virtio_gpu_pci_rutabaga} \
%{requires_device_display_virtio_vga} \
%{requires_device_display_virtio_vga_gl} \
%{requires_device_display_virtio_vga_rutabaga} \
%{requires_device_usb_host} \
%{requires_device_usb_redirect} \
%{requires_device_usb_smartcard} \
%{requires_package_qemu_pr_helper} \
%{requires_package_virtiofsd} \

# Modules which can be conditionally built
%global obsoletes_some_modules \
%{obsoletes_block_gluster} \
%{obsoletes_block_rbd} \
%{obsoletes_package_virtiofsd} \
Obsoletes: %{name}-system-cris <= %{epoch}:%{version}-%{release} \
Obsoletes: %{name}-system-cris-core <= %{epoch}:%{version}-%{release} \
Obsoletes: %{name}-system-lm32 <= %{epoch}:%{version}-%{release} \
Obsoletes: %{name}-system-lm32-core <= %{epoch}:%{version}-%{release} \
Obsoletes: %{name}-system-moxie <= %{epoch}:%{version}-%{release} \
Obsoletes: %{name}-system-moxie-core <= %{epoch}:%{version}-%{release} \
Obsoletes: %{name}-system-nios2 <= %{epoch}:%{version}-%{release} \
Obsoletes: %{name}-system-nios2-core <= %{epoch}:%{version}-%{release} \
Obsoletes: %{name}-system-unicore32 <= %{epoch}:%{version}-%{release} \
Obsoletes: %{name}-system-unicore32-core <= %{epoch}:%{version}-%{release} \
Obsoletes: sgabios-bin <= 1:0.20180715git-10.fc38

%global dlurl  https://download.qemu.org
%global vc_url https://gitlab.com/qemu-project/qemu/-/commit

%global ver     %%{lua:ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(ver)}

Summary:        QEMU is a FAST! processor emulator
Name:           qemu
# If rc, use "~" instead "-", as ~rc1
Version:        9.2.2
Release:        100%{?dist}
Epoch:          2

License: %{shrink:
    Apache-2.0 AND
    BSD-2-Clause AND
    BSD-3-Clause AND
    FSFAP AND
    GPL-1.0-or-later AND
    GPL-2.0-only AND
    GPL-2.0-or-later AND
    GPL-2.0-or-later WITH GCC-exception-2.0 AND
    LGPL-2.0-only AND
    LGPL-2.0-or-later AND
    LGPL-2.1-only AND
    LGPL-2.1-or-later AND
    MIT AND
    LicenseRef-Fedora-Public-Domain AND
    CC-BY-3.0
}

URL:            http://www.qemu.org/

Source0:        %{dlurl}/%{name}-%{ver}.tar.xz
Source1:        %{dlurl}/%{name}-%{ver}.tar.xz.sig
Source2:        gpgkey-CEACC9E15534EBABB82D3FA03353C9CEF108B584.gpg

Source10: qemu-guest-agent.service
Source11: 99-qemu-guest-agent.rules
Source12: bridge.conf
Source16: %{name}-sysusers.conf
Source17: qemu-ga.sysconfig
Source21: 95-kvm-memlock.conf
Source26: vhost.conf
Source27: kvm.conf
Source30: kvm-s390x.conf
Source31: kvm-x86.conf
Source36: README.tests

# Skip failing test in copr
# https://gitlab.com/qemu-project/qemu/-/issues/2541
Patch: 0001-Disable-9p-local-tests-that-fail-on-copr-aarch64.patch

BuildRequires: gnupg2
BuildRequires: meson >= %{meson_version}
BuildRequires: bison
BuildRequires: flex
BuildRequires: zlib-devel
BuildRequires: glib2-devel
BuildRequires: gnutls-devel
BuildRequires: libselinux-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: libaio-devel
BuildRequires: python3-devel
BuildRequires: libiscsi-devel
BuildRequires: libattr-devel
BuildRequires: libusbx-devel >= %{libusbx_version}
%if %{have_usbredir}
BuildRequires: usbredir-devel >= %{usbredir_version}
%endif
BuildRequires: python3-sphinx
BuildRequires: python3-sphinx_rtd_theme
BuildRequires: libseccomp-devel >= %{libseccomp_version}
# For network block driver
BuildRequires: libcurl-devel
BuildRequires: libssh-devel
%if %{have_block_rbd}
BuildRequires: librbd-devel
%endif
# We need both because the 'stap' binary is probed for by configure
BuildRequires: systemtap
BuildRequires: systemtap-sdt-devel
BuildRequires: /usr/bin/dtrace
# For VNC PNG support
BuildRequires: libpng-devel
# For virtiofs
BuildRequires: libcap-ng-devel
# Hard requirement for version >= 1.3
BuildRequires: pixman-devel
# For rdma
%if %{have_librdma}
BuildRequires: rdma-core-devel
%endif
%if %{have_fdt}
BuildRequires: libfdt-devel >= %{libfdt_version}
%endif
# For compressed guest memory dumps
BuildRequires: lzo-devel snappy-devel
# For NUMA memory binding
%if %{have_numactl}
BuildRequires: numactl-devel
%endif
# qemu-pr-helper multipath support (requires libudev too)
BuildRequires: device-mapper-multipath-devel
BuildRequires: systemd-devel
%if %{have_pmem}
BuildRequires: libpmem-devel
%endif
# qemu-keymap
BuildRequires: pkgconfig(xkbcommon)
%if %{have_opengl}
BuildRequires: pkgconfig(epoxy)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(gbm)
%endif
BuildRequires: perl-Test-Harness
BuildRequires: libslirp-devel
BuildRequires: libbpf-devel >= 1.0.0
%if %{have_libblkio}
BuildRequires: libblkio-devel
%endif


# Fedora specific
%if "%{toolchain}" == "clang"
BuildRequires: clang
%else
BuildRequires: gcc
%endif
BuildRequires: make
# For autosetup git_am
BuildRequires: git
# -display sdl support
BuildRequires: SDL2-devel
# pulseaudio audio output
BuildRequires: pulseaudio-libs-devel
# alsa audio output
BuildRequires: alsa-lib-devel
%if %{have_block_nfs}
# NFS drive support
BuildRequires: libnfs-devel
%endif
# curses display backend
BuildRequires: ncurses-devel
%if %{have_spice}
# spice graphics support
BuildRequires: spice-protocol
BuildRequires: spice-server-devel
%endif
# VNC JPEG support
BuildRequires: libjpeg-devel
# Braille device support
BuildRequires: brlapi-devel
%if %{have_block_gluster}
# gluster block driver
BuildRequires: glusterfs-api-devel
%endif
# GTK frontend
BuildRequires: gtk3-devel
BuildRequires: vte291-devel
# GTK translations
BuildRequires: gettext
%if %{have_xen}
# Xen support
BuildRequires: xen-devel
%endif
# reading bzip2 compressed dmg images
BuildRequires: bzip2-devel
# TLS test suite
BuildRequires: libtasn1-devel
%if %{have_libcacard}
# smartcard device
BuildRequires: libcacard-devel
%endif
%if %{have_virgl}
# virgl 3d support
BuildRequires: virglrenderer-devel
%endif
# preferred disassembler for TCG
BuildRequires: capstone-devel
# qemu-ga
BuildRequires: libudev-devel
# qauth infrastructure
BuildRequires: pam-devel
%if %{have_liburing}
# liburing support. Library isn't built for arm
BuildRequires: liburing-devel
%endif
# zstd compression support
BuildRequires: libzstd-devel
# `hostname` used by test suite
BuildRequires: hostname
# nvdimm dax
BuildRequires: daxctl-devel
# fuse block device
BuildRequires: fuse-devel
%if %{have_jack}
# jack audio driver
BuildRequires: (pipewire-jack-audio-connection-kit-devel or jack-audio-connection-kit-devel)
%endif
BuildRequires: fuse3-devel
%if %{have_sdl_image}
BuildRequires: SDL2_image-devel
%endif
%if %{have_gvnc_devel}
# Used by vnc-display-test
BuildRequires: pkgconfig(gvnc-1.0)
%endif
# Used by pipewire audio backend
BuildRequires: pipewire-devel
# Used by cryptodev-backend-lkcf
BuildRequires: keyutils-libs-devel
# Used by net AF_XDP
BuildRequires: libxdp-devel
# used by virtio-gpu-rutabaga
%if %{have_rutabaga_gfx}
BuildRequires: rutabaga-gfx-ffi-devel
%endif
%if 0%{?rhel} <= 9
# Builds on centos-stream 9 require python-tomli
BuildRequires: python-tomli
%endif
%if %{have_qatzip}
# --enable-qatzip
BuildRequires: qatzip-devel
%endif
%if %{have_libcbor}
# --enable-libcbor
BuildRequires: libcbor-devel
%endif

BuildRequires: systemd-rpm-macros
%{?sysusers_requires_compat}

%if %{user_static}
BuildRequires: glibc-static
BuildRequires: glib2-static
BuildRequires: zlib-static
# -latomic added by GLib 2.81.0, 2024-06-28
BuildRequires: libatomic-static
%endif

# Requires for the Fedora 'qemu' metapackage
Requires: %{name}-user = %{epoch}:%{version}-%{release}
Requires: %{name}-system-aarch64 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-alpha = %{epoch}:%{version}-%{release}
Requires: %{name}-system-arm = %{epoch}:%{version}-%{release}
Requires: %{name}-system-avr = %{epoch}:%{version}-%{release}
Requires: %{name}-system-loongarch64 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-m68k = %{epoch}:%{version}-%{release}
Requires: %{name}-system-microblaze = %{epoch}:%{version}-%{release}
Requires: %{name}-system-mips = %{epoch}:%{version}-%{release}
Requires: %{name}-system-or1k = %{epoch}:%{version}-%{release}
Requires: %{name}-system-ppc = %{epoch}:%{version}-%{release}
Requires: %{name}-system-riscv = %{epoch}:%{version}-%{release}
Requires: %{name}-system-rx = %{epoch}:%{version}-%{release}
Requires: %{name}-system-s390x = %{epoch}:%{version}-%{release}
Requires: %{name}-system-sh4 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-sparc = %{epoch}:%{version}-%{release}
Requires: %{name}-system-tricore = %{epoch}:%{version}-%{release}
Requires: %{name}-system-x86 = %{epoch}:%{version}-%{release}
Requires: %{name}-system-xtensa = %{epoch}:%{version}-%{release}
Requires: %{name}-img = %{epoch}:%{version}-%{release}
Requires: %{name}-tools = %{epoch}:%{version}-%{release}


%description
%{name} is an open source virtualizer that provides hardware
emulation for the KVM hypervisor. %{name} acts as a virtual
machine monitor together with the KVM kernel modules, and emulates the
hardware for a full system such as a PC and its associated peripherals.


%package common
Summary: QEMU common files needed by all QEMU targets
Requires(post): /usr/bin/getent
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/useradd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%{obsoletes_some_modules}
Requires: ipxe-roms-qemu >= %{ipxe_version}
%description common
%{name} is an open source virtualizer that provides hardware emulation for
the KVM hypervisor.

This package provides documentation and auxiliary programs used with %{name}.


%package docs
Summary: %{name} documentation
BuildArch: noarch
%description docs
%{name}-docs provides documentation files regarding %{name}.


%package -n qemu-img
Summary: QEMU command line tool for manipulating disk images
%description -n qemu-img
This package provides a command line tool for manipulating disk images.


%package -n qemu-guest-agent
Summary: QEMU guest agent
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%description -n qemu-guest-agent
%{name} is an open source virtualizer that provides hardware emulation for
the KVM hypervisor.

This package provides an agent to run inside guests, which communicates
with the host over a virtio-serial channel named "org.qemu.guest_agent.0"

This package does not need to be installed on the host OS.


%package tools
Summary: %{name} support tools
%description tools
%{name}-tools provides various tools related to %{name} usage.


%package -n qemu-pr-helper
Summary: qemu-pr-helper utility for %{name}
%description -n qemu-pr-helper
This package provides the qemu-pr-helper utility that is required for certain
SCSI features.


%package tests
Summary: tests for the %{name} package
Requires: %{name} = %{epoch}:%{version}-%{release}

%define testsdir %{_libdir}/%{name}/tests-src

%description tests
The %{name}-tests rpm contains tests that can be used to verify
the functionality of the installed %{name} package

Install this package if you want access to the avocado_qemu
tests, or qemu-iotests.


%if %{have_libblkio}
%package  block-blkio
Summary: QEMU blkio block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-blkio
This package provides the additional blkio block driver for QEMU.

Install this package if you want to access disks over vhost-user-blk, vdpa-blk,
and other transports using the libblkio library.
%endif


%package  block-curl
Summary: QEMU CURL block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-curl
This package provides the additional CURL block driver for QEMU.

Install this package if you want to access remote disks over
http, https, ftp and other transports provided by the CURL library.


%package  block-iscsi
Summary: QEMU iSCSI block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-iscsi
This package provides the additional iSCSI block driver for QEMU.

Install this package if you want to access iSCSI volumes.


%if %{have_block_rbd}
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


%if %{have_opengl}
%package  ui-opengl
Summary: QEMU opengl support
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: mesa-libGL
Requires: mesa-libEGL
Requires: mesa-dri-drivers
%description ui-opengl
This package provides opengl support.
%endif


# Fedora specific
%package  block-dmg
Summary: QEMU block driver for DMG disk images
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-dmg
This package provides the additional DMG block driver for QEMU.

Install this package if you want to open '.dmg' files.


%if %{have_block_gluster}
%package  block-gluster
Summary: QEMU Gluster block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description block-gluster
This package provides the additional Gluster block driver for QEMU.

Install this package if you want to access remote Gluster storage.
%endif


%if %{have_block_nfs}
%package  block-nfs
Summary: QEMU NFS block driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}

%description block-nfs
This package provides the additional NFS block driver for QEMU.

Install this package if you want to access remote NFS storage.
%endif


%package  audio-alsa
Summary: QEMU ALSA audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-alsa
This package provides the additional ALSA audio driver for QEMU.

%if %{have_dbus_display}
%package  audio-dbus
Summary: QEMU D-Bus audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-dbus
This package provides the additional D-Bus audio driver for QEMU.
%endif

%package  audio-oss
Summary: QEMU OSS audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-oss
This package provides the additional OSS audio driver for QEMU.

%package  audio-pa
Summary: QEMU PulseAudio audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-pa
This package provides the additional PulseAudio audio driver for QEMU.

%package  audio-pipewire
Summary: QEMU Pipewire audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-pipewire
This package provides the additional Pipewire audio driver for QEMU.

%package  audio-sdl
Summary: QEMU SDL audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-sdl
This package provides the additional SDL audio driver for QEMU.

%if %{have_jack}
%package  audio-jack
Summary: QEMU Jack audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-jack
This package provides the additional Jack audio driver for QEMU.
%endif


%package  ui-curses
Summary: QEMU curses UI driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-curses
This package provides the additional curses UI for QEMU.

%if %{have_dbus_display}
%package  ui-dbus
Summary: QEMU D-Bus UI driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-dbus
This package provides the additional D-Bus UI for QEMU.
%endif

%package  ui-gtk
Summary: QEMU GTK UI driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-ui-opengl%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-gtk
This package provides the additional GTK UI for QEMU.

%package  ui-sdl
Summary: QEMU SDL UI driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-ui-opengl%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-sdl
This package provides the additional SDL UI for QEMU.

%package  ui-egl-headless
Summary: QEMU EGL headless driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-ui-opengl%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-egl-headless
This package provides the additional egl-headless UI for QEMU.


%package  char-baum
Summary: QEMU Baum chardev driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description char-baum
This package provides the Baum chardev driver for QEMU.


%package device-display-virtio-gpu
Summary: QEMU virtio-gpu display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-gpu
This package provides the virtio-gpu display device for QEMU.

%if %{have_virgl}
%package device-display-virtio-gpu-gl
Summary: QEMU virtio-gpu-gl display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-device-display-virtio-gpu%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-gpu-gl
This package provides the virtio-gpu-gl display device for QEMU.
%endif

%if %{have_rutabaga_gfx}
%package device-display-virtio-gpu-rutabaga
Summary: QEMU virtio-gpu-rutabaga display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-device-display-virtio-gpu%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-gpu-rutabaga
This package provides the virtio-gpu-rutabaga display device for QEMU.
%endif

%package device-display-virtio-gpu-pci
Summary: QEMU virtio-gpu-pci display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-device-display-virtio-gpu%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-gpu-pci
This package provides the virtio-gpu-pci display device for QEMU.

%if %{have_virgl}
%package device-display-virtio-gpu-pci-gl
Summary: QEMU virtio-gpu-pci-gl display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-device-display-virtio-gpu-pci%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-device-display-virtio-gpu-gl%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-gpu-pci-gl
This package provides the virtio-gpu-pci-gl display device for QEMU.
%endif

%if %{have_rutabaga_gfx}
%package device-display-virtio-gpu-pci-rutabaga
Summary: QEMU virtio-gpu-pci-rutabaga display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-device-display-virtio-gpu-pci%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-gpu-pci-rutabaga
This package provides the virtio-gpu-pci-rutabaga display device for QEMU.
%endif

%package device-display-virtio-gpu-ccw
Summary: QEMU virtio-gpu-ccw display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-device-display-virtio-gpu%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-gpu-ccw
This package provides the virtio-gpu-ccw display device for QEMU.

%package device-display-virtio-vga
Summary: QEMU virtio-vga display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-device-display-virtio-gpu%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-vga
This package provides the virtio-vga display device for QEMU.

%if %{have_virgl}
%package device-display-virtio-vga-gl
Summary: QEMU virtio-vga-gl display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-device-display-virtio-vga%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-vga-gl
This package provides the virtio-vga-gl display device for QEMU.
%endif

%if %{have_rutabaga_gfx}
%package device-display-virtio-vga-rutabaga
Summary: QEMU virtio-vga-rutabaga display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-device-display-virtio-vga%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-virtio-vga-rutabaga
This package provides the virtio-vga-rutabaga display device for QEMU.
%endif

%package device-usb-host
Summary: QEMU usb host device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-usb-host
This package provides the USB pass through driver for QEMU.

%package device-usb-redirect
Summary: QEMU usbredir device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-usb-redirect
This package provides the usbredir device for QEMU.

%if %{have_libcacard}
%package device-usb-smartcard
Summary: QEMU USB smartcard device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-usb-smartcard
This package provides the USB smartcard device for QEMU.
%endif

%if %{have_virgl}
%package device-display-vhost-user-gpu
Summary: QEMU QXL display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-vhost-user-gpu
This package provides the vhost-user-gpu display device for QEMU.
%endif

%if %{have_spice}
%package  ui-spice-core
Summary: QEMU spice-core UI driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-ui-opengl%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-spice-core
This package provides the additional spice-core UI for QEMU.

%package  ui-spice-app
Summary: QEMU spice-app UI driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-ui-spice-core%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-char-spice%{?_isa} = %{epoch}:%{version}-%{release}
%description ui-spice-app
This package provides the additional spice-app UI for QEMU.

%package device-display-qxl
Summary: QEMU QXL display device
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-ui-spice-core%{?_isa} = %{epoch}:%{version}-%{release}
%description device-display-qxl
This package provides the QXL display device for QEMU.

%package  char-spice
Summary: QEMU spice chardev driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-ui-spice-core%{?_isa} = %{epoch}:%{version}-%{release}
%description char-spice
This package provides the spice chardev driver for QEMU.

%package  audio-spice
Summary: QEMU spice audio driver
Requires: %{name}-common%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-ui-spice-core%{?_isa} = %{epoch}:%{version}-%{release}
%description audio-spice
This package provides the spice audio driver for QEMU.
%endif


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
%description user
This package provides the user mode emulation of qemu targets


%package user-binfmt
Summary: QEMU user mode emulation of qemu targets
Requires: %{name}-user = %{epoch}:%{version}-%{release}
Requires(post): systemd-units
Requires(postun): systemd-units
# qemu-user-binfmt + qemu-user-static both provide binfmt rules
# Temporarily disable to get fedora CI working. Re-enable
# once this CI issue let's us deal with subpackage conflicts:
# https://pagure.io/fedora-ci/general/issue/184
#Conflicts: qemu-user-static
%description user-binfmt
This package provides the user mode emulation of qemu targets

%if %{user_static}
%package user-static
Summary: QEMU user mode emulation of qemu targets static build
Requires(post): systemd-units
Requires(postun): systemd-units
# qemu-user-binfmt + qemu-user-static both provide binfmt rules
# Temporarily disable to get fedora CI working. Re-enable
# once this CI issue let's us deal with subpackage conflicts:
# https://pagure.io/fedora-ci/general/issue/184
#Conflicts: qemu-user-binfmt
#Provides: qemu-user-binfmt
Requires: qemu-user-static-aarch64
Requires: qemu-user-static-alpha
Requires: qemu-user-static-arm
Requires: qemu-user-static-hexagon
Requires: qemu-user-static-hppa
Requires: qemu-user-static-loongarch64
Requires: qemu-user-static-m68k
Requires: qemu-user-static-microblaze
Requires: qemu-user-static-mips
Requires: qemu-user-static-or1k
Requires: qemu-user-static-ppc
Requires: qemu-user-static-riscv
Requires: qemu-user-static-s390x
Requires: qemu-user-static-sh4
Requires: qemu-user-static-sparc
Requires: qemu-user-static-x86
Requires: qemu-user-static-xtensa
Obsoletes: qemu-user-static-nios2 <= %{epoch}:%{version}-%{release}
Obsoletes: qemu-user-static-cris <= %{epoch}:%{version}-%{release}

%description user-static
This package provides the user mode emulation of qemu targets built as
static binaries

%package user-static-aarch64
Summary: QEMU user mode emulation of aarch64 qemu targets static build
%description user-static-aarch64
This package provides the aarch64 user mode emulation of qemu targets built as
static binaries

%package user-static-alpha
Summary: QEMU user mode emulation of alpha qemu targets static build
%description user-static-alpha
This package provides the alpha user mode emulation of qemu targets built as
static binaries

%package user-static-arm
Summary: QEMU user mode emulation of arm qemu targets static build
%description user-static-arm
This package provides the arm user mode emulation of qemu targets built as
static binaries

%package user-static-hexagon
Summary: QEMU user mode emulation of hexagon qemu targets static build
%description user-static-hexagon
This package provides the hexagon user mode emulation of qemu targets built as
static binaries

%package user-static-hppa
Summary: QEMU user mode emulation of hppa qemu targets static build
%description user-static-hppa
This package provides the hppa user mode emulation of qemu targets built as
static binaries

%package user-static-loongarch64
Summary: QEMU user mode emulation of loongarch64 qemu targets static build
%description user-static-loongarch64
This package provides the loongarch64 user mode emulation of qemu targets built as
static binaries

%package user-static-m68k
Summary: QEMU user mode emulation of m68k qemu targets static build
%description user-static-m68k
This package provides the m68k user mode emulation of qemu targets built as
static binaries

%package user-static-microblaze
Summary: QEMU user mode emulation of microblaze qemu targets static build
%description user-static-microblaze
This package provides the microblaze user mode emulation of qemu targets built as
static binaries

%package user-static-mips
Summary: QEMU user mode emulation of mips qemu targets static build
%description user-static-mips
This package provides the mips user mode emulation of qemu targets built as
static binaries

%package user-static-or1k
Summary: QEMU user mode emulation of or1k qemu targets static build
%description user-static-or1k
This package provides the or1k user mode emulation of qemu targets built as
static binaries

%package user-static-ppc
Summary: QEMU user mode emulation of ppc qemu targets static build
%description user-static-ppc
This package provides the ppc user mode emulation of qemu targets built as
static binaries

%package user-static-riscv
Summary: QEMU user mode emulation of riscv qemu targets static build
%description user-static-riscv
This package provides the riscv user mode emulation of qemu targets built as
static binaries

%package user-static-s390x
Summary: QEMU user mode emulation of s390x qemu targets static build
%description user-static-s390x
This package provides the s390x user mode emulation of qemu targets built as
static binaries

%package user-static-sh4
Summary: QEMU user mode emulation of sh4 qemu targets static build
%description user-static-sh4
This package provides the sh4 user mode emulation of qemu targets built as
static binaries
%endif

%package user-static-sparc
Summary: QEMU user mode emulation of sparc qemu targets static build
%description user-static-sparc
This package provides the sparc user mode emulation of qemu targets built as
static binaries

%package user-static-x86
Summary: QEMU user mode emulation of x86 qemu targets static build
%description user-static-x86
This package provides the x86 user mode emulation of qemu targets built as
static binaries

%package user-static-xtensa
Summary: QEMU user mode emulation of xtensa qemu targets static build
%description user-static-xtensa
This package provides the xtensa user mode emulation of qemu targets built as
static binaries


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
# Drop the next line in Fedora >= 44.
Obsoletes: edk2-arm <= 20241117-2.fc42
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


%package system-loongarch64
Summary: QEMU system emulator for LoongArch (LA64)
Requires: %{name}-system-loongarch64-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-loongarch64
This package provides the QEMU system emulator for Loongson boards.

%package system-loongarch64-core
Summary: QEMU system emulator for LoongArch (LA64)
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%description system-loongarch64-core
This package provides the QEMU system emulator for Loongson boards.


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


%package system-or1k
Summary: QEMU system emulator for OpenRisc32
Requires: %{name}-system-or1k-core = %{epoch}:%{version}-%{release}
%{requires_all_modules}
%description system-or1k
This package provides the QEMU system emulator for OpenRisc32 boards.

%package system-or1k-core
Summary: QEMU system emulator for OpenRisc32
Requires: %{name}-common = %{epoch}:%{version}-%{release}
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
%if %{have_edk2}
Requires: edk2-riscv64
%endif
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
%autosetup -S git_am

%global qemu_kvm_build qemu_kvm_build
mkdir -p %{qemu_kvm_build}
%global static_builddir static_builddir
mkdir -p %{static_builddir}



%build
%define disable_everything         \\\
  --audio-drv-list=                \\\
  --disable-af-xdp                 \\\
  --disable-alsa                   \\\
  --disable-asan                   \\\
  --disable-attr                   \\\
  --disable-auth-pam               \\\
  --disable-avx2                   \\\
  --disable-avx512bw               \\\
  --disable-blkio                  \\\
  --disable-block-drv-whitelist-in-tools \\\
  --disable-bochs                  \\\
  --disable-bpf                    \\\
  --disable-brlapi                 \\\
  --disable-bsd-user               \\\
  --disable-bzip2                  \\\
  --disable-cap-ng                 \\\
  --disable-capstone               \\\
  --disable-cfi                    \\\
  --disable-cfi-debug              \\\
  --disable-cloop                  \\\
  --disable-cocoa                  \\\
  --disable-colo-proxy             \\\
  --disable-coreaudio              \\\
  --disable-coroutine-pool         \\\
  --disable-crypto-afalg           \\\
  --disable-curl                   \\\
  --disable-curses                 \\\
  --disable-dbus-display           \\\
  --disable-debug-graph-lock       \\\
  --disable-debug-info             \\\
  --disable-debug-mutex            \\\
  --disable-debug-remap            \\\
  --disable-debug-tcg              \\\
  --disable-dmg                    \\\
  --disable-docs                   \\\
  --disable-download               \\\
  --disable-dsound                 \\\
  --disable-fdt                    \\\
  --disable-fuse                   \\\
  --disable-fuse-lseek             \\\
  --disable-gcrypt                 \\\
  --disable-gettext                \\\
  --disable-gio                    \\\
  --disable-glusterfs              \\\
  --disable-gnutls                 \\\
  --disable-gtk                    \\\
  --disable-gtk-clipboard          \\\
  --disable-guest-agent            \\\
  --disable-guest-agent-msi        \\\
  --disable-hv-balloon             \\\
  --disable-hvf                    \\\
  --disable-iconv                  \\\
  --disable-jack                   \\\
  --disable-kvm                    \\\
  --disable-l2tpv3                 \\\
  --disable-libcbor                \\\
  --disable-libdaxctl              \\\
  --disable-libdw                  \\\
  --disable-libkeyutils            \\\
  --disable-libiscsi               \\\
  --disable-libnfs                 \\\
  --disable-libpmem                \\\
  --disable-libssh                 \\\
  --disable-libudev                \\\
  --disable-libusb                 \\\
  --disable-linux-aio              \\\
  --disable-linux-io-uring         \\\
  --disable-linux-user             \\\
  --disable-lto                    \\\
  --disable-lzfse                  \\\
  --disable-lzo                    \\\
  --disable-malloc-trim            \\\
  --disable-membarrier             \\\
  --disable-modules                \\\
  --disable-module-upgrades        \\\
  --disable-mpath                  \\\
  --disable-multiprocess           \\\
  --disable-netmap                 \\\
  --disable-nettle                 \\\
  --disable-numa                   \\\
  --disable-nvmm                   \\\
  --disable-opengl                 \\\
  --disable-oss                    \\\
  --disable-pa                     \\\
  --disable-parallels              \\\
  --disable-pie                    \\\
  --disable-pipewire               \\\
  --disable-pixman                 \\\
  --disable-plugins                \\\
  --disable-qcow1                  \\\
  --disable-qed                    \\\
  --disable-qom-cast-debug         \\\
  --disable-qpl                    \\\
  --disable-rbd                    \\\
  --disable-rdma                   \\\
  --disable-relocatable            \\\
  --disable-replication            \\\
  --disable-rust                   \\\
  --disable-rutabaga-gfx           \\\
  --disable-rng-none               \\\
  --disable-safe-stack             \\\
  --disable-sdl                    \\\
  --disable-sdl-image              \\\
  --disable-seccomp                \\\
  --disable-selinux                \\\
  --disable-slirp                  \\\
  --disable-slirp-smbd             \\\
  --disable-smartcard              \\\
  --disable-snappy                 \\\
  --disable-sndio                  \\\
  --disable-sparse                 \\\
  --disable-spice                  \\\
  --disable-spice-protocol         \\\
  --disable-strict-rust-lints      \\\
  --disable-strip                  \\\
  --disable-system                 \\\
  --disable-tcg                    \\\
  --disable-tools                  \\\
  --disable-tpm                    \\\
  --disable-tsan                   \\\
  --disable-uadk                   \\\
  --disable-u2f                    \\\
  --disable-ubsan                  \\\
  --disable-usb-redir              \\\
  --disable-user                   \\\
  --disable-vpc                    \\\
  --disable-vde                    \\\
  --disable-vdi                    \\\
  --disable-vfio-user-server       \\\
  --disable-vhdx                   \\\
  --disable-vhost-crypto           \\\
  --disable-vhost-kernel           \\\
  --disable-vhost-net              \\\
  --disable-vhost-user             \\\
  --disable-vhost-user-blk-server  \\\
  --disable-vhost-vdpa             \\\
  --disable-virglrenderer          \\\
  --disable-virtfs                 \\\
  --disable-vnc                    \\\
  --disable-vnc-jpeg               \\\
  --disable-png                    \\\
  --disable-vnc-sasl               \\\
  --disable-vte                    \\\
  --disable-vvfat                  \\\
  --disable-werror                 \\\
  --disable-whpx                   \\\
  --disable-xen                    \\\
  --disable-xen-pci-passthrough    \\\
  --disable-xkbcommon              \\\
  --disable-zstd                   \\\
  --without-default-devices

run_configure() {
    ../configure  \
        --cc=%{__cc} \
        --cxx=/bin/false \
        --prefix="%{_prefix}" \
        --libdir="%{_libdir}" \
        --datadir="%{_datadir}" \
        --sysconfdir="%{_sysconfdir}" \
        --interp-prefix=%{_prefix}/qemu-%M \
        --localstatedir="%{_localstatedir}" \
        --docdir="%{_docdir}" \
        --libexecdir="%{_libexecdir}" \
        --extra-ldflags="%{build_ldflags}" \
%ifnarch %{arm}
        --extra-cflags="%{optflags}" \
%else
        --extra-cflags="%{optflags} -DSTAP_SDT_ARG_CONSTRAINT=g" \
%endif
        --with-pkgversion="%{name}-%{version}-%{release}" \
        --with-suffix="%{name}" \
        --firmwarepath="%firmwaredirs" \
        --enable-trace-backends=dtrace \
        --with-coroutine=ucontext \
        --tls-priority=@QEMU,SYSTEM \
        %{disable_everything} \
        "$@" \
    || ( cat config.log ; exit 1 )

    echo "config-host.mak contents:"
    echo "==="
    cat config-host.mak
    echo "==="
}


pushd %{qemu_kvm_build}
run_configure \
%if %{defined target_list}
  --target-list="%{target_list}" \
%endif
%if %{defined block_drivers_rw_list}
  --block-drv-rw-whitelist=%{block_drivers_rw_list} \
%endif
%if %{defined block_drivers_ro_list}
  --block-drv-ro-whitelist=%{block_drivers_ro_list} \
%endif
  --enable-af-xdp \
  --enable-alsa \
  --enable-attr \
%ifarch %{ix86} x86_64
  --enable-avx2 \
  --enable-avx512bw \
%endif
%if %{have_libblkio}
  --enable-blkio \
%endif
  --enable-bpf \
  --enable-cap-ng \
  --enable-capstone \
  --enable-coroutine-pool \
  --enable-curl \
%if %{have_dbus_display}
  --enable-dbus-display \
%endif
  --enable-debug-info \
  --enable-docs \
%if %{have_fdt}
  --enable-fdt=system \
%endif
  --enable-gettext \
  --enable-gnutls \
  --enable-guest-agent \
  --enable-iconv \
%if %{have_jack}
  --enable-jack \
%endif
  --enable-kvm \
  --enable-l2tpv3 \
%if %{have_libcbor}
  --enable-libcbor \
%endif
  --enable-libiscsi \
%if %{have_pmem}
  --enable-libpmem \
%endif
  --enable-libssh \
  --enable-libusb \
  --enable-libudev \
  --enable-linux-aio \
%if "%{_lto_cflags}" != "%{nil}"
  --enable-lto \
%endif
  --enable-lzo \
  --enable-malloc-trim \
  --enable-modules \
  --enable-mpath \
%if %{have_numactl}
  --enable-numa \
%endif
%if %{have_opengl}
  --enable-opengl \
%endif
  --enable-oss \
  --enable-pa \
  --enable-pie \
  --enable-pipewire \
  --enable-pixman \
%if %{have_block_rbd}
  --enable-rbd \
%endif
  --enable-relocatable \
%if %{have_librdma}
  --enable-rdma \
%endif
  --enable-seccomp \
  --enable-selinux \
  --enable-slirp \
  --enable-slirp-smbd \
  --enable-snappy \
  --enable-system \
  --enable-tcg \
  --enable-tools \
  --enable-tpm \
%if %{have_usbredir}
  --enable-usb-redir \
%endif
  --enable-vhost-kernel \
  --enable-vhost-net \
  --enable-vhost-user \
  --enable-vhost-user-blk-server \
  --enable-vhost-vdpa \
  --enable-vnc \
  --enable-png \
  --enable-vnc-sasl \
%if %{enable_werror}
  --enable-werror \
%endif
  --enable-xkbcommon \
  \
  \
  --audio-drv-list=pipewire,pa,sdl,alsa,%{?jack_drv}oss \
  --target-list-exclude=moxie-softmmu \
  --with-default-devices \
  --enable-auth-pam \
  --enable-bochs \
  --enable-brlapi \
  --enable-bzip2 \
  --enable-cloop \
  --enable-curses \
  --enable-dmg \
  --enable-fuse \
  --enable-gio \
%if %{have_block_gluster}
  --enable-glusterfs \
%endif
  --enable-gtk \
  --enable-hv-balloon \
  --enable-libdaxctl \
  --enable-libdw \
  --enable-libkeyutils \
%if %{have_block_nfs}
  --enable-libnfs \
%endif
%if %{have_liburing}
  --enable-linux-io-uring \
%endif
  --enable-linux-user \
  --enable-multiprocess \
  --enable-parallels \
%if %{have_qatzip}
  --enable-qatzip \
%endif
  --enable-qcow1 \
  --enable-qed \
  --enable-qom-cast-debug \
  --enable-replication \
%if %{have_rutabaga_gfx}
  --enable-rutabaga-gfx \
%endif
  --enable-sdl \
%if %{have_sdl_image}
  --enable-sdl-image \
%endif
%if %{have_libcacard}
  --enable-smartcard \
%endif
%if %{have_spice}
  --enable-spice \
  --enable-spice-protocol \
%endif
  --enable-vdi \
  --enable-vhost-crypto \
%if %{have_virgl}
  --enable-virglrenderer \
%endif
  --enable-vhdx \
  --enable-virtfs \
  --enable-vpc \
  --enable-vnc-jpeg \
  --enable-vte \
  --enable-vvfat \
%if %{have_xen}
  --enable-xen \
%ifarch x86_64
  --enable-xen-pci-passthrough \
%endif
%endif
  --enable-zstd \
%{nil}

%if %{tools_only}
%make_build qemu-img
%make_build qemu-io
%make_build qemu-nbd
%make_build storage-daemon/qemu-storage-daemon

%make_build docs/qemu-img.1
%make_build docs/qemu-nbd.8
%make_build docs/qemu-storage-daemon.1
%make_build docs/qemu-storage-daemon-qmp-ref.7

%make_build qga/qemu-ga
%make_build docs/qemu-ga.8
# endif tools_only
%endif


%if !%{tools_only}
%make_build
popd

# Fedora build for qemu-user-static
%if %{user_static}
pushd %{static_builddir}

run_configure \
  --enable-attr \
  --enable-linux-user \
%ifnarch %{power64}
  --enable-pie \
%endif
  --enable-tcg \
  --disable-install-blobs \
  --static

%make_build
popd  # static
%endif
# endif !tools_only
%endif


%install
# Install qemu-guest-agent service and udev rules
install -D -m 0644 %{_sourcedir}/qemu-guest-agent.service %{buildroot}%{_unitdir}/qemu-guest-agent.service
install -D -m 0644 %{_sourcedir}/qemu-ga.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/qemu-ga
install -D -m 0644 %{_sourcedir}/99-qemu-guest-agent.rules %{buildroot}%{_udevrulesdir}/99-qemu-guest-agent.rules


# Install qemu-ga fsfreeze bits
mkdir -p %{buildroot}%{_sysconfdir}/qemu-ga/fsfreeze-hook.d
install -p scripts/qemu-guest-agent/fsfreeze-hook %{buildroot}%{_sysconfdir}/qemu-ga/fsfreeze-hook
mkdir -p %{buildroot}%{_datadir}/%{name}/qemu-ga/fsfreeze-hook.d/
install -p -m 0644 scripts/qemu-guest-agent/fsfreeze-hook.d/*.sample %{buildroot}%{_datadir}/%{name}/qemu-ga/fsfreeze-hook.d/
mkdir -p -v %{buildroot}%{_localstatedir}/log/qemu-ga/


%if %{tools_only}
pushd %{qemu_kvm_build}
install -D -p -m 0755 qga/qemu-ga %{buildroot}%{_bindir}/qemu-ga
install -D -p -m 0755 qemu-img %{buildroot}%{_bindir}/qemu-img
install -D -p -m 0755 qemu-io %{buildroot}%{_bindir}/qemu-io
install -D -p -m 0755 qemu-nbd %{buildroot}%{_bindir}/qemu-nbd
install -D -p -m 0755 storage-daemon/qemu-storage-daemon %{buildroot}%{_bindir}/qemu-storage-daemon

mkdir -p %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_mandir}/man7/
mkdir -p %{buildroot}%{_mandir}/man8/

install -D -p -m 644 docs/qemu-img.1* %{buildroot}%{_mandir}/man1
install -D -p -m 644 docs/qemu-nbd.8* %{buildroot}%{_mandir}/man8
install -D -p -m 644 docs/qemu-storage-daemon.1* %{buildroot}%{_mandir}/man1
install -D -p -m 644 docs/qemu-storage-daemon-qmp-ref.7* %{buildroot}%{_mandir}/man7
install -D -p -m 644 docs/qemu-ga.8* %{buildroot}%{_mandir}/man8
popd
# endif tools_only
%endif


%if !%{tools_only}
# Install rules to use the bridge helper with libvirt's virbr0
install -D -m 0644 %{_sourcedir}/bridge.conf %{buildroot}%{_sysconfdir}/%{name}/bridge.conf

# Install qemu-pr-helper service
install -m 0644 contrib/systemd/qemu-pr-helper.service %{buildroot}%{_unitdir}
install -m 0644 contrib/systemd/qemu-pr-helper.socket %{buildroot}%{_unitdir}

%if %{have_vmsr_helper}
# Install qemu-vmsr-helper service
install -m 0644 contrib/systemd/qemu-vmsr-helper.service %{buildroot}%{_unitdir}
install -m 0644 contrib/systemd/qemu-vmsr-helper.socket %{buildroot}%{_unitdir}
%endif

%if %{have_memlock_limits}
install -D -p -m 644 %{_sourcedir}/95-kvm-memlock.conf %{buildroot}%{_sysconfdir}/security/limits.d/95-kvm-memlock.conf
%endif

%if %{have_kvm}
install -D -p -m 0644 %{_sourcedir}/vhost.conf %{buildroot}%{_sysconfdir}/modprobe.d/vhost.conf
install -D -p -m 0644 %{modprobe_kvm_conf} %{buildroot}%{_sysconfdir}/modprobe.d/kvm.conf
%endif

# Copy some static data into place
install -D -p -m 0644 -t %{buildroot}%{qemudocdir} README.rst COPYING COPYING.LIB LICENSE docs/interop/qmp-spec.rst
install -D -p -m 0644 qemu.sasl %{buildroot}%{_sysconfdir}/sasl2/%{name}.conf

install -m 0644 scripts/dump-guest-memory.py %{buildroot}%{_datadir}/%{name}


# Install simpletrace
install -m 0755 scripts/simpletrace.py %{buildroot}%{_datadir}/%{name}/simpletrace.py
mkdir -p %{buildroot}%{_datadir}/%{name}/tracetool
install -m 0644 -t %{buildroot}%{_datadir}/%{name}/tracetool scripts/tracetool/*.py
mkdir -p %{buildroot}%{_datadir}/%{name}/tracetool/backend
install -m 0644 -t %{buildroot}%{_datadir}/%{name}/tracetool/backend scripts/tracetool/backend/*.py
mkdir -p %{buildroot}%{_datadir}/%{name}/tracetool/format
install -m 0644 -t %{buildroot}%{_datadir}/%{name}/tracetool/format scripts/tracetool/format/*.py

# Ensure vhost-user directory is present even if built without virgl
mkdir -p %{buildroot}%{_datadir}/%{name}/vhost-user

# Create new directories and put them all under tests-src
mkdir -p %{buildroot}%{testsdir}/python
mkdir -p %{buildroot}%{testsdir}/tests
mkdir -p %{buildroot}%{testsdir}/tests/avocado
mkdir -p %{buildroot}%{testsdir}/tests/qemu-iotests
mkdir -p %{buildroot}%{testsdir}/scripts/qmp

# Install avocado_qemu tests
cp -R %{qemu_kvm_build}/tests/avocado/* %{buildroot}%{testsdir}/tests/avocado/

# Install qemu.py and qmp/ scripts required to run avocado_qemu tests
cp -R %{qemu_kvm_build}/python/qemu %{buildroot}%{testsdir}/python
cp -R %{qemu_kvm_build}/scripts/qmp/* %{buildroot}%{testsdir}/scripts/qmp
install -p -m 0755 tests/Makefile.include %{buildroot}%{testsdir}/tests/

# Install qemu-iotests
cp -R tests/qemu-iotests/* %{buildroot}%{testsdir}/tests/qemu-iotests/
cp -ur %{qemu_kvm_build}/tests/qemu-iotests/* %{buildroot}%{testsdir}/tests/qemu-iotests/

# Install our custom tests README
install -p -m 0644 %{_sourcedir}/README.tests %{buildroot}%{testsdir}/README


# Do the actual qemu tree install
pushd %{qemu_kvm_build}
%make_install
popd


# We need to make the block device modules and other qemu SO files executable
# otherwise RPM won't pick up their dependencies.
chmod +x %{buildroot}%{_libdir}/%{name}/*.so

# Remove docs we don't care about
find %{buildroot}%{qemudocdir} -name .buildinfo -delete
rm -rf %{buildroot}%{qemudocdir}/specs


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
rm -rf %{buildroot}%{_datadir}/%{name}/bios*.bin
# Provided by edk2
rm -rf %{buildroot}%{_datadir}/%{name}/edk2*
rm -rf %{buildroot}%{_datadir}/%{name}/firmware


# Fedora specific stuff below
%find_lang %{name}

# Generate qemu-system-* man pages
chmod -x %{buildroot}%{_mandir}/man1/*
for emu in %{buildroot}%{_bindir}/qemu-system-*; do
    ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/$(basename $emu).1.gz
 done

# Install kvm specific source bits, and qemu-kvm manpage
%if %{need_qemu_kvm}
ln -sf qemu.1.gz %{buildroot}%{_mandir}/man1/qemu-kvm.1.gz
ln -sf qemu-system-x86_64 %{buildroot}%{_bindir}/qemu-kvm
   %endif


# Install binfmt
%global binfmt_dir %{buildroot}%{_exec_prefix}/lib/binfmt.d
mkdir -p %{binfmt_dir}

./scripts/qemu-binfmt-conf.sh --systemd ALL --exportdir %{binfmt_dir} --qemu-path %{_bindir}
for i in %{binfmt_dir}/*; do mv $i $(echo $i | sed 's/.conf/-dynamic.conf/'); done


# Install qemu-user-static tree
%if %{user_static}
%define static_buildroot %{buildroot}/static/
mkdir -p %{static_buildroot}

pushd %{static_builddir}
make DESTDIR=%{static_buildroot} install

# Duplicates what the main build installs and we don't
# need second copy with a -static suffix
rm -f %{static_buildroot}%{_bindir}/qemu-trace-stap
popd  # static

# Rename all QEMU user emulators to have a -static suffix
for src in %{static_buildroot}%{_bindir}/qemu-*; do
    mv $src %{buildroot}%{_bindir}/$(basename $src)-static; done

# Rename trace files to match -static suffix
for src in %{static_buildroot}%{_datadir}/systemtap/tapset/qemu-*.stp; do
  dst=`echo $src | sed -e 's/.stp/-static.stp/'`
  mv $src $dst
  perl -i -p -e 's/(qemu-\w+)/$1-static/g; s/(qemu\.user\.\w+)/$1.static/g' $dst
  mv $dst %{buildroot}%{_datadir}/systemtap/tapset
 done

for regularfmt in %{binfmt_dir}/*; do
  staticfmt="$(echo $regularfmt | sed 's/-dynamic/-static/g')"
  cat $regularfmt | tr -d '\n' | sed "s/:$/-static:F/" > $staticfmt
  done

rm -rf %{static_buildroot}
# endif user_static
 %endif
# end Fedora specific
# endif !tools_only
%endif

## chinforpms changes
mkdir -p %{buildroot}%{_localstatedir}/lib/qemu/
install -Dpm 644 %{SOURCE16} %{buildroot}%{_sysusersdir}/%{name}.conf


%check
# Disable iotests. RHEL has done this forever, and these
# tests have been flakey in the past
export MTESTARGS="--no-suite block"

# Most architectures can use the default timeouts, but in some cases
# the hardware that's currently available is too slow and we need to
# allow tests to run for a little bit longer
%define timeout_multiplier 1
%ifarch riscv64
%define timeout_multiplier 3
%endif

%if %{with check}
%if !%{tools_only}

pushd %{qemu_kvm_build}
echo "Testing %{name}-build"
# ppc64le random qtest segfaults with no discernable pattern
#   Last check: 2023-10
#   Added: 2022-06
#
# i686 test failing as of qemu-9.2.0-rcX. Discussed here:
# https://src.fedoraproject.org/rpms/qemu/pull-request/71
# Decided to disable i686 tests entirely, en route to fully
# removing i686 support in the future
%ifnarch %{power64} %{ix86}
%make_build check TIMEOUT_MULTIPLIER=%{timeout_multiplier}
%endif

popd

# endif !tools_only
%endif
# endif with check
%endif

%post -n qemu-guest-agent
%systemd_post qemu-guest-agent.service
%preun -n qemu-guest-agent
%systemd_preun qemu-guest-agent.service
%postun -n qemu-guest-agent
%systemd_postun_with_restart qemu-guest-agent.service


%if !%{tools_only}
%pre common
%sysusers_create_compat %{SOURCE16}



%post user-binfmt
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-binfmt
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%if %{user_static}
%post user-static-aarch64
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static-aarch64
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%post user-static-alpha
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static-alpha
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%post user-static-arm
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static-arm
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%post user-static-hexagon
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static-hexagon
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%post user-static-hppa
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static-hppa
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%post user-static-loongarch64
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static-loongarch64
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%post user-static-m68k
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static-m68k
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%post user-static-microblaze
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static-microblaze
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%post user-static-mips
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static-mips
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%post user-static-or1k
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static-or1k
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%post user-static-ppc
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static-ppc
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%post user-static-riscv
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static-riscv
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%post user-static-s390x
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static-s390x
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%post user-static-sh4
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static-sh4
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%endif

%post user-static-sparc
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static-sparc
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%post user-static-x86
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static-x86
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

%post user-static-xtensa
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :
%postun user-static-xtensa
/bin/systemctl --system try-restart systemd-binfmt.service &>/dev/null || :

# endif !tools_only
%endif



%files -n qemu-img
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_bindir}/qemu-storage-daemon
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*
%{_mandir}/man1/qemu-storage-daemon.1*
%{_mandir}/man7/qemu-storage-daemon-qmp-ref.7*

%{_datadir}/systemtap/tapset/qemu-img.stp
%{_datadir}/systemtap/tapset/qemu-img-log.stp
%{_datadir}/systemtap/tapset/qemu-img-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-io.stp
%{_datadir}/systemtap/tapset/qemu-io-log.stp
%{_datadir}/systemtap/tapset/qemu-io-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-nbd.stp
%{_datadir}/systemtap/tapset/qemu-nbd-log.stp
%{_datadir}/systemtap/tapset/qemu-nbd-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-storage-daemon.stp
%{_datadir}/systemtap/tapset/qemu-storage-daemon-log.stp
%{_datadir}/systemtap/tapset/qemu-storage-daemon-simpletrace.stp


%files -n qemu-guest-agent
%doc COPYING README.rst
%{_bindir}/qemu-ga
%{_mandir}/man8/qemu-ga.8*
%{_unitdir}/qemu-guest-agent.service
%{_udevrulesdir}/99-qemu-guest-agent.rules
%config(noreplace) %{_sysconfdir}/sysconfig/qemu-ga
%{_sysconfdir}/qemu-ga
%{_datadir}/%{name}/qemu-ga
%dir %{_localstatedir}/log/qemu-ga


%if !%{tools_only}
%files
# Deliberately empty


%files -n qemu-pr-helper
%{_bindir}/qemu-pr-helper
%{_unitdir}/qemu-pr-helper.service
%{_unitdir}/qemu-pr-helper.socket
%{_mandir}/man8/qemu-pr-helper.8*


%files tools
%{_bindir}/qemu-keymap
%{_bindir}/qemu-edid
%if %{with systemtap}
%{_bindir}/qemu-trace-stap
%endif
%{_datadir}/%{name}/simpletrace.py*
%dir %{_datadir}/%{name}/tracetool/
%{_datadir}/%{name}/tracetool/*.py*
%dir %{_datadir}/%{name}/tracetool/backend/
%{_datadir}/%{name}/tracetool/backend/*.py*
%dir %{_datadir}/%{name}/tracetool/format/
%{_datadir}/%{name}/tracetool/format/*.py*
%{_datadir}/%{name}/dump-guest-memory.py*
%{_datadir}/%{name}/trace-events-all
%if %{with systemtap}
%{_mandir}/man1/qemu-trace-stap.1*
%endif
# Fedora specific
%{_bindir}/elf2dmp


%files docs
%doc %{qemudocdir}


%files common -f %{name}.lang
%license COPYING COPYING.LIB LICENSE
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/vhost-user/
%{_datadir}/icons/*
%{_datadir}/%{name}/keymaps/
%{_datadir}/%{name}/linuxboot_dma.bin
%attr(4755, -, -) %{_libexecdir}/qemu-bridge-helper
%dir %{_libdir}/%{name}/
%{_mandir}/man1/%{name}.1*
%{_mandir}/man7/qemu-block-drivers.7*
%{_mandir}/man7/qemu-cpu-models.7*
%{_mandir}/man7/qemu-ga-ref.7*
%{_mandir}/man7/qemu-qmp-ref.7*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/bridge.conf
%if %{have_kvm}
%config(noreplace) %{_sysconfdir}/modprobe.d/kvm.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/vhost.conf
%endif
%config(noreplace) %{_sysconfdir}/sasl2/%{name}.conf


# Fedora specific
%{_datadir}/applications/qemu.desktop
%exclude %{_datadir}/%{name}/qemu-nsis.bmp

## chinforpms changes
%dir %attr(0751, qemu, qemu) %{_localstatedir}/lib/qemu/
%{_sysusersdir}/%{name}.conf


%files tests
%{testsdir}
%{_libdir}/%{name}/accel-qtest-*.so

%if %{have_libblkio}
%files block-blkio
%{_libdir}/%{name}/block-blkio.so
%endif
%files block-curl
%{_libdir}/%{name}/block-curl.so
%files block-iscsi
%{_libdir}/%{name}/block-iscsi.so
%if %{have_block_rbd}
%files block-rbd
%{_libdir}/%{name}/block-rbd.so
%endif
%files block-ssh
%{_libdir}/%{name}/block-ssh.so

%if %{have_opengl}
%files ui-opengl
%{_libdir}/%{name}/ui-opengl.so
%endif


%files block-dmg
%{_libdir}/%{name}/block-dmg-bz2.so
%if %{have_block_gluster}
%files block-gluster
%{_libdir}/%{name}/block-gluster.so
%endif
%if %{have_block_nfs}
%files block-nfs
%{_libdir}/%{name}/block-nfs.so
%endif

%files audio-alsa
%{_libdir}/%{name}/audio-alsa.so
%if %{have_dbus_display}
%files audio-dbus
%{_libdir}/%{name}/audio-dbus.so
%endif
%files audio-oss
%{_libdir}/%{name}/audio-oss.so
%files audio-pa
%{_libdir}/%{name}/audio-pa.so
%files audio-pipewire
%{_libdir}/%{name}/audio-pipewire.so
%files audio-sdl
%{_libdir}/%{name}/audio-sdl.so
%if %{have_jack}
%files audio-jack
%{_libdir}/%{name}/audio-jack.so
%endif


%files ui-curses
%{_libdir}/%{name}/ui-curses.so
%if %{have_dbus_display}
%files ui-dbus
%{_libdir}/%{name}/ui-dbus.so
%endif
%files ui-gtk
%{_libdir}/%{name}/ui-gtk.so
%files ui-sdl
%{_libdir}/%{name}/ui-sdl.so
%files ui-egl-headless
%{_libdir}/%{name}/ui-egl-headless.so

%files char-baum
%{_libdir}/%{name}/chardev-baum.so


%files device-display-virtio-gpu
%{_libdir}/%{name}/hw-display-virtio-gpu.so
%if %{have_virgl}
%files device-display-virtio-gpu-gl
%{_libdir}/%{name}/hw-display-virtio-gpu-gl.so
%endif
%if %{have_rutabaga_gfx}
%files device-display-virtio-gpu-rutabaga
%{_libdir}/%{name}/hw-display-virtio-gpu-rutabaga.so
%endif
%files device-display-virtio-gpu-pci
%{_libdir}/%{name}/hw-display-virtio-gpu-pci.so
%if %{have_virgl}
%files device-display-virtio-gpu-pci-gl
%{_libdir}/%{name}/hw-display-virtio-gpu-pci-gl.so
%endif
%if %{have_rutabaga_gfx}
%files device-display-virtio-gpu-pci-rutabaga
%{_libdir}/%{name}/hw-display-virtio-gpu-pci-rutabaga.so
%endif
%files device-display-virtio-gpu-ccw
%{_libdir}/%{name}/hw-s390x-virtio-gpu-ccw.so
%files device-display-virtio-vga
%{_libdir}/%{name}/hw-display-virtio-vga.so
%if %{have_virgl}
%files device-display-virtio-vga-gl
%{_libdir}/%{name}/hw-display-virtio-vga-gl.so
%endif
%if %{have_rutabaga_gfx}
%files device-display-virtio-vga-rutabaga
%{_libdir}/%{name}/hw-display-virtio-vga-rutabaga.so
%endif
%files device-usb-host
%{_libdir}/%{name}/hw-usb-host.so
%files device-usb-redirect
%{_libdir}/%{name}/hw-usb-redirect.so
%if %{have_libcacard}
%files device-usb-smartcard
%{_libdir}/%{name}/hw-usb-smartcard.so
%endif


%if %{have_virgl}
%files device-display-vhost-user-gpu
%{_datadir}/%{name}/vhost-user/50-qemu-gpu.json
%{_libexecdir}/vhost-user-gpu
%endif

%if %{have_spice}
%files audio-spice
%{_libdir}/%{name}/audio-spice.so
%files char-spice
%{_libdir}/%{name}/chardev-spice.so
%files device-display-qxl
%{_libdir}/%{name}/hw-display-qxl.so
%files ui-spice-core
%{_libdir}/%{name}/ui-spice-core.so
%files ui-spice-app
%{_libdir}/%{name}/ui-spice-app.so
%endif


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
%{_bindir}/qemu-hppa
%{_bindir}/qemu-hexagon
%{_bindir}/qemu-loongarch64
%{_bindir}/qemu-m68k
%{_bindir}/qemu-microblaze
%{_bindir}/qemu-microblazeel
%{_bindir}/qemu-mips
%{_bindir}/qemu-mipsel
%{_bindir}/qemu-mips64
%{_bindir}/qemu-mips64el
%{_bindir}/qemu-mipsn32
%{_bindir}/qemu-mipsn32el
%{_bindir}/qemu-or1k
%{_bindir}/qemu-ppc
%{_bindir}/qemu-ppc64
%{_bindir}/qemu-ppc64le
%{_bindir}/qemu-riscv32
%{_bindir}/qemu-riscv64
%{_bindir}/qemu-s390x
%{_bindir}/qemu-sh4
%{_bindir}/qemu-sh4eb
%{_bindir}/qemu-sparc
%{_bindir}/qemu-sparc32plus
%{_bindir}/qemu-sparc64
%{_bindir}/qemu-xtensa
%{_bindir}/qemu-xtensaeb

%{_datadir}/systemtap/tapset/qemu-aarch64.stp
%{_datadir}/systemtap/tapset/qemu-aarch64-log.stp
%{_datadir}/systemtap/tapset/qemu-aarch64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-aarch64_be.stp
%{_datadir}/systemtap/tapset/qemu-aarch64_be-log.stp
%{_datadir}/systemtap/tapset/qemu-aarch64_be-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-alpha.stp
%{_datadir}/systemtap/tapset/qemu-alpha-log.stp
%{_datadir}/systemtap/tapset/qemu-alpha-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-armeb.stp
%{_datadir}/systemtap/tapset/qemu-armeb-log.stp
%{_datadir}/systemtap/tapset/qemu-armeb-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-arm.stp
%{_datadir}/systemtap/tapset/qemu-arm-log.stp
%{_datadir}/systemtap/tapset/qemu-arm-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-hexagon.stp
%{_datadir}/systemtap/tapset/qemu-hexagon-log.stp
%{_datadir}/systemtap/tapset/qemu-hexagon-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-hppa.stp
%{_datadir}/systemtap/tapset/qemu-hppa-log.stp
%{_datadir}/systemtap/tapset/qemu-hppa-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-i386.stp
%{_datadir}/systemtap/tapset/qemu-i386-log.stp
%{_datadir}/systemtap/tapset/qemu-i386-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-loongarch64.stp
%{_datadir}/systemtap/tapset/qemu-loongarch64-log.stp
%{_datadir}/systemtap/tapset/qemu-loongarch64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-m68k.stp
%{_datadir}/systemtap/tapset/qemu-m68k-log.stp
%{_datadir}/systemtap/tapset/qemu-m68k-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-microblaze.stp
%{_datadir}/systemtap/tapset/qemu-microblaze-log.stp
%{_datadir}/systemtap/tapset/qemu-microblaze-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel-log.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mips.stp
%{_datadir}/systemtap/tapset/qemu-mips-log.stp
%{_datadir}/systemtap/tapset/qemu-mips-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mips64el.stp
%{_datadir}/systemtap/tapset/qemu-mips64el-log.stp
%{_datadir}/systemtap/tapset/qemu-mips64el-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mips64.stp
%{_datadir}/systemtap/tapset/qemu-mips64-log.stp
%{_datadir}/systemtap/tapset/qemu-mips64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mipsel.stp
%{_datadir}/systemtap/tapset/qemu-mipsel-log.stp
%{_datadir}/systemtap/tapset/qemu-mipsel-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32-log.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32el.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32el-log.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32el-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-or1k.stp
%{_datadir}/systemtap/tapset/qemu-or1k-log.stp
%{_datadir}/systemtap/tapset/qemu-or1k-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-ppc.stp
%{_datadir}/systemtap/tapset/qemu-ppc-log.stp
%{_datadir}/systemtap/tapset/qemu-ppc-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-ppc64.stp
%{_datadir}/systemtap/tapset/qemu-ppc64-log.stp
%{_datadir}/systemtap/tapset/qemu-ppc64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-ppc64le.stp
%{_datadir}/systemtap/tapset/qemu-ppc64le-log.stp
%{_datadir}/systemtap/tapset/qemu-ppc64le-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-riscv32.stp
%{_datadir}/systemtap/tapset/qemu-riscv32-log.stp
%{_datadir}/systemtap/tapset/qemu-riscv32-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-riscv64.stp
%{_datadir}/systemtap/tapset/qemu-riscv64-log.stp
%{_datadir}/systemtap/tapset/qemu-riscv64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-s390x.stp
%{_datadir}/systemtap/tapset/qemu-s390x-log.stp
%{_datadir}/systemtap/tapset/qemu-s390x-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sh4.stp
%{_datadir}/systemtap/tapset/qemu-sh4-log.stp
%{_datadir}/systemtap/tapset/qemu-sh4-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb-log.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sparc.stp
%{_datadir}/systemtap/tapset/qemu-sparc-log.stp
%{_datadir}/systemtap/tapset/qemu-sparc-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus-log.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-sparc64.stp
%{_datadir}/systemtap/tapset/qemu-sparc64-log.stp
%{_datadir}/systemtap/tapset/qemu-sparc64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-x86_64.stp
%{_datadir}/systemtap/tapset/qemu-x86_64-log.stp
%{_datadir}/systemtap/tapset/qemu-x86_64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-xtensa.stp
%{_datadir}/systemtap/tapset/qemu-xtensa-log.stp
%{_datadir}/systemtap/tapset/qemu-xtensa-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-xtensaeb.stp
%{_datadir}/systemtap/tapset/qemu-xtensaeb-log.stp
%{_datadir}/systemtap/tapset/qemu-xtensaeb-simpletrace.stp


%files user-binfmt
%{_exec_prefix}/lib/binfmt.d/qemu-*-dynamic.conf

%if %{user_static}
%files user-static
%license COPYING COPYING.LIB LICENSE

%files user-static-aarch64
%{_bindir}/qemu-aarch64-static
%{_bindir}/qemu-aarch64_be-static
%{_datadir}/systemtap/tapset/qemu-aarch64-log-static.stp
%{_datadir}/systemtap/tapset/qemu-aarch64-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-aarch64-static.stp
%{_datadir}/systemtap/tapset/qemu-aarch64_be-log-static.stp
%{_datadir}/systemtap/tapset/qemu-aarch64_be-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-aarch64_be-static.stp
%ifnarch aarch64
%{_exec_prefix}/lib/binfmt.d/qemu-aarch64-static.conf
%endif
%{_exec_prefix}/lib/binfmt.d/qemu-aarch64_be-static.conf

%files user-static-alpha
%{_bindir}/qemu-alpha-static
%{_datadir}/systemtap/tapset/qemu-alpha-log-static.stp
%{_datadir}/systemtap/tapset/qemu-alpha-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-alpha-static.stp
%{_exec_prefix}/lib/binfmt.d/qemu-alpha-static.conf

%files user-static-arm
%{_bindir}/qemu-arm-static
%{_bindir}/qemu-armeb-static
%{_datadir}/systemtap/tapset/qemu-arm-log-static.stp
%{_datadir}/systemtap/tapset/qemu-arm-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-arm-static.stp
%{_datadir}/systemtap/tapset/qemu-armeb-log-static.stp
%{_datadir}/systemtap/tapset/qemu-armeb-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-armeb-static.stp
%ifnarch aarch64
%{_exec_prefix}/lib/binfmt.d/qemu-arm-static.conf
%endif
%{_exec_prefix}/lib/binfmt.d/qemu-armeb-static.conf

%files user-static-hexagon
%{_bindir}/qemu-hexagon-static
%{_datadir}/systemtap/tapset/qemu-hexagon-log-static.stp
%{_datadir}/systemtap/tapset/qemu-hexagon-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-hexagon-static.stp
%{_exec_prefix}/lib/binfmt.d/qemu-hexagon-static.conf

%files user-static-hppa
%{_bindir}/qemu-hppa-static
%{_datadir}/systemtap/tapset/qemu-hppa-log-static.stp
%{_datadir}/systemtap/tapset/qemu-hppa-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-hppa-static.stp
%{_exec_prefix}/lib/binfmt.d/qemu-hppa-static.conf

%files user-static-loongarch64
%{_bindir}/qemu-loongarch64-static
%{_datadir}/systemtap/tapset/qemu-loongarch64-log-static.stp
%{_datadir}/systemtap/tapset/qemu-loongarch64-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-loongarch64-static.stp
%{_exec_prefix}/lib/binfmt.d/qemu-loongarch64-static.conf

%files user-static-m68k
%{_bindir}/qemu-m68k-static
%{_datadir}/systemtap/tapset/qemu-m68k-log-static.stp
%{_datadir}/systemtap/tapset/qemu-m68k-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-m68k-static.stp
%{_exec_prefix}/lib/binfmt.d/qemu-m68k-static.conf

%files user-static-microblaze
%{_bindir}/qemu-microblaze-static
%{_bindir}/qemu-microblazeel-static
%{_datadir}/systemtap/tapset/qemu-microblaze-log-static.stp
%{_datadir}/systemtap/tapset/qemu-microblaze-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-microblaze-static.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel-log-static.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-microblazeel-static.stp
%{_exec_prefix}/lib/binfmt.d/qemu-microblaze-static.conf
%{_exec_prefix}/lib/binfmt.d/qemu-microblazeel-static.conf

%files user-static-mips
%{_bindir}/qemu-mips-static
%{_bindir}/qemu-mips64-static
%{_bindir}/qemu-mips64el-static
%{_bindir}/qemu-mipsel-static
%{_bindir}/qemu-mipsn32-static
%{_bindir}/qemu-mipsn32el-static
%{_datadir}/systemtap/tapset/qemu-mips-log-static.stp
%{_datadir}/systemtap/tapset/qemu-mips-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-mips-static.stp
%{_datadir}/systemtap/tapset/qemu-mips64-log-static.stp
%{_datadir}/systemtap/tapset/qemu-mips64-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-mips64-static.stp
%{_datadir}/systemtap/tapset/qemu-mips64el-log-static.stp
%{_datadir}/systemtap/tapset/qemu-mips64el-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-mips64el-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsel-log-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsel-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsel-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32-log-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32el-log-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32el-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-mipsn32el-static.stp
%{_exec_prefix}/lib/binfmt.d/qemu-mips-static.conf
%{_exec_prefix}/lib/binfmt.d/qemu-mips64-static.conf
%{_exec_prefix}/lib/binfmt.d/qemu-mips64el-static.conf
%{_exec_prefix}/lib/binfmt.d/qemu-mipsel-static.conf
%{_exec_prefix}/lib/binfmt.d/qemu-mipsn32-static.conf
%{_exec_prefix}/lib/binfmt.d/qemu-mipsn32el-static.conf

%files user-static-or1k
%{_bindir}/qemu-or1k-static
%{_datadir}/systemtap/tapset/qemu-or1k-log-static.stp
%{_datadir}/systemtap/tapset/qemu-or1k-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-or1k-static.stp
%{_exec_prefix}/lib/binfmt.d/qemu-or1k-static.conf

%files user-static-ppc
%{_bindir}/qemu-ppc-static
%{_bindir}/qemu-ppc64-static
%{_bindir}/qemu-ppc64le-static
%{_datadir}/systemtap/tapset/qemu-ppc-log-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc64-log-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc64-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc64-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc64le-log-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc64le-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-ppc64le-static.stp
%{_exec_prefix}/lib/binfmt.d/qemu-ppc-static.conf
%{_exec_prefix}/lib/binfmt.d/qemu-ppc64-static.conf
%ifnarch ppc64le
%{_exec_prefix}/lib/binfmt.d/qemu-ppc64le-static.conf
%endif

%files user-static-riscv
%{_bindir}/qemu-riscv32-static
%{_bindir}/qemu-riscv64-static
%{_datadir}/systemtap/tapset/qemu-riscv32-log-static.stp
%{_datadir}/systemtap/tapset/qemu-riscv32-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-riscv32-static.stp
%{_datadir}/systemtap/tapset/qemu-riscv64-log-static.stp
%{_datadir}/systemtap/tapset/qemu-riscv64-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-riscv64-static.stp
%{_exec_prefix}/lib/binfmt.d/qemu-riscv32-static.conf
%ifnarch riscv64
%{_exec_prefix}/lib/binfmt.d/qemu-riscv64-static.conf
%endif

%files user-static-s390x
%{_bindir}/qemu-s390x-static
%{_datadir}/systemtap/tapset/qemu-s390x-log-static.stp
%{_datadir}/systemtap/tapset/qemu-s390x-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-s390x-static.stp
%ifnarch s390x
%{_exec_prefix}/lib/binfmt.d/qemu-s390x-static.conf
%endif

%files user-static-sh4
%{_bindir}/qemu-sh4-static
%{_bindir}/qemu-sh4eb-static
%{_datadir}/systemtap/tapset/qemu-sh4-log-static.stp
%{_datadir}/systemtap/tapset/qemu-sh4-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-sh4-static.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb-log-static.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-sh4eb-static.stp
%{_exec_prefix}/lib/binfmt.d/qemu-sh4-static.conf
%{_exec_prefix}/lib/binfmt.d/qemu-sh4eb-static.conf

%files user-static-sparc
%{_bindir}/qemu-sparc-static
%{_bindir}/qemu-sparc32plus-static
%{_bindir}/qemu-sparc64-static
%{_datadir}/systemtap/tapset/qemu-sparc-log-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc64-log-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc64-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc64-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus-log-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-sparc32plus-static.stp
%{_exec_prefix}/lib/binfmt.d/qemu-sparc-static.conf
%{_exec_prefix}/lib/binfmt.d/qemu-sparc32plus-static.conf
%{_exec_prefix}/lib/binfmt.d/qemu-sparc64-static.conf

%files user-static-x86
%{_bindir}/qemu-i386-static
%{_bindir}/qemu-x86_64-static
%{_datadir}/systemtap/tapset/qemu-i386-log-static.stp
%{_datadir}/systemtap/tapset/qemu-i386-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-i386-static.stp
%{_datadir}/systemtap/tapset/qemu-x86_64-log-static.stp
%{_datadir}/systemtap/tapset/qemu-x86_64-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-x86_64-static.stp
%ifnarch %{ix86} x86_64
%{_exec_prefix}/lib/binfmt.d/qemu-i386-static.conf
%{_exec_prefix}/lib/binfmt.d/qemu-i486-static.conf
%{_exec_prefix}/lib/binfmt.d/qemu-x86_64-static.conf
%endif

%files user-static-xtensa
%{_bindir}/qemu-xtensa-static
%{_bindir}/qemu-xtensaeb-static
%{_datadir}/systemtap/tapset/qemu-xtensa-log-static.stp
%{_datadir}/systemtap/tapset/qemu-xtensa-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-xtensa-static.stp
%{_datadir}/systemtap/tapset/qemu-xtensaeb-log-static.stp
%{_datadir}/systemtap/tapset/qemu-xtensaeb-simpletrace-static.stp
%{_datadir}/systemtap/tapset/qemu-xtensaeb-static.stp
%{_exec_prefix}/lib/binfmt.d/qemu-xtensa-static.conf
%{_exec_prefix}/lib/binfmt.d/qemu-xtensaeb-static.conf

%endif


%files system-aarch64
%files system-aarch64-core
%{_bindir}/qemu-system-aarch64
%{_datadir}/systemtap/tapset/qemu-system-aarch64.stp
%{_datadir}/systemtap/tapset/qemu-system-aarch64-log.stp
%{_datadir}/systemtap/tapset/qemu-system-aarch64-simpletrace.stp
%{_mandir}/man1/qemu-system-aarch64.1*


%files system-alpha
%files system-alpha-core
%{_bindir}/qemu-system-alpha
%{_datadir}/systemtap/tapset/qemu-system-alpha.stp
%{_datadir}/systemtap/tapset/qemu-system-alpha-log.stp
%{_datadir}/systemtap/tapset/qemu-system-alpha-simpletrace.stp
%{_mandir}/man1/qemu-system-alpha.1*
%{_datadir}/%{name}/palcode-clipper


%files system-arm
%files system-arm-core
%{_bindir}/qemu-system-arm
%{_datadir}/%{name}/npcm7xx_bootrom.bin
%{_datadir}/systemtap/tapset/qemu-system-arm.stp
%{_datadir}/systemtap/tapset/qemu-system-arm-log.stp
%{_datadir}/systemtap/tapset/qemu-system-arm-simpletrace.stp
%{_mandir}/man1/qemu-system-arm.1*


%files system-avr
%files system-avr-core
%{_bindir}/qemu-system-avr
%{_datadir}/systemtap/tapset/qemu-system-avr.stp
%{_datadir}/systemtap/tapset/qemu-system-avr-log.stp
%{_datadir}/systemtap/tapset/qemu-system-avr-simpletrace.stp
%{_mandir}/man1/qemu-system-avr.1*


%files system-hppa
%files system-hppa-core
%{_bindir}/qemu-system-hppa
%{_datadir}/systemtap/tapset/qemu-system-hppa.stp
%{_datadir}/systemtap/tapset/qemu-system-hppa-log.stp
%{_datadir}/systemtap/tapset/qemu-system-hppa-simpletrace.stp
%{_mandir}/man1/qemu-system-hppa.1*
%{_datadir}/%{name}/hppa-firmware.img
%{_datadir}/%{name}/hppa-firmware64.img


%files system-loongarch64
%files system-loongarch64-core
%{_bindir}/qemu-system-loongarch64
%{_datadir}/systemtap/tapset/qemu-system-loongarch64.stp
%{_datadir}/systemtap/tapset/qemu-system-loongarch64-log.stp
%{_datadir}/systemtap/tapset/qemu-system-loongarch64-simpletrace.stp
%{_mandir}/man1/qemu-system-loongarch64.1*


%files system-m68k
%files system-m68k-core
%{_bindir}/qemu-system-m68k
%{_datadir}/systemtap/tapset/qemu-system-m68k.stp
%{_datadir}/systemtap/tapset/qemu-system-m68k-log.stp
%{_datadir}/systemtap/tapset/qemu-system-m68k-simpletrace.stp
%{_mandir}/man1/qemu-system-m68k.1*


%files system-microblaze
%files system-microblaze-core
%{_bindir}/qemu-system-microblaze
%{_bindir}/qemu-system-microblazeel
%{_datadir}/systemtap/tapset/qemu-system-microblaze.stp
%{_datadir}/systemtap/tapset/qemu-system-microblaze-log.stp
%{_datadir}/systemtap/tapset/qemu-system-microblaze-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-system-microblazeel.stp
%{_datadir}/systemtap/tapset/qemu-system-microblazeel-log.stp
%{_datadir}/systemtap/tapset/qemu-system-microblazeel-simpletrace.stp
%{_mandir}/man1/qemu-system-microblaze.1*
%{_mandir}/man1/qemu-system-microblazeel.1*
%{_datadir}/%{name}/petalogix*.dtb


%files system-mips
%files system-mips-core
%{_bindir}/qemu-system-mips
%{_bindir}/qemu-system-mipsel
%{_bindir}/qemu-system-mips64
%{_bindir}/qemu-system-mips64el
%{_datadir}/systemtap/tapset/qemu-system-mips.stp
%{_datadir}/systemtap/tapset/qemu-system-mips-log.stp
%{_datadir}/systemtap/tapset/qemu-system-mips-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-system-mipsel.stp
%{_datadir}/systemtap/tapset/qemu-system-mipsel-log.stp
%{_datadir}/systemtap/tapset/qemu-system-mipsel-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-system-mips64.stp
%{_datadir}/systemtap/tapset/qemu-system-mips64-log.stp
%{_datadir}/systemtap/tapset/qemu-system-mips64-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-system-mips64el.stp
%{_datadir}/systemtap/tapset/qemu-system-mips64el-log.stp
%{_datadir}/systemtap/tapset/qemu-system-mips64el-simpletrace.stp
%{_mandir}/man1/qemu-system-mips.1*
%{_mandir}/man1/qemu-system-mipsel.1*
%{_mandir}/man1/qemu-system-mips64el.1*
%{_mandir}/man1/qemu-system-mips64.1*


%files system-or1k
%files system-or1k-core
%{_bindir}/qemu-system-or1k
%{_datadir}/systemtap/tapset/qemu-system-or1k.stp
%{_datadir}/systemtap/tapset/qemu-system-or1k-log.stp
%{_datadir}/systemtap/tapset/qemu-system-or1k-simpletrace.stp
%{_mandir}/man1/qemu-system-or1k.1*


%files system-ppc
%files system-ppc-core
%{_bindir}/qemu-system-ppc
%{_bindir}/qemu-system-ppc64
%{_datadir}/systemtap/tapset/qemu-system-ppc.stp
%{_datadir}/systemtap/tapset/qemu-system-ppc-log.stp
%{_datadir}/systemtap/tapset/qemu-system-ppc-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-system-ppc64.stp
%{_datadir}/systemtap/tapset/qemu-system-ppc64-log.stp
%{_datadir}/systemtap/tapset/qemu-system-ppc64-simpletrace.stp
%{_mandir}/man1/qemu-system-ppc.1*
%{_mandir}/man1/qemu-system-ppc64.1*
%{_datadir}/%{name}/bamboo.dtb
%{_datadir}/%{name}/canyonlands.dtb
%{_datadir}/%{name}/qemu_vga.ndrv
%{_datadir}/%{name}/skiboot.lid
%{_datadir}/%{name}/u-boot.e500
%{_datadir}/%{name}/u-boot-sam460-20100605.bin
%{_datadir}/%{name}/vof*.bin
%if %{have_memlock_limits}
%{_sysconfdir}/security/limits.d/95-kvm-memlock.conf
%endif


%files system-riscv
%files system-riscv-core
%{_bindir}/qemu-system-riscv32
%{_bindir}/qemu-system-riscv64
%{_datadir}/%{name}/opensbi-riscv*.bin
%{_datadir}/systemtap/tapset/qemu-system-riscv32.stp
%{_datadir}/systemtap/tapset/qemu-system-riscv32-log.stp
%{_datadir}/systemtap/tapset/qemu-system-riscv32-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-system-riscv64.stp
%{_datadir}/systemtap/tapset/qemu-system-riscv64-log.stp
%{_datadir}/systemtap/tapset/qemu-system-riscv64-simpletrace.stp
%{_mandir}/man1/qemu-system-riscv*.1*


%files system-rx
%files system-rx-core
%{_bindir}/qemu-system-rx
%{_datadir}/systemtap/tapset/qemu-system-rx.stp
%{_datadir}/systemtap/tapset/qemu-system-rx-log.stp
%{_datadir}/systemtap/tapset/qemu-system-rx-simpletrace.stp
%{_mandir}/man1/qemu-system-rx.1*


%files system-s390x
%files system-s390x-core
%{_bindir}/qemu-system-s390x
%{_datadir}/systemtap/tapset/qemu-system-s390x.stp
%{_datadir}/systemtap/tapset/qemu-system-s390x-log.stp
%{_datadir}/systemtap/tapset/qemu-system-s390x-simpletrace.stp
%{_mandir}/man1/qemu-system-s390x.1*
%{_datadir}/%{name}/s390-ccw.img


%files system-sh4
%files system-sh4-core
%{_bindir}/qemu-system-sh4
%{_bindir}/qemu-system-sh4eb
%{_datadir}/systemtap/tapset/qemu-system-sh4.stp
%{_datadir}/systemtap/tapset/qemu-system-sh4-log.stp
%{_datadir}/systemtap/tapset/qemu-system-sh4-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-system-sh4eb.stp
%{_datadir}/systemtap/tapset/qemu-system-sh4eb-log.stp
%{_datadir}/systemtap/tapset/qemu-system-sh4eb-simpletrace.stp
%{_mandir}/man1/qemu-system-sh4.1*
%{_mandir}/man1/qemu-system-sh4eb.1*


%files system-sparc
%files system-sparc-core
%{_bindir}/qemu-system-sparc
%{_bindir}/qemu-system-sparc64
%{_datadir}/systemtap/tapset/qemu-system-sparc.stp
%{_datadir}/systemtap/tapset/qemu-system-sparc-log.stp
%{_datadir}/systemtap/tapset/qemu-system-sparc-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-system-sparc64.stp
%{_datadir}/systemtap/tapset/qemu-system-sparc64-log.stp
%{_datadir}/systemtap/tapset/qemu-system-sparc64-simpletrace.stp
%{_mandir}/man1/qemu-system-sparc.1*
%{_mandir}/man1/qemu-system-sparc64.1*
%{_datadir}/%{name}/QEMU,tcx.bin
%{_datadir}/%{name}/QEMU,cgthree.bin


%files system-tricore
%files system-tricore-core
%{_bindir}/qemu-system-tricore
%{_datadir}/systemtap/tapset/qemu-system-tricore.stp
%{_datadir}/systemtap/tapset/qemu-system-tricore-log.stp
%{_datadir}/systemtap/tapset/qemu-system-tricore-simpletrace.stp
%{_mandir}/man1/qemu-system-tricore.1*


%files system-x86
%files system-x86-core
%{_bindir}/qemu-system-i386
%{_bindir}/qemu-system-x86_64
%{_libdir}/%{name}/accel-tcg-i386.so
%{_libdir}/%{name}/accel-tcg-x86_64.so
%if %{with systemtap}
%{_datadir}/systemtap/tapset/qemu-system-i386.stp
%{_datadir}/systemtap/tapset/qemu-system-i386-log.stp
%{_datadir}/systemtap/tapset/qemu-system-i386-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-system-x86_64.stp
%{_datadir}/systemtap/tapset/qemu-system-x86_64-log.stp
%{_datadir}/systemtap/tapset/qemu-system-x86_64-simpletrace.stp
%endif
%{_mandir}/man1/qemu-system-i386.1*
%{_mandir}/man1/qemu-system-x86_64.1*
%{_datadir}/%{name}/kvmvapic.bin
%{_datadir}/%{name}/linuxboot.bin
%{_datadir}/%{name}/multiboot.bin
%{_datadir}/%{name}/multiboot_dma.bin
%{_datadir}/%{name}/pvh.bin
%{_datadir}/%{name}/qboot.rom
%if %{need_qemu_kvm}
%{_bindir}/qemu-kvm
%{_mandir}/man1/qemu-kvm.1*
%endif
%if %{have_vmsr_helper}
%{_bindir}/qemu-vmsr-helper
%{_unitdir}/qemu-vmsr-helper.service
%{_unitdir}/qemu-vmsr-helper.socket
%endif


%files system-xtensa
%files system-xtensa-core
%{_bindir}/qemu-system-xtensa
%{_bindir}/qemu-system-xtensaeb
%{_datadir}/systemtap/tapset/qemu-system-xtensa.stp
%{_datadir}/systemtap/tapset/qemu-system-xtensa-log.stp
%{_datadir}/systemtap/tapset/qemu-system-xtensa-simpletrace.stp
%{_datadir}/systemtap/tapset/qemu-system-xtensaeb.stp
%{_datadir}/systemtap/tapset/qemu-system-xtensaeb-log.stp
%{_datadir}/systemtap/tapset/qemu-system-xtensaeb-simpletrace.stp
%{_mandir}/man1/qemu-system-xtensa.1*
%{_mandir}/man1/qemu-system-xtensaeb.1*
# endif !tools_only
%endif


%changelog
* Mon Feb 24 2025 Phantom X <megaphantomx at hotmail dot com> - 2:9.2.2-100
- 9.2.2

* Wed Feb 12 2025 Phantom X <megaphantomx at hotmail dot com> - 2:9.2.1-100
- 9.2.1

* Wed Dec 11 2024 Phantom X <megaphantomx at hotmail dot com> - 2:9.2.0-100
- 9.2.0

* Wed Dec 11 2024 Phantom X <megaphantomx at hotmail dot com> - 2:9.1.2-101
- f41 sync

* Thu Nov 21 2024 Phantom X <megaphantomx at hotmail dot com> - 2:9.1.2-100
- 9.1.2

* Mon Oct 21 2024 Phantom X <megaphantomx at hotmail dot com> - 2:9.1.1-100
- 9.1.1

* Fri Sep 20 2024 Phantom X <megaphantomx at hotmail dot com> - 2:9.1.0-101
- Rawhide sync

* Wed Sep 04 2024 Phantom X <megaphantomx at hotmail dot com> - 2:9.1.0-100
- 9.1.0

* Wed Jul 17 2024 Phantom X <megaphantomx at hotmail dot com> - 2:9.0.2-100
- 9.0.2

* Wed Jun 12 2024 Phantom X <megaphantomx at hotmail dot com> - 2:9.0.1-100
- 9.0.1

* Wed Apr 24 2024 Phantom X <megaphantomx at hotmail dot com> - 2:9.0.0-100
- 9.0.0
- Rawhide sync

* Mon Mar 04 2024 Phantom X <megaphantomx at hotmail dot com> - 2:8.2.2-100
- 8.2.2

* Tue Jan 30 2024 Phantom X <megaphantomx at hotmail dot com> - 2:8.2.1-100
- 8.2.1

* Mon Dec 25 2023 Phantom X <megaphantomx at hotmail dot com> - 2:8.2.0-100
- 8.2.0

* Thu Nov 23 2023 Phantom X <megaphantomx at hotmail dot com> - 2:8.1.3-100
- 8.1.3

* Mon Oct 16 2023 Phantom X <megaphantomx at hotmail dot com> - 2:8.1.2-100
- 8.1.2

* Sun Sep 24 2023 Phantom X <megaphantomx at hotmail dot com> - 2:8.1.1-100
- 8.1.1

* Fri Aug 25 2023 Phantom X <megaphantomx at hotmail dot com> - 2:8.1.0-100
- 8.1.0

* Mon Aug 21 2023 Phantom X <megaphantomx at hotmail dot com> - 2:8.0.4-100
- 8.0.4

* Thu Jul 13 2023 Phantom X <megaphantomx at hotmail dot com> - 2:8.0.3-100
- 8.0.3

* Thu Jun 01 2023 Phantom X <megaphantomx at hotmail dot com> - 2:8.0.2-100
- 8.0.2

* Mon May 01 2023 Phantom X <megaphantomx at hotmail dot com> - 2:8.0.0-101
- Rawhide sync

* Wed Apr 26 2023 Phantom X <megaphantomx at hotmail dot com> - 2:8.0.0-100
- 8.0.0
- Rawhide sync

* Fri Apr 07 2023 Phantom X <megaphantomx at hotmail dot com> - 2:7.2.1-100
- 7.2.1

* Wed Mar 15 2023 Phantom X <megaphantomx at hotmail dot com> - 2:7.2.0-101
- Rawhide sync

* Fri Dec 23 2022 Phantom X <megaphantomx at hotmail dot com> - 2:7.2.0-100
- 7.2.0

* Thu Sep 01 2022 Phantom X <megaphantomx at hotmail dot com> - 2:7.1.0-100
- 7.1.0

* Sun May 29 2022 Phantom X <megaphantomx at hotmail dot com> - 2:7.0.0-101
- Rawhide sync
- Some upstream patches

* Fri Apr 22 2022 Phantom X <megaphantomx at hotmail dot com> - 2:7.0.0-100
- 7.0.0
- Rawhide sync

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 2:6.2.0-101
- Rawhide sync

* Wed Dec 15 2021 Phantom X <megaphantomx at hotmail dot com> - 2:6.2.0-100
- 6.2.0

* Thu Dec 09 2021 Phantom X <megaphantomx at hotmail dot com> - 2:6.2.0~rc4-100
- 6.2.0-rc4

* Sat Nov 13 2021 Phantom X <megaphantomx at hotmail dot com> - 2:6.1.0-103
- Rawhide sync

* Fri Sep 24 2021 Phantom X <megaphantomx at hotmail dot com> - 2:6.1.0-102
- Rawhide sync

* Fri Aug 27 2021 Phantom X <megaphantomx at hotmail dot com> - 2:6.1.0-101
- Rawhide sync (gnutls fix)

* Tue Aug 24 2021 Phantom X <megaphantomx at hotmail dot com> - 2:6.1.0-100
- 6.1.0
- Rawhide sync

* Sun Jul 25 2021 Phantom X <megaphantomx at hotmail dot com> - 2:6.0.0-101
- Rawhide sync

* Fri Apr 30 2021 Phantom X <megaphantomx at hotmail dot com> - 2:6.0.0-100
- 6.0.0
- Rawhide sync
- Use sysusers compat macro

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 2:5.2.0-101
- f34 sync

* Wed Dec 09 2020 Phantom X <megaphantomx at hotmail dot com> - 2:5.2.0-100
- 5.2.0

* Sat Dec 05 2020 Phantom X <megaphantomx at hotmail dot com> - 2:5.2.0~rc4-100
- 5.2.0-rc4

* Mon Nov 30 2020 Phantom X <megaphantomx at hotmail dot com> - 2:5.2.0~rc3-100
- 5.2.0-rc3
- Rawhide sync

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
