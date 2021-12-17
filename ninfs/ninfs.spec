%global commit dee583ba3205c4e050e0b193a85a4177eb334159
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210629
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global ver %%{lua:ver = string.gsub(rpm.expand("%{version}"), "~", ""); print(ver)}

%global haccryptover 0.1.1
%global pyctrver 0.5.1

Name:           ninfs
Version:        2.0~a6
Release:        1%{?gver}%{?dist}
Summary:        FUSE program to extract data from Nintendo® game consoles

License:        MIT
URL:            https://github.com/ihaveamac/ninfs

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{ver}/%{name}-%{ver}.tar.gz
%endif

Patch0:         0001-Remove-desktop-file-command-line-parameter.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist haccrypto} = %{haccryptover}
BuildRequires:  %{py3_dist pyctr} = %{pyctrver}
BuildRequires:  %{py3_dist pycryptodomex} >= 3.10.1
BuildRequires:  python3-tkinter
BuildRequires:  desktop-file-utils
Requires:       fuse
Requires:       python3-tkinter
Requires:       hicolor-icon-theme


%description
ninfs is a FUSE program to extract data from Nintendo® game consoles. It works by
presenting a virtual filesystem with the contents of your games, NAND, or SD
card contents, and you can browse and copy out just the files that you need.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install

%pyproject_save_files %{name}


mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<'EOF'
[Desktop Entry]
Name=%{name}
Comment=Mount Nintendo® contents
Exec=%{name} gui
Icon=%{name}
Terminal=false
Type=Application
Categories=Utility;
EOF

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

for res in 16 32 64 128 1024 ; do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 %{name}/gui/data/${res}x${res}.png ${dir}/%{name}.png
done


%files -f %{pyproject_files}
%license LICENSE.md
%doc README.md
%{_bindir}/%{name}*
%{_bindir}/mount_*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*


%changelog
* Sun Sep 05 2021 Phantom X <megaphantomx at hotmail dot com> - 2.0~a6-1.20210629gitdee583b
- 2.0-a6 snapshot
- Update to best packaging practices

* Sat May 08 2021 Phantom X <megaphantomx at hotmail dot com> - 2.0~a4-2.20210506gitc674c92
- Bump

* Mon Apr 19 2021 Phantom X <megaphantomx at hotmail dot com> - 2.0~a4-1.20210416git55058a6
- 2.0a4

* Wed Jan 20 2021 Phantom X <megaphantomx at hotmail dot com> - 2.0~a3-1.20210107git9d016f7
- Initial spec.
