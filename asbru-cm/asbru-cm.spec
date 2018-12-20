%global _bashcompletiondir %(pkg-config --variable=completionsdir bash-completion)

Name:           asbru-cm
Version:        5.1.0
Release:        1%{?dist}
Summary:        A multi-purpose SSH/terminal connection manager

License:        GPLv3+
URL:            https://asbru-cm.net
Source0:        https://github.com/asbru-cm/asbru-cm/archive/%{version}/%{name}-%{version}.tar.gz

# Dirty way to disable gconf
Patch0:         %{name}-nogconf.patch
# Fix passwords with TigerVNC
Patch1:         %{name}-vncpasswd.patch

BuildArch:      noarch

BuildRequires:  pkgconfig(bash-completion)
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig
Requires:       perl-interpreter
Requires:       perl(Carp)
Requires:       perl(Compress::Raw::Zlib)
Requires:       perl(Crypt::CBC)
Requires:       perl(Crypt::Rijndael)
Requires:       perl(Crypt::Blowfish)
Requires:       perl(Data::Dumper)
Requires:       perl(Digest::SHA)
Requires:       perl(DynaLoader)
Requires:       perl(Encode)
Requires:       perl(Expect)
Requires:       perl(Exporter)
Requires:       perl(File::Basename)
Requires:       perl(File::Copy)
Requires:       perl(FindBin)
Requires:       perl(Gtk2)
#Requires:       perl(Gtk2::AppIndicator)
Requires:       perl(Gtk2::Ex::Simple::List)
Requires:       perl(Gtk2::Ex::Simple::TiedCommon)
Requires:       perl(Gtk2::GladeXML)
Requires:       perl(Gtk2::SourceView2)
Requires:       perl(Gtk2::Unique)
Requires:       perl(IO::Handle)
Requires:       perl(IO::Stty)
Requires:       perl(IO::Tty)
Requires:       perl(IO::Socket)
Requires:       perl(IO::Socket::INET)
Requires:       perl(MIME::Base64)
Requires:       perl(Net::ARP)
Requires:       perl(Net::Ping)
Requires:       perl(HTTP::Proxy)
Requires:       perl(OSSP::uuid)
Requires:       perl(POSIX)
Requires:       perl(Socket)
Requires:       perl(Socket6)
Requires:       perl(Storable)
Requires:       perl(Sys::Hostname)
Requires:       perl(Time::HiRes)
Requires:       perl(XML::Parser)
Requires:       perl(YAML)
Requires:       perl(constant)
Requires:       perl(lib)
Requires:       perl(strict)
Requires:       perl(utf8)
Requires:       perl(vars)
Requires:       perl(warnings)
Requires:       perl-Gnome2-Vte
Requires:       vte
Requires:       ftp
Requires:       telnet
Requires:       bash


%description
Ásbrú Connection Manager is a user interface that helps organizing
remote terminal sessions and automating repetitive tasks.


%prep
%autosetup -p1

sed -r -e "s|\\\$RealBin[ ]*\.[ ]*'|'%{_datadir}/%{name}/lib|g" -i lib/pac_conn
sed -r -e "s|\\\$RealBin,|'%{_datadir}/%{name}',|g" -i lib/pac_conn
find . -type f -exec sed -i \
  -e "s|\$RealBin[ ]*\.[ ]*'|'%{_datadir}/%{name}|g" \
  -e 's|"\$RealBin/|"%{_datadir}/%{name}/|g' \
  -e 's|/\.\.\(/\)|\1|' \
  '{}' \+

sed -r \
  -e 's|(^Categories=).*|\1GTK;Network;|' \
  -e 's|(^Actions=.*;)|\1Tray;|' \
  -i res/%{name}.desktop

%build


%check
desktop-file-validate res/%{name}.desktop


%install
mkdir -p %{buildroot}/{%{_mandir}/man1,%{_bindir}}
mkdir -p %{buildroot}/%{_datadir}/{%{name}/{lib,res},applications}
mkdir -p %{buildroot}/%{_bashcompletiondir}
mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/{24x24,64x64,256x256,scalable}/apps

install -m 755 %{name} %{buildroot}/%{_bindir}/%{name}
install -m 755 utils/pac_from_mcm.pl %{buildroot}/%{_bindir}/%{name}_from_mcm
install -m 755 utils/pac_from_putty.pl %{buildroot}/%{_bindir}/%{name}_from_putty

cp -a res/%{name}.desktop %{buildroot}/%{_datadir}/applications/%{name}.desktop
cp -a res/%{name}.1 %{buildroot}/%{_mandir}/man1/%{name}.1
cp -a res/asbru_bash_completion %{buildroot}/%{_bashcompletiondir}/%{name}

# Copy the icons over to /usr/share/icons/
cp -a res/asbru-logo-24.png %{buildroot}/%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
cp -a res/asbru-logo-64.png %{buildroot}/%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
cp -a res/asbru-logo-256.png %{buildroot}/%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
cp -a res/asbru-logo.svg %{buildroot}/%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# Copy the remaining resources and libraries
cp -a res/*.{png,jpg,pl,glade} res/termcap %{buildroot}/%{_datadir}/%{name}/res/
cp -a lib/* %{buildroot}/%{_datadir}/%{name}/lib/


%files
%doc README.md
%license LICENSE
%{_mandir}/man1/%{name}*
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_bashcompletiondir}/%{name}*
%{_bindir}/%{name}*


%changelog
* Thu Jul 26 2018 Phantom X <megaphantomx at bol dot com dot br> - 5.1.0-1
- 5.1.0

* Fri Jun 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 5.0.0-1
- Initial spec, mixgin old Fedora pacmanager and asbru official specs
