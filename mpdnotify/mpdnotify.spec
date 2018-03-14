%global gitcommitid e04107795398781aa88a973f7e9989c635a53b88
%global shortcommit %(c=%{gitcommitid}; echo ${c:0:7})
%global use_git 1

%if 0%{?with_snapshot}
%global gver .git%{shortcommit}
%endif

Name:           mpdnotify
Version:        0
Release:        2%{?dist}
Summary:        'Now Playing' information via notify-send and mpc 

License:        Public Domain
URL:            https://github.com/vehk/mpdnotify
%if 0%{?with_snapshot}
Source0:        https://github.com/vehk/mpdnotify/archive/%{gitcommitid}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/vehk/mpdnotify/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

BuildArch:      noarch

Requires:       mpc libnotify
#Requires:       ImageMagick

%description
mpdnotify is a simple bash script that uses notify-send and mpc to create
notifications about what song is currently playing in mpd.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{gitcommitid}
%else
%autosetup -n %{name}-%{version}
%endif

# Search links too
sed -e '/^cover=/s|-type f|\0 -o -type l|g' -i %{name}

%build


%install

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/

%files
%doc mpdnotify.conf mpdnotify.png README.md
%{_bindir}/%{name}


%changelog
* Fri Dec 30 2016 Phantom X <megaphantomx at bol dot com dot br> - 0-2
- Search for links.

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br> - 0.gite041077
- Initial spec.
