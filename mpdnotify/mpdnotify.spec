%global commit 36e3ac8380e87193351fa3e1b061358b0a200fce
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20171127
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           mpdnotify
Version:        0
Release:        3%{?gver}%{?dist}
Summary:        'Now Playing' information via notify-send and mpc 

License:        Public Domain
URL:            https://github.com/vehk/mpdnotify
%if 0%{?with_snapshot}
Source0:        https://github.com/vehk/mpdnotify/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/vehk/mpdnotify/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

BuildArch:      noarch

Requires:       mpc libnotify
#Requires:       ImageMagick

%description
mpdnotify is a simple bash script that uses notify-send and mpc to create
notifications about what song is currently playing in mpd.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit}
%else
%autosetup -n %{name}-%{version}
%endif

# Search links too
sed -e '/^    cover=/s|-type f|\0 -o -type l|g' -i.orig %{name}

%build


%install

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/

%files
%doc mpdnotify.conf mpdnotify.png README.md
%{_bindir}/%{name}


%changelog
* Mon Apr 16 2018 Phantom X <megaphantomx at bol dot com dot br> - 0-3.20171127git6e3ac8
- New snapshot.

* Fri Dec 30 2016 Phantom X <megaphantomx at bol dot com dot br> - 0-2
- Search for links.

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br> - 0.gite041077
- Initial spec.
