%define name		dvb-apps
%define version		1.1.1
%define beta		0
%define rel		7
%define distname	linuxtv-dvb-apps
%define scandata_rev	1237

%if %beta
%define release %mkrel 0.%{beta}.%{rel}
%else
%define release %mkrel %{rel}
%endif

Summary:	Various apps for DVB cards
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://linuxtv.org/download/dvb/%{distname}-%{version}.tar.bz2
# hg clone http://linuxtv.org/hg/dvb-apps scan-data
# tar -cjf scan-data-$(cd scan-data; hg tip --template {rev}).tar.bz2 scan-data/util/scan/{atsc,dvb-[cst]}
# /bin/rm -r scan-data
Source1:	scan-data-%{scandata_rev}.tar.bz2
# (Anssi 02/2008): dvbnet tries to strip 'path/' out from 'path/dvbnet'
# in argv[0] when showing it in commandline usage help output. The NULL
# check is buggy as 's' has already been incremented by 1 before the check.
# This patch removes the stripping altogether and uses the full argv[0]
# in usage(), as GNU utilities do.
Patch0:		dvbnet-do-not-strip-dir-from-argv0.patch
# (Anssi) Do not set CA to non-zero by default for VDR, from upstream hg:
Patch1:		scan-vdr-zero-ca.patch
License:	GPL
Group:		Video
URL:		http://linuxtv.org/dvb/
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
Various apps for DVB cards.

%prep
%setup -q -n %distname-%version -a 1
%patch0 -p1
%patch1 -p1

%build
# (Anssi 02/2008) version.h gets written too late for dvbnet.c,
# parallel make broken
make

%install
rm -rf $RPM_BUILD_ROOT
install -d -m755 %buildroot/%{_bindir}

cd util
#
# binaries
#

install -m755 av7110_loadkeys/av7110_loadkeys %buildroot/%{_bindir}/
install -m755 av7110_loadkeys/evtest %buildroot/%{_bindir}/av7110_evtest
install -m755 dvbdate/dvbdate %buildroot/%{_bindir}/
install -m755 dvbnet/dvbnet %buildroot/%{_bindir}/
install -m755 dvbtraffic/dvbtraffic %buildroot/%{_bindir}/
install -m755 scan/scan %buildroot/%{_bindir}/scandvb
install -m755 szap/*zap %buildroot/%{_bindir}/
install -m755 szap/femon %buildroot/%{_bindir}/

cd ../scan-data/util
# from source1:
install -d -m755 %buildroot/%{_datadir}/%{name}/scan
cp -pr scan/dvb-c %buildroot/%{_datadir}/%{name}/scan/
cp -pr scan/dvb-s %buildroot/%{_datadir}/%{name}/scan/
cp -pr scan/dvb-t %buildroot/%{_datadir}/%{name}/scan/
cp -pr scan/atsc %buildroot/%{_datadir}/%{name}/scan/
cd -

install -d -m755 %buildroot/%{_datadir}/%{name}/av7110_loadkeys
install -m644 av7110_loadkeys/*rc5  %buildroot/%{_datadir}/%{name}/av7110_loadkeys/
install -m644 av7110_loadkeys/*rcmm  %buildroot/%{_datadir}/%{name}/av7110_loadkeys/
#
# confs & doc
#

install -d -m755 %buildroot/%{_sysconfdir}/dvb
install -m644 szap/channels.conf* %buildroot/%{_sysconfdir}/dvb

install -m644 av7110_loadkeys/README ../README.av7110_loadkeys
perl -pi -e 's:./evtest:av7110_evtest:' ../README.av7110_loadkeys
perl -pi -e 's:./av7110_loadkeys:av7110_loadkeys:' ../README.av7110_loadkeys
perl -pi -e "s:hauppauge.rc5:%{_datadir}/%{name}/av7110_loadkeys/hauppauge.rc5:" ../README.av7110_loadkeys

install -m644 scan/README ../README.scandvb
perl -pi -e "s:./scan :scandvb :"  ../README.scandvb
perl -pi -e "s:dvb-s/Astra-19.2E:%{_datadir}/%{name}/scan/dvb-s/Astra-19.2E:"  ../README.scandvb
perl -pi -e "s:scandvb -h.:scandvb -h, tuning files are stored in %{_datadir}/%{name}/scan .:"  ../README.scandvb

install -m755 dvbnet/net_start.* ../

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/dvb/
%config(noreplace) %{_sysconfdir}/dvb/*
%{_bindir}/*
%dir %{_datadir}/%name
%{_datadir}/%name/*
%doc TODO README README.av7110_loadkeys README.scandvb net_start.pl  net_start.sh
