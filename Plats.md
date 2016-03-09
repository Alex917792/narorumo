# What is plats? #
plats helps you localize your client-side webapp. All you have to do is include a script in your page, and you'll get information about the user's language preferences -- which is usually hard to get from javascript.

If you tell plats it which locales your application supports, it tells you which of those locales your user would prefer.

"plats" is Swedish for "locale" or "place".

## You shouldn't use plats unless you trust Alex ##
Seriously, don't let random dudes and ladies run their javascript all up in your context. Just go get the source [here](http://narorumo.googlecode.com/svn/trunk/plats). It's very simple; you can adapt it for your own use.

## If you're a GWT app ##
GWT applications can set their locale with a [special meta tag](http://code.google.com/docreader/#p=google-web-toolkit-doc-1-5&s=google-web-toolkit-doc-1-5&t=DevGuideSpecifyingLocale) -- you can use plats to set yours, automatically.

In your containing HTML's head tag, go like this, before you load your GWT selection script (the ".nocache.js" file):

```
...
  <head>
    <script src="http://plats.appspot.com/set_metatag.js?available=en,es,lt,it">
    </script>
  </head>
```

NB: This is assuming your application is localized for English, Spanish, Lithuanian and Italian. Modify the `available` parameter for the locales you support.

## If you just want some JavaScript variables ##
plats can do that too. Go like this:
```
...
  <head>
    <script src="http://plats.appspot.com/put_variable.js?available=fr,jp">
    </script>
  </head>
```
You'll get two variables set on your `window` object: `window.plats_best_locale` and `window.plats_ordered_locales`. The latter of these is the list of all locales that the user would like, even if you don't support them.

## Tell me more! ##
So web users can configure which languages they prefer for content, and this information is sent in HTTP requests to web servers as the [Accept-Language](http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html) header. Strangely, this information doesn't seem accessible from javascript.

## Issues ##
plats isn't perfect yet. There's a mismatch between locale codes and the language codes as sent by `Accept-Language`; if you get more specific than just a language code, things probably won't match up; there are underbars in locale codes and dashes in the Accept-Language header. Also I need to do more research about capitalization...