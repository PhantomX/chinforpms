%global commit 36e3ac8380e87193351fa3e1b061358b0a200fce
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20171127
%bcond_without snapshot

BuildArch:      noarch

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           mpdnotify
Version:        0
Release:        4%{?dist}
Summary:        'Now Playing' information via notify-send and mpc 

License:        LicenseRef-Fedora-Public-Domain
URL:            https://github.com/vehk/mpdnotify
%if %{with snapshot}
Source0:        https://github.com/vehk/mpdnotify/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/vehk/mpdnotify/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

Patch0:         0001-ShellCheck-revision.patch

Requires:       libnotify
Requires:       mpc
Requires:       ImageMagick

%description
mpdnotify is a simple bash script that uses notify-send and mpc to create
notifications about what song is currently playing in mpd.

%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1


%build


%install

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/

%files
%doc mpdnotify.conf mpdnotify.png README.md
%{_bindir}/%{name}


%changelog
* Wed Dec 11 2024 Phantom X <megaphantomx at hotmail dot com> - 0-4.20171127git36e3ac8
- ShellCheck revision

* Mon Apr 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 0-3.20171127git6e3ac8
- New snapshot.

* Fri Dec 30 2016 Phantom X <megaphantomx at bol dot com dot br> - 0-2
- Search for links.

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br> - 0.gite041077
- Initial spec.
