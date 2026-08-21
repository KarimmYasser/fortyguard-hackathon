# FortyGuard Hackathon - Participant Handbook


---
## Page 1


---
## Page 2

TABLE OF CONTENTS

Table of contents..............................................................................................................................2

1. Welcome........................................................................................................................................4

2. Key dates...................................................................................................................................... 4

3. Rules at a glance.......................................................................................................................... 4

4. Why build with FortyGuard......................................................................................................... 5

5. Getting started (your first hour)..................................................................................................5

Step 1 - Create your free Dashboard account..................................................................... 5

Step 2 - Generate a heatmap in the Dashboard.................................................................. 5

Step 3 - Get your API key & trial credits...............................................................................6

Step 4 - Clone the Temperature API Quickstart and run your first call.................................6

Step 5 - Skim the API docs.................................................................................................. 6

Step 6 - Join the community.................................................................................................6

6. Understanding the platform........................................................................................................ 6

7. API usage guide........................................................................................................................... 7

7.1 How to learn the API: theory vs. practice............................................................................... 7

7.2 Coverage & data range - read this first................................................................................ 8

7.3 Base URL & authentication.................................................................................................... 8

7.4 The asynchronous pattern......................................................................................................8

7.5 Endpoint overview.................................................................................................................. 9

7.6 Core request fields (heatmap)..............................................................................................10

7.7 Best practices.......................................................................................................................10

8. Your learning environment: the Temperature API Quickstart................................................ 11

8.1 What’s inside........................................................................................................................ 11

8.2 Five-minute setup.................................................................................................................12

8.3 Use-case notebooks - working starting points................................................................... 13

9. Implementation examples......................................................................................................... 14

9.1 The fastest path - the quickstart client (Python).................................................................14

10. Tracks & project ideas............................................................................................................. 15

Track 1 - Resilient Cities & Infrastructure...........................................................................15

Track 2 - Future Buildings & Energy.................................................................................. 15

Track 3 - Industrial & Enterprise.........................................................................................16

Track 4 - Government & Environment................................................................................16

Track 5 - Model Designing...................................................................................................16

Track 6 - Agentic Track (API + Agentic)............................................................................... 16

Track 7 - Data Analysis & Correlation.................................................................................. 17

11. Judging & submission............................................................................................................. 17

Submission checklist.................................................................................................................. 18

12. Prizes.........................................................................................................................................18

13. Webinars & program support..................................................................................................19

Building the World’s Temperature AI · Participant Handbook · Page 2


---
## Page 3

14. Support routing........................................................................................................................ 19

15. Terms & Conditions..................................................................................................................20

Building the World’s Temperature AI · Participant Handbook · Page 3


---
## Page 4

1. WELCOME

Extreme urban heat is one of the fastest-growing climate risks and one of the least visible. FortyGuard

tells you how hot it is on this street, next to this building, at 2 p.m. - at 20 meters spatial resolution, 2

meters elevation, human-relevant resolution, hour by hour. That difference is the whole opportunity.

Building the World’s Temperature AI brings developers, researchers, designers, and climate-tech

builders together to turn that intelligence into working applications: tools that cool cities, protect people,

and de-risk infrastructure. You bring the idea; this handbook gives you everything else - onboarding, a

hands-on learning environment, working code, project ideas, and the judging criteria your project will be

scored against.

2. KEY DATES

MILESTONE DATE

Registration opens Jun 20 - Aug 17 (11:59 PM GST)

Kickoff Aug 18

Mentor Webinars Released through the program and will be

announced on Slack

Submission deadline Aug 30 (11:59 PM GST)

Judging window Sept 1 - Sept 14 (11:59 PM GST)

Winners announced Sept 16

All deadlines are published on the official hackathon site and announced on Slack. The site and slack are the

source of truth if anything here changes.

3. RULES AT A GLANCE

● Free to enter. Participation, Dashboard access, and trial API credentials cost nothing.

● Open globally. Anyone may participate, subject to the eligibility rules on the hackathon site. Note

that all analysis runs on U.S. locations - see §7.2.

