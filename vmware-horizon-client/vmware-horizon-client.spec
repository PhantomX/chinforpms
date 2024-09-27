# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

# Adapted from: https://github.com/rathann/vmware-horizon-client

%undefine _missing_build_ids_terminate_build
%global debug_package %{nil}
%undefine _unique_build_ids
%global _build_id_links none
%global _no_recompute_build_ids 1

%global cart   25FQ2
%global yymm   2406
%global pdfver %(echo %{yymm} | tr -d '.' )
%global pdfiver %(echo %{yymm} | cut -d. -f1 )
%global ver    8.13.0
%global rel    9995429239
%global fver   %{yymm}-%{ver}-%{rel}
%ifarch x86_64
%global mark64 ()(64bit)
%global vhc_arch x64
%else
%global mark64 %nil
%global vhc_arch armhf
%endif
%if 0%{?fedora} > 39
%bcond bundled_ssl 0
%else
%bcond bundled_ssl 1
%endif

%global cef_ver 126.0.6478.127
%global ffmpeg_ver 6.1.1
%global libpng_ver 1.6.37
%global webrtc_ver 90

Name:           vmware-horizon-client
Version:        %{yymm}.%{ver}.%{rel}
Release:        1%{?dist}
Summary:        Remote access client for VMware Horizon

License:        VMware
URL:            https://www.vmware.com/products/horizon.html

# https://customerconnect.vmware.com/en/downloads/info/slug/desktop_end_user_computing/vmware_horizon_clients/horizon_8
Source0:        https://download3.omnissa.com/software/CART%{cart}_LIN_%{yymm}_TARBALL/VMware-Horizon-Client-Linux-%{yymm}-%{ver}-%{rel}.tar.gz
%dnl Source1:        https://docs.omnissa.com/en/VMware-Horizon-Client-for-Linux/%{yymm}/rn/vmware-horizon-client-for-linux-%{pdfver}-release-notes/vmware-horizon-client-for-linux-%{pdfver}-release-notes.pdf
%dnl Source2:        https://docs.omnissa.com/en/VMware-Horizon-Client-for-Linux/%{pdfiver}/horizon-client-linux-installation.pdf
Source3:        https://docs.broadcom.com/doc/end-user-agreement-english#/end-user-agreement-english.pdf
Source10:       usbarb.rules
Source11:       vmware-eucusbarbitrator.service
Source14:       vmware-eucusbarbitrator.preset
Source15:       vmware-ftsprhv.preset
Source16:       vmware-ftscanhv.preset

ExclusiveArch:  armv7hl x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  %{_bindir}/execstack
BuildRequires:  systemd-rpm-macros
BuildRequires:  ImageMagick

Provides:       bundled(atk) = 2.28.1
Provides:       bundled(boost) = 1.67
Provides:       bundled(bzip2) = 1.0.6
Provides:       bundled(c-ares) = 1.13.0
Provides:       bundled(curl) = 7.74
Provides:       bundled(gtkmm30) = 3.10.1
Provides:       bundled(hal) = 0.5.12
Provides:       bundled(icu) = 60.2
Provides:       bundled(libjpeg-turbo) = 1.4.2
Provides:       bundled(libwebrtc) = %{webrtc_ver}
Provides:       bundled(libxml2) = 2.9.9
Provides:       bundled(mechanical-fonts) = 1.00
%if %{with bundled_ssl}
Provides:       bundled(curl) = 8.5.0
Provides:       bundled(openssl) = 3.0.12
%endif
Provides:       bundled(opus) = 1.1.4.60
Provides:       bundled(speex) = 1.2rc3
Provides:       bundled(zlib) = 1.2.11
Provides:       %{name}-seamless-window = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-media-provider < 2303.8.9.0.21435420
Obsoletes:      %{name}-seamless-window < 5.2.0.14604769
Requires:       %{_bindir}/pidof
Requires:       libudev.so.1%{mark64}

