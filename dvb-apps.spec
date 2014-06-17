# Otherwise we don't pass rpmlint control
%define _enable_debug_packages %{nil}
%define debug_package %{nil}
# linting will fail anyway due the not-standard-release-extension .Sflo
%define _build_pkgcheck_set %{nil}

%define snapshot	1500
%define rel		1
%define distname	dvb-apps

%if %{snapshot}
%else
%endif

Summary:	Various apps for DVB cards
Name:		dvb-apps
Version:	1.1.1
Release:	%{rel}
License:	GPLv2+
Group:		Video
Url:		http://www.linuxtv.org/wiki/index.php/LinuxTV_dvb-apps
%if %{snapshot}
Source0:	%{distname}-%{snapshot}.tar.xz
%else
Source0:	http://linuxtv.org/download/dvb/%{distname}-%{version}.tar.bz2
%endif
# (Anssi 02/2008): dvbnet tries to strip 'path/' out from 'path/dvbnet'
# in argv[0] when showing it in commandline usage help output. The NULL
# check is buggy as 's' has already been incremented by 1 before the check.
# This patch removes the stripping altogether and uses the full argv[0]
# in usage(), as GNU utilities do.
Patch0:		dvbnet-do-not-strip-dir-from-argv0.patch

BuildRequires:	pkgconfig(libv4l2)
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

%package -n %{libname}
Summary:	Common libraries used by dvb-apps
Group:		System/Libraries

%description -n %{libname}
Common libraries as used by the dvb-apps package.

%package -n %{devname}
Summary:	Development files for dvb-apps
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
Development files for dvb-apps, for building applications that depend on:
- libdvbapi
- libdvbcfg
- libdvben50221
- libdvbsec
- libesg
- libucsi

%prep
%if %{snapshot}
%setup -q -n %{distname}-%{snapshot}
%else
%setup -q -n %{distname}-%{version} -a 1
%endif
%patch0 -p1

%build
%setup_compile_flags
# (Anssi 02/2008) version.h gets written too late for dvbnet.c,
# parallel make broken
make prefix=%{_prefix} libdir=%{_libdir} includedir=%{_includedir} sharedir=%{_datadir}

%install
%makeinstall_std prefix=%{_prefix} libdir=%{_libdir} includedir=%{_includedir} sharedir=%{_datadir}

install -m644 util/av7110_loadkeys/README README.av7110_loadkeys
sed -i -e 's:./evtest:evtest:' README.av7110_loadkeys
sed -i -e 's:./av7110_loadkeys:av7110_loadkeys:' README.av7110_loadkeys
sed -i -e "s:hauppauge.rc5:%{_datadir}/dvb/av7110_loadkeys/hauppauge.rc5:" README.av7110_loadkeys

install -m644 util/scan/README README.scan
sed -i -e "s:\./::g" README.scan
sed -i -e "s:dvb-s/Astra-19.2E:%{_datadir}/dvb/dvb-s/Astra-19.2E:" README.scan
sed -i -e "s:atscscan -h:atscscan -h\nTuning files are stored in %{_datadir}/dvb.:"  README.scan

install -m644 util/szap/README README.zap
sed -i -e "s:\./::g" README.zap

# backward compatibility:
ln -s scan %{buildroot}%{_bindir}/scandvb

%files
%doc README README.av7110_loadkeys README.scan util/dvbnet/net_start.*
%doc util/dib3000-watch/README.* README.zap
%{_bindir}/*
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

%files -n %{devname}
%{_includedir}/libdvbapi
%{_includedir}/libdvbcfg
%{_includedir}/libdvben50221
%{_includedir}/libdvbsec
%{_includedir}/libesg
%{_includedir}/libucsi
%{_libdir}/libdvb*.a
%{_libdir}/libesg.a
%{_libdir}/libucsi.a