● Individuals or teams. Teams are 1-3 people and solo entries are welcome.

● Original work. Your project must be created during the hackathon period unless the rules state

otherwise.

● Be a good participant. Follow the Code of Conduct: no abuse of the platform, no

reverse-engineering of the models, no harassment.

Building the World’s Temperature AI · Participant Handbook · Page 4


---
## Page 5

4. WHY BUILD WITH FORTYGUARD

WHAT YOU GET WHY IT MATTERS FOR YOUR BUILD

Hyperlocal resolution (~2 m) Model heat where people actually stand - 

sidewalks, bus stops, courtyards - not a single

city-wide number.

Historic, near-real-time & short-range forecast

data

Analyze past heat patterns over multiple years,

monitor current and 12hrs ahead conditions ,

hour by hour.

Large Temperature Models (LTMs) Calibrated temperature fields built for

operational use, fusing satellite signals, GIS

layers, meteorology, and ground observations.

Heat Intelligence reports Each location pairs temperature with contextual

layers (geographic, environmental, urban

dynamics) - the “why” behind the heat.

Simple, scalable API A few HTTP calls return structured heat data

you can drop into GIS, asset management,

dashboards, or simulations.

300× more precise, 100× cheaper than satellite Tasks that once took months and tens of

thousands of dollars run in seconds for a fraction

of the cost.

5. GETTING STARTED (YOUR FIRST HOUR)

Follow these steps in order. Steps 1-4 get you to your first heatmap; steps 5-6 set you up to build.

Step 1 - Create your free Dashboard account

Sign up at dashboard.fortyguard.com. The Temperature Dashboard is a browser app - no installation,

best on desktop. Explore a heatmap visually before you touch the API; it makes the API responses

intuitive.

Step 2 - Generate a heatmap in the Dashboard

● Draw a polygon over a U.S. area of interest (a neighborhood, campus, or industrial site).

● Pick a date and time window, then generate the map.

Building the World’s Temperature AI · Participant Handbook · Page 5


---
## Page 6

● Read the result with the time-series player, side-by-side comparison, and per-tile Heat Intelligence

reports.

Step 3 - Get your API key & trial credits

Now that you're signed in to the Temperature Dashboard, you can get your API key right there. Open

the Profile tab and generate your API key to start accessing data - it comes with your hackathon trial

credits. Keep your key secret: store it in an environment variable, never hard-code it, and never commit

it to a public repo.

Note: The API key generation will be available near the start of the build sprint. You will be notified on

slack when you can generate your API keys

Step 4 - Clone the Temperature API Quickstart and run your first call

Every participant is given access to the Temperature API Quickstart repository (§8) - a ready-made

Python + Jupyter environment. Clone it, paste your key into .env, and run notebook 00 (auth check) and

notebook 01 (your first heatmap). No key yet? The use-case notebooks ship with cached API

responses, so you can run them end-to-end before your credentials even arrive.

Step 5 - Skim the API docs

Bookmark docs-api.fortyguard.com. Use it as your theoretical reference for endpoint definitions and

parameters while the quickstart gives you the practical, runnable side (§7.1). You can enter your API

key right on the docs page to make live calls and track your credit consumption, so you don't burn your

quota mid-build.

Step 6 - Join the community

Join the hackathon Slack for announcements, mentor office hours, and peer support. Most “how do I...”

questions are answered there faster than by email.

60-MINUTE FIRST-RUN CHECKLIST

☐ Dashboard account created ☐ One heatmap generated visually

☐ API key stored in .env / environment variable ☐ Quickstart cloned, notebook 00 passes

☐ Notebook 01 returns your first heatmap ☐ Slack joined

6. UNDERSTANDING THE PLATFORM

A quick mental model of how the pieces fit together. The Large Temperature Model (LTM) is the

Intelligence Layer; the Dashboard and API are the two ways you reach it.

CONCEPT WHAT IT IS

Building the World’s Temperature AI · Participant Handbook · Page 6


---
## Page 7

LTMs - Large Temperature Models Purpose-built AI models that predict ambient air