%global __provides_exclude_from ^%{_libdir}/(vmware|pcoip)/.*$
%global __requires_exclude ^libatkmm-.*\\.so.*$
%global __requires_exclude %__requires_exclude|^libav(codec|util)\\.so.*$
%global __requires_exclude %__requires_exclude|^libcef\\.so.*$
%global __requires_exclude %__requires_exclude|^libclientSdkCPrimitive\\.so.*$
%global __requires_exclude %__requires_exclude|^libcrtbora\\.so.*$
%global __requires_exclude %__requires_exclude|^libgiomm-.*.so.*$
%global __requires_exclude %__requires_exclude|^libglibmm-.*.so.*$
%global __requires_exclude %__requires_exclude|^libgdkmm-.*.so.*$
%global __requires_exclude %__requires_exclude|^libgtkmm-.*.so.*$
%global __requires_exclude %__requires_exclude|^libpangomm-.*.so.*$
%if %{with bundled_ssl}
%global __requires_exclude %__requires_exclude|^libcrypto\\.so.*$
%global __requires_exclude %__requires_exclude|^libcurl\\.so.*$
%global __requires_exclude %__requires_exclude|^libssl\\.so.*$
%endif
%global __requires_exclude %__requires_exclude|^libGLESv2\\.so.*$
%global __requires_exclude %__requires_exclude|^libMicrosoft.SlimCV.VBM\\.so.*$
%global __requires_exclude %__requires_exclude|^libudev\\.so.*$
%global __requires_exclude %__requires_exclude|^libvmwarebase\\.so.*$
%global __requires_exclude %__requires_exclude|^libvmware-view-usbd\\.so.*$
%global __requires_exclude %__requires_exclude|^libx264\\.so.*$


%description
Remote access client for VMware Horizon.

Requires Horizon Agent 7.0 or later on the virtual desktop.

%package html5mmr
Summary:        HTML5 Multimedia Redirection support plugin for VMware Horizon Client
Provides:       bundled(chromium-embedded-framework) = %{cef_ver}
Provides:       bundled(webrtc) = %{webrtc_ver}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description html5mmr
HTML5 Multimedia Redirection support plugin for VMware Horizon Client.

Requires Horizon Agent 7.9 or later on the virtual desktop.

%package integrated-printing
Summary:        Integrated Printing support plugin for VMware Horizon Client
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description integrated-printing
Integrated Printing support plugin for VMware Horizon Client.

%package mmr
Summary:        Multimedia Redirection support plugin for VMware Horizon Client
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libgstlibav.so%{mark64}
Recommends:     gstreamer1-vaapi%{_isa}

%description mmr
Multimedia Redirection support plugin for VMware Horizon Client.

Requires Horizon Agent 7.0 or later on the virtual desktop.

%package pcoip
Summary:        PCoIP support plugin for VMware Horizon Client
Provides:       bundled(libavcodec) = %{ffmpeg_ver}
Provides:       bundled(libavformat) = %{ffmpeg_ver}
Provides:       bundled(libavutil) = %{ffmpeg_ver}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       bundled(libpng) = %{libpng_ver}
Provides:       bundled(pcoip-soft-clients) = 3.75

%description pcoip
PCoIP support plugin for VMware Horizon Client.

Requires Horizon Agent 7.0.2 or later on the virtual desktop.

%package rtav
Summary:        Real-Time Audio-Video support plugin for VMware Horizon Client
Requires:       %{name}-pcoip = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libspeex.so.1%{mark64}
Requires:       libtheoradec.so.1%{mark64}
Requires:       libtheoraenc.so.1%{mark64}
%ifarch x86_64
Provides:       bundled(x264-libs) = 0.164
%endif

%description rtav
Real-Time Audio-Video support plugin for VMware Horizon Client.

Requires Horizon Agent 7.0 or later on the virtual desktop.

