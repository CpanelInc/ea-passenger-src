Summary: Phusion Passenger application server Source Code
Name: ea-passenger-src

# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4590 for more details
%define release_prefix 1

Version: 6.1.1
Release: %{release_prefix}%{?dist}.cpanel
Group: System Environment/Daemons
# Passenger code uses MIT license.
# Bundled(Boost) uses Boost Software License
# BCrypt and Blowfish files use BSD license.
# Documentation is CC-BY-SA
# See: https://bugzilla.redhat.com/show_bug.cgi?id=470696#c146
License: Boost and BSD and BSD with advertising and MIT and zlib
URL: https://www.phusionpassenger.com

Source0: release-%{version}.tar.gz
Source1: cxxcodebuilder.tar.gz

AutoReqProv: no

# httpd on RHEL7 is using private /tmp. This break passenger status.
# We workaround that by using "/var/run/ea-ruby27-passenger" instead of "/tmp".
Patch0:         0001-Avoid-using-tmp-for-the-TMPDIR.patch
# Supress logging of empty messages
Patch1:         0002-Suppress-logging-of-empty-messages.patch
# Add a new directive to Passenger that will allow us to disallow
## Passenger directives in .htaccess files
Patch2:         0003-Add-new-PassengerDisableHtaccess-directive.patch

Patch3:         0004-Fix-AlmaLinux-10-build-add-host-flag-support-for-lib.patch

%description
Phusion Passenger(r) is a web server and application server, designed to be fast,
robust and lightweight. It takes a lot of complexity out of deploying web apps,
adds powerful enterprise-grade features that are useful in production,
and makes administration much easier and less complex. It supports Ruby,
Python, Node.js and Meteor.

%prep
%setup -n passenger-release-%{version}

%patch0 -p1 -b .tmpdir
%patch1 -p1 -b .emptymsglog
%patch2 -p1 -b .disablehtaccess

%if 0%{?rhel} >= 10
%patch3 -p1 -b .hostflagsupport
# Package consuming this src ball will need:
# %if 0%{?rhel} >= 10
# export LIBEV_CONFIGURE_HOST=x86_64-redhat-linux-gnu
# %endif
%endif

%build

mkdir -p build/support/vendor/cxxcodebuilder/
tar xzf %{SOURCE1} \
    --strip-components=1 \
    -C build/support/vendor/cxxcodebuilder/

# Find files with a hash-bang that do not have executable permissions
for script in `find . -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $script | grep \"^#!/\"`" ] && chmod -v 755 $script
    /bin/true
done

# C8 barfs without this but do it for everyone for consisteny, C6 might not get it but everything else should
perl -pi -e 's{#!/usr/bin/env python}{#!/usr/bin/python3}' \
    src/cxx_supportlib/vendor-copy/libuv/gyp_uv.py

# since we rely on the system ruby there is no need to run
#   update_ruby_shebang.pl in %{buildroot}/opt/cpanel/ea-passenger-src

%install

if [ "$0" == "debian/override_dh_auto_install.sh" ]; then
    mkdir -p opt/cpanel/ea-passenger-src/passenger-release-%{version}
    find . ! -name . -prune ! -name opt ! -name debian -exec mv {} opt/cpanel/ea-passenger-src/passenger-release-%{version} \;
else
    mkdir -p %{buildroot}/opt/cpanel/ea-passenger-src/passenger-release-%{version}
    cp -rf ./* %{buildroot}/opt/cpanel/ea-passenger-src/passenger-release-%{version}
fi

%files
/opt/cpanel/ea-passenger-src/

%changelog
* Tue Dec 23 2025 Cory McIntire <cory.mcintire@webpros.com> - 6.1.1-1
- EA-13306: Update ea-passenger-src from v6.1.0 to v6.1.1

* Thu Dec 11 2025 Dan Muey <daniel.muey@webpros.com> - 6.1.0-2
- EA4-223: Move A10 host-flag-support from Apache module that uses this src ball (that way NGINX benefits form it too w/out duplicating efforts)

* Tue Sep 23 2025 Dan Muey <daniel.muey@webpros.com> - 6.1.0-1
- EA-13128: Update ea-passenger-src from v6.0.27 to v6.1.0

* Fri Apr 04 2025 Cory McIntire <cory.mcintire@webpros.com> - 6.0.27-1
- EA-12801: Update ea-passenger-src from v6.0.26 to v6.0.27

* Wed Feb 19 2025 Cory McIntire <cory.mcintire@webpros.com> - 6.0.26-1
- EA-12725: Update ea-passenger-src from v6.0.25 to v6.0.26
  * [CVE-2025-26803] The http parser (from Passenger 6.0.21-6.0.25) was susceptible to a denial of service attack when parsing a request with an invalid HTTP method.

* Wed Feb 12 2025 Cory McIntire <cory.mcintire@webpros.com> - 6.0.25-1
- EA-12705: Update ea-passenger-src from v6.0.24 to v6.0.25

* Wed Feb 05 2025 Cory McIntire <cory.mcintire@webpros.com> - 6.0.24-1
- EA-12681: Update ea-passenger-src from v6.0.23 to v6.0.24

* Thu Aug 01 2024 Cory McIntire <cory@cpanel.net> - 6.0.23-1
- EA-12307: Update ea-passenger-src from v6.0.22 to v6.0.23

* Sat May 18 2024 Cory McIntire <cory@cpanel.net> - 6.0.22-1
- EA-12161: Update ea-passenger-src from v6.0.20 to v6.0.22

* Mon Jan 22 2024 Cory McIntire <cory@cpanel.net> - 6.0.20-1
- EA-11926: Update ea-passenger-src from v6.0.19 to v6.0.20

* Wed Nov 29 2023 Cory McIntire <cory@cpanel.net> - 6.0.19-1
- EA-11827: Update ea-passenger-src from v6.0.18 to v6.0.19

* Thu Jun 15 2023 Cory McIntire <cory@cpanel.net> - 6.0.18-1
- EA-11497: Update ea-passenger-src from v6.0.17 to v6.0.18

* Mon May 08 2023 Julian Brown <julian.brown@cpanel.net> - 6.0.17-2
- ZC-10936: Clean up Makefile and remove debug-package-nil

* Sun Jan 29 2023 Cory McIntire <cory@cpanel.net> - 6.0.17-1
- EA-11187: Update ea-passenger-src from v6.0.16 to v6.0.17

* Wed Dec 21 2022 Cory McIntire <cory@cpanel.net> - 6.0.16-1
- EA-11116: Update ea-passenger-src from v6.0.15 to v6.0.16

* Wed Sep 21 2022 Cory McIntire <cory@cpanel.net> - 6.0.15-1
- EA-10945: Update ea-passenger-src from v6.0.14 to v6.0.15

* Wed May 11 2022 Cory McIntire <cory@cpanel.net> - 6.0.14-1
- EA-10700: Update ea-passenger-src from v6.0.13 to v6.0.14

* Mon Apr 18 2022 Cory McIntire <cory@cpanel.net> - 6.0.13-1
- EA-10642: Update ea-passenger-src from v6.0.10 to v6.0.13

* Thu Aug 12 2021 Dan Muey <dan@cpanel.net> - 6.0.10-1
- ZC-9200: Initial version
