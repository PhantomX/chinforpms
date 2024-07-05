%global commit 842c15192041f8e71c512851834f4dadb1a554fb
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240704

%global dist .%{date}git%{shortcommit}%{?dist}

Name:           discord-rpc
Version:        3.4.0
Release:        1%{?dist}
Summary:        Discord Rich Presence library

License:        MIT
URL:            https://github.com/stenzek/%{name}

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

Patch0:         0001-cmake-shared-fixes.patch
Patch1:         0001-cmake-use-system-libraries.patch

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake(RapidJSON) >= 1.1


%description
%{name} is a library for interfacing your game with a locally running Discord
desktop client.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{commit} -p1

rm -rf thirdparty/

sed \
  -e 's|INCLUDES|PUBLIC_HEADER|' \
  -e '/DESTINATION/s|include|\0/%{name}|' -i src/CMakeLists.txt

%build
%cmake \
  -DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir}/%{name} \
%{nil}

%cmake_build

%install
%cmake_install


%files
%license LICENSE
%doc README.md
%{_libdir}/lib%{name}.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/DiscordRPC


%changelog
* Thu Jul 04 2024 Phantom X <megaphantomx at hotmail dot com> - 3.4.0-1.20240704git842c151
- Initial spec
