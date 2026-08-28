# Informing the Data: How We Understand What Temperature Means for the Human Experience — Full Transcript & Summary

**Recording:** [Zoho Webinar Recording (Session 13)](https://webinar.zoho.com/meeting/videoprv?recordingId=6556c125af16ba14d3a0aa91d7a8147547d243298b779de54fe55d485d732319&x-meeting-org=935374719)  
**Date:** August 27, 2026 | **Duration:** 35 mins 1 sec | **Language:** English | **Engine:** Whisper AI (Apple Silicon Metal GPU)  

**Speakers:**
- **Mike Stelfox** — Landscape Architect, Urban Designer, Founder of *Stelfox Design Studio*; Virginia Sea Grant Fellow; Expert in Green Infrastructure, Urban Heat Island Mitigation & Resilient Public Spaces; Hackathon Mentor & Judge
- **Snehil Ahuja** — Product Lead at FortyGuard (Host & Moderator)

---

## Executive Summary & Session Overview

In this urban design and microclimate masterclass, **Mike Stelfox** (Founder of *Stelfox Design Studio*, Virginia Sea Grant Fellow, and Hackathon Mentor) bridges the critical divide between raw geospatial temperature data and the real-world human experience of heat in cities.

Mike demonstrates how landscape architects and municipal planners translate FortyGuard's 2-meter air temperature intelligence into targeted cooling interventions. He introduces a **5-Layer Priority Model for Cooling Design** (Conditions $\to$ Causes $\to$ Exposure $\to$ Vulnerability $\to$ Opportunity) and exposes the fundamental fallacy of chasing raw temperature peaks on heat maps without human context. By analyzing Washington, D.C.’s historic drainage basins, school campuses, and transit corridors, he reveals how topography, buried streams, canopy cover, and social vulnerability intersect to determine where urban cooling investments achieve the highest return on human well-being.

---

## Key Highlights & Core Thematic Insights

### 1. The 5-Layer Priority Model for Urban Cooling Design
Raw temperature alone cannot determine where to intervene. Mike outlines a multi-dimensional framework to prioritize urban cooling investments:

```
┌─────────────────────────────────┬────────────────────────────────────────────────────────────────────────┐
│ Layer Group                     │ What It Evaluates                                                      │
├─────────────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ 1. Thermal Conditions           │ FortyGuard 2m ambient air temperature, persistence, diurnal heat peaks │
├─────────────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ 2. Underlying Causes            │ Land cover (impervious % vs canopy %), albedo, building canyon geometry│
├─────────────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ 3. Human Exposure               │ Pedestrian foot traffic, transit wait times, bus stops, school zones   │
├─────────────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ 4. Social Vulnerability         │ Demographic health indicators (asthma, elderly, poverty, night shelter)│
├─────────────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ 5. Actionable Opportunity       │ Plantable public ground %, right-of-way permissions, budget feasibility│
└─────────────────────────────────┴────────────────────────────────────────────────────────────────────────┘
```

---

### 2. The "Empty Parking Lot vs. School Bus Stop" Paradox
- **The Heat Map Blind Spot:** A vacant industrial asphalt lot or commercial roof may register as the hottest pixel on a satellite heat map, but zero pedestrians or vulnerable residents spend time there.
- **The Multiplicative Risk Rule:** Thermal intervention priority must be computed as:
  $$\text{Intervention Priority} = \text{Thermal Hazard} \times \text{Exposure} \times \text{Vulnerability} \times \text{Opportunity}$$
- **The Walker Jones Case Study:** An educational campus with 418 students, 5 bus stops within 150m, 79% impervious surface, and only 8% tree canopy ranks in the top 1% of actionable risk on both clear and overcast days—making it a vastly higher priority than an uninhabited industrial hotspot.

---

### 3. 2-Meter Air Temperature vs. Radiant Heat & Perceived Comfort
- **Convective Air vs. Radiant Load:** FortyGuard measures convective air temperature at 2 meters (what enters human lungs and envelops electrical equipment). However, human thermal strain is heavily driven by **Mean Radiant Temperature (MRT)** and solar irradiance ($W/m^2$).
- **The Canopy Impact:** Adding shade or tripling tree canopy in an urban street canyon may only reduce 2m dry-bulb air temperature by a fraction of a degree, but it slashes direct and reflected radiant heat flux by hundreds of watts per square meter, reducing perceived thermal strain (UTCI / PET / WBGT) by multiple degrees Celsius.

---

### 4. Historic Hydrology, Topography & Nocturnal Cold Air Pooling
- **Buried Streams as Nocturnal Corridors:** Historic 1861 stream beds (e.g. Boschke maps) that were paved over and turned into storm sewers remain measurably cooler at 3:00 AM.
- **Topographical Drainage:** Cold air naturally drains and pools into low-lying terrain valleys. Understanding historic hydrology allows planners to identify natural cold air channels and protect them from heat-trapping structural development.

---

### 5. Implications for Hackathon Builders & Decision Support Dashboards
- **Design for the Human/Asset Scale:** Connect spatial data to real operational behaviors (e.g. outdoor worker rest cycles, transit shelter shading, schoolyard cooling).
- **Quantify Opportunity & Feasibility:** Don't just identify problem zones; compute actionable intervention parcels based on plantable surface area and municipal right-of-way.
- **Translate Data into Meaning:** Non-technical decision-makers (city council members, facility directors, school boards) need clear trade-off visualizations and risk indices, not raw raster numbers.

---

## Subtitle & Document Exports

- **SRT Subtitles:** [`informing_the_data_subtitles.srt`](file:///Users/karim/.gemini/antigravity/scratch/informing_the_data_subtitles.srt)
- **WebVTT Subtitles:** [`informing_the_data_subtitles.vtt`](file:///Users/karim/.gemini/antigravity/scratch/informing_the_data_subtitles.vtt)
- **Plain Text Transcript:** [`informing_the_data_transcript.txt`](file:///Users/karim/.gemini/antigravity/scratch/informing_the_data_transcript.txt)
- **JSON Data:** [`informing_the_data_transcript.json`](file:///Users/karim/.gemini/antigravity/scratch/informing_the_data_transcript.json)

---

## Complete Timestamped Transcript

**[00:00.000]** you

**[00:30.000]** Hello everyone. Thank you for waiting and we are all set now. Hello Mike. How are you? Good. How are you? I'm good as well. So before we begin guys, for most of this hackathon itself, you've been building on 40GARTS

**[00:59.000]** of the most precise hyperlocal insights and into how actually heat moves through a city. This next session is actually a very important one. It takes a step further and asks how do we translate that

**[01:13.000]** intelligence into design decisions that genuinely improve how people experience a place. I'm delighted to introduce your mentor for this hackathon, Mike Stelfox. Mike is a landscape architect and an urban

**[01:27.000]** architect who is working at the scene between architecture and the nature in cities. And the founder of Stelfox Design Studio. His work began with a question back in 2016. Through a Virginia Sea Grant Fellowship, he explored how a

**[01:41.000]** city could repair its natural floodways as green infrastructure in the face of rising seas. And he's been asking that very question like that. He's been asking that every day of his day. He has been carrying that thinking into

**[01:59.000]** practices at renowned firms, as well as contributing to Greenroof Gardens, urban parks, and even a memorial, by the way, on the National Mall in Washington, DC. Through his studio today, Mike does something very remarkable. He

**[02:13.000]** reveals the collages buried between our existing cities and designs of future ones as living symbiotic systems and natural materials that are being used back into the natural fabric as it grew from. He layers geospatial and lidar

**[02:32.000]** data over a deep, botanical and microbial understanding, working all the way from the root zone to the watershed. It's a passion that goes right back to his multi-generational nursery family, by the way. And here's

**[02:47.000]** why this session actually matters for you all. You have the powerful ability to understand what is still, is turning that intelligence into meaning, into something which is useful in your projects. Understanding

**[03:00.000]** what it tells us about how a real person actually experiences it at a real street, using it to design better spaces. That's exactly what Mike here is here to do for you. Translating that data into ground-level understanding

**[03:14.000]** of the benefits to the public space. His session is informing the data how we can help to understand the benefits of the human experience for the human experience. Mike, the floor is yours. Thanks, Nihal. Hey, everyone.

**[03:30.000]** Thank you for ready, Gard, for giving me the opportunity to share some of this with you. I'm going to share my screen and kind of step you through the actions that we're taking here in our studio. And we actually took a few

**[03:48.000]** steps, some past work, and looked at Washington, D.C. in particular, where we focus a lot of our efforts to actually see how we implement the 40-Guard data. So I'll step you through that now. Again, like Snihal said, I'm

**[04:08.000]** Mike Stelfox, I run on the Landscape Architecture Studio here in the District. This is a five-layer priority model that I'm going to step you through for cooling design. It's built on the 40-Guard temperature

**[04:18.000]** API in 165 years of maps of the city. Fortunately, in D.C. we actually have pretty extensive data. I'm thankful for this because it really allows us to show you some moves that we make. I think the real subject of our talk

**[04:34.000]** today is going to be about our user discretion. So a model like what I'm going to show you, like what we made, can make dozens of judgment calls, and we're going to do a lot of things that are going to be

**[04:50.000]** automated by now that can become formulaic. It can get automated over time. But now the designer or the scientist, the data expert is going to be more important than ever because their discretion is

**[05:04.000]** going to tune these models for the actions that we really want to realize here. So like Snihal said, we're going to do a little bit of british-grant talk and then some research publication of what sea

**[05:21.000]** level rise could actually mean to the city of Virginia Beach just a couple hundred miles south of here and what that means for people living amongst the climate events of the future. And ultimately what

**[05:42.000]** we're going to do is actually take on the changing environment of the world if we plan ahead, right? And this is looking at least back in 2016. I thought 2050 was really far away. Now in 2026 it seems quite

**[05:59.000]** close. But we'll get into here is actually how we step through the model for your presentation is not being shown if you are sharing your slides. I'm sharing by mistake.

**[06:17.000]** Snihal. Are you back? Not yet. Yeah. You're back. Did you all see the last few slides? No.

**[06:33.000]** Thanks for that. I'll go back a little bit. Real quick. Yep. It is visible. You can continue. Sorry. Here what you're seeing is digital

**[06:49.000]** elevation model that we showed sea level rise on over 2016 to 2100, 31 inches here in Virginia Beach and then that shows where that overlays actually with a residential community in some parks. That then could become

**[07:07.000]** a city of Virginia Beach if we plan ahead. We allow people to connect to each other but take in some of that water. Today what we're going to step through is actually how a heat map is an

**[07:26.000]** indication. It tells you that the city is hot, which we understand that is more resolution that we actually need to come in with. FortiGuard gives us these great measurements of air temperature at

**[07:42.000]** two meters, which is what a person feels when they're standing and walking around. From there, the design intervention lives where three things go inside, heat people and our power to

**[07:57.000]** actually act on that information. This method is five groups of thermal conditions, causes, exposure, vulnerability, and opportunity to explain. Multiplication is that important area

**[08:16.000]** of where we pull all these factors together and a very hot, completely empty block may look like a critical area that we need to multiply that factor across the exposure, vulnerability, and

**[08:37.000]** opportunities to impact people. We can see really where the main action areas should be. So what we did here was we took a study area of basically all 18 square kilometers, and we did a

**[09:01.000]** study of the range basions of Washington, D.C. and that's 101 square kilometers. Came back with 23,000 tiles per layer, without any gaps, and two caveats.

**[09:19.000]** Around 18 square kilometers, we actually returned empty fields because the model didn't map right in Anacostia, since in the city, a fifth of the historic basin system is actually a river.

**[09:38.000]** Ultimately, we pulled two days worth of data, one on an overcast day and one on a clear day, and we checked against the whole exercise that we'll show you in a few slides. We did a study on the

**[09:58.000]** 今回 system, and we did a study on the land plan that we mapped four different ways. There's streams and springs that were existing around 1861 here in the city.

**[10:17.000]** We have the sewers and drainage temperature model over this past summer. The table underneath is what coincides with that and the findings that we'll see later on. So when I first pulled this on the main drainage basin covering downtown DC, we look at around, there's an area around Howard University and the neighborhood of Shaw. And the afternoon field read was nearly flat two-thirds of a degree from end to end and the

**[11:00.340]** initial reading said the data didn't necessarily feedback enough information for us to really say this is an implementation area. Right, so we widen the frame and spread out kind of what we were looking at. We said on the same day Mike your presentation went away again. Just try it out. Okay thanks.

**[11:39.199]** Yep, all back up.

**[11:51.039]** Thermally there there was not necessarily enough information that we could save for certain hey this is an area we really want to intervene. So we took a few more steps to actually allow us more discretion for that. So where we looked at the streams of what's called a Boczki map in 1861, a lot of these instances have become storm sewers and what we found was that we could predictively assume that the areas where these streams ran on the ground plane before

**[12:41.559]** they were covered up with asphalt and the rest of you know our urban conditions. They're predictably cooler at 3 a.m. right so right romantically if you were to talk about this right you could say that like our city actually has markers of what used to exist here. We then added topography and we looked at how the streams actually went from showing really meaningful information potentially to somewhat marginal. We see that cold air pools in low ground and streams mark where

**[13:30.799]** that low ground actually is. The terrain is a historical indication of it and the valleys and the water cuts are doing a lot of the cooling while today a lot of that actual water running over land is gone. So then we jumped into what temperature and vulnerability mean together. So our third finding is the one with some political action and wait for when we talk about how we design our cities. So east of what we see here on the left as a stream or this major

**[14:13.039]** rivers Rock Creek and temperature and vulnerability kind of run in opposite directions. You can see what's mapped here is people of color folks with asthma or experiencing poverty. These measures correlate negatively with heat because the highest ground in the frame is the commercial core and almost no one lives there. If you read the heat map this way you'll send crews to areas where they're not necessarily impacting people who live in these conditions and so the

**[14:54.559]** interpretation here is that we need to be aware of how we direct what we're seeing. So when we tune the model to look at where people live and sleep overnight we actually find an area called Walker Jones is where a school is. And this isn't necessarily the hottest area in all of DC but it's an educational campus with 418 students. Five bus stops within 150 meters and 80% canopy over 79% impervious area. It holds the top 1% on both the overcast day and a clear one and not necessarily a weather artifact. On one

**[15:53.800]** specific site we have all of these rationales proven out. So at 300 meters around the school canopy today is about 8%. Plantable ground that we're finding is 20%. This is the area that we can actually intervene in and two of the parcels here actually carry most of the opportunity area. There are 173 parcels and just under 44 acres. So the next question is what does that planting actually do for us if we were to intervene here? Honestly fitting this

**[16:42.960]** field zone canopy coefficient tripling the trees moves the afternoon air by a few hundreds of a degree. Small honestly and a few reasons for this. The field resolves near one kilometer so a street corner is below what we can actually see and the air at two meters is not exactly what we're feeling. The shade moves the radio. Mike your presentation went okay. Okay I think there is some button that is being pressed because of which the presentation is going again.

**[17:38.679]** All right here we go.
