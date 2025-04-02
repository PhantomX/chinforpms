%global commit 0d9515e2d2d55bfe4ed0e7ab19a47ca693a85f67
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240818
%bcond_with snapshot

BuildArch:      noarch

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           pipe-viewer
Version:        0.5.5
Release:        1%{?dist}
Summary:        A lightweight YouTube client for Linux

License:        Artistic-2.0
URL:            https://github.com/trizen/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
BuildRequires:  perl-interpreter >= 5.016
BuildRequires:  perl-generators
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Data::Dump)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(HTTP::Request)
BuildRequires:  perl(JSON)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Memoize)
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(List::Util) >= 1.33
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(LWP::Protocol::https)
BuildRequires:  perl(Term::ANSIColor)
BuildRequires:  perl(Term::ReadLine)
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(Text::Wrap)
BuildRequires:  perl(URI::Escape)
# Test
BuildRequires:  perl(Test::More)
# Recommended
BuildRequires:  perl(JSON::XS)
BuildRequires:  perl(LWP::UserAgent::Cached)
BuildRequires:  perl(Parallel::ForkManager) >= 2.02
BuildRequires:  perl(Term::ReadLine::Gnu)
BuildRequires:  perl(Unicode::GCString)
BuildRequires:  perl(Text::Unidecode)

Requires:       perl(JSON::XS)
Requires:       perl(LWP::UserAgent::Cached)
Requires:       perl(Parallel::ForkManager) >= 2.02
Requires:       perl(Term::ReadLine::Gnu)
Requires:       perl(Unicode::GCString)
Requires:       yt-dlp
Recommends:     ffmpeg
Recommends:     (mpv or vlc)
Recommends:     wget

%{?perl_default_filter}

%description
%{name} is a lightweight YouTube client for Linux, without requiring an API key.


%package gtk
Summary:        A lightweight YouTube client for Linux (Qt frontend)
BuildRequires:  perl(Gtk3)
BuildRequires:  perl(File::ShareDir)
BuildRequires:  perl(Storable)
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl(File::ShareDir)
Requires:       hicolor-icon-theme
Recommends:     gnome-icon-theme

%description gtk
%{name} is a lightweight YouTube client for Linux, without requiring an API key.

This is the Gtk frontend.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1


%build
%{__perl} Build.PL --gtk3


%install
./Build install --destdir "%{buildroot}" --installdirs vendor --install_path script=%{_bindir}

find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*


desktop-file-install \
    --delete-original \
    --dir %{buildroot}%{_datadir}/applications \
    %{buildroot}%{perl_vendorlib}/auto/share/dist/WWW-PipeViewer/gtk-%{name}.desktop

for res in 16 22 24 32 36 48 64 72 96 128 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick share/icons/gtk-%{name}.png \
    -filter Lanczos -resize ${res}x${res} ${dir}/gtk-%{name}.png
done


%check
./Build test
desktop-file-validate %{buildroot}%{_datadir}/applications/gtk-%{name}.desktop


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{perl_vendorlib}/*
%exclude %{perl_vendorlib}/auto/
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*


%files gtk
%license LICENSE
%{_bindir}/gtk-%{name}
%{perl_vendorlib}/auto/share/dist/WWW-PipeViewer
%{_datadir}/applications/gtk-%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*


%changelog
* Tue Apr 01 2025 Phantom X <megaphantomx at hotmail dot com> - 0.5.5-1
- 0.5.5

* Mon Feb 17 2025 Phantom X <megaphantomx at hotmail dot com> - 0.5.4-1
- 0.5.4

* Thu Sep 19 2024 Phantom X <megaphantomx at hotmail dot com> - 0.5.3-1
- 0.5.3

* Mon Aug 19 2024 Phantom X <megaphantomx at hotmail dot com> - 0.5.2-1.20240818git0d9515e
- 0.5.2

* Mon May 20 2024 Phantom X <megaphantomx at hotmail dot com> - 0.5.1-1
- 0.5.1

* Thu Mar 07 2024 Phantom X <megaphantomx at hotmail dot com> - 0.5.0-1
- 0.5.0

* Sat Jan 20 2024 Phantom X <megaphantomx at hotmail dot com> - 0.4.9-1.20230604git50a0a7b
- 0.4.9

* Sun Aug 06 2023 Phantom X <megaphantomx at hotmail dot com> - 0.4.8-1
- 0.4.8

* Thu Jun 22 2023 Phantom X <megaphantomx at hotmail dot com> - 0.4.7-1
- 0.4.7

* Thu May 18 2023 Phantom X <megaphantomx at hotmail dot com> - 0.4.6-1
- 0.4.6

* Mon Mar 20 2023 Phantom X <megaphantomx at hotmail dot com> - 0.4.5-2
- Add upstream commit

* Sat Feb 11 2023 Phantom X <megaphantomx at hotmail dot com> - 0.4.5-1
- 0.4.5

* Sat Dec 17 2022 Phantom X <megaphantomx at hotmail dot com> - 0.4.4-1
- Initial spec
