# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%undefine _missing_build_ids_terminate_build
%global debug_package %{nil}
%undefine _unique_build_ids
%global _build_id_links none
%global _no_recompute_build_ids 1

%ifarch x86_64
%global mark64 ()(64bit)
%else
%global mark64 %{nil}
%endif

%bcond bundled_ssl 0

%global ver    13.0.1.0
%global rel    24954779


Name:           vmware-vmrc
Version:        %{ver}.%{rel}
Release:        1%{?dist}
Summary:        VMware Remote Console

License:        VMware

URL:            https://support.broadcom.com/
Source0:        VMware-Remote-Console-%{ver}.%{rel}.x86_64.bundle.zip
Source1:        https://docs.broadcom.com/doc/end-user-agreement-english#/end-user-agreement-english.pdf
Source10:       vmware-usbarbitrator.service
Source11:       vmware-usbarbitrator.preset

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  systemd-rpm-macros

Requires:       vmware-common%{?_isa}

Provides:       bundled(gtkmm30) = 3.10.1
%if %{with bundled_ssl}
Provides:       bundled(curl) = 7.74
Provides:       bundled(openssl) = 3.0.12
%endif
Provides:       bundled(libtiff) = 4.5

%global __provides_exclude_from ^%{_libdir}/(vmware|pcoip)/.*$
%global __requires_exclude ^libatkmm-.*\\.so.*$
%global __requires_exclude %__requires_exclude|^libbasichttp\\.so.*$
%global __requires_exclude %__requires_exclude|^libcairomm-.*\\.so.*$
%global __requires_exclude %__requires_exclude|^libcds\\.so.*$
%global __requires_exclude %__requires_exclude|^libgdkmm-.*\\.so.*$
%global __requires_exclude %__requires_exclude|^libgiomm-.*\\.so.*$
%global __requires_exclude %__requires_exclude|^libglibmm-.*\\.so.*$
%global __requires_exclude %__requires_exclude|^libglibmm_generate_extra_defs-.*\\.so.*$
%global __requires_exclude %__requires_exclude|^libgtkmm-.*\\.so.*$
%global __requires_exclude %__requires_exclude|^libpangomm-.*\\.so.*$
%global __requires_exclude %__requires_exclude|^libsigc-.*\\.so.*$
%global __requires_exclude %__requires_exclude|^libxml2.*\\.so.*$
%if %{with bundled_ssl}
%global __requires_exclude %__requires_exclude|^libcrypto\\.so.*$
%global __requires_exclude %__requires_exclude|^libcurl\\.so.*$
%global __requires_exclude %__requires_exclude|^libssl\\.so.*$
%endif
%global __requires_exclude %__requires_exclude|^libgvmomi\\.so.*$
%global __requires_exclude %__requires_exclude|^libtiff\\.so.*$
%global __requires_exclude %__requires_exclude|^libvmplayer\\.so.*$
%global __requires_exclude %__requires_exclude|^libvmrc\\.so.*$
%global __requires_exclude %__requires_exclude|^libvmwarebase\\.so.*$
%global __requires_exclude %__requires_exclude|^libvmware-gksu\\.so.*$
%global __requires_exclude %__requires_exclude|^libvmwareui\\.so.*$
%global __requires_exclude %__requires_exclude|^libvmware-zenity\\.so.*$


%description
%{summary}.


%package usb
Summary:        USB Redirection support plugin for VMware Remote Client
BuildRequires:  systemd
%{?systemd_requires}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires(post): %{_sbindir}/semodule
Requires(postun): %{_sbindir}/semodule

%description usb
USB Redirection support plugin for VMware Horizon Client.


%prep
%autosetup -c

chmod +x VMware-Remote-Console-%{ver}.%{rel}.%{_arch}.bundle
./VMware-Remote-Console-%{ver}.%{rel}.%{_arch}.bundle -x bundle

cp %{S:1} .
cp %{S:10} .
cp %{S:11} .

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

mkdir -p %{_vpath_builddir}

