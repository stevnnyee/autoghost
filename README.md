# Autoghost - Automated Content Factory

An automated backend system that runs 5 faceless TikTok/YouTube accounts, generating 1-2 videos per account daily with minimal human oversight (30 min/day monitoring).

## What This System Does

**Automated Content Pipeline:**
```
Trend Scraper → Script Generator → Video Producer → Uploader → Analytics Tracker
      ↓              ↓                  ↓              ↓              ↓
   Reddit/Twitter   GPT-4            MoviePy      TikTok/YouTube   Database
                                   + ElevenLabs
                                   + Pexels
```

**Your Role:** 30 minutes/day to monitor analytics, approve content strategy, and create digital products to sell.

**Operating Costs:** ~$100-150/month for 10 videos/day across 5 accounts.

---

## Technology Stack

- **Python 3.10+** - Core language
- **OpenAI GPT-4** - Script generation
- **ElevenLabs** - AI voiceovers
- **Pexels API** - Stock footage (free)
- **MoviePy** - Video assembly
- **Selenium/Playwright** - TikTok upload automation
- **YouTube Data API** - YouTube upload automation
- **SQLite** - Database (or PostgreSQL for scale)
- **APScheduler** - Task scheduling
- **FastAPI** - Optional dashboard

---

## Build Breakdown (11 Builds)

### BUILD 1: Foundation & Setup ⏱️ 2-3 hours
**Goal**: Get project structure and configuration working

**What You'll Build:**
1. Create directory structure
2. Set up `requirements.txt` with all dependencies
3. Create `.env.example` for API keys
4. Create `.gitignore` for sensitive data
5. Build `config/settings.py` for centralized configuration
6. Create database schema in `autoghost/core/database.py`:
   - Accounts table (platform, username, niche, status)
   - Videos table (script, paths, upload status)
   - Trends table (topic, source, score)
   - Analytics table (views, likes, engagement)
7. Initialize SQLite database

**Testing:**
- Run `python -m autoghost.core.database` to verify database creation
- Check that config loads API keys from `.env`

**Deliverable:** Project skeleton with working config and database ✅

---

### BUILD 2: Trend Scraping ⏱️ 4-6 hours
**Goal**: Pull trending topics from Reddit/Twitter

**What You'll Build:**
1. **`autoghost/scrapers/reddit_scraper.py`**
   - Use PRAW library to scrape Reddit
   - Target subreddits: r/productivity, r/personalfinance, r/Entrepreneur, etc.
   - Filter by upvotes (>500), comments (>50), recency (last 24 hours)
   - Extract post titles, themes, keywords

