%global commit 970fcde6c1e924a731754152e21ab0d3af635193
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20211031
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname LiveprogIDE

Name:           liveprogide
Version:        0
Release:        1%{?gver}%{?dist}
Summary:        Basic embeddable Liveprog IDE

License:        GPLv3
URL:            https://github.com/ThePBone/%{pkgname}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source1:         https://github.com/Audio4Linux/JDSP4Linux/raw/master/LICENSE

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qcodeeditor-devel
BuildRequires:  cmake(qtadvanceddocking)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Widgets)

Provides:       %{pkgname}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       eeleditor%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       EELEditor%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


%description
%{summary}.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cmake(qtadvanceddocking)
Requires:       qcodeeditor-devel
Provides:       %{pkgname}-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       eeleditor-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       EELEditor-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

rm -rf 3rdparty QCodeEditor

find \
  -type f \( -name "*.cpp" -o -name "*.h" -o -name "*.hpp" -o -name "*.pri" -o -name "*.qrc" -o -name "*.ui" \) -exec chmod -x {} ';'

cp -p %{S:1} .

sed -e '/docking-system/d' -i EELEditor.pro

sed \
  -e '/staticlib/s|^|#|g' \
  -e '/TEMPLATE = lib/a\    unix: target.path = %{_libdir}' \
  -e '/TEMPLATE = lib/a\    !isEmpty(target.path): INSTALLS += target' \
  -i src/src.pro

sed -e '/QCodeEditor.pri/d' -i src/EELEditor.pri

cat > src/EELEditor-Linker.pri <<EOF
LIBS += -lqtadvanceddocking -lQCodeEditor
INCLUDEPATH += %{_includedir}/qtadvanceddocking %{_includedir}/QCodeEditor
EOF


%build
%qmake_qt5 EELEditor.pro
%make_build


%install
%make_install INSTALL_ROOT=%{buildroot}

mkdir -p %{buildroot}%{_includedir}/%{name}
pushd src
find -iname '*.h' | xargs -I {} install -m0644 -D {} %{buildroot}%{_includedir}/%{pkgname}/{}
popd


%files
%license LICENSE
%doc README.md
%{_libdir}/*.so.*


%files devel
%license LICENSE
%{_includedir}/%{pkgname}
%{_libdir}/*.so


%changelog
* Mon Dec 13 2021 Phantom X <megaphantomx at hotmail dot com> - 0-1.20211031git970fcde
- Initial spec
