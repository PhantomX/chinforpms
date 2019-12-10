// Chinforinfula Firefox settings
// 20191209

// Some borrowed from https://github.com/ghacksuserjs/ghacks-user.js

pref("accessibility.force_disabled", 1);
pref("beacon.enabled", false);
pref("browser.bookmarks.showRecentlyBookmarked", false);
pref("browser.cache.offline.enable", false);
pref("browser.download.folderList", 1);
pref("browser.download.hide_plugins_without_extensions", false);
pref("browser.download.manager.addToRecentDocs", false);
pref("browser.helperApps.deleteTempFileOnExit", true);
pref("browser.contentblocking.enabled", true);
pref("browser.ctrlTab.previews", false);
pref("browser.fixup.alternate.enabled", false);
pref("browser.fixup.hide_user_pass", true);
pref("browser.link.open_newwindow", 3);
pref("browser.link.open_newwindow.override.external", 3);
pref("browser.link.open_newwindow.restriction", 0);
pref("browser.laterrun.enabled", false);
pref("browser.pagethumbnails.capturing_disabled", true);
pref("browser.sessionstore.interval", 30000);
pref("browser.shell.checkDefaultBrowser", false);
pref("browser.ssl_override_behavior", 1);
pref("browser.startup.blankWindow", false);
pref("browser.tabs.closeWindowWithLastTab", false);
pref("browser.tabs.insertRelatedAfterCurrent", true);
pref("browser.tabs.loadBookmarksInTabs", true);
pref("browser.tabs.opentabfor.middleclick", false);
//pref("browser.tabs.remote.allowLinkedWebInFileUriProcess", false);
pref("browser.urlbar.clickSelectsAll", false);
pref("browser.urlbar.doubleClickSelectsAll", true);
pref("browser.urlbar.openintab", true);
pref("browser.urlbar.trimURLs", false);
pref("browser.urlbar.speculativeConnect.enabled", false);
pref("browser.urlbar.usepreloadedtopurls.enabled", false);
pref("browser.xul.error_pages.expert_bad_cert", true);
pref("dom.allow_cut_copy", false);
pref("dom.disable_open_during_load", true);
pref("dom.IntersectionObserver.enabled", false);
// "change click dblclick mouseup pointerup notificationclick reset submit touchend"
pref("dom.popup_allowed_events", "click dblclick");
pref("dom.popup_maximum", 3);
pref("dom.targetBlankNoOpener.enabled", true);
pref("dom.vibrator.enabled", false);
pref("extensions.getAddons.showPane", false);
pref("extensions.htmlaboutaddons.recommendations.enabled", false);
pref("general.autoScroll", false);
pref("general.smoothScroll", false);
pref("general.warnOnAboutConfig", false);
pref("browser.aboutConfig.showWarning", false);
pref("keyword.enabled", false);
pref("layout.css.prefixes.animations", false);
pref("layout.spellcheckDefault", 0);
pref("media.autoplay.enabled", false);
pref("media.autoplay.enabled.user-gestures-needed", false);
pref("media.autoplay.default", 5);
pref("media.autoplay.allow-muted", false);
pref("media.block-autoplay-until-in-foreground", true);
pref("middlemouse.contentLoadURL", false);
pref("privacy.userContext.longPressBehavior", 2);
pref("privacy.userContext.enabled", true);
pref("privacy.userContext.ui.enabled", true);
pref("toolkit.cosmeticAnimations.enabled", false);
pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);

// Startup
pref("browser.startup.page", 0);
pref("browser.startup.homepage", "about:blank");
pref("browser.newtabpage.enabled", false);
pref("browser.newtab.preload", false);

// History
pref("browser.sessionhistory.max_entries", 10);
pref("browser.urlbar.filter.javascript", true);
pref("layout.css.visited_links_enabled", false);

