# Otherwise we don't pass rpmlint control
%define _enable_debug_packages %{nil}
%define debug_package %{nil}

%define snapshot	1331
%define rel		7
%define distname	linuxtv-dvb-apps

%if %snapshot
%define release 8.hg%{snapshot}.%{rel}
%else
%define release %{rel}
%endif

Summary:	Various apps for DVB cards
Name:		dvb-apps
Version:	1.1.1
Release:	%{release}
License:	GPLv2+
Group:		Video
URL:		http://www.linuxtv.org/wiki/index.php/LinuxTV_dvb-apps
%if %{snapshot}
Source0:	%{distname}-%{snapshot}.tar.bz2
%else
Source0:	http://linuxtv.org/download/dvb/%{distname}-%{version}.tar.bz2
%endif
# (Anssi 02/2008): dvbnet tries to strip 'path/' out from 'path/dvbnet'
# in argv[0] when showing it in commandline usage help output. The NULL
# check is buggy as 's' has already been incremented by 1 before the check.
# This patch removes the stripping altogether and uses the full argv[0]
# in usage(), as GNU utilities do.
Patch0:		dvbnet-do-not-strip-dir-from-argv0.patch
Patch1:		dvb-apps-format-string.patch
# fix transport stream id 0 on first transponder in some cases, when outputting
# in vdr format
Patch2:		dvb-apps-scan-fix-transport-stream-id.patch
# Fix czap channel line parser using %a in scanf, which doesn't work with recent
# glibc (from upstream)
Patch3:		dvb-apps-czap-fix-sscanf-c99-modifier.patch
Patch4:		linuxtv-dvb-apps-1331-videodev.patch
BuildRequires:	libv4l-devel
# bin/scan conflict:
Conflicts:	nmh

%description
Various apps for DVB cards.
# No sonames, and these are presumably only used internally,
# so put them all in the same package;
# If some other apps start using them, sonames should be fixed,
# and package splitted properly. - Anssi
%define libname %mklibname dvbapps
%define devname %mklibname -d dvbapps

%package -n %libname
Summary:	Common libraries used by dvb-apps
Group:		System/Libraries

%description -n %libname
Common libraries as used by the dvb-apps package.

%package -n %devname
Summary:	Development files for dvb-apps
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%libname = %{version}-%{release}

%description -n %devname
Development files for dvb-apps, for building applications that depend on:
- libdvbapi
- libdvbcfg
- libdvben50221
- libdvbsec
- libesg
- libucsi

%prep
%if %snapshot
%setup -q -n %distname-%snapshot
%else
%setup -q -n %distname-%version -a 1
%endif
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0

%build
%setup_compile_flags
# (Anssi 02/2008) version.h gets written too late for dvbnet.c,
# parallel make broken
make prefix=%_prefix libdir=%_libdir includedir=%_includedir sharedir=%_datadir

%install
%makeinstall_std prefix=%_prefix libdir=%_libdir includedir=%_includedir sharedir=%_datadir

install -m644 util/av7110_loadkeys/README README.av7110_loadkeys
perl -pi -e 's:./evtest:evtest:' README.av7110_loadkeys
perl -pi -e 's:./av7110_loadkeys:av7110_loadkeys:' README.av7110_loadkeys
perl -pi -e "s:hauppauge.rc5:%{_datadir}/dvb/av7110_loadkeys/hauppauge.rc5:" README.av7110_loadkeys

install -m644 util/scan/README README.scan
perl -pi -e "s:\./::g" README.scan
perl -pi -e "s:dvb-s/Astra-19.2E:%{_datadir}/dvb/dvb-s/Astra-19.2E:" README.scan
perl -pi -e "s:atscscan -h:atscscan -h\nTuning files are stored in %{_datadir}/dvb.:"  README.scan

install -m644 util/szap/README README.zap
perl -pi -e "s:\./::g" README.zap

# backward compatibility:
ln -s scan %{buildroot}%{_bindir}/scandvb

%files
%doc README README.av7110_loadkeys README.scan util/dvbnet/net_start.*
%doc util/dib3000-watch/README.* README.zap
%{_bindir}/atsc_epg
%{_bindir}/av7110_loadkeys
%{_bindir}/azap
%{_bindir}/czap
%{_bindir}/dib3000-watch
%{_bindir}/dst_test
%{_bindir}/dvbdate
%{_bindir}/dvbnet
%{_bindir}/dvbscan
%{_bindir}/dvbtraffic
%{_bindir}/femon
%{_bindir}/gnutv
%{_bindir}/scan
%{_bindir}/scandvb
%{_bindir}/szap
%{_bindir}/tzap
%{_bindir}/zap
%dir %{_datadir}/dvb
%{_datadir}/dvb/atsc
%{_datadir}/dvb/av7110_loadkeys
%{_datadir}/dvb/dvb-c
%{_datadir}/dvb/dvb-s
%{_datadir}/dvb/dvb-t

