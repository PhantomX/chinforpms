# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%undefine _missing_build_ids_terminate_build
%undefine _debugsource_packages
%undefine _unique_build_ids
%global _build_id_links none
%global _no_recompute_build_ids 1

%global cart   23FQ3
%global yymm   2209
%global ver    8.7.0
%global rel    20616018
%global fver   %{yymm}-%{ver}-%{rel}
%global s4br_ver 15.0.0.0
%global s4br_bld 20450170
%ifarch x86_64
%global mark64 ()(64bit)
%global vhc_arch x64
%else
%global mark64 %nil
%global vhc_arch armhf
%endif

Name:           vmware-horizon-client
Version:        %{yymm}.%{ver}.%{rel}
Release:        2%{?dist}
Summary:        Remote access client for VMware Horizon

License:        VMware
URL:            https://www.vmware.com/products/horizon.html

# https://customerconnect.vmware.com/en/downloads/info/slug/desktop_end_user_computing/vmware_horizon_clients/horizon_8
Source0:        https://download3.vmware.com/software/CART%{cart}_LIN_%{yymm}_TARBALL/VMware-Horizon-Client-Linux-%{yymm}-%{ver}-%{rel}.tar.gz
Source1:        https://docs.vmware.com/en/VMware-Horizon-Client-for-Linux/%{yymm}/rn/vmware-horizon-client-for-linux-%{yymm}-release-notes/vmware-horizon-client-for-linux-%{yymm}-release-notes.pdf
Source2:        https://docs.vmware.com/en/VMware-Horizon-Client-for-Linux/%{yymm}/horizon-client-linux-installation.pdf
Source10:       usbarb.rules
Source11:       vmware-usbarbitrator.service
Source14:       vmware-usbarbitrator.preset
Source15:       vmware-ftsprhv.preset
Source16:       vmware-ftscanhv.preset

Patch0:         %{name}-fedora.patch
Patch1:         %{name}-systemd.patch

ExclusiveArch:  armv7hl x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  %{_bindir}/execstack
BuildRequires:  systemd-rpm-macros
BuildRequires:  ImageMagick

Provides:       bundled(atk) = 2.28.1
Provides:       bundled(atkmm) = 2.22.7
Provides:       bundled(boost) = 1.67
Provides:       bundled(bzip2) = 1.0.6
Provides:       bundled(c-ares) = 1.13.0
Provides:       bundled(curl) = 7.74
Provides:       bundled(glibmm24) = 2.44.0
Provides:       bundled(gtkmm30) = 3.10.1
Provides:       bundled(hal) = 0.5.12
Provides:       bundled(icu) = 60.2
Provides:       bundled(libjpeg-turbo) = 1.4.2
Provides:       bundled(libwebrtc) = 90
Provides:       bundled(libxml2) = 2.9.9
Provides:       bundled(mechanical-fonts) = 1.00
Provides:       bundled(openssl) = 1.0.2y
Provides:       bundled(opus) = 1.1.4.60
Provides:       bundled(pangomm) = 2.34.0
Provides:       bundled(speex) = 1.2rc3
Provides:       bundled(zlib) = 1.2.11
Provides:       %{name}-seamless-window = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-seamless-window < 5.2.0.14604769
Requires:       %{_bindir}/pidof
Requires:       libudev.so.1%{mark64}

%global __provides_exclude_from ^%{_libdir}/(vmware|pcoip)/.*$
%global __requires_exclude ^lib\(atkmm-1\\.6\\.so\\.1\|curl\\.so\\.4\|g\(io\|lib\)mm-2\\.4\\.so\\.1\|g\(dk\|tk\)mm-3\\.0\\.so\\.1\|pangomm-1\\.4\\.so\\.1\|\(crypto\|ssl\)\\.so\\.1\\.0\\.2\|udev\\.so\\.0\|\(cef\|clientSdkCPrimitive\|crtbora\|GLESv2\|json_linux-gcc-4.1.1_libmt\|vmware\(base\|-view-usbd\)\)\\.so).*$

%description
Remote access client for VMware Horizon.

Requires Horizon Agent 7.0 or later on the virtual desktop.

%package html5mmr
Summary:        HTML5 Multimedia Redirection support plugin for VMware Horizon Client
Provides:       bundled(chromium-embedded-framework) = 87.0.4280.20
Provides:       bundled(webrtc) = 90
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description html5mmr
HTML5 Multimedia Redirection support plugin for VMware Horizon Client.

Requires Horizon Agent 7.9 or later on the virtual desktop.

%package integrated-printing
Summary:        Integrated Printing support plugin for VMware Horizon Client
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description integrated-printing
Integrated Printing support plugin for VMware Horizon Client.