// Search
pref("browser.search.openintab", true);
pref("browser.urlbar.oneOffSearches", false);
pref("browser.urlbar.unifiedcomplete", false);
pref("browser.search.suggest.enabled", false);
pref("browser.urlbar.maxHistoricalSearchSuggestions", 0);
pref("browser.urlbar.suggest.searches", false);
pref("browser.urlbar.userMadeSearchSuggestionsChoice", true);

// Enable Containers 
// pref("privacy.userContext.enabled", true);

// No reset nagging
pref("browser.disableResetPrompt", true);

// Don't show 'know your rights' on first run
pref("browser.rights.3.shown", true);

// Don't show Onboarding on first run after every update
pref("browser.onboarding.enabled", false);

// Activity Stream
pref("browser.library.activity-stream.enabled", false);
pref("browser.newtabpage.activity-stream.asrouter.providers.snippets", "");
pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.addons", false);
pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.features", false);
pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr", false);
pref("browser.newtabpage.activity-stream.disableSnippets", true);
pref("browser.newtabpage.activity-stream.feeds.snippets", false);
pref("browser.newtabpage.activity-stream.feeds.section.topstories", false);
pref("browser.newtabpage.activity-stream.section.highlights.includePocket", false);
pref("browser.newtabpage.activity-stream.showSponsored", false);
pref("browser.newtabpage.activity-stream.feeds.discoverystreamfeed", false);
pref("browser.newtabpage.activity-stream.feeds.telemetry", false);
pref("browser.newtabpage.activity-stream.telemetry", false);
pref("browser.newtabpage.activity-stream.telemetry.ping.endpoint", "");

// Don't show WhatsNew on first run after every update
pref("browser.startup.homepage_override.mstone","ignore");
pref("startup.homepage_welcome_url", "");
pref("startup.homepage_welcome_url.additional", "");
pref("startup.homepage_override_url", "");

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
pref("extensions.pocket.enabled", false);

// No DRM too
pref("browser.eme.ui.enabled", false);
pref("media.eme.enabled", false);
pref("media.eme.apiVisible", false);

// Developer tools
pref("devtools.chrome.enabled", false);
pref("devtools.debugger.remote-enabled", false);
pref("devtools.webide.enabled", false);
pref("devtools.webide.adbAddonURL", "");
pref("devtools.webide.autoinstallADBExtension", false);
pref("devtools.webide.autoinstallADBHelper", false);
pref("devtools.webide.autoinstallFxdtAdapters", false);
pref("devtools.webide.autoConnectRuntime", false);

// No blobs
pref("media.gmp-gmpopenh264.provider.enabled",false);
pref("media.gmp-gmpopenh264.autoupdate",false);
pref("media.gmp-gmpopenh264.enabled",false);
pref("media.gmp-gmpopenh264.visible",false);
pref("media.gmp-manager.url","http://127.0.0.1/");
pref("media.gmp-manager.url.override", "data:text/plain,");
pref("media.gmp-provider.enabled",false);
pref("media.gmp.trial-create.enabled",false);
pref("media.gmp-widevinecdm.visible", false);
pref("media.gmp-widevinecdm.enabled", false);

// No ads downloads
pref("browser.newtab.preload", false);
pref("browser.newtabpage.activity-stream.feeds.section.highlights", false);
pref("browser.newtabpage.activity-stream.feeds.snippets", false);
pref("browser.newtabpage.activity-stream.migrationExpired", true);
pref("browser.newtabpage.activity-stream.prerender", false);
pref("browser.newtabpage.activity-stream.showSearch", false);
pref("browser.newtabpage.activity-stream.showTopSites", false);
pref("browser.newtabpage.directory.source","data:application/json,{}");
pref("browser.newtabpage.enabled", false);
pref("browser.newtabpage.enhanced", false);
pref("browser.newtabpage.directory.ping", "");
pref("browser.newtabpage.introShown", true);

// Disable DoH
pref("network.trr.mode", 0);
pref("network.trr.bootstrapAddress", "");
pref("network.trr.uri", "");

// Disable home snippets
pref("browser.aboutHomeSnippets.updateUrl", "data:text/html");

