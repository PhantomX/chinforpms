Name:           waterfox-filesystem
Version:        1.0
Release:        1%{?dist}
Summary:        Waterfox filesytem layout
License:        MPLv1.1

Requires:       mozilla-filesystem

%description
This package provides some directories required by packages which use
Waterfox technologies such as NPAPI plugins or toolkit extensions.

%prep

%build

%install
mkdir -p %{buildroot}%{_libdir}/waterfox/extensions
mkdir -p %{buildroot}%{_datadir}/waterfox/extensions
mkdir -p %{buildroot}%{_sysconfdir}/skel/.waterfox/{plugins,extensions}

ln -sf ../mozilla/plugins %{buildroot}%{_libdir}/waterfox/plugins
%ifarch x86_64
  mkdir -p %{buildroot}/usr/lib/waterfox/extensions
  # This still can be used for the time
  ln -s ../mozilla/plugins %{buildroot}/usr/lib/waterfox/plugins
%endif

%preun
# is it a final removal?
if [ $1 -eq 0 ]; then
  rm -rf %{_libdir}/waterfox/extensions
  rm -rf %{_libdir}/waterfox/plugins
fi

%files
/usr/lib*/waterfox/extensions
%{_libdir}/waterfox/plugins
%ifarch x86_64
/usr/lib/waterfox/plugins
%endif
%{_datadir}/waterfox
%{_sysconfdir}/skel/.waterfox

%changelog
* Wed Dec 27 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0-1
- Initial spec
