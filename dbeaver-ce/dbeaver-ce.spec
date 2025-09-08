%global _build_id_links none
%undefine _debugsource_packages
%global __jar_repack %{nil}

%global rname   dbeaver

%global jre_ver 21

%global vc_url https://github.com/%{rname}/%{rname}

Name:           %{rname}-ce
Version:        25.2.0
Release:        1%{?dist}
Summary:        Free database tool

License:        Apache-2.0
URL:            https://dbeaver.io

Source0:        %{vc_url}/releases/download/%{version}/%{name}-%{version}-linux.gtk.%{_arch}-nojdk.tar.gz

ExclusiveArch:  x86_64 aarch64

BuildRequires:  desktop-file-utils
BuildRequires:  unzip
BuildRequires:  ImageMagick
Requires:       jre-%{jre_ver}
Requires:       hicolor-icon-theme

%global __provides_exclude_from ^%{_libdir}/%{name}/.*


%description
Free multi-platform database tool for developers, SQL programmers, database
administrators and analysts. Supports all popular databases: MySQL,
PostgreSQL, MariaDB, SQLite, Oracle, DB2, SQL Server, Sybase, MS Access,
Teradata, Firebird, Derby, etc.


%prep
%autosetup -n %{rname}

sed -e 's/\r//' licenses/*.txt

sed \
  -e 's|org.eclipse.equinox.launcher_.*.jar$|org.eclipse.equinox.launcher.jar|' \
  -e 's|org.eclipse.equinox.launcher.gtk.linux.%{_arch}_.*$|org.eclipse.equinox.launcher.gtk.linux.%{_arch}|' \
  -e '/Dfile.encoding/i-Ddbeaver.distribution.type=rpm' \
  -i %{rname}.ini

cat > %{name}.sh <<'EOF'
#!/usr/bin/bash
app_name=%{rname}
app_path="%{_libdir}/%{name}"
jre_ver=%{jre_ver}
jre_dir="/usr/lib/jvm"

if [ -x "${jre_dir}/temurin-${jre_ver}-jdk/bin/java" ] ;then
  jre_bin="${jre_dir}/temurin-${jre_ver}-jdk/bin/java"
else
  jre_bin="${jre_dir}/jre-${jre_ver}/bin/java"
fi
exec "${app_path}/${app_name}" -vm "${jre_bin}" "$@"
EOF

mkdir _jnacleanup
%ifarch x86_64
  mv plugins/com.sun.jna_*/com/sun/jna/linux-x86-64 _jnacleanup/
%endif
%ifarch aarch64
  mv plugins/com.sun.jna_*/com/sun/jna/linux-aarch64 _jnacleanup/
%endif
rm -rf plugins/com.sun.jna_*/com/sun/jna/*/
mv _jnacleanup/* plugins/com.sun.jna_*/com/sun/jna/

pushd plugins
ln -s org.eclipse.equinox.launcher_*.jar org.eclipse.equinox.launcher.jar
ln -s org.eclipse.equinox.launcher.gtk.linux.%{_arch}_*/ org.eclipse.equinox.launcher.gtk.linux.%{_arch}
popd


%build


%install
mkdir -p %{buildroot}%{_libdir}/%{name}
install -pm0755 %{rname} %{buildroot}%{_libdir}/%{name}/

install -pm0644 icon.xpm .eclipseproduct \
  %{buildroot}%{_libdir}/%{name}/

cp -rp configuration configuration features p2 plugins \
  %{buildroot}%{_libdir}/%{name}/

