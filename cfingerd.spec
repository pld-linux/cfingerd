Summary:	Highly configurable and secure finger daemon with IPv6 support
Summary(pl):	Niezwykle konfigurowalny i bezpieczny demon fingerd ze wsparciem dla IPv6
Name:		cfingerd
Version:	1.4.3
Release:	13
License:	GPL
Group:		Networking/Daemons
Vendor:		Martin Schulze <joey@infodrom.north.de>
URL:		http://www.infodrom.north.de/cfingerd/
Source0:	http://www.infodrom.org/projects/cfingerd/download/%{name}-%{version}.tar.gz
# Source0-md5:	fe9365f811624248aa3df52c4a832fc7
Source1:	%{name}.logrotate
Source2:	%{name}.inetd
Patch0:		http://www.misiek.eu.org/ipv6/%{name}-1.4.3-ipv6-12121999.patch.gz
Patch1:		%{name}-config.patch
Patch2:		%{name}-security_format_bug.patch
Patch3:		%{name}-gpg.patch
Requires:	inetdaemon
Prereq:		rc-inetd >= 0.8.1
Provides:	fingerd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	cfingerd-nobody
Obsoletes:	cfingerd-noroot
Obsoletes:	efingerd
Obsoletes:	ffingerd
Obsoletes:	finger-server
Obsoletes:	bsd-fingerd

%description
CFINGERD is a free finger daemon replacement for standard finger
daemons such as GNU Finger, MIT Finger, or KFINGERD. CFINGERD is
highly becoming a respected standard as the finger daemon to use.

%description -l pl
CFINGERD jest darmowym serwerem us³ugi finger zastêpuj±cym inne demony
fingera takie jak GNU Finger, MIT Finger, lub KFINGERD. CFINGERD staje
siê respektowanym standardem dla demonów us³ugi finger.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
./Configure
%{__make} all CFLAGS="-DINET6=1 %{rpmcflags}" LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{%{name}/scripts,logrotate.d,sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{1,5,8}}

install src/cfingerd userlist/userlist $RPM_BUILD_ROOT%{_sbindir}/
install	cfingerd.conf userlist/userlist.conf texts/*.txt \
$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/

install scripts/* $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/scripts/

install %{SOURCE1} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}
install	%{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/fingerd

install userlist/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/
install	docs/*.5 $RPM_BUILD_ROOT%{_mandir}/man5/
install	docs/*.8 $RPM_BUILD_ROOT%{_mandir}/man8/


%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES CREDITS FAQ README README.noroot RECOMMEND TODO
%attr(755,root,root) %dir %{_sysconfdir}/%{name}
%attr(755,root,root) %dir %{_sysconfdir}/%{name}/scripts
%attr(755,root,root) %{_sysconfdir}/%{name}/scripts/*
%attr(755,root,root) %{_sbindir}/*
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}/cfingerd.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}/userlist.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}/*.txt
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/logrotate.d/%{name}
%attr(640,root,root) /etc/sysconfig/rc-inetd/fingerd
%{_mandir}/man[158]/*
