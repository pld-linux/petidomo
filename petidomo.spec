# TODO
# - build ;)
# - there is no petidomo user/group (anywhere)
# - move to /var/lib and /etc (FHS)
%define		_beta	b6
%define		_rel	0.1
Summary:	Easy-to-use, easy-to-install mailing list server
Summary(pl.UTF-8):	Łatwy w użyciu oraz instalacji serwer list pocztowych
Name:		petidomo
Version:	4.0
Release:	%{_beta}.%{_rel}
License:	Free for non-commercial use
Group:		Applications/Mail
Source0:	ftp://ftp.ossp.org/pkg/tool/petidomo/%{name}-%{version}%{_beta}.tar.gz
# Source0-md5:	968f4ca0a0b97acc2e095090ba31afcc
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
Requires(post):	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		homedir		/home/services/petidomo
%define		cgidir		/home/services/httpd/cgi-bin

%description
Petidomo Mailing List Manager.

%description -l pl.UTF-8
Petidomo Mailing List Manager - zarządca pocztowych list
dyskusyjnych.

%package cgimanager
Summary:	CGI Manager for Petidomo
Summary(pl.UTF-8):	Program CGI do zarządzania serwerem Petidomo
Group:		Applications/Mail
Requires:	%{name} = %{version}-%{release}

%description cgimanager
CGI program, that lets you do all the configuration out of your
favourite WWW-Browser.

Warning: cgi manager is SUID root!

%description cgimanager -l pl.UTF-8
Program CGI pozwalający na konfigurację serwera Petidomo poprzez
ulubioną przeglądarkę WWW.

Uwaga: zarządca CGI obdarzony jest SUID-em root.

%prep
%setup -q -n %{name}-%{version}%{_beta} -a1
#%%patch0 -p1
#%%patch1 -p1
#%%patch2 -p1

%build
%{__autoconf}
%configure
%{__make} \
	CFLAGS+="%{rpmcflags}"

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
sed -i -e "s#@HOSTNAME@#`hostname --fqdn`#" %{homedir}/etc/petidomo.conf

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

%attr(660,root,petidomo) %config(noreplace) %verify(not md5 mtime size) %{homedir}/etc/*

%attr(644,root,petidomo) %{homedir}/.nofinger

%files cgimanager
%defattr(644,root,root,755)
%attr(6755,root,petidomo) %{cgidir}/petidomoconf