temperature at human height and high spatial

resolution by fusing satellite signals, GIS layers,

meteorology, and in-situ observations.

Temperature Dashboard The visual, browser-based product for drawing

areas, generating heatmaps, comparing

scenarios, and reading Heat Intelligence reports.

Temperature API Programmatic access to the same intelligence

 -  submit areas and times, receive structured

temperature data for your own app.

Polygon (AOI) The geographic area of interest you analyze,

expressed as GeoJSON polygon coordinates - 

[longitude, latitude] order.

Granularity The spatial detail of the output grid in meters

(60, 80, or 100) - smaller values mean finer

tiles and more compute/credits.

Activity ID The task ticket is returned when you submit an

analysis request; you poll it to collect the

finished result (§7.4).

API credits The currency consumed per request, based on

the complexity and data needs of the call. Failed

tasks are free - credits are only deducted when

a task succeeds.

7. API USAGE GUIDE

7.1 How to learn the API: theory vs. practice

TWO RESOURCES, TWO JOBS

📘 The official API documentation (docs-api.fortyguard.com) is your theoretical reference - endpoint

definitions, parameters, request and response schemas. Read it to understand what each endpoint can do.

🧪 The Temperature API Quickstart repository (§8) is your practical environment - every participant gets

access. It wraps every endpoint in a ready-made Python client, walks each one in a runnable notebook, and

shows you real requests and real results. Run it to understand how each endpoint actually behaves - what

you send, what comes back, and what the data looks like - before you start building your project.

Recommended: run the quickstart first, keep the docs open beside it as reference.

Building the World’s Temperature AI · Participant Handbook · Page 7


---
## Page 8

7.2 Coverage & data range - read this first

⚠ TWO CONSTRAINTS THAT SHAPE EVERY PROJECT

Coverage is U.S.-only. All endpoints operate over locations inside the United States. Polygons or points outside

the U.S. return errors or empty results - don’t spend credits on other countries. Wherever you are in the world,

design your project around U.S. geographies (e.g. Phoenix, Houston, Miami, New York, San José).

Date range: 2021-01-01 to the present. Create Heatmap additionally supports forecasting up to 12 hours

beyond the current time, so the latest accepted value is now + 12 hours. Anything earlier than 2021-01-01, or

more than 12 hours in the future, is rejected. For Satellite Segmentation, Environmental Parameters, and Heat

Intelligence, use a date/time matching the heatmap you generated for the same location and time.

7.3 Base URL & authentication

Base URL: https://api.fortyguard.com

Auth header: api-key: YOUR_API_KEY

Content-Type: application/json

Store the key in an environment variable (the quickstart uses FORTYGUARD_API_KEY in a git-ignored

.env file), never hard-code it, and never commit it.

7.4 The asynchronous pattern

Analysis endpoints are asynchronous because the model is doing real work (seconds to minutes).

Every analysis call follows the same two-stage flow:

Building the World’s Temperature AI · Participant Handbook · Page 8


---
## Page 9

● Submit - POST your request (area/point + date_time + options). The response returns an

activity_id.

● Poll - GET /v1/status/{activity_id} until the status is terminal: “succeeded” / “completed” means

your result is in the response’s data.result; “failed” / “error” means the task failed (and cost nothing).

The quickstart’s Python client does the polling for you - one call, result back.

7.5 Endpoint overview

ENDPOINT WHAT IT RETURNS PLAN QUICKSTART NOTEBOOK

POST /v1/heatmap Tile-by-tile thermal

map over a polygon

AOI

All plans 01

POST

/v1/env_params

Heat index, AQI, solar

irradiance and more,

at a point

All plans 02

POST /v1/satellite Land-cover

segmentation of a

satellite tile (greenery,

roads, buildings...)

Premium 03

POST /v1/streetview Segmentation of a

ground-level street

view

Premium 04

POST

/v1/heat_intelligence

Multi-dimensional heat

analysis as a PDF

report

Premium 05

POST

/v1/system/fetch-api-k

ey-usage

Your credit balance

and billing-cycle

usage

