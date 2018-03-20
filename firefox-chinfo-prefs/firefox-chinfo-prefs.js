// Chinforinfula Firefox settings
// 20180315

pref("browser.bookmarks.showRecentlyBookmarked", false);
pref("browser.ctrlTab.previews", false);
pref("browser.fixup.alternate.enabled", false);
pref("browser.fixup.hide_user_pass", true);
pref("browser.link.open_newwindow.restriction", 0);
pref("browser.search.openintab", true);
pref("browser.search.suggest.enabled", false);
pref("browser.tabs.closeWindowWithLastTab", false);
pref("browser.tabs.insertRelatedAfterCurrent", true);
pref("browser.urlbar.clickSelectsAll", false);
pref("browser.urlbar.doubleClickSelectsAll", true);
pref("browser.urlbar.oneOffSearches", false);
pref("browser.urlbar.trimURLs", false);
pref("extensions.getAddons.showPane", false);
pref("general.autoScroll", false);
pref("general.smoothScroll", false);
pref("keyword.enabled", false);
pref("layout.spellcheckDefault", 0);
pref("media.autoplay.enabled", false);
pref("middlemouse.contentLoadURL", false);
pref("toolkit.cosmeticAnimations.enabled", false);

// Enable Containers 
// pref("privacy.userContext.enabled", true);

// Don't show 'know your rights' on first run
pref("browser.rights.3.shown", true);

// Don't show WhatsNew on first run after every update
pref("browser.startup.homepage_override.mstone","ignore");

// Enforce default permissions to blocked
pref("permissions.default.camera", 2);
pref("permissions.default.desktop-notification", 2);
pref("permissions.default.geo", 2);
pref("permissions.default.microphone", 2);

// Disable the internal PDF viewer
pref("pdfjs.disabled", true);

// No Pocket here
pref("browser.pocket.enabled", false);
pref("browser.pocket.api", "");
pref("browser.pocket.site", "");
pref("browser.pocket.oAuthConsumerKey", "");
pref("browser.pocket.useLocaleList", false);
pref("browser.pocket.enabledLocales", "");
pref("browser.newtabpage.activity-stream.feeds.section.topstories", false);

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
pref("browser.newtabpage.activity-stream.feeds.section.highlights", false);
pref("browser.newtabpage.activity-stream.feeds.snippets", false);
pref("browser.newtabpage.activity-stream.migrationExpired", true);
pref("browser.newtabpage.activity-stream.prerender", false);
pref("browser.newtabpage.activity-stream.showSearch", false);
pref("browser.newtabpage.activity-stream.showTopSites", false);
pref("browser.newtabpage.directory.source","");
pref("browser.newtabpage.enabled", false);
pref("browser.newtabpage.enhanced", false);
pref("browser.newtabpage.directory.ping", "");
pref("browser.newtabpage.introShown", true);

// Disable home snippets
pref("browser.aboutHomeSnippets.updateUrl", "data:text/html");

// Disable form autofill
pref("browser.formfill.enable", false);
// Manual autofill (if above is true)
pref("signon.autofillForms", false);
// Disable autofill on non-HTTPS sites (if autofill is true)
pref("signon.autofillForms.http", false);

// Display warning UI for insecure login fields
pref("security.insecure_field_warning.contextual.enabled", true);

// Disable password manager
pref("signon.rememberSignons", false);

// Disable plugin installer
pref("plugins.hide_infobar_for_missing_plugin", true);
pref("plugins.hide_infobar_for_outdated_plugin", true);
pref("plugins.notifyMissingFlash", false);

// Enable tracking protection
pref("privacy.trackingprotection.enabled", true);
pref("privacy.trackingprotection.pbmode.enabled", true);

// Disable datareporting and telemetry
pref("browser.ping-centre.telemetry", false);
pref("datareporting.healthreport.dataSubmissionEnabled", false);
pref("datareporting.healthreport.uploadEnabled", false);
pref("toolkit.telemetry.archive.enabled", false);
pref("toolkit.telemetry.bhrPing.enabled", false);
pref("toolkit.telemetry.enabled", false);
pref("toolkit.telemetry.firstShutdownPing.enabled", false);
pref("toolkit.telemetry.newProfilePing.enabled", false);
pref("toolkit.telemetry.reportingpolicy.firstRun", false);
pref("toolkit.telemetry.shutdownPingSender.enabled", false);
pref("toolkit.telemetry.unified", false);
pref("toolkit.telemetry.updatePing.enabled", false);
pref("experiments.enabled", false);
pref("experiments.activeExperiment", false);
pref("experiments.supported", false);
pref("extensions.ui.experiment.hidden", false);
pref("nsITelemetry.canRecordBase", false);
pref("nsITelemetry.canRecordExtended", false);

// Disable Safe Browsing service
//pref("browser.safebrowsing.malware.enabled", false);
//pref("browser.safebrowsing.phishing.enabled", false);
//pref("browser.safebrowsing.downloads.enabled", false);
//pref("services.sync.prefs.sync.browser.safebrowsing.enabled", false);
//pref("services.sync.prefs.sync.browser.safebrowsing.malware.enabled", false);

// Disable Screenshots
//pref("extensions.screenshots.disabled", true);