%package media-provider
Summary:        Virtualization Pack for Skype for Business
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       bundled(hidapi) = 0.8.9
Provides:       bundled(json-c) = 0.12.1
Provides:       bundled(libjpeg-turbo) = 2.0.5
Provides:       bundled(libsrtp) = 2.2.0
Provides:       bundled(openssl) = 1.0.2y
Provides:       bundled(webrtc) = 90

%description media-provider
Virtualization Pack for Skype for Business.

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
Requires:       libavcodec.so.58%{mark64}
Requires:       libavutil.so.56%{mark64}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       bundled(libpng) = 1.6.37
Provides:       bundled(pcoip-soft-clients) = 3.75
Provides:       bundled(openssl) = 1.0.2w

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
Provides:       bundled(x264-libs) = 0.157
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
cp -p %{S:1} %{S:2} ./

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

%ifarch x86_64
mkdir -p %{_vpath_builddir}/lib/vmware/mediaprovider
tar xzf SkypeForBusiness\ Redirection/VMware-Horizon-Media-Provider-%{s4br_ver}-%{s4br_bld}.%{vhc_arch}.tar.gz\
  -C %{_vpath_builddir}/lib/vmware/mediaprovider \
  --strip-components=2 \
  VMware-Horizon-Media-Provider-%{s4br_ver}-%{s4br_bld}.%{vhc_arch}/lin64/\*.so
%endif

%patch0 -p3 -d %{_vpath_builddir}
%ifarch x86_64
%patch1 -p2 -d %{_vpath_builddir}
%endif

pushd %{_vpath_builddir}
mv -v doc ../
mv -v systemd ../
mv -v vmware ../
mv -v lib/vmware{/view/lib,}/libclientSdkCPrimitive.so
mv -v lib{,/vmware}/libpcoip_client.so
%ifarch armv7hl
mv -v lib{,/vmware}/libpcoip_client_neon.so
chmod 755 lib/vmware/libcurl.so.4
chrpath -d lib/vmware/libcurl.so.4
%endif
%ifarch x86_64
mv -v lib/vmware/view/integratedPrinting/prlinuxcupsppd bin/

pushd lib/vmware/view/html5mmr
find . -type f | xargs chmod 644
chmod 0755 \
  HTML5VideoPlayer \
  chrome_sandbox \
  lib*.so \

popd

chmod 0755 lib/vmware/view/vdpService/webrtcRedir/libwebrtc_sharedlib.so
chrpath -d lib/vmware/view/bin/ftscanhvd
%endif

rm -frv \
  init.d \
  lib/vmware/gcc \
  lib/vmware/libcairomm-1.0.so.1 \
  lib/vmware/libffi.so.6 \
  lib/vmware/libpcre.so.1 \
  lib/vmware/libpng16.so.16 \
  lib/vmware/libsigc-2.0.so.0 \
  lib/vmware/libv4l2.so.0 \
  lib/vmware/libv4lconvert.so.0 \
  lib/vmware/libXss.so.1 \
  lib/vmware/libz.so.1 \
  lib/vmware/view/crtbora \
  lib/vmware/view/html5mmr/libhtml5Client.so \
  lib/vmware/view/html5mmr/libvulkan.so.1 \
  lib/vmware/view/integratedPrinting/{integrated-printing-setup.sh,README} \
  lib/vmware/view/{software,vaapi{,2},vdpau} \
  share/icons \
  patches \
  README* \

rmdir lib/vmware/view/lib

sed -e 's|/usr/lib/|%{_libdir}/|g' -i bin/vmware-view{,-lib-scan,-log-collector}

popd


%build


