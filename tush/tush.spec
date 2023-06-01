Name:           tush
Version:        1.1.1
Release:        3%{?dist}
Summary:        The Utility for SNES Headers

License:        Unknown
URL:            https://www.romhacking.net/utilities/608

Source0:        tush.zip

Patch0:         0001-fix-OpenDialog-crash.patch


BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  wxGTK-devel >= 3.2
Requires:       gnome-icon-theme


%description
TUSH is a tool for adding or removing headers from SNES roms.

%prep
%autosetup -n %{name} -p1
rm -f *.exe
sed -e 's/\r//' -i *.txt

sed \
  -e 's|^CFLAGS=-Os -pipe|CFLAGS+=|g' \
  -e '/^LDFLAGS=/d' \
  -i src/Makefile

cat > %{name}.desktop <<'EOF'
[Desktop Entry]
Name=TUSH
Comment=The Utility for SNES Headers
Exec=%{name}
Icon=applications-games
Terminal=false
Type=Application
Categories=Utility;
EOF


%build
%make_build -C src WXCONFIG=wx-config-3.2


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 src/%{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{name}.desktop


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%doc changes.txt readme.txt
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop


%changelog
* Fri Apr 21 2023 Phantom X <megaphantomx at hotmail dot com> - 1.1.1-3
- wxGTK 3.2

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1.1.1-2
- Fix for package_note_file

* Sat Nov 20 2021 Phantom X <megaphantomx at hotmail dot com>
- Initial spec
