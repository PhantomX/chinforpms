%global _waterfox_app_id \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}

%global _waterfox_extensions %{_datadir}/waterfox/extensions
%global _waterfox_extdir %{_waterfox_extensions}/%{_waterfox_app_id}

# needed for this package
%global extension_id \{73a6fe31-595d-460b-a920-fcc0f8843232\}

Name:           waterfox-noscript
Version:        5.1.8.5
Release:        1%{?dist}
Summary:        JavaScript white list extension for Waterfox

License:        GPLv2+
URL:            http://noscript.net/
# Source is a .xpi file, there is no public VCS or a tarball
Source0:        https://secure.informaction.com/download/releases/noscript-%{version}.xpi
# https://bugzilla.redhat.com/show_bug.cgi?id=1364409
Source1:        %{name}.metainfo.xml

BuildRequires:  dos2unix
# GNOME Software Center not present on EL < 7 and Fedora
BuildRequires:  libappstream-glib
Requires:       waterfox-filesystem
BuildArch:      noarch

%description
The NoScript Waterfox extension provides extra protection for Waterfox.
It allows JavaScript, Java, Flash and other plug-ins to be executed only by
trusted web sites of your choice (e.g. your online bank) and additionally
provides Anti-XSS protection.

%prep
%setup -q -c
dos2unix -k -f GPL.txt
dos2unix -k NoScript_License.txt

%build

%install
# install into _waterfox_extdir
install -Dp -m 644 %{SOURCE0} %{buildroot}%{_waterfox_extdir}/%{extension_id}.xpi

# install MetaInfo file for waterfox, etc
appstream-util validate-relax --nonet %{SOURCE1}
DESTDIR=%{buildroot} appstream-util install %{SOURCE1}

%files
%license GPL.txt
%doc NoScript_License.txt mozilla.cfg
%{_waterfox_extdir}/%{extension_id}.xpi
# GNOME Software Center metadata
%{_datadir}/appdata/%{name}.metainfo.xml


%changelog
* Fri Apr 13 2018 Phantom X <megaphantomx at bol dot com dot br> - 5.1.8.5-1
- 5.1.8.5

* Thu Feb 01 2018 Phantom X <megaphantomx at bol dot com dot br> - 5.1.8.4-1
- 5.1.8.4

* Wed Dec 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 5.1.7-1
- Initial spec, borrowed from Fedora mozilla-noscript