All plans 00

GET

/v1/status/{activity_id}

Status / result of any

submitted analysis

task

All plans - 

Building the World’s Temperature AI · Participant Handbook · Page 9


---
## Page 10

7.6 Core request fields (heatmap)

FIELD TYPE MEANING

polygon_aoi GeoJSON Your area of interest as a

GeoJSON FeatureCollection

containing a Polygon.

Coordinates are [longitude,

latitude]; the first and last pair

must match to close the ring.

date_time.start_date string Date to analyze,

YYYY-MM-DD. Past

dates/today/ +12hrs

forecasting only.

date_time.start_time string Time of day, HH:MM (heat

varies enormously by hour).

date_time.filter_type int Time window: 1 = single hour,

2 = range of hours (add

end_time), 3 = entire day. 4 =

range of days, 5 = single

month

granularity int Output grid detail in meters:

60, 80, or 100. Smaller = finer

tiles and higher credit cost.

7.7 Best practices

● Start small: validate your pipeline on a tiny polygon and a single timestamp before batching.

● Cache aggressively: store every result keyed by area + date/time so you never pay twice for the

same query.

● Poll politely: back off between status checks (e.g. 3s → 6s → 12s) rather than hammering the

endpoint.

● Handle failures: wrap calls in try/except, check HTTP status codes, and log the activity_id for

debugging. Remember failed tasks are free - credits are only deducted on success.

Building the World’s Temperature AI · Participant Handbook · Page 10


---
## Page 11

● Mind the geography and the calendar: U.S. locations, dates from 2021-01-01 to now (+12h for

heatmaps) - see §7.2.

● Pick the right time window: filter_type 3 (entire day) is ideal for daily max/mean analysis; filter_type

1 for a specific hour like 14:00 peak heat.

● Respect the area limit: heatmap AOIs are capped at roughly 130 km2 (50 mi2). Larger polygons are

rejected - split them or zoom in.

8. YOUR LEARNING ENVIRONMENT: THE

TEMPERATURE API QUICKSTART

Participants are provided access to the Temperature API Quickstart - a Python + Jupyter sandbox built

by FortyGuard so you can learn the endpoints hands-on before starting your project. Where the API

docs give you the theory, the quickstart is the place to see each endpoint actually run: what a request

looks like, what the response contains, and how the results behave on real U.S. locations. The access

link is shared at registration and pinned on Slack.

8.1 What’s inside

COMPONENT WHAT IT GIVES YOU

fortyguard/ Python client One method per endpoint

(client.create_heatmap(...),

client.environmental_parameters(...), ...).

Handles authentication and the submit-then-poll

pattern for you.

Endpoint notebooks 00-05 A runnable walkthrough of every endpoint in

order: setup & auth check, heatmap,

environmental parameters, satellite

segmentation, street view segmentation, heat

intelligence PDF.

Use-case notebooks Three complete narrative workflows that

combine your own CSV data with FortyGuard

layers and end in a ranked, defensible action list

(see §8.3).

Sample data & cached responses Sample polygons, point lists, and pre-fetched

API responses - so the use-case notebooks

run end-to-end even without an API key (cached

mode).

Troubleshooting guide Common errors (auth, timeouts, payload

mistakes) with fixes, in the README.

Building the World’s Temperature AI · Participant Handbook · Page 11


---
## Page 12

8.2 Five-minute setup

git clone <quickstart-repo-url> temperature-api-quickstart

cd temperature-api-quickstart

python -m venv venv

venv\Scripts\activate # Windows (macOS/Linux: source venv/bin/activate)

pip install -r requirements.txt

cp .env.example .env # then paste your key into .env:

# FORTYGUARD_API_KEY=fg_live_xxxxxxxxxxxxxxxx

jupyter lab # open notebooks/00_setup.ipynb and run all cells

If notebook 00’s last cell prints your plan and remaining credits, you’re wired up. Work through

notebooks 01-05 in order, then pick a use-case workflow.

8.3 Use-case notebooks - working starting points

These are complete, end-to-end workflows. Each ships with sample input data - replace it with your

