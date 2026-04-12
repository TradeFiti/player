# Joseph Ojwang Portfolio — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-page, scroll-driven portfolio website for Joseph Omondi Ojwang that showcases him to professional football scouts with premium dark cinematic design, animated statistics, and compelling storytelling.

**Architecture:** Single `index.html` file using Tailwind CSS v3 (CDN), AOS scroll animations (CDN), GLightbox (CDN), Google Fonts (Inter + Oswald), and custom JavaScript for counter animations. All media served from local `assets/` directory. No build step, no frameworks.

**Tech Stack:** HTML5, Tailwind CSS v3 CDN, AOS.js, GLightbox, vanilla JavaScript, Google Fonts

**Spec:** `docs/superpowers/specs/2026-04-12-joseph-ojwang-portfolio-design.md`

---

### Task 1: Organize Media Assets

**Files:**
- Create: `assets/images/` (directory with renamed image files)
- Create: `assets/videos/` (directory with renamed video files)

- [ ] **Step 1: Create asset directories**

```bash
mkdir -p assets/images assets/videos
```

- [ ] **Step 2: Copy and rename image files from jose-gallery**

```bash
# Hero portrait (lifestyle shot with sunglasses — best for hero)
cp "jose-gallery/WhatsApp Image 2026-04-12 at 14.12.36 (1).jpeg" assets/images/hero-portrait.jpeg

# Additional portraits
cp "jose-gallery/WhatsApp Image 2026-04-12 at 14.12.36.jpeg" assets/images/portrait-1.jpeg
cp "jose-gallery/WhatsApp Image 2026-04-12 at 14.12.37.jpeg" assets/images/portrait-2.jpeg

# Trial certificate with coach
cp "jose-gallery/WhatsApp Image 2026-03-25 at 20.35.27 (1).jpeg" assets/images/trial-certificate.jpeg

# Certificate B&W (JOLIU event)
cp "jose-gallery/WhatsApp Image 2026-03-25 at 20.35.29 (2).jpeg" assets/images/trial-certificate-2.jpeg

# Match action at Cambrils
cp "jose-gallery/WhatsApp Image 2026-03-25 at 20.35.28 (1).jpeg" assets/images/trial-action-1.jpeg

# Joseph #10 on Cambrils pitch
cp "jose-gallery/WhatsApp Image 2026-04-12 at 13.54.46 (1).jpeg" assets/images/trial-pitch.jpeg

# Team photo with both squads
cp "jose-gallery/WhatsApp Image 2026-03-25 at 20.35.30.jpeg" assets/images/trial-team.jpeg

# Team huddle with coach
cp "jose-gallery/WhatsApp Image 2026-04-12 at 13.54.46.jpeg" assets/images/trial-huddle.jpeg

# Receiving gear
cp "jose-gallery/WhatsApp Image 2026-03-25 at 20.35.29 (1).jpeg" assets/images/trial-gear.jpeg

# Action shots (home team / Kenya)
cp "jose-gallery/WhatsApp Image 2026-03-25 at 20.35.28.jpeg" assets/images/action-kick.jpeg
cp "jose-gallery/WhatsApp Image 2026-03-25 at 20.35.29 (3).jpeg" assets/images/action-goal.jpeg
cp "jose-gallery/WhatsApp Image 2026-03-25 at 20.35.32 (1).jpeg" assets/images/action-control.jpeg

# Local team photo
cp "jose-gallery/WhatsApp Image 2026-03-25 at 20.35.31.jpeg" assets/images/team-local.jpeg

# Camp Nou / Messi Ballon d'Or
cp "jose-gallery/WhatsApp Image 2026-03-25 at 20.35.31 (1).jpeg" assets/images/campnou.jpeg

# Performance data screenshots
cp "jose-gallery/WhatsApp Image 2026-03-25 at 20.35.29.jpeg" assets/images/stats-overview.jpeg
cp "jose-gallery/WhatsApp Image 2026-03-25 at 20.35.27.jpeg" assets/images/stats-speed.jpeg
cp "jose-gallery/WhatsApp Image 2026-03-25 at 20.35.31 (2).jpeg" assets/images/stats-twofeet.jpeg
cp "jose-gallery/WhatsApp Image 2026-03-25 at 20.35.32.jpeg" assets/images/stats-agility.jpeg

# Cambrils UCF Instagram screenshot
cp "jose-gallery/WhatsApp Image 2026-04-12 at 13.40.06.jpeg" assets/images/cambrils-instagram.jpeg
```

- [ ] **Step 3: Copy and rename video files**

```bash
cp "jose-gallery/WhatsApp Video 2026-03-25 at 20.35.26.mp4" assets/videos/highlight-01.mp4
cp "jose-gallery/WhatsApp Video 2026-03-25 at 20.35.26 (1).mp4" assets/videos/highlight-02.mp4
cp "jose-gallery/WhatsApp Video 2026-03-25 at 20.35.27.mp4" assets/videos/highlight-03.mp4
cp "jose-gallery/WhatsApp Video 2026-03-25 at 20.35.27 (1).mp4" assets/videos/highlight-04.mp4
cp "jose-gallery/WhatsApp Video 2026-03-25 at 20.35.27 (2).mp4" assets/videos/highlight-05.mp4
cp "jose-gallery/WhatsApp Video 2026-03-25 at 20.35.28.mp4" assets/videos/highlight-06.mp4
cp "jose-gallery/WhatsApp Video 2026-03-25 at 20.35.28 (1).mp4" assets/videos/highlight-07.mp4
cp "jose-gallery/WhatsApp Video 2026-03-25 at 20.35.30.mp4" assets/videos/highlight-08.mp4
cp "jose-gallery/WhatsApp Video 2026-03-25 at 20.35.31.mp4" assets/videos/highlight-09.mp4
cp "jose-gallery/WhatsApp Video 2026-03-25 at 20.35.31 (1).mp4" assets/videos/highlight-10.mp4
cp "jose-gallery/WhatsApp Video 2026-03-25 at 20.35.32.mp4" assets/videos/highlight-11.mp4
```

- [ ] **Step 4: Verify all assets copied**

```bash
ls -la assets/images/ | wc -l
# Expected: ~21 (20 images + total line)
ls -la assets/videos/ | wc -l
# Expected: ~12 (11 videos + total line)
```

- [ ] **Step 5: Commit**

```bash
git add assets/
git commit -m "chore: organize media assets from jose-gallery into assets/"
```

---

### Task 2: HTML Foundation + Hero Section

**Files:**
- Create: `index.html`

- [ ] **Step 1: Create index.html with full head section, CDN links, custom CSS, and Hero section**

