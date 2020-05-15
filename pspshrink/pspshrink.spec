Name:           pspshrink
Version:        1.1.2
Release:        3%{?dist}
Summary:        Iso compressor for PSP games

License:        GPLv2
URL:            https://code.google.com/p/%{name}/
Source0:        https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  librsvg2-tools
BuildRequires:  pkgconfig(gtkmm-2.4)


%description
PSP shrink is a tool that allows you compress your psp iso files to the cso
format compatible with devhook.


%package ui
Summary:        Iso compressor for PSP games (GTK+ frontend)
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       hicolor-icon-theme

%description ui
PSP shrink is a tool that allows you compress your psp iso files to the cso
format compatible with devhook.

This packages provides the GTK+ frontend.


%prep
%autosetup

mv ChangeLog ChangeLog.orig
head -n 1000 ChangeLog.orig > ChangeLog
touch -r ChangeLog.orig ChangeLog

%build
CXXFLAGS="%{build_cxxflags} -std=c++11" \
%configure \
  --disable-silent-rules
%make_build


%install
%make_install

desktop-file-install \
  --remove-key="Encoding" \
  --set-key="Version" \
  --set-value="1.0" \
  --set-icon="%{name}" \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
ln -s ../../../../pixmaps/%{name}.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

for res in 16 22 24 32 36 48 64 72 96 128 192 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  rsvg-convert data/%{name}.svg -h ${res} -w ${res} \
    -o ${dir}/%{name}.png || exit 1
done

%files
%license COPYING
%doc AUTHORS ChangeLog README
%{_bindir}/%{name}


%files ui
%license COPYING
%{_bindir}/%{name}ui
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/%{name}.*
%{_datadir}/pixmaps/%{name}.svg


%changelog
* Wed May 13 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.1.2-3
- Split ui package

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.1.2-2
- BR: desktop-file-utils

* Sat Jan  7 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.1.2-1
- Initial spec.
