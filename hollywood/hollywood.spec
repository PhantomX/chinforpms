Name:           hollywood
Version:        1.18
Release:        1%{?dist}
Summary:        Fill your console with Hollywood melodrama technobabble

License:        ASL 2.0
URL:            http://launchpad.net/%{name}
Source0:        https://launchpad.net/%{name}/trunk/%{version}/+download/%{name}_%{version}.orig.tar.gz
Source1:        copyright

BuildArch:      noarch

BuildRequires:  sed
Requires:       apg
Requires:       bmon
# img2txt
Requires:       caca-utils
Requires:       ccze
Requires:       cmatrix
# stat
Requires:       coreutils
Requires:       htop
Requires:       jp2a
Requires:       man
Requires:       mlocate
# errno
Requires:       moreutils
Requires:       mplayer
# tput
Requires:       ncurses
Requires:       newsbeuter
Requires:       openssh-clients
# pygmentize
Requires:       python3-pygments
#Requires:       rsstail
#Requires:       speedometer
#Requires:       ticker
Requires:       tmux
Requires:       tree
# hexdump
Requires:       util-linux
# view
Requires:       vim
Requires:       w3m

%description
This utility will split your console into a multiple panes of genuine
technobabble, perfectly suitable for any Hollywood geek melodrama.
It is particularly suitable on any number of computer consoles in the
background of any excellent schlock technothriller.

%prep
%autosetup

sed -i \
  -e 's|lib/hollywood/|/usr/libexec/$PKG/|g' \
  -e '/^widget_dir=/s|=.*$|="/usr/libexec/$PKG"|g' \
  -e '/^WIDGET_DIR=/s|=.*$|="/usr/libexec/$PKG"|g' \
  -e 's|lib/$PKG/|/usr/libexec/$PKG/|g' \
  bin/%{name} bin/wallstreet

sed -i \
  -e 's|lib/hollywood/|/usr/libexec/hollywood/|g' \
  lib/{%{name},wallstreet}/*

sed -i -e '/^dir=/s|=.*$|=/usr/share/$PKG|g' lib/%{name}/mplayer || exit 1

%{__cp} %{SOURCE1} .

%build

%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 bin/* %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_libexecdir}/{%{name},wallstreet}
install -pm0755 lib/%{name}/* %{buildroot}%{_libexecdir}/%{name}/
install -pm0755 lib/wallstreet/* %{buildroot}%{_libexecdir}/wallstreet/

mkdir -p %{buildroot}%{_datadir}/{%{name},wallstreet}
install -pm0644 share/%{name}/* %{buildroot}%{_datadir}/%{name}/
install -pm0644 share/wallstreet/* %{buildroot}%{_datadir}/wallstreet/

mkdir -p %{buildroot}%{_mandir}/man1
install -pm0644 share/man/man1/%{name}.1 %{buildroot}%{_mandir}/man1


%files
%license copyright
%doc ChangeLog README TODO
%{_bindir}/*
%{_libexecdir}/%{name}/*
%{_libexecdir}/wallstreet/*
%{_datadir}/%{name}/*
%{_datadir}/wallstreet/*
%{_mandir}/man1/%{name}.1*

%changelog
* Sat Jun 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.18-1
- 1.18
- Disable speedometer requires, no python3

* Fri May 10 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.15-1
- 1.15

* Thu Jul 26 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.14-1
- 1.14
- R: cmatrix, jp2a, newsbeuter, python3-pygments, speedometer, w3m
- R: coreutils, man, ncurses, util-linux

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.12-1
- 1.12

* Sat Dec  3 2016 Phantom X <megaphantomx at bol com br> - 1.11-1
- First spec.