%files -n %{libname}
%{_libdir}/libdvb*.so
%{_libdir}/libesg.so
%{_libdir}/libucsi.so

%files -n %devname
%{_includedir}/libdvbapi
%{_includedir}/libdvbcfg
%{_includedir}/libdvben50221
%{_includedir}/libdvbsec
%{_includedir}/libesg
%{_includedir}/libucsi
%{_libdir}/libdvb*.a
%{_libdir}/libesg.a
%{_libdir}/libucsi.a


%changelog
* Tue May 03 2011 Funda Wang <fwang@mandriva.org> 1.1.1-8.hg1331.5mdv2011.0
+ Revision: 664523
- fix build with latest kernel

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-8.hg1331.4mdv2011.0
+ Revision: 604833
- rebuild

* Wed Jun 23 2010 Anssi Hannula <anssi@mandriva.org> 1.1.1-8.hg1331.3mdv2010.1
+ Revision: 548754
- fix czap config file parser (it uses %%a in sscanf for a string field,
  while recent glibc versions interpret %%a as a floating point conversion
  specifier as specified in C99, as per glibc CONFORMANCE file, contrary
  to sscanf man page; patch from upstream)

  + Frederic Crozat <fcrozat@mandriva.com>
    - Fix url
    - fix license

* Sun Jan 24 2010 Anssi Hannula <anssi@mandriva.org> 1.1.1-8.hg1331.2mdv2010.1
+ Revision: 495574
- fix zero transport stream id in scan output under some circuimstances
  (fixes EPG in VDR, scan-fix-transport-stream-id.patch)

* Sat Jan 16 2010 Anssi Hannula <anssi@mandriva.org> 1.1.1-8.hg1331.1mdv2010.1
+ Revision: 492505
- new snapshot
- introduces library and devel packages, currently used internally only
- use upstream file locations
- do not rename scan to scandvb, instead add conflict with nmh
  (compatibility link is added)
- fix format string (format-string.patch)
- rediff do-not-strip-dir-from-argv0.patch
- remove vdr-zero-ca.patch, applied upstream

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-7mdv2010.0
+ Revision: 413412
- rebuild

* Tue Dec 02 2008 Anssi Hannula <anssi@mandriva.org> 1.1.1-6mdv2009.1
+ Revision: 309377
- update scan data

* Thu Mar 13 2008 Anssi Hannula <anssi@mandriva.org> 1.1.1-5mdv2008.1
+ Revision: 187533
- scandvb: do not incorrectly set CA field to non-zero value by default for
  VDR 1.3+ (patch from upstream trunk)

* Thu Feb 28 2008 Anssi Hannula <anssi@mandriva.org> 1.1.1-4mdv2008.1
+ Revision: 175962
- disable parallel make
- dvbnet: do not strip directories from argv[0] when displaying
  help output, fixes segfault (P0, fixes #38012)
- new snapshot of scan data

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 1.1.1-3mdv2008.1
+ Revision: 140722
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Sep 24 2007 Anssi Hannula <anssi@mandriva.org> 1.1.1-3mdv2008.0
+ Revision: 92519
- new initial transponder scan data snapshot

* Tue Jun 26 2007 Adam Williamson <awilliamson@mandriva.org> 1.1.1-2mdv2008.0
+ Revision: 44258
- drop unneeded BuildRequires, rebuild for 2008
- Import dvb-apps



* Fri Jun 02 2006 Anssi Hannula <anssi@mandriva.org> 1.1.1-1mdv2007.0
- 1.1.1
- drop patch1, unneeded
- add atsc tuning files

* Sun Oct 2 2005 Erwan Velu <erwan@seanodes.com> 1.1.0-6mdk
- Updating dvb-t config files from CVS

* Mon Aug 29 2005 Marcel Pol <mpol@mandriva.org> 1.1.0-5mdk
- rebuild

* Tue Jul 27 2004 Svetoslav Slavtchev <svetljo@gmx.de> 1.1.0-4mdk
- rebuild

* Mon Jun 07 2004 Svetoslav Slavtchev <svetljo@gmx.de> 1.1.0-3mdk
- drop an unused patch & fix perms

* Mon Jun 07 2004 Svetoslav Slavtchev <svetljo@gmx.de> 1.1.0-2mdk
- contrib build
  clean up club stuff

* Sun Apr 04 2004 Svetoslav Slavtchev <svetljo@gmx.de> 1.1.0-1mdk
- update source
- tweak the docs to the mdk layout
- build for club

* Wed Sep 17 2003 Marcel Pol <mpol@gmx.net> 1.0.0-1mdk
- initial contrib from Svetoslav Slavtchev
