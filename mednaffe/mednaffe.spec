%global commit 8cc6e65aca08f0c6c94444594f6289d8a3702e1e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200307
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           mednaffe
Version:        0.9.2
Release:        1%{?gver}%{?dist}
Summary:        A front-end (GUI) for mednafen emulator

License:        GPL-3.0-only
URL:            https://github.com/AmatCoder/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/releases/download/%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        %{name}.appdata.xml

BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.4
BuildRequires:  pkgconfig(glib-2.0) >= 2.32
BuildRequires:  pkgconfig(gthread-2.0)
Requires:       mednafen >= 1.21.1
Requires:       hicolor-icon-theme

%description
Mednaffe is a front-end (GUI) for mednafen emulator.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1


%build
%configure \
  --disable-silent-rules

%make_build


%install
%make_install

rm -rf %{buildroot}/%{_datadir}/doc

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{S:1} %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files
%license COPYING
%doc AUTHORS ChangeLog README
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*.*
%{_datadir}/pixmaps/*.png
%{_metainfodir}/*.xml


%changelog
* Wed Dec 29 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.2-1
- 0.9.2

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.1-1
- 0.9.1

* Mon May 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.8.8-2.20200307git8cc6e65
- Snapshot

* Fri May 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.8.8-1
- Initial spec
