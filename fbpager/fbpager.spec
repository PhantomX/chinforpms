%global commit 8e0927e6365ef295bab9a6037e0647cb9cc57fb2
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20090221

%global gver .%{date}git%{shortcommit}

%global src_hash 58400d2750f1a4a726b95f8c375eb97c

Name:           fbpager
Version:        0.1.5
Release:        1%{?gver}%{?dist}
Summary:        A pager for fluxbox

License:        MIT
URL:            http://git.fluxbox.org/%{name}.git

# Only git repository available
%dnl Source0:        %{url}/snapshot/%{name}-%{commit}.tar.bz2#/%{name}-%{shortcommit}.tar.bz2
# Broken link, source obtained with Makefile
Source0:        https://copr-dist-git.fedorainfracloud.org/repo/pkgs/phantomx/chinforpms/%{name}/%{name}-%{shortcommit}.tar.xz/%{src_hash}/%{name}-%{shortcommit}.tar.xz
# Man generated from Debian patchset
# xsltproc -nonet /usr/share/sgml/docbook/xsl-stylesheets-1.79.2/manpages/docbook.xsl manpage.dbk -o %%{name}.man
Source1:        %{name}.man
# From Debian
Source2:        %{name}.resource
Source3:        Makefile

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xrender)
Enhances:       fluxbox


%description
%{name} is fbpager: A pager for fluxbox.

%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

cp -p %{S:1} %{name}.1
cp -p %{S:2} %{name}.resource

./autogen.sh


%build
%set_build_flags
CXXFLAGS+=" -std=c++14" \
%configure --enable-xrender
%make_build


%install
%make_install

mkdir -p %{buildroot}%{_mandir}/man1
install -pm0644 %{name}.1 %{buildroot}%{_mandir}/man1/

mkdir -p %{buildroot}%{_datadir}/fluxbox
install -pm0644 %{name}.resource %{buildroot}%{_datadir}/fluxbox/%{name}


%files
%license COPYING
%doc ChangeLog README
%{_bindir}/%{name}
%{_datadir}/fluxbox/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
* Fri Jun 10 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1.5-1.20090221git8e0927e
- Initial spec

