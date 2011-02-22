Summary:	Script to load automatically IPMI kernel drivers
Name:		ipmi-init
Version:	0.1
Release:	3
License:	BSD
Group:		Applications/System
Source0:	ipmi.init
Source1:	ipmi.sysconfig
URL:		http://en.wikipedia.org/wiki/IPMI
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Conflicts:	ipmitool < 1.8.11-9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Script to load IPMI (Intelligent Platform Management Interface) device
drivers on boot and adjusts /dev notes accordingly if needed.

%prep
%setup -qcT

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}
install -p %{SOURCE0} $RPM_BUILD_ROOT/etc/rc.d/init.d/ipmi
cp -a %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/ipmi

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ipmi
# NOTE: we do not restart ipmi on upgrade

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del ipmi
	# NOTE: ipmi stop doesn't do anything
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ipmi
%attr(754,root,root) /etc/rc.d/init.d/ipmi
