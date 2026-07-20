/* Comments — giscus (GitHub Discussions), themed to match the site.
   Loads into #giscus-comments. Lives on GitHub, so it survives every deploy —
   nothing here writes to this folder or depends on it. */
(function () {
  var mount = document.getElementById('giscus-comments');
  if (!mount) return;

  var LIGHT = 'https://aseembhandari.com/giscus-theme-light.css';
  var DARK = 'https://aseembhandari.com/giscus-theme-dark.css';
  var mql = window.matchMedia('(prefers-color-scheme: dark)');

  function themeUrl() { return mql.matches ? DARK : LIGHT; }

  var script = document.createElement('script');
  script.src = 'https://giscus.app/client.js';
  script.async = true;
  script.crossOrigin = 'anonymous';
  script.setAttribute('data-repo', 'aseembhandari/aseembhandari.com');
  script.setAttribute('data-repo-id', 'R_kgDOTRGzNw');
  script.setAttribute('data-category', 'Announcements');
  script.setAttribute('data-category-id', 'DIC_kwDOTRGzN84DBjuc');
  script.setAttribute('data-mapping', 'pathname');
  script.setAttribute('data-strict', '0');
  script.setAttribute('data-reactions-enabled', '1');
  script.setAttribute('data-emit-metadata', '0');
  script.setAttribute('data-input-position', 'bottom');
  script.setAttribute('data-lang', 'en');
  script.setAttribute('data-theme', themeUrl());
  mount.appendChild(script);

  // live-update if the OS theme changes while the page is open
  mql.addEventListener('change', function () {
    var iframe = document.querySelector('iframe.giscus-frame');
    if (!iframe) return;
    iframe.contentWindow.postMessage(
      { giscus: { setConfig: { theme: themeUrl() } } },
      'https://giscus.app'
    );
  });
})();
