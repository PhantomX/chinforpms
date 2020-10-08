# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global progdir %{_libdir}/%{name}
%global fontname mtextra

Name:           wps-office
Version:        11.1.0.9126
Release:        1%{?dist}
Summary:        WPS Office Suite

License:        Proprietary
URL:            http://wps-community.org/

%global minver  %(echo %{version} | cut -d. -f4)
Source0:        http://wdl1.pcfg.cache.wpscdn.com/wpsdl/wpsoffice/download/linux/%{minver}/%{name}-%{version}.XA-1.x86_64.rpm

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  fontpackages-devel
Requires:       dejavu-sans-fonts
Requires:       dejavu-serif-fonts
Requires:       dejavu-sans-mono-fonts
Requires:       liberation-sans-fonts
Requires:       liberation-serif-fonts
Requires:       liberation-mono-fonts
Requires:       dejavu-math-tex-gyre-fonts
Requires:       %{name}-%{fontname}-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       hicolor-icon-theme

Provides:       bundled(qt) = 4.7.4
Provides:       bundled(qt-x11) = 4.7.4
Provides:       bundled(qtwebkit) = 4.9.3
Provides:       bundled(libssl) = 1.0.0

%global __provides_exclude_from ^%{_libdir}/%{name}/.*

%global __requires_exclude ^libssl.so.1.0.0
%global __requires_exclude %__requires_exclude|^libcrypto.so.1.0.0
%global __requires_exclude %__requires_exclude|^libpng12.so.0
%global __requires_exclude %__requires_exclude|^libavcodec.so.57
%global __requires_exclude %__requires_exclude|^libavformat.so.57
%global __requires_exclude %__requires_exclude|^libavutil.so.55
%global __requires_exclude %__requires_exclude|^libjpeg.so.8
%global __requires_exclude %__requires_exclude|^libKMailLib.so.80
%global __requires_exclude %__requires_exclude|^libQtCore.so.4
%global __requires_exclude %__requires_exclude|^libQtDBus.so.4
%global __requires_exclude %__requires_exclude|^libQtNetwork.so.4
%global __requires_exclude %__requires_exclude|^libQtOpenGL.so.4
%global __requires_exclude %__requires_exclude|^libQtScript.so.4
%global __requires_exclude %__requires_exclude|^libQtWebKit.so.4
%global __requires_exclude %__requires_exclude|^libQtXml.so.4
%global __requires_exclude %__requires_exclude|^libssl.so.1.0.0
%global __requires_exclude %__requires_exclude|^libswresample.so.2
%global __requires_exclude %__requires_exclude|^libswscale.so.4
%global __requires_exclude %__requires_exclude|^libaeocenter.so
%global __requires_exclude %__requires_exclude|^libauth.so
%global __requires_exclude %__requires_exclude|^libdatasourcereader.so
%global __requires_exclude %__requires_exclude|^libdocwriter.so
%global __requires_exclude %__requires_exclude|^libetapi.so
%global __requires_exclude %__requires_exclude|^libethtmlrw2.so
%global __requires_exclude %__requires_exclude|^libethtmrw.so
%global __requires_exclude %__requires_exclude|^libetmain.so
%global __requires_exclude %__requires_exclude|^libetsolver.so
%global __requires_exclude %__requires_exclude|^libetxmlrw.so
%global __requires_exclude %__requires_exclude|^libexcel2003htmlrw.so
%global __requires_exclude %__requires_exclude|^libexcelrw.so
%global __requires_exclude %__requires_exclude|^libfriso.so
%global __requires_exclude %__requires_exclude|^libgriddrawer.so
%global __requires_exclude %__requires_exclude|^libhtml2.so
%global __requires_exclude %__requires_exclude|^libhtmlpub.so
%global __requires_exclude %__requires_exclude|^libinkdata.so
%global __requires_exclude %__requires_exclude|^libjscefservice.so
%global __requires_exclude %__requires_exclude|^libkdcsdk_linux.so
%global __requires_exclude %__requires_exclude|^libkdownload.so
%global __requires_exclude %__requires_exclude|^libkpromecloudopendialog.so
%global __requires_exclude %__requires_exclude|^libkprometheus.so
%global __requires_exclude %__requires_exclude|^libkqingaccountsdk.so
%global __requires_exclude %__requires_exclude|^libkrecentfile.so
%global __requires_exclude %__requires_exclude|^libksmso.so
%global __requires_exclude %__requires_exclude|^libksoapi.so
%global __requires_exclude %__requires_exclude|^libksolite.so
%global __requires_exclude %__requires_exclude|^libkso.so
%global __requires_exclude %__requires_exclude|^libmediacoder.so
%global __requires_exclude %__requires_exclude|^libmediaflash.so
%global __requires_exclude %__requires_exclude|^libmediaplayer.so
%global __requires_exclude %__requires_exclude|^libmisc_linux.so
%global __requires_exclude %__requires_exclude|^libmythes.so
%global __requires_exclude %__requires_exclude|^libnssckbi.so
%global __requires_exclude %__requires_exclude|^libpdfmain.so
%global __requires_exclude %__requires_exclude|^libpinyintag.so
%global __requires_exclude %__requires_exclude|^libplayer.so
%global __requires_exclude %__requires_exclude|^libpptreader.so
%global __requires_exclude %__requires_exclude|^libpptwriter.so
%global __requires_exclude %__requires_exclude|^libpptxrw.so
%global __requires_exclude %__requires_exclude|^libqingipc.so
%global __requires_exclude %__requires_exclude|^libqpdfpaint.so
%global __requires_exclude %__requires_exclude|^librpcetapi.so
%global __requires_exclude %__requires_exclude|^librpcetapi_sysqt5.so
%global __requires_exclude %__requires_exclude|^librpcserver.so
%global __requires_exclude %__requires_exclude|^librpcwppapi.so
%global __requires_exclude %__requires_exclude|^librpcwppapi_sysqt5.so
%global __requires_exclude %__requires_exclude|^librpcwpsapi.so
%global __requires_exclude %__requires_exclude|^librpcwpsapi_sysqt5.so
%global __requires_exclude %__requires_exclude|^librtfreader.so
%global __requires_exclude %__requires_exclude|^libspelldllv3.so
%global __requires_exclude %__requires_exclude|^libswfplayer.so
%global __requires_exclude %__requires_exclude|^libtxtrw.so
%global __requires_exclude %__requires_exclude|^libvbeapi.so
%global __requires_exclude %__requires_exclude|^libwordconvert.so
%global __requires_exclude %__requires_exclude|^libwordml12w.so
%global __requires_exclude %__requires_exclude|^libwppapi.so
%global __requires_exclude %__requires_exclude|^libwppcore.so
%global __requires_exclude %__requires_exclude|^libwpphtmlrw.so
%global __requires_exclude %__requires_exclude|^libwppmain.so
%global __requires_exclude %__requires_exclude|^libwppoutline.so
%global __requires_exclude %__requires_exclude|^libwpsapiex.so
%global __requires_exclude %__requires_exclude|^libwpsapi.so
%global __requires_exclude %__requires_exclude|^libwpscloudsvrimp.so
%global __requires_exclude %__requires_exclude|^libwpshtmlrw.so
%global __requires_exclude %__requires_exclude|^libwpsinkdraw.so
%global __requires_exclude %__requires_exclude|^libwpsio.so
%global __requires_exclude %__requires_exclude|^libwpsmain.so
%global __requires_exclude %__requires_exclude|^libwpstablestyle.so
%global __requires_exclude %__requires_exclude|^libwpswordtool.so
%global __requires_exclude %__requires_exclude|^libwpsxmlrw.so
%global __requires_exclude %__requires_exclude|^libxercesc3.so
%global __requires_exclude %__requires_exclude|^libxlsbrw.so
%global __requires_exclude %__requires_exclude|^libxlsxrw.so

