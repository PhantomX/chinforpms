%global build_plugins rsp-z64 video-arachnoid video-glide64 video-z64

%global origname mupen64plus

Name:           mupen64plus-extraplugins
Version:        2.0.0
Release:        1%{?dist}
Summary:        Mupen64Plus additional plugins

License:        GPLv2
URL:            http://www.mupen64plus.org/
Source0:        http://www.mupen64plus.org/old-releases/%{name}-src-2.0.0.tar.gz

BuildRequires:  mupen64plus-devel
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(sdl)
Requires:       mupen64plus

%description
%{summary}.

%prep
%autosetup -c

for plugin in %{build_plugins} ;do
  [ -f %{origname}-${plugin}/COPYING ] && cp %{origname}-${plugin}/COPYING COPYING.${plugin}
  [ -f %{origname}-${plugin}/README ] && cp %{origname}-${plugin}/README README.${plugin}
done

sed -e 's|<glew.h>|<GL/glew.h>|g' \
  -i %{origname}-video-z64/src/{rgl.h,glshader.cpp}

# Borrowed from AUR
sed \
  -e 's|min[[:blank:]]*(|glide_min(|g' \
  -e 's|max[[:blank:]]*(|glide_max(|g' \
  -i %{origname}-video-glide64/src/*.{cpp,h}

%build
export OPTFLAGS="%{optflags}"
export LDFLAGS="%{__global_ldflags}"
export V=1
export LDCONFIG=/bin/true
export PREFIX=/usr
export LIBDIR=%{_libdir}
export INCDIR=%{_includedir}/%{origname}
export SHAREDIR=%{_datadir}/%{origname}
export MANDIR=%{_mandir}

for plugin in %{build_plugins} ;do
  ( cd %{origname}-${plugin}/projects/unix
    %make_build all INSTALL_STRIP_FLAG=
  )
done


%install
rm -rf %{buildroot}

export OPTFLAGS="%{optflags}"
export LDFLAGS="%{__global_ldflags}"
export LDCONFIG=/bin/true
export PREFIX=/usr
export LIBDIR=%{_libdir}
export INCDIR=%{_includedir}/%{origname}
export SHAREDIR=%{_datadir}/%{origname}
export MANDIR=%{_mandir}

for plugin in %{build_plugins} ;do
  ( cd %{origname}-${plugin}/projects/unix
    %make_install INSTALL="install -p" INSTALL_STRIP_FLAG=
  )
done
chmod +x %{buildroot}%{_libdir}/%{origname}/%{origname}-*.so

%files
%license COPYING.*
%doc README.*
%{_libdir}/%{origname}/%{origname}-*.so
%{_datadir}/%{origname}/*.ini


%changelog
* Thu Jan  5 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.0.0-1
- Initial spec.
