%global perms_cdda2wav %caps(cap_dac_override,cap_sys_admin,cap_sys_nice,cap_net_bind_service,cap_sys_rawio+ep)
%global perms_cdrecord %caps(cap_sys_resource,cap_dac_override,cap_sys_admin,cap_sys_nice,cap_net_bind_service,cap_ipc_lock,cap_sys_rawio+ep)
%global perms_readcd %caps(cap_dac_override,cap_sys_admin,cap_net_bind_service,cap_sys_rawio+ep)

# Build can fail if more than one job
%global _smp_build_ncpus 1

%global ver %%(echo %{version} | tr -d '~')
%global mver %%(echo %{version} | cut -d'~' -f1)

Name:           cdrtools
Version:        3.02~a09
Release:        2%{?dist}
Epoch:          11
Summary:        CD/DVD/BluRay command line recording software

License:        CDDL and GPLv2 and BSD
URL:            http://cdrtools.sourceforge.net/private/cdrecord.html

%if 0%(echo %{version} | grep -q '~a' ; echo $?) == 0
%global alpha_url /alpha
%endif
Source0:        http://downloads.sourceforge.net/%{name}%{?alpha_url}/%{name}-%{ver}.tar.bz2
Patch0:         %{name}-3.02-cdrecord-default.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gettext-devel
BuildRequires:  libcap-devel

%description
A set of command line programs that allows to record CD/DVD/BluRay media.

%package -n cdrecord
Summary:        Creates an image of an ISO9660 file system
Requires:       %{name}-libs%{?_isa} = %{?epoch}:%{version}-%{release}
Obsoletes:      wodim < %{epoch}:
Provides:       wodim = %{epoch}:

%description -n cdrecord
A set of command line programs that allows to record and read CD/DVD/BluRay
media.

%package -n mkisofs
Summary:        Creates an image of an ISO9660 file system
Requires:       %{name}-libs%{?_isa} = %{?epoch}:%{version}-%{release}
Obsoletes:      genisoimage < %{epoch}:
Provides:       genisoimage = %{epoch}:

%description -n mkisofs
Programs to create and manipulate hybrid ISO9660/JOLIET/HFS file systems with
Rock Ridge attributes.

%package -n cdda2wav
Summary:        A CD-Audio Grabbing tool
Requires:       %{name}-libs%{?_isa} = %{?epoch}:%{version}-%{release}
Obsoletes:      icedax < %{epoch}: 
Provides:       icedax = %{epoch}:

%description -n cdda2wav
The most evolved CD-audio extraction program with paranoia support.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{?epoch}:%{version}-%{release}

%description devel
This package provides the development files of the %{name} package.

%package libs
Summary:        Libraries for %{name}
Requires(post): ldconfig

%description libs
This package provides the shared libraries for %{name}.

%prep
%autosetup -n %{name}-%{mver} -p0
rm -fr btcflash

# Convert files to utf8 for german letters
for i in \
    $(find . -name "*.c") \
    $(find . -name "*.1") \
    $(find . -name "*.3") \
    $(find . -name "*.8") \
    $(find . -name "README*") \
    $(find . -name "THANKS*"); do
    iconv -f iso-8859-1 $i -t utf-8 -o $i.new && mv -f $i.new $i
done

%build
%set_build_flags
%make_build GMAKE_NOWARN=true LINKMODE="dynamic" RUNPATH= \
    CPPOPTX="$CXXFLAGS" COPTX="$CFLAGS -DTRY_EXT2_FS" \
    LDOPTX="$LDFLAGS"

%install
make GMAKE_NOWARN=true LINKMODE="dynamic" RUNPATH= \
    INS_BASE=%{_prefix} INS_RBASE=/ DESTDIR=%{buildroot} \
    install

# Remove unused libraries
rm -fr %{buildroot}%{_prefix}/lib/profiled
rm -f %{buildroot}%{_prefix}/lib/lib*.a
# Remove makefiles and makerules manpages
rm -fr %{buildroot}%{_mandir}/man5
# Install documents directly from the files section
rm -fr %{buildroot}%{_docdir}

