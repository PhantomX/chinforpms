%global with_sdk 0

Name:           vulkan-loader
Version:        1.3.274
Release:        100%{?dist}
Summary:        Vulkan ICD desktop loader

License:        Apache-2.0
URL:            https://github.com/KhronosGroup/Vulkan-Loader

%if 1%(echo %{version} | cut -d. -f4) != 1
%global with_sdk 1
%endif

%if 0%{?with_sdk}
Source0:        %{url}/archive/sdk-%{version}.tar.gz#/Vulkan-Loader-sdk-%{version}.tar.gz
%else
Source0:        %{url}/archive/v%{version}.tar.gz#/Vulkan-Loader-%{version}.tar.gz
%endif

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake3
BuildRequires:  ninja-build
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  cmake(VulkanHeaders) >= %{version}
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xrandr)

Provides:       vulkan%{?_isa} = %{version}-%{release}
Provides:       vulkan = %{version}-%{release}
Obsoletes:      vulkan < %{version}-%{release}
Provides:       vulkan-filesystem = %{version}-%{release}
Obsoletes:      vulkan-filesystem < %{version}-%{release}

Requires:       mesa-vulkan-drivers%{?_isa}


%description
This project provides the Khronos official Vulkan ICD desktop 
loader for Windows, Linux, and MacOS.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       vulkan-headers
Provides:       vulkan-devel%{?_isa} = %{version}-%{release}
Provides:       vulkan-devel = %{version}-%{release}
Obsoletes:      vulkan-devel < %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%if 0%{?with_sdk}
%autosetup -p1 -n Vulkan-Loader-sdk-%{version}
%else
%autosetup -p1 -n Vulkan-Loader-%{version}
%endif

%build
%cmake3 \
  -GNinja \
  -DCMAKE_BUILD_TYPE=Release \
%{nil}

%cmake3_build


%install
%cmake3_install

# create the filesystem
mkdir -p %{buildroot}%{_sysconfdir}/vulkan/{explicit,implicit}_layer.d/ \
%{buildroot}%{_datadir}/vulkan/{explicit,implicit}_layer.d/ \
%{buildroot}{%{_sysconfdir},%{_datadir}}/vulkan/icd.d


