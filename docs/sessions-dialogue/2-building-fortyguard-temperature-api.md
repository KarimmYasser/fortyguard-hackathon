# Building on the FortyGuard Temperature API® — Full Session Transcript & Summary

**Recording URL:** [Zoho Webinar Recording](https://webinar.zoho.com/meeting/videoprv?recordingId=63d82747aa1472191eb371cf93f5e4894b610ee1af6efd8c6649e1debbfc0024&x-meeting-org=935374719)

**Date:** August 18, 2026 | **Duration:** 1 hour 1 minute | **Language:** English

**Speakers:**
- **Nahil** — Hackathon Organizer & Community Lead
- **Fawad** — Head of Software Engineering at FortyGuard

---

## Executive Summary & Session Overview

This session is a technical mentorship webinar for hackathon participants and developers building applications on the **FortyGuard Temperature API®**.
Fawad (Head of Software Engineering at FortyGuard) and Nahil guide participants through API authentication, key endpoints, data structures, polling architecture, sample Python workflows, and submission expectations for the hackathon.

### Key Highlights & Technical Insights

1. **Core API Capabilities & Data Scope:**
   - High-resolution outdoor urban temperature and microclimate data (surface temperature, apparent temperature, heat index).
   - Support for historical observations and forward-looking forecasted values.
   - Spatial breakdown by bounding boxes, polygon areas, tile grids, and parcel-level segmentation.

2. **Architecture & 6 Core Endpoints:**
   - Major endpoints include Heat Map, Parcel Analytics, Time-Series / Historical Data, Forecast Data, and Environmental Parameters.
   - **Polling Pattern:** Due to heavy geospatial computations for large polygons, the API processes queries asynchronously. Clients initiate a request and poll every 3–5 seconds until results are ready.

3. **Quickstart Template & Code Walkthrough:**
   - Walkthrough of the official FortyGuard Temperature API Quickstart template repository.
   - API Key setup via headers, setting bounding boxes, configuring data parameters, and parsing JSON payloads.
   - Handling rate limits and request concurrency.

4. **Environmental Analytics & Case Studies:**
   - Calculating standard deviation, temperature thresholds (e.g. continuous hours > 35°C), and heat wave event detection.
   - Identifying 'Hottest to Coolest Parcels' to prioritize urban cooling interventions and heat resilience.
   - Generating automated heat analysis reports and visual distributions.

5. **AI & LLM Integration (Agentic AI Track):**
   - Encouragement to build Agentic AI workflows, autonomous climate bots, urban planning copilots, or predictive alerting agents utilizing FortyGuard API endpoints.

6. **Hackathon Submission Guidelines & Q&A:**
   - Mandatory deliverables: A working live URL / deployed application, demo video (explaining architecture & value proposition), public GitHub repository, and documented use of the FortyGuard Temperature API.
   - Post-hackathon Startup API program for teams wanting commercial continuation.

---

## Agenda & Timeline Breakdown

| Timestamp | Section / Topic | Lead Speaker |
| :--- | :--- | :--- |
| `07:14 - 09:45` | Welcome, Housekeeping & Speaker Introduction | Nahil |
| `09:45 - 13:30` | Overview of FortyGuard Temperature API & Data Models | Fawad |
| `13:30 - 18:30` | API Architecture, Polling Pattern & 6 Key Endpoints | Fawad |
| `18:30 - 24:00` | Quickstart Repository & Python Code Walkthrough | Fawad |
| `24:00 - 32:00` | Environmental Parameters, Metrics & Thresholds | Fawad |
| `32:00 - 39:00` | Parcel Heat Analysis Reports & Spatial Visualization | Fawad |
| `39:00 - 44:00` | Agentic AI Applications & Hackathon Track Ideas | Fawad & Nahil |
| `44:00 - 54:00` | Hackathon Rules, Submission Criteria & Deadlines | Nahil |
| `54:00 - 01:01:03` | Live Q&A, Technical Support & Closing Remarks | Nahil & Fawad |

---

## Complete Spoken Transcript (Timestamped)

> *Note: Dialogue has been cleaned and formatted with timestamps for easy reference and searchability.*

**[07:14.639]** Hello, everyone. Guys, we do have a request before we start the webinar itself is to keep the Q&A section related to the Q&A and ask the questions which are there. We do get your excitement that you want to introduce yourselves.

**[07:42.620]** We have a team who wants to dedicate the time and effort to answer all of your questions which are there. So let's just keep it to the questions itself related to the session, or if you have anything related to the Hackathon as well. We have people who will be helping you out

**[07:57.500]** on that part as well. So don't worry about that. And regarding the previous sessions, we will be sharing all the recordings. So don't worry. All right, so we can get started

**[08:07.199]** and there are people who are coming on board as well. Welcome for Vad to your mentorship session. I'll be taking over for a few seconds and then I'll be going offline for this. Welcome guys to the Hackathon and to getting hands-on

**[08:21.060]** with like the 40 guard temperature API. I have for Vad here who's our software engineering lead. He's heading our team at 40 guard. He is the mastermind behind how the configurations regarding temperature API work, the dashboards work. He is the one who's dealing with all of these things.

**[08:38.980]** And our technical questions and aspects is he is the head of the person you need to contact to. So for Vad will be here to answer all of your questions here live as well. He will be dealing into one of the tracks as well if I'm not wrong, right?

**[08:52.259]** Pavad, you'll be talking about agent to AI. Pavad is a fanatic about agent to AI, by the way. This guy, I have seen him work on like a lot of different things. He has a lot of experience as well, eight to 10 years of experience coming into the industry.

**[09:08.629]** There is a lot that we learn from him every day about the technology that we don't know about and how to use AI or even code as well. So there's a lot that is there on your shoulders right now for Vad. So people who are here, participants,

**[09:23.710]** we encourage you to ask questions regarding the API. You have been already given access to it or if you have not yet taken the access or generated your API key, Pavad will be telling you about where it is located as well but we did talk about it in the previous session.

**[09:38.190]** So don't worry, you are all on board and you still have time to get it as well. So Pavad, over to you, let's get started. Yeah, so I'll just present now. Okay, so as Nahil mentioned, I am the head of software engineering in FortiGuard.

**[10:00.600]** So my journey started here quite recently, I would say three, four months back but pretty excited to work here. So moving, this session is mostly about all the technical aspects of what we are going to go through within the hackathon.

**[10:20.620]** We have the set of endpoints, majorly six endpoints. There could be many smaller ones as well but all the things that you need are within these six endpoints. So moving ahead, yeah. So this is how I planned my session.

**[10:42.669]** So I'll be talking about how we can set up everything. I can just go over the temperature API quickstart repo that is already set up. For you guys, I have actually added it as a template and you guys can just use it to building everything. So everything's there is defined pretty nicely

**[11:06.590]** and a lot of details. Then I will be also talking about a use case from there. I think it's sort of a case study that we did for a client. I think I'll be showing it just briefly. And then I think there are a few things

**[11:24.940]** that we can talk about as agent tools that we could use. So the first 20, 25 minutes will mostly cover the temperature API and all the use cases and everything. And then a few minutes on the agent AI and then we move towards the question answer. So let's start with the part first,

**[11:47.470]** which is the temperature API. So talking about what this API actually is and what it isn't. So this is basically a heat catalog that we have developed within the 40 guard, the ML team, the software team, all we are part of it.

**[12:08.309]** And the catalog, it has the forecasted data of up to 12 hours. So it's not just like the previous data, historical data or the current data, you can also have the forecasted values as well, like up to 12 hours of data.

**[12:25.059]** So for temperatures, which is a really good thing, I think some of the use cases or some of the people might be building upon this. So it's a very good start for you guys. Then I think we have all the data heading back till 2021, till today.

**[12:41.940]** And as I mentioned, 12 hours ahead of today. So I think in the previous session, Snehal talked to you about the granularity. I think we have three types of it. We have three, it's limited to 60 meters, 80 meters and 100 meters.

**[12:59.919]** So it's according to the use case that you have. Secondly, I think we have been getting a lot of questions on the Slack and I think people are asking about what data coverage or which geographic coverage we have. So let me make it very clear,

**[13:16.039]** like this is only limited United States. And hopefully someday we will cover the rest of the world as well. So all of it. So if you guys want to go ahead and play around with the APIs,

**[13:30.919]** if you're going to set up the location to Dubai or Berlin or whatever you are, apart from the US, I don't think it's going to work and it's just going to spend your credit. So I would advise not to do that. That everything is in Celsius,

**[13:47.679]** including the thresholds you pass out. So the geo JSON data, it's all majorly longitude, latitude. So you really need to know which area you are exploring. Just use the Google or whatever means of searching or just to check out what area you're using

**[14:07.879]** and what are the latitude, longitude for it. Then those six endpoints we have, I think they are different on everything. And yeah, a lot of people are asking also about the API that's premium. So let me make it very clear.

**[14:26.860]** This is the most premium API key that we are heading to you guys that we are allowing you to use it. You can utilize it and you can make it to run everything you have. So it has all those limit

**[14:42.100]** and actually the limit is double than what we are normally giving. So you guys can use it, plan it accordingly. Then let's move towards the next slide. I think I can just explain how from getting the Slack invitation

**[15:01.809]** and then users getting to register themselves. So you start with registering yourself on the dashboard on FortiGuard and as soon as you log in in the profile section, you can see the API key section. And if you're not created it,

**[15:16.850]** you just click on create API key. So that is the key that you are going to copy. Just save it somewhere else. I think you're also going to get an email is going to be there as well. You can just copy it.

**[15:29.990]** This is the API key that's you're getting to put it into an ENV file or whatever the secret manager that you're using. So you'll just be using it to make sure like nobody else gets it and make sure that the repos that you're creating

**[15:49.409]** add a git ignore file and try to add the .env there. So it does not get uploaded into the data repository. So, and yeah, one good thing about using the credit is that if a task fails, it does not cost you any credit. So just try to experiment freely and you have about 2 million credits per API key.

**[16:22.070]** So you're good on that. Moving ahead, I think these are all the six endpoints and I'll just talk about like majorly, the five are one for the analysis and talking about heat map, environmental parameters, satellite, straight view, heat intelligence.

**[16:40.279]** And then we have the one for the status ID. So whatever those five APIs return like the activity ID, that is something you use it and use it instead of the ID to call it. Because these APIs could take, if you have a very large area that you're covering,

**[16:59.220]** it could take a lot more time. So the idea is you add polling. So every five seconds or three seconds, I would assume you can just start polling it and as soon as you have the data return, you could use that.

**[17:16.000]** So I'll just talk a little about the APIs that we have but the heat map API is basically, it returns the tile grade of surface temperature over an area. So there are multiple parts of it. I think I'll cover it once I move ahead. It is basically exceedance, persistence, time of measure.

**[17:40.190]** I'll talk to it about it in more details in the next slides. Then you have the environmental parameters. You have apparent temperature, heat indexing, humidity and all those other types of it. I think it's clearly mentioned in the documentation.

**[17:57.069]** So you can check it out as well. Then we have the satellite view, satellite and it actually covers all the areas like building, tree road and everything. And then we have the street view. We actually provide the ground level segmentation as well.

**[18:15.400]** And then we have the heat intelligence. So it is actually a PDF generated and it has five sections to it. And you get all the particular details in a very long, I think PDF is generated. So this is something it could take up to minutes.

**[18:31.160]** And that is why I was asking that maybe adding a polling to calling the status API after some time, just to know if it's completes and then you can just download it. Moving ahead. So this is something I was talking about.

**[18:47.039]** So each of these APIs, these analysis endpoints are asynchronous, which means they are non-blocking. For all the software guys, I think you'll understand what I'm saying. So we cannot hold the server for too long. So what it does, it creates a heat map

**[19:05.150]** and then you use the status API to getting the status of if that heat map or heat intelligence report is generated and it gives you a status of completed. Moving ahead. So this is something we have, I think, if you go to the quick start repo

**[19:25.779]** and as I talked about this is something already there and once everything is done, I think it'll just return everything to you like whatever area of interest is the start date or all the filter types. So there are multiple filter types,

**[19:41.940]** each of them like single hour, we have range of hours, we have a single day, we have a range of days and then we have a single month. So we are giving you the opportunity to get as much as 30 days worth of data return to use for your use case.

**[20:00.099]** And I think if you guys are going to use it, I think maybe some sort of caching, you guys can use it, maybe store it with yourself just for those one month or something. And if you do your analysis,

**[20:15.950]** it will be a good sign for you because I think every time if you bring in the data, it will take more time to load. Moving ahead, I think we have already shared the quick start repo and I think this is a template,

**[20:32.029]** you can just sort of create a new repository, you can use it as a, I would say starting point. There are some setups as well, there are some notebooks for use cases as well. I think it runs on the Jupyter lab and I think mostly all of us have a lot of,

**[20:55.170]** I would say knowledge about coming in from the university, especially the software guys, you can check with the Python and basic language. So it's actually set up that way that even people with low coding environment experience can also just add the environment variables

**[21:14.329]** and start working on it. So yeah, next I'll move to, maybe I'll just unshare my screen and I will walk you through the Jupyter notebook. So I'll just give me a second. So if you guys go to this is basically

**[21:48.829]** what's inside the temperature API quick start. So when you go there, I think in the notebook sections, if you go through, this is the first slide that is something just to get you set up for whatever you're planning to do. So in the environment file,

**[22:11.599]** I think there's a way and describing the read me, I cannot share the environment file I have on live here, but it's clearly mentioned the read me. You can just open it and you can start playing along with this and each part that you just go, you start running it.

**[22:31.740]** So I uploaded it and I think this is the base URL we're following because this is the live environment that we're hitting. So I ran this and I think it's all good. Then I think this is how you're going to get how we are using the.

**[22:48.769]** So on the API key that I use, I think I will use about 1-8-7-4-20. These are the sort of credits that I've used altogether so far. And if you get the individual credits being used for different type of APIs,

**[23:04.789]** I think for tile segmentation, I use 72,000 and so on. So heat intelligence, yeah. And this is how I made these many calls and these are these many credits I have spent. So the idea I'm giving you this is because I think even though the credits are 2 million,

**[23:21.750]** but it's still limited, I would suggest not wasting it all. Try to use it to your requirement. Don't overuse it for smaller things, make it more useful to your use case that you're building or the idea you have

**[23:39.890]** or multiple ideas you have. Then moving to the next one, I think I'll just talk about, this is the create heat map. So if you go, this is the end point I think I talked to you about.

**[23:53.450]** So on this plan, I think we have the premium one for you. So the limit is about 15 miles square. So this is the area of interest size. So basically a tile that you create, that latitude, longitude, whatever that is,

**[24:11.569]** I think this is something you need to be aware of. It should have the longitude, latitude, and the date time, start time, filter type. So basically what I described, filter type one is for single hour, range of hours, and four is for range of days.

**[24:29.130]** So you can plan it accordingly. Then we have also the analytic type. So this is like basically the TCM is, this is just the simple snapshot. And then we have these other analysis things like time of measure, exceedance persistence.

**[24:47.930]** So exceedance is something like for how many hours a certain value was above the threshold. For example, the temperatures you're getting is 25 to 40 degrees and you want to know for how many hours it was above 35 degrees Celsius. So it gets you that.

**[25:05.890]** And for persistence, it's quite similar, but it gives you a continuous long run. Like for example, continuously it stayed above 35 for six hours, seven hours. Now moving to the next part, I'll just move. And yeah, this is the granularity

**[25:21.589]** that we talked about the spatial resolution. I think 100 means the 100 meter, 80 meters, 60 meters. And then this is the response schema. So all of this is shared. And I think you guys can just look into it. We are also returning the average temperature,

**[25:41.130]** minimum temperature and the maximum temperature for you guys. And all the temperatures are in the Celsius. Now moving ahead, this is just before the call, I tried to run it because I didn't want to spend so much time on it.

**[25:57.539]** I just created a heat map, a polygon. And this is the date and this is the time. So it's just for a single hour. And I selected the granularity to be 100 meter. And I think it worked. And this is, if you see the response is continuously

**[26:15.099]** being checked after two, three seconds. So we, and then it completed. So this is the place where we stop. And I think we have everything. And if you look into the stats, this is the minimum temperature.

**[26:27.900]** This is the maximum temperature. This is the mean. This is the standard deviation. And then we have actually used the map library to just get the distribution of it. So this is just, I mean, this is just for one single hour.

**[26:42.220]** So if we increase it, maybe we have more temperature distribution. And then there are other things as well, like the heat, the exceedance heat map that we were talking about, we created exceedance map, like for this date and the end date.

**[26:59.609]** So it runs for almost six days. We have the filter type four, because it's range of days. And analytic type is exceedance. We set up the threshold 35 and the direction is above, which means above 35 degrees. So it gave us all the results.

**[27:15.890]** And this was the activity ID. And I think this is how it's going to maximum. It took about, was about six hours and minimum is two. So this is something I wanted to share as well. Then talking about the other part is the environmental parameters.

**[27:38.710]** So there are multiple environmental parameters. I think I talked to about a few of them. So here are these, like the heat index Celsius. These are the exact values that could be used apparent temperature Celsius. Here are the descriptions as well.

**[27:58.369]** So due to the time restriction, I don't think I could go over everything in too much details, but I'll just run over it. CO2, methane and everything. And then you have, then we started running it and we got like this one ran pretty quickly.

**[28:16.289]** Like we have set up the environmental variables, latitude, longitude, temperature, start date and filter type two. So it gives us everything we needed. And then we actually plotted it. So this is the values we are getting

**[28:33.980]** for each of the environment variables for each hour or each time duration that we're running it. And this is how the parameters are plotted here. So we can see. So this is just an idea how we are pulling things together. This is something you can use.

**[28:50.559]** And this is something we're using the solar irradiance thing. Talking about the satellite segmentation. So this is also something you guys can use. So we can also classify what actually lives within that tile.

**[29:10.009]** Like it's a building, a router road or the sidewalk or earth or maybe grass. So most of the world is green by the way. So that is how like we envisioning how we can set it up like. So we created another set create,

**[29:27.680]** used the client to create satellite segmentation for the latitude for this location. And we plotted it. So this is what we got. This is the original satellite tile and this is the segmentation mask that we're using.

**[29:43.869]** So it shows that we are getting a building 100%. So it's just returning like what we are looking into it. So it could be like for some other area, it could be grass or trees or anything else. So this is just a view of it. And then when we move toward the street view segmentation,

**[30:04.480]** you can look into it like there are different views for it as well. Like what we are covering like this gives you a straight view from within the street view. So if I ran it like I created a street view segmentation and this is how the street view segmentation we analyzed it.

**[30:25.740]** This is something we build and this is how we segmented. So you can see that fountain covers 34.5% of it, then tree, then sky and water and grass also. So this is how we are segmenting it. So it's pretty good use case for it.

**[30:43.099]** And I think this is something you guys can use as well. Then the last part of it is the heat intelligence reward. So this is something that's pretty comprehensive because we're using very sophisticated tools, using the latest tools to build it. I think it has a lot of knowledge about a single tile.

**[31:08.170]** So a single place where you can just point it in the app and it will return to you all the analysis categories. So you can also select the categories. Like for example, this is the geographic and it just tells you about the general location, terrain, elevation about it.

**[31:23.130]** Then we have the environmental factors analysis. Then we have the urban factor analysis and it also gives you all the surface fractions, zoning, planning. So this could be a use case for many people like the builders or anything.

**[31:37.529]** Then we have the events like what are the extreme weather or heat event history. So it's actually a very good way to know about a certain location. Then we have the anthropogenic factors analysis that you could use as well.

**[31:54.910]** So I created a heat intelligence for this latitude longitude and this took some time because I already told you, it takes about two to three minutes and I think I just loaded it here. So this is, I'll just quickly show you how it works. This is, let me just, so this creates a complete report.

**[32:25.079]** It has all the table of contents and everything. And if we go in detail, like this shows you which was the part of the map that you selected. Then it gives you all the environmental factor analysis. Like it's not like something that is, that could be random or anything.

**[32:49.230]** It's actually tested out and it, every single source is like a really accurate up to, I would say close to a hundred percent. So all the pollutants and everything. So it's all the classification that's done. It is giving you the details

**[33:13.589]** in the very manner that you want. Like every single thing, like soil moisture and permeability and humidity levels. So it's a very comprehensive 25 page document. And I think it's, if I get to explain this, I think it's going to get over the time

**[33:32.700]** we have limited time today. Then lastly, I'll just talk about the use cases. So if you go on here, I think we have created use cases here as well. So this is the use case that I'm going to show. It's the parcel.

**[33:49.200]** Parcel is basically a more smaller area than a tile. Like tile could be 180, 60 meter. It could be even less than it. So this was a sort of a use case we developed to demo. And this is something that shows like a six different areas that we are covering.

**[34:13.820]** So let me just walk you through. We selected those areas. And if I go, I will just share the results. So this is like the buffer, the granularity is 80 here. The window is it's 28 July to 3rd August. So this is what we're covering.

**[34:36.659]** Then if we are loading this data and building. So this is like all those six areas. So we've given them IDs and we're giving them names and everything. So how many vertices and acres of area so altogether this is 17.38 acres of area

**[34:56.659]** and how much it is covering. And we've also drawn a visual representation of it. So this is basically a tile. So inside a tile, you can see that these are the six points that are covered. So going further about it,

**[35:13.400]** I think we were looking into how we can analyze it differently. So over these snapshots, we can see the daily peak is around 36.3 and the average is like 24.2. So it means that at some point it was speaking a lot.

**[35:35.039]** And then we actually draw it here. So we get to know like this is basically a heat map generated so where it heats and it gives us all the mean and the daily peak areas. So there's a distribution of it as well. And you can see that at some point,

**[35:51.789]** it got over a reach around 98.5 Fahrenheit, which is about 37 degrees. And then what we did was we clipped them each parcel to rank them. So this is how we ranked them like these old six parcels, the names, acres, the areas.

**[36:11.039]** So how they differentiated. So how much they cover. So the hottest to coolest parcel, that's like 0.77 degrees Celsius, South Campus Edge versus the River North. So this is the analysis it's giving.

**[36:28.179]** Then we have the parcels weighted by the daily peak and also showing the distribution as well. Talking further on, I think we are also giving the exposure duration per parcel. Like this is where the exceedance and persistence comes in.

**[36:49.420]** Like how much time the longest run was. Like for example, this is, it remained persistent for above a certain point for five straight hours. So that's a lot of heat. I think this area faced a lot of heat over this time.

**[37:09.610]** And here, how it is just showing it. So this is just a visual way of showing it. Like for example, for more than 19 hours, it stayed a bit above and then for five hours straight, it was above the threshold. Then talking about the satellite segmentation,

**[37:29.250]** you can see these areas. It shows about the road route, building, grass. Usually the areas around the buildings are much hotter. Basically the roads and everything and near to the others they could be. So it is showing all those as well.

**[37:47.480]** So building, grass and everything. So I'll just skip over it. And then we have the street view as well for some point. So it also shows like it's road sky. It's just giving the segmentation to us. So all for all those six areas.

**[38:09.480]** Yes. So moving ahead. This is like the charts that we've drawn just to show you the heat distribution and everything for the environment variables. So pretty much that's all.

**[38:28.659]** And I think at the end, we also added some heat analysis reports as well. So all of it, if you're interested, I think in outputs, you could just see what we've done. So it's already there. Some of the samples are there.

**[38:45.780]** You can see it. So this is something it's been generating. Yeah. Okay, so I'll go back towards it and I'll talk about the agentic AI as well a bit. Let me share my screen.

**[39:11.739]** I'll quickly jump in till the time for others sharing a screen as well. So the direction that for others showed as an in-depth knowledge about how you actually deal with the temperature API is talking to you about every endpoint that we serve,

**[39:27.739]** what we can do with it, the parcel demonstration that he has done right now. This is crucial for like a lot of different tracks, technically, if you're building something which is on a cooler route, you're going for like industrial and enterprise

**[39:39.719]** where you're targeting like logistics. You're talking about like data centers. Data centers is a big thing and they are heating up pretty often as well. So these kinds of parcels, just think of it like assets and buildings,

**[39:51.059]** even like investments when you're doing on buildings, so you get to see what kind of assets and infrastructure are being affected. This is one use case that we are just showing you. This is just a starting point. This is already shared within the API

**[40:05.840]** quick start guide as well. And in terms of integration as well, if you do have any questions up until now, you can post it in chat as well. And if not, for a while we'll be there on Slack as well to attend all of these questions as well.

**[40:19.599]** Over to you for a while. Yeah, so the last part, I am afraid I don't have enough time, but I'll just quickly walk over the agentic AI thing. So basically what you guys can do is you might be building a solution.

**[40:38.360]** So for example, one of the sixth location that we showed, one of them might be a worse for your idea, for example, the ground floor cafe terrace or something. So it's really good to know that which of the APIs are essential to you.

**[41:00.940]** So which of these could give you a better answer to what you want to serve. So I would say that you could use, for example, it might need four, just like in this one. You can just rank the sites on duration, not B or the model that you use,

**[41:21.880]** for example, any LLM or something, some solution you're building yourself. It's really important to know what the use case you're serving and you're using those APIs in that way. So that was one observation.

**[41:38.280]** Yeah, so talking further about it, you just need to make sure that the model that you build, it should be more relevant to you than the endpoint list. So you should know like heat map, what it serves, the environment variables, what are they sending you back

**[42:00.969]** and also the heat intelligence, satellite. So it's not something, the agentic, it's only depends upon the idea that you're building or what you have in mind. So use the agentic AI track for that purpose. Moving further on, I think it talks about

**[42:21.630]** the plausible temptation and everything could go wrong. So yeah, so as we know, I think majorly different,

**[42:37.440]** there are people who are going to go solo for this and there are a few people who are just going to start with the team. So make sure that you have the budget in mind when you're using those credits and everything don't stick to a particular framework,

**[42:59.309]** I would say, like it's mentioned that maybe the better would be to use a maybe cloud desktop or any LLM or anything and use the API for the coverage and everything. Moving ahead. So I think this is the track six that we're talking about.

**[43:20.789]** I think there are a few examples given here. I think heat response agent. So how you can use it. For example, you have a tool that could, you give it data and you ask it something and it analyze it and it gives you a better result.

**[43:39.670]** So one of the example could be to create an agent that does it, the other could be to have a bot. So basically the terrorist question that I asked and it gives you the evidence to support it and the judges know that you can see the reasoning is there as well.

**[43:57.460]** And then there are a few things, the alert automation engine as well. This is something we are building ourselves also. So for example, you get alerts to an area that's being above 32 degrees. So these are some cool ideas that you guys can work on.

**[44:15.139]** I think the agent AI, we are living in a world, I think it's more easy to build something and more difficult to understand the problem. So I would assume that whatever you're building, try to understand what you're building, then go towards the development and everything.

**[44:35.250]** And I think we are at the end of the session. So let me know what questions you guys have and the team can answer a few as well. I can vouch that the team has been answering questions while you gave a magnificent mentorship session here for a while.

**[44:56.849]** A lot of people were asking regarding how do they get access to the Quick Start? How do they navigate through the Quick Start? If you can give a quick overview regarding how they can start with the Quick Start itself. So basically, it's a public repo

**[45:13.230]** and I think we are already sharing the repo access links to everyone. So it's a public repo, anybody can just clone it and start using it and then you build your own solution to it. And if anybody is finding it difficult to find just,

**[45:33.679]** I think in the chat, we can just give them the access to it as well. All right. So there are people coming up with, is it possible to get reviews on your solutions along the way?

**[45:44.280]** Yes, of course. If you do have a developed idea and you do want reviews on that, you can email hackathon at threatfortygar.com as well to send your ideas. I'll give you a quick hint

**[45:57.760]** regarding how you can frame your idea itself. The criteria of judging that has been shared with you. Do make sure it falls under the whole category itself so that even you can decide whether or not to move forward with that direction. If not, and you're uncertain

**[46:12.800]** between two different possibilities to go forward with, we can advise you. However, we will be screening through the projects that you submit at the end of the day. We cannot give you a lot of information about it. We can give you a general direction

**[46:26.199]** in terms of what you're thinking and what might be the best approach of it as well. I need technical support with the API. Can I reach out for how do you, do you want to take that? Yeah, we are all,

**[46:40.019]** all the software team is available to support you throughout the day and every, you just need to send a query on the Slack. Use the Slack channels wisely. For the technicals, we have separated them and for anything else, there's a separate section as well.

**[46:57.059]** So we have the experts sitting there just to answer you. So make full use of it. Also, if you use your credits for the API, unlikely, but if you do so, we will be happy to accommodate that as well. So don't worry.

**[47:14.730]** We want you to experiment, test it out thoroughly, and we want a very good product from out of you guys as well. So don't worry about that. You can go ahead and test it out to the utmost limit that you want.

**[47:25.800]** Also one point to make, I think to all the attendees that are here and even on Slack, we have just the official way of communicating is Slack if there's all the email. So if there's anything else, any community,

**[47:42.519]** I can say you just need to clarify it. Yeah, that is not an issue. And I see people who are talking about if they, the report that was displayed is not on the repo itself, is it not there on the repo for? Which?

**[48:00.219]** The parcel repo that we just did. That is something you just, I generated it for the demo. So you guys have to run the code to generate it. I think there are several as well. There is one related to the bus stop

**[48:13.460]** and you guys can quickly just, it's like technically like a Jupyter notebook, right? And there are cache results as well. If you don't have the API access right now, you can use the cache results and just press play, play, play

**[48:24.780]** and you'll get the end report as well in order to see how everything works in terms of results, how you get the API endpoint, how every endpoint is actually configured. How do you have to put the headers in and all the other configurations that are required as well?

**[48:46.800]** Yeah. You can pick, I did see one more, I'm sorry for that. You can pick any idea that is there. You can, what we require, there is one more innovation. So it is up to you how you innovate that idea from scratch

**[49:02.650]** or if you want to build up on something which is pre-existing, that is also fine. But we want to see your touch into the project that you are delivering, how you came up with the innovation. What was the idea behind it?

**[49:14.409]** What did you improve in it? So that's how we can check how innovation is coming into the place. Yeah, Pavad, you were saying something. Yeah, I was just mentioning that. Is there any other question?

**[49:29.090]** Would the bot answer any of my technical questions? Pavad, you trained the bot as well. You can answer that. Yeah, for any technical, I think it's going to answer you anything you need for the hackathon.

**[49:41.630]** So try to use it wisely. For the projects itself, it's not limited to Jupyter Notebooks. What the submission criteria is, there should be a live website in order to check your results as well.

**[49:57.090]** A live demo video, as well as you have to add Fortiguard Hackathon FG as a collaborator on your GitHub repository. Yes, I think there's only one way to judge it. I think you have to add us as collaborators, so don't miss that.

**[50:16.139]** In case your repo is private. Even if it's not private, we still advise you to add us because for the screening, if you are, I'll make this very clear, guys. If it's not added as a collaborator

**[50:31.880]** on the GitHub or your repo, and we don't have access to your code to see how you have utilized the Fortiguard API, that is like we can't move forward with the judging criteria for you. So the submissions that we send to the judges,

**[50:47.670]** this submission would not be counted. So this is a pre-limb for like you need to have, this is a prerequisite, by the way, that you need to add Fortiguard as a collaborator on your project. There are two to three people in a team can all of,

**[51:11.039]** okay, yeah, all of you can join the temperature dashboard, it's complete. Everyone will have a different idea, right? And all of you can generate your own API keys and then work on your way as well. But the final result, you will need to submit one API key,

**[51:25.559]** that's fine, but I would advise everyone in the team to have their own API keys so that you have the freedom of experimenting with the API on your own as well and using your own credits. So just to add up to what Snail mentioned,

**[51:40.030]** I think it's good to get individual guys should get their own keys because you will be setting up everything on your local PC as well. So each of you have a separate one. So that would be key for your work.

**[51:56.710]** By the way, whatever solutions you guys are building, it is your own. We will be broadcasting, we will be sharing it on all of our social medias and beyond to show like team A has done this, team Fawad has done this and we are proud to present this

**[52:12.230]** and this is your idea and we'll keep it as that. So if you want to broadcast it, you're broadcasting it, that's fine, but do not leak any API key, which is there, which is related to you. And if you do end up getting all your credits used up because of that, that will be a quick bit problematic

**[52:28.469]** for you at the end of the day. It just goes with the silences that we're just trying to navigate between all the questions which are there and trying to pick the best ones that we can. I think we are above our time

**[52:56.559]** and we respect all of your guys' time. So I think if there are any further questions, we are available on the Slack channels as well. You can just email us as well. So... It's fine, we can go like five, 10 minutes over as well

**[53:12.519]** if people have questions. However, I did see one question, like if it's clashing with 40 guys' products, it's fine. Go ahead, clash it with our products, it's fine. If you can make something better out of it, you're all means, go with all means and you're upper.

**[53:26.559]** It's not, you won't be hampered or you won't be penalized for it. We respect the idea that you are bringing in and we will account that as well, so don't worry. If we are building something and you can do it in a better way than us, I think we would appreciate it.

**[53:45.280]** There's always room for improvement. Always, yes. Can you seek technical support outside? Yes, you can. If you are not a technical expert and you have someone who can guide you

**[53:56.449]** on technical aspects and they are willing to help you, that is totally fine. But if it's something related to the Temperature API and you're not able to understand the results or the data itself or the reasoning behind it, this is where we come into picture as well

**[54:13.119]** and we can provide you more details about it. I see a question related to the request. So we do have the rate limiting applied, but it's only for like someone shouldn't bombard the service. So we're limiting it, but as such, there's no limit for a day or something.

**[54:34.570]** So you guys are fully, you can avail it fully.

**[54:45.489]** By the way, this is a global hackathon, guys. People are joining from all parts of the world. The API itself is in US. The coverage is completely within the US. All parts of the world, we have street data for US. So whatever project you are building on,

**[55:02.750]** the idea is you can target any place within the US and you have all the data. Looking at right now, there is a heatwave going on, started in early June in US. I think every part of the world is actually experiencing heatwave,

**[55:16.190]** but US, you can target that as well. You have monthly data, yearly data, which is coming in and you can accumulate that and use that as well. Will you submit your tasks and other links like videos, documents?

**[55:36.239]** We will be sharing a link with you guys near the submission date as well, so don't worry. Keep an eye out on Slack and emails as well. We'll be updating both and you will get the link, just be patient about it. While you're making your project and designing everything,

**[55:52.159]** what you can do earlier on is add FortiGuard as a collaborator already. And if you do so, you will already be done with one prerequisite and the other parts we'll share it with you, so don't worry.

**[56:09.550]** I think we have, how many requests per layer allowed for the API, the rate limiting question for us? So hourly, we have put a limit to it, not the daily one. hourly, because mostly somebody can just, as I mentioned, bombard the API service, so we're limiting it to not more than,

**[56:31.630]** I think, 100 requests per minute or something. But as such, there's no other limits. We appreciate how everyone is gonna code and use the API. Let's not test the rate limits and, you know, reverse engineer it. Let's be respective about it

**[56:50.230]** and let's not do all of this. But regarding the late limits, you are more than welcome to test it out as well, but this should not be a problem regarding the day you can make multiple queries as well. And if you do end up facing any issues,

**[57:04.110]** as far as I've mentioned, our technical team is there to support you on that, so don't worry. All right, I think so we have covered all the questions which I can use here. The API access will end after the submission,

**[57:21.440]** like when the judging date has ended, which is 16th, and the API access will be revoked since this is an enterprise-level API key that is being available to you all. And these are APIs which are being used by bigger companies as we speak right now.

**[57:39.320]** So we will have to revoke the access as well. But if you're interested in using it, you can reach out to us as well. If our implementation is very nice but we don't have a presentation. Okay, so 10% goes into like communication

**[57:59.000]** where the presentation comes into place. It is fine. If, I'll tell you one thing, there is aspects where you can't talk about a good thing which is there, but if the product speaks for itself,

**[58:12.380]** you don't have to talk about it as well. So in your presentation, even if you fumbled or you think you fumbled within it, that will be fine. We will not be taking it to like, oh, you are an NVIDIA merchant right now,

**[58:24.539]** and you will be presenting at that level of pitch. So it's fine. So don't worry about it, just express what you made and what is it about and who is it served to and you pick it. And just one thing,

**[58:38.269]** make sure the product you build speaks. So there's nothing to worry about. Yeah, the part that is there is relevance. So it has to be relevant. If it speaks for the relevance, you are all good. And we do have a startup API program as well.

**[58:53.590]** So people who are interested in using the API after the hackathon as well, do sign up for the startup API program and we'll be happy to assist you on that. We will be sharing on how to submit and how to submit every track

**[59:08.230]** that you're working on soon enough so that you have a way of moving forward. So don't worry about it, but we do require a link, the live website link, why? Because the judges won't be opening

**[59:21.309]** the GitHub repositories that often. You can expect them to open it, you can expect not to open them. But what they will 100% open is your pitch, the live link, make sure it is live until the judging period has ended,

**[59:35.030]** which is 16th of September. Make sure you have it up until one or two more days because the judges will take their time to review it as well. So do keep in mind for all of these aspects. And we will be sharing more about how to submit,

**[59:47.780]** where to submit soon on Slack as well as email. Is it compulsory to add Fortiguard as a collaborator and public repos? Yes. In public, private, both repos, we need to see the integration of the temperature API

**[01:00:02.340]** and how you have done it. And it will be shared with the judges as well, so it will be there. Can I add you guys on the link? Sure, go ahead. No worries.

**[01:00:17.889]** Can I apply for the startup API program? Just give me one second, I'll give you the link right here. People who are wondering as well, I'll just add it to the link and you guys can see it as well.

**[01:00:34.159]** All right, for what? I think it's done. Thank you, everyone. And we'll close the session for now. If there are any questions from the previous section about the hackathon,

**[01:00:45.119]** or if there are any questions regarding the API itself or any technical questions, reach out to us on Slack or the emails that we have provided you in the previous meeting as well, and we'll be sharing more information soon. All right, have a nice day and good luck.

**[01:00:59.440]** Bye-bye. Bye.
