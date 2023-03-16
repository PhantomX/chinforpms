Name:           pipe-viewer
Version:        0.4.5
Release:        1%{?dist}
Summary:        A lightweight YouTube client for Linux

License:        Artistic-2.0
URL:            https://github.com/trizen/%{name}

Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

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

Requires:       perl(JSON::XS)
Requires:       perl(LWP::UserAgent::Cached)
Requires:       perl(Parallel::ForkManager) >= 2.02
Requires:       perl(Term::ReadLine::Gnu)
Requires:       perl(Unicode::GCString)
Recommends:     ffmpeg
Recommends:     (mpv or vlc)
Recommends:     wget
Recommends:     (youtube-dlp or youtube-dl)

%{?perl_default_filter}

%description
%{name} is a lightweight YouTube client for Linux, without requiring an API key.


%package gtk
Summary:        A Nintendo 3DS Emulator (Qt frontend)
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
%autosetup -p1


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
  convert share/icons/gtk-%{name}.png \
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
* Sat Feb 11 2023 Phantom X <megaphantomx at hotmail dot com> - 0.4.5-1
- 0.4.5

* Sat Dec 17 2022 Phantom X <megaphantomx at hotmail dot com> - 0.4.4-1
- Initial spec
