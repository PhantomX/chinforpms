Name:           tush
Version:        1.1.1
Release:        1%{?dist}
Summary:        The Utility for SNES Headers

License:        Unknown
URL:            https://www.romhacking.net/utilities/608

Source0:        tush.zip

Patch0:         0001-fix-OpenDialog-crash.patch


BuildRequires:  gcc-c++
BuildRequires:  wxGTK3-devel
Requires:       gnome-icon-theme


%description
TUSH is a tool for adding or removing headers from SNES roms.

%prep
%autosetup -n %{name} -p1
rm -f *.exe
sed -e 's/\r//' -i *.txt

sed \
  -e 's|-Os -pipe|%{build_cxxflags}|g' \
  -e '/LDFLAGS/s|-s|%{build_ldflags}|g' \
  -i src/Makefile


%build
%make_build -C src WXCONFIG=wx-config-3.0


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 src/%{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<'EOF'
[Desktop Entry]
Name=TUSH
Comment=The Utility for SNES Headers
Exec=%{name}
Icon=applications-games
Terminal=false
Type=Application
Categories=Utility;
EOF

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%doc changes.txt readme.txt
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop


%changelog
* Sat Nov 20 2021 Phantom X <megaphantomx at hotmail dot com>
- Initial spec