%install
mkdir -p %{buildroot}%{_libdir}
mv %{_vpath_builddir}/lib/* %{buildroot}%{_libdir}

mkdir -p %{buildroot}/%{_bindir}
mv %{_vpath_builddir}/bin/* %{buildroot}%{_bindir}

mkdir -p %{buildroot}/%{_datadir}
mv %{_vpath_builddir}/share/* %{buildroot}%{_datadir}

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
install -pm0644 vmware-usbarbitrator.service %{buildroot}%{_unitdir}/
install -pm0644 vmware-usbarbitrator.preset %{buildroot}%{_presetdir}/96-vmware-usbarbitrator.preset
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

for v in software vaapi2 vdpau ; do
  dir=%{buildroot}%{_libdir}/vmware/view/${v}
  mkdir -p ${dir}
  relpath=$(abs2rel %{buildroot}%{_libdir} %{buildroot}%{_libdir}/vmware/view/${v})
  ln -s ${relpath}/libavcodec.so.58 ${dir}/
  ln -s ${relpath}/libavutil.so.56 ${dir}/
done

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
  convert %{buildroot}%{_datadir}/pixmaps/vmware-view.png \
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
%systemd_post vmware-usbarbitrator.service
exit 0

%preun usb
%systemd_preun vmware-usbarbitrator.service

%postun usb
%systemd_postun_with_restart vmware-usbarbitrator.service
if [ $1 -eq 0 ]; then
  %{_sbindir}/semodule -r %{name}-usb-rpm || :
fi

%files -f vmware-view.lang
%license doc/open_source_licenses.txt
%doc vmware-horizon-client-for-linux-%{yymm}-release-notes.pdf
%doc horizon-client-linux-installation.pdf
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
%{_bindir}/vmware-view-usbdloader
%dir %{_libdir}/vmware
%attr(0644,root,root) %config(noreplace) %ghost %{_libdir}/vmware/config
%{_libdir}/vmware/view/dct
%dir %{_libdir}/vmware/view/env
%{_libdir}/vmware/view/env/env_utils.sh
%{_libdir}/vmware/view/env/vmware-view.info
%{_libdir}/vmware/libatkmm-1.6.so.1
%{_libdir}/vmware/libclientSdkCPrimitive.so
%{_libdir}/vmware/libcrtbora.so
%{_libdir}/vmware/libcrypto.so.1.0.2
%{_libdir}/vmware/libcurl.so.4
%{_libdir}/vmware/libgdkmm-3.0.so.1
%{_libdir}/vmware/libgiomm-2.4.so.1
%{_libdir}/vmware/libglibmm-2.4.so.1
%{_libdir}/vmware/libgtkmm-3.0.so.1
%{_libdir}/vmware/libpangomm-1.4.so.1
%{_libdir}/vmware/librtavCliLib.so
%{_libdir}/vmware/libssl.so.1.0.2
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
%{_libdir}/vmware/libpcoip_client.so
%ifarch armv7hl
%{_libdir}/vmware/libpcoip_client_neon.so
%endif
%{_libdir}/vmware/view/client/vmware-remotemks
%{_libdir}/vmware/view/vdpService/libmksvchanclient.so
%{_libdir}/vmware/view/vdpService/librdeSvc.so
%{_libdir}/vmware/view/software
%{_libdir}/vmware/view/vaapi2
%{_libdir}/vmware/view/vdpau
%{_libdir}/vmware/xkeymap

%files rtav
%{_libdir}/pcoip/vchan_plugins/libviewMMDevRedir.so
%ifarch x86_64
%{_libdir}/vmware/libx264.so.157.6
%endif

%files smartcard
%{_libdir}/pcoip/vchan_plugins/libscredirvchanclient.so
%dir %{_libdir}/vmware/view/pkcs11
%{_libdir}/vmware/view/pkcs11/libopenscpkcs11.so

%files usb
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/vmware/usbarb.rules
%{_presetdir}/96-vmware-usbarbitrator.preset
%{_unitdir}/vmware-usbarbitrator.service
%{_bindir}/vmware-usbarbitrator
%dir %{_libdir}/vmware/view/usb
%{_libdir}/vmware/view/usb/libvmware-view-usbd.so
%{_libdir}/vmware/view/vdpService/libusbRedirectionClient.so
%{_datadir}/vmware/selinux/%{name}-usb-rpm.cil

%ifarch x86_64
%files html5mmr
%{_libdir}/vmware/libjson_linux-gcc-4.1.1_libmt.so
%{_libdir}/vmware/view/html5mmr
%{_libdir}/vmware/view/vdpService/libhtml5Client.so

%files integrated-printing
%{_bindir}/prlinuxcupsppd
%dir %{_libdir}/vmware/view/integratedPrinting
%{_libdir}/vmware/view/integratedPrinting/vmware-print-redir-client
%{_libdir}/vmware/view/vdpService/libvmwprvdpplugin.so

%files media-provider
%dir %{_libdir}/vmware/mediaprovider
%{_libdir}/vmware/mediaprovider/libV264.so
%{_libdir}/vmware/mediaprovider/libVMWMediaProvider.so

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
* Mon Dec 19 2022 - 2209.8.7.0.20616018-2
- chinforpms release
- %%{_prefix}/lib -> %%{_libdir}
- Cosmetic changes

* Thu Nov 03 2022 Dominik 'Rathann' Mierzejewski <dominik@greysector.net> 2209.8.7.0.20616018-1
- update to 2209 (8.7.0.20616018)
- use upstream systemd service files
