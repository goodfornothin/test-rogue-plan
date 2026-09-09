/**
 * Shared Wednesday booking + one-off venue-notice helpers.
 *
 * Dates are compared in Europe/London. Past calendar days are skipped.
 *
 * Optional one-night venue notice (do NOT hard-code banners in HTML):
 *   {
 *     "date": "2026-11-04",
 *     "venue": "Temporary Venue, Address",
 *     "url": "https://aalaap.app/e/...",
 *     "venueNotice": {
 *       "endDate": "2026-11-04",
 *       "tag": "This occasion only · 4 November 2026",
 *       "headline": "Wednesday class has moved",
 *       "body": "Directions and details…"
 *     }
 *   }
 * The notice is injected only while London date <= endDate (defaults to event date).
 */
(function (global) {
  var TZ = 'Europe/London';
  var FALLBACK_URL = 'https://aalaap.app/e/rogue-bachata-wednesdays-keystone-crescent-hy6c';

  function londonTodayISO() {
    return new Intl.DateTimeFormat('en-CA', {
      timeZone: TZ,
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    }).format(new Date());
  }

  function noticeEndDate(event) {
    var notice = event && event.venueNotice;
    if (!notice) return '';
    return notice.endDate || notice.expires || event.date || '';
  }

  function isNoticeActive(event, todayISO) {
    var end = noticeEndDate(event);
    return !!(end && todayISO <= end);
  }

  function upcomingEvents(list) {
    var today = londonTodayISO();
    return (list || [])
      .filter(function (e) { return e && e.date && e.date >= today; })
      .sort(function (a, b) { return a.date < b.date ? -1 : a.date > b.date ? 1 : 0; });
  }

  function featuredEvent(list) {
    var upcoming = upcomingEvents(list);
    return upcoming[0] || null;
  }

  function activeVenueNotice(list) {
    var today = londonTodayISO();
    var events = list || [];
    for (var i = 0; i < events.length; i++) {
      if (isNoticeActive(events[i], today)) return events[i];
    }
    return null;
  }

  function renderVenueNotice(mount, event) {
    if (!mount) return;
    mount.innerHTML = '';
    if (!event || !event.venueNotice) {
      mount.hidden = true;
      return;
    }
    var notice = event.venueNotice;
    var inner = document.createElement('div');
    inner.className = 'venue-alert-inner';
    var copy = document.createElement('div');
    copy.className = 'venue-alert-copy';

    if (notice.tag) {
      var tag = document.createElement('p');
      tag.className = 'venue-alert-tag';
      tag.textContent = notice.tag;
      copy.appendChild(tag);
    }
    if (notice.headline) {
      var headline = document.createElement('p');
      headline.className = 'venue-alert-headline';
      headline.textContent = notice.headline;
      copy.appendChild(headline);
    }
    if (notice.body) {
      var body = document.createElement('p');
      body.className = 'venue-alert-body';
      body.textContent = notice.body;
      copy.appendChild(body);
    }
    inner.appendChild(copy);
    mount.appendChild(inner);
    mount.hidden = false;
  }

  function applyBookLinks(url) {
    var href = url || FALLBACK_URL;
    document.querySelectorAll('.js-book-link').forEach(function (el) {
      el.href = href;
      el.target = '_blank';
      el.rel = 'noopener';
    });
  }

  global.RogueEvents = {
    TZ: TZ,
    FALLBACK_URL: FALLBACK_URL,
    londonTodayISO: londonTodayISO,
    upcomingEvents: upcomingEvents,
    featuredEvent: featuredEvent,
    activeVenueNotice: activeVenueNotice,
    renderVenueNotice: renderVenueNotice,
    applyBookLinks: applyBookLinks
  };
})(window);
