%define name		dvb-apps
%define version		1.1.1
%define beta		0
%define mdkrel		%mkrel 2
%define distname	linuxtv-dvb-apps

%if %beta
%define release 0.%{beta}.%{mdkrel}
%else
%define release %{mdkrel}
%endif

Summary:	Various apps for DVB cards
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://linuxtv.org/download/dvb/%{distname}-%{version}.tar.bz2
License:	GPL
Group:		Video
URL:		http://linuxtv.org/dvb/
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
Various apps for DVB cards.

%prep
%setup -q -n %distname-%version

%build
%make

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

install -d -m755 %buildroot/%{_datadir}/%{name}/scan
cp -pr scan/dvb-c %buildroot/%{_datadir}/%{name}/scan/
cp -pr scan/dvb-s %buildroot/%{_datadir}/%{name}/scan/
cp -pr scan/dvb-t %buildroot/%{_datadir}/%{name}/scan/
cp -pr scan/atsc %buildroot/%{_datadir}/%{name}/scan/

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
