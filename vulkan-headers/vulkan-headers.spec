%global __python %{__python3}
Name:           vulkan-headers
Version:        1.4.323
Release:        100%{?dist}
Summary:        Vulkan Header files and API registry

License:        Apache-2.0
URL:            https://github.com/KhronosGroup/Vulkan-Headers

%if 1%(echo %{version} | cut -d. -f4) != 1
%global with_sdk 1
%endif

%if 0%{?with_sdk}
Source0:        %{url}/archive/sdk-%{version}.tar.gz#/Vulkan-Headers-sdk-%{version}.tar.gz
%else
Source0:        %{url}/archive/v%{version}.tar.gz#/Vulkan-Headers-%{version}.tar.gz
%endif

BuildRequires:  cmake3
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildArch:      noarch

%description
Vulkan Header files and API registry

%prep
%if 0%{?with_sdk}
%autosetup -n Vulkan-Headers-sdk-%{version} -p1
%else
%autosetup -n Vulkan-Headers-%{version} -p1
%endif

%build
%cmake3 \
  -G Ninja \
  -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
%{nil}

%cmake3_build


%install
%cmake3_install


%files
%license LICENSE.md
%doc README.md
%{_includedir}/vk_video/
%{_includedir}/vulkan/
%dir %{_datadir}/vulkan/
%{_datadir}/cmake/VulkanHeaders/
%{_datadir}/vulkan/registry/


%changelog
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

* Fri Mar 21 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.311-100
- 1.4.311

* Tue Mar 11 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.310-100
- 1.4.310

* Tue Feb 25 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.309-100
- 1.4.309

* Fri Feb 07 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.307-100
- 1.4.307

* Fri Jan 24 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.306-100
- 1.4.306

* Fri Jan 24 2025 Phantom X <megaphantomx at hotmail dot com> - 1.4.305-101
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

* Fri Aug 30 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.295-100
- 1.3.295

* Fri Aug 23 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.294-100
- 1.3.294

* Sun Aug 18 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.293-100
- 1.3.293

* Mon Aug 05 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.292-100
- 1.3.292

* Fri Jul 19 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.291-100
- 1.3.291

* Sat Jun 29 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.289-100
- 1.3.289

* Sun Jun 09 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.287-100
- 1.3.287

* Sat Jun 01 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.286-100
- 1.3.286

* Fri May 10 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.285-100
- 1.3.285

* Tue May 07 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.284-100
- 1.3.284

* Fri Apr 19 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.283-100
- 1.3.283

* Tue Mar 26 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.281-100
- 1.3.281

* Fri Mar 08 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.280-100
- 1.3.280

* Sat Mar 02 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.279-100
- 1.3.279

* Fri Feb 16 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.278-100
- 1.3.278

* Thu Feb 01 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.277-100
- 1.3.277

* Fri Jan 26 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.276-100
- 1.3.276

* Thu Jan 11 2024 Phantom X <megaphantomx at hotmail dot com> - 1.3.275-100
- 1.3.275

* Tue Dec 19 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.274-100
- 1.3.274

* Sat Dec 09 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.273-100
- 1.3.273

* Sat Dec 02 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.272-100
- 1.3.272

* Sat Nov 11 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.270-102
- 1.3.270

* Sat Oct 28 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.269-100
- 1.3.269

* Sat Oct 14 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.268-100
- 1.3.268

* Fri Oct 06 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.267-100
- 1.3.267

* Fri Sep 15 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.264-101
- Add missing include file

* Sat Sep 09 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.264-100
- 1.3.264

* Mon Sep 04 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.263-100
- 1.3.263

* Fri Aug 25 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.262-100
- 1.3.262

* Fri Aug 04 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.261-100
- 1.3.261

* Fri Jul 28 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.260-100
- 1.3.260

* Fri Jul 21 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.258-100
- 1.3.258

* Thu Jul 13 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.257-100
- 1.3.257

* Fri Jun 30 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.256-100
- 1.3.256

* Mon Jun 26 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.255-100
- 1.3.255

* Fri Jun 16 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.254-100
- 1.3.254

* Sun May 28 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.251-100
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

* Thu Feb 16 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.241-100
- 1.3.241

* Thu Jan 26 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.240-100
- 1.3.240

* Thu Jan 19 2023 Phantom X <megaphantomx at hotmail dot com> - 1.3.239-100
- 1.3.239

* Mon Dec 19 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.238-100
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

* Thu Sep 22 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.229-100
- 1.3.229

* Fri Sep 16 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.228-100
- 1.3.228

* Thu Sep 08 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.227-100
- 1.3.227

* Thu Sep 01 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.226-100
- 1.3.226

* Thu Aug 18 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.225-100
- 1.3.225

* Thu Aug 04 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.224-100
- 1.3.224

* Sun Jul 24 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.222-100
- 1.3.222

* Fri Jul 15 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.221-100
- 1.3.221

* Sat Jul 02 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.219-100
- 1.3.129

* Fri Jun 17 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.218-100
- 1.3.218

* Thu Jun 09 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.217-100
- 1.3.217

* Tue May 24 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.215-100
- 1.3.215

* Tue May 17 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.214-100
- 1.3.214

* Tue May 10 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.213-100
- 1.3.213

* Wed Apr 27 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.212-100
- 1.3.212

