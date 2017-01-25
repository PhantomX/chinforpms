%global gkplugindir %{_libdir}/gkrellm2/plugins
%global pkgname     gkrellm2-cpupower

Name:           gkrellm-cpupower
Version:        0.1.6
Release:        1%{?dist}
Summary:        Gkrellm plugin for manipulating CPU frequency

License:        GPLv2
URL:            https://github.com/sainsaar/gkrellm2-cpupower
Source0:        https://github.com/sainsaar/gkrellm2-cpupower/tarball/%{version}#/%{pkgname}-%{version}.tar.gz

Patch0:         %{pkgname}-0.1.6-cpupower.patch
Requires:       gkrellm >= 2.2.0
BuildRequires:  gkrellm-devel >= 2.2.0

%description
A Gkrellm2 plugin for displaying and manipulating CPU frequency.

%prep
%setup -a 0 -c
%{__mv} */* .

%patch0

sed -i \
  -e "s|-O2 -Wall|%{optflags}|g" \
  -e '/^LFLAGS =/s|-shared|\0 %{__global_ldflags} -Wl,--as-needed|g' \
  Makefile

%build
%make_build

%install
rm -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{gkplugindir}
%{__install} -pm0755 cpupower.so \
  %{buildroot}%{gkplugindir}/

%{__mkdir_p} %{buildroot}%{_sbindir}
install -pm0755 cpufreqnextgovernor %{buildroot}%{_sbindir}/


%files
%license LICENSE
%doc ChangeLog README
%{_sbindir}/cpufreqnextgovernor
%{gkplugindir}/cpupower.so

%changelog
* Fri Dec  2 2016 Phantom X - 0.1.6-1
- First spec.
