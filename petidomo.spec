Summary:	Easy-to-use, easy-to-install mailing list server
Summary(pl):	£atwy w u¿yciu oraz instalacji serwer list pocztowych
Name:		petidomo
Version:	2.2
Release:	5d
License:	Free for non-commercial use
Vendor:		Peter Simons <simons@petidomo.com>
Group:		Applications/Mail
Source0:	http://www.petidomo.com/download/%{version}/source/%{name}-%{version}-src.tar.gz
Source1:	%{name}-manual-html.tar.gz
Source2:	help-pl-eng
Source3:	commercial.txt
Patch0:		%{name}-src.PLD.diff
Patch1:		%{name}-src.aliases.diff
URL:		http://www.petidomo.com/
BuildRequires:	autoconf
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Petidomo Mailing List Manager.

%description -l pl
Petidomo Mailing List Manager - zarz±dca pocztowych list dyskusyjnych.

%package cgimanager
Summary:	CGI Manager for Petidomo
Summary(pl):	Program CGI do zarz±dzania serwerem Petidomo
Group:		Applications/Mail
Requires:	%{name} = %{version}

%description cgimanager
CGI program, that lets you do all the configuration out of your
favourite WWW-Browser.

Warning: cgi manager is SUID root!

%description cgimanager -l pl
Program CGI pozwalaj±cy na konfiguracjê serwera Petidomo poprzez
ulubion± przegl±darkê WWW.

Ostrze¿enie: mened¿er CGI obdarzony jest SUID-em root.

%prep
%setup -q -n %{name}-src
%patch  -p1
%patch1 -p1
%setup -q -D -T -a 1 -n %{name}-src

%build
autoconf
./configure \
--prefix=%{_prefix}

%{__make} CFLAGS+="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/home/httpd/cgi-bin
# 751 petidomo petidomo
install -d $RPM_BUILD_ROOT/home/petidomo/bin
# 750 petidomo petidomo
install -d $RPM_BUILD_ROOT/home/petidomo/{etc,lists}
# 770 petidomo petidomo
install -d $RPM_BUILD_ROOT/home/petidomo/crash
# 6111 petidomo petidomo
install src/petidomo/petidomo $RPM_BUILD_ROOT/home/petidomo/bin
# 750 petidomo petidomo
install scripts/InsertNameInSubject.sh $RPM_BUILD_ROOT/home/petidomo/bin
install scripts/rfc2369.sh $RPM_BUILD_ROOT/home/petidomo/bin
# 750 petidomo petidomo
install scripts/pgp-encrypt.sh $RPM_BUILD_ROOT/home/petidomo/bin
install scripts/pgp-decrypt.sh $RPM_BUILD_ROOT/home/petidomo/bin
# 755 petidomo petidomo
install scripts/send-pr $RPM_BUILD_ROOT/home/petidomo/bin
# 660 petidomo petidomo
install %SOURCE2 $RPM_BUILD_ROOT/home/petidomo%{_sysconfdir}/help
install etc/masteracl $RPM_BUILD_ROOT/home/petidomo%{_sysconfdir}/acl
install etc/masterconfig $RPM_BUILD_ROOT/home/petidomo%{_sysconfdir}/petidomo.conf
# 6111 root petidomo
install src/htmlconf/htmlconf \
	$RPM_BUILD_ROOT/home/httpd/cgi-bin/petidomoconf
# doc
install %{SOURCE3} .

sed -e  "s#@MTA@#%{_libdir}/sendmail#" < $RPM_BUILD_ROOT/home/petidomo/\
etc/petidomo.conf > $RPM_BUILD_ROOT/home/petidomo%{_sysconfdir}/petidomo.conf.new
mv -f $RPM_BUILD_ROOT/home/petidomo%{_sysconfdir}/petidomo.conf.new \
$RPM_BUILD_ROOT/home/petidomo%{_sysconfdir}/petidomo.conf

ln -sf petidomo	$RPM_BUILD_ROOT/home/petidomo/bin/listserv
ln -sf petidomo  $RPM_BUILD_ROOT/home/petidomo/bin/hermes

touch $RPM_BUILD_ROOT/home/petidomo/.nofinger

%clean
rm -rf $RPM_BUILD_ROOT

%post
mv -f /home/petidomo/etc/petidomo.conf /home/petidomo/etc/petidomo.conf.new
sed -e "s#@HOSTNAME@#`hostname --fqdn`#" < \
/home/petidomo/etc/petidomo.conf.new > /home/petidomo/etc/petidomo.conf
rm -f /home/petidomo/etc/petidomo.conf.new
chown -f petidomo.petidomo /home/petidomo/etc/petidomo.conf
chmod -f 660 /home/petidomo/etc/petidomo.conf

if ! grep -q ^petidomo /etc/mail/aliases; then
echo "#" 				>> /etc/mail/aliases
echo "# Mailing List Stuff"		>> /etc/mail/aliases
echo "#"				>> /etc/mail/aliases
echo "petidomo-manager:postmaster"	>> /etc/mail/aliases
echo "petidomo:\"|/home/petidomo/bin/listserv\"" >> /etc/mail/aliases
/usr/bin/newaliases
fi

chmod -f 751 /home/petidomo

%files
%defattr(644,root,root,755)
%doc petidomo-manual-html README COPYRIGHT etc/ChangeLog etc/mail2news.c
%doc scripts/list2news scripts/aliases4qmail.sh etc/listconfig commercial.txt

%attr(751,root,petidomo) %dir /home/petidomo/bin
%attr(750,root,petidomo) %dir /home/petidomo%{_sysconfdir}
%attr(770,root,petidomo) %dir /home/petidomo/lists
%attr(770,root,petidomo) %dir /home/petidomo/crash

%attr(6111,root,petidomo) /home/petidomo/bin/petidomo
%attr(6111,root,petidomo) /home/petidomo/bin/listserv
%attr(6111,root,petidomo) /home/petidomo/bin/hermes

%attr(750,root,petidomo) /home/petidomo/bin/InsertNameInSubject.sh
%attr(750,root,petidomo) /home/petidomo/bin/rfc2369.sh
%attr(750,root,petidomo) /home/petidomo/bin/pgp-encrypt.sh
%attr(750,root,petidomo) /home/petidomo/bin/pgp-decrypt.sh
%attr(755,root,petidomo) /home/petidomo/bin/send-pr

%attr(660,root,petidomo) %config(noreplace) %verify(not size mtime md5) /home/petidomo%{_sysconfdir}/*

%attr(644,root,petidomo) /home/petidomo/.nofinger

%files cgimanager
%defattr(644,root,root,755)
%attr(6111,root,petidomo) /home/httpd/cgi-bin/petidomoconf