%package scannerclient
Summary:        Scanner redirection support plugin for VMware Horizon Client
Provides:       bundled(scanner_linux) = 2.6.3
%{?systemd_requires}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libudev.so.1%{mark64}
Requires(post): %{_sbindir}/semodule
Requires(postun): %{_sbindir}/semodule

%description scannerclient
The Scanner Redirection component allows you to use local scanner devices from a
remote desktop.

Requires Horizon Agent 7.8 or later on the virtual desktop.

%package serialportclient
Summary:        Serial port redirection support plugin for VMware Horizon Client
Provides:       bundled(serial_linux) = 2.6.3
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libudev.so.1%{mark64}

%description serialportclient
Serial port redirection support plugin for VMware Horizon Client.

Requires Horizon Agent 7.6 or later on the virtual desktop.

%package smartcard
Summary:        SmartCard authentication support plugin for VMware Horizon Client
Requires:       %{name}-pcoip = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       opensc%{_isa}

%description smartcard
SmartCard authentication support plugin for VMware Horizon Client.

%package teams
Summary:        Media Optimization for Microsoft Teams support plugin for VMware Horizon Client
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description teams
The Media Optimization for Microsoft Teams redirects audio calls, video calls,
and viewing desktop shares for a seamless experience between the client system
and the remote session without negatively affecting the virtual infrastructure
and overloading the network. Microsoft Teams media processing takes place on the
client machine instead of in the virtual desktop and does not rely on Real-Time
Audio-Video (RTAV).

%package tsdr
Summary:        Client Drive Redirection support plugin for VMware Horizon Client
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description tsdr
Client Drive Redirection support plugin for VMware Horizon Client.

%package usb
Summary:        USB Redirection support plugin for VMware Horizon Client
BuildRequires:  systemd
%{?systemd_requires}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires(post): %{_sbindir}/semodule
Requires(postun): %{_sbindir}/semodule

%description usb
USB Redirection support plugin for VMware Horizon Client.


%prep
%autosetup -N -n VMware-Horizon-Client-Linux-%{yymm}-%{ver}-%{rel}
%dnl cp -p %{S:1} %{S:2} ./
cp -p %{S:3} ./

cp -p %{S:10} %{S:11} %{S:14} %{S:15} %{S:16} ./

cat > %{name}-scannerclient-rpm.cil << 'EOF'
(typeattributeset cil_gen_require init_t)
(typeattributeset cil_gen_require printer_device_t)
(typeattributeset cil_gen_require tmp_t)
(typeattributeset cil_gen_require usb_device_t)
(typeattributeset cil_gen_require v4l_device_t)
(allow init_t tmp_t (sock_file (create setattr unlink)))
(allow init_t printer_device_t (chr_file (open read)))
(allow init_t usb_device_t (chr_file (ioctl open read write)))
(allow init_t v4l_device_t (chr_file (ioctl open read write)))
EOF

cat > %{name}-usb-rpm.cil << 'EOF'
(typeattributeset cil_gen_require init_t)
(typeattributeset cil_gen_require var_log_t)
(typeattributeset cil_gen_require vmware_log_t)
(typeattributeset cil_gen_require vmware_sys_conf_t)
(allow init_t var_log_t (file (create unlink)))
(allow init_t vmware_log_t (file (getattr unlink)))
(allow init_t vmware_sys_conf_t (dir (add_name remove_name write)))
(allow init_t vmware_sys_conf_t (file (create rename setattr unlink write)))
EOF

mkdir -p %{_vpath_builddir}/usr
for f in \
  VMware-Horizon-Client-%{yymm}-%{ver}-%{rel}.%{vhc_arch}.tar.gz \
  VMware-Horizon-PCoIP-%{yymm}-%{ver}-%{rel}.%{vhc_arch}.tar.gz \
  VMware-Horizon-USB-%{yymm}-%{ver}-%{rel}.%{vhc_arch}.tar.gz \
