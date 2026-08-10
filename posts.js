/* ============================================================
   BLOG MANIFEST
   To publish a new post:
     1. Create a new HTML file (copy blog-spc-system.html as a template).
     2. Add ONE entry to the TOP of the array below (newest first).
   That's it — blog.html and the homepage update automatically.
   ============================================================ */
window.POSTS = [
  {
    title: "Why we built our own MES — and shipped it to two factories",
    url: "blog-mes-build.html",
    date: "2026-08-10",
    tag: "MES · Leadership",
    excerpt: "The build-vs-buy call behind an in-house manufacturing execution system — and why the hard parts were bilingual launch gates and floor trust, not code."
  },
  {
    title: "The pilot build is a question, not a milestone",
    url: "blog-pilot-build.html",
    date: "2026-07-05",
    tag: "NPI · Process",
    excerpt: "A first pilot that only proves \"we can build one\" wastes most of its value. Treating the pilot as an experiment that answers whether the process is ready to scale."
  },
  {
    title: "Reading a yield signal: from noise to a ranked cause list",
    url: "blog-yield-signal.html",
    date: "2026-06-22",
    tag: "Yield · Root-Cause",
    excerpt: "\"Yield dropped to 84%\" is an alarm, not information. How to stratify, bound, and reproduce a yield loss until it becomes a short list of things you can actually fix."
  },
  {
    title: "Building an SPC system operators actually use",
    url: "blog-spc-system.html",
    date: "2026-06-08",
    tag: "Process · Data",
    excerpt: "Control charts only work if the line trusts them. Notes on standing up statistical process control at Infinitum — and the data plumbing underneath it."
  }
  // , { title: "...", url: "blog-...html", date: "YYYY-MM-DD", tag: "...", excerpt: "..." }
];
