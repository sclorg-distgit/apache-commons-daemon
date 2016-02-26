%global pkg_name apache-commons-daemon
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}


%global base_name   daemon
%global short_name  commons-%{base_name}

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.0.13
Release:        6.14%{?dist}
Summary:        Defines API to support an alternative invocation mechanism
License:        ASL 2.0
URL:            http://commons.apache.org/%{base_name}
Source0:        http://archive.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Patch0:         0001-execve-path-warning.patch
Patch1:         apache-commons-daemon-JAVA_OS.patch
Patch2:         apache-commons-daemon-s390x.patch
Patch3:         apache-commons-daemon-ppc64.patch
Patch4:         apache-commons-daemon-aarch64.patch
BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix_java_common}javapackages-tools
BuildRequires:  %{?scl_prefix}apache-commons-parent >= 26-7
BuildRequires:  %{?scl_prefix}maven-surefire-provider-junit
BuildRequires:  xmlto




%description
The scope of this package is to define an API in line with the current
Java Platform APIs to support an alternative invocation mechanism
which could be used instead of the public static void main(String[])
method.  This specification covers the behavior and life cycle of what
we define as Java daemons, or, in other words, non interactive
Java applications.

%package        jsvc
Summary:        Java daemon launcher
Requires:       %{?scl_prefix}runtime


%description    jsvc
%{summary}.

%package        javadoc
Summary:        API documentation for %{pkg_name}
BuildArch:      noarch


%description    javadoc
%{summary}.


%prep
%setup -q -n %{short_name}-%{version}-src
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%patch0 -p1 -b .execve
%patch1 -p1 -b .java_os
%patch2 -p1 -b .s390x
%patch3 -p1 -b .ppc64
%patch4 -p1 -b .aarch64

# remove java binaries from sources
rm -rf src/samples/build/

chmod 644 src/samples/*
cd src/native/unix
xmlto man man/jsvc.1.xml
%{?scl:EOF}


%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x

. /opt/rh/rh-java-common/root/usr/share/java-utils/java-functions
set_jvm
export JAVA_HOME

# build native jsvc
pushd src/native/unix
%configure --with-java=${JAVA_HOME}
# this is here because 1.0.2 archive contains old *.o
make clean
make %{?_smp_mflags}
popd

# build jars
%mvn_file  : %{short_name} %{pkg_name}
%mvn_alias : org.apache.commons:%{short_name}
%mvn_build
%{?scl:EOF}


%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# install native jsvc
install -Dpm 755 src/native/unix/jsvc $RPM_BUILD_ROOT%{_bindir}/jsvc
install -Dpm 644 src/native/unix/jsvc.1 $RPM_BUILD_ROOT%{_mandir}/man1/jsvc.1

%mvn_install
%{?scl:EOF}


%files -f .mfiles
%doc LICENSE.txt PROPOSAL.html NOTICE.txt RELEASE-NOTES.txt src/samples
%doc src/docs/*


%files jsvc
%doc LICENSE.txt NOTICE.txt
%{_bindir}/jsvc
%{_mandir}/man1/jsvc.1*


%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt


%changelog
* Mon Feb 08 2016 Michal Srb <msrb@redhat.com> - 1.0.13-6.14
- Fix BR on maven-local & co.

* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 1.0.13-6.13
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 1.0.13-6.12
- maven33 rebuild

* Wed Jun 10 2015 Michal Srb <msrb@redhat.com> - 1.0.13-6.11
- Build for ppc64

* Wed Jan 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.13-6.10
- Add requires on SCL filesystem package

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1.0.13-6.9
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 1.0.13-6.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.13-6.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.13-6.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.13-6.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.13-6.4
- Remove requires on java

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.13-6.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.13-6.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.13-6.1
- First maven30 software collection build

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.0.13-6
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0.13-5
- Mass rebuild 2013-12-27

* Mon Nov 11 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.13-4
- Add aarch64 support patch
- Resolves: rhbz#1028109

* Fri Sep 20 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.13-3
- Add BuildRequires on apache-commons-parent >= 26-7

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.13-2
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Feb 13 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.13-1
- Update to upstream version 1.0.13

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.12-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 24 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.12-1
- Update to upstream version 1.0.12
- Install NOTICE files

* Tue Jan 15 2013 Michal Srb <msrb@redhat.com> - 1.0.11-2
- Build with xmvn
- Spec file cleanup

* Tue Dec 11 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.11-1
- Update to upstream version 1.0.11

* Fri Aug 17 2012 Karsten Hopp <karsten@redhat.com> 1.0.10-5
- add ppc64 as known arch

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Dan Horák <dan[at]danny.cz> - 1.0.10-3
- add s390x as known arch

* Thu Mar 29 2012 Dennis Gilmore <dennis@ausil.us> - 1.0.10-2
- $supported_os and $JAVA_OS in configure do not always match 
- on arches that override supported_os to be the arch we can not find headers

* Thu Jan 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.10-1
- Update to latest upstream (1.0.10)
- Several bugfixes concerning libcap and building upstream

* Thu Jan 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.8-1
- Update to latest upstream (1.0.8)
- Drop s390/ppc patches (upstream seems to already include them)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 15 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.7-1
- Update to latest upstream (1.0.7)
- Fix CVE-2011-2729

* Wed Jul 20 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.6-1
- Update to latest upstream (1.0.6)
- Cleanups according to new guidelines

* Mon May  9 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.5-5
- Use mvn-rpmbuild instead of mvn-local (changes in maven)

* Wed May  4 2011 Dan Horák <dan[at]danny.cz> - 1.0.5-4
- updated the s390x patch

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.5-2
- Fix bug 669259 (execve warning segfault)

* Tue Jan 18 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.5-1
- Update to latest version
- Use maven 3 to build
- Versionless jars & javadocs
- Use apache-commons-parent for BR

* Tue Oct 26 2010 Chris Spike <chris.spike@arcor.de> 1.0.4-2
- Added fix to remove java binaries from sources

* Tue Oct 26 2010 Chris Spike <chris.spike@arcor.de> 1.0.4-1
- Updated to 1.0.4

* Fri Oct 22 2010 Chris Spike <chris.spike@arcor.de> 1.0.3-1
- Updated to 1.0.3
- Cleaned up BRs

* Thu Jul  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.2-4
- Add license to javadoc subpackage

* Fri Jun  4 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.2-3
- Make javadoc subpackage noarch

* Tue Jun  1 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.2-2
- Fix add_to_maven_depmap call
- Added depmap for old groupId
- Unified use of `install`

* Wed May 12 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0.2-1
- Rename and rebase to apache-commons-daemon
- Get rid of gcj, native conditional compilation
- Build with maven
- Update patches to cleanly apply on new version, remove unneeded
- Clean up whole spec

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.1-8.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 03 2009 Karsten Hopp <karsten@redhat.com> 1.0.1-7.8
- ppc needs a similar patch

* Tue Mar 03 2009 Karsten Hopp <karsten@redhat.com> 1.0.1-7.7
- add configure patch for s390x

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.1-7.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:1.0.1-6.6
- drop repotag

* Fri Feb 08 2008 Permaine Cheung <pcheung@redhat.com> - 1:1.0.1-6jpp.5
- Add configure patch for ia64 from Doug Chapman

* Mon Sep 24 2007 Permaine Cheung <pcheung@redhat.com> - 1:1.0.1-6jpp.4
- Add execve path warning patch from James Ralston
