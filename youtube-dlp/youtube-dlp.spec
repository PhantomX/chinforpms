%global forkname youtube-dlc
%global pkgname yt-dlp

Name:           youtube-dlp
Version:        2021.06.09
Release:        1%{?dist}
Summary:        A command-line program to download videos

License:        Unlicense
URL:            https://github.com/yt-dlp/yt-dlp

Source0:        %{url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
Source1:        %{pkgname}.conf

Patch0:         0001-Use-pycryptodomex-instead-pycryptodome.patch

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

Recommends:     AtomicParsley
Suggests:       aria2c

Provides:       %{forkname} = %{?epoch:%{epoch}:}%{version}-%{release}


%description
A command-line program to download videos from youtube.com and many other video
platforms.

This is a fork of youtube-dlc which is inturn a fork of youtube-dl.


%prep
%autosetup -p1 -n %{pkgname}-%{version}

# remove pre-built file
rm -f %{pkgname}

cp -a setup.py setup.py.installpath
sed -i '/README.txt/d' setup.py

# Remove interpreter shebang from module files.
find yt_dlp -type f -exec sed -i -e '1{/^\#!\/usr\/bin\/env python$/d;};' {} +


%build
%py3_build

%make_build %{pkgname}.1 completion-bash completion-zsh completion-fish

%install
%py3_install

mkdir -p %{buildroot}%{_sysconfdir}
install -pm0644 %{S:1} %{buildroot}%{_sysconfdir}/


%check
# This basically cannot work without massive .flake8rc
# starts with flake8 and of course no contributors bothered to make
# their code truly PEP8 compliant.
#
# make offlinetest


%files
%doc CONTRIBUTORS Changelog.md README.md
%license LICENSE
%{_bindir}/%{pkgname}
%config(noreplace) %{_sysconfdir}/%{pkgname}.conf
%{_mandir}/man1/%{pkgname}.1*
%{python3_sitelib}/yt_dlp/
%{python3_sitelib}/yt_dlp*.egg-info
%{_datadir}/bash-completion/completions/%{pkgname}
%{_datadir}/zsh/site-functions/_%{pkgname}
%{_datadir}/fish/vendor_completions.d/%{pkgname}.fish


%changelog
* Sat Jun 12 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.06.09-1
- 2021.06.09

* Sat Jun 05 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.06.01-1
- 2021.06.01

* Fri May 21 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.05.20-1
- 2021.05.20

* Fri Apr 23 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.04.22-1
- 2021.04.22

* Mon Apr 19 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.04.11-1
- 2021.04.11

* Fri Apr 09 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.04.03-1
- 2021.04.03

* Mon Mar 22 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.03.21-1
- 2021.03.21

* Mon Mar 15 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.03.15-1
- 2021.03.15

* Thu Mar 04 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.03.03.2-1
- 2021.03.03.2

* Thu Feb 25 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.02.24-1
- 2021.02.24

* Thu Feb 18 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.02.15-2
- pycryptodomex fix

* Tue Feb 16 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.02.15-1
- 2021.02.15

* Tue Feb 09 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.02.09-1
- Initial spec, borrowed from youtube-dl.spec