own CSV using matching columns and everything downstream runs. The FortyGuard temperature data

they use is real, at 2 meters above the ground and 20-meter spatial resolution. Each notebook is a

directional example of how to use the endpoints, not a finished project. Hackathon submissions are

expected to go well beyond them, built on your own data, region, problem, and approach.

Building the World’s Temperature AI · Participant Handbook · Page 12


---
## Page 13

USE CASE YOUR DATA OUTPUT

Urban planner - bus-stop

cooling prioritization

Bus-stop points (CSV) Ranked intervention list - 

which stops need shade first,

and why

Public-parks heat-resilience

audit

Park points (id, type, acres,

lat/lon)

Per-park audit with

threshold-triggered

recommendations citing

federal programs (EPA, USDA)

Real-estate portfolio heat risk Property portfolio (CSV) Client-deck slide pack +

per-property action brief citing

public programs (EPA, USDA,

ASHRAE, OSHA)

NO API KEY YET? START ANYWAY.

Every use-case notebook ships in cached mode (CACHED=True) with bundled sample responses, so you can

run the entire workflow and study real API results before your trial credentials arrive. Flip CACHED=False once

you have a key to run live against any U.S. area you choose.

Building the World’s Temperature AI · Participant Handbook · Page 13


---
## Page 14

9. IMPLEMENTATION EXAMPLES

Copy-paste starting points, verified against the quickstart. Example coordinates are Lower Manhattan;

any U.S. location works.

9.1 The fastest path - the quickstart client (Python)

from dotenv import load_dotenv; load_dotenv()

from fortyguard import FortyGuardClient

Building the World’s Temperature AI · Participant Handbook · Page 14


---
## Page 15

client = FortyGuardClient() # reads FORTYGUARD_API_KEY from .env

response = client.create_heatmap(

polygon_aoi={

"type": "FeatureCollection",

"features": [{

"type": "Feature", "properties": {},

"geometry": {

"type": "Polygon",

"coordinates": [[ # [longitude, latitude]

[-74.017, 40.705], [-74.003, 40.705],

[-74.003, 40.718], [-74.017, 40.718],

[-74.017, 40.705], # first == last closes the ring

]],

},

}],

},

start_date="2025-07-15", # 2021-01-01 → now (+12h ahead for heatmaps)

start_time="14:00", # peak-heat hour

filter_type=1, # 1=single hour, 2=range, 3=entire day

granularity=100, # meters: 60, 80, or 100

)

print(response["activity_id"])

print(response["result"]["stats_data"]) # summary statistics for the AOI

The client submits, polls GET /v1/status/{activity_id} for you, and returns the finished result. Pass

wait=False to get the activity_id immediately and poll on your own schedule.

10. TRACKS & PROJECT IDEAS

Pick the track that matches your interest; use the ideas as launch points, not limits. The strongest

projects pair a real heat problem with a measurable before/after outcome - the same logic FortyGuard

uses with enterprise clients.

Track 1 - Resilient Cities & Infrastructure

Design the physical city around heat - route people along cooler paths, rank which public assets

need shade first, and test interventions before a shovel hits the ground.

● A cool-route planner that, given start and end points, returns the lowest-heat-exposure

walking path using hourly heatmaps.

● A bus-stop / playground heat-audit tool that ranks a city's public assets by peak-hour

exposure to prioritize shade investment. (Working starting point: the quickstart's bus-stop

prioritization notebook, §8.3.)

● A digital-twin overlay that simulates how adding tree canopy or reflective paving changes

street-level temperature.

Track 2 - Future Buildings & Energy

Bring street-level heat into how buildings are sited, powered, and retrofitted - so cooling is sized

to real thermal load and every upgrade can prove its payback.

Building the World’s Temperature AI · Participant Handbook · Page 15


---
## Page 16

● A facade-orientation advisor that scores building sites by solar/heat load to inform HVAC

sizing and glazing choices.

● A demand-response signal that uses historical heat patterns to estimate neighborhood

cooling load for a utility.

