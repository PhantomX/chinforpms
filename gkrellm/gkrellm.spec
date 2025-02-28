Name:           gkrellm
Version:        2.4.0
Release:        100%{?dist}
Summary:        Multiple stacked system monitors in one process

Epoch:          1

License:        GPL-3.0-or-later
URL:            https://gkrellm.srcbox.net/

Source0:        https://gkrellm.srcbox.net/releases/%{name}-%{version}.tar.bz2

Patch1:         gkrellm-2.4.0-config.patch
Patch3:         gkrellm-2.4.0-width.patch
Patch10:        https://git.srcbox.net/%{name}/%{name}/commit/f961318d048b85eb0d40ea530906b040b173a7d0.patch#/%{name}-git-f961318.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  gcc
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(libntlm)
BuildRequires:  lm_sensors-devel
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(sm)
BuildRequires:  libappstream-glib
Requires:       gdk-pixbuf2-modules-extra%{?_isa}

%description
GKrellM charts CPU, load, Disk, and all active net interfaces
automatically.  An on/off button and online timer for the PPP
interface is provided, as well as monitors for memory and swap usage,
file system, internet connections, APM laptop battery, mbox style
mailboxes, and temperature sensors on supported systems.  Also
included is an uptime monitor, a hostname label, and a clock/calendar.
Additional features are:

  * Autoscaling grid lines with configurable grid line resolution.
  * LED indicators for the net interfaces.
  * A gui popup for configuration of chart sizes and resolutions.


%package daemon
Summary:        The GNU Krell Monitors Server
# systemd >= 186 for scriptlet macros
BuildRequires:  systemd >= 186
BuildRequires: make
Requires(pre):  systemd
Requires(post,preun,postun): systemd


%description daemon
gkrellmd listens for connections from gkrellm clients. When a gkrellm
client connects to a gkrellmd server all builtin monitors collect their
data from the server.


%package        devel
Summary:        Development files for the GNU Krell Monitors
Requires:       pkgconfig(gtk+-2.0)

%description devel
Development files for the GNU Krell Monitors.


%prep
%autosetup -p1

for i in gkrellmd.1 gkrellm.1 README Changelog.OLD Changelog-plugins.html \
    src/gkrellm.h server/gkrellmd.h; do
   sed -i -e "s@/usr/lib/gkrellm2*/plugins@%{_libdir}/gkrellm2/plugins@" $i
   sed -i -e "s@/usr/local/lib/gkrellm2*/plugins@/usr/local/%{_lib}/gkrellm2/plugins@" $i
done

# Create a sysusers.d config file
cat >gkrellm.sysusers.conf <<EOF
u gkrellmd - 'GNU Krell daemon' - -
EOF


%build
make %{?_smp_mflags} PREFIX=%{_prefix} \
    PKGCONFIGDIR=%{_libdir}/pkgconfig \
    INCLUDEDIR=%{_includedir} \
    SINSTALLDIR=%{_sbindir} \
    CFLAGS="$CFLAGS -D_GNU_SOURCE -Wno-error=incompatible-pointer-types" \
    LDFLAGS="$LDFLAGS"


%install
mkdir -p %{buildroot}%{_datadir}/gkrellm2/themes
mkdir -p %{buildroot}%{_libdir}/gkrellm2/plugins

make install DESTDIR=%{buildroot} PREFIX=%{_prefix} \
    LOCALEDIR=%{buildroot}%{_datadir}/locale \
    INSTALLDIR=%{buildroot}%{_bindir} \
    SINSTALLDIR=%{buildroot}%{_sbindir} \
    MANDIR=%{buildroot}%{_mandir}/man1 \
    PKGCONFIGDIR=%{buildroot}%{_libdir}/pkgconfig \
    INCLUDEDIR=%{buildroot}%{_includedir} \
    CFGDIR=%{buildroot}%{_sysconfdir}

%find_lang %name

desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml

install -m0644 -D gkrellm.sysusers.conf %{buildroot}%{_sysusersdir}/gkrellm.conf



%post daemon
%systemd_post gkrellmd.service

%preun daemon
%systemd_preun gkrellmd.service

%postun daemon
%systemd_postun_with_restart gkrellmd.service


%files -f %{name}.lang
%license COPYRIGHT
%doc CHANGELOG.md Changelog.OLD README Themes.html
%{_bindir}/%{name}
%{_libdir}/gkrellm2
%{_datadir}/gkrellm2
%{_mandir}/man1/%{name}.1*
%{_metainfodir}/*.metainfo.xml
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%files devel
%license %{_licensedir}/%{name}*
%{_includedir}/gkrellm2
%{_libdir}/pkgconfig/%{name}.pc

%files daemon
%license %{_licensedir}/%{name}*
%{_unitdir}/gkrellmd.service
%{_sbindir}/gkrellmd
%{_mandir}/man1/gkrellmd.*
%config(noreplace) %{_sysconfdir}/gkrellmd.conf
%{_sysusersdir}/gkrellm.conf


%changelog
* Sat Feb 22 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2.4.0-100
- chinforpms build

* Mon Jan 20 2025 Adam Goode <adam@spicenitz.org> - 2.4.0-3
- Fix systemd unit file to point to correct gkrellmd location

* Mon Jan 20 2025 Adam Goode <adam@spicenitz.org> - 2.4.0-2
- Don't rename desktop file, it's referenced elsewhere

* Mon Jan 20 2025 Adam Goode <adam@spicenitz.org> - 2.4.0-1
- New upstream release and modernize spec file

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.11-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 18 2024 Kevin Fenzi <kevin@scrye.com> - 2.3.11-19
- Rebuild for new libntlm soname bump.

* Fri Jul 26 2024 Benjamin Gilbert <bgilbert@backtick.net> - 2.3.11-18
- Require gdk-pixbuf2-modules-extra on F41+ to fix crash (rhbz#2276464)

* Thu Jul 25 2024 Miroslav Suchý <msuchy@redhat.com> - 2.3.11-17
- convert GPLv3+ license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.11-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.11-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.11-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.11-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild
