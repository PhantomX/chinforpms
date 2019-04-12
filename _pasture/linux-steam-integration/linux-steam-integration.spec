Name:           linux-steam-integration
Version:        0.7.3
Release:        1%{?dist}
Summary:        Helper for enabling better Steam integration on Linux 

License:        LGPLv2
URL:            https://github.com/clearlinux/%{name}

Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.xz

Patch0:          %{name}-paths.patch


BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  pkgconfig(gtk+-3.0)
Requires:       steam

%ifarch x86_64
Requires:       %{name}(x86-32) = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

Provides:       bundled(nica) = 2


%description
Linux Steam Integration is a helper system to make the Steam Client and
Steam games run better on Linux. In a nutshell, LSI automatically applies
various workarounds to get games working, and fixes long standing bugs
in both games and the client.


%package        settings
Summary:        Application for managing Steam integration settings
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    settings
%{name}-settings is an application for managing Steam integration settings.


%prep
%autosetup -p1


%build
%meson \
  -Dwith-shim=co-exist \
  -Dwith-steam-binary=%{_bindir}/steam \
  -Dwith-new-libcxx-abi=true \
  -Dwith-frontend=true \
  -Dwith-libressl-mode=none

%meson_build


%install
%meson_install

mkdir -p %{buildroot}%{_libdir}/lsi
mv %{buildroot}%{_libdir}/*.so %{buildroot}%{_libdir}/lsi/

for desktop in settings steam ;do
  desktop-file-edit \
    --remove-category="Network" \
    --remove-category="FileTransfer" \
    --remove-category="Settings" \
    %{buildroot}/%{_datadir}/applications/lsi-$desktop.desktop
done

%find_lang %{name}


%files
%license LICENSE
%doc README.md TECHNICAL.md
%{_bindir}/lsi-exec
%{_bindir}/lsi-steam
%{_libdir}/lsi/*.so
%{_datadir}/applications/lsi-steam.desktop

%files settings -f %{name}.lang
%license LICENSE
%{_bindir}/lsi-settings
%{_datadir}/applications/lsi-settings.desktop


%changelog
* Tue Jan 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.7.3-1
- Initial spec
