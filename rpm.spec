Name: udplogger
Version: 0
Release: 1

Summary: UDP Logger for stage machines
Group: Applications/ZIM
Requires: cleanpython26
Requires: sbo
BuildRequires: cleanpython26
%define python /opt/cleanpython26/bin/python

##########################################################################
# Lines below this point normally shouldn't change

%define source %{name}-%{version}

Vendor: Zope Corporation
Packager: Zope Corporation <sales@zope.com>
License: ZPL
AutoReqProv: no
Source: %{source}.tgz
Prefix: /opt
BuildRoot: /tmp/%{name}

%description
%{summary}

%prep
%setup -n %{source}

%build
rm -rf %{buildroot}
mkdir %{buildroot} %{buildroot}/opt
cp -r $RPM_BUILD_DIR/%{source} %{buildroot}/opt/%{name}
%{python} %{buildroot}/opt/%{name}/install.py bootstrap
%{python} %{buildroot}/opt/%{name}/install.py buildout:extensions=
%{python} -m compileall -q -f -d /opt/%{name}/eggs  \
   %{buildroot}/opt/%{name}/eggs \
   > /dev/null 2>&1 || true
rm -rf %{buildroot}/opt/%{name}/release-distributions

# Gaaaa! buildout doesn't handle relative paths in egg links. :(
sed -i s-/tmp/zc.%{name}-- \
   %{buildroot}/opt/%{name}/develop-eggs/zc.%{name}.egg-link 
%clean
rm -rf %{buildroot}
rm -rf $RPM_BUILD_DIR/%{source}

%pre
rm -rf /opt/%{name}/eggs/setuptools*

%posttrans
if [[ ! -d /etc/%{name} ]]
then
   mkdir /etc/%{name}
fi

echo "
[buildout]
parts = rc agent.cfg

[deployment]
recipe = zc.recipe.deployment
name = stage-zim-events-and-metrics
user = root

[rc]
recipe = zc.recipe.rhrc
deployment = deployment
parts = agent
process-management = true
chkconfig = 345 90 10

[udplogger]
recipe = zc.zdaemonrecipe
deployment = deployment
program = \${buildout:bin-directory}/udplogger localhost:4515
zdaemon.conf =
  <runner>
    logfile \${deployment:log-directory}/zimagent.log
  </runner>

[udplogger.cfg]
recipe = zc.recipe.deployment:configuration
text = 
  \${deployment:log-directory}/zimagent.log {
    rotate 5
    daily
    compress
    postrotate
      \${deployment:rc-directory} \
          -C \${deployment:rc-directory}/udplogger-zdaemon.conf \
          reopen_transcript
    endscript
  }

" > /etc/%{name}/%{name}.cfg

/usr/local/bin/sbo

%preun
/usr/local/bin/sbo -u %{name}
rm -rf /etc/%{name}


%files
%defattr(-, root, root)
/opt/%{name}
