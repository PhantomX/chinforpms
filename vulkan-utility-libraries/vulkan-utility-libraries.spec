%global debug_package %{nil}

%global with_sdk 0

Name:           vulkan-utility-libraries
Version:        1.4.339
Release:        100%{?dist}
Summary:        Vulkan utility libraries

License:        Apache-2.0
URL:            https://github.com/KhronosGroup/Vulkan-Utility-Libraries

%if 0%{?with_sdk}
Source0:        %{url}/archive/sdk-%{version}.tar.gz#/Vulkan-Utility-Libraries-sdk-%{version}.tar.gz
%else
Source0:        %{url}/archive/v%{version}.tar.gz#/Vulkan-Utility-Libraries-%{version}.tar.gz
%endif

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake3
BuildRequires:  ninja-build
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  cmake(VulkanHeaders) >= %{version}

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       vulkan-headers >= %{version}
Obsoletes:      vulkan-validation-layers-devel < 1.3.268.0-2
Provides:       vulkan-validation-layers-devel = %{version}-%{release}
Provides:       vulkan-validation-layers-devel%{?_isa} = %{version}-%{release}

%description    devel
%{summary}.


%prep
%if 0%{?with_sdk}
%autosetup -n Vulkan-Utility-Libraries-sdk-%{version} -p1
%else
%autosetup -n Vulkan-Utility-Libraries-%{version} -p1
%endif

%build
%cmake3 \
  -GNinja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
  -DBUILD_TESTS:BOOL=OFF \
  -DVUL_WERROR:BOOL=OFF \
  -DUPDATE_DEPS:BOOL=OFF \
%{nil}

%cmake3_build

%install
%cmake_install

%files devel
%license LICENSE.md
%doc README.md
%{_includedir}/vulkan/
%{_libdir}/cmake/VulkanUtilityLibraries/*.cmake
%{_libdir}/libVulkanLayerSettings.a
%{_libdir}/libVulkanSafeStruct.a


%changelog
* Mon Jan 19 2026 Phantom X <megaphantomx at hotmail dot com> - 1.4.339-100
- 1.4.339

* Fri Dec 19 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.337-100
- 1.4.337

* Fri Dec 12 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.336-100
- 1.4.336

* Tue Dec 02 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.335-100
- 1.4.335

* Fri Nov 14 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.333-100
- 1.4.333

* Sat Nov 08 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.332-100
- 1.4.332

* Fri Oct 31 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.331-100
- 1.4.331

* Sun Oct 26 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.330-100
- 1.4.330

* Fri Oct 10 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.329-100
- 1.4.329

* Fri Sep 26 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.328-100
- 1.4.328

* Mon Sep 22 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.327-100
- 1.4.327

* Tue Sep 02 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.326-100
- 1.4.326

* Fri Aug 15 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.325-100
- 1.4.325

* Sat Jul 26 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.323-100
- 1.4.323

* Wed Jul 16 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.322-100
- 1.4.322

* Wed Jul 09 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.321-100
- 1.4.321

* Wed Jun 25 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.319-100
- 1.4.319

* Sat Jun 14 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.318-100
- 1.4.318

* Sat Jun 07 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.317-100
- 1.4.317

* Thu May 15 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.315-100
- 1.4.315

* Fri May 02 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.313-100
- 1.4.313

* Fri Apr 04 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.312-100
- 1.4.312

* Sat Mar 22 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.311-100
- 1.4.311

* Tue Mar 11 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.310-100
- 1.4.310

* Tue Feb 25 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.309-100
- 1.4.309

* Fri Feb 07 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.307-100
- 1.4.307

* Fri Jan 24 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.306-100
- 1.4.306

* Fri Jan 17 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.305-100
- 1.4.305

* Fri Dec 20 2024 Phantom X <megaphantomx at hotmail dot com> - 1.4.304-100
- 1.4.304

* Tue Dec 03 2024 Phantom X <megaphantomx at hotmail dot com> - 1.4.303-100
- 1.4.303

* Thu Nov 21 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.302-100
- 1.3.302

* Tue Nov 05 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.301-100
- 1.3.301

* Sat Oct 26 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.300-100
- 1.3.300

* Wed Oct 09 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.297-100
- 1.3.297

* Thu Sep 26 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.296-100
- 1.3.296

* Mon Sep 02 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.295-100
- 1.3.295

* Sat Aug 24 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.294-100
- 1.3.294

* Sun Aug 18 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.293-100
- 1.3.293

* Mon Aug 05 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.292-100
- 1.3.292

* Mon Jul 22 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.291-100
- 1.3.290

* Sat Jun 29 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.289-100
- 1.3.289

* Sun Jun 09 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.287-100
- 1.3.287

* Tue May 14 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.285-100
- 1.3.285

* Wed May 08 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.284-100
- 1.3.284

* Sat Apr 20 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.283-100
- 1.3.283

* Tue Mar 26 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.281-100
- 1.3.281

* Fri Mar 08 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.280-100
- 1.3.280

* Tue Mar 05 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.279-100
- 1.3.279

* Sat Feb 17 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.278-100
- 1.3.278

* Fri Feb 09 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.277-100
- 1.3.277

* Thu Feb 01 2024 José Expósito <jexposit@redhat.com> - 1.3.268.0-5
- Add Provides and Obsoletes vulkan-validation-layers-devel

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.268.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Nov 17 2023 José Expósito <jexposit@redhat.com> - 1.3.268.0-3
- Avoid generating an empty non-devel package

* Fri Nov 17 2023 José Expósito <jexposit@redhat.com> - 1.3.268.0-2
- Generate non-devel package

* Thu Nov 16 2023 José Expósito <jexposit@redhat.com> - 1.3.268.0-1
- Initial import (fedora#2247640)
