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
  var FALLBACK_URL = 'https://aalaap.app/e/rogue-bachata-wednesdays-keystone-crescent-copy-ez3e';

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

  var MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  var PUBLIC_VENUE = "Keystone Crescent Members Club, King's Cross N1 9DX";
  var OCT7_POSTER = 'wednesday-7-october-2026';

  function formatLongDate(iso) {
    var parts = (iso || '').split('-');
    if (parts.length < 3) return iso || '';
    return String(+parts[2]) + ' ' + MONTHS[+parts[1] - 1] + ' ' + parts[0];
  }

  /* The 7 October 2026 artwork stays on that night only. */
  function posterSrc(event) {
    if (!event || !event.image) return '';
    var src = String(event.image);
    if (src.indexOf(OCT7_POSTER) !== -1 && event.date !== '2026-10-07') return '';
    return src;
  }

  function appendStructure(parent, event) {
    var p = document.createElement('p');
    p.className = 'wed-night-structure';
    /* Angy Pérez is the guest on 14 Oct 2026 only. Later Wednesdays keep the same night shape without naming that guest. */
    var angyNight = event && event.date === '2026-10-14';
    var klass = angyNight
      ? 'Rogue Bachata Open Level Bachata Class with Zach'
      : 'Rogue Bachata Open Level Bachata Class';
    var workshop = angyNight
      ? 'Wed 14 Oct: the Connection Workshop with Angy Pérez, international Bachata connection teacher'
      : 'a connection workshop';
    p.textContent = klass + ', for people with 0 to 1 year experience in Bachata, and ' + workshop + ', for dancers of any background, experienced bachata dancers, and people passionate about movement and connection. Both run at the same time, 7:30–8:45pm. Free social 9pm–late.';
    parent.appendChild(p);
  }

  function renderWednesdayNights(mount, events) {
    if (!mount) return;
    var upcoming = upcomingEvents(events);
    mount.innerHTML = '';
    if (!upcoming.length) {
      mount.hidden = true;
      return;
    }
    upcoming.forEach(function (ev) {
      var article = document.createElement('article');
      article.className = 'card wed-night';
      var heading = document.createElement('h3');
      heading.textContent = 'Wednesday ' + formatLongDate(ev.date);
      article.appendChild(heading);

      var venue = document.createElement('p');
      venue.className = 'wed-night-venue';
      venue.textContent = ev.venue || PUBLIC_VENUE;
      article.appendChild(venue);

      var src = posterSrc(ev);
      if (src) {
        var img = document.createElement('img');
        img.className = 'wed-night-poster';
        img.alt = 'Official poster for Wednesday ' + formatLongDate(ev.date);
        img.addEventListener('error', function () { img.remove(); });
        img.src = src;
        article.appendChild(img);
      }

      appendStructure(article, ev);

      if (ev.url) {
        var book = document.createElement('a');
        book.className = 'wed-night-book';
        book.href = ev.url;
        book.target = '_blank';
        book.rel = 'noopener';
        book.textContent = 'Book ' + formatLongDate(ev.date);
        article.appendChild(book);
      }
      mount.appendChild(article);
    });
    mount.hidden = false;
  }

  function renderFeaturedPoster(mount, event) {
    if (!mount) return;
    var src = posterSrc(event);
    mount.innerHTML = '';
    if (!src) {
      mount.hidden = true;
      return;
    }
    var kicker = document.createElement('span');
    kicker.className = 'section-kicker';
    kicker.textContent = 'This Wednesday';
    mount.appendChild(kicker);

    var heading = document.createElement('h2');
    heading.textContent = 'Wednesday ' + formatLongDate(event.date);
    mount.appendChild(heading);

    var figure = document.createElement('figure');
    figure.className = 'this-wed-poster';
    var img = document.createElement('img');
    img.alt = 'Official poster for Wednesday ' + formatLongDate(event.date);
    img.addEventListener('error', function () { figure.remove(); });
    img.src = src;
    figure.appendChild(img);
    mount.appendChild(figure);

    var venue = document.createElement('p');
    venue.className = 'lede';
    venue.textContent = event.venue || PUBLIC_VENUE;
    mount.appendChild(venue);
    mount.hidden = false;
  }

  global.RogueEvents = {
    TZ: TZ,
    FALLBACK_URL: FALLBACK_URL,
    PUBLIC_VENUE: PUBLIC_VENUE,
    londonTodayISO: londonTodayISO,
    upcomingEvents: upcomingEvents,
    featuredEvent: featuredEvent,
    activeVenueNotice: activeVenueNotice,
    renderVenueNotice: renderVenueNotice,
    applyBookLinks: applyBookLinks,
    formatLongDate: formatLongDate,
    posterSrc: posterSrc,
    renderWednesdayNights: renderWednesdayNights,
    renderFeaturedPoster: renderFeaturedPoster
  };
})(window);
