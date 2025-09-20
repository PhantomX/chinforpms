%bcond man 1
%bcond tests 0

%global forkname youtube-dlc

Name:           yt-dlp
Version:        2025.09.05
Release:        101%{?dist}
Epoch:          1
Summary:        A command-line program to download videos

License:        Unlicense
URL:            https://github.com/yt-dlp/yt-dlp

Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}.conf

Patch0:         %{url}/commit/a1c98226a4e869a34cc764a9dcf7a4558516308e.patch#/%{name}-gh-a1c9822.patch
Patch1:         %{url}/commit/677997d84eaec0037397f7d935386daa3025b004.patch#/%{name}-gh-677997d.patch

BuildArch:      noarch

BuildRequires:  python3-devel >= 3.10
BuildRequires:  %{py3_dist hatchling}
BuildRequires:  %{py3_dist pycrypto}
BuildRequires:  %{py3_dist mutagen}
BuildRequires:  %{py3_dist setuptools}
BuildRequires:  %{py3_dist pycryptodomex}
BuildRequires:  %{py3_dist websockets}
BuildRequires:  make
%if %{with man}
BuildRequires:  pandoc
%endif
%if %{with tests}
# Needed for %%check
BuildRequires:  %{py3_dist pytest}
%endif

Recommends:     AtomicParsley
Suggests:       aria2c

# ffmpeg-free is now available in Fedora.
Recommends:     /usr/bin/ffmpeg
Recommends:     /usr/bin/ffprobe

Suggests:       %{py3_dist keyring}

Obsoletes:      youtube-dlp < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       youtube-dlp = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{forkname} = %{?epoch:%{epoch}:}%{version}-%{release}


%description
%{name} is a command-line program to download videos from youtube.com and many
other video platforms.

This is a fork of youtube-dlc which is inturn a fork of youtube-dl.


%package bash-completion
Summary:        Bash completion for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       bash-completion
Supplements:    (%{name} and bash-completion)

%description bash-completion
Bash command line completion support for %{name}.

%package zsh-completion
Summary:        Zsh completion for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       zsh
Supplements:    (%{name} and zsh)

%description zsh-completion
Zsh command line completion support for %{name}.

%package fish-completion
Summary:        Fish completion for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       fish
Supplements:    (%{name} and fish)

%description fish-completion
Fish command line completion support for %{name}.


%prep
%autosetup -p1

# remove pre-built file
rm -f %{name}

# Remove interpreter shebang from module files.
find yt_dlp -type f -exec sed -i -e '1{\@^#!.*@d}' {} +

sed \
  -e '/^install:/s|%{name} %{name}\.1|%{name}\.1|g' \
  -e '/$(DESTDIR)$(BINDIR)/d' \
  -i Makefile

%if %{without man}
sed \
  -e '/^install:/s|%{name}\.1 ||g' \
  -e '/$(DESTDIR)$(MANDIR)/d' \
  -i Makefile
%endif

%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel

%make_build completion-bash completion-zsh completion-fish
%if %{with man}
%make_build %{name}.1
%endif

%install
%pyproject_install

%pyproject_save_files yt_dlp

mkdir -p %{buildroot}%{_mandir}/man1
%make_install MANDIR=%{_mandir} SHAREDIR=%{_datadir}

mkdir -p %{buildroot}%{_sysconfdir}
install -pm0644 %{S:1} %{buildroot}%{_sysconfdir}/


%check
%if %{with tests}
# See https://github.com/yt-dlp/yt-dlp/blob/master/devscripts/run_tests.sh
%pytest -k "not download"
%endif


%files -f %{pyproject_files}
%doc CONTRIBUTORS Changelog.md README.md
%license LICENSE
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%if %{with man}
%{_mandir}/man1/%{name}.1*
%endif

%files bash-completion
%{bash_completions_dir}/%{name}

%files zsh-completion
%{zsh_completions_dir}/_%{name}

%files fish-completion
%{fish_completions_dir}/%{name}.fish


%changelog
* Thu Sep 18 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2025.09.05-101
- Add some upstream fixes

* Sat Sep 06 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2025.09.05-100
- 2025.09.05

* Fri Aug 29 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2025.08.27-100
- 2025.08.27

* Sat Aug 23 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2025.08.22-100
- 2025.08.22

* Mon Aug 11 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2025.08.11-100
- 2025.08.11

* Tue Jul 22 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2025.07.21-100
- 2025.07.21

* Tue Jul 01 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2025.06.30-100
- 2025.06.30

* Thu Jun 26 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2025.06.25-100
- 2025.06.25

* Wed Jun 11 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2025.06.09-100
- 2025.06.09

* Thu May 22 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2025.05.22-100
- 2025.05.22

* Fri May 02 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2025.04.30-100
- 2025.04.30

* Tue Apr 01 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2025.03.31-100
- 2025.03.31

* Wed Mar 26 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2025.03.26-100
- 2025.03.26

* Tue Mar 25 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2025.03.25-100
- 2025.03.25

* Wed Feb 19 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2025.02.19-100
- 2025.02.19

* Sun Jan 26 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2025.01.26-100
- 2025.01.26

* Thu Jan 16 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2025.01.15-100
- 2025.01.15

* Mon Jan 13 2025 Phantom X <megaphantomx at hotmail dot com> - 1:2025.01.12-100
- 2025.01.12

* Wed Dec 25 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2024.12.23-100
- 2024.12.23

