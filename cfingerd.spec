Summary:	Highly configurable and secure finger daemon with IPv6 support
Summary(pl):	Niezwykle konfigurowalny i bezpieczny demon fingerd ze wspraciem dla IPv6
Name:		cfingerd
Version:	1.4.3
Release:	2
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Copyright:	GPL
Vendor:		Martin Schulze <joey@infodrom.north.de>
URL:		http://www.infodrom.north.de/cfingerd/
Source0:	ftp://ftp.infodrom.north.de/pub/people/joey/cfingerd/%{name}-%{version}.tar.gz
Source1:	%{name}.logrotate
Source2:	%{name}.inetd
Patch0:		http://www.misiek.eu.org/ipv6/cfingerd-1.4.3-ipv6-12121999.patch.gz
Patch1:		%{name}-config.patch
Requires:	inetdaemon
Requires:	rc-inetd
Provides:	fingerd
Obsoletes:	cfingerd-nobody
Obsoletes:	cfingerd-noroot
Obsoletes:	ffingetd
Obsoletes:	finger-server
Obsoletes:	bsd-fingerd
BuildRoot:	/tmp/%{name}-%{version}-root

%description
* CFINGERD is a free finger daemon replacement for standard finger daemons
  such as GNU Finger, MIT Finger, or KFINGERD.  CFINGERD is highly
  becoming a respected standard as the finger daemon to use. 

%description -l pl
* CFINGERD jest darmowym serwerem us³ugi finger zastêpuj±cym inne demony
  fingera takie jak GNU Finger, MIT Finger, lub KFINGERD. CFINGERD staje
  siê respektowanym standardem dla demonów us³ugi finger.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
./Configure
make all CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

install	-d $RPM_BUILD_ROOT/etc/{%{name}/scripts,logrotate.d,sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{1,5,8}}

install -s src/cfingerd	userlist/userlist $RPM_BUILD_ROOT%{_sbindir}/
install	cfingerd.conf userlist/userlist.conf $RPM_BUILD_ROOT/etc/%{name}/

install	scripts/* $RPM_BUILD_ROOT/etc/%{name}/scripts/

install %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install	%{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/%{name}

install userlist/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/
install	docs/*.5 $RPM_BUILD_ROOT%{_mandir}/man5/
install	docs/*.8 $RPM_BUILD_ROOT%{_mandir}/man8/

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	CHANGES CREDITS FAQ README README.noroot RECOMMEND TODO

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %dir /etc/%{name}
%attr(755,root,root) %dir /etc/%{name}/scripts
%attr(755,root,root) /etc/%{name}/scripts/*
%attr(755,root,root) %{_sbindir}/*
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) /etc/%{name}/cfingerd.conf
%config(noreplace) %verify(not size mtime md5) /etc/%{name}/userlist.conf
/etc/%{name}/*.txt
%attr(640,root,root) /etc/logrotate.d/%{name}
%attr(640,root,root) /etc/sysconfig/rc-inetd/%{name}
%{_mandir}/man[158]/*