* Tue Apr 05 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.211-100
- 1.3.211

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.210-100
- 1.3.210

* Wed Mar 16 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.208-100
- 1.3.208

* Tue Mar 08 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.207-100
- 1.3.207

* Tue Mar 01 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.206-100
- 1.3.206

* Tue Jan 25 2022 Phantom X <megaphantomx at hotmail dot com> - 1.3.204-100
- 1.3.204

* Mon Dec 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.203-100
- 1.2.203

* Fri Dec 10 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.202-100
- 1.2.202

* Sat Dec 04 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.201-100
- 1.2.201

* Tue Nov 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.200-1
- 1.2.200

* Tue Nov 16 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.199-1
- 1.2.199

* Tue Nov 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.197-1
- 1.2.197

* Sat Oct 16 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.196-2
- Add missing header

* Wed Oct 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.196-1
- 1.2.196

* Tue Oct 05 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.195-1
- 1.2.195

* Tue Sep 28 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.194-1
- 1.2.194

* Thu Sep 16 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.192-1
- 1.2.192

* Tue Sep 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.191-1
- 1.2.191

* Mon Aug 30 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.190-1
- 1.2.190

* Fri Aug 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.188-1
- 1.2.188

* Sun Aug 08 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.187-1
- 1.2.187

* Tue Jul 20 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.185-1
- 1.2.185

* Mon Jul 05 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.184-1
- 1.2.184

* Mon Jun 21 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.182-1
- 1.2.182

* Mon Jun 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.180-1
- 1.2.180

* Sun May 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.178-1
- 1.2.178

* Mon Apr 26 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.177-1
- 1.2.177

* Mon Apr 19 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.176-1
- 1.2.176

* Tue Apr 13 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.175-1
- 1.2.175

* Wed Apr 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.174-1
- 1.2.174

* Mon Mar 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.173-1
- 1.2.173

* Fri Mar 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.172-1
- 1.2.172

* Mon Mar 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.171-1
- 1.2.171

* Mon Feb 15 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.170-1
- 1.2.170

* Sun Feb 14 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.169-1
- 1.2.169

* Mon Jan 25 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.168-1
- 1.2.168

* Fri Jan 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.167-1
- 1.2.167

* Mon Jan 11 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.166-1
- 1.2.166

* Tue Dec 22 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.165-1
- 1.2.165

* Mon Dec 07 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.164-1
- 1.2.164

* Sat Dec  5 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.163-1
- 1.2.163

* Mon Nov 23 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.162-1
- 1.2.162

* Tue Nov 17 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.161-1
- 1.2.161

* Tue Nov 10 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.160-1
- 1.2.160

* Tue Nov  3 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.159-1
- 1.2.159

* Mon Oct 19 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.158-1
- 1.2.158

* Tue Oct 13 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.157-1
- 1.2.157

* Mon Oct  5 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.156-1
- 1.2.156

* Mon Sep 28 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.155-1
- 1.2.155

* Tue Sep 22 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.154-1
- 1.2.154

* Tue Sep 08 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.153-1
- 1.2.153

* Wed Sep 02 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.152-1
- 1.2.152

* Fri Aug 21 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.151-1
- 1.2.151

* Mon Aug 03 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.149-1
- 1.2.149

* Mon Jul 20 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.148-1
- 1.2.148

* Wed Jul 15 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.147-1
- 1.2.147

* Sat Jul 04 2020 Phantom X <megaphantomx at hotmail dot com> - 1.2.146-1
- 1.2.146

* Sun Jun 21 2020 Phantom X <megaphantomx at hotmail dot com>
- 1.2.145

* Wed Jun 10 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.2.143-1
- 1.2.143

* Mon May 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.2.141-1
- 1.2.141

* Wed May 06 2020 Phantom X <megaphantomx at bol dot com dot br> - 1.2.140-1
- Update to 1.2.140 headers

* Wed Apr 22 2020 Dave Airlie <airlied@redhat.com> - 1.2.135.0-1
- Update to 1.2.135.0 headers

* Wed Jan 29 2020 Dave Airlie <airlied@redhat.com> - 1.2.131.1-1
- Update to 1.2.131.1 headers

* Tue Nov 12 2019 Dave Airlie <airlied@redhat.com> - 1.1.126.0-1
- Update to 1.1.126.0 headers

* Mon Jul 29 2019 Dave Airlie <airlied@redhat.com> - 1.1.114.0-2
- Update to 1.1.114.0 headers

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.108.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 25 2019 Dave Airlie <airlied@redhat.com> - 1.1.108.0-1
- Update to 1.1.108.0 headers

* Thu Apr 18 2019 Dave Airlie <airlied@redhat.com> - 1.1.106.0-1
- Update to 1.1.106.0 headers

* Wed Mar 06 2019 Dave Airlie <airlied@redhat.com> - 1.1.101.0-1
- Update to 1.1.101.0 headers

* Wed Feb 13 2019 Dave Airlie <airlied@redhat.com> - 1.1.97.0-1
- Update to 1.1.97.0 headers

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.92.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 03 2018 Dave Airlie <airlied@redhat.com> - 1.1.92.0-1
- Update to 1.1.92.0

* Sat Oct 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.85.0-1
- Update to 1.1.85.0

* Tue Aug 07 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.82.0-1
- Update to 1.1.82.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.77.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 22 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.77.0-1
- Initial package