%files
%license LICENSE.txt
%doc README.md CONTRIBUTING.md
%dir %{_sysconfdir}/vulkan/
%dir %{_sysconfdir}/vulkan/explicit_layer.d/
%dir %{_sysconfdir}/vulkan/icd.d/
%dir %{_sysconfdir}/vulkan/implicit_layer.d/
%dir %{_datadir}/vulkan/
%dir %{_datadir}/vulkan/explicit_layer.d/
%dir %{_datadir}/vulkan/icd.d/
%dir %{_datadir}/vulkan/implicit_layer.d/
%{_libdir}/*.so.*

%files devel
%{_libdir}/cmake/VulkanLoader/
%{_libdir}/pkgconfig/vulkan.pc
%{_libdir}/*.so


%changelog
* Tue Dec 19 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.274-100
- 1.3.274

* Sat Dec 09 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.273-100
- 1.3.273

* Sat Dec 02 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.272-100
- 1.3.272

* Sat Nov 11 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.270-100
- 1.3.270

* Sat Oct 28 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.269-100
- 1.3.269

* Sat Oct 14 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.268-100
- 1.3.268

* Fri Oct 06 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.267-100
- 1.3.267

* Fri Sep 15 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.264-100
- 1.3.264

* Tue Sep 05 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.263-100
- 1.3.263

* Fri Aug 25 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.262-100
- 1.3.262

* Sat Aug 05 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.261-100
- 1.3.261

* Fri Jul 28 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.259-100
- 1.3.259

* Fri Jul 21 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.258-100
- 1.3.258

* Thu Jul 13 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.257-100
- 1.3.257

* Sat Jul 01 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.256-100
- 1.3.256

* Mon Jun 26 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.255-100
- 1.3.255

* Fri Jun 16 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.254-100
- 1.3.254

* Thu Jun 01 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.251-100
- 1.3.251

* Thu May 04 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.250-100
- 1.3.250

* Thu Apr 27 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.249-100
- 1.3.249

* Tue Apr 25 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.248-100
- 1.3.248

* Sat Apr 15 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.247-100
- 1.3.247

* Fri Mar 31 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.246-100
- 1.3.246

* Sun Mar 26 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.245-100
- 1.3.245

* Mon Feb 27 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.242-100
- 1.3.242

* Sat Jan 28 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.240-100
- 1.3.240

* Fri Jan 20 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.239-100
- 1.3.239

* Tue Dec 20 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.238-100
- 1.3.238

* Thu Dec 08 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.237-100
- 1.3.237

* Tue Dec 06 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.236-100
- 1.3.236

* Thu Nov 17 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.235-100
- 1.3.235

* Mon Nov 14 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.234-100
- 1.3.234

* Thu Nov 03 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.233-100
- 1.3.233

* Fri Oct 14 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.231-100
- 1.3.231

* Thu Sep 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.230-100
- 1.3.230

* Thu Sep 22 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.229-1
- 1.3.229

* Fri Sep 16 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.228-1
- 1.3.228

* Thu Sep 08 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.227-1
- 1.3.227

* Thu Sep 01 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.226-1
- 1.3.226

* Thu Aug 18 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.225-1
- 1.3.225

* Fri Aug 05 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.224-100
- 1.3.224

* Sun Jul 24 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.222-100
- 1.3.222

* Fri Jul 15 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.221-100
- 1.3.221

* Sat Jul 02 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.219-100
- 1.3.219

* Fri Jun 17 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.218-100
- 1.3.218

* Sat Jun 11 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.216-100
- 1.3.216

* Tue May 24 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.215-100
- 1.3.215

* Tue May 17 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.214-100
- 1.3.214

* Wed May 11 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.213-100
- 1.3.213

* Wed Apr 27 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.212-100
- 1.3.212

* Tue Apr 05 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.211-100
- 1.3.211

* Sat Apr 02 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.210-100
- 1.3.210

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.209-100
- 1.3.209

* Wed Mar 16 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.208-100
- 1.3.208

* Tue Mar 08 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.207-100
- 1.3.207

* Tue Mar 01 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.206-100
- 1.3.206

* Wed Jan 26 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.204-100
- 1.3.204

* Mon Dec 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.203-100
- 1.2.203

* Fri Dec 10 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.202-100
- 1.2.202

* Sat Dec 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.201-100
- 1.2.201

* Wed Nov 17 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.199-2
- Remove reverts

* Tue Nov 16 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.199-1
- 1.2.199

* Thu Nov 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.197-1
- 1.2.197

* Sat Oct 16 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.196-1
- 1.2.196

* Tue Oct 05 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.195-1
- 1.2.195

* Tue Sep 28 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.194-1
- 1.2.194

* Thu Sep 16 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.192-1
- 1.2.192

* Thu Sep 09 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.191-1
- 1.2.191

* Mon Aug 30 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.190-1
- 1.2.190

* Fri Aug 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.188-1
- 1.2.188

* Sun Aug 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.187-1
- 1.2.187

* Wed Jul 21 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.185-1
- 1.2.185

* Sun Jul 18 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.184-1
- 1.8.184

* Tue Jul 06 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.183-1
- 1.2.183

* Tue Jun 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.182-1
- 1.2.182

* Tue Jun 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.180-1
- 1.2.180

* Sun May 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.178-1
- 1.2.178

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.176-1
- 1.2.176

* Wed Apr 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.174-1
- 1.2.174

* Thu Mar 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.173-1
- 1.2.173

* Fri Mar 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.172-1
- 1.2.172

* Mon Mar 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.170-1
- 1.2.170

* Sun Feb 14 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.169-1
- 1.2.169

* Mon Jan 11 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.166-1
- 1.2.166

* Tue Dec 01 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.162-2
- Remove @LIB_SUFFIX@ from library

* Thu Nov 26 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.162-1
- 1.2.162

* Thu Nov 26 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.161-2
- 1.2.162

* Sat Nov 21 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.161-1
- 1.2.161

* Tue Nov 17 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.160-1
- 1.2.160

* Tue Nov 10 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.159-1
- 1.2.159

* Tue Nov  3 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.158-1
- 1.2.158

* Tue Oct 20 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.157-1
- 1.2.157

* Tue Sep 22 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.154-1
- 1.2.154

* Sun Sep 20 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.153-2
- Upstream fixes

* Tue Sep 08 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.153-1
- 1.2.153

* Fri Aug 21 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.151-1
- 1.2.151

* Wed Jul 22 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.148-1
- 1.2.148

* Wed Jul 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.147-1
- 1.2.147

* Thu Jul 09 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.146-1
- 1.2.146

* Wed Jul 01 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.145-1
- 1.2.145

* Sun May 31 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.2.141-1
- 1.2.141

* Wed May 06 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.2.140-1
- Update to 1.2.140

* Wed Apr 22 2020 Dave Airlie <airlied@redhat.com> - 1.2.135.0-1
- Update to 1.2.135.0

* Wed Jan 29 2020 Dave Airlie <airlied@redhat.com> - 1.2.131.1-1
- Update to 1.2.131.1

* Tue Nov 12 2019 Dave Airlie <airlied@redhat.com> - 1.1.126.0-1
- Update to 1.1.126.0

* Wed Jul 31 2019 Dave Airlie <airlied@redhat.com> - 1.1.114.0-1
- Update to 1.1.114.0

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.108.0-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 25 2019 Dave Airlie <airlied@redhat.com> - 1.1.108.0-0
- Update to 1.1.108.0

* Wed Mar 06 2019 Dave Airlie <airlied@redhat.com> - 1.1.101.0-0
- Update to 1.1.101.0

* Wed Feb 13 2019 Dave Airlie <airlied@redhat.com> - 1.1.97.0-0
- Update to 1.1.97.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.92.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 03 2018 Dave Airlie <airlied@redhat.com> - 1.1.92.0-1
- Update to 1.1.92.0

* Mon Nov 19 2018 Dave Airlie <airlied@redhat.com> - 1.1.85.0-1
- Update to 1.1.85.0

* Tue Aug 07 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.82.0-1
- Update to 1.1.82.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.77.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.77.0-4
- Fix update path

* Tue Jun 26 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.77.0-3
- Add conditional for mesa-vulkan-drivers requires

* Tue Jun 26 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.77.0-2
- Improve description and summary
- Set release

* Sat Jun 23 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.77.0-1
- Initial package
