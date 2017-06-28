// Chinforinfula Firefox settings
// 20170627

pref("browser.search.suggest.enabled", false);
pref("browser.urlbar.clickSelectsAll", false);
pref("browser.urlbar.doubleClickSelectsAll", true);
pref("browser.urlbar.trimURLs", false);
pref("general.autoScroll", false);
pref("general.smoothScroll", false);
pref("layout.spellcheckDefault", 0);
pref("media.autoplay.enabled", false);
pref("middlemouse.contentLoadURL", false);

// Don't show 'know your rights' on first run
pref("browser.rights.3.shown", true);

// Don't show WhatsNew on first run after every update
pref("browser.startup.homepage_override.mstone","ignore");

// Disable the internal PDF viewer
pref("pdfjs.disabled", true);

// No Pocket here
pref("browser.pocket.enabled", false);
pref("browser.pocket.api", "");
pref("browser.pocket.site", "");
pref("browser.pocket.oAuthConsumerKey", "");
pref("browser.pocket.useLocaleList", false);
pref("browser.pocket.enabledLocales", "");

// No DRM too
pref("browser.eme.ui.enabled", false);
pref("media.eme.enabled", false);
pref("media.eme.apiVisible", false);

// No blobs
pref("media.gmp-gmpopenh264.provider.enabled",false);
pref("media.gmp-gmpopenh264.autoupdate",false);
pref("media.gmp-gmpopenh264.enabled",false);
pref("media.gmp-manager.url","http://127.0.0.1/");
pref("media.gmp-manager.url.override", "data:text/plain,");
pref("media.gmp-provider.enabled",false);

// No ads downloads
pref("browser.newtabpage.directory.source","");
pref("browser.newtabpage.enabled", false);
pref("browser.newtabpage.enhanced", false);
pref("browser.newtabpage.directory.ping", "");
pref("browser.newtabpage.introShown", true);

// Disable home snippets
pref("browser.aboutHomeSnippets.updateUrl", "data:text/html");

// Disable plugin installer
pref("plugins.hide_infobar_for_missing_plugin", true);
pref("plugins.hide_infobar_for_outdated_plugin", true);
pref("plugins.notifyMissingFlash", false);

// Enable tracking protection
pref("privacy.trackingprotection.enabled", true);

// Disable datareporting and telemetry
pref("datareporting.healthreport.dataSubmissionEnabled", false);
pref("datareporting.healthreport.uploadEnabled", false);
pref("toolkit.telemetry.enabled", false);

// Disable Safe Browsing service
//pref("browser.safebrowsing.malware.enabled", false);
//pref("browser.safebrowsing.phishing.enabled", false);
//pref("browser.safebrowsing.downloads.enabled", false);
//pref("services.sync.prefs.sync.browser.safebrowsing.enabled", false);
//pref("services.sync.prefs.sync.browser.safebrowsing.malware.enabled", false);

// Disable battery api
pref("dom.battery.enabled", false);

// Disable geolocation
//pref("geo.enabled", false);

// Disable WebGL
//pref("webgl.disabled", false);

// Disable WebRTC
//pref("media.peerconnection.enabled", false);

// Prevent websites from getting local IP from WebRTC
pref("media.peerconnection.ice.default_address_only", true);