2. **`autoghost/scrapers/twitter_scraper.py`**
   - Use Tweepy or nitter-scraper for Twitter/X
   - Track trending hashtags (#sidehustle, #financetips, etc.)
   - Extract trending topics by engagement

3. **`autoghost/scrapers/trend_analyzer.py`**
   - Score trends: (upvotes + comments) × recency_weight
   - Match trends to account niches (finance, productivity, etc.)
   - Store top 10-20 trends per niche in database

**Testing:**
- Run scrapers manually, verify 20+ trends stored in database
- Check trend quality (are they relevant to your niches?)
- Verify no duplicates

**Deliverable:** Working trend scraping system that finds viral topics ✅

---

### BUILD 3: Script Generation ⏱️ 3-4 hours
**Goal**: Generate video scripts from trends using GPT-4

**What You'll Build:**
1. **`autoghost/content/script_generator.py`**
   - OpenAI API integration (GPT-4)
   - Prompt engineering for viral 60-second scripts:
     ```
     Create a 60-second TikTok script about: {trend_topic}
     Niche: {account_niche}
     Style: Fast-paced, hook in first 3 seconds, casual tone
     Structure:
     - Hook (0-3s): Question or shocking statement
     - Main content (3-45s): 3-5 key points
     - CTA (45-60s): Follow for more, check bio
     Keep it conversational, use "you", avoid jargon.
     ```
   - Niche-specific prompt variations (finance vs productivity)
   - Generate 2-3 script variations per trend

2. **`autoghost/content/script_validator.py`**
   - Word count validation (150-200 words for 60s video)
   - Profanity/content policy check
   - Readability score (Flesch-Kincaid)
   - Reject and regenerate if quality too low

**Testing:**
- Generate 10 scripts from real trends
- Manually review quality (are they engaging? clear?)
- Check API costs (~$0.01-0.05 per script)

**Deliverable:** GPT-4 script generator with quality validation ✅

---

### BUILD 4: Voiceover Generation ⏱️ 2-3 hours
**Goal**: Convert scripts to audio using ElevenLabs

**What You'll Build:**
1. **`autoghost/production/voiceover_generator.py`**
   - ElevenLabs API integration
   - Voice selection per account/niche:
     - Finance: Professional male voice
     - Productivity: Energetic female voice
     - etc.
   - Generate MP3 audio from script text
   - Cost tracking (~$0.20-0.30 per video)
   - Save to `data/audio/{video_id}.mp3`

**Testing:**
- Generate 5 voiceovers from sample scripts
- Listen to quality (natural? good pacing?)
- Verify audio file format (MP3, 44.1kHz sample rate)
- Check duration matches script length

**Deliverable:** Working voiceover generator with cost tracking ✅

---

### BUILD 5: Stock Footage Downloader ⏱️ 3-4 hours
**Goal**: Download relevant video clips from Pexels

**What You'll Build:**
1. **`autoghost/production/footage_downloader.py`**
   - Pexels API integration (free, 200 requests/hour)
   - Extract keywords from script (e.g., "money", "laptop", "success")
   - Search Pexels for relevant videos
   - Download 5-10 clips per video (vertical format preferred)
   - Organize: `data/footage/{video_id}/clip_1.mp4`, etc.
   - Cache popular clips (e.g., generic "person working" clips)

**Testing:**
- Download footage for 5 different topics
- Check clip relevance (do they match the script?)
- Verify file format (MP4, 1080p or higher)
- Test caching (second request should use cached clips)

**Deliverable:** Automated footage downloader with caching ✅

---

### BUILD 6: Video Assembly ⏱️ 6-8 hours
**Goal**: Combine footage and voiceover into final video

**What You'll Build:**
1. **`autoghost/production/video_assembler.py`**
   - MoviePy pipeline:
     1. Load footage clips
     2. Trim clips to match voiceover duration
     3. Concatenate clips with smooth transitions
     4. Add voiceover audio track
     5. Add text overlays/captions (optional but boosts engagement)
     6. Add background music (low volume, royalty-free)
   - Output format: 1080x1920 (9:16), MP4, H.264
   - Save to `data/videos/{video_id}.mp4`

2. **`autoghost/production/video_optimizer.py`**
   - Compress video for upload (target: <100MB)
   - Validate file size (<287MB for TikTok)
   - Validate duration (15-60 seconds)
   - Quality check (not corrupted, audio synced)

**Testing:**
- Generate 3-5 complete videos end-to-end
- Manually watch each video (quality check)
- Check audio sync (voiceover matches video)
- Check visual quality (smooth transitions, readable captions)
- Measure generation time (target: 3-5 min per video)

**Deliverable:** Working video production pipeline ✅

---

### BUILD 7: TikTok Upload Automation ⏱️ 8-10 hours ⚠️ HARDEST
**Goal**: Automate TikTok video uploads via browser automation

**What You'll Build:**
1. **`autoghost/upload/tiktok_uploader.py`**
   - Selenium or Playwright setup (headless Chrome)
   - Login flow:
     - Handle username/password
     - Handle 2FA (manual first time, save cookies)
     - Save session cookies for future logins
   - Navigate to TikTok upload page
   - Upload video file (handle drag-and-drop or file input)
   - Fill in caption (include trending hashtags from trend data)
   - Set visibility (public)
   - Submit and wait for processing
   - Verify upload success
   - **Anti-detection measures:**
     - Random delays (5-15 sec between actions)
     - Human-like mouse movements (bezier curves)
     - Residential proxy (optional, $10-20/month)
   - Error handling (network failures, rate limits, login issues)

**Testing:**
- Upload 5 test videos to dummy TikTok account
- Verify videos appear correctly on TikTok
- Test error handling (disconnect network mid-upload)
- Monitor for account warnings/bans
- Check upload speed (target: 2-5 min per video)

**Deliverable:** Reliable TikTok upload automation ✅

**⚠️ CRITICAL RISK:** TikTok may detect automation and ban accounts. Mitigate with:
- Warm up new accounts: manual posts for first 3-5 days
- Limit to 1-2 posts per day per account
- Use test accounts first
- Random delays and human-like behavior

---

### BUILD 8: YouTube Upload Automation ⏱️ 4-5 hours
**Goal**: Automate YouTube Shorts uploads via official API

**What You'll Build:**
1. **Set up YouTube Data API v3:**
   - Create Google Cloud Platform (GCP) project
   - Enable YouTube Data API v3
   - Set up OAuth2 credentials
   - Authorize each YouTube account

2. **`autoghost/upload/youtube_uploader.py`**
   - OAuth2 authentication flow
   - Upload video via API
   - Set metadata:
     - Title (from script hook)
     - Description (with hashtags)
     - Tags (from trend keywords)
   - Mark as Short (duration < 60s)
   - Set visibility (public or unlisted for testing)
   - Handle quota limits:
     - 10,000 units/day
     - Upload costs 1,600 units = 6 uploads/day per project
     - Solution: Create multiple GCP projects for quota expansion

**Testing:**
- Upload 5 test videos to dummy YouTube channel
- Verify videos appear as Shorts (not regular videos)
- Check metadata accuracy (title, description, tags)
- Test quota limit handling (what happens when quota exceeded?)

**Deliverable:** Working YouTube upload automation ✅

---

### BUILD 9: Analytics Tracking ⏱️ 6-8 hours
**Goal**: Pull performance data from platforms

**What You'll Build:**
1. **`autoghost/analytics/tiktok_analytics.py`**
   - Scrape TikTok Creator Studio via browser automation
   - Extract metrics: views, likes, shares, comments, watch time
   - Store in database with timestamp

2. **`autoghost/analytics/youtube_analytics.py`**
   - YouTube Analytics API integration
   - Extract metrics: views, likes, comments, watch time, CTR, avg view duration
   - Store in database with timestamp

3. **`autoghost/analytics/performance_tracker.py`**
   - Calculate engagement rate: `(likes + comments + shares) / views`
   - Identify top-performing videos (top 10% by engagement)
   - Identify winning trends/topics
   - Generate weekly/monthly reports
   - Feed insights back into script generation:
     - "Videos about 'side hustle' get 2x engagement → prioritize this topic"

**Testing:**
- Pull analytics for test videos
- Verify data accuracy (cross-check with platform UI)
- Check insights make sense (top videos actually have high engagement)
- Test report generation

**Deliverable:** Analytics system with performance insights ✅

---

### BUILD 10: Scheduling & Orchestration ⏱️ 5-6 hours
**Goal**: Automate daily content generation pipeline

**What You'll Build:**
1. **`autoghost/core/scheduler.py`**
   - APScheduler setup
   - Jobs:
     - Daily at 3am: Run content generation pipeline
     - Hourly: Check for videos ready to upload
     - Daily at 11pm: Pull analytics

2. **`scripts/run_daily_generation.py`** (main orchestration script)
   - Step 1: Scrape trends (5-10 per niche)
   - Step 2: Generate scripts (2 scripts per account = 10 scripts/day)
   - Step 3: Produce videos (10 videos/day)
   - Step 4: Queue for upload at scheduled times
   - Step 5: Log all actions
   - Error handling: continue on failure, log errors
   - Target runtime: 30-60 min total

3. **`scripts/setup_accounts.py`**
   - Initial setup wizard
   - Add account credentials
   - Test API connections
   - Create database schema

**Testing:**
- Run full pipeline manually, verify all steps complete
- Let scheduler run for 3-5 days
- Monitor for failures (check logs)
- Verify video quality and upload success

**Deliverable:** Fully automated content pipeline ✅

---

### BUILD 11 (OPTIONAL): Dashboard ⏱️ 8-12 hours
**Goal**: Web interface for monitoring (nice-to-have)

**What You'll Build:**
1. **`dashboard/app.py`** - FastAPI application
2. **API endpoints:**
   - `GET /accounts` - List all accounts with status
   - `GET /analytics` - Recent performance metrics
   - `GET /videos` - List generated videos with thumbnails
   - `POST /generate` - Manually trigger content generation
   - `POST /accounts/{id}/pause` - Pause automation for an account
3. **Simple HTML templates** for viewing data

**Features:**
- View account status (active, paused, errors)
- See recent videos with performance metrics
- Charts: views over time, engagement rate trends
- Manually trigger content generation
- View logs and errors

**Testing:**
- Navigate dashboard in browser
- Verify data accuracy (matches database)
- Test manual triggers (generate content on demand)

**Deliverable:** Monitoring dashboard for easy oversight ✅

**Alternative:** Skip dashboard, use Jupyter notebooks or direct database queries.

---

## Recommended Build Order

### Week 1: Core Pipeline
- **Day 1:** BUILD 1 (Foundation & Setup)
- **Day 2:** BUILD 2 (Trend Scraping)
- **Day 3:** BUILD 3 (Script Generation)
- **Day 4:** BUILD 4 (Voiceovers) + BUILD 5 (Footage Downloader)
- **Day 5-6:** BUILD 6 (Video Assembly)
- **Day 7:** Testing and iteration

### Week 2: Upload & Analytics
- **Day 8-10:** BUILD 7 (TikTok Upload) ⚠️ Most time-consuming
- **Day 11-12:** BUILD 8 (YouTube Upload)
- **Day 13-14:** BUILD 9 (Analytics Tracking)

### Week 3: Automation & Polish
- **Day 15-16:** BUILD 10 (Scheduling & Orchestration)
- **Day 17-19:** End-to-end testing
- **Day 20-21:** BUILD 11 (Optional Dashboard)

### Week 4: Production Testing
- Run system for 1 week with test accounts
- Monitor for issues
- Optimize based on results
- Scale to all 5 accounts

---

## Success Criteria Per Build

- ✅ **BUILD 1:** Database created, config loads API keys
- ✅ **BUILD 2:** 20+ trends scraped and stored
- ✅ **BUILD 3:** 10 quality scripts generated
- ✅ **BUILD 4:** 5 natural-sounding voiceovers
- ✅ **BUILD 5:** 25+ relevant video clips downloaded
- ✅ **BUILD 6:** 3 high-quality videos produced
- ✅ **BUILD 7:** 5 videos uploaded to TikTok, no bans
- ✅ **BUILD 8:** 5 videos uploaded to YouTube
- ✅ **BUILD 9:** Analytics pulled for all test videos
- ✅ **BUILD 10:** System runs autonomously for 3 days
- ✅ **BUILD 11:** Dashboard shows real-time data

---

## Project Structure

```
Autoghost/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .env.example                       # API keys template
├── .gitignore                         # Git ignore rules
├── config/
│   ├── __init__.py
│   ├── settings.py                    # Central configuration
│   └── accounts.json                  # Account credentials (gitignored)
├── autoghost/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py                # SQLAlchemy models
│   │   └── scheduler.py               # APScheduler setup
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── reddit_scraper.py
│   │   ├── twitter_scraper.py
│   │   └── trend_analyzer.py
│   ├── content/
│   │   ├── __init__.py
│   │   ├── script_generator.py        # GPT-4 integration
│   │   └── script_validator.py
│   ├── production/
│   │   ├── __init__.py
│   │   ├── footage_downloader.py      # Pexels API
│   │   ├── voiceover_generator.py     # ElevenLabs
│   │   ├── video_assembler.py         # MoviePy
│   │   └── video_optimizer.py
│   ├── upload/
│   │   ├── __init__.py
│   │   ├── tiktok_uploader.py         # Selenium automation
│   │   ├── youtube_uploader.py        # YouTube API
│   │   └── upload_scheduler.py
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── tiktok_analytics.py
│   │   ├── youtube_analytics.py
│   │   └── performance_tracker.py
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       └── validators.py
├── dashboard/                         # Optional
│   ├── __init__.py
│   ├── app.py
│   ├── routes.py
│   └── templates/
├── scripts/
│   ├── run_daily_generation.py        # Main automation
│   ├── setup_accounts.py              # Initial setup
│   └── test_pipeline.py
├── data/
│   ├── videos/                        # Generated videos
│   ├── footage/                       # Stock footage
│   ├── audio/                         # Voiceovers
│   └── database.db                    # SQLite DB
└── tests/
    ├── __init__.py
    ├── test_scrapers.py
    ├── test_generation.py
    └── test_production.py
```

---

## API Costs (Monthly Estimate)

**Per Video:**
- GPT-4 script: $0.01-0.05
- ElevenLabs voiceover: $0.20-0.30
- Pexels footage: Free (rate limited)
- **Total per video:** ~$0.25-0.35

**For 10 videos/day:**
- Daily: ~$2.50-3.50
- Monthly: ~$75-105

**Other costs:**
- Residential proxy (optional): $10-20/month
- Hosting (optional cloud): $10-20/month
- **Total monthly:** ~$100-150

---

## Risk Mitigation

### TikTok Account Bans
- **Problem:** TikTok detects automation and bans accounts
- **Mitigation:**
  - Warm up accounts with manual posts (3-5 days)
  - Use residential proxies
  - Random delays (5-15 sec) between actions
  - Limit to 1-2 posts per day per account
  - Monitor ban rates, adjust strategy

### API Rate Limits
- **OpenAI:** 3,500 requests/min (plenty)
- **ElevenLabs:** 100k chars/month = ~60-80 videos (upgrade plan if needed)
- **YouTube API:** 10,000 units/day = ~6 uploads/day (use multiple GCP projects)
- **Pexels:** 200 requests/hour (cache popular footage)

### Content Quality Issues
- **Problem:** AI scripts are generic or low-quality
- **Mitigation:**
  - Improve prompts with examples
  - Use GPT-4 (not 3.5)
  - Add human review step (optional)
  - A/B test script styles

### Video Production Speed
- **Problem:** MoviePy is slow, can't generate 10 videos in time
- **Mitigation:**
  - Use multiprocessing (generate videos in parallel)
  - Optimize resolution (720p vs 1080p)
  - Run on powerful machine or cloud instance
  - Target: 3-5 min per video, 30-50 min total

---

## Getting Started

### 1. Prerequisites
- Python 3.10+
- API keys:
  - OpenAI (GPT-4)
  - ElevenLabs
  - Pexels
  - Reddit (PRAW)
  - Twitter (optional)
  - YouTube Data API
- TikTok/YouTube accounts (5 total)

### 2. Start with BUILD 1
Follow the builds in order. Each build is designed to be completed independently and tested before moving to the next.

### 3. Next Steps
After BUILD 1, you'll have:
- Project structure set up
- Database initialized
- Config management working

Then move to BUILD 2, and so on.

---

## Success Metrics

### Month 1 (Validation)
- ✅ 10 videos posted per day (2 per account)
- ✅ 50%+ videos reach >1,000 views
- ✅ 0 account bans
- ✅ System runs with <30 min daily monitoring

### Month 2-3 (Growth)
- ✅ At least 1 account reaches 5,000 followers
- ✅ Average engagement rate >5%
- ✅ Identify 2-3 winning content themes per niche

### Month 4+ (Monetization)
- ✅ 3+ accounts with 10,000+ followers
- ✅ Email list building (link in bio)
- ✅ Launch digital product ($100-300)
- ✅ First sales: $2-5k

---

## Questions?

Start with BUILD 1 and work your way through. Test each build before moving to the next. Good luck!
