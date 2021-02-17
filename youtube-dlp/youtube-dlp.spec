%global forkname youtube-dlc
%global pkgname yt-dlp

Name:           youtube-dlp
Version:        2021.02.15
Release:        1%{?dist}
Summary:        A command-line program to download videos

License:        Unlicense
URL:            https://github.com/pukkandan/yt-dlp

Source0:        %{url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
Source1:        %{pkgname}.conf

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist pycrypto}
BuildRequires:  %{py3_dist mutagen}
BuildRequires:  %{py3_dist setuptools}
BuildRequires:  %{py3_dist pycryptodomex}
BuildRequires:  make
BuildRequires:  pandoc
# Tests failed because of no connection in Koji.
# BuildRequires:  python-nose

Requires:       %{py3_dist pycryptodomex}
Suggests:       aria2c
Provides:       %{forkname} = %{?epoch:%{epoch}:}%{version}-%{release}


%description
A command-line program to download videos from youtube.com and many other video
platforms.

This is a fork of youtube-dlc which is inturn a fork of youtube-dl.


%prep
%autosetup -p1 -n %{pkgname}-%{version}

sed -e "s|Crypto|pycrypto|g" -i setup.py requirements.txt

# remove pre-built file
rm -f %{forkname}

cp -a setup.py setup.py.installpath
# Remove files that are installed to the wrong path
sed -i '/%{forkname}.bash-completion/d' setup.py
sed -i '/%{forkname}.fish/d' setup.py
sed -i '/README.txt/d' setup.py

# Remove interpreter shebang from module files.
find youtube_dlc -type f -exec sed -i -e '1{/^\#!\/usr\/bin\/env python$/d;};' {} +


%build
%py3_build

%make_build youtube-dlc.1 bash-completion zsh-completion fish-completion

%install
%py3_install

mkdir -p %{buildroot}%{_sysconfdir}
install -pm0644 %{S:1} %{buildroot}%{_sysconfdir}/

mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
install -pm0644 %{forkname}.bash-completion \
  %{buildroot}%{_datadir}/bash-completion/completions/%{forkname}

mkdir -p %{buildroot}%{_datadir}/zsh/site-functions/
install -pm0644 %{forkname}.zsh \
  %{buildroot}%{_datadir}/zsh/site-functions/_%{forkname}

mkdir -p %{buildroot}%{_datadir}/fish/vendor_functions.d
install -pm0644 %{forkname}.fish \
  %{buildroot}%{_datadir}/fish/vendor_functions.d/%{forkname}.fish


%check
# This basically cannot work without massive .flake8rc
# starts with flake8 and of course no contributors bothered to make
# their code truly PEP8 compliant.
#
# make offlinetest


%files
%doc CONTRIBUTORS Changelog.md README.md
%license LICENSE
%{_bindir}/%{forkname}
%config(noreplace) %{_sysconfdir}/%{pkgname}.conf
%{_mandir}/man1/%{forkname}.1*
%{python3_sitelib}/youtube_dlc/
%{python3_sitelib}/yt_dlp*.egg-info
%{_datadir}/bash-completion/completions/%{forkname}
%{_datadir}/zsh/site-functions/_%{forkname}
%{_datadir}/fish/vendor_functions.d/%{forkname}.fish


%changelog
* Tue Feb 16 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.02.15-1
- 2021.02.15

* Tue Feb 09 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.02.09-1
- Initial spec, borrowed from youtube-dl.spec