%ifarch x86_64
  VMware-Horizon-html5mmr-%{yymm}-%{ver}-%{rel}.%{vhc_arch}.tar.gz \
  VMware-Horizon-integratedPrinting-%{yymm}-%{ver}-%{rel}.%{vhc_arch}.tar.gz \
  VMware-Horizon-scannerClient-%{yymm}-%{ver}-%{rel}.%{vhc_arch}.tar.gz \
  VMware-Horizon-serialportClient-%{yymm}-%{ver}-%{rel}.%{vhc_arch}.tar.gz \
%endif
; do
  tar xzf %{vhc_arch}/${f} -C %{_vpath_builddir} --strip-components=1
done

pushd %{_vpath_builddir}
mv -v usr/share/doc/%{name} ../docs
mv -v systemd ../
mv -v etc/vmware ../
mv -v usr/lib{,/vmware}/libclientSdkCPrimitive.so
mv -v usr/lib{,/vmware}/libpcoip_client.so
%ifarch armv7hl
mv -v usr/lib{,/vmware}/libpcoip_client_neon.so
chrpath -d usr/lib/vmware/libcurl.so.4
%endif
%ifarch x86_64
mv -v usr/lib/vmware/view/integratedPrinting/prlinuxcupsppd usr/bin/
mv -v usr/lib/vmware/view/usb/vmware-eucusbarbitrator usr/bin/

pushd usr/lib/vmware/view/html5mmr
find . -type f | xargs chmod 644
popd

chrpath -d usr/lib/vmware/view/bin/ftscanhvd
%endif

rm -frv \
  etc/init.d \
  etc/udev \
  usr/lib/vmware/fips.so \
  usr/lib/vmware/gcc \
  usr/lib/vmware/libatkmm-1.6.so.1 \
  usr/lib/vmware/libcairomm-1.0.so.1 \
%if %{without bundled_ssl}
  usr/lib/vmware/libcrypto.so.3 \
  usr/lib/vmware/libcurl.so.4 \
  usr/lib/vmware/libssl.so.3 \
%endif
  usr/lib/vmware/libgdkmm-3.0.so.1 \
  usr/lib/vmware/libgiomm-2.4.so.1 \
  usr/lib/vmware/libglibmm-2.4.so.1 \
  usr/lib/vmware/libpangomm-1.4.so.1 \
  usr/lib/vmware/libpng16.so.16 \
  usr/lib/vmware/libsigc-2.0.so.0 \
  usr/lib/vmware/libz.so.1 \
  usr/lib/vmware/view/html5mmr/libvulkan.so.1 \
  usr/lib/vmware/view/integratedPrinting/{integrated-printing-setup.sh,README} \
  usr/lib/vmware/view/urlRedirection/install-url-redirection.py \
  usr/lib/vmware/view/vaapi{,2.7} \
  README \
  ../docs/patches \
  ../docs/scannerClient/README \
  ../docs/serialPortClient/README \
  usr/share/doc \
  usr/share/icons/vmware-view.png \
%{nil}

sed -e 's|/usr/lib/|%{_libdir}/|g' -i usr/bin/vmware-view{,-lib-scan,-log-collector}

popd

find %{_vpath_builddir} -type f | xargs file | grep ELF | cut -d: -f1 | xargs chmod 0755


%build


