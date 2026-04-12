# Joseph Ojwang — Player Portfolio Website

## Overview

A single-page, scroll-driven portfolio website to showcase Joseph Omondi Ojwang to professional football scouts. The site positions Joseph as a high-ceiling attacking talent with verified European trial experience, backed by hard performance data and compelling visual storytelling.

**Target audience:** Professional football scouts, club talent acquisition departments, and academy recruiters — primarily in Europe.

**Core goal:** A scout receives a link, opens it on mobile or desktop, and within 60 seconds understands who Joseph is, sees proof of his ability, watches him play, and knows how to make contact.

## Player Profile

- **Full Name:** Joseph Omondi Ojwang
- **Date of Birth:** 13 September 2010 (Age 15)
- **Nationality:** Kenyan
- **Position:** Attacking Midfielder / #10
- **Preferred Foot:** Right (dominant), strong left foot — two-footed player
- **Current School:** Kitengela International, Year 10
- **Trial Experience:** Successful trial at Cambrils UCF (Cambrils, Tarragona, Spain, 2026) — organized through Kitengela International

## Tech Stack

- **Structure:** Single `index.html` file
- **Styling:** Tailwind CSS v3 (CDN link)
- **Animations:** AOS (Animate On Scroll) library (CDN) + custom CSS transitions
- **Video:** Native HTML5 `<video>` elements
- **Gallery:** CSS Grid layout + lightweight lightbox (GLightbox CDN)
- **Icons:** Lucide Icons (CDN)
- **Fonts:** Google Fonts — Inter (body) + Oswald (headings/display)
- **No build step.** No frameworks. No dependencies to install. Open the file and it works.

## Visual Design

**Direction:** Dark Cinematic + Clean Athletic hybrid