# Move libraries to the appropriate place on 64 bit arches
if [ %{_libdir} != %{_prefix}/lib ]; then 
    mkdir -p %{buildroot}%{_libdir}
    mv %{buildroot}%{_prefix}/lib/lib*.so* %{buildroot}%{_libdir}
fi

chmod 755 %{buildroot}%{_libdir}/lib*.so* \
    %{buildroot}%{_bindir}/* %{buildroot}%{_sbindir}/*

# Renaming for alternatives
for i in cdrecord readcd cdda2wav ;do
  mv %{buildroot}%{_bindir}/$i %{buildroot}%{_bindir}/%{name}-$i
  ln -sf %{name}-$i %{buildroot}%{_bindir}/$i
  mv %{buildroot}%{_mandir}/man1/$i.1 %{buildroot}%{_mandir}/man1/%{name}-$i.1
  ln -sf %{name}-$i.1 %{buildroot}%{_mandir}/man1/$i.1
done

rm -f %{buildroot}%{_bindir}/dvdrecord
ln -sf %{name}-cdrecord %{buildroot}%{_bindir}/%{name}-dvdrecord
ln -sf %{name}-cdrecord %{buildroot}%{_bindir}/dvdrecord
ln -sf %{name}-cdrecord.1 %{buildroot}%{_mandir}/man1/%{name}-dvdrecord.1

mv %{buildroot}%{_bindir}/mkisofs %{buildroot}%{_bindir}/%{name}-mkisofs
ln -sf %{name}-mkisofs %{buildroot}%{_bindir}/mkisofs

rm -f %{buildroot}%{_bindir}/mkhybrid
ln -sf %{name}-mkisofs %{buildroot}%{_bindir}/%{name}-mkhybrid
ln -sf %{name}-mkisofs %{buildroot}%{_bindir}/mkhybrid


%post -n cdrecord
for i in cdrecord readcd cdda2wav ;do
  link=`readlink %{_bindir}/$i`
  if [ "$link" == "%{_bindir}/%{name}-$i" ]; then
    rm -f %{_bindir}/$i
  fi
  link=`readlink %{_mandir}/man1/$i.1.gz`
  if [ "$link" == "%{name}-$i.1.gz" ]; then
    rm -f %{_mandir}/man1/%{name}-$i.1.gz
  fi
done
link=`readlink %{_bindir}/dvdrecord`
if [ "$link" == "%{name}-cdrecord" ]; then
  rm -f %{_bindir}/dvdrecord
fi
link=`readlink %{_mandir}/man1/dvdrecord.1.gz`
if [ "$link" == "%{name}-cdrecord.1.gz" ]; then
  rm -f %{_mandir}/man1/%{name}-dvdrecord.1.gz
fi

%{_sbindir}/alternatives --install %{_bindir}/cdrecord cdrecord \
          %{_bindir}/%{name}-cdrecord 50 \
  --slave %{_mandir}/man1/cdrecord.1.gz cdrecord-cdrecordman \
          %{_mandir}/man1/%{name}-cdrecord.1.gz \
  --slave %{_bindir}/dvdrecord cdrecord-dvdrecord \
          %{_bindir}/%{name}-cdrecord \
  --slave %{_mandir}/man1/dvdrecord.1.gz cdrecord-dvdrecordman \
          %{_mandir}/man1/%{name}-cdrecord.1.gz \
  --slave %{_bindir}/readcd cdrecord-readcd \
          %{_bindir}/%{name}-readcd \
  --slave %{_mandir}/man1/readcd.1.gz cdrecord-readcdman \
          %{_mandir}/man1/%{name}-readcd.1.gz

%preun -n cdrecord
if [ $1 = 0 ]; then
  %{_sbindir}/alternatives --remove cdrecord %{_bindir}/%{name}-cdrecord
fi


%post -n mkisofs
link=`readlink %{_bindir}/mkisofs`
if [ "$link" == "%{name}-cdrecord" ]; then
  rm -f %{_bindir}/mkisofs
fi

%{_sbindir}/alternatives --install %{_bindir}/mkisofs mkisofs \
  %{_bindir}/%{name}-mkisofs 50 \
  --slave %{_bindir}/mkhybrid mkisofs-mkhybrid \
          %{_bindir}/%{name}-mkisofs

%preun -n mkisofs
if [ $1 = 0 ]; then
  %{_sbindir}/alternatives --remove mkisofs %{_bindir}/genisoimage
fi


%post -n cdda2wav
link=`readlink %{_bindir}/cdda2wav`
if [ "$link" == "%{name}-cdda2wav" ]; then
  rm -f %{_bindir}/%{name}-cdda2wav
fi
link=`readlink %{_mandir}/man1/cdda2wav.1.gz`
if [ "$link" == "%{name}-cdda2wav.1.gz" ]; then
  rm -f %{_mandir}/man1/%{name}-cdda2wav.1.gz
fi

%{_sbindir}/alternatives --install %{_bindir}/cdda2wav cdda2wav \
%{_bindir}/%{name}-cdda2wav 50 \
  --slave %{_mandir}/man1/cdda2wav.1.gz cdda2wav-cdda2wavman \
          %{_mandir}/man1/%{name}-cdda2wav.1.gz 

%preun -n cdda2wav
if [ $1 = 0 ]; then
  %{_sbindir}/alternatives --remove cdda2wav %{_bindir}/%{name}-cdda2wav
fi


%files -n cdrecord
%doc cdrecord/README*
%config(noreplace) /etc/default/cdrecord
%config(noreplace) /etc/default/rscsi
%ghost %{_bindir}/cdrecord
%ghost %{_bindir}/dvdrecord
%ghost %{_bindir}/readcd
%{perms_cdrecord} %{_bindir}/%{name}-cdrecord
%{_bindir}/%{name}-dvdrecord
%{_bindir}/scgcheck
%{_bindir}/scgskeleton
%{perms_readcd} %{_bindir}/%{name}-readcd
%{_sbindir}/rscsi
%{_mandir}/man1/%{name}-cdrecord.*
%{_mandir}/man1/%{name}-dvdrecord.*
%{_mandir}/man1/%{name}-readcd.*
%ghost %{_mandir}/man1/cdrecord.*
%ghost %{_mandir}/man1/dvdrecord.*
%ghost %{_mandir}/man1/readcd.*
%{_mandir}/man1/scgcheck.*
%{_mandir}/man1/rscsi.*
%{_mandir}/man1/scgskeleton.*

%files -n mkisofs
%license mkisofs/COPYING
%doc mkisofs/RELEASE mkisofs/TODO mkisofs/README*
%ghost %{_bindir}/mkisofs
%ghost %{_bindir}/mkhybrid
%{_bindir}/%{name}-mkisofs
%{_bindir}/%{name}-mkhybrid
%{_bindir}/isoinfo
%{_bindir}/devdump
%{_bindir}/isodump
%{_bindir}/isovfy
%{_bindir}/isodebug
%{_mandir}/man8/*
%{_prefix}/lib/siconv/*

%files -n cdda2wav
%doc cdda2wav/FAQ cdda2wav/HOWTOUSE cdda2wav/NEEDED cdda2wav/TODO cdda2wav/THANKS cdda2wav/README
%{_bindir}/cdda2mp3
%{_bindir}/cdda2ogg
%ghost %{_bindir}/cdda2wav
%{perms_cdda2wav} %{_bindir}/%{name}-cdda2wav
%{_mandir}/man1/%{name}-cdda2wav.*
%ghost %{_mandir}/man1/cdda2wav.*
%{_mandir}/man1/cdda2mp3.*
%{_mandir}/man1/cdda2ogg.*

%files libs
%license COPYING GPL-2.0.txt LGPL-2.1.txt CDDL.Schily.txt
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/*
%{_libdir}/lib*.so
%{_mandir}/man3/*


%changelog
* Thu Mar 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 11:3.02~a09-2
- Fix build

* Fri Nov 30 2018 Phantom X <megaphantomx at bol dot com dot br> - 11:3.02~a09-1
- chinforpms with altenatives support

* Wed Feb 14 2018 Simone Caronni <negativo17@gmail.com> - 10:3.02-a09.1
- Update to 3.02a09.

* Mon Feb 27 2017 Simone Caronni <negativo17@gmail.com> - 10:3.02-a07.2
- Remove support for RHEL 5
- Implement license macro.

* Fri Dec 16 2016 Simone Caronni <negativo17@gmail.com> - 10:3.02-a07.1
- Update to 3.02a07.

* Fri Mar 25 2016 Simone Caronni <negativo17@gmail.com> - 10:3.02-a05.1
- Update to 3.02a06.

* Thu Jan 28 2016 Simone Caronni <negativo17@gmail.com> - 10:3.02-a05.1
- Update to 3.02a05.

* Mon Dec 21 2015 Simone Caronni <negativo17@gmail.com> - 10:3.02-a04.1
- Update to 3.02a04.

* Sun Dec 06 2015 Simone Caronni <negativo17@gmail.com> - 10:3.02-a03.1
- Update to 3.02a03.

* Fri Nov 20 2015 Simone Caronni <negativo17@gmail.com> - 10:3.02-a02.1
- Updated to 3.02a02.

* Tue Nov 10 2015 Simone Caronni <negativo17@gmail.com> - 10:3.02-a01.1
- Updated to 3.02a01.

* Tue Sep 08 2015 Simone Caronni <negativo17@gmail.com> - 10:3.01-a31.2
- Fix isaed requirements.

* Tue Aug 04 2015 Simone Caronni <negativo17@gmail.com> - 10:3.01-a31.1
- Update to 3.01a31.

* Wed Jul 08 2015 Simone Caronni <negativo17@gmail.com> - 10:3.01-a30.1
- Updated to 3.01a30, rc for 3.01 final.
- Add libschily manpages to devel subpackage, adjust docs for each subpackage
  and charset conversion accordingly.
- Update URL.
- Update permissions on executables.
- Use RUNPATH= also on install section, required for libschily.

* Wed Jun 10 2015 Simone Caronni <negativo17@gmail.com> - 10:3.01-a29.1
- Update to 3.01a29.

* Wed Mar 25 2015 Simone Caronni <negativo17@gmail.com> - 10:3.01-a28.1
- Update to 3.01a28.
- Switched to Sourceforge URL.

* Sat Jan 31 2015 Simone Caronni <negativo17@gmail.com> - 10:3.01-a27.1
- Update to 3.01a27.

* Wed Jan 07 2015 Simone Caronni <negativo17@gmail.com> - 10:3.01-a26.1
- Update to 3.01a26.

* Tue Oct 07 2014 Simone Caronni <negativo17@gmail.com> - 10:3.01-a25.1
- Updated to 3.01a25.

* Mon May 19 2014 Simone Caronni <negativo17@gmail.com> - 10:3.01-a24.1
- Updated to 3.01a24.

* Wed Mar 05 2014 Simone Caronni <negativo17@gmail.com> - 10:3.01-a23.1
- Updated to 3.01a23.

* Tue Jan 21 2014 Simone Caronni <negativo17@gmail.com> - 10:3.01-a22.1
- Updated to 3.01a22.

* Sat Jan 04 2014 Simone Caronni <negativo17@gmail.com> - 10:3.01-a21.1
- Updated to 3.01a21.

* Thu Jan 02 2014 Simone Caronni <negativo17@gmail.com> - 10:3.01-a20.2
- Add patch for mkisofs -help bug. Thanks Frederik.

* Mon Dec 30 2013 Simone Caronni <negativo17@gmail.com> - 10:3.01-a20.1
- Update to 3.01a20.
- Removed upstreamed patch.

* Mon Nov 25 2013 Simone Caronni <negativo17@gmail.com> - 10:3.01-a19.1
- Update to 3.01a19.

* Mon Oct 14 2013 Simone Caronni <negativo17@gmail.com> - 10:3.01-a18.2
- Add explicit dependency on versioned library packages.

* Mon Oct 14 2013 Simone Caronni <negativo17@gmail.com> - 10:3.01-a18.1
- Update to 3.01a18.

* Mon Oct 07 2013 Simone Caronni <negativo17@gmail.com> - 10:3.01-a17.2
- Enable dynamic linking and shared objects with LINKMODE; added libraries and
  devel subpackage.
- Try supporting linux file flags.
- Fix capabilities support packaging error introduced in 3.01-a17.2.

* Mon Aug 05 2013 Simone Caronni <negativo17@gmail.com> - 10:3.01-a17.1
- Updated to 3.01a17.
- Added patch to enable additional platforms (ppc/el5, ppc64/el6, armv7hl/f20).

* Mon Jul 15 2013 Simone Caronni <negativo17@gmail.com> - 10:3.01-a16.1
- Updated.

* Mon Jun 03 2013 Simone Caronni <negativo17@gmail.com> - 10:3.01-a15.1
- Updated.

* Wed Apr 24 2013 Simone Caronni <negativo17@gmail.com> - 10:3.01-a14.1
- Updated.
- Added file capabilities for RHEL 6+ and Fedora.
- Moved around %%caps enabled files as in:
  https://bugzilla.redhat.com/show_bug.cgi?id=956190
  https://bugzilla.redhat.com/show_bug.cgi?id=904818

* Tue Mar 05 2013 Simone Caronni <negativo17@gmail.com> - 10:3.01-a13.1
- Updated.

* Wed Feb 13 2013 Simone Caronni <negativo17@gmail.com> - 10:3.01-a12.1
- Updated.

* Thu Jan 10 2013 Simone Caronni <negativo17@gmail.com> - 10:3.01-a11.1
- Updated.

* Mon Dec 17 2012 Simone Caronni <negativo17@gmail.com> - 10:3.01-a10.1
- Updated.

* Tue Dec 11 2012 Simone Caronni <negativo17@gmail.com> - 10:3.01-a09.1
- Updated.

* Thu Aug 16 2012 Simone Caronni <negativo17@gmail.com> - 10:3.01-a08.1
- Updated.

* Mon May 21 2012 Simone Caronni <negativo17@gmail.com> - 10:3.01-a07.3
- Added ?_isa.
- Added license files everywhere.
- Removed devel and btcflash subpackage.
- Changed man pages packaging.

* Wed May 16 2012 Simone Caronni <negativo17@gmail.com> - 10:3.01-a07.2
- Changed default device to sr0 as the cdrom symlink changes over time.

* Mon Mar 05 2012 Simone Caronni <negativo17@gmail.com> - 10:3.01-a07.1
- Updated.

* Thu Oct 27 2011 Simone Caronni <negativo17@gmail.com> - 10:3.01-a06.1
- Updated.

* Fri Sep 16 2011 Simone Caronni <negativo17@gmail.com> - 10:3.01-a05.2
- rpmlint fixes.

* Mon Jun 06 2011 Simone Caronni <negativo17@gmail.com> - 10:3.01-a05.1
- Updated.

* Mon May 09 2011 Simone Caronni <negativo17@gmail.com> - 10:3.01-a04.1
- Updated.

* Tue Mar 15 2011 Simone Caronni <negativo17@gmail.com> - 10:3.01-a03.1
- Updated.

* Tue Feb 08 2011 Simone Caronni <negativo17@gmail.com> - 10:3.01-a02.1
- Updated.

* Fri Dec 10 2010 Simone Caronni <negativo17@gmail.com> - 10:3.01-a01.2
- Fixed rpmlint errors.

* Tue Dec 07 2010 Simone Caronni <negativo17@gmail.com> - 3.01-a01.1
- Updated to 3.01a01.

* Mon Nov 29 2010 Simone Caronni <negativo17@gmail.com> - 3.00-4
- Remove linker paths.
- setuid for cdda2wav, readcd and rscsi.

* Fri Nov 26 2010 Roman Rakus <rrakus@redhat.com> - 3.00-2
- Fixed some rpmlint errors and warnings

* Thu Nov 25 2010 Simone Caronni <negativo17@gmail.com> - 3.00-1
- First build:
    +Patch default device to match standard Fedora behaviour, the first
     cdrom device setup by udev can be used without parameters.
    +Fix german letters in copyright.
    +Obsoletes cdrkit but provides its components for Anaconda, etc.
    +Epoch set to 10 to avoid loop problems with yum.