%global __requires_exclude %__requires_exclude|^libcef.so
%global __requires_exclude %__requires_exclude|^libkbrowserclient.so


%description
WPS Office including Writer, Presentation and Spreadsheets, is a powerful
office suite, which is able to process word file, produce wonderful
slides, and analyze data as well.

%package %{fontname}-fonts
Summary:        WPS Office MT Extra font
Requires:       fontpackages-filesystem
BuildArch:      noarch

%description %{fontname}-fonts
MT Extra font distributed with WPS Office.


%prep
%setup -c -T
rpm2cpio %{S:0} | cpio -imdv --no-absolute-filenames

find opt/ -name '*.so*' | xargs chmod +x

cp -p opt/kingsoft/%{name}/office6/mui/default/EULA_linux.txt .

sed -e '/^gBinPath=/s|=.*|=%{_libdir}/%{name}|g' -i usr/bin/*

sed -e '/^X-DBUS-/d' -e '/^X-KDE-/d' -e '/^InitialPreference/d' \
  -i usr/share/applications/*.desktop

sed -e 's| weight=".0"||g' -i usr/share/mime/packages/*.xml


%build


%install
mkdir -p %{buildroot}%{progdir}

mv opt/kingsoft/%{name}/{office6,templates} %{buildroot}%{progdir}/

rm -fv %{buildroot}%{progdir}/office6/libc++*.so*
rm -fv %{buildroot}%{progdir}/office6/libbz2.so*
rm -fv %{buildroot}%{progdir}/office6/libfreebl*.so*
rm -fv %{buildroot}%{progdir}/office6/libnspr4.so*
rm -fv %{buildroot}%{progdir}/office6/libnss3.so*
rm -fv %{buildroot}%{progdir}/office6/libnssdbm3.so*
rm -fv %{buildroot}%{progdir}/office6/libnssutil3.so*
rm -fv %{buildroot}%{progdir}/office6/libplc4.so*
rm -fv %{buildroot}%{progdir}/office6/libodbc.so*
rm -fv %{buildroot}%{progdir}/office6/libsmime3.so*
rm -fv %{buildroot}%{progdir}/office6/libsoftokn3.so*
rm -fv %{buildroot}%{progdir}/office6/libSDL2*.so*
rm -fv %{buildroot}%{progdir}/office6/libtcmalloc.so*

for i in \
  libtcmalloc libswscale libswresample libssl libpng12 libjpeg \
  libcrypto libavutil libavformat libavcodec \
  libQtWebKit libQtScript libQtOpenGL libQtNetwork \
  libQtDBus libQtCore libKMailLib addons/ruby/libQtScript \
  ;do
    rm -vf "%{buildroot}%{progdir}/office6/$i.so"
done

mkdir -p %{buildroot}%{_bindir}
install -pm0755 usr/bin/* %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_fontdir}
install -pm0644 usr/share/fonts/%{name}/mtextra.ttf %{buildroot}%{_fontdir}/

mkdir -p %{buildroot}%{_datadir}/applications
for desktop in usr/share/applications/*.desktop ;do
  desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications \
    ${desktop}
done

for res in 16 24 32 48 64 128 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/mimetypes
  mkdir -p ${dir}
  install -pm0644 usr/share/icons/hicolor/${res}x${res}/mimetypes/*.png \
    ${dir}/
done
for res in 16 24 32 48 64 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}
  mkdir -p ${dir}/apps
  mv ${dir}/mimetypes/%{name}2019*.png \
    ${dir}/apps/
done

mkdir -p %{buildroot}%{_datadir}/mime/packages
install -pm0644 usr/share/mime/packages/*.xml \
  %{buildroot}%{_datadir}/mime/packages/

mkdir -p %{buildroot}%{_datadir}/templates
install -pm0644 usr/share/templates/*.desktop \
  %{buildroot}%{_datadir}/templates/


%files
%license EULA_linux.txt
%{_bindir}/*
%{progdir}/office6
%{progdir}/templates
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/mime/packages/*.xml
%{_datadir}/templates/*.desktop

%_font_pkg -n %{fontname} mtextra.ttf
%doc EULA_linux.txt


%changelog
* Fri Feb 28 2020 Phantom X <megaphantomx at bol dot com dot br> - 11.1.0.9126-1
- 11.1.0.9126

* Fri Feb 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 11.1.0.9080-1
- Initial spec
