# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global progdir %{_libdir}/%{name}
%global fontname mtextra
%global minver %%(echo %{version} | cut -d. -f4)

Name:           wps-office
Version:        11.1.0.10702
Release:        1%{?dist}
Summary:        WPS Office Suite

License:        Proprietary
URL:            http://wps-community.org/

Source0:        https://wdl1.pcfg.cache.wpscdn.com/wpsdl/wpsoffice/download/linux/%{minver}/%{name}-%{version}.XA-1.x86_64.rpm

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  fontpackages-devel
BuildRequires:  libcxx%{?_isa}
Requires:       dejavu-sans-fonts
Requires:       dejavu-serif-fonts
Requires:       dejavu-sans-mono-fonts
Requires:       liberation-sans-fonts
Requires:       liberation-serif-fonts
Requires:       liberation-mono-fonts
Requires:       hicolor-icon-theme

Provides:       bundled(qt5-qtbase) = 5.12.9
Provides:       bundled(qt5-qtwebkit) = 5.212.0
Provides:       bundled(libssl) = 1.1

%global __provides_exclude_from ^%{_libdir}/%{name}/.*

%global __requires_exclude ^libaeocenter.so*
%global __requires_exclude %__requires_exclude|^libauth.so*
%global __requires_exclude %__requires_exclude|^libavcodec.so*
%global __requires_exclude %__requires_exclude|^libavdevice.so*
%global __requires_exclude %__requires_exclude|^libavformat.so*
%global __requires_exclude %__requires_exclude|^libavutil.so*
%global __requires_exclude %__requires_exclude|^libcef.so*
%global __requires_exclude %__requires_exclude|^libcrypto.so*
%global __requires_exclude %__requires_exclude|^libc\\+\\+.so
%global __requires_exclude %__requires_exclude|^libcurl.so*
%global __requires_exclude %__requires_exclude|^libdatasourcereader.so*
%global __requires_exclude %__requires_exclude|^libdocwriter.so*
%global __requires_exclude %__requires_exclude|^libetapi.so*
%global __requires_exclude %__requires_exclude|^libethtmlrw2.so*
%global __requires_exclude %__requires_exclude|^libethtmrw.so*
%global __requires_exclude %__requires_exclude|^libetmain.so*
%global __requires_exclude %__requires_exclude|^libetsolver.so*
%global __requires_exclude %__requires_exclude|^libetxmlrw.so*
%global __requires_exclude %__requires_exclude|^libexcel2003htmlrw.so*
%global __requires_exclude %__requires_exclude|^libexcelrw.so*
%global __requires_exclude %__requires_exclude|^libfriso.so*
%global __requires_exclude %__requires_exclude|^libgriddrawer.so*
%global __requires_exclude %__requires_exclude|^libhtml2.so*
%global __requires_exclude %__requires_exclude|^libhtmlpub.so*
%global __requires_exclude %__requires_exclude|^libicudata.so*
%global __requires_exclude %__requires_exclude|^libicui18n.so*
%global __requires_exclude %__requires_exclude|^libicuuc.so*
%global __requires_exclude %__requires_exclude|^libinkdata.so*
%global __requires_exclude %__requires_exclude|^libjdecontrol.so*
%global __requires_exclude %__requires_exclude|^libjpeg.so*
%global __requires_exclude %__requires_exclude|^libjsapiservice.so*
%global __requires_exclude %__requires_exclude|^libjscefservice.so*
%global __requires_exclude %__requires_exclude|^libkbrowserclient.so*
%global __requires_exclude %__requires_exclude|^libkdcsdk_linux.so*
%global __requires_exclude %__requires_exclude|^libkdownload.so*
%global __requires_exclude %__requires_exclude|^libKMailLib.so*
%global __requires_exclude %__requires_exclude|^libknewshare.so*
%global __requires_exclude %__requires_exclude|^libkpromecloudopendialog.so*
%global __requires_exclude %__requires_exclude|^libkprometheus.so*
%global __requires_exclude %__requires_exclude|^libkqingaccountsdk.so*
%global __requires_exclude %__requires_exclude|^libkrecentfile.so*
%global __requires_exclude %__requires_exclude|^libksmso.so*
%global __requires_exclude %__requires_exclude|^libksoapi.so*
%global __requires_exclude %__requires_exclude|^libksolite.so*
%global __requires_exclude %__requires_exclude|^libkso.so*
%global __requires_exclude %__requires_exclude|^libmediacoder.so*
%global __requires_exclude %__requires_exclude|^libmediaflash.so*
%global __requires_exclude %__requires_exclude|^libmediaplayer.so*
%global __requires_exclude %__requires_exclude|^libmisc_linux.so*
%global __requires_exclude %__requires_exclude|^libmythes.so*
%global __requires_exclude %__requires_exclude|^libnssckbi.so*
%global __requires_exclude %__requires_exclude|^libopencv_world.so*
%global __requires_exclude %__requires_exclude|^libpdfmain.so*
%global __requires_exclude %__requires_exclude|^libpinyintag.so*
%global __requires_exclude %__requires_exclude|^libplayer.so*
%global __requires_exclude %__requires_exclude|^libpng12.so*
%global __requires_exclude %__requires_exclude|^libpptreader.so*
%global __requires_exclude %__requires_exclude|^libpptwriter.so*
%global __requires_exclude %__requires_exclude|^libpptxrw.so*
%global __requires_exclude %__requires_exclude|^libqingipc.so*
%global __requires_exclude %__requires_exclude|^libqpdfpaint.so*
%global __requires_exclude %__requires_exclude|^libQtCore.so*
%global __requires_exclude %__requires_exclude|^libQtDBus.so*
%global __requires_exclude %__requires_exclude|^libQtNetwork.so*
%global __requires_exclude %__requires_exclude|^libQtOpenGL.so*
%global __requires_exclude %__requires_exclude|^libQtScript.so*
%global __requires_exclude %__requires_exclude|^libQtWebKit.so*
%global __requires_exclude %__requires_exclude|^libQtXml.so.4
%global __requires_exclude %__requires_exclude|^libQt5Core.so*
%global __requires_exclude %__requires_exclude|^libQt5Gui.so*
%global __requires_exclude %__requires_exclude|^libQt5Network.so*
%global __requires_exclude %__requires_exclude|^libQt5WebKit.so*
%global __requires_exclude %__requires_exclude|^libQt5WebKitWidgets.so*
%global __requires_exclude %__requires_exclude|^libQt5Widgets.so*
%global __requires_exclude %__requires_exclude|^libQt5ConcurrentKso.so*
%global __requires_exclude %__requires_exclude|^libQt5CoreKso.so*
%global __requires_exclude %__requires_exclude|^libQt5DBusKso.so*
%global __requires_exclude %__requires_exclude|^libQt5GuiKso.so*
%global __requires_exclude %__requires_exclude|^libQt5NetworkKso.so*
%global __requires_exclude %__requires_exclude|^libQt5PrintSupportKso.so*
%global __requires_exclude %__requires_exclude|^libQt5SvgKso.so*
%global __requires_exclude %__requires_exclude|^libQt5WidgetsKso.so*
%global __requires_exclude %__requires_exclude|^libQt5X11ExtrasKso.so*
%global __requires_exclude %__requires_exclude|^libQt5XcbQpaKso.so*
%global __requires_exclude %__requires_exclude|^libQt5XmlKso.so*
%global __requires_exclude %__requires_exclude|^librpcetapi.so*
%global __requires_exclude %__requires_exclude|^librpcetapi_sysqt5.so*
%global __requires_exclude %__requires_exclude|^librpcetapi_wpsqt.so*
%global __requires_exclude %__requires_exclude|^librpcserver.so*
%global __requires_exclude %__requires_exclude|^librpcwppapi.so*
%global __requires_exclude %__requires_exclude|^librpcwppapi_sysqt5.so*
%global __requires_exclude %__requires_exclude|^librpcwppapi_wpsqt.so*
%global __requires_exclude %__requires_exclude|^librpcwpsapi.so*
%global __requires_exclude %__requires_exclude|^librpcwpsapi_sysqt5.so*
%global __requires_exclude %__requires_exclude|^librpcwpsapi_wpsqt.so*
%global __requires_exclude %__requires_exclude|^librtfreader.so*
%global __requires_exclude %__requires_exclude|^libsearchcore.so*
%global __requires_exclude %__requires_exclude|^libspelldllv3.so*
%global __requires_exclude %__requires_exclude|^libssl.so*
%global __requires_exclude %__requires_exclude|^libswfplayer.so*
%global __requires_exclude %__requires_exclude|^libswresample.so*
%global __requires_exclude %__requires_exclude|^libswscale.so*
%global __requires_exclude %__requires_exclude|^libthrift.so*
%global __requires_exclude %__requires_exclude|^libtxtrw.so*
%global __requires_exclude %__requires_exclude|^libuof.so*
%global __requires_exclude %__requires_exclude|^libv8.so*
%global __requires_exclude %__requires_exclude|^libv8_libbase.so*
%global __requires_exclude %__requires_exclude|^libv8_libplatform.so*
%global __requires_exclude %__requires_exclude|^libvbeapi.so*
%global __requires_exclude %__requires_exclude|^libwordconvert.so*
%global __requires_exclude %__requires_exclude|^libwordml12w.so*
%global __requires_exclude %__requires_exclude|^libwppapi.so*
%global __requires_exclude %__requires_exclude|^libwppcore.so*
%global __requires_exclude %__requires_exclude|^libwpphtmlrw.so*
%global __requires_exclude %__requires_exclude|^libwppmain.so*
%global __requires_exclude %__requires_exclude|^libwppoutline.so*
%global __requires_exclude %__requires_exclude|^libwpsapiex.so*
%global __requires_exclude %__requires_exclude|^libwpsapi.so*
%global __requires_exclude %__requires_exclude|^libwpsbox.so*
%global __requires_exclude %__requires_exclude|^libwpscloudsvrimp.so*
%global __requires_exclude %__requires_exclude|^libwpshtmlrw.so*
%global __requires_exclude %__requires_exclude|^libwpsinkdraw.so*
%global __requires_exclude %__requires_exclude|^libwpsio.so*
%global __requires_exclude %__requires_exclude|^libwpsmain.so*
%global __requires_exclude %__requires_exclude|^libwpstablestyle.so*
%global __requires_exclude %__requires_exclude|^libwpswordtool.so*
%global __requires_exclude %__requires_exclude|^libwpsxmlrw.so*
%global __requires_exclude %__requires_exclude|^libxercesc3.so*
%global __requires_exclude %__requires_exclude|^libxlsbrw.so*
%global __requires_exclude %__requires_exclude|^libxlsxrw.so*