%install
mkdir -p %{buildroot}%{_libdir}
mv %{_vpath_builddir}/usr/lib/* %{buildroot}%{_libdir}

mkdir -p %{buildroot}/%{_bindir}
mv %{_vpath_builddir}/usr/bin/* %{buildroot}%{_bindir}

mkdir -p %{buildroot}/%{_datadir}
mv %{_vpath_builddir}/usr/share/* %{buildroot}%{_datadir}

mkdir -p %{buildroot}/var/log/vmware

mkdir -p %{buildroot}%{_sysconfdir}/teradici
mkdir -p %{buildroot}%{_sysconfdir}/vmware{/udpProxy,/vdp/host_overlay_plugins,-vix}
echo 'BINDIR="%{_bindir}"' > %{buildroot}%{_sysconfdir}/vmware/bootstrap
echo 'BINDIR="%{_bindir}"' > %{buildroot}%{_sysconfdir}/vmware-vix/bootstrap

echo "%{_libdir}/pcoip/vchan_plugins/libvdpservice.so" \
  > %{buildroot}%{_sysconfdir}/vmware/vdp/host_overlay_plugins/config

mv vmware/*.conf %{buildroot}%{_sysconfdir}/vmware/

install -pm0644 usbarb.rules %{buildroot}%{_sysconfdir}/vmware/

abs2rel(){
  realpath -m --relative-to="$2" "$1"
}

mkdir -p %{buildroot}%{_presetdir}
mkdir -p %{buildroot}%{_unitdir}
install -pm0644 vmware-eucusbarbitrator.service %{buildroot}%{_unitdir}/
install -pm0644 vmware-eucusbarbitrator.preset %{buildroot}%{_presetdir}/96-vmware-eucusbarbitrator.preset
%ifarch x86_64
mv systemd/system/ftsprhv.service %{buildroot}%{_unitdir}/
mv systemd/system/ftscanhv.service %{buildroot}%{_unitdir}/
install -pm0644 vmware-ftsprhv.preset %{buildroot}%{_presetdir}/96-ftsprhv.preset
install -pm0644 vmware-ftscanhv.preset %{buildroot}%{_presetdir}/96-ftscanhv.preset
%endif

ln -s \
  $(abs2rel %{buildroot}%{_libdir} %{buildroot}%{_libdir}/vmware)/libudev.so.1 \
  %{buildroot}%{_libdir}/vmware/libudev.so.0

mkdir -p %{buildroot}%{_libdir}/vmware/view/pkcs11
ln -s \
  $(abs2rel %{buildroot}%{_libdir}/pkcs11 %{buildroot}%{_libdir}/vmware/view/pkcs11)/opensc-pkcs11.so \
  %{buildroot}%{_libdir}/vmware/view/pkcs11/libopenscpkcs11.so

mkdir -p %{buildroot}%{_datadir}/vmware/selinux/
install -pm0644 %{name}-scannerclient-rpm.cil %{buildroot}%{_datadir}/vmware/selinux/
install -pm0644 %{name}-usb-rpm.cil %{buildroot}%{_datadir}/vmware/selinux/

desktop-file-install \
  --delete-original \
  --dir %{buildroot}%{_datadir}/applications \
  --set-icon=vmware-view \
  --remove-key=Encoding \
  --remove-category=Application \
  %{buildroot}%{_datadir}/applications/vmware-view.desktop

for res in 16 22 24 32 36 48 64 72 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick %{buildroot}%{_datadir}/pixmaps/vmware-view.png \
    -filter Lanczos -resize ${res}x${res} ${dir}/vmware-view.png
done


%find_lang vmware-view


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/vmware-view.desktop


%post scannerclient
%{_sbindir}/semodule -i %{_datadir}/vmware/selinux/%{name}-scannerclient-rpm.cil
%systemd_post ftscanhv.service
exit 0

%preun scannerclient
%systemd_preun ftscanhv.service

%postun scannerclient
%systemd_postun_with_restart ftscanhv.service
if [ $1 -eq 0 ]; then
  %{_sbindir}/semodule -r %{name}-scannerclient-rpm || :
fi

%post serialportclient
%systemd_post ftsprhv.service
exit 0

%preun serialportclient
%systemd_preun ftsprhvd.service

%postun serialportclient
%systemd_postun_with_restart ftsprhv.service

%post usb
%{_sbindir}/semodule -i %{_datadir}/vmware/selinux/%{name}-usb-rpm.cil
%systemd_post vmware-eucusbarbitrator.service
exit 0

%preun usb
%systemd_preun vmware-eucusbarbitrator.service

%postun usb
%systemd_postun_with_restart vmware-eucusbarbitrator.service
if [ $1 -eq 0 ]; then
  %{_sbindir}/semodule -r %{name}-usb-rpm || :
fi

%files -f vmware-view.lang
%license docs/open_source_licenses.txt
%license end-user-agreement-english.pdf
%dnl vmware-horizon-client-for-linux-%{pdfver}-release-notes.pdf
%dnl %doc horizon-client-linux-installation.pdf
%dir %{_sysconfdir}/vmware
%config %{_sysconfdir}/vmware/bootstrap
%attr(0644,root,root) %config(noreplace) %ghost %{_sysconfdir}/vmware/config
%attr(0644,root,root) %config(noreplace) %ghost %{_sysconfdir}/vmware/view-keycombos-config
%dir %{_sysconfdir}/vmware/udpProxy
%attr(0644,root,root) %config(noreplace) %ghost %{_sysconfdir}/vmware/udpProxy/config
%dir %{_sysconfdir}/vmware/vdp
%dir %{_sysconfdir}/vmware-vix
%config %{_sysconfdir}/vmware-vix/bootstrap
%{_bindir}/vmware-view
%{_bindir}/vmware-view-lib-scan
%{_bindir}/vmware-view-log-collector
%dir %{_libdir}/vmware
%attr(0644,root,root) %config(noreplace) %ghost %{_libdir}/vmware/config
%{_libdir}/vmware/view/dct
%dir %{_libdir}/vmware/view/env
%{_libdir}/vmware/view/env/vmware-view.info
%{_libdir}/vmware/libclientSdkCPrimitive.so
%{_libdir}/vmware/libcrtbora.so
%if %{with bundled_ssl}
%{_libdir}/vmware/libcrypto.so.3
%{_libdir}/vmware/libcurl.so.4
%{_libdir}/vmware/libssl.so.3
%endif
%{_libdir}/vmware/libgtkmm-3.0.so.1
%{_libdir}/vmware/librtavCliLib.so
%{_libdir}/vmware/libudev.so.0
%{_libdir}/vmware/libudpProxyLib.so
%{_libdir}/vmware/libvmwarebase.so
%ifarch x86_64
%{_libdir}/vmware/rdpvcbridge/ftnlses3hv.so
%{_libdir}/vmware/liburlFilterPlugin.so
%{_libdir}/vmware/view/bin/vmware-urlFilter
%{_bindir}/vmware-url-filter
%endif
%dir %{_libdir}/vmware/rdpvcbridge
%attr(0644,root,root) %config(noreplace) %ghost %{_libdir}/vmware/settings
%dir %{_libdir}/vmware/view
%dir %{_libdir}/vmware/view/bin
%{_libdir}/vmware/view/bin/vmware-view
%dir %{_libdir}/vmware/view/vdpService
%{_datadir}/applications/vmware-view.desktop
%{_datadir}/icons/hicolor/*/apps/vmware-view.png
%{_datadir}/pixmaps/vmware-view.png
%{_datadir}/X11/xorg.conf.d/20-vmware-hid.conf
%{_var}/log/vmware

