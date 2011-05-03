%define name		dvb-apps
%define version		1.1.1
%define snapshot	1331
%define rel		5
%define distname	linuxtv-dvb-apps

%if %snapshot
%define release %mkrel 8.hg%{snapshot}.%{rel}
%else
%define release %mkrel %{rel}
%endif

Summary:	Various apps for DVB cards
Name:		%{name}
Version:	%{version}
Release:	%{release}
%if %snapshot
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
License:	GPLv2+
Group:		Video
URL:		http://www.linuxtv.org/wiki/index.php/LinuxTV_dvb-apps
BuildRoot:	%{_tmppath}/%{name}-buildroot
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

%build
%setup_compile_flags
# (Anssi 02/2008) version.h gets written too late for dvbnet.c,
# parallel make broken
make prefix=%_prefix libdir=%_libdir includedir=%_includedir sharedir=%_datadir

%install
rm -rf $RPM_BUILD_ROOT

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
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

%files -n %libname
%defattr(-,root,root)
%{_libdir}/libdvb*.so
%{_libdir}/libesg.so
%{_libdir}/libucsi.so

%files -n %devname
%defattr(-,root,root)
%{_includedir}/libdvbapi
%{_includedir}/libdvbcfg
%{_includedir}/libdvben50221
%{_includedir}/libdvbsec
%{_includedir}/libesg
%{_includedir}/libucsi
%{_libdir}/libdvb*.a
%{_libdir}/libesg.a
%{_libdir}/libucsi.a
