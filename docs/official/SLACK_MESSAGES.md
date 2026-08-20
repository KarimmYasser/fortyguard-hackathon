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

---

### 📌 Pinned Announcement: Hackathon Project Submission is LIVE! [12:44 PM]
**Hackathon Team**
> **Hackathon Project Submission is LIVE!**
> You can now submit your final project for FortyGuard Hackathon'26.
> 
> * **Submit here:** [https://forms.gle/jLgBzVTG1NhJ3gNe6](https://forms.gle/jLgBzVTG1NhJ3gNe6)
> * **Deadline:** **30 August 2026, 11:59 PM GST**
> 
> **Before submitting, make sure you have:**
> • Your project title + one-line pitch  
> • Your primary track  
> • A working live demo link  
> • A demo video — max 3 minutes  
> • Your GitHub or GitLab repository  
> • Details on how you used the FortyGuard Temperature API and AI tools  
> 
> **Important:** Please add `hackathon@fortyguard.com` to your GitHub/GitLab repository so our judges can access your code.  
> Solo participants submit their own project. For teams, only the team leader needs to submit on behalf of the full team.  
> You can resubmit before the deadline if you need to make changes — only your latest submission will be considered.  
> Good luck — we can't wait to see what you've built!

---

### 💬 Thread: Early Commits & Start Date Compliance (Aug 17 vs Aug 18)
**Participant [2:58 PM & 3:06 PM]**
> Hey @FortyGuard Assistant, if I started the project one day before the hackathon (17th Aug) with mock data setup, will it be disqualified? I did make an initial commit on Aug 17, but since the FortyGuard API key wasn’t provided until Aug 18, I was only building the basic site structure and testing features using mock data. Once the API key was officially given to us on Aug 18, I started integrating the actual FortyGuard data and building the core functionality around it. Would this be okay under the hackathon rules?

**FortyGuard Assistant [2:58 PM & 3:06 PM]**
> **That's totally fine.** You've got a clear, legitimate story: you set up scaffolding with mock data on the 17th (before the API was even live), then pivoted to real FortyGuard integration the moment credentials arrived on the 18th. That's exactly the kind of early prep the rules allow.
> 
> The rule is there to keep things fair, not to disqualify good work. Just make sure your README spells it out clearly — something like:
> `"Initial repo setup and mock-data structure: 17 August. Real FortyGuard API integration and core functionality: 18 August onward."`
> 
> That transparency is all you need. No disqualification risk at all — you're good to go.

---

### 💬 Thread: Map Generation Progress & Granularity Performance
**Participant [12:21 PM]**
> I am trying to generate maps of July 2021, but it's not getting over 60%, I have been trying for 2 days now.

**FortyGuard Assistant [12:21 PM]**
> • **July 2021 is valid** — it's well within the supported date range (2021-01-01 to present).
> • **If the task is stuck in progress**, large polygons or fine granularity ($60\text{ m}$) can take time. Try checking the `activity_id` status again.
> • **Failed tasks don't cost credits** — so resubmitting with a smaller polygon or coarser granularity ($80–100\text{ m}$) is free to try.

---

### 💬 Thread: Google Form Submission Access Issue ("Request Access to Submit")
**Participant [2:04 PM]**
> Why can't I submit the project and why does it show a 'request access to submit' message?

**FortyGuard Assistant [2:07 PM]**
> That's a permissions issue with the Google Form itself. Here's what to try:
> 1. Make sure you're signed in to Google with the email address you used to register for the hackathon.
> 2. Try again in an incognito/private window with that email signed in.
> 3. Clear your browser cookies for `forms.google.com` and try again.
> 4. If still unresolved, reach out to `hackathon@fortyguard.com` with registered email, screenshot, and time attempted.