%description
WPS Office including Writer, Presentation and Spreadsheets, is a powerful
office suite, which is able to process word file, produce wonderful
slides, and analyze data as well.


%prep
%setup -c -T
rpm2cpio %{S:0} | cpio -imd --no-absolute-filenames

find usr/ -name '*.orig' -delete

find opt/ -name '*.so*' | xargs chmod +x

chmod -x opt/kingsoft/%{name}/office6/cfgs/domain_qing.cfg

cp -p opt/kingsoft/%{name}/office6/mui/default/EULA_linux.html .

sed -e '/^gBinPath=/s|=.*|=%{_libdir}/%{name}|g' -i usr/bin/*

sed -e '/^X-DBUS-/d' -e '/^X-KDE-/d' -e '/^InitialPreference/d' \
  -i usr/share/applications/*.desktop

sed \
  -e 's| weight=".0"| weight="40"|g' \
  -e 's| weight="100"| weight="40"|g' \
  -i usr/share/mime/packages/*.xml


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
rm -fv %{buildroot}%{progdir}/office6/librpcetapi.so
rm -fv %{buildroot}%{progdir}/office6/librpcwppapi.so
rm -fv %{buildroot}%{progdir}/office6/librpcwpsapi.so
rm -fv %{buildroot}%{progdir}/office6/addons/cef/libcairo.so*
rm -fv %{buildroot}%{progdir}/office6/addons/cef/libpng*.so*

for i in \
  libtcmalloc libswscale libswresample libssl libpng12 libjpeg \
  libcrypto libavutil libavformat libavcodec \
  libQtWebKit libQtScript libQtOpenGL libQtNetwork \
  libQtDBus libQtCore libKMailLib addons/ruby/libQtScript \
  libQt5ConcurrentKso libQt5CoreKso libQt5DBusKso libQt5GuiKso \
  libQt5NetworkKso libQt5OpenGLKso libQt5PrintSupportKso libQt5SvgKso \
  libQt5WebKit libQt5WebKitWidgets libQt5WidgetsKso libQt5X11ExtrasKso \
  libQt5XcbQpaKso libQt5XmlKso libQt5WebKit libQt5WebKitWidgets.so \
  ;do
    rm -vf "%{buildroot}%{progdir}/office6/$i.so"
done

abs2rel(){
  realpath -m --relative-to="$2" "$1"
}

missing(){
  if ! [ -e "$1" ] ;then
    echo "File $1 is missing!"
    exit 5
  fi
}

xtcsoname(){
  objdump -p "${1}" | grep SONAME | awk '{print $2}'
}

pushd %{buildroot}%{progdir}/office6
for file in libQt5*Kso.so.* ;do
  if [ -e "$file" ] && [ ! -L "$file" ] ;then
    SONAME=$(xtcsoname ${file})
    ln -s $file "${SONAME//Kso}"
  fi
done
popd

reldir=$(abs2rel %{_libdir} %{progdir}/office6)
for file in %{_libdir}/libc++.so.* ;do
  missing "$file"
  if [ -L "$file" ] ;then
    ln -sf ${reldir}/$(basename $file) %{buildroot}%{progdir}/office6/libc++.so
  fi
done

mkdir -p %{buildroot}%{_bindir}
install -pm0755 usr/bin/* %{buildroot}%{_bindir}/

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
  mv ${dir}/mimetypes/%{name}*.png \
    ${dir}/apps/
done

mkdir -p %{buildroot}%{_datadir}/mime/packages
install -pm0644 usr/share/mime/packages/*.xml \
  %{buildroot}%{_datadir}/mime/packages/

mkdir -p %{buildroot}%{_datadir}/templates
install -pm0644 usr/share/templates/*.desktop \
  %{buildroot}%{_datadir}/templates/


%files
%license EULA_linux.html
%{_bindir}/*
%{progdir}/office6
%{progdir}/templates
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/mime/packages/*.xml
%{_datadir}/templates/*.desktop


%changelog
* Fri Sep 10 2021 - 11.1.0.10702-1
- 11.1.0.10702

* Wed Jun 30 2021 - 11.1.0.10161-1
- 11.1.0.10161

* Wed Oct 28 2020 - 11.1.0.9719-1
- 11.1.0.9719

* Fri Feb 28 2020 - 11.1.0.9126-1
- 11.1.0.9126

* Fri Feb 21 2020 - 11.1.0.9080-1
- Initial spec