● A retrofit ROI calculator linking modeled temperature reduction to estimated energy

savings.

Track 3 - Industrial & Enterprise

Turn hyperlocal heat into an operational and financial signal - screen where to build, protect cargo

and crews in transit, and price exposure into underwriting.

● A data-center siting screener that flags candidate locations with elevated ambient heat (and

higher cooling cost).

● A logistics route/temperature tool that protects heat-sensitive cargo and worker safety on

last-mile routes.

● A parametric heat-risk score for insurers or real-estate portfolios, turning hyperlocal

exposure into an underwriting input. (Working starting point: quickstart's real-estate portfolio

notebook, §8.3.)

Track 4 - Government & Environment

Point public resources at the people heat hits hardest - target relief by vulnerability, warn outdoor

workers before thresholds are crossed, and time agriculture to the microclimate.

● A heat-vulnerability map that combines temperature with demographics to target cooling centers

and outreach. (Related starting point: quickstart's public-parks audit notebook, §8.3.)

● A worker-safety alerting service that warns outdoor crews when a site crosses a heat threshold.

● An agricultural micro-climate tool that guides planting and irrigation timing from historical heat

patterns.

Track 5 - Model Designing

Build the models under the applications - train, validate, and package the algorithms that turn raw

temperature into vulnerability scores, safety alerts, and microclimate forecasts others can deploy.

● A heat-vulnerability model that combines temperature with demographics to target cooling

centers and outreach. (Related starting point: quickstart's public-parks audit notebook, §8.3.)

● A worker-safety alerting model that warns outdoor crews when a site crosses a heat threshold.

● An agricultural micro-climate model that guides planting and irrigation timing from historical heat

patterns.

Track 6 - Agentic Track (API + Agentic)

Wrap FortyGuard's endpoints in autonomous agents that plan, call, and decide - turning a

natural-language goal into a completed heat workflow with minimal human steering.

● A goal-driven heat agent that takes a plain-language brief ("find the hottest bus stops in Phoenix

across last July and draft a shade-investment memo"), chooses and sequences the right

endpoints, and returns a ranked, source-cited action plan.

Building the World’s Temperature AI · Participant Handbook · Page 16


---
## Page 17

● A monitoring agent that sweeps current-day conditions across a portfolio of U.S. sites, polls

status tasks on its own schedule, and fires alerts or downstream actions when a location

crosses a heat threshold.

● A tool-using research assistant that combines FortyGuard layers with public datasets to answer

open-ended heat questions, showing its API calls and reasoning so the output is auditable.

(Starting point: the submit-then-poll client in the quickstart, §8.1 - let the agent drive it.)

Track 7 - Data Analysis & Correlation

Move beyond mapping heat to explaining it - correlate hyperlocal temperature with the non-weather

variables it drives or is driven by, and quantify the relationship.

● A correlation study linking temperature to non-weather outcomes - hospital admissions,

energy load, transit ridership, crime, or retail foot traffic - to surfaces where heat measurably

moves the needle.

● A heat-equity analysis that joins historical temperature patterns with demographic or

socioeconomic layers to quantify unequal exposure across neighborhoods. (Related starting

point: the public-parks audit notebook, §8.3.)

● A regression toolkit that ingests a user-supplied CSV of outcomes, aligns each row to

FortyGuard temperature at its coordinates and timestamp, and reports the strength and

significance of the relationship.

WHAT MAKES A PROJECT WIN

Real use of the platform (the API or Dashboard is central, not decorative); a clear problem and user; a

measurable outcome (e.g. “−7°F (−4°C) on this route”); and a path to real-world deployment. Judges reward

applied relevance over flashy demos.

11. JUDGING & SUBMISSION

Projects are scored on the four weighted criteria below. Judges' decisions are final.

CRITERION WEIGHT WHAT JUDGES LOOK FOR

Impact & relevance 40% A real urban-heat problem with

measurable benefit;

commercially viable solutions a

real client would adopt

Building the World’s Temperature AI · Participant Handbook · Page 17


---
## Page 18

Technical execution 35% It works, the build is sound,

data handled well; deployable,

client-grade quality

Innovation 15% Original approach or a fresh

combination of ideas

Communication 10% Clear, compelling demo and

write-up

Submission checklist

● ☐ A live demo link - your working project

● ☐ A public (or judge-accessible) repository (share it with FortyGuard) with your code and a

README explaining how to run it.

● ☐ A demo video (≈ 3 minutes) showing the project working.

● ☐ A written summary (max 500 words): the problem → who it’s for → the FortyGuard

endpoints/features used → the measured result.

Tip: structure your summary exactly as problem → user → FortyGuard usage → measured result. It mirrors the

judging rubric, and the strongest summaries get showcased as case studies.

12. PRIZES

Final prize amounts and tiers are published on the hackathon site. The award categories:

TIER / AWARD PRIZE

Cash - 1st / 2nd / 3rd Cash prizes and Nvidia GPUs

Incubation Post-hackathon incubation or acceleration with

partner programs

Career Internship opportunities with FortyGuard or a

partner (for qualifying graduates)

Platform Monthly/annual API-usage discounts

Hardware / compute GPU hardware or cloud-credit deals

Everyone who completes the hackathon Certificate of completion + a shareable “I built at

the FortyGuard Hackathon” social asset

Building the World’s Temperature AI · Participant Handbook · Page 18


---
## Page 19

13. WEBINARS & PROGRAM SUPPORT

● Mentor webinars - Live and recorded. All sessions are announced in #announcements on Slack

and the FortyGuard Hackathon’26 website.

● Live Q&A - The FortyGuard team answers questions live.

All sessions are announced on Slack and recorded for replay.

14. SUPPORT ROUTING

RESOURCE WHERE

Temperature Dashboard (free) dashboard.fortyguard.com

API documentation (theory / reference) docs-api.fortyguard.com/docs/introduction

Temperature API Quickstart (practice /

runnable)

Access link shared at registration and

pinned on Slack

API pricing & trial fortyguard.com/api-pricing

Technology overview fortyguard.com/our-technology

Community & live help Hackathon Slack

Email support support@fortyguard.com /

hackathon@fortyguard.com

Fastest route: ask the assistant bot in Slack → post in #help-technical (API/dev) or #help-general

(everything else) → email us if you're still stuck.

Building the World’s Temperature AI · Participant Handbook · Page 19


---
## Page 20

15. TERMS & CONDITIONS

1. Who can join: Join solo or in a team of up to 3. Everyone on a team must register.

2. The event: FortyGuard Hackathon'26 runs 18-30 August 2026 (11:59 PM GST), fully online.

Submissions close 30 August 2026 (11:59 PM GST) - no late entries.

3. Using FortyGuard's data (please respect this): We're giving you free access to our

Temperature API and data for the hackathon. In return:

● Use it only for your hackathon project - nothing else.

● Keep your API key private - it's yours alone. Our data, API, and models stay ours. Access

ends when the hackathon ends; anything beyond that needs a separate agreement with us.

4. Your project: You own what you build. By submitting, you let us show and share your project

and your team's name to run and promote the hackathon. Your work must be your own, use our

Temperature data, and not copy anyone else's.

5. How to submit: a live demo link, and a short (max 3-minute) video showing your project

working. For your code, add Hackathon-FG(hackathon@fortyguard.com) as a collaborator

on your GitHub repo so the judges have access to review it.

6. Judging: Our tech team first shortlists submissions, then judges score them on Impact &

Relevance (40%), Technical Execution (35%), Innovation (15%), and Communication (10%).

Judges' decisions are final. Cheating or plagiarism means disqualification.

7. Prizes: The top three teams each win one Nvidia GPU (three GPUs total - one per winning

team, whatever your team size; your team decides how to share it; Team leader gets it if in

dispute).

8. Be decent: Be respectful, don't cheat, don't harass anyone. We can remove or disqualify

anyone who breaks these rules.

9. Questions? Technical: support@fortyguard.com · Everything else: hackathon@fortyguard.com

Building the World’s Temperature AI · Participant Handbook · Page 20
