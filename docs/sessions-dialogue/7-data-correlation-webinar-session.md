# From Heat Data to Real Signal: Data Correlation Analysis — Full Transcript & Summary

**Recording URL:** [Zoho Webinar Recording](https://webinar.zoho.com/meeting/videoprv?recordingId=c37ca458b4d665ffb2849fe0059aeac421993fb9817994c7ebd743072ed325cd&x-meeting-org=935374719)

**Language:** English | **Engine:** Whisper AI (Apple Silicon Metal GPU)

---

## Executive Summary & Key Highlights

This technical session led by Mudethir and Aamir demonstrates how to extract real analytical signals from FortyGuard's hyperlocal temperature data:
- **Hyperlocal Temperature Correlation:** How to frame high-value analytical questions and correlate microclimate data with secondary business/social datasets.
- **Heat Equity Analysis:** Quantifying disparate heat impact across urban demographics and neighborhood vulnerability indices.
- **Productivity & Health Modeling:** Modeling worker thermal comfort, labor productivity drop-offs, and health risk thresholds.
- **Statistical Significance & Verification:** Distinguishing true environmental causation from random geospatial noise using spatial regression and statistical testing.

---

## Subtitle & Document Exports

- **SRT Subtitles:** [`data_correlation_subtitles.srt`](file:///Users/karim/.gemini/antigravity/scratch/data_correlation_subtitles.srt)
- **WebVTT Subtitles:** [`data_correlation_subtitles.vtt`](file:///Users/karim/.gemini/antigravity/scratch/data_correlation_subtitles.vtt)
- **Plain Text Transcript:** [`data_correlation_transcript.txt`](file:///Users/karim/.gemini/antigravity/scratch/data_correlation_transcript.txt)
- **JSON Data:** [`data_correlation_transcript.json`](file:///Users/karim/.gemini/antigravity/scratch/data_correlation_transcript.json)

---

## Complete Timestamped Transcript

**[00:00.000]** Hello everyone. I think people are still joining. The session is already recorded. So people who will be watching it after this, that's fine as well because we have seen people watching it after the live session as well. So that is not an issue.

**[00:40.399]** We can get started. So hello everyone. I'm very pleased to introduce our next session, which takes us behind the technology that powers this entire hackathon. Throughout this event, you all have been building on 40 guard temperature API. You've been querying it, pulling insights from it and turning it into your own solutions.

**[01:07.000]** But today you have a rare opportunity to hear directly from two people who are responsible for building the engine behind it. The system that makes all of that possible in the first place. First I'd like to introduce Mudhasur, our machine learning lead who works at the intersection of large scale spatial data and applied research, which is exactly where the hardest and the most interesting problems in temperature intelligence live.

**[01:35.640]** He leads our deep learning work, our spatial temporal modeling and the large scale data work around it as well as well as the GPU infrastructure that supports it all. A major part of his work involves the designing the pipelines that combine multiple data sources into a single unified source of temperature intelligence. And then building the training and inference systems that allow our models to run reliably at scale.

**[02:05.359]** He leads the development of our large temperature models along with the intelligence engine built on top of them. The layer that turns raw model output into meaningful analytics, simulation and decision making tools. Joining him is Amir, a software engineer on the team whose work ensures that all of this intelligence actually operates reliably in the real world.

**[02:29.680]** Amir works across data engineering, cloud architecture and applied machine learning. He architects the ingestion and transformation of machine learning algorithms, cloud architecture and the cloud system that serve temperature intelligence across millions of spatial grid cells. Infrastructure that has also performed consistently day in and day out against complex real world data.

**[02:58.840]** He is also behind the system that powers some of Fortigaert's most advanced capabilities, including its data center ambient thermal screening and temperature aware routing. Together, Modiser and Amir here, they will take us some of the most complex data available and transform it into clean reliable signal that you all have been building for the past week or so. In this session, they'll open up that process, show you how it works beneath the surface

**[03:27.439]** and share how you can apply that same thinking to your own projects. Modiser and Amir, the floor is yours. Thank you so much for this introduction. Thank you very much, Snehal for the warm introduction. I couldn't have put words better myself. Let me start off the session and I welcome you all.

**[04:02.719]** Let me share my screen and begin.

**[04:09.000]** So, I will be going through how heat data can be transformed into real signals and understanding how different fields like temperature can be turned into analysis that actually holds up. So, Modiser and myself, we will be looking at four different aspects on how to do that. First, there's space and time, where spatial and temporal data are present and what resolution means and how the main temperature data in different sources differ.

**[05:03.560]** Then, how we can couple them and how we bring together different sources alongside temperature without breaking the analysis and make changes and deliver the third step would be to deliver the analytics using that. Now, how do we derive analytics from it? How do we make other possibilities happen? We will be looking at that.

**[05:26.480]** And finally, the mindset behind it, the planning, the execution and the traps usually which come into play when we are doing this process.

**[05:38.839]** So, first section, space, time and resolution. What do we understand from this? Every temperature value we use carries a where and when and almost every time this is the mistake which is made early on in the project which leads to the analysis not coming out as we expected to be. So, what is spatial now?

**[06:02.600]** A particular value, it can be anywhere on the earth, a point, a street segment, a grid cell, a neighborhood boundary and when covers the temporal aspect of it, a moment or a window in time and hour, a day or a month, decade and interval, it could be as well. Now, the what aspect refers to as the value of the time and the time. The value of the measurement itself, the first two spatial and temporal act as the axis or the dimensions of the data, whereas the value defines what that value, where the value lies

**[06:41.240]** in that dimension and what it represents. Now, if two datasets do not agree on where, when and what was measured, then any correlation you compute between them will be an accident or will be a mistaken value. Now, for how the location and time are actually stored, the spatial data covered is in two different aspects, two different formats which one is a vector and one is raster. So, vector data usually represents points, lines, polygons and a weather station, for example,

**[07:25.160]** is a point data as well. Now, it could be a road, a city boundary, all of this is vector data. Now, in terms of the format, usually it is represented as a geoshawn, geoshawn, then there is a shape file or a geo package. And in terms of raster, it is a grid of cells, each holding one value and every satellite image you see is represented as a raster.

**[07:56.439]** It can be represented as a geotiff, netcdf, czar, etc. And now, when it comes to temporal data, what do we have? There are two ways to describe time. One can be an instant, a moment in time, let's say, for example, 14 or 4 p.m., let's say, or 2 p.m. on a particular date. That is one particular time spot.

**[08:25.159]** Now, it could also be an interval, a window, let's say, July, that's entire month representation, or 10 years. And in these scenarios, you need to ask an important question. Is it a mean? Is it a max? Or is it a minimum of that window?

**[08:43.720]** Now, what to watch out for in this case is that this time can be represented in another dimension where it represents, based on the spatial area, different time zones. It could be UTC, it could be local, generally, for in these scenarios, whether data usually uses UTC time zone and how it is labeled. That is also very important. For example, it says 14 ohm, and it means that either it could be starting or ending at that time.

**[09:18.279]** So does the temperature value lie within that hour or after that hour? So these are some things we need to pay attention to, and as well as gaps within these missing hours. Now, in terms of resolution and where it comes into play, there are two types of resolutions based on the spatial and temporal data. We have spatial resolution and temporal resolution. So now spatial resolution defines how fine in space value is represented.

**[09:53.879]** In terms of the size of a cell on the ground, let's say, for example, a 25-kilometer cell gives one number for an entire city, whereas a 20-meter cell gives a different number for a park or a smaller area street, let's say. Now, when it comes to temporal resolution, it's how often new value arrives. It can arrive early, daily, monthly, and so on. Now, these three words specifically, when it comes to spatial resolution, temporal resolution,

**[10:27.800]** get mixed up is coverage, the resolution, and accuracy. What are the differences between them? Whereas one is coverage is where the data exists, and then inside it, we see what type of resolution it is. So first comes the coverage, where it is lying. Now, then how fine of a detail is inside that coverage? That's resolution.

**[10:49.480]** And in terms of accuracy, that value, how close is it to the real value? Or sometimes even higher resolution value can be wrong if it's not accurately measured.

**[11:05.560]** Now, this is an example over here shown at different resolutions, how data and its patterns we observe from it can differ. So you can see over here four different resolutions. First, we have the 25 kilometer, which comes from a global climate model. And it represents one value for the whole city. Now, it comes to the analysis models, similar to error five.

**[11:32.039]** And we can observe a few more patterns in it, but it's still very low in terms of resolution. So it can compare, we can use to compare the city center versus the outskirts roughly. Now it comes to regional model, it can dive more into the different districts, neighborhoods. And now the final one is street block scale, where you can see small aspects and small patterns within the heat map, as you can observe over here at a street level scale. You can observe the water, how the parks are, individual blocks within the district itself,

**[12:13.720]** and see how they differ. So this resolution is, you can see how it difference and how each of the values represented over here have different meaning and how we lose the detail as we go in lower resolutions and how the details increase as we go higher. Now, one common mistake people make is not looking at the value itself, which we are seeing. Now, if we consider temperature, there are different types of temperature, there is air

**[12:47.879]** temperature, surface temperature. So we should not mistake between them. These two are distinct values. So one of them, let's say for example, we have surface temperature. It can come from satellite and it represents how hot the surface or the ground is. Now air temperature is how hot the air is above that ground.

**[13:14.279]** These two are distinct and they represent different values. They, you cannot compare them directly, they represent different aspects of temperature and give different analytics into it. Now, where the temperature data comes from at a high level, these are the four families of sources and how they are represented, let me show you. So first one is weather station, a single truth point, but it's very sparse.

**[13:45.879]** Only a few weather stations here and there, you can find them at the airports, ports, etc. And it's very scarce. Now, satellite, which is LST, land surface temperature, you can get, and it's a wide coverage, it is very finely detailed, however, it's not air temperature. So it represents not how a person feels, but how the temperature on the ground is. Now, re-analysis models, physical models, the RFI, their strength, they have a long coverage,

**[14:17.560]** they have a larger period of temporal resolution, but they lack in terms of spatial resolution. So they have core cells, if they can cover a whole city, maybe maximum district as well, but they cannot go street level. This is where the Fordigar models comes in. It's a learned model where different data sources have been compiled to construct and predict air temperature at two meters level.

**[14:42.759]** The strength of it is at street level and it is also represented early at two meters. So what the user actually feels. Now, let me go next. So over here, you can see the same different sources and you can see how they, especially one point and temporarily as well early. And you can see certain passes in terms of temporal resolution need to pay attention.

**[15:11.639]** Is that satellite sources have where they cover and they rotate and they take certain passes per day or it can be after one week or after two weeks. And it also depends upon the cloud cover. So if the cloud is covering, the satellite data might not be collected. See, there are some things we need to consider. So this is the highlights of them.

**[15:35.080]** Go next. Now, how was the data for Fordigar's models collected and how they were trained at a high level? You can see that there were multiple data sources used, collected. One is ground truth values at certain points at a very high resolution. This is a proprietary data. It is not available everywhere, which we make use of to give us the finer detail you see in our predictions of our models.

**[16:05.799]** Then satellite images also we use that we use reanalysis models as well. We use geotraffricant urban forms and atmospheric and environmental as well. And all of this is fed into and used to create our large temperature models, which is our family of models. It is a different deep learning models trained specifically to predict the air temperature at two meters level at a street and block scale hour by hour.

**[16:36.439]** Now, section two, we understood how the data is, what type of parameters and factors we need to consider. And now we will see how to take that data and couple it with another data source to derive analytics from it. So temperature on its own only describes the weather, but to make it to take it to the next stage, we need to connect it to other data sources, to people, to assets, to different domains. So the coupling.

**[17:08.759]** Now, this is an example where if you see, if you're measuring a temperature at a particular point, let's say we say that the east district in an area has reached 43 degrees Celsius on 14 July. This is a fact. We cannot derive a decision from it. We cannot, how this will affect the area, what was previously there. This does not tell us anything except that this is the fact.

**[17:35.559]** Now, how do you convert this into a finding? Let's look at this example. Now, you can see the east district spends three times more hours above 40 degrees Celsius than the west and has a quarter of the tree canopy. Now, over here, we are adding another factor, like say tree canopy, and comparing it to another area to extract more out of it.

**[18:00.359]** So this is a finding. We understand more of it. There is, there can be decisions made from it and these numbers can be defended. So this is what we expect from you as well when you are deriving insights or based on your domain and presenting them. So these are the six families of data.

**[18:20.680]** There are more, but these are the high level, what you can couple with. So there is geographic and urban which covers roads, land, use, tree canopy, and then there is atmospheric, where is humidity, wind, solar, air quality, then there's environmental, vegetation, health, human and socio-economic, operational, energy load, and then there is climate baselines. So these are all the different and where they, it's also mentioned where they're

**[18:49.319]** being collected from, where you can gather them from. So yeah. Now, what that looks like when you're actually building it. So when we use these datasets, we check how the shape is, what they are actually giving us, what type of parameters, what type of values they're giving us. So first thing we need to decide when selecting any source is what variables

**[19:17.559]** we mean to collect from it. What is important to us? Air, it could be surface, dew point, fields like index, etc. Now, what geometry is on it? Like I explained, what type of specialties is it a raster vector? It is it giving a polygon?

**[19:33.240]** And then comes the time aspect of it, that how often is it collected in terms of temporal resolution? And we see, let's say for example, I said it collects every 16 days, or let's say for example, corporate magazine, which is the elevation data. It does not have a temporal axis because it is static and elevation does not change. So these are certain examples of how you can collect and what three factors

**[19:59.880]** you need to consider while choosing a source. Now, two datasets, like I mentioned previously as well, you need to consider the different geometries they come in. And like for example, the first dataset you are using is our temperature data source. And it is at two meters grid level. 20 meters, sorry, the grid level.

**[20:21.000]** And the other is collected. It's irregular. It is at a higher, lower resolution. Or it is collected at a different time period. So different cadences as well. Let's say ours is hourly and then the energy load you're getting from,

**[20:38.279]** let's say from a utility or a gate facility is every 15 minutes. So how would you couple it? And the meaning. Now, when it considers meaning, what do we understand from it? Is what is the metric you collected? If you collect the temperature, what was it in Kelvin?

**[20:54.360]** What is in Fahrenheit? Was it in Celsius? So these are all the important factors we need to consider. And I'll be going through them one by one. Now, when it comes to the spatial data, and you see that one data source is collected at a different resolution

**[21:11.079]** and another is collected different, what do you do then? How do you compare them or couple them together? Now to compare or couple them together, they need to be at both of them at the same level. So either you do upscaling, which is basically simply saying, going from a finite resolution, let's say we have over here an example,

**[21:32.759]** that we have these nine cells and we are taking them, dividing them into smaller cells. Okay. So we go into more, basically taking the small cells into a big one. So you are removing the detail from it. Now, when it comes to downscaling,

**[21:52.759]** you're taking one big cell and dividing it into smaller pieces. This is less risky, but you need to be careful doing it because the values as you divide them might not represent the same thing. Now, when it comes to interpolation, it's basically filling in the gaps, which come when certain sources based on their coverage cannot cover. So some sources might only cover, let's say for example, the weather station,

**[22:17.639]** it's only in particular points, in particular area. So how do you cover the area around it, which is missing? You don't have data for it. That's where you do look at interpolation. Now, things to keep in mind is like I mentioned, cadence, cadence, match the slower one.

**[22:35.800]** You see if you're collecting something daily or if you're collecting something early, then you're looking...