* Thu Dec 19 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2024.12.13-100
- 2024.12.13

* Wed Dec 04 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2024.12.03-100
- 2024.12.03

* Thu Nov 28 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2024.11.18-100
- 2024.11.18

* Sun Nov 10 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2024.11.04-100
- 2024.11.04

* Thu Oct 24 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2024.10.22-100
- 2024.10.22

* Sun Oct 13 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2024.10.07-100
- 2024.10.07

* Sat Sep 28 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2024.09.27-100
- 2024.09.27
- Rawhide sync

* Fri Aug 09 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2024.08.06-100
- 2024.08.06

* Tue Aug 06 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2024.08.01-100
- 2024.08.01

* Fri Jul 26 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2024.07.25-100
- 2024.07.25

* Mon Jul 08 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2024.07.07-100
- 2024.07.07

* Thu Jul 04 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2024.07.02-100
- 2024.07.02

* Fri May 31 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2024.05.27-100
- 2024.05.27

* Wed Apr 10 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2024.04.09-100
- 2024.04.09

* Thu Mar 28 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2024.03.10-101
- Fix duplicated files

* Mon Mar 11 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2024.03.10-100
- 2024.03.10

* Thu Jan 04 2024 Phantom X <megaphantomx at hotmail dot com> - 1:2023.12.30-100
- 2023.12.30

* Sun Nov 26 2023 Phantom X <megaphantomx at hotmail dot com> - 1:2023.11.16-100
- 2023.11.14

* Wed Nov 15 2023 Phantom X <megaphantomx at hotmail dot com> - 1:2023.11.14-100
- 2023.11.14

* Sat Oct 14 2023 Phantom X <megaphantomx at hotmail dot com> - 1:2023.10.13-100
- 2023.10.13

* Sat Oct 07 2023 Phantom X <megaphantomx at hotmail dot com> - 2023.10.07-100
- 2023.10.07
- Rawhide sync
- Rename spec, youtube-dlp to yt-dlp

* Sun Oct 01 2023 Phantom X <megaphantomx at hotmail dot com> - 2023.09.24-1
- 2023.09.24

* Mon Jul 24 2023 Phantom X <megaphantomx at hotmail dot com> - 2023.07.06-1
- 2023.07.06

* Thu Jun 22 2023 Phantom X <megaphantomx at hotmail dot com> - 2023.06.22-1
- 2023.06.22

* Sun Mar 05 2023 Phantom X <megaphantomx at hotmail dot com> - 2023.03.04-1
- 2023.03.04

* Sat Mar 04 2023 Phantom X <megaphantomx at hotmail dot com> - 2023.03.03-1
- 2023.03.03

* Fri Feb 17 2023 Phantom X <megaphantomx at hotmail dot com> - 2023.02.17-1
- 2023.02.17

* Mon Jan 02 2023 Phantom X <megaphantomx at hotmail dot com> - 2023.01.02-1
- 2023.01.02

* Mon Nov 14 2022 Phantom X <megaphantomx at hotmail dot com> - 2022.11.11-1
- 2022.11.11

* Wed Oct 05 2022 Phantom X <megaphantomx at hotmail dot com> - 2022.10.04-1
- 2022.10.04

* Thu Sep 01 2022 Phantom X <megaphantomx at hotmail dot com> - 2022.09.01-1
- 2022.09.01

* Thu Aug 25 2022 Phantom X <megaphantomx at hotmail dot com> - 2022.08.19-1
- 2022.08.19

* Sun Aug 14 2022 Phantom X <megaphantomx at hotmail dot com> - 2022.08.08-1
- 2022.08.08

* Mon Jul 25 2022 Phantom X <megaphantomx at hotmail dot com> - 2022.07.18-1
- 2022.07.18

* Thu Jul 07 2022 Phantom X <megaphantomx at hotmail dot com> - 2022.06.29-1
- 2022.06.29

* Tue May 24 2022 Phantom X <megaphantomx at hotmail dot com> - 2022.05.18-1
- 2022.05.18

* Sat Apr 09 2022 Phantom X <megaphantomx at hotmail dot com> - 2022.04.08-1
- 2022.04.08

* Mon Mar 21 2022 Phantom X <megaphantomx at hotmail dot com> - 2022.03.08.1-1
- 2022.03.08.1

* Fri Feb 04 2022 Phantom X <megaphantomx at hotmail dot com> - 2022.02.04-1
- 2022.02.04

* Fri Feb 04 2022 Phantom X <megaphantomx at hotmail dot com> - 2022.02.03-1
- 2022.02.03

* Mon Jan 24 2022 Phantom X <megaphantomx at hotmail dot com> - 2022.01.21-1
- 2022.01.21

* Mon Dec 27 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.12.27-1
- 2021.12.27

* Sun Dec 26 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.12.25-1
- 2021.12.25

* Wed Dec 01 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.12.01-1
- 2021.12.01

* Thu Nov 11 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.11.10.1-1
- 2021.11.10.1

* Mon Oct 25 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.10.22-1
- 2021.10.22

* Wed Oct 13 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.10.10-1
- 2021.10.10

* Fri Oct 01 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.09.25-1
- 2021.09.25

* Mon Sep 06 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.09.02-1
- 2021.09.02
- Update to best packaging practices

* Sun Aug 22 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.08.10-1
- 2021.08.10

* Thu Jul 08 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.07.07-1
- 2021.07.07

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