ln -sf "$(realpath -m --relative-to="%{_libdir}/%{name}" "%{_licensedir}/%{name}")" \
  %{buildroot}%{_libdir}/%{name}/licenses

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -pm0644 %{rname}.ini %{buildroot}%{_sysconfdir}/%{name}/
ln -sf "$(realpath -m --relative-to="%{_libdir}/%{name}" "%{_sysconfdir}/%{name}")"/%{rname}.ini \
  %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name}.sh %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key="Path" \
  --set-value="%{_libdir}/%{name}" \
  --set-key="Exec" \
  --set-value="%{name}" \
  --set-icon="%{name}" \
  %{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
install -pm0644 %{rname}.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
ln -sf "$(realpath -m --relative-to="%{_libdir}/%{name}" "%{_datadir}/icons/hicolor/256x256/apps")"/%{name}.png \
  %{buildroot}%{_libdir}/%{name}/%{rname}.png

for res in 16 24 32 48 64 96 128 192 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick %{rname}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done


%files
%license licenses/*.{txt,html}
%doc readme.txt
%config %{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png


%changelog
* Fri Sep 05 2025 Phantom X <megaphantomx at hotmail dot com> - 25.2.0-1
- 25.2.0

* Mon Aug 18 2025 Phantom X <megaphantomx at hotmail dot com> - 25.1.5-1
- 25.1.5

* Tue Aug 12 2025 Phantom X <megaphantomx at hotmail dot com> - 25.1.4-1
- 25.1.4

* Wed Jul 16 2025 Phantom X <megaphantomx at hotmail dot com> - 25.1.2-1
- 25.1.2

* Tue Jun 03 2025 Phantom X <megaphantomx at hotmail dot com> - 25.1.0-1
- 25.1.0

* Wed May 21 2025 Phantom X <megaphantomx at hotmail dot com> - 25.0.5-1
- 25.0.5

* Mon Mar 31 2025 Phantom X <megaphantomx at hotmail dot com> - 25.0.1-1
- 25.0.1

* Mon Mar 10 2025 Phantom X <megaphantomx at hotmail dot com> - 25.0.0-1
- 25.0.0

* Thu Feb 27 2025 Phantom X <megaphantomx at hotmail dot com> - 24.3.5-1
- 24.3.5
- jre_ver 21

* Tue Jan 28 2025 Phantom X <megaphantomx at hotmail dot com> - 24.3.3-1
- 24.3.3

* Mon Jan 06 2025 Phantom X <megaphantomx at hotmail dot com> - 24.3.2-1
- 24.3.2

* Fri Dec 27 2024 Phantom X <megaphantomx at hotmail dot com> - 24.3.1-1
- 24.3.1

* Wed Dec 11 2024 Phantom X <megaphantomx at hotmail dot com> - 24.3.0-1
- 24.3.0

* Wed Nov 27 2024 Phantom X <megaphantomx at hotmail dot com> - 24.2.5-1
- 24.2.5

* Sun Nov 10 2024 Phantom X <megaphantomx at hotmail dot com> - 24.2.4-1
- 24.2.4

* Tue Oct 22 2024 Phantom X <megaphantomx at hotmail dot com> - 24.2.3-1
- 24.2.3

* Sun Oct 13 2024 Phantom X <megaphantomx at hotmail dot com> - 24.2.2-1
- 24.2.2

* Sun Sep 22 2024 Phantom X <megaphantomx at hotmail dot com> - 24.2.1-1
- 24.2.1

* Tue Sep 17 2024 Phantom X <megaphantomx at hotmail dot com> - 24.2.0-1
- 24.2.0

* Fri Aug 09 2024 Phantom X <megaphantomx at hotmail dot com> - 24.1.4-1
- 24.1.4

* Wed Jul 24 2024 Phantom X <megaphantomx at hotmail dot com> - 24.1.3-1
- 24.1.3

* Mon Jul 15 2024 Phantom X <megaphantomx at hotmail dot com> - 24.1.2-1
- 24.1.2

* Mon Jul 01 2024 Phantom X <megaphantomx at hotmail dot com> - 24.1.1-1
- 24.1.1

* Tue Jun 18 2024 Phantom X <megaphantomx at hotmail dot com> - 24.1.0-1
- 24.1.0

* Mon May 20 2024 Phantom X <megaphantomx at hotmail dot com> - 24.0.5-1
- 24.0.5

* Fri May 10 2024 Phantom X <megaphantomx at hotmail dot com> - 24.0.4-1
- 24.0.4
- Hardcode Java version

* Mon Apr 22 2024 Phantom X <megaphantomx at hotmail dot com> - 24.0.3-1
- 24.0.3

* Tue Apr 16 2024 Phantom X <megaphantomx at hotmail dot com> - 24.0.2-1
- 24.0.2

* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 24.0.1-1
- 24.0.1

* Wed Feb 07 2024 Phantom X <megaphantomx at hotmail dot com> - 23.3.4-1
- 23.3.4

* Thu Jan 25 2024 Phantom X <megaphantomx at hotmail dot com> - 23.3.3-1
- 23.3.3

* Tue Dec 26 2023 Phantom X <megaphantomx at hotmail dot com> - 23.3.1-1
- 23.3.1

* Wed Nov 01 2023 Phantom X <megaphantomx at hotmail dot com> - 23.2.3-1
- 23.2.3

* Sun Oct 15 2023 Phantom X <megaphantomx at hotmail dot com> - 23.2.2-1
- 23.2.2

* Tue Sep 26 2023 Phantom X <megaphantomx at hotmail dot com> - 23.2.1-1
- 23.2.1

* Mon Sep 11 2023 Phantom X <megaphantomx at hotmail dot com> - 23.2.0-1
- 23.2.0

* Wed Aug 09 2023 Phantom X <megaphantomx at hotmail dot com> - 23.1.4-1
- 23.1.4

* Wed Jun 14 2023 Phantom X <megaphantomx at hotmail dot com> - 23.1.0-1
- 23.1.0

* Mon Apr 17 2023 Phantom X <megaphantomx at hotmail dot com> - 23.0.2-1
- 23.0.2

* Thu Mar 16 2023 Phantom X <megaphantomx at hotmail dot com> - 23.0.0-1
- 23.0.0

* Sat Feb 11 2023 Phantom X <megaphantomx at hotmail dot com> - 22.3.4-1
- 22.3.4

* Mon Jan 09 2023 Phantom X <megaphantomx at hotmail dot com> - 22.3.2-1
- 22.3.2

* Tue Dec 06 2022 Phantom X <megaphantomx at hotmail dot com> - 22.3.0-1
- 22.3.0

* Mon Nov 07 2022 Phantom X <megaphantomx at hotmail dot com> - 22.2.4-1
- 22.2.4

* Wed Nov 02 2022 Phantom X <megaphantomx at hotmail dot com> - 22.2.3-1
- 22.2.3

* Wed Oct 05 2022 Phantom X <megaphantomx at hotmail dot com> - 22.2.1-1
- 22.2.1

* Wed Sep 14 2022 Phantom X <megaphantomx at hotmail dot com> - 22.2.0-1
- 22.2.0

* Thu Jul 28 2022 Phantom X <megaphantomx at hotmail dot com> - 22.1.3-1
- 22.1.3

* Thu Jul 14 2022 Phantom X <megaphantomx at hotmail dot com> - 22.1.2-1
- 22.1.2

* Tue Jun 28 2022 Phantom X <megaphantomx at hotmail dot com> - 22.1.1-1
- 22.1.1

* Wed Jun 01 2022 Phantom X <megaphantomx at hotmail dot com> - 22.0.5-1
- 22.0.5

* Mon Apr 18 2022 Phantom X <megaphantomx at hotmail dot com> - 22.0.3-1
- 22.0.3

* Tue Apr 05 2022 Phantom X <megaphantomx at hotmail dot com> - 22.0.2-1
- Initial spec