- **Base:** Dark background (#0a0a0f to #111827 gradients)
- **Primary accent:** Gold (#ffd700) — elite aspiration, used for section labels, highlights, CTAs
- **Text:** White (#ffffff) for headings, rgba(255,255,255,0.5-0.7) for body
- **Data cards:** Subtle glass-morphism — rgba(255,255,255,0.04) background, 1px border rgba(255,255,255,0.08), rounded corners
- **Typography:** Oswald 900 weight for display text (name, section headers), Inter 400/600 for body and data labels
- **Spacing:** Generous whitespace, sections clearly separated

## Page Sections (Scroll Order)

### Section 1: Hero (Full Viewport)

**Purpose:** The 15-second hook. A scout decides to keep scrolling or close the tab here.

**Layout:**
- Full viewport height (100vh)
- Left side: Position label ("Attacking Midfielder · #10"), name treatment (JOSEPH in white, OJWANG in gold), DOB/age/nationality line, two CTA buttons ("View Highlights" gold filled, "Contact" outline)
- Right side: Joseph's portrait photo (one of the Spain lifestyle shots — black hoodie, sunglasses), faded gold #10 watermark behind
- Bottom center: "Scroll to Discover" indicator with animated arrow
- Background: Subtle radial gold glow from left side

**Animations:**
- Name text: fade-in + slide-right (0.6s)
- Portrait: scale from 0.95 to 1.0 with fade (0.8s, 0.2s delay)
- CTA buttons: fade-up (0.4s, 0.6s delay)
- Scroll indicator: infinite bounce animation

**Responsive (mobile):**
- Stack vertically: photo on top (60vh with gradient overlay), text overlaid at bottom
- Name font size reduced
- CTAs full width

### Section 2: Player Profile

**Purpose:** Who is he? Quick-reference facts and a scout-language bio.

**Layout:**
- Left side (60%): Bio paragraph written in scout terminology — "press-resistant attacking midfielder", "plays vertical", "carries into half-spaces", "high ceiling". Mentions Kitengela International (Year 10) and the Spain trial as credibility anchors.
- Right side (40%): Stacked fact cards — Full Name, Date of Birth, Age, Position (AM / #10 in gold), Preferred Foot (Both, R dominant), Nationality (Kenyan flag), School (Kitengela International, Year 10)
- Each fact card: dark glass background, label left, value right

**Animations:** Fade-up for bio text, staggered fade-up for each fact card (100ms delay between each)

### Section 3: Spain Trial — Cambrils UCF

**Purpose:** The credibility anchor. Verified European club exposure at age 15, organized through his school.

**Layout:**
- Section header: "International Experience" label, "Successful Trial — Cambrils UCF" heading with Spanish flag
- Subheading note: "Organized through Kitengela International School"
- 3-column image grid: certificate photo with coach, match action at Cambrils facilities, team photo with both squads
- Bottom: Club info bar — Cambrils UCF details (location, est. 2009, followers count), "CERTIFIED" badge
- Images from gallery: certificate with coach (JOLIU event), match action (white vs yellow/black kits), team group photo, Joseph in #10 on the pitch

**Animations:** Images slide-up with staggered delays, club info bar fades in last

### Section 4: Performance Data

**Purpose:** Hard numbers that build credibility. Clearly framed as a single-session snapshot to imply much higher ceiling.

**Layout:**
- Header row: "Performance Metrics" label, "Session Snapshot" heading, pill badge reading "Single 149-min Technical Session · Early Indicators"
- 4-column stat grid: Ball Touches (352, above avg), Kick Power (79.2 kph, above avg), Top Speed (24.5 kph), Sprints (33)
- Two-Footed breakdown: side-by-side with progress bars — Left Foot (117 touches, 33%, 76.7 kph) | Right Foot (235 touches, 67%, 79.2 kph, DOMINANT badge)
- Secondary stats row: Sprint Distance (142.2m), Accel/Decel (29), Total Distance (4.9 km)
- Agility section: Left turns (19), Back turns (26), Right turns (23)
- Contextual note at bottom: "Data captured from a single technical training session. Full match analytics and additional session data available on request."

**Animations:**
- Stat numbers: counter animation from 0 to final value (1.5s ease-out) triggered on scroll into view
- Progress bars: width animation from 0% to target (1s, 0.3s delay after counter)
- Cards: staggered fade-up

### Section 5: Video Highlights

**Purpose:** Scouts must see movement, decision-making, and technique. This is non-negotiable.

**Layout:**
- Header: "Match Footage" label, "See Him Play" heading
- Featured video: large player at top (one of the best clips selected as hero), 16:9 ratio, play button overlay
- Grid below: 4-column grid of remaining video thumbnails, each with play button overlay and hover effect
- Videos sourced from jose-gallery (11 .mp4 files)
- Videos play inline with native HTML5 controls

**Animations:** Featured video fade-in, grid items staggered fade-up

### Section 6: Photo Gallery

**Purpose:** Visual proof across contexts — match action, training, lifestyle, personality.

**Layout:**
- Header: "Gallery" label, "On & Off the Pitch" heading
- Masonry-style CSS grid (4 columns desktop, 2 mobile) with varying row spans for visual interest
- Images include: action shots (#10 striking ball, match play), training photos, team photos, lifestyle/portrait shots from Spain, equipment distribution
- Click any image to open in GLightbox overlay with navigation
- 20 images total from jose-gallery

**Animations:** Staggered reveal — each image fades in with a random short delay (50-200ms between items)

### Section 7: The Dream

**Purpose:** Emotional closer. Connects Joseph's ambition to the highest level of football.

**Layout:**
- Full-width section with deeper purple-dark gradient background
- Centered layout: "The Dream" label, quote heading "Standing Where Legends Stood"
- Joseph's Camp Nou photo (in front of Messi's Ballon d'Or trophies and #10 jersey) — centered, with subtle gold border glow
- Caption: connecting his #10 to Messi's #10, his ambition to the elite level
- This section uses slightly different background tone to create emotional shift

**Animations:** Slow fade-in (1.2s), slight parallax scroll effect on the image

### Section 8: Contact

**Purpose:** The conversion point. Everything above is wasted without an easy way to reach out.

**Layout:**
- Centered: "Get in Touch" label, "Interested in Joseph?" heading, subtitle about contacting his representative
- Contact form (centered, max-width 500px): Name, Email, Organization/Club, Message, gold "Send Enquiry" button
- Note: form will use mailto: or a simple form service (Formspree/FormSubmit) — no backend needed
- Below form: direct contact details for coach/guardian (phone, email, WhatsApp) — to be provided by user
- Footer: small copyright line

**Animations:** Form fields slide-up sequentially (100ms delay each)

## Image & Media Organization

All media files are currently in `jose-gallery/` with WhatsApp naming. During implementation:

1. Create an `assets/images/` directory with renamed, organized files:
   - `hero-portrait.jpeg` — best lifestyle shot for hero section
   - `trial-certificate.jpeg` — certificate photo with coach
   - `trial-action-1.jpeg`, `trial-action-2.jpeg` — match action at Cambrils
   - `trial-team.jpeg` — group photo with both squads
   - `trial-pitch.jpeg` — Joseph in #10 on the Cambrils pitch
   - `trial-gear.jpeg` — receiving equipment
   - `action-*.jpeg` — on-pitch action shots
   - `team-local.jpeg` — Kenyan team photo
   - `campnou.jpeg` — FC Barcelona museum photo
   - `portrait-*.jpeg` — lifestyle/off-pitch photos
2. Create `assets/videos/` with renamed video files
3. Optimize images for web (compress, appropriate sizing)

## Scout-Language Copy Guidelines

The bio and descriptive text should use terminology that resonates with professional scouts:

- "Press-resistant" — comfortable on the ball under pressure
- "Plays vertical" / "forward-thinking" — looks to progress play, not sideways
- "Carries into half-spaces" — takes the ball into dangerous areas between defense and midfield
- "High ceiling" — significant room for development beyond current level
- "Technically gifted with both feet" — rare at any level, exceptional at 15
- "Tactically mature" — reads the game, makes intelligent decisions
- "Adaptable" — demonstrated by performing in an unfamiliar European environment

Avoid vague terms like "talented", "gifted", or "amazing". Specificity signals credibility.

## Responsive Design

- **Desktop (1024px+):** Full layouts as described, side-by-side content
- **Tablet (768-1023px):** Reduce grid columns (4→3 or 2), stack hero content
- **Mobile (< 768px):** Single column, stacked sections, full-width images, hamburger nav (if nav exists), touch-friendly video controls

## Performance

- Tailwind CSS via CDN (no purge needed for single file)
- Images lazy-loaded (`loading="lazy"`)
- Videos load on interaction (poster frame shown, load on play)
- AOS library initialized once on DOMContentLoaded
- Target: under 3s first meaningful paint on 4G mobile

## Deployment

Static files — deploy to any static host:
- GitHub Pages (free, easy)
- Netlify (free tier, custom domain)
- Vercel (free tier)
- Or simply share the folder — it works by opening `index.html` in any browser

## What We Need From the User

Before implementation, confirm or provide:
1. Contact details for the contact section (coach/guardian name, phone, email, WhatsApp)
2. Any specific images to exclude from the gallery
3. Preferred domain name (if any)
4. Any additional achievements or stats to include
