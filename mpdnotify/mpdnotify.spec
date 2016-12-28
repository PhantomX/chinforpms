%global gitcommitid e04107795398781aa88a973f7e9989c635a53b88
%global shortcommit %(c=%{gitcommitid}; echo ${c:0:7})
%global use_git 1

%if 0%{?use_git}
%global gver .git%{shortcommit}
%endif

Name:           mpdnotify
Version:        0
Release:        1%{?dist}
Summary:        'Now Playing' information via notify-send and mpc 

License:        Public Domain
URL:            https://github.com/vehk/mpdnotify
%if 0%{?use_git}
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
%if 0%{?use_git}
%autosetup -n %{name}-%{gitcommitid}
%else
%autosetup -n %{name}-%{version}
%endif


%build


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/

%files
%doc mpdnotify.conf mpdnotify.png README.md
%{_bindir}/%{name}


%changelog
* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br> - 0.gite041077
- Initial spec.
