Summary:     Easy-to-use, easy-to-install mailing list server
Name:        petidomo
Version:     2.2
Release:     5d
Copyright:   free for non commercial use
Group:	     Applications/Mail
Group(pl):   Aplikacje/Poczta
#######      ftp://ftp.petidomo.com/pub/petidomo/source
Source:      %{name}-%{version}-src.tar.gz
Source1:     %{name}-manual-html.tar.gz
Source2:     help-pl-eng
Source3:     commercial.txt
Patch:	     %{name}-src.PLD.diff
Patch1:	     %{name}-src.aliases.diff
URL:	     http://www.petidomo.com
BuildRoot:   /var/tmp/%{name}-%{version}-buildroot
Vendor:	     Peter Simons <simons@petidomo.com>
Summary(pl): £atwy w u¿yciu oraz instalacji serwer list pocztowych

%description
Petidomo Mailing List Manager

%description -l pl
Petidomo Mailing List Manager - zarz±dca pocztowych list dyskusyjnych

%package cgimanager
Summary:     CGI Manager for Petidomo
Group:       Applications/Mail
Group(pl):   Aplikacje/Poczta
Requires:    %{name} = %{version}
Summary(pl): Program CGI do zarz±dzania serwerem Petidomo

%description cgimanager
CGI program, that lets you do all the configuration out of your favourite
WWW-Browser.

Warning: cgi manager is SUID root!

%description -l pl cgimanager
Program CGI pozwalaj±cy na konfiguracjê serwera Petidomo poprzez ulubion±
przegl±darkê WWW.

Ostrze¿enie: mened¿er CGI obdarzony jest SUID'em root.

%prep
%setup -q -n %{name}-src
%patch  -p1
%patch1 -p1
%setup -q -D -T -a 1 -n %{name}-src

%build
autoconf
./configure \
    --prefix=/usr

%{__make} CFLAGS+="$RPM_OPT_FLAGS"

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
install -s src/petidomo/petidomo $RPM_BUILD_ROOT/home/petidomo/bin
# 750 petidomo petidomo
install scripts/InsertNameInSubject.sh $RPM_BUILD_ROOT/home/petidomo/bin
install scripts/rfc2369.sh $RPM_BUILD_ROOT/home/petidomo/bin
# 750 petidomo petidomo
install scripts/pgp-encrypt.sh $RPM_BUILD_ROOT/home/petidomo/bin
install scripts/pgp-decrypt.sh $RPM_BUILD_ROOT/home/petidomo/bin
# 755 petidomo petidomo
install scripts/send-pr $RPM_BUILD_ROOT/home/petidomo/bin
# 660 petidomo petidomo
install %SOURCE2 $RPM_BUILD_ROOT/home/petidomo/etc/help
install etc/masteracl $RPM_BUILD_ROOT/home/petidomo/etc/acl
install etc/masterconfig $RPM_BUILD_ROOT/home/petidomo/etc/petidomo.conf
# 6111 root petidomo
install -s src/htmlconf/htmlconf \
    $RPM_BUILD_ROOT/home/httpd/cgi-bin/petidomoconf
# doc
install %SOURCE3 .

sed -e  "s#@MTA@#/usr/lib/sendmail#" < $RPM_BUILD_ROOT/home/petidomo/\
etc/petidomo.conf > $RPM_BUILD_ROOT/home/petidomo/etc/petidomo.conf.new
mv -f $RPM_BUILD_ROOT/home/petidomo/etc/petidomo.conf.new \
$RPM_BUILD_ROOT/home/petidomo/etc/petidomo.conf

ln -s petidomo	$RPM_BUILD_ROOT/home/petidomo/bin/listserv
ln -s petidomo  $RPM_BUILD_ROOT/home/petidomo/bin/hermes

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
echo "petidomo-manager: postmaster"	>> /etc/mail/aliases
echo "petidomo:  \"|/home/petidomo/bin/listserv\"" >> /etc/mail/aliases
/usr/bin/newaliases
fi

chmod -f 751 /home/petidomo

%files
%defattr(644,root,root,755)
%doc petidomo-manual-html README COPYRIGHT etc/ChangeLog etc/mail2news.c
%doc scripts/list2news scripts/aliases4qmail.sh etc/listconfig commercial.txt

%attr(751,petidomo,petidomo) %dir /home/petidomo/bin
%attr(750,petidomo,petidomo) %dir /home/petidomo/etc
%attr(750,petidomo,petidomo) %dir /home/petidomo/lists
%attr(770,petidomo,petidomo) %dir /home/petidomo/crash

%attr(6111,petidomo,petidomo) /home/petidomo/bin/petidomo
%attr(6111,petidomo,petidomo) /home/petidomo/bin/listserv
%attr(6111,petidomo,petidomo) /home/petidomo/bin/hermes

%attr(750,petidomo,petidomo) /home/petidomo/bin/InsertNameInSubject.sh
%attr(750,petidomo,petidomo) /home/petidomo/bin/rfc2369.sh
%attr(750,petidomo,petidomo) /home/petidomo/bin/pgp-encrypt.sh
%attr(750,petidomo,petidomo) /home/petidomo/bin/pgp-decrypt.sh
%attr(755,petidomo,petidomo) /home/petidomo/bin/send-pr

%attr(660,petidomo,petidomo) %config(noreplace) %verify(not size mtime md5) /home/petidomo/etc/*

%attr(644,petidomo,petidomo) /home/petidomo/.nofinger

%files cgimanager
%attr(6111,root,petidomo) /home/httpd/cgi-bin/petidomoconf

%changelog
* Sat Jan 16 1999 Arkadiusz Mi¶kiewicz <misiek@pld.za.net>
[2.2-5d]
- added cgimanager subpackage (includes SUID)
- changed /etc/aliases to /etc/mail/aliases
- removed /home/petidomo
- added stripping

* Tue Dec 22 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
[2.2-3d]
- added commercial.txt (now we can put this rpm on ftp server)
- few corrections

* Sun Nov 08 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
- removed patch
- removed archived directory
- corrected few paths
- removed (noreplace) from acl and petidomo.conf file
- added usermod
- added .nofinger
- added help-pl-eng

* Thu Oct 29 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
- initial RPM release
