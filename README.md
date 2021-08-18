# What this package is for

This package is intended for things that need passenger source code like, `ea-apache24-mod-passenger` and `ea-nginx`.

This passenger will use the system ruby. As always an application can use whatever ruby it wants to (or even non-ruby), regardless of what ruby passenger is using.

For more details see the [Design Doc](DESIGN.md).

# How to use this package

1. Add this to the SPEC file: `BuildRequires: ea-passenger-src`
2. In the `%build` section of the SPEC file copy the source to the package’s build directory:
   * `cp -rf /opt/cpanel/ea-passenger-src/passenger-*/ %{buildroot}/_passenger_source_code`
3. Use `%{buildroot}/_passenger_source_code` to configure and build the thing.
4. See “ea-passenger-runtime” below for another important part of this process.

## ea-passenger-runtime

If you are using `ea-passenger-src` to compile passenger support in a package, that package will also need the shared runtime files.

To accomplish this add this to that packages’s part of the SPEC file:

`Requires: ea-passenger-runtime`