%files pcoip
%dir %{_sysconfdir}/teradici
%attr(0644,root,root) %config(noreplace) %ghost %{_sysconfdir}/teradici/pcoip_admin.conf
%attr(0644,root,root) %config(noreplace) %ghost %{_sysconfdir}/teradici/pcoip_admin_defaults.conf
%dir %{_sysconfdir}/vmware/vdp/host_overlay_plugins
%config(noreplace) %{_sysconfdir}/vmware/vdp/host_overlay_plugins/config
%dir %{_libdir}/pcoip
%dir %{_libdir}/pcoip/vchan_plugins
%{_libdir}/pcoip/vchan_plugins/libvdpservice.so
%{_libdir}/pcoip/vchan_plugins/librdpvcbridge.so
%{_libdir}/vmware/rdpvcbridge/freerdp_plugins.conf
%{_libdir}/vmware/libffi.so
%{_libdir}/vmware/libpcoip_client.so
%ifarch armv7hl
%{_libdir}/vmware/libpcoip_client_neon.so
%endif
%{_libdir}/vmware/view/client/vmware-remotemks
%{_libdir}/vmware/view/vdpService/libMicrosoft.SlimCV.VBM.so
%{_libdir}/vmware/view/vdpService/libmksvchanclient.so
%{_libdir}/vmware/view/vdpService/librdeSvc.so
%{_libdir}/vmware/view/software
%{_libdir}/vmware/view/vaapi2
%{_libdir}/vmware/view/vdpau
%{_libdir}/vmware/xkeymap