// Disable Captive Portal
pref("captivedetect.canonicalURL", "");
pref("network.captive-portal-service.enabled", false);
pref("network.connectivity-service.enabled", false);

// Disable form autofill
pref("browser.formfill.enable", false);
// Manual autofill (if above is true)
pref("signon.autofillForms", false);
// Disable autofill on non-HTTPS sites (if autofill is true)
pref("signon.autofillForms.http", false);

pref("extensions.formautofill.addresses.enabled", false);
pref("extensions.formautofill.available", "off");
pref("extensions.formautofill.creditCards.enabled", false);
pref("extensions.formautofill.heuristics.enabled", false);

// Disable Web Compatibility Reporter
pref("extensions.webcompat-reporter.enabled", false);

pref("security.insecure_connection_icon.enabled", true);
pref("security.insecure_connection_text.enabled", true);

// Display warning UI for insecure login fields
pref("security.insecure_field_warning.contextual.enabled", true);

pref("security.ssl.require_safe_negotiation", true);

// Disable SSL Error Reporting
pref("security.ssl.errorReporting.automatic", false);
pref("security.ssl.errorReporting.enabled", false);
pref("security.ssl.errorReporting.url", "");

pref("security.tls.enable_0rtt_data", false);

// Potential credentials phishing hardening
pref("network.auth.subresource-http-auth-allow", 1);

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
pref("app.normandy.enabled", false);
pref("app.normandy.api_url", "");
pref("app.shield.optoutstudies.enabled", false);
pref("extensions.shield-recipe-client.enabled", false);
pref("shield.savant.enabled", false);
pref("breakpad.reportURL", "");
pref("browser.chrome.errorReporter.enabled", false);
pref("browser.chrome.errorReporter.submitUrl", "");
pref("browser.crashReports.unsubmittedCheck.enabled", false);
pref("browser.crashReports.unsubmittedCheck.autoSubmit", false);
pref("browser.crashReports.unsubmittedCheck.autoSubmit2", false);
pref("browser.discovery.enabled", false);
pref("browser.ping-centre.telemetry", false);
pref("browser.tabs.crashReporting.sendReport", false);
pref("datareporting.policy.dataSubmissionEnabled", false);
pref("datareporting.healthreport.dataSubmissionEnabled", false);
pref("datareporting.healthreport.uploadEnabled", false);
pref("dom.ipc.plugins.flash.subprocess.crashreporter.enabled", false);
pref("dom.ipc.plugins.reportCrashURL", false);
pref("middlemouse.paste", false);
pref("toolkit.telemetry.archive.enabled", false);
pref("toolkit.telemetry.bhrPing.enabled", false);
pref("toolkit.telemetry.cachedClientID", "");
pref("toolkit.telemetry.enabled", false);
pref("toolkit.telemetry.firstShutdownPing.enabled", false);
pref("toolkit.telemetry.hybridContent.enabled", false);
pref("toolkit.telemetry.newProfilePing.enabled", false);
pref("toolkit.telemetry.reportingpolicy.firstRun", false);
pref("toolkit.telemetry.server", "data:,");
pref("toolkit.telemetry.shutdownPingSender.enabled", false);
pref("toolkit.telemetry.unified", false);
pref("toolkit.telemetry.updatePing.enabled", false);
pref("experiments.enabled", false);
pref("experiments.manifest.uri", "");
pref("experiments.activeExperiment", false);
pref("experiments.supported", false);
pref("network.allow-experiments", false);
pref("extensions.ui.experiment.hidden", false);
pref("extensions.webcompat-reporter.enabled", false);
pref("nsITelemetry.canRecordBase", false);
pref("nsITelemetry.canRecordExtended", false);
pref("toolkit.coverage.endpoint.base", "");
pref("toolkit.coverage.opt-out", true);
pref("toolkit.telemetry.coverage.opt-out", true);

