# EA4 Passenger

## Target Audiences

1. Maintenance and security teams
2. Training and technical support
3. Managers and other internal key stakeholders
4. Future project/feature owners/maintainers

## Detailed Summary

Initially, EA4’s passeger support was tied to ruby versions.

That was becoming unwieldy and is in fact not neccessary.

## Overall Intent

### Clarification

It is confusing to have Apache’s mod passenger named under `ea-ruby24` and `ea-ruby27`.

It is confusing to need to require an Apache module in order for NGINX to build.

### Simplify how we do passenger to make maintenance and support easier

1. Passenger itself can be tracked in one spot: `ea-passenger-src`
   * Anything needing it, like `BuildRequires` for Apache and NGINX, can get it from the same place.
2. Runtime files shared between consumers, like `Requires` for Apache and NGINX, are in `ea-passenger-runtime`.
3. Then the actual use of it can be in the thing’s package. e.g.:
   * ea-apache24-mod-passenger (for .so, conf to load the .so, and templates for ULC to generate Apache configs from)
   * ea-nginx (mod passenger is compiled in and it generates the config it needs)

This means we have one spot to keep passenger up to date instead of multiple or a single spot whose name seems out of place.

This also allows for future things like ea-apache42 or ea-whatever to have its own separate passenger thing while still sharing the common stuff with everything else.

### Do not provide ruby via EA4

Maintaining ruby (multiple rubies in fact) is a lot of work and gets more and more difficult as time goes by and OS support changes.

It turns out there is no need to do so: passenger does not care about the ruby versions.

> Once installed, you can run Passenger's Ruby parts under any Ruby interpreter you want, even if that Ruby interpreter was not the one you originally installed Passenger with.
>
> The reason for this is that Passenger does not dynamically link to Ruby: Passenger uses Ruby entirely out-of-process. Thus you can switch to any Ruby interpreter you want during runtime, without recompiling Passenger, and without worrying about what Ruby you used to install Passenger.
>
> Passenger is also capable of running Ruby web applications under any Ruby interpreter you want. So it is not important which Ruby you use to install Passenger: it will work regardless.
>
>  — https://www.phusionpassenger.com/library/indepth/ruby/multiple_rubies.html

In other words:

* Passenger itself only cares about the ruby path it is configured to use. What ruby was used to build it is irrelevant at runtime.
* Ruby applications only care about the ruby path each is configured to use.

This also means that we could have `ea-apache24-mod-passenger` properly `Obsoletes` the `ea-ruby*-passenger`s if we can get it to build on all OSs (ATM C8 is really difficult). As it stands at the time of this writing they will all conflict at least.

## Maintainability

This will make automated updates possible because we no longer have to update the same thing in more than one spot.

## Options/Decisions

1. Keep doing the multiple `ea-ruby*` approach and continue covering the expense of the ever increasing complexity.
2. Drop `ea-ruby*` and do it as outlined above and save the expenses by making it simple in a way that never needs increaed complexity.

# Child Documents

None.
