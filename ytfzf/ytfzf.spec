%global commit 8eb2e5228385669cb5e31a30ab7ab862917dc456
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210419
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           ytfzf
Version:        1.2.0
Release:        1%{?dist}
Summary:        A posix script to find and watch youtube videos from the terminal

License:        GPLv3
URL:            https://github.com/pystardust/ytfzf

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

BuildArch:      noarch

BuildRequires:  make
Requires:       ( youtube-dl or youtube-dlp)
Requires:       jq
# shuf
Recommends:     coreutils
Recommends:     fzf
Recommends:     mpv
Recommends:     libnotify
Recommends:     ueberzug

%description
A POSIX script that helps you find Youtube videos (without API) and
opens/downloads them using mpv/youtube-dl


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif


%build


%install
%make_install PREFIX=%{_bindir}


%files
%license LICENSE
%doc README.md docs/USAGE.md docs/conf.sh
%{_bindir}/%{name}


%changelog
* Thu Jul 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.0-1
- 1.2.0

* Mon Apr 26 2021 Phantom X <megaphantomx at hotmail dot com> - 1.1.4-1
- Initial spec
