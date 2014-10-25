%define	ver	0.1.2
%define	subver	hp11
Summary:	Primecoin - First Scientific Computing Cryptocurrency
Name:		primecoin-hp
Version:	%{ver}.%{subver}
Release:	4
License:	MIT/X11
Group:		X11/Applications
Source0:	http://downloads.sourceforge.net/primecoin-hp/%{ver}-%{subver}/primecoin-%{ver}-%{subver}.tar.bz2
# Source0-md5:	7d17123d62fe4ef6205da4775e5a3228
Patch0:		build-i486.patch
URL:		http://primecoin.org
BuildRequires:	QtCore-devel
BuildRequires:	QtDBus-devel
BuildRequires:	QtGui-devel
BuildRequires:	boost-devel
BuildRequires:	db-cxx-devel
BuildRequires:	miniupnpc-devel >= 1.5
BuildRequires:	openssl-devel
BuildRequires:	qrencode-devel
BuildRequires:	qt4-qmake
Requires:	perl-base
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Primecoin - First Scientific Computing Cryptocurrency.

%package qt
Summary:	Qt-based Primecoin Wallet
Group:		X11/Applications

%description qt
Qt-based Primecoin Wallet.

%prep
%setup -q -n primecoin-%{ver}-%{subver}
%patch0 -p1

%build
qmake-qt4 \
	USE_UPNP=1 \
	USE_DBUS=1 \
	USE_QRCODE=1 \
	bitcoin-qt.pro

%{__make}

%{__make} -C src -f makefile.unix \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcflags} %{rpmcxxflags} %{rpmcppflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name},%{_mandir}/man{1,5},%{_localedir},%{_desktopdir},%{_pixmapsdir},%{_datadir}/kde4/services}

install src/primecoind $RPM_BUILD_ROOT%{_libdir}/%{name}/primecoind
ln -s %{_libdir}/%{name}/primecoind $RPM_BUILD_ROOT%{_bindir}/primecoind
#sed -e 's#/usr/lib/#%{_libdir}/#g' -e 's#bitcoin#primecoin#g' contrib/debian/bin/bitcoind > $RPM_BUILD_ROOT%{_bindir}/primecoind
#chmod 755 $RPM_BUILD_ROOT%{_bindir}/primecoind

install primecoin-qt $RPM_BUILD_ROOT%{_bindir}
sed -e 's#bitcoin#primecoin#g' contrib/debian/bitcoin-qt.desktop > $RPM_BUILD_ROOT%{_desktopdir}/primecoin-qt.desktop
sed -e 's#bitcoin#primecoin#g' contrib/debian/bitcoin-qt.protocol > $RPM_BUILD_ROOT%{_datadir}/kde4/services/primecoin-qt.protocol

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*.txt contrib/debian/examples/bitcoin.conf
%attr(755,root,root) %{_bindir}/primecoind
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/primecoind

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/primecoin-qt
%{_datadir}/kde4/services/primecoin-qt.protocol
%{_desktopdir}/primecoin-qt.desktop