// Disable Safe Browsing service
//pref("browser.safebrowsing.malware.enabled", false);
//pref("browser.safebrowsing.phishing.enabled", false);
//pref("browser.safebrowsing.downloads.enabled", false);
//pref("services.sync.prefs.sync.browser.safebrowsing.enabled", false);
//pref("services.sync.prefs.sync.browser.safebrowsing.malware.enabled", false);
pref("browser.safebrowsing.downloads.remote.enabled", false);
pref("browser.safebrowsing.downloads.remote.url", "");
pref("browser.safebrowsing.provider.google.reportURL", "");
pref("browser.safebrowsing.reportPhishURL", "");
pref("browser.safebrowsing.provider.google4.reportURL", "");
pref("browser.safebrowsing.provider.google.reportMalwareMistakeURL", "");
pref("browser.safebrowsing.provider.google.reportPhishMistakeURL", "");
pref("browser.safebrowsing.provider.google4.reportMalwareMistakeURL", "");
pref("browser.safebrowsing.provider.google4.reportPhishMistakeURL", "");
pref("browser.safebrowsing.provider.google4.dataSharing.enabled", false);
pref("browser.safebrowsing.provider.google4.dataSharingURL", "");

// Disable Screenshots
//pref("extensions.screenshots.disabled", true);

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
//pref("media.peerconnection.use_document_iceservers", false);
//pref("media.peerconnection.video.enabled", false);
//pref("media.peerconnection.identity.enabled", false);
//pref("media.peerconnection.identity.timeout", 1);
//pref("media.peerconnection.turn.disable", true);
//pref("media.peerconnection.ice.tcp", false);
//pref("media.navigator.video.enabled", false);

// Screensharing
//pref("media.getusermedia.screensharing.enabled", false);
//pref("media.getusermedia.browser.enabled", false);
//pref("media.getusermedia.audiocapture.enabled", false);


// Prevent websites from getting local IP from WebRTC
pref("media.peerconnection.ice.default_address_only", true);
pref("media.peerconnection.ice.no_host", true);
pref("media.peerconnection.ice.proxy_only_if_behind_proxy", true);

// Disable HTML5 pinging
pref("browser.send_pings", false);
// Ping the same host as the origin page (if above is true)
pref("browser.send_pings.require_same_host", true);

// Disable SPDY
pref("network.http.spdy.enabled", false);
pref("network.http.spdy.enabled.deps", false);
pref("network.http.spdy.enabled.http2", false);

// alsvc too
pref("network.http.altsvc.enabled", false);
pref("network.http.altsvc.oe", false);

// Disable uitour
pref("browser.uitour.enabled", false);
pref("browser.uitour.url", "");

// Blocklist sanitize
pref("extensions.blocklist.enabled", true);
pref("extensions.blocklist.url", "https://blocklists.settings.services.mozilla.com/v1/blocklist/3/%APP_ID%/%APP_VERSION%/");
pref("services.blocklist.update_enabled", true);
pref("services.blocklist.signing.enforced", true);

// No window messing
pref("dom.disable_window_open_feature.close", true);
pref("dom.disable_window_open_feature.location", true);
pref("dom.disable_window_open_feature.menubar", true);
pref("dom.disable_window_open_feature.minimizable", true);
pref("dom.disable_window_open_feature.personalbar", true);
pref("dom.disable_window_open_feature.resizable", true);
pref("dom.disable_window_open_feature.status", true);
pref("dom.disable_window_open_feature.titlebar", true);
pref("dom.disable_window_open_feature.toolbar", true);
pref("dom.disable_window_move_resize", true);

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

// Classic Toolbar Theme
pref("extensions.cstbb-extension.navbarbuttons", "nabbuttons_small");
pref("extensions.cstbb-extension.navbicons", "ico_ff45d");
pref("extensions.cstbb-extension.svgfilters", true);
pref("extensions.cstbb-extension.verdomainid", true);

// Download Status Bar
pref("extensions.downloadbar.autocleancompletedonquit", true);
pref("extensions.downloadbar.autoclosebarwhendownloadscomplete", true);
pref("extensions.downloadbar.autoclosesecond", 3);
pref("extensions.downloadbar.firstrun", true);

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
