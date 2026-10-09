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
 *
 * Optional one-night feature (text-free wide banner + the night's copy; the card
 * is built from the data, so it does not repeat a poster):
 *   {
 *     "date": "2026-10-14",
 *     "banner": "images/wednesday-14-october-2026-banner.png",
 *     "feature": {
 *       "tag": "Wednesday 14 October",
 *       "headline": "…", "lede": "…", "bannerAlt": "…",
 *       "schedule": [{ "time": "7:30–8:45pm", "title": "…", "teacher": "…", "role": "…", "text": "…", "lead": true }],
 *       "note": "…", "price": "£10 + booking fee"
 *     }
 *   }
 * While it is the next Wednesday it shows at the top of the homepage and the
 * Wednesday page, and goes once the date has passed.
 * Artwork named wednesday-<day>-<month>-<year> only ever shows on that date.
 *
 * Static copy for one night: data-show-until="YYYY-MM-DD" hides after that
 * London date; data-show-from="YYYY-MM-DD" (ship it with `hidden`) appears from it.
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
  var DATED_ART = /wednesday-(\d{1,2})-([a-z]+)-(\d{4})/i;

  function pad2(n) { return (+n < 10 ? '0' : '') + (+n); }

  function formatLongDate(iso) {
    var parts = (iso || '').split('-');
    if (parts.length < 3) return iso || '';
    return String(+parts[2]) + ' ' + MONTHS[+parts[1] - 1] + ' ' + parts[0];
  }

  /* ISO date named in artwork like images/wednesday-14-october-2026.jpg, else ''. */
  function artDate(src) {
    var m = DATED_ART.exec(src || '');
    if (!m) return '';
    var month = MONTHS.map(function (name) { return name.toLowerCase(); }).indexOf(m[2].toLowerCase());
    return month < 0 ? '' : m[3] + '-' + pad2(month + 1) + '-' + pad2(m[1]);
  }

  /* Date-specific artwork stays on its own night only. */
  function artSrc(event, key) {
    if (!event || !event[key]) return '';
    var src = String(event[key]);
    var dated = artDate(src);
    if (dated && dated !== event.date) return '';
    return src;
  }

  function posterSrc(event) {
    return artSrc(event, 'image');
  }

  function addText(parent, tag, className, text) {
    if (!text) return null;
    var el = document.createElement(tag);
    if (className) el.className = className;
    el.textContent = text;
    parent.appendChild(el);
    return el;
  }

  /* The banner artwork carries no text, so the night's details sit right under it. */
  function buildNightFeature(event) {
    var f = event.feature || {};
    var card = document.createElement('article');
    card.className = 'night-feature';

    var banner = artSrc(event, 'banner');
    if (banner) {
      var bannerImg = document.createElement('img');
      bannerImg.className = 'night-feature-banner';
      bannerImg.alt = f.bannerAlt || '';
      bannerImg.addEventListener('error', function () { bannerImg.remove(); });
      bannerImg.src = banner;
      card.appendChild(bannerImg);
    }

    var body = document.createElement('div');
    body.className = 'night-feature-body';
    var copy = document.createElement('div');
    copy.className = 'night-feature-copy';
    addText(copy, 'p', 'night-feature-tag', f.tag || 'Wednesday ' + formatLongDate(event.date));
    addText(copy, 'h3', 'night-feature-headline', f.headline);
    addText(copy, 'p', 'night-feature-lede', f.lede);

    if (f.schedule && f.schedule.length) {
      var list = document.createElement('ul');
      list.className = 'night-feature-schedule';
      f.schedule.forEach(function (item) {
        var li = document.createElement('li');
        /* A class with a named teacher gets poster-style billing; "lead" marks the headliner. */
        if (item.teacher) li.className = 'night-feature-class' + (item.lead ? ' is-lead' : '');
        addText(li, 'span', 'night-feature-time', item.time);
        var what = document.createElement('span');
        what.className = 'night-feature-what';
        addText(what, 'strong', '', item.title);
        if (item.teacher) {
          var teacher = document.createElement('span');
          teacher.className = 'night-feature-teacher';
          teacher.appendChild(document.createTextNode('with '));
          addText(teacher, 'em', '', item.teacher);
          what.appendChild(teacher);
        }
        addText(what, 'span', 'night-feature-role', item.role);
        addText(what, 'span', 'night-feature-for', item.text);
        li.appendChild(what);
        list.appendChild(li);
      });
      copy.appendChild(list);
    }

    addText(copy, 'p', 'night-feature-note', f.note);
    addText(copy, 'p', 'night-feature-meta', [event.venue || PUBLIC_VENUE, f.price].filter(Boolean).join(' · '));

    if (event.url) {
      var book = document.createElement('a');
      book.className = 'night-feature-book';
      book.href = event.url;
      book.target = '_blank';
      book.rel = 'noopener';
      book.textContent = 'Book ' + formatLongDate(event.date);
      copy.appendChild(book);
    }
    body.appendChild(copy);
    card.appendChild(body);
    return card;
  }

  function applyDatedCopy() {
    var today = londonTodayISO();
    document.querySelectorAll('[data-show-until], [data-show-from]').forEach(function (el) {
      var until = el.getAttribute('data-show-until');
      var from = el.getAttribute('data-show-from');
      el.hidden = !!((until && today > until) || (from && today < from));
    });
  }

  function appendStructure(parent, event) {
    var p = document.createElement('p');
    p.className = 'wed-night-structure';
    /* Angy Pérez is the guest on 14 Oct 2026 only. Later Wednesdays keep the same night shape without naming that guest. */
    var angyNight = event && event.date === '2026-10-14';
    p.textContent = angyNight
      ? 'The Connection Workshop with Angy Pérez, international Bachata connection teacher, for dancers of any background, experienced bachata dancers, and people passionate about movement and connection, and the Rogue Bachata Open Level Bachata Class with Zach, for people with 0 to 1 year experience in Bachata. Both run at the same time, 7:30–8:45pm. Free social 9pm–late.'
      : 'Rogue Bachata Open Level Bachata Class, for people with 0 to 1 year experience in Bachata, and a connection workshop, for dancers of any background, experienced bachata dancers, and people passionate about movement and connection. Both run at the same time, 7:30–8:45pm. Free social 9pm–late.';
    parent.appendChild(p);
  }

  /* opts.shownAbove: the event whose feature card is already at the top of the
     page, so its list entry is a plain booking card without the artwork. */
  function renderWednesdayNights(mount, events, opts) {
    var shownAbove = opts && opts.shownAbove;
    if (!mount) return;
    var upcoming = upcomingEvents(events);
    mount.innerHTML = '';
    if (!upcoming.length) {
      mount.hidden = true;
      return;
    }
    upcoming.forEach(function (ev) {
      var above = !!(shownAbove && shownAbove.feature && shownAbove.date === ev.date);
      if (ev.feature && !above) {
        mount.appendChild(buildNightFeature(ev));
        return;
      }
      var article = document.createElement('article');
      article.className = 'card wed-night';
      var heading = document.createElement('h3');
      heading.textContent = 'Wednesday ' + formatLongDate(ev.date);
      article.appendChild(heading);

      var venue = document.createElement('p');
      venue.className = 'wed-night-venue';
      venue.textContent = ev.venue || PUBLIC_VENUE;
      article.appendChild(venue);

      var src = above ? '' : posterSrc(ev);
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
    if (!src && !(event && event.feature)) {
      mount.hidden = true;
      return;
    }
    /* A feature card carries its own date, so it goes in without the section heading. */
    if (event.feature) {
      mount.appendChild(buildNightFeature(event));
      mount.hidden = false;
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
    applyDatedCopy: applyDatedCopy,
    renderWednesdayNights: renderWednesdayNights,
    renderFeaturedPoster: renderFeaturedPoster
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyDatedCopy);
  } else {
    applyDatedCopy();
  }
})(window);
