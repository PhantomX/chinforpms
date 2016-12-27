Name:           hollywood
Version:        1.11
Release:        1%{?dist}
Summary:        Fill your console with Hollywood melodrama technobabble

License:        Apache-2
URL:            http://launchpad.net/%{name}
Source0:        https://launchpad.net/%{name}/trunk/%{version}/+download/%{name}_%{version}.orig.tar.gz
Source1:        copyright

BuildArch:      noarch

BuildRequires:  sed
Requires:       apg
Requires:       bmon
Requires:       ccze
Requires:       htop
#Requires:       jp2a
Requires:       mlocate
Requires:       moreutils
Requires:       mplayer
Requires:       openssh-clients
#Requires:       speedometer
Requires:       tmux
Requires:       tree
Requires:       vim

%description
This utility will split your console into a multiple panes of genuine
technobabble, perfectly suitable for any Hollywood geek melodrama.
It is particularly suitable on any number of computer consoles in the
background of any excellent schlock technothriller.

%prep
%autosetup

%{__sed} -i \
  -e 's|lib/hollywood/|/usr/libexec/$PKG/|g' \
  -e '/^widget_dir=/s|=.*$|=/usr/libexec/$PKG|g' \
  -e 's|lib/$PKG/|/usr/libexec/$PKG/|g' \
  bin/%{name} bin/wallstreet

%{__sed} -i \
  -e 's|lib/hollywood/|/usr/libexec/hollywood/|g' \
  lib/{%{name},wallstreet}/*

%{__sed} -i -e '/^dir=/s|=.*$|=/usr/share/$PKG|g' lib/%{name}/mplayer || exit 1

%{__cp} %{SOURCE1} .

%build

%install
rm -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -pm0755 bin/* %{buildroot}%{_bindir}/

%{__mkdir_p} %{buildroot}%{_libexecdir}/{%{name},wallstreet}
%{__install} -pm0755 lib/%{name}/* %{buildroot}%{_libexecdir}/%{name}/
%{__install} -pm0755 lib/wallstreet/* %{buildroot}%{_libexecdir}/wallstreet/

%{__mkdir_p} %{buildroot}%{_datadir}/{%{name},wallstreet}
%{__install} -pm0644 share/%{name}/* %{buildroot}%{_datadir}/%{name}/
%{__install} -pm0644 share/wallstreet/* %{buildroot}%{_datadir}/wallstreet/

%{__mkdir_p} %{buildroot}%{_mandir}/man1
%{__install} -pm0644 share/man/man1/%{name}.1 %{buildroot}%{_mandir}/man1


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
* Sat Dec  3 2016 Phantom X <megaphantomx at bol com br>
- First spec.
