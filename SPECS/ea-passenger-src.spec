Summary: Phusion Passenger application server Source Code
Name: ea-passenger-src

# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4590 for more details
%define release_prefix 1

Version: 6.0.10
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

%description
Phusion Passenger(r) is a web server and application server, designed to be fast,
robust and lightweight. It takes a lot of complexity out of deploying web apps,
adds powerful enterprise-grade features that are useful in production,
and makes administration much easier and less complex. It supports Ruby,
Python, Node.js and Meteor.

%install

mkdir -p %{buildroot}/opt/cpanel/ea-passenger-src
tar xzf %{SOURCE0} -C %{buildroot}/opt/cpanel/ea-passenger-src/

# ^^^ tar creates ./passenger-release-%{version}/
tar xzf %{SOURCE1} \
    --strip-components=1 \
    -C %{buildroot}/opt/cpanel/ea-passenger-src/passenger-release-%{version}/build/support/vendor/cxxcodebuilder/

# since we rely on the system ruby there is no need to run
#   update_ruby_shebang.pl in %{buildroot}/opt/cpanel/ea-passenger-src

# C8 barfs without this but do it for everyone for consisteny, C6 might not get it but everything else should
perl -pi -e 's{#!/usr/bin/env python}{/usr/bin/python3}' \
    %{buildroot}/opt/cpanel/ea-passenger-src/passenger-release-%{version}/src/cxx_supportlib/vendor-copy/libuv/gyp_uv.py

%files
/opt/cpanel/ea-passenger-src/

%changelog
* Thu Aug 12 2021 Dan Muey <dan@cpanel.net> - 6.0.10-1
- ZC-9200: Initial version