// Disable SHIELD
pref("extensions.shield-recipe-client.enabled", false);
pref("app.shield.optoutstudies.enabled", false);

// Disable battery api
pref("dom.battery.enabled", false);

// Enable anti fingerprinting
// pref("privacy.resistFingerprinting", true);

// Disable FlyWeb
pref("dom.flyweb.enabled", false);

// Disable gamepad API
pref("dom.gamepad.enabled", false);

// Disable geolocation
//pref("geo.enabled", false);
pref("geo.wifi.logging.enabled", false);

// Disable WebGL
//pref("webgl.disabled", false);
// WebGL minimum capability mode (if above is true)
// pref("webgl.min_capability_mode", true);
// Disable webGL extensions, if WebGL is enabled
// pref("webgl.disable-extensions", true);

// Disable web notifications
pref("dom.push.connection.enabled", false);
pref("dom.push.enabled", false);
pref("dom.webnotifications.enabled", false);
pref("dom.webnotifications.serviceworker.enabled", false);

// Disable WebRTC
//pref("media.peerconnection.enabled", false);

// Prevent websites from getting local IP from WebRTC
pref("media.peerconnection.ice.default_address_only", true);
pref("media.peerconnection.ice.no_host", true);

// Disable HTML5 pinging
pref("browser.send_pings", false);
// Ping the same host as the origin page (if above is true)
pref("browser.send_pings.require_same_host", true);

// Classic Theme Restorer
pref("extensions.classicthemerestorer.altautocompl", true);
pref("extensions.classicthemerestorer.altoptions", "options_win_alt");
pref("extensions.classicthemerestorer.am_compact", true);
pref("extensions.classicthemerestorer.backforward", true);
pref("extensions.classicthemerestorer.bfurlbarfix", true);
pref("extensions.classicthemerestorer.closeabarbut", true);
pref("extensions.classicthemerestorer.ctroldsearch", true);
pref("extensions.classicthemerestorer.ctroldsearchc", true);
pref("extensions.classicthemerestorer.ctrreset", false);
pref("extensions.classicthemerestorer.feedinurl", true);
pref("extensions.classicthemerestorer.firstrun", false);
pref("extensions.classicthemerestorer.fsaduration", false);
pref("extensions.classicthemerestorer.padlock", "padlock_classic");
pref("extensions.classicthemerestorer.showtabclose", true);
pref("extensions.classicthemerestorer.starinurl", true);
pref("extensions.classicthemerestorer.tabsontop", "false");
pref("extensions.classicthemerestorer.wincontrols", true);

// Download Status Bar
pref("extensions.downloadbar.autocleancompletedonquit", true);
pref("extensions.downloadbar.autoclosebarwhendownloadscomplete", true);
pref("extensions.downloadbar.autoclosesecond", 3);
pref("extensions.downloadbar.firstrun", true)

// Firetray
pref("extensions.firetray.firstrun", false);
pref("extensions.firetray.hides_on_close", false);
pref("extensions.firetray.hides_on_minimize", false);
pref("extensions.firetray.hides_single_window", false);

// NoScript
pref("noscript.clearClick.prompt", false);
pref("noscript.confirmSiteInfo", false);
pref("noscript.ctxMenu", false);
pref("noscript.firstRunRedirection", false);
pref("noscript.forbidBookmarklets", true);
pref("noscript.forbidMedia", false);
pref("noscript.hoverUI", false);
pref("noscript.notify", false);
pref("noscript.notify.bottom", false);
pref("noscript.showAbout", false);
pref("noscript.showDomain", true);
pref("noscript.sound.oncePerSite", false);
pref("noscript.visibleUIChecked", true);

// Status-4-ever
pref("extensions.caligon.s4e.addonbar.windowGripper", false);
pref("extensions.caligon.s4e.download.label.force", true);
pref("extensions.caligon.s4e.firstRun", false);
pref("extensions.caligon.s4e.firstRun.australis", false);
pref("extensions.caligon.s4e.progress.urlbar", 0);

// TabMixPlus
pref("extensions.tabmix.appearance.selectedTabIndex", 1);
pref("extensions.tabmix.autoReloadMenu", true);
pref("extensions.tabmix.closeRightMenu", false);
pref("extensions.tabmix.events.selectedTabIndex", 4);
pref("extensions.tabmix.focusTab", 4);
pref("extensions.tabmix.hideTabBarButton", false);
pref("extensions.tabmix.openTabNext", true);
pref("extensions.tabmix.opentabfor.bookmarks", true);
pref("extensions.tabmix.opentabfor.history", true);
pref("extensions.tabmix.opentabfor.urlbar", true);
pref("extensions.tabmix.opentabforLinks", 2);
pref("extensions.tabmix.progressMeter", false);
pref("extensions.tabmix.sessions.crashed", true);
pref("extensions.tabmix.sessions.restore.overwritewindows", false);
pref("extensions.tabmix.singleWindow", true);
pref("extensions.tabmix.syncPrefs", true);
pref("extensions.tabmix.tabBarMaxRow", 2);
pref("extensions.tabmix.tabBarMode", 2);
pref("extensions.tabmix.tabs.closeButtons", 2);