Create `index.html` with this content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Joseph Ojwang | #10 — Attacking Midfielder</title>
  <meta name="description" content="Joseph Omondi Ojwang — 15-year-old attacking midfielder with successful European trial experience at Cambrils UCF, Spain. Two-footed, press-resistant, high ceiling.">

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Oswald:wght@700;900&display=swap" rel="stylesheet">

  <!-- Tailwind CSS v3 CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            dark: { DEFAULT: '#0a0a0f', light: '#0d0d14', mid: '#111827' },
            gold: { DEFAULT: '#ffd700', dark: '#b8960f', light: '#ffe44d' },
            glass: { bg: 'rgba(255,255,255,0.04)', border: 'rgba(255,255,255,0.08)' },
          },
          fontFamily: {
            display: ['Oswald', 'sans-serif'],
            body: ['Inter', 'sans-serif'],
          },
        },
      },
    }
  </script>

  <!-- AOS (Animate On Scroll) -->
  <link href="https://unpkg.com/aos@2.3.4/dist/aos.css" rel="stylesheet">
  <script src="https://unpkg.com/aos@2.3.4/dist/aos.js"></script>

  <!-- GLightbox -->
  <link href="https://cdn.jsdelivr.net/npm/glightbox/dist/css/glightbox.min.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/gh/mcstudios/glightbox/dist/js/glightbox.min.js"></script>

  <style>
    html { scroll-behavior: smooth; }
    body { font-family: 'Inter', sans-serif; background-color: #0a0a0f; color: #ffffff; }

    /* Gold radial glow effect */
    .gold-glow {
      background: radial-gradient(ellipse at 25% 50%, rgba(255,215,0,0.07) 0%, transparent 60%);
    }

    /* Bounce animation for scroll indicator */
    @keyframes bounce-slow {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(8px); }
    }
    .animate-bounce-slow { animation: bounce-slow 2s ease-in-out infinite; }

    /* Fade-in animation for hero load */
    @keyframes fadeSlideRight {
      from { opacity: 0; transform: translateX(-30px); }
      to { opacity: 1; transform: translateX(0); }
    }
    @keyframes fadeScaleUp {
      from { opacity: 0; transform: scale(0.95); }
      to { opacity: 1; transform: scale(1); }
    }
    @keyframes fadeUp {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .hero-text { animation: fadeSlideRight 0.6s ease-out both; }
    .hero-photo { animation: fadeScaleUp 0.8s ease-out 0.2s both; }
    .hero-cta { animation: fadeUp 0.4s ease-out 0.6s both; }
    .hero-scroll { animation: fadeUp 0.4s ease-out 1s both; }

    /* Counter animation target */
    .stat-number { transition: all 0.3s ease; }

    /* Progress bar animation */
    .progress-fill {
      transition: width 1s ease-out 0.3s;
    }

    /* Video play overlay */
    .video-card:hover .play-overlay {
      background: rgba(255,215,0,0.2);
    }
    .play-overlay {
      transition: background 0.3s ease;
    }

    /* Gallery image hover */
    .gallery-item img {
      transition: transform 0.4s ease, filter 0.4s ease;
    }
    .gallery-item:hover img {
      transform: scale(1.05);
      filter: brightness(1.1);
    }

    /* Section divider line */
    .section-label {
      font-family: 'Inter', sans-serif;
      font-size: 0.625rem;
      letter-spacing: 0.25em;
      text-transform: uppercase;
      color: #ffd700;
    }

    /* Glass card */
    .glass-card {
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 0.75rem;
    }

    /* Smooth scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0a0a0f; }
    ::-webkit-scrollbar-thumb { background: rgba(255,215,0,0.3); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,215,0,0.5); }
  </style>
</head>
<body class="antialiased overflow-x-hidden">

  <!-- ============================================ -->
  <!-- SECTION 1: HERO                              -->
  <!-- ============================================ -->
  <section id="hero" class="relative min-h-screen flex items-center gold-glow overflow-hidden">
    <!-- Background #10 watermark -->
    <div class="absolute top-1/2 right-8 -translate-y-1/2 font-display text-[12rem] md:text-[16rem] font-black text-gold/[0.05] select-none pointer-events-none leading-none">
      10
    </div>

    <div class="container mx-auto px-6 md:px-12 lg:px-20 grid grid-cols-1 lg:grid-cols-2 gap-8 items-center relative z-10">
      <!-- Left: Text content -->
      <div class="hero-text order-2 lg:order-1 text-center lg:text-left">
        <p class="section-label mb-3">Attacking Midfielder · #10</p>
        <h1 class="font-display text-5xl md:text-7xl lg:text-8xl font-black leading-[0.9] tracking-tight">
          JOSEPH<br>
          <span class="text-gold">OJWANG</span>
        </h1>
        <p class="mt-4 text-white/40 text-xs md:text-sm tracking-widest font-medium">
          D.O.B: 13 SEPT 2010 &nbsp;·&nbsp; AGE 15 &nbsp;·&nbsp; KENYA 🇰🇪
        </p>
        <p class="mt-1 text-white/30 text-xs tracking-wider">
          Kitengela International · Year 10
        </p>

        <!-- CTA Buttons -->
        <div class="hero-cta flex flex-col sm:flex-row gap-3 mt-8 justify-center lg:justify-start">
          <a href="#highlights" class="bg-gold text-dark font-bold text-xs tracking-widest px-8 py-3.5 rounded-lg hover:bg-gold-light transition-colors duration-300 text-center">
            VIEW HIGHLIGHTS
          </a>
          <a href="#contact" class="border border-white/20 text-white font-semibold text-xs tracking-widest px-8 py-3.5 rounded-lg hover:border-gold/50 hover:text-gold transition-colors duration-300 text-center">
            CONTACT AGENT
          </a>
        </div>
      </div>

      <!-- Right: Portrait photo -->
      <div class="hero-photo order-1 lg:order-2 flex justify-center lg:justify-end">
        <div class="relative">
          <div class="absolute -inset-4 bg-gradient-to-br from-gold/10 to-transparent rounded-2xl blur-2xl"></div>
          <img
            src="assets/images/hero-portrait.jpeg"
            alt="Joseph Ojwang — Attacking Midfielder #10"
            class="relative w-64 md:w-72 lg:w-80 h-auto rounded-2xl object-cover shadow-2xl shadow-gold/10"
          >
        </div>
      </div>
    </div>

    <!-- Scroll indicator -->
    <div class="hero-scroll absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2">
      <span class="text-white/30 text-[10px] tracking-[0.2em] uppercase">Scroll to Discover</span>
      <svg class="w-5 h-5 text-gold/40 animate-bounce-slow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"/>
      </svg>
    </div>
  </section>

  <!-- Sections 2-8 will be added in subsequent tasks -->

  <!-- ============================================ -->
  <!-- SCRIPTS                                      -->
  <!-- ============================================ -->
  <script>
    // Initialize AOS
    AOS.init({
      duration: 700,
      once: true,
      offset: 80,
    });
  </script>

</body>
</html>
```

- [ ] **Step 2: Open in browser and verify**

```bash
open index.html
```

Expected: Full-viewport dark hero with Joseph's portrait, gold name treatment, CTA buttons, and scroll indicator. Animations should play on load.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add HTML foundation with CDN links and Hero section"
```

---

### Task 3: Player Profile Section

**Files:**
- Modify: `index.html` (insert after Hero section closing `</section>` tag, before the `<!-- Sections 2-8 -->` comment)

- [ ] **Step 1: Add Player Profile section HTML**

Insert the following after the Hero `</section>` closing tag, replacing the `<!-- Sections 2-8 will be added in subsequent tasks -->` comment:

```html
  <!-- ============================================ -->
  <!-- SECTION 2: PLAYER PROFILE                    -->
  <!-- ============================================ -->
  <section id="profile" class="py-20 md:py-28 bg-dark-light relative">
    <div class="container mx-auto px-6 md:px-12 lg:px-20">
      <div class="grid grid-cols-1 lg:grid-cols-5 gap-12 items-start">
        <!-- Bio (3 cols) -->
        <div class="lg:col-span-3" data-aos="fade-up">
          <p class="section-label mb-4">Player Profile</p>
          <h2 class="font-display text-3xl md:text-4xl font-black mb-6">The Player</h2>
          <p class="text-white/60 leading-relaxed text-sm md:text-base">
            A <strong class="text-white">press-resistant attacking midfielder</strong> with exceptional
            two-footed ability and sharp vertical play. Joseph reads the game beyond his years — finding
            half-spaces, carrying the ball under pressure, and delivering decisive passes in the final third.
          </p>
          <p class="text-white/60 leading-relaxed text-sm md:text-base mt-4">
            At 15, he has already completed a <strong class="text-gold">successful trial at Cambrils UCF in
            Spain</strong> — organized through his school, <strong class="text-white">Kitengela International</strong>
            — demonstrating the tactical maturity and adaptability that European academies demand.
            His two-footed capability (only a 3% power drop-off between feet, vs. the typical 15-20% at academy level)
            makes him a rare profile in the attacking midfielder market.
          </p>
          <p class="text-white/40 text-sm mt-4 italic">
            "A high-ceiling #10 — technically complete with both feet, physically developing,
            and mentally resilient. The profile European academies are actively seeking."
          </p>

          <!-- Pathway reference -->
          <div class="mt-6 flex items-center gap-3 text-xs text-white/30">
            <div class="w-8 h-px bg-gold/30"></div>
            <span>Following the pathway of <strong class="text-white/50">Victor Wanyama</strong> (Kenya → Belgium at 16 → Celtic → Tottenham Hotspur)</span>
          </div>
        </div>

        <!-- Fact cards (2 cols) -->
        <div class="lg:col-span-2 flex flex-col gap-3">
          <div class="glass-card px-4 py-3 flex justify-between items-center" data-aos="fade-up" data-aos-delay="0">
            <span class="text-white/40 text-xs">Full Name</span>
            <span class="text-white text-xs font-semibold">Joseph Omondi Ojwang</span>
          </div>
          <div class="glass-card px-4 py-3 flex justify-between items-center" data-aos="fade-up" data-aos-delay="50">
            <span class="text-white/40 text-xs">Date of Birth</span>
            <span class="text-white text-xs font-semibold">13 September 2010</span>
          </div>
          <div class="glass-card px-4 py-3 flex justify-between items-center" data-aos="fade-up" data-aos-delay="100">
            <span class="text-white/40 text-xs">Age</span>
            <span class="text-white text-xs font-semibold">15</span>
          </div>
          <div class="glass-card px-4 py-3 flex justify-between items-center" data-aos="fade-up" data-aos-delay="150">
            <span class="text-white/40 text-xs">Position</span>
            <span class="text-gold text-xs font-bold">Attacking Midfielder / #10</span>
          </div>
          <div class="glass-card px-4 py-3 flex justify-between items-center" data-aos="fade-up" data-aos-delay="200">
            <span class="text-white/40 text-xs">Preferred Foot</span>
            <span class="text-white text-xs font-semibold">Both <span class="text-white/40">(R dominant)</span></span>
          </div>
          <div class="glass-card px-4 py-3 flex justify-between items-center" data-aos="fade-up" data-aos-delay="250">
            <span class="text-white/40 text-xs">Nationality</span>
            <span class="text-white text-xs font-semibold">🇰🇪 Kenyan</span>
          </div>
          <div class="glass-card px-4 py-3 flex justify-between items-center" data-aos="fade-up" data-aos-delay="300">
            <span class="text-white/40 text-xs">School</span>
            <span class="text-white text-xs font-semibold">Kitengela International <span class="text-white/40">· Yr 10</span></span>
          </div>
          <div class="glass-card px-4 py-3 flex justify-between items-center border-gold/20" data-aos="fade-up" data-aos-delay="350">
            <span class="text-white/40 text-xs">European Trial</span>
            <span class="text-gold text-xs font-bold">Cambrils UCF 🇪🇸 ✓</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Sections 3-8 will be added in subsequent tasks -->
```

- [ ] **Step 2: Open in browser and verify**

```bash
open index.html
```

Expected: Profile section appears below hero with bio text on the left and 8 fact cards on the right. Cards animate in with staggered delays on scroll.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add Player Profile section with bio and fact cards"
```

---

### Task 4: Spain Trial Section

**Files:**
- Modify: `index.html` (insert after Player Profile section, replacing `<!-- Sections 3-8 -->` comment)

- [ ] **Step 1: Add Spain Trial section HTML**

Replace `<!-- Sections 3-8 will be added in subsequent tasks -->` with:

```html
  <!-- ============================================ -->
  <!-- SECTION 3: SPAIN TRIAL — CAMBRILS UCF        -->
  <!-- ============================================ -->
  <section id="trial" class="py-20 md:py-28 bg-gradient-to-b from-dark-light to-dark-mid relative">
    <div class="container mx-auto px-6 md:px-12 lg:px-20">
      <p class="section-label mb-3" data-aos="fade-up">International Experience</p>
      <h2 class="font-display text-3xl md:text-4xl font-black mb-2" data-aos="fade-up" data-aos-delay="50">
        Successful Trial — Cambrils UCF <span class="text-2xl">🇪🇸</span>
      </h2>
      <p class="text-white/40 text-sm mb-10" data-aos="fade-up" data-aos-delay="100">
        Organized through Kitengela International School — verified institutional pathway
      </p>

      <!-- Image grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div class="rounded-xl overflow-hidden aspect-[4/3]" data-aos="fade-up" data-aos-delay="100">
          <img src="assets/images/trial-certificate.jpeg" alt="Joseph receiving certificate from Cambrils UCF coach" class="w-full h-full object-cover hover:scale-105 transition-transform duration-500" loading="lazy">
        </div>
        <div class="rounded-xl overflow-hidden aspect-[4/3]" data-aos="fade-up" data-aos-delay="200">
          <img src="assets/images/trial-action-1.jpeg" alt="Joseph in match action at Cambrils UCF facilities" class="w-full h-full object-cover hover:scale-105 transition-transform duration-500" loading="lazy">
        </div>
        <div class="rounded-xl overflow-hidden aspect-[4/3]" data-aos="fade-up" data-aos-delay="300">
          <img src="assets/images/trial-team.jpeg" alt="Team photo with Cambrils UCF squad" class="w-full h-full object-cover hover:scale-105 transition-transform duration-500" loading="lazy">
        </div>
      </div>

      <!-- Second row: more trial images -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div class="rounded-xl overflow-hidden aspect-square" data-aos="fade-up" data-aos-delay="150">
          <img src="assets/images/trial-pitch.jpeg" alt="Joseph wearing #10 on the Cambrils pitch" class="w-full h-full object-cover hover:scale-105 transition-transform duration-500" loading="lazy">
        </div>
        <div class="rounded-xl overflow-hidden aspect-square" data-aos="fade-up" data-aos-delay="200">
          <img src="assets/images/trial-huddle.jpeg" alt="Team huddle with Cambrils coach" class="w-full h-full object-cover hover:scale-105 transition-transform duration-500" loading="lazy">
        </div>
        <div class="rounded-xl overflow-hidden aspect-square" data-aos="fade-up" data-aos-delay="250">
          <img src="assets/images/trial-certificate-2.jpeg" alt="Joseph with certificate at JOLIU event" class="w-full h-full object-cover hover:scale-105 transition-transform duration-500" loading="lazy">
        </div>
        <div class="rounded-xl overflow-hidden aspect-square" data-aos="fade-up" data-aos-delay="300">
          <img src="assets/images/trial-gear.jpeg" alt="Receiving equipment at Cambrils facility" class="w-full h-full object-cover hover:scale-105 transition-transform duration-500" loading="lazy">
        </div>
      </div>

      <!-- Club info bar -->
      <div class="glass-card p-4 md:p-5 flex flex-col md:flex-row items-start md:items-center gap-4" data-aos="fade-up" data-aos-delay="400">
        <div class="flex items-center gap-4 flex-1">
          <div class="w-12 h-12 rounded-full bg-gold/10 border-2 border-gold/30 flex items-center justify-center text-2xl flex-shrink-0">
            🇪🇸
          </div>
          <div>
            <p class="text-white font-semibold text-sm">Cambrils Unió Club de Futbol</p>
            <p class="text-white/40 text-xs mt-0.5">Tarragona, Catalonia, Spain · Catalan football pyramid · Est. 2009</p>
            <p class="text-white/30 text-xs mt-0.5">Training in the Catalan positional play methodology — the philosophy behind FC Barcelona's La Masia</p>
          </div>
        </div>
        <div class="bg-gold/10 border border-gold/25 rounded-md px-4 py-2 flex-shrink-0">
          <span class="text-gold text-[10px] font-bold tracking-widest uppercase">Trial Certified</span>
        </div>
      </div>
    </div>
  </section>

  <!-- Sections 4-8 will be added in subsequent tasks -->
```

- [ ] **Step 2: Open in browser and verify**

```bash
open index.html
```

Expected: Trial section with 3 large images (certificate, action, team), 4 smaller images below, and a club info bar at the bottom with certified badge.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add Spain Trial section with Cambrils UCF imagery and club info"
```

---

### Task 5: Performance Data Section

**Files:**
- Modify: `index.html` (insert after Spain Trial section, replace `<!-- Sections 4-8 -->` comment)

- [ ] **Step 1: Add Performance Data section HTML**

Replace `<!-- Sections 4-8 will be added in subsequent tasks -->` with:

```html
  <!-- ============================================ -->
  <!-- SECTION 4: PERFORMANCE DATA                  -->
  <!-- ============================================ -->
  <section id="stats" class="py-20 md:py-28 bg-dark relative">
    <div class="container mx-auto px-6 md:px-12 lg:px-20">
      <!-- Header -->
      <div class="flex flex-col md:flex-row md:items-end md:justify-between gap-4 mb-10">
        <div data-aos="fade-up">
          <p class="section-label mb-3">Performance Metrics</p>
          <h2 class="font-display text-3xl md:text-4xl font-black">Session Snapshot</h2>
        </div>
        <div class="glass-card px-4 py-2 rounded-full text-[10px] text-white/50 tracking-wider flex items-center gap-2" data-aos="fade-up" data-aos-delay="100">
          <span>📊</span>
          <span>SINGLE 149-MIN TECHNICAL SESSION · EARLY INDICATORS</span>
        </div>
      </div>

      <!-- Primary stats grid -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div class="glass-card p-6 text-center" data-aos="fade-up" data-aos-delay="0">
          <div class="font-display text-4xl md:text-5xl font-black stat-number" data-target="352">0</div>
          <p class="text-white/40 text-[10px] tracking-widest uppercase mt-2">Ball Touches</p>
          <p class="text-gold text-[10px] mt-1.5 font-medium">▲ Above avg for age</p>
        </div>
        <div class="glass-card p-6 text-center" data-aos="fade-up" data-aos-delay="100">
          <div class="font-display text-4xl md:text-5xl font-black stat-number" data-target="79.2" data-decimals="1">0</div>
          <p class="text-white/40 text-[10px] tracking-widest uppercase mt-2">Kick Power <span class="text-white/25">(kph)</span></p>
          <p class="text-gold text-[10px] mt-1.5 font-medium">▲ U-16 elite range: 70-85</p>
        </div>
        <div class="glass-card p-6 text-center" data-aos="fade-up" data-aos-delay="200">
          <div class="font-display text-4xl md:text-5xl font-black stat-number" data-target="24.5" data-decimals="1">0</div>
          <p class="text-white/40 text-[10px] tracking-widest uppercase mt-2">Top Speed <span class="text-white/25">(kph)</span></p>
          <p class="text-white/30 text-[10px] mt-1.5">Elite U-16 band: 24-27</p>
        </div>
        <div class="glass-card p-6 text-center" data-aos="fade-up" data-aos-delay="300">
          <div class="font-display text-4xl md:text-5xl font-black stat-number" data-target="33">0</div>
          <p class="text-white/40 text-[10px] tracking-widest uppercase mt-2">Sprints</p>
          <p class="text-white/30 text-[10px] mt-1.5">149 min session</p>
        </div>
      </div>

      <!-- Two-footed breakdown -->
      <div class="glass-card p-6 md:p-8 mb-8" data-aos="fade-up">
        <p class="text-white/50 text-[10px] tracking-widest uppercase mb-6">Two-Footed Ability — <span class="text-gold">Key Differentiator</span></p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12">
          <!-- Left foot -->
          <div class="text-center">
            <div class="flex items-baseline justify-center gap-2">
              <span class="font-display text-3xl font-black">117</span>
              <span class="text-white/40 text-sm">(33%)</span>
            </div>
            <div class="h-1.5 bg-white/[0.08] rounded-full mt-3 overflow-hidden">
              <div class="h-full bg-gradient-to-r from-gold to-gold-dark rounded-full progress-fill" style="width: 0%;" data-width="33%"></div>
            </div>
            <p class="text-white/40 text-xs mt-2">Left Foot · 76.7 kph kick power</p>
            <p class="text-white/25 text-[10px] mt-1">Only 3% drop-off vs. dominant foot (typical: 15-20%)</p>
          </div>
          <!-- Right foot -->
          <div class="text-center">
            <div class="flex items-baseline justify-center gap-2">
              <span class="font-display text-3xl font-black">235</span>
              <span class="text-white/40 text-sm">(67%)</span>
            </div>
            <div class="h-1.5 bg-white/[0.08] rounded-full mt-3 overflow-hidden">
              <div class="h-full bg-gradient-to-r from-gold to-gold-dark rounded-full progress-fill" style="width: 0%;" data-width="67%"></div>
            </div>
            <p class="text-white/40 text-xs mt-2">Right Foot · 79.2 kph kick power
              <span class="inline-block bg-gold text-dark text-[8px] font-bold px-2 py-0.5 rounded ml-2 align-middle">DOMINANT</span>
            </p>
          </div>
        </div>
      </div>

      <!-- Secondary stats -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div class="glass-card p-5 text-center" data-aos="fade-up" data-aos-delay="0">
          <div class="font-display text-2xl font-black">142.2<span class="text-sm text-white/40 ml-1">m</span></div>
          <p class="text-white/40 text-[10px] tracking-widest uppercase mt-1">Sprint Distance</p>
        </div>
        <div class="glass-card p-5 text-center" data-aos="fade-up" data-aos-delay="100">
          <div class="font-display text-2xl font-black">29</div>
          <p class="text-white/40 text-[10px] tracking-widest uppercase mt-1">Accel / Decel</p>
        </div>
        <div class="glass-card p-5 text-center" data-aos="fade-up" data-aos-delay="200">
          <div class="font-display text-2xl font-black">4.9<span class="text-sm text-white/40 ml-1">km</span></div>
          <p class="text-white/40 text-[10px] tracking-widest uppercase mt-1">Total Distance</p>
        </div>
        <div class="glass-card p-5 text-center" data-aos="fade-up" data-aos-delay="300">
          <div class="font-display text-2xl font-black">149<span class="text-sm text-white/40 ml-1">min</span></div>
          <p class="text-white/40 text-[10px] tracking-widest uppercase mt-1">Session Duration</p>
        </div>
      </div>

      <!-- Agility -->
      <div class="glass-card p-6 mb-6" data-aos="fade-up">
        <p class="text-white/50 text-[10px] tracking-widest uppercase mb-4">Agility Profile</p>
        <div class="grid grid-cols-3 gap-4 text-center">
          <div>
            <div class="text-white/30 text-lg mb-1">↰</div>
            <div class="font-display text-xl font-black">19</div>
            <p class="text-white/40 text-[10px] mt-1">Left Turns</p>
          </div>
          <div>
            <div class="text-white/30 text-lg mb-1">↻</div>
            <div class="font-display text-xl font-black">26</div>
            <p class="text-white/40 text-[10px] mt-1">Back Turns</p>
          </div>
          <div>
            <div class="text-white/30 text-lg mb-1">↱</div>
            <div class="font-display text-xl font-black">23</div>
            <p class="text-white/40 text-[10px] mt-1">Right Turns</p>
          </div>
        </div>
      </div>

      <!-- Contextual note -->
      <p class="text-white/25 text-xs text-center" data-aos="fade-up">
        Data captured from a single technical training session. Full match analytics and additional session data available on request.
      </p>
    </div>
  </section>

  <!-- Sections 5-8 will be added in subsequent tasks -->
```

- [ ] **Step 2: Add counter animation and progress bar JavaScript**

Find the existing `<script>` block at the bottom of the file (the one that initializes AOS) and replace it with:

```html
  <script>
    // Initialize AOS
    AOS.init({
      duration: 700,
      once: true,
      offset: 80,
    });

    // Counter animation for stat numbers
    function animateCounters() {
      const counters = document.querySelectorAll('.stat-number');
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const el = entry.target;
            const target = parseFloat(el.dataset.target);
            const decimals = parseInt(el.dataset.decimals || '0');
            const duration = 1500;
            const start = performance.now();

            function update(now) {
              const elapsed = now - start;
              const progress = Math.min(elapsed / duration, 1);
              const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
              const current = eased * target;
              el.textContent = current.toFixed(decimals);
              if (progress < 1) requestAnimationFrame(update);
            }
            requestAnimationFrame(update);
            observer.unobserve(el);
          }
        });
      }, { threshold: 0.3 });

      counters.forEach(counter => observer.observe(counter));
    }

    // Progress bar fill animation
    function animateProgressBars() {
      const bars = document.querySelectorAll('.progress-fill');
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const el = entry.target;
            el.style.width = el.dataset.width;
            observer.unobserve(el);
          }
        });
      }, { threshold: 0.3 });

      bars.forEach(bar => observer.observe(bar));
    }

    // Initialize on DOM ready
    document.addEventListener('DOMContentLoaded', () => {
      animateCounters();
      animateProgressBars();
    });
  </script>
```

- [ ] **Step 3: Open in browser and verify**

```bash
open index.html
```

Expected: Stats section with counters animating from 0 to final values on scroll, progress bars filling, agility turns displayed. Pill badge shows "SINGLE 149-MIN TECHNICAL SESSION".

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: add Performance Data section with animated counters and progress bars"
```

---

### Task 6: Video Highlights Section

**Files:**
- Modify: `index.html` (insert after Performance Data section, replace `<!-- Sections 5-8 -->` comment)

- [ ] **Step 1: Add Video Highlights section HTML**

Replace `<!-- Sections 5-8 will be added in subsequent tasks -->` with:

```html
  <!-- ============================================ -->
  <!-- SECTION 5: VIDEO HIGHLIGHTS                  -->
  <!-- ============================================ -->
  <section id="highlights" class="py-20 md:py-28 bg-dark-light relative">
    <div class="container mx-auto px-6 md:px-12 lg:px-20">
      <p class="section-label mb-3" data-aos="fade-up">Match Footage</p>
      <h2 class="font-display text-3xl md:text-4xl font-black mb-2" data-aos="fade-up" data-aos-delay="50">See Him Play</h2>
      <p class="text-white/40 text-sm mb-10" data-aos="fade-up" data-aos-delay="100">Training sessions and match highlights — movement, technique, and decision-making</p>

      <!-- Featured video -->
      <div class="mb-8 rounded-2xl overflow-hidden" data-aos="fade-up">
        <div class="relative video-card cursor-pointer group">
          <video class="w-full aspect-video object-cover bg-dark" preload="metadata" controls>
            <source src="assets/videos/highlight-01.mp4" type="video/mp4">
          </video>
        </div>
      </div>

      <!-- Video grid -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="rounded-xl overflow-hidden" data-aos="fade-up" data-aos-delay="50">
          <div class="relative video-card">
            <video class="w-full aspect-video object-cover bg-dark" preload="metadata" controls>
              <source src="assets/videos/highlight-02.mp4" type="video/mp4">
            </video>
          </div>
        </div>
        <div class="rounded-xl overflow-hidden" data-aos="fade-up" data-aos-delay="100">
          <div class="relative video-card">
            <video class="w-full aspect-video object-cover bg-dark" preload="metadata" controls>
              <source src="assets/videos/highlight-03.mp4" type="video/mp4">
            </video>
          </div>
        </div>
        <div class="rounded-xl overflow-hidden" data-aos="fade-up" data-aos-delay="150">
          <div class="relative video-card">
            <video class="w-full aspect-video object-cover bg-dark" preload="metadata" controls>
              <source src="assets/videos/highlight-04.mp4" type="video/mp4">
            </video>
          </div>
        </div>
        <div class="rounded-xl overflow-hidden" data-aos="fade-up" data-aos-delay="200">
          <div class="relative video-card">
            <video class="w-full aspect-video object-cover bg-dark" preload="metadata" controls>
              <source src="assets/videos/highlight-05.mp4" type="video/mp4">
            </video>
          </div>
        </div>
        <div class="rounded-xl overflow-hidden" data-aos="fade-up" data-aos-delay="250">
          <div class="relative video-card">
            <video class="w-full aspect-video object-cover bg-dark" preload="metadata" controls>
              <source src="assets/videos/highlight-06.mp4" type="video/mp4">
            </video>
          </div>
        </div>
        <div class="rounded-xl overflow-hidden" data-aos="fade-up" data-aos-delay="300">
          <div class="relative video-card">
            <video class="w-full aspect-video object-cover bg-dark" preload="metadata" controls>
              <source src="assets/videos/highlight-07.mp4" type="video/mp4">
            </video>
          </div>
        </div>
        <div class="rounded-xl overflow-hidden" data-aos="fade-up" data-aos-delay="350">
          <div class="relative video-card">
            <video class="w-full aspect-video object-cover bg-dark" preload="metadata" controls>
              <source src="assets/videos/highlight-08.mp4" type="video/mp4">
            </video>
          </div>
        </div>
        <div class="rounded-xl overflow-hidden" data-aos="fade-up" data-aos-delay="400">
          <div class="relative video-card">
            <video class="w-full aspect-video object-cover bg-dark" preload="metadata" controls>
              <source src="assets/videos/highlight-09.mp4" type="video/mp4">
            </video>
          </div>
        </div>
        <div class="rounded-xl overflow-hidden" data-aos="fade-up" data-aos-delay="450">
          <div class="relative video-card">
            <video class="w-full aspect-video object-cover bg-dark" preload="metadata" controls>
              <source src="assets/videos/highlight-10.mp4" type="video/mp4">
            </video>
          </div>
        </div>
        <div class="rounded-xl overflow-hidden" data-aos="fade-up" data-aos-delay="500">
          <div class="relative video-card">
            <video class="w-full aspect-video object-cover bg-dark" preload="metadata" controls>
              <source src="assets/videos/highlight-11.mp4" type="video/mp4">
            </video>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Sections 6-8 will be added in subsequent tasks -->
```

- [ ] **Step 2: Open in browser and verify**

```bash
open index.html
```

Expected: Featured video large at top, grid of 10 smaller videos below, all with native HTML5 controls. Videos stagger in on scroll.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add Video Highlights section with featured video and grid"
```

---

### Task 7: Photo Gallery Section

**Files:**
- Modify: `index.html` (insert after Video Highlights section, replace `<!-- Sections 6-8 -->` comment)

- [ ] **Step 1: Add Photo Gallery section HTML**

Replace `<!-- Sections 6-8 will be added in subsequent tasks -->` with:

```html
  <!-- ============================================ -->
  <!-- SECTION 6: PHOTO GALLERY                     -->
  <!-- ============================================ -->
  <section id="gallery" class="py-20 md:py-28 bg-dark relative">
    <div class="container mx-auto px-6 md:px-12 lg:px-20">
      <p class="section-label mb-3" data-aos="fade-up">Gallery</p>
      <h2 class="font-display text-3xl md:text-4xl font-black mb-2" data-aos="fade-up" data-aos-delay="50">On & Off the Pitch</h2>
      <p class="text-white/40 text-sm mb-10" data-aos="fade-up" data-aos-delay="100">Match action, training, and life in Spain</p>

      <!-- Masonry-style grid -->
      <div class="columns-2 md:columns-3 lg:columns-4 gap-4 space-y-4">
        <a href="assets/images/action-kick.jpeg" class="glightbox gallery-item block rounded-xl overflow-hidden" data-gallery="portfolio" data-aos="fade-up" data-aos-delay="50">
          <img src="assets/images/action-kick.jpeg" alt="Joseph striking the ball wearing #10" class="w-full object-cover" loading="lazy">
        </a>
        <a href="assets/images/hero-portrait.jpeg" class="glightbox gallery-item block rounded-xl overflow-hidden" data-gallery="portfolio" data-aos="fade-up" data-aos-delay="100">
          <img src="assets/images/hero-portrait.jpeg" alt="Joseph off the pitch in Spain" class="w-full object-cover" loading="lazy">
        </a>
        <a href="assets/images/trial-certificate.jpeg" class="glightbox gallery-item block rounded-xl overflow-hidden" data-gallery="portfolio" data-aos="fade-up" data-aos-delay="150">
          <img src="assets/images/trial-certificate.jpeg" alt="Receiving certificate from coach" class="w-full object-cover" loading="lazy">
        </a>
        <a href="assets/images/action-goal.jpeg" class="glightbox gallery-item block rounded-xl overflow-hidden" data-gallery="portfolio" data-aos="fade-up" data-aos-delay="200">
          <img src="assets/images/action-goal.jpeg" alt="Goal-scoring action" class="w-full object-cover" loading="lazy">
        </a>
        <a href="assets/images/trial-pitch.jpeg" class="glightbox gallery-item block rounded-xl overflow-hidden" data-gallery="portfolio" data-aos="fade-up" data-aos-delay="100">
          <img src="assets/images/trial-pitch.jpeg" alt="Joseph on the Cambrils pitch" class="w-full object-cover" loading="lazy">
        </a>
        <a href="assets/images/portrait-1.jpeg" class="glightbox gallery-item block rounded-xl overflow-hidden" data-gallery="portfolio" data-aos="fade-up" data-aos-delay="150">
          <img src="assets/images/portrait-1.jpeg" alt="Joseph portrait" class="w-full object-cover" loading="lazy">
        </a>
        <a href="assets/images/trial-action-1.jpeg" class="glightbox gallery-item block rounded-xl overflow-hidden" data-gallery="portfolio" data-aos="fade-up" data-aos-delay="200">
          <img src="assets/images/trial-action-1.jpeg" alt="Match action at Cambrils" class="w-full object-cover" loading="lazy">
        </a>
        <a href="assets/images/trial-huddle.jpeg" class="glightbox gallery-item block rounded-xl overflow-hidden" data-gallery="portfolio" data-aos="fade-up" data-aos-delay="250">
          <img src="assets/images/trial-huddle.jpeg" alt="Team huddle" class="w-full object-cover" loading="lazy">
        </a>
        <a href="assets/images/action-control.jpeg" class="glightbox gallery-item block rounded-xl overflow-hidden" data-gallery="portfolio" data-aos="fade-up" data-aos-delay="100">
          <img src="assets/images/action-control.jpeg" alt="Ball control in training" class="w-full object-cover" loading="lazy">
        </a>
        <a href="assets/images/portrait-2.jpeg" class="glightbox gallery-item block rounded-xl overflow-hidden" data-gallery="portfolio" data-aos="fade-up" data-aos-delay="150">
          <img src="assets/images/portrait-2.jpeg" alt="Joseph portrait with sunglasses" class="w-full object-cover" loading="lazy">
        </a>
        <a href="assets/images/trial-team.jpeg" class="glightbox gallery-item block rounded-xl overflow-hidden" data-gallery="portfolio" data-aos="fade-up" data-aos-delay="200">
          <img src="assets/images/trial-team.jpeg" alt="Team photo at Cambrils" class="w-full object-cover" loading="lazy">
        </a>
        <a href="assets/images/team-local.jpeg" class="glightbox gallery-item block rounded-xl overflow-hidden" data-gallery="portfolio" data-aos="fade-up" data-aos-delay="250">
          <img src="assets/images/team-local.jpeg" alt="Joseph's local team in Kenya" class="w-full object-cover" loading="lazy">
        </a>
        <a href="assets/images/trial-certificate-2.jpeg" class="glightbox gallery-item block rounded-xl overflow-hidden" data-gallery="portfolio" data-aos="fade-up" data-aos-delay="100">
          <img src="assets/images/trial-certificate-2.jpeg" alt="Certificate at JOLIU event" class="w-full object-cover" loading="lazy">
        </a>
        <a href="assets/images/trial-gear.jpeg" class="glightbox gallery-item block rounded-xl overflow-hidden" data-gallery="portfolio" data-aos="fade-up" data-aos-delay="150">
          <img src="assets/images/trial-gear.jpeg" alt="Receiving gear at Cambrils" class="w-full object-cover" loading="lazy">
        </a>
      </div>
    </div>
  </section>

  <!-- Sections 7-8 will be added in subsequent tasks -->
```

- [ ] **Step 2: Initialize GLightbox in the script section**

In the `<script>` block at the bottom, add GLightbox initialization inside the `DOMContentLoaded` callback, after `animateProgressBars();`:

```javascript
    // Initialize GLightbox
    const lightbox = GLightbox({
      touchNavigation: true,
      loop: true,
      skin: 'clean',
    });
```

- [ ] **Step 3: Open in browser and verify**

```bash
open index.html
```

Expected: Masonry grid of images, clicking any image opens GLightbox overlay with navigation. Images animate in on scroll.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: add Photo Gallery section with masonry grid and GLightbox"
```

---

### Task 8: The Dream Section

**Files:**
- Modify: `index.html` (insert after Photo Gallery section, replace `<!-- Sections 7-8 -->` comment)

- [ ] **Step 1: Add The Dream section HTML**

Replace `<!-- Sections 7-8 will be added in subsequent tasks -->` with:

```html
  <!-- ============================================ -->
  <!-- SECTION 7: THE DREAM                         -->
  <!-- ============================================ -->
  <section id="dream" class="py-24 md:py-32 bg-gradient-to-b from-dark via-[#12091e] to-dark relative overflow-hidden">
    <!-- Subtle background glow -->
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(255,215,0,0.04)_0%,transparent_60%)]"></div>

    <div class="container mx-auto px-6 md:px-12 lg:px-20 relative z-10 text-center">
      <p class="section-label mb-4" data-aos="fade-up">The Dream</p>
      <h2 class="font-display text-3xl md:text-5xl font-black mb-4" data-aos="fade-up" data-aos-delay="100">
        "Standing Where Legends Stood"
      </h2>
      <p class="text-white/40 text-sm md:text-base max-w-xl mx-auto mb-10" data-aos="fade-up" data-aos-delay="200">
        Joseph at Camp Nou, in front of Messi's Ballon d'Or collection — the same #10 that inspires his game.
        From Kitengela to Catalonia, the journey has begun.
      </p>

      <!-- Camp Nou photo -->
      <div class="max-w-xs mx-auto" data-aos="fade-up" data-aos-delay="300">
        <div class="relative">
          <div class="absolute -inset-3 bg-gradient-to-br from-gold/15 to-gold/5 rounded-2xl blur-xl"></div>
          <img
            src="assets/images/campnou.jpeg"
            alt="Joseph Ojwang at Camp Nou in front of Messi's Ballon d'Or trophies"
            class="relative w-full rounded-2xl shadow-2xl shadow-gold/10"
            loading="lazy"
          >
        </div>
      </div>

      <!-- Caption -->
      <p class="text-white/25 text-xs mt-8 tracking-wider" data-aos="fade-up" data-aos-delay="400">
        His #10 · Messi's #10 · The number that carries dreams
      </p>

      <!-- Trailblazers note -->
      <div class="mt-12 max-w-lg mx-auto" data-aos="fade-up" data-aos-delay="500">
        <div class="glass-card p-5 text-left">
          <p class="text-white/50 text-[10px] tracking-widest uppercase mb-3">Kenyan Trailblazers Before Him</p>
          <div class="space-y-2 text-xs">
            <div class="flex items-center gap-3">
              <span class="text-gold font-bold w-5">→</span>
              <span class="text-white/60"><strong class="text-white">Victor Wanyama</strong> — Kenya → Belgium (age 16) → Celtic → Southampton → Tottenham Hotspur</span>
            </div>
            <div class="flex items-center gap-3">
              <span class="text-gold font-bold w-5">→</span>
              <span class="text-white/60"><strong class="text-white">McDonald Mariga</strong> — First Kenyan in the UEFA Champions League (Inter Milan, 2010)</span>
            </div>
            <div class="flex items-center gap-3">
              <span class="text-gold font-bold w-5">→</span>
              <span class="text-white/60"><strong class="text-white">Michael Olunga</strong> — Kenya → Sweden → La Liga (Girona) → Top scorer</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Section 8 will be added in the next task -->
```

- [ ] **Step 2: Open in browser and verify**

```bash
open index.html
```

Expected: Emotional section with purple-dark gradient, Camp Nou photo centered with gold glow border, quote heading, and Kenyan trailblazers card below.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add The Dream section with Camp Nou imagery and trailblazers"
```

---

### Task 9: Contact Section + Footer

**Files:**
- Modify: `index.html` (insert after The Dream section, replace `<!-- Section 8 -->` comment)

- [ ] **Step 1: Add Contact section and footer HTML**

Replace `<!-- Section 8 will be added in the next task -->` with:

```html
  <!-- ============================================ -->
  <!-- SECTION 8: CONTACT                           -->
  <!-- ============================================ -->
  <section id="contact" class="py-20 md:py-28 bg-dark-light relative">
    <div class="container mx-auto px-6 md:px-12 lg:px-20">
      <div class="max-w-lg mx-auto text-center">
        <p class="section-label mb-3" data-aos="fade-up">Get in Touch</p>
        <h2 class="font-display text-3xl md:text-4xl font-black mb-3" data-aos="fade-up" data-aos-delay="50">
          Interested in Joseph?
        </h2>
        <p class="text-white/40 text-sm mb-10" data-aos="fade-up" data-aos-delay="100">
          Contact his representative for full match footage, physical assessments, and availability.
        </p>

        <!-- Contact form -->
        <form action="https://formsubmit.co/oluwamartin@gmail.com" method="POST" class="space-y-4 text-left">
          <!-- FormSubmit config -->
          <input type="hidden" name="_subject" value="Scout Enquiry — Joseph Ojwang Portfolio">
          <input type="hidden" name="_captcha" value="false">
          <input type="hidden" name="_template" value="box">

          <div data-aos="fade-up" data-aos-delay="150">
            <input
              type="text" name="name" required
              placeholder="Your Name"
              class="w-full bg-white/[0.04] border border-white/[0.08] rounded-lg px-5 py-3.5 text-white text-sm placeholder-white/30 focus:outline-none focus:border-gold/50 focus:ring-1 focus:ring-gold/30 transition-colors"
            >
          </div>
          <div data-aos="fade-up" data-aos-delay="200">
            <input
              type="email" name="email" required
              placeholder="Email Address"
              class="w-full bg-white/[0.04] border border-white/[0.08] rounded-lg px-5 py-3.5 text-white text-sm placeholder-white/30 focus:outline-none focus:border-gold/50 focus:ring-1 focus:ring-gold/30 transition-colors"
            >
          </div>
          <div data-aos="fade-up" data-aos-delay="250">
            <input
              type="text" name="organization"
              placeholder="Organization / Club (optional)"
              class="w-full bg-white/[0.04] border border-white/[0.08] rounded-lg px-5 py-3.5 text-white text-sm placeholder-white/30 focus:outline-none focus:border-gold/50 focus:ring-1 focus:ring-gold/30 transition-colors"
            >
          </div>
          <div data-aos="fade-up" data-aos-delay="300">
            <textarea
              name="message" rows="4" required
              placeholder="Your Message"
              class="w-full bg-white/[0.04] border border-white/[0.08] rounded-lg px-5 py-3.5 text-white text-sm placeholder-white/30 focus:outline-none focus:border-gold/50 focus:ring-1 focus:ring-gold/30 transition-colors resize-none"
            ></textarea>
          </div>
          <div data-aos="fade-up" data-aos-delay="350">
            <button
              type="submit"
              class="w-full bg-gold text-dark font-bold text-xs tracking-widest py-4 rounded-lg hover:bg-gold-light transition-colors duration-300"
            >
              SEND ENQUIRY
            </button>
          </div>
        </form>

        <!-- Direct contact -->
        <div class="mt-10 glass-card p-5" data-aos="fade-up" data-aos-delay="400">
          <p class="text-white/50 text-[10px] tracking-widest uppercase mb-3">Direct Contact</p>
          <div class="space-y-2">
            <div class="flex items-center justify-center gap-3 text-sm">
              <span class="text-gold">Agent:</span>
              <span class="text-white font-medium">Martin Lugendo</span>
            </div>
            <div class="flex items-center justify-center gap-3 text-sm">
              <span class="text-gold">Email:</span>
              <a href="mailto:oluwamartin@gmail.com" class="text-white/70 hover:text-gold transition-colors">oluwamartin@gmail.com</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ============================================ -->
  <!-- FOOTER                                       -->
  <!-- ============================================ -->
  <footer class="py-8 bg-dark border-t border-white/[0.04]">
    <div class="container mx-auto px-6 md:px-12 lg:px-20 text-center">
      <p class="text-white/20 text-xs">
        &copy; 2026 Joseph Ojwang · Player Portfolio · Represented by Martin Lugendo
      </p>
    </div>
  </footer>
```

- [ ] **Step 2: Open in browser and verify**

```bash
open index.html
```

Expected: Contact form with Name, Email, Organization, Message fields and gold Submit button. Direct contact card below with Martin Lugendo's info. Footer at bottom. Form submits to FormSubmit.co service (will redirect to confirmation on submit).

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add Contact section with form and footer"
```

---

### Task 10: Navigation Bar + Final Polish

**Files:**
- Modify: `index.html` (add sticky nav at top of `<body>`, add smooth scroll anchors)

- [ ] **Step 1: Add sticky navigation bar**

Add the following immediately after the `<body>` opening tag, before the Hero section:

```html
  <!-- ============================================ -->
  <!-- NAVIGATION                                   -->
  <!-- ============================================ -->
  <nav id="navbar" class="fixed top-0 left-0 right-0 z-50 transition-all duration-300 bg-dark/80 backdrop-blur-md border-b border-white/[0.04]">
    <div class="container mx-auto px-6 md:px-12 lg:px-20 flex items-center justify-between h-14">
      <a href="#hero" class="font-display text-lg font-black tracking-tight">
        <span class="text-white">J.</span><span class="text-gold">OJWANG</span>
        <span class="text-white/20 text-xs font-body font-normal ml-2 hidden sm:inline">#10</span>
      </a>
      <div class="hidden md:flex items-center gap-6">
        <a href="#profile" class="text-white/40 text-xs tracking-wider hover:text-gold transition-colors">Profile</a>
        <a href="#trial" class="text-white/40 text-xs tracking-wider hover:text-gold transition-colors">Trial</a>
        <a href="#stats" class="text-white/40 text-xs tracking-wider hover:text-gold transition-colors">Stats</a>
        <a href="#highlights" class="text-white/40 text-xs tracking-wider hover:text-gold transition-colors">Videos</a>
        <a href="#gallery" class="text-white/40 text-xs tracking-wider hover:text-gold transition-colors">Gallery</a>
        <a href="#contact" class="bg-gold/10 text-gold text-xs font-semibold tracking-wider px-4 py-1.5 rounded-md hover:bg-gold/20 transition-colors">Contact</a>
      </div>
      <!-- Mobile menu button -->
      <button id="mobile-menu-btn" class="md:hidden text-white/60 hover:text-gold transition-colors">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path id="menu-icon" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
        </svg>
      </button>
    </div>
    <!-- Mobile menu -->
    <div id="mobile-menu" class="md:hidden hidden bg-dark/95 backdrop-blur-md border-t border-white/[0.04]">
      <div class="container mx-auto px-6 py-4 flex flex-col gap-3">
        <a href="#profile" class="text-white/50 text-sm py-2 hover:text-gold transition-colors mobile-nav-link">Profile</a>
        <a href="#trial" class="text-white/50 text-sm py-2 hover:text-gold transition-colors mobile-nav-link">Spain Trial</a>
        <a href="#stats" class="text-white/50 text-sm py-2 hover:text-gold transition-colors mobile-nav-link">Stats</a>
        <a href="#highlights" class="text-white/50 text-sm py-2 hover:text-gold transition-colors mobile-nav-link">Videos</a>
        <a href="#gallery" class="text-white/50 text-sm py-2 hover:text-gold transition-colors mobile-nav-link">Gallery</a>
        <a href="#contact" class="text-gold text-sm py-2 font-semibold mobile-nav-link">Contact Agent</a>
      </div>
    </div>
  </nav>
```

- [ ] **Step 2: Add mobile menu toggle and scroll-aware nav JavaScript**

Add this to the bottom of the existing `DOMContentLoaded` callback in the `<script>` block:

```javascript
    // Mobile menu toggle
    const menuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');

    menuBtn.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
      const isOpen = !mobileMenu.classList.contains('hidden');
      menuIcon.setAttribute('d', isOpen
        ? 'M6 18L18 6M6 6l12 12'
        : 'M4 6h16M4 12h16M4 18h16'
      );
    });

    // Close mobile menu on link click
    document.querySelectorAll('.mobile-nav-link').forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.add('hidden');
        menuIcon.setAttribute('d', 'M4 6h16M4 12h16M4 18h16');
      });
    });
```

- [ ] **Step 3: Add padding-top to hero section for nav offset**

In the Hero section's opening `<section>` tag, add `pt-14` to account for the fixed navbar:

Change:
```html
<section id="hero" class="relative min-h-screen flex items-center gold-glow overflow-hidden">
```
To:
```html
<section id="hero" class="relative min-h-screen flex items-center gold-glow overflow-hidden pt-14">
```

- [ ] **Step 4: Open in browser and verify the complete site**

```bash
open index.html
```

Full verification checklist:
- Sticky nav visible at top with logo and section links
- Mobile hamburger menu works (resize browser to test)
- All nav links scroll smoothly to correct sections
- Hero section: portrait visible, gold text, CTAs work
- Profile: bio + 8 fact cards animate on scroll
- Spain Trial: 7 images + club info bar
- Stats: counters animate from 0, progress bars fill
- Videos: featured + 10 thumbnails play
- Gallery: masonry grid, lightbox opens on click
- Dream: Camp Nou photo with gold glow
- Contact: form fields, submit button, direct contact card
- Footer at bottom

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "feat: add sticky navigation with mobile menu and final polish"
```

---

## Completion

After all 10 tasks, the deliverable is:
- `index.html` — fully self-contained single-page portfolio
- `assets/images/` — 20 organized images
- `assets/videos/` — 11 highlight clips

The site works by simply opening `index.html` in any browser. No build step, no server required. Ready to deploy to GitHub Pages, Netlify, or Vercel, or share the folder directly.
