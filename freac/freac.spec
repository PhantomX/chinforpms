%global date 20180306
%global prerel 1

%global freaccdkver 1.1
%global smoothver 0.8.74

%if 0%{?prerel}
%global prereltag .alpha.%{date}
%global prereltarball -alpha-%{date}
%endif

Name:           freac
Version:        1.1
Release:        0.2%{prereltag}%{?dist}
Summary:        A free audio converter and CD ripper

License:        GPLv2
URL:            http://www.freac.org/
Source0:        https://downloads.sourceforge.net/bonkenc/%{name}-%{version}%{?prereltarball}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  freac-cdk-devel >= %{freaccdkver}
BuildRequires:  smooth-devel >= %{smoothver}
BuildRequires:  pkgconfig(libudev)
Requires:       hicolor-icon-theme
Requires:       flac
Requires:       lame
Requires:       libsamplerate
Requires:       opus-tools
Requires:       shntool
Requires:       speex
Requires:       timidity++
Requires:       twolame
Requires:       vorbis-tools
Requires:       wavpack
Requires:       xmp
#Suggests:       aften
Suggests:       alac_decoder
Suggests:       ffmpeg


%description
fre:ac is a free audio converter and CD ripper with support for various
popular formats and encoders. It currently converts between MP3, MP4/M4A,
WMA, Ogg Vorbis, FLAC, AAC, WAV and Bonk formats.


%prep
%autosetup -n %{name}-%{version}%{?prereltarball}

sed -e 's/\r//' -i COPYING Readme

sed -e 's|/lib/|/%{_lib}/|g' -i src/loader/console.cpp src/loader/gui.cpp

%build

export CFLAGS="%{build_cflags}"
export CXXFLAGS="%{build_cxxflags}"
export LDFLAGS="%{build_ldflags}"

%make_build prefix=/usr libdir=%{_libdir}


%install

%make_install prefix=/usr libdir=%{_libdir}

chmod +x %{buildroot}%{_libdir}/%{name}/*.so*

mv %{buildroot}%{_datadir}/doc _docs

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=fre:ac
GenericName=Audio Converter
GenericName[pt_BR]=Conversor de Áudio
Type=Application
Comment=Audio converter and CD ripper
Exec=%{name} --scale:1.2
Icon=%{name}
Terminal=false
Categories=GTK;AudioVideo;
EOF

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
ln -s ../../../../%{name}/icons/%{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

for res in 16 22 24 32 36 48 64 72 96 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert %{buildroot}%{_datadir}/%{name}/icons/%{name}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license COPYING
%doc _docs/*
%{_bindir}/%{name}*
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.png


%changelog
* Wed May 23 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-0.2.alpha.20180306
- Fix dangling icon link

* Tue May 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.1-0.1.alpha.20180306
- Initial spec
