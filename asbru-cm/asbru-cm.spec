%global commit a072b861a213f3caab1184427aa10105d7b5086e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250504
%bcond_without snapshot

BuildArch:      noarch

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global _bashcompletiondir %(pkg-config --variable=completionsdir bash-completion)

%global vc_url  https://github.com/%{name}/%{name}

Name:           asbru-cm
Version:        6.4.1
Release:        4%{?dist}
Summary:        A multi-purpose SSH/terminal connection manager

License:        GPL-3.0-or-later
URL:            https://asbru-cm.net

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
%global ver     %{lua:ver = string.gsub(rpm.expand("%{version}"), "~", ""); print(ver)}
Source0:        %{vc_url}/archive/%{ver}/%{name}-%{ver}.tar.gz
%endif

Patch0:         0001-Always-set-GTK_OVERLAY_SCROLLING.patch

BuildRequires:  pkgconfig(bash-completion)
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig
Requires:       perl-interpreter
Requires:       perl(Carp)
Requires:       perl(Compress::Raw::Zlib)
Requires:       perl(Crypt::CBC) >= 3.04
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
Requires:       perl(Gtk3)
Requires:       perl(Gtk3::SimpleList)
Requires:       perl(IO::Handle)
Requires:       perl(IO::Stty)
Requires:       perl(IO::Tty)
Requires:       perl(IO::Socket)
Requires:       perl(IO::Socket::INET)
Requires:       perl(MIME::Base64)
Requires:       perl(Net::ARP)
Requires:       perl(Net::Ping)
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
Requires:       dbus-x11
Requires:       libwnck3
Requires:       vte291 >= 0.62
Requires:       ftp
Requires:       telnet
Requires:       bash
Suggests:       libappindicator-gtk3
Suggests:       perl(X11::GUITest)
Suggests:       tigervnc-server-minimal


%description
Ásbrú Connection Manager is a user interface that helps organizing
remote terminal sessions and automating repetitive tasks.


%prep
%autosetup -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{ver}} -p1

sed -r -e "s|\\\$RealBin[ ]*\.[ ]*'|'%{_datadir}/%{name}/lib|g" -i lib/asbru_conn
sed -r -e "s|\\\$RealBin,|'%{_datadir}/%{name}/lib',|g" -i lib/asbru_conn
sed -r -e "s|\\\$RealBin/\.\./|%{_datadir}/%{name}/|g" -i lib/asbru_conn
sed -r -e "s|\\\$RealBin/|%{_datadir}/%{name}/lib/|g" -i lib/asbru_conn
find . -type f -exec sed -i \
  -e "s|\$RealBin[ ]*\.[ ]*'|'%{_datadir}/%{name}|g" \
  -e 's|"\$RealBin/|"%{_datadir}/%{name}/|g' \
  -e 's|/\.\.\(/\)|\1|' \
  '{}' \+

