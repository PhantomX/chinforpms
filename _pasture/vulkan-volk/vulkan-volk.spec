%global debug_package %{nil}

%global commit 02ffc36f3c7f8a744e741127eda7ccbdb5c622e6
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250509
%bcond_without snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global pkgname volk

Name:           vulkan-%{pkgname}
Version:        1.4.315
Release:        100%{?dist}
Summary:        Meta loader for Vulkan API 

License:        MIT
URL:            https://github.com/zeux/%{pkgname}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif

Patch10:        0001-cmake-change-namespace-to-vulkan_volk.patch
Patch11:        0001-library-set-PIC.patch

BuildRequires:  cmake3
BuildRequires:  gcc
BuildRequires:  ninja-build
BuildRequires:  cmake(VulkanHeaders) >= %{version}


%description
volk is a meta-loader for Vulkan. It allows you to dynamically load entrypoints
required to use Vulkan without linking to vulkan-1.dll or statically linking
Vulkan loader. Additionally, volk simplifies the use of Vulkan extensions by
automatically loading all associated entrypoints. Finally, volk enables loading
Vulkan entrypoints directly from the driver which can increase performance
by skipping loader dispatch overhead.


%package        devel
Summary:        Development files for %{name}
Provides:       %{name}-static = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{pkgname}-volk-static = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{pkgname}-volk-devel < %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1


%build
%cmake3 \
  -G Ninja \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DVOLK_INSTALL:BOOL=ON \
%{nil}

%cmake3_build


%install
%cmake3_install

%files devel
%license LICENSE.md
%{_libdir}/lib*.a
%{_includedir}/vulkan/volk/
%{_libdir}/cmake/vulkan_volk/


%changelog
* Thu May 15 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.315-100.20250509git02ffc36
- 1.4.315

* Fri May 02 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.313-100.20250418git43c29e6
- 1.4.313

* Fri Apr 04 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.312-100.20250404gitc85253a
- 1.4.312

* Sat Mar 22 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.311-100.20250321gite3e9ea8
- 1.4.311

* Tue Mar 11 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.310-100.20250307git225628c
- 1.4.310

* Tue Feb 25 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.309-100.20250221git58689c0
- 1.4.309

* Sat Feb 08 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.307-100.20250130git362e53e
- 1.4.307

* Fri Jan 24 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.306-100.20250124git23d3ab9
- 1.4.306

* Fri Jan 17 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.305-100.20250117gitce3b8ca
- 1.4.305

* Fri Dec 20 2024 Phantom X <megaphantomx at hotmail dot com> - 1.4.304-100.20241220git0b17a76
- 1.4.304

* Tue Dec 03 2024 Phantom X <megaphantomx at hotmail dot com> - 1.4.303-100.20241202gite767d0e
- 1.4.303

* Thu Nov 21 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.302-100.20241121git8f63285
- 1.3.302

* Tue Nov 05 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.301-100.20241102git2b0df05
- 1.3.301

* Sat Oct 26 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.300-100.20241025gitbb523d7
- 1.3.300

* Wed Oct 09 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.297-100.20241007gite816744
- 1.3.297

* Thu Sep 26 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.296-100.20240926git59d2690
- 1.3.296

* Mon Sep 02 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.295-100.20240830git6368f2c
- 1.3.295

* Sat Aug 24 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.294-100.20240823gitd2d0cdd
- 1.3.294

* Sun Aug 18 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.293-100.20240816git8783587
- 1.3.293

* Mon Aug 05 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.292-100.20240727git8a73954
- 1.3.292

* Fri Jul 19 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.291-100.20240719git12e006f
- 1.3.291

* Sat Jun 29 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.289-100.20240628git692bef4
- 1.3.289

* Sun Jun 09 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.287-100.20240607git955e5e4
- 1.3.287

* Sat Jun 01 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.286-100.20240531git16c2936
- 1.3.286

* Tue May 14 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.285-100.20240510git749f0ab
- 1.3.285

* Wed May 08 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.284-100.20240506git3ca2bd9
- 1.3.284

* Fri Apr 19 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.283-1.20240419git3a8068a
- 1.3.283
- volk-vulkan -> vulkan-volk

* Tue Mar 26 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.281-1.20240325gita2ca537
- 1.3.281

* Fri Mar 08 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.280-1.20240308git01986ac
- 1.3.280

* Sat Mar 02 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.279-1.20240301gitea44c79
- 1.3.279

* Fri Jan 26 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.276-1.20240125git3ee06ec
- 1.3.276

* Tue Dec 19 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.274-1.20231219gitdbfeadc
- 1.3.274

* Sat Dec 09 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.273-1.20231208gitad36e8b
- 1.3.273

* Sat Dec 02 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.272-1.20231201git630309f
- Initial spec
