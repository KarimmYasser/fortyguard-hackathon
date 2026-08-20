:wave: Hi everyone — a quick note on API key access
Please hang tight for your API key details! The hackathon officially begins tomorrow, and API key access opens then — so it's completely normal not to have your key just yet.
In the meantime, we've given you everything you need to get familiar with the API and its results now, so you can hit the ground running. Here's the good news: you can start exploring today, even without a key.
The Temperature API Quickstart (Python + Jupyter notebooks) was shared with you at registration and is pinned here in Slack. Here's how to get going:
:one: Clone the Quickstart repo — the link was in your registration confirmation and is pinned in this workspace.
 :two: Paste your API key into a .env file — once API access opens around 18 August.
 :three: Run the notebooks in order:
 • Notebook 00 — auth check (verifies your key works)
 • Notebook 01 — first heatmap
 • Notebook 02 — environmental parameters
 • Notebook 03 — satellite segmentation (Premium)
 • Notebook 04 — street view segmentation (Premium)
 • Notebook 05 — heat intelligence report (Premium)
:bulb: Tip: The notebooks ship with cached responses (CACHED=True), so you can run them end-to-end right now — even before your key arrives. It's a great way to understand the data structure, see what the API returns, and plan your project today.
Thanks for your patience — we can't wait to see what you build! :thermometer:

:rocket: API Access is LIVE!
The moment you've been waiting for — you can now generate your Temperature API® key on the FortyGuard Dashboard. Time to start building! :thermometer:
How to get your key:
 :one: Sign up free on the Temperature Dashboard → https://dashboard.fortyguard.com
 :two: Click Profile (bottom-left corner)
 :three: Hit Create API Key to generate your access
You'll get a free Hackathon API key with 2,000,000 credits, valid for 5 weeks — plenty to build, test, and demo your project. :white_check_mark:
:tada: Best part: your access is fully Premium — all endpoints are unlocked and completely free for the hackathon. So you can use everything the Temperature API offers, including the premium features, at no cost.
Coverage is US-wide, so pick a US city for your study area.

---

### 💬 Thread: Polling Intervals, Caching, and Credit Management
**Adina [12:00 PM]**
> @FortyGuard Assistant is there a recommended minimum polling interval for repeated env_params calls against the same locations, to avoid wasting credits or hitting rate limits? Planning something that checks conditions periodically rather than once.

**FortyGuard Assistant [12:01 PM]**
> Good question — here's what matters:
> 
> **Credits:** Failed tasks are free, so a failed request won't sting. Successful ones consume credits based on your plan. If you're polling the same location and time repeatedly, you're paying each time — so **cache aggressively**. Store results keyed by `location + timestamp`, and reuse them rather than re-query.
> 
> **Rate limits:** The API docs at https://docs-api.fortyguard.com/docs/introduction are the authoritative source on rate-limit specifics (thresholds, backoff strategy, etc.). I'd check there for the exact limits and recommended polling intervals.
> 
> **General best practice** for any asynchronous endpoint: start with a reasonable backoff (e.g. `3s → 6s → 12s` between polls) rather than hammering `/v1/status`. That's polite and gives the backend time to finish.
> 
> For periodic checks of the same locations over time (e.g. "re-check this street every hour"), the real win is caching — store hourly snapshots keyed by `location + hour`, and only call the API if you don't already have that data. That cuts credit burn dramatically.
> 
> If you hit actual rate limits or credit questions as you build, drop into `#help-technical` or email `support@fortyguard.com` and they can help tune it for your use case.