%files rtav
%{_libdir}/pcoip/vchan_plugins/libviewMMDevRedir.so
%ifarch x86_64
%{_libdir}/vmware/libx264.so.164.5
%endif

%files smartcard
%{_libdir}/pcoip/vchan_plugins/libscredirvchanclient.so
%dir %{_libdir}/vmware/view/pkcs11
%{_libdir}/vmware/view/pkcs11/libopenscpkcs11.so

%files usb
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/vmware/usbarb.rules
%{_presetdir}/96-vmware-eucusbarbitrator.preset
%{_unitdir}/vmware-eucusbarbitrator.service
%{_bindir}/vmware-eucusbarbitrator
%dir %{_libdir}/vmware/view/usb
%{_libdir}/vmware/view/usb/libvmware-view-usbd.so
%{_libdir}/vmware/view/vdpService/libusbRedirectionClient.so
%{_datadir}/vmware/selinux/%{name}-usb-rpm.cil

%ifarch x86_64
%files html5mmr
%{_libdir}/vmware/view/html5mmr
%{_libdir}/vmware/view/vdpService/libhtml5Client.so

%files integrated-printing
%{_bindir}/prlinuxcupsppd
%dir %{_libdir}/vmware/view/integratedPrinting
%{_libdir}/vmware/view/integratedPrinting/vmware-print-redir-client
%{_libdir}/vmware/view/vdpService/libvmwprvdpplugin.so

%files mmr
%{_libdir}/vmware/view/vdpService/libtsmmrClient.so

%files scannerclient
%config(noreplace) /etc/vmware/ftplugins.conf
%{_libdir}/vmware/view/bin/ftscanhvd
%{_presetdir}/96-ftscanhv.preset
%{_unitdir}/ftscanhv.service
%{_datadir}/vmware/selinux/%{name}-scannerclient-rpm.cil

%files serialportclient
%attr(0644,root,root) %config(noreplace) %ghost %{_sysconfdir}/ftsprhv.db
%{_libdir}/vmware/view/bin/ftsprhvd
%{_presetdir}/96-ftsprhv.preset
%{_unitdir}/ftsprhv.service

%files teams
%{_libdir}/vmware/view/vdpService/webrtcRedir

%files tsdr
%{_libdir}/vmware/view/vdpService/libtsdrClient.so
%endif


%changelog
* Mon Sep 23 2024 - 2406.8.13.0.9995429239-1
- 2406
- Sync with rathann

* Mon May 27 2024 - 2312.1.8.12.1.23543969-1
- 2312.1

* Fri Feb 17 2023 - 2212.1.8.8.1.21219348-1
- 2212.1

* Mon Dec 19 2022 - 2209.8.7.0.20616018-2
- chinforpms release
- %%{_prefix}/lib -> %%{_libdir}
- Cosmetic changes

* Thu Nov 03 2022 Dominik 'Rathann' Mierzejewski <dominik@greysector.net> 2209.8.7.0.20616018-1
- update to 2209 (8.7.0.20616018)
- use upstream systemd service files