sed -e 's|$PATH/asbru_confirm|$PATH/utils/asbru_confirm|g' -i utils/*2*.pl

sed -r \
  -e 's|(^Categories=).*|\1GTK;Network;|' \
  -e 's|(^Actions=.*;)|\1Tray;|' \
  -i res/%{name}.desktop

%build


%check
desktop-file-validate res/%{name}.desktop


%install
mkdir -p %{buildroot}/{%{_mandir}/man1,%{_bindir}}
mkdir -p %{buildroot}/%{_datadir}/{%{name}/{lib,res,utils},applications}
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
cp -a res/*.{png,pl,glade,svg} %{buildroot}%{_datadir}/%{name}/res/
cp -ar res/themes/ %{buildroot}%{_datadir}/%{name}/res/
cp -a lib/* %{buildroot}/%{_datadir}/%{name}/lib/
cp -a utils/asbru_confirm.pl %{buildroot}%{_datadir}/%{name}/utils/
cp -a utils/asbru2pac.pl %{buildroot}%{_datadir}/%{name}/utils/
cp -a utils/pac2asbru.pl %{buildroot}%{_datadir}/%{name}/utils/


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
* Tue Dec 17 2024 Phantom X <megaphantomx at hotmail dot com> - 6.4.1-3.20241010git912227f
- Fix GTK_OVERLAY_SCROLLING

* Thu Dec 01 2022 Phantom X <megaphantomx at hotmail dot com> - 6.4.1-1.20221112git8dce568
- 6.4.2

* Fri Nov 25 2022 Phantom X <megaphantomx at hotmail dot com> - 6.4.1-1
- 6.4.1

* Thu Nov 17 2022 Phantom X <megaphantomx at hotmail dot com> - 6.4.0-1
- 6.4.0

* Fri Jul 15 2022 Phantom X <megaphantomx at hotmail dot com> - 6.3.3-2
- perl-Crypt-CBC 3.04 fix

* Wed May 25 2022 Phantom X <megaphantomx at hotmail dot com> - 6.3.3-1
- 6.3.3

* Mon Apr 11 2022 Phantom X <megaphantomx at hotmail dot com> - 6.3.3-0.2.20220409git1407195
- Bump to improve new KeePassXC support

* Tue Mar 15 2022 Phantom X <megaphantomx at hotmail dot com> - 6.3.3-0.1.20220206git0b6a141
- 6.3.3 snapshot

* Fri Mar 05 2021 Phantom X <megaphantomx at hotmail dot com> - 6.3.2-1
- 6.3.2

* Thu Feb 18 2021 Phantom X <megaphantomx at hotmail dot com> - 6.3.0-1
- 6.3.0

* Tue Dec 29 2020 Phantom X <megaphantomx at hotmail dot com> - 6.2.2-2
- vte upstream fix

* Tue Nov 10 2020 Phantom X <megaphantomx at hotmail dot com> - 6.2.2-1
- 6.2.2

* Tue Oct 27 2020 Phantom X <megaphantomx at hotmail dot com> - 6.2.1-2
- Patch to fix vte291 0.62 issues

* Mon Jun 08 2020 Phantom X <megaphantomx at bol dot com dot br> - 6.2.1-1
- 6.2.1

* Wed May 20 2020 Phantom X <megaphantomx at bol dot com dot br> - 6.2.0-1
- 6.2.0

* Tue May 12 2020 Phantom X <megaphantomx at bol dot com dot br> - 6.1.3-1
- 6.1.4

* Wed Apr 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 6.1.2-1
- 6.1.2

* Sun Mar 29 2020 Phantom X <megaphantomx at bol dot com dot br> - 6.1.1-1
- 6.1.1

* Mon Mar 16 2020 Phantom X <megaphantomx at bol dot com dot br> - 6.1.0~rc2-1
- 6.1.0rc2

* Mon Mar 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 6.1.0~rc1-1
- 6.1.0rc1

* Wed Feb 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 6.0.4-1
- 6.0.4

* Wed Jan 29 2020 Phantom X <megaphantomx at bol dot com dot br> - 6.0.3-2
- Patch to fix resizing crashes

* Wed Jan 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 6.0.3-1
- 6.0.3

* Tue Jan 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 6.0.2-1
- 6.0.2

* Fri Jan 10 2020 Phantom X <megaphantomx at bol dot com dot br> - 6.0.1-1
- 6.0.1

* Tue Nov 26 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.1-2
- Fix search path

* Wed Nov 20 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.1-1
- 5.2.1

* Fri May 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.2.0-1
- 5.2.0

* Thu Jul 26 2018 Phantom X <megaphantomx at bol dot com dot br> - 5.1.0-1
- 5.1.0

* Fri Jun 15 2018 Phantom X <megaphantomx at bol dot com dot br> - 5.0.0-1
- Initial spec, mixgin old Fedora pacmanager and asbru official specs
