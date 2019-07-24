%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%ifarch x86_64
%global parch amd64
%else
%global parch i386
%endif

%global real_name hakuneko

Name:           %{real_name}-desktop
Version:        5.0.6
Release:        1%{?dist}
Summary:        Manga Downloader

License:        Unlicense and MIT
URL:            https://sourceforge.net/projects/%{real_name}/
Source0:        https://downloads.sourceforge.net/%{real_name}/%{name}_%{version}_linux_%{parch}.rpm
Source1:        https://github.com/manga-download/hakuneko/raw/master/UNLICENSE

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
Requires:       libglvnd-egl%{?_isa}
Requires:       libglvnd-gles%{?_isa}
Requires:       hicolor-icon-theme

%global __provides_exclude_from ^%{_libdir}/%{name}/.*

%global __requires_exclude ^libffmpeg.so
%global __requires_exclude %__requires_exclude|^libVkICD_mock_icd.so


%description
HakuNeko allows you to download manga images from some selected online
manga reader websites.

%prep
%setup -c -T
rpm2cpio %{S:0} | cpio -imdv --no-absolute-filenames

cp %{S:1} .

find usr/lib/%{name}/ -name '*.so*' | xargs chmod +x

chrpath --delete usr/lib/%{name}/%{real_name}

%build

%install
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<'EOF'
#!/usr/bin/sh
LD_LIBRARY_PATH="%{_libdir}/%{name}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec %{_libdir}/%{name}/%{real_name} "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_libdir}/%{name}
cp -rp usr/lib/%{name}/{%{real_name},locales,resources,*.{bin,dat,pak,so}} \
  %{buildroot}%{_libdir}/%{name}/

rm -fv %{buildroot}%{_libdir}/%{name}/libEGL.so*
rm -fv %{buildroot}%{_libdir}/%{name}/libGLESv2.so*

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key="Exec" \
  --set-value="%{name}" \
  usr/share/applications/%{name}.desktop

for res in 16 24 32 48 64 96 128 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 usr/share/icons/hicolor/${res}x${res}/apps/%{name}.png \
    ${dir}/
done


%files
%license UNLICENSE
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png


%changelog
* Tue Jul 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 5.0.6-1
- 5.0.6 testing

* Sun Aug 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.4.0-2
- New source
- Add missing locales directory

* Sun Aug 12 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.4.0-1
- 0.4.0

* Wed Mar 21 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.3.1-1
- 0.3.1

* Sat Mar 03 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.3.0-1
- 0.3.0

* Fri Feb 02 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.2.0-1
- 0.2.0

* Fri Nov 24 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.1.0-1
- 0.1.0

* Sat Oct 14 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.0.32-1
- Fist spec