pushd bundle
mv vmware-vmrc/doc/EULA ../
mv vmware-vmrc-app/doc/open_source_licenses.txt ../
mv vmware-player-core/lib/lib/*.so vmware-vmrc-app/lib/lib/
mv vmware-usbarbitrator/bin/* vmware-vmrc-app/bin/
mv vmware-vmrc/share/icons vmware-vmrc-app/share/
mv vmware-player-core/lib/share/pixmaps/*.{png,svg} vmware-vmrc-app/lib/share/pixmaps/
mv vmware-vmrc-app/{bin,lib,messages,share} ../%{_vpath_builddir}
popd

pushd %{_vpath_builddir}
mv bin/{vmware,vmrc}-gksu
sed -e 's|vmware-gksu|vmrc-gksu|g' -i bin/vmrc*
mv messages lib/
rm -frv \
  lib/libconf \
  lib/lib/libaio.so.1 \
  lib/lib/libatk-1.0.so.0 \
  lib/lib/libatk-bridge-2.0.so.0 \
  lib/lib/libatspi.so.0 \
  lib/lib/libcairo-gobject.so.2 \
  lib/lib/libcairo.so.2 \
  lib/lib/libcroco-0.6.so.3 \
%if %{without bundled_ssl}
  lib/lib/libcrypto.so.3 \
  lib/lib/libcurl.so.4 \
  lib/lib/libssl.so.3 \
%endif
  lib/lib/libgcc_s.so.1 \
  lib/lib/libepoxy.so.0 \
  lib/lib/libffi.so.6 \
  lib/lib/libfontconfig.so.1 \
  lib/lib/libfreetype.so.6 \
  lib/lib/libgailutil-3.so.0 \
  lib/lib/libgck-1.so.0 \
  lib/lib/libgcr-base-3.so.1 \
  lib/lib/libgcr-ui-3.so.1 \
  lib/lib/libgcrypt.so.20 \
  lib/lib/libgdk-3.so.0 \
  lib/lib/libgdk_pixbuf-2.0.so.0 \
  lib/lib/libgdk_pixbuf_xlib-2.0.so.0 \
  lib/lib/libgio-2.0.so.0 \
  lib/lib/libglib-2.0.so.0 \
  lib/lib/libgmodule-2.0.so.0 \
  lib/lib/libgobject-2.0.so.0 \
  lib/lib/libgpg-error.so.0 \
  lib/lib/libgthread-2.0.so.0 \
  lib/lib/libgtk-3.so.0 \
  lib/lib/libharfbuzz.so.0 \
  lib/lib/libICE.so.6 \
  lib/lib/libjpeg.so.62 \
  lib/lib/libp11-kit.so.0 \
  lib/lib/libpango-1.0.so.0 \
  lib/lib/libpangocairo-1.0.so.0 \
  lib/lib/libpangoft2-1.0.so.0 \
  lib/lib/libpcre.so.1 \
  lib/lib/libpcsclite.so.1 \
  lib/lib/libpixman-1.so.0 \
  lib/lib/libpng16.so.16 \
  lib/lib/librsvg-2.so.2 \
  lib/lib/libsecret-1.so.0 \
  lib/lib/libstdc++.so.6 \
  lib/lib/libSM.so.6 \
  lib/lib/libtasn1.so.6 \
  lib/lib/libX11.so.6 \
  lib/lib/libXau.so.6 \
  lib/lib/libxcb.so.1 \
  lib/lib/libXcomposite.so.1 \
  lib/lib/libXcursor.so.1 \
  lib/lib/libXdamage.so.1 \
  lib/lib/libXdmcp.so.6 \
  lib/lib/libXext.so.6 \
  lib/lib/libXfixes.so.3 \
  lib/lib/libXft.so.2 \
  lib/lib/libXinerama.so.1 \
  lib/lib/libXi.so.6 \
  lib/lib/libXrandr.so.2 \
  lib/lib/libXrender.so.1 \
  lib/lib/libXss.so.1 \
  lib/lib/libXtst.so.6 \
  lib/lib/libz.so.1 \
  share/icons/hicolor/*/mimetypes

mv lib/xkeymap lib/xkm

sed \
  -e 's,%s/xkeymap/%s,%s/xkm/%s\x00\x00\x00\x00,g' \
  -e 's,\.\./xkeymap,../xkm\x00\x00\x00\x00,g' \
  -i lib/bin/vmware-remotemks \
     lib/lib/libvmwareui.so/libvmwareui.so \
     lib/lib/libvmwarebase.so/libvmwarebase.so

chmod +x lib/bin/*
find lib/lib -name '*.so*' -exec chmod +x '{}' ';'

popd

%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{_vpath_builddir}/bin/* %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_libdir}/vmware
mv %{_vpath_builddir}/lib/* %{buildroot}%{_libdir}/vmware/

mkdir -p %{buildroot}%{_libdir}/vmware/lib/libvmrc.so
ln -s ../libvmplayer.so/libvmplayer.so %{buildroot}%{_libdir}/vmware/lib/libvmrc.so/libvmrc.so
ln -s appLoader %{buildroot}%{_libdir}/vmware/bin/vmrc
ln -s appLoader %{buildroot}%{_libdir}/vmware/bin/vmrc-gksu

mkdir -p %{buildroot}%{_presetdir}
mkdir -p %{buildroot}%{_unitdir}
install -pm0644 vmware-usbarbitrator.service %{buildroot}%{_unitdir}/
install -pm0644 vmware-usbarbitrator.preset %{buildroot}%{_presetdir}/96-vmware-usbarbitrator.preset

mkdir -p %{buildroot}%{_datadir}/vmware/selinux/
install -pm0644 %{name}-usb-rpm.cil %{buildroot}%{_datadir}/vmware/selinux/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key=Exec \
  --set-value="vmrc %%u"\
  --set-icon=%{name} \
  --remove-key=Encoding \
  --remove-category=Application \
  %{_vpath_builddir}/share/applications/vmware-vmrc.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor
cp -rp %{_vpath_builddir}/share/icons/hicolor/* %{buildroot}%{_datadir}/icons/hicolor/


%post usb
%{_sbindir}/semodule -i %{_datadir}/vmware/selinux/%{name}-usb-rpm.cil
%systemd_post vmware-usbarbitrator.service
exit 0

%preun usb
%systemd_preun vmware-usbarbitrator.service

%postun usb
%systemd_postun_with_restart vmware-eucusbarbitrator.service
if [ $1 -eq 0 ]; then
  %{_sbindir}/semodule -r %{name}-usb-rpm || :
fi


%files
%license end-user-agreement-english.pdf
%license EULA
%license open_source_licenses.txt
%{_bindir}/vmrc
%{_bindir}/vmrc-gksu
%{_libdir}/vmware/bin
%{_libdir}/vmware/config
%{_libdir}/vmware/lib
%{_libdir}/vmware/messages
%{_libdir}/vmware/scripts
%{_libdir}/vmware/share
%{_libdir}/vmware/vnckeymap
%{_libdir}/vmware/xkm
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png


%files usb
%{_presetdir}/96-vmware-usbarbitrator.preset
%{_unitdir}/vmware-usbarbitrator.service
%{_bindir}/vmware-usbarbitrator
%{_datadir}/vmware/selinux/%{name}-usb-rpm.cil


%changelog
* Mon Dec 08 2025 - 13.0.1.0.24954779-1
- 13.0.1

* Tue Oct 01 2024 - 12.0.5.22744838-1
- Initial spec

