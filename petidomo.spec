# TODO: there is no petidomo user/group (anywhere)
Summary:	Easy-to-use, easy-to-install mailing list server
Summary(pl):	£atwy w u¿yciu oraz instalacji serwer list pocztowych
Name:		petidomo
Version:	2.2
Release:	5d
License:	Free for non-commercial use
Vendor:		Peter Simons <simons@petidomo.com>
Group:		Applications/Mail
Source0:	http://www.petidomo.com/download/%{version}/source/%{name}-%{version}-src.tar.gz
# Source0-md5:	37f1380503f60d6a53ca70e1500bd50a
Source1:	%{name}-manual-html.tar.gz
# Source1-md5:	6dc92bea47f13588d0b53594426fbff1
Source2:	help-pl-eng
Source3:	commercial.txt
Patch0:		%{name}-src.PLD.diff
Patch1:		%{name}-src.aliases.diff
Patch2:		%{name}-acfix.patch
URL:		http://www.petidomo.com/
BuildRequires:	autoconf >= 2.53
Requires(post):	fileutils
Requires(post):	grep
Requires(post):	sed
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		homedir		/home/services/petidomo
%define		cgidir		/home/services/httpd/cgi-bin

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

Uwaga: zarz±dca CGI obdarzony jest SUID-em root.

%prep
%setup -q -n %{name}-src -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__autoconf}
%configure

%{__make} CFLAGS+="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{cgidir}
# 751 petidomo petidomo
install -d $RPM_BUILD_ROOT%{homedir}/bin
# 750 petidomo petidomo
install -d $RPM_BUILD_ROOT%{homedir}/{etc,lists}
# 770 petidomo petidomo
install -d $RPM_BUILD_ROOT%{homedir}/crash
# 6111 petidomo petidomo
install src/petidomo/petidomo $RPM_BUILD_ROOT%{homedir}/bin
# 750 petidomo petidomo
install scripts/InsertNameInSubject.sh $RPM_BUILD_ROOT%{homedir}/bin
install scripts/rfc2369.sh $RPM_BUILD_ROOT%{homedir}/bin
# 750 petidomo petidomo
install scripts/pgp-encrypt.sh $RPM_BUILD_ROOT%{homedir}/bin
install scripts/pgp-decrypt.sh $RPM_BUILD_ROOT%{homedir}/bin
# 755 petidomo petidomo
install scripts/send-pr $RPM_BUILD_ROOT%{homedir}/bin
# 660 petidomo petidomo
install %{SOURCE2} $RPM_BUILD_ROOT%{homedir}/etc/help
install etc/masteracl $RPM_BUILD_ROOT%{homedir}/etc/acl
sed -e "s#@MTA@#/usr/lib/sendmail#" etc/masterconfig \
	>$RPM_BUILD_ROOT%{homedir}/etc/petidomo.conf
# 6111 root petidomo
install src/htmlconf/htmlconf \
	$RPM_BUILD_ROOT%{cgidir}/petidomoconf
# doc
install %{SOURCE3} .

ln -sf petidomo	$RPM_BUILD_ROOT%{homedir}/bin/listserv
ln -sf petidomo  $RPM_BUILD_ROOT%{homedir}/bin/hermes

touch $RPM_BUILD_ROOT%{homedir}/.nofinger

%clean
rm -rf $RPM_BUILD_ROOT

%post
mv -f %{homedir}/etc/petidomo.conf %{homedir}/etc/petidomo.conf.new
sed -e "s#@HOSTNAME@#`hostname --fqdn`#" %{homedir}/etc/petidomo.conf.new \
	> %{homedir}/etc/petidomo.conf
rm -f %{homedir}/etc/petidomo.conf.new
chown -f petidomo:petidomo %{homedir}/etc/petidomo.conf
chmod -f 660 %{homedir}/etc/petidomo.conf

if ! grep -q ^petidomo /etc/mail/aliases; then
echo "#" 				>> /etc/mail/aliases
echo "# Mailing List Stuff"		>> /etc/mail/aliases
echo "#"				>> /etc/mail/aliases
echo "petidomo-manager:postmaster"	>> /etc/mail/aliases
echo "petidomo:\"|%{homedir}/bin/listserv\"" >> /etc/mail/aliases
/usr/bin/newaliases
fi

%files
%defattr(644,root,root,755)
%doc petidomo-manual-html README COPYRIGHT etc/ChangeLog etc/mail2news.c
%doc scripts/list2news scripts/aliases4qmail.sh etc/listconfig commercial.txt

%attr(751,root,root) %dir %{homedir}
%attr(751,root,petidomo) %dir %{homedir}/bin
%attr(750,root,petidomo) %dir %{homedir}/etc
%attr(770,root,petidomo) %dir %{homedir}/lists
%attr(770,root,petidomo) %dir %{homedir}/crash

%attr(6755,root,petidomo) %{homedir}/bin/petidomo
%attr(6755,root,petidomo) %{homedir}/bin/listserv
%attr(6755,root,petidomo) %{homedir}/bin/hermes

%attr(750,root,petidomo) %{homedir}/bin/InsertNameInSubject.sh
%attr(750,root,petidomo) %{homedir}/bin/rfc2369.sh
%attr(750,root,petidomo) %{homedir}/bin/pgp-encrypt.sh
%attr(750,root,petidomo) %{homedir}/bin/pgp-decrypt.sh
%attr(755,root,petidomo) %{homedir}/bin/send-pr

%attr(660,root,petidomo) %config(noreplace) %verify(not size mtime md5) %{homedir}/etc/*

%attr(644,root,petidomo) %{homedir}/.nofinger

%files cgimanager
%defattr(644,root,root,755)
%attr(6755,root,petidomo) %{cgidir}/petidomoconf
