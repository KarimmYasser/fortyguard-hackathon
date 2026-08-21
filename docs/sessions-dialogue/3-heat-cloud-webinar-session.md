# Heat Intelligence Cloud: What You Can Build on the FortyGuard API - Full Transcript & Summary

**Recording URL:** [Zoho Webinar Recording](https://webinar.zoho.com/meeting/public/videoprv?recordingId=02adbe26d7441dfba535b4bf5b46ed300cef01518c64d1ea40a9fdd4902c6e66&x-meeting-org=935374719)

**Date:** August 19, 2026 | **Duration:** 37 minutes 58 seconds (2,194s) | **Language:** English

**Speaker:** FortyGuard Lead Solutions Architect

---

## Executive Summary & Key Takeaways

This deep-dive session focuses on the architecture of the **FortyGuard Heat Intelligence Cloud** and practical applications developers can build. The speaker contrasts conventional weather APIs (which only provide macro zip-code level data) with FortyGuard's parcel-level microclimate data engine.

The session showcases live product demonstrations across 6 major target industries, detailing which endpoints to query, how to parse environmental layers, and how to create commercial-grade climate resilience software.

### Key Highlights

1. **The 4 Data Layers:** Surface Temperature, Thermal Comfort Analysis (UTCI/Apparent Temp), Air Quality, and Land Cover Analysis.
2. **Granularity Advantage:** Moving from regional weather stations to street and building parcel level microclimate resolution.
3. **6 Target Industry Applications & Live Demos:**
 - **Real Estate & Property Tech:** Climate risk scoring and thermal comfort ratings for asset valuation.
 - **Insurance & Underwriting:** Dynamic heat stress risk indices and extreme weather claim modeling.
 - **Urban Planning & Municipalities:** Pinpointing Urban Heat Islands to optimize shade tree placement and cool pavements.
 - **Public Health & Outdoor Workers:** Real-time heat exhaustion warnings and hydration/rest shift scheduling.
 - **Logistics & Cold Chain:** Temperature-sensitive route planning and cargo spoilage prevention.
 - **Energy & Utilities:** Grid peak load forecasting driven by hyper-local AC demand spikes.
4. **Live Product Demos:** Full walkthrough of 6 production-grade web applications built with React/Next.js, Mapbox/Deck.gl, and the FortyGuard Temperature API.

---

## Subtitle & File Exports

- **SRT Subtitles:** [heat_cloud_subtitles.srt](file:///Users/karim/.gemini/antigravity/scratch/heat_cloud_subtitles.srt)
- **WebVTT Subtitles:** [heat_cloud_subtitles.vtt](file:///Users/karim/.gemini/antigravity/scratch/heat_cloud_subtitles.vtt)
- **Raw Text Transcript:** [heat_cloud_transcript.txt](file:///Users/karim/.gemini/antigravity/scratch/heat_cloud_transcript.txt)
- **Structured JSON:** [heat_cloud_transcript.json](file:///Users/karim/.gemini/antigravity/scratch/heat_cloud_transcript.json)

---

## Full Timestamped Transcript

**[00:00.000]** built around those endpoints. So I'll be focusing on those endpoints. I'll be focusing on the industries, and I'll be focusing on the live demo as well. So live demo will come at the end of the presentation, where I will go through each of the products that I've built using

**[00:27.940]** the API and I'll explain everything in detail to you guys.

**[00:36.299]** So the agenda, as I mentioned, I'll be going through the idea in one line. Then I'll be explaining the API, what it gives you, what intelligence you can extract, the most useful endpoints that are there. I'll be giving you guys exposure to six different industries,

**[00:56.520]** and I've built the products around those six different industries using the same Fortygards API. So that gives, shows you the variety and what you can build with those products or with those APIs. Then I'll explain, give you some ideas as well, which you can take further,

**[01:13.960]** and then there will be a live demo and some questions from you guys as well. So the Fortygards API is fundamentally different from the Weather Station APIs that you usually see online. They usually operate at a much higher level, usually at a zip code level, and mainly you cannot go granular with those APIs.

**[01:39.319]** Fortygard, entire intelligence revolves around giving you exact intelligence at that parcel level, be it the street, building, you will get exact spot intelligence for that particular point. So Fortygards data layer is spread across four different domains. So you get temperature, you get comfort analysis,

**[02:01.960]** you have air quality, and then you have land cover analysis as well. All of this comes down to a individual parcel point, which is at a street level. So that gives you a lot of control over granularity and helps you build amazing thermal maps as well,

**[02:18.979]** and helps point out the heat exposure in a better way as well. So that's particularly unique about Fortygards point. So I showed you four different layers are there, and there's a parcel level intelligence. So make sure that the products that you build revolves around this particular advantage that you have with Fortygards API.

**[02:40.780]** The building blocks of your products will mostly be revolving around these three major heat map and API endpoints. The first one is heat map. So it gives you a true predicted temperature over the tiles block by block, as I told you, and it is a much granular level as well. So you get 60, 80,

**[03:01.860]** 100 meter tiles as you would like for your particular use case. And then there is environmental parameters, which I think is the most useful endpoint right now after heat map, and Fortygards temperature data. So this gives you a lot more than just a single temperature number. So you have fields like you have wet build, you have humidity,

**[03:23.099]** and then there's air quality and solar radiance. So there's a lot of different domain. And for each domain, you have an endpoint, which gives you the particular intelligence for that. So you want to target the cold chain logistics, you have an endpoint, you have to target the outdoor worker heat stress,

**[03:44.019]** you have wet build for that. So all of these things are available at your fingertip, and you just have to call the endpoint, utilize that particular intelligence, and build to your products around that. The final thing is set lights.

**[03:57.099]** So set light is usually important because it gives you context about why a certain area is behaving in a certain way. So for example, if a certain area is hot, this endpoint gives you the context and gives you the credibility behind it. So there may be a build-up percentage there,

**[04:14.500]** there may be less greenery there. All of this can be achieved through set lights. So you can call this endpoint, you can get the set light percentages, land cover percentages for that area, and then you can find your basis around that.

**[04:26.980]** So temperature is hot because the build-up is hot, build-up is more, and if temperature is less, because the greenery is more. So you can find that correlation as well using these endpoints. So the six products that I was talking about, so these six products,

**[04:43.459]** each cater a different industry, cool scope. This is for real estate. So I mean, in real estate, whenever you are building your home or making an investment, you always care about the temperature and the climate there, right?

**[04:57.019]** So you can build your product around that, you can simulate cooling, you can quantify the ROI, you can diagnose the urban heat effect. Similarly for cool route, Coltrane Logistics, I'm sure most of you guys will be building products

**[05:13.620]** around this idea where the worker he starts also comes into account and you need the cooler route system developed so that you can plan those cargos and plan the heat explosion a better way. So you can build product around this,

**[05:31.060]** there's a wet build temperature available for you guys and you can combine it with different other factors like solar radiance and maybe air quality as well. You can include in this and this gives you a combined effect. Then there is thermal grid. So for data centers,

**[05:49.139]** you guys know that there's heat involved in those data centers. So to analyze those data centers, you can use our 40 guards temperature outdoor,

**[06:02.060]** simulate cooling levels, PUEs, carbon aware computing, scheduling. There's a variety of things that you can explore. So these are just few of the things mentioned here. So grid peak for electric demand, you have transmissions, you have grid stations

**[06:21.819]** and you know that there's a big demand over there for cooling for those feeder peaks. So you can use 40 guards data to forecast that temperature, make alert systems, make AI agents that alert the relevant authorities. So grid peak is another industry you can target.

**[06:41.379]** Then there is insurance industry. So for example, you might have heard about Los Angeles and how the fire there had like insurances running around and they wanted the system where they could like predict a certain climatic event or predict heat exposure there. So you can build a system around that,

**[07:03.939]** you can build your product around that. You can give a heat risk index with a lot of triggers. You can combine this data with a lot of different open source insurance data available to find your basis of the product. And then there's carbon lens, which is ESG.

**[07:21.819]** You can take into account heat and air quality. So you can correlate heat with air quality and build a basis on top of that for a particular city. I'll be showing these in the live demo as well. I've built each of this product myself. But for your understanding that there's a lot more potential

**[07:42.699]** than you think right now. And there's a lot of intelligence that can be extracted by combining 40 guards API with a lot of different open source available data.

**[07:56.699]** So mainly your process of building will be starting with the single place. So you'll pick the area of interest, whatever industry you pick and choose, starting point will be the area of interest. So you'll be picking that and building the heat map on top of it.

**[08:15.699]** That's when you get the temperature information from 40 guard. Then you will add the context to that particular thing or particular area of interest. And as I said, for context, you have rich sources of information. So you have environmental parameters. You have satellite to explain why it's hot and why it's cool

**[08:35.700]** as well, why it's good size, the relation. And then the final thing will be to build a product out of it. So either it will be a AI agent. It will be a route scoring model. It will be a schedule that someone can act on. So this will be the most critical part.

**[08:55.700]** So you have to think commercially when you are building this decision. What target segment you are catering, will this be helpful? And if yes, then in what way? So you have to think from a commercial perspective when you come to this stage of the decision making.

**[09:18.700]** Okay. So live demo. Before I go into the live demo and show you guys all of these products, I want to share something with you. Whenever you build something, whenever you build a product in a hackathon, I've seen a lot of people focus a lot of energy and their time

**[09:45.700]** in building a scalable solution. So they think a lot about engineering and spend a lot of time perfecting your solution, which is good in a way. But with this particular hackathon, the value is on the commercial objective. So if you do great engineering, but your product doesn't answer a commercial question, it doesn't show value clearly.

**[10:11.700]** And we as judges or mentors don't see the value of your product, then it will be of less use. So you have to think that engineering is good. It is always useful, but the commercial angle will always be important. And as I said, I only showed you six different industries, but I showed you the potential of the endpoints itself

**[10:35.700]** by combining these endpoints with different other open source status that is available right now. You can target almost any industry right now. That's the quality of the API that we are giving you right now, that this information can be utilized with almost any other open source data that is available and you can build great products out of it.

**[10:58.700]** So I'll just be sharing now my dashboard to show you guys that. So this is the product itself. Okay. So this is Heat Intelligence Cloud. As I mentioned, there are six products, there are six categories that have catered. Let me start with the CoolScope.

**[11:30.700]** I think this is the most useful in terms of giving context to what we are trying to convey here. CoolScope is basically to understand the value of your particular real estate property or your home, maybe, urban center, anything you can pick as an area of interest. So you can analyze the temperature through Fodegaard's temperature, obviously, that is clear. And then to form the basing of your other things, like cooling potential,

**[12:05.700]** what will be the temperature after that particular intervention, like introducing trees, introducing shade, all of those things will be formed on the basis of Fodegaard's satellite data. You'll be using this segmentation. As you can see, the temperature here is 40.7 degrees Celsius, that is coming out to be. And why it is hot, you can see that the building percentage is almost 72.7 percent.

**[12:35.700]** And the rest of the thing is roads, sidewalks, and almost no greenery here. So this makes sense, right? This makes sense to introduce cooling interventions here. For example, if there's an AI engine, it will need this context to inform a particular stakeholder that, okay, this is hot, but this is why it is hot. And this is what we are doing next to optimize this and reduce the cooling potential.

**[13:01.700]** And then you can actually simulate. So you can simulate adding tree canopy, you can simulate adding reflectance. You can see how the percentage of each intervention changes the overall projected cooling and then the new temperature as well. And you can also see where the most efficient intervention is coming from. So obviously cool roofs and then there's tree canopy.

**[13:30.700]** So you can actually project this up. You can next have some other parameters to this. For example, energy savings for building HVAC systems. You can project heat days, extreme heat days that are there. You can, for example, take into historical data and then project heat days. Similarly, for property value, you can project your uplifts and your comfort arts as well within the day.

**[14:01.700]** And for example, I said why this will matter. So commercially cities, developers, and a lot of other stakeholders that are interested in real estate property value, you can actually go and sell this product to them. So this is itself, you can say, a SaaS product that you can build on top of Fortygards API and then you can go ahead and sell this. So this is just one example. And I'll show you some other examples as well.

**[14:31.700]** So the next famous, I'm sure many of you are targeting puller routes. I expect that a lot of you guys will build that. So I'll just show you a very brief demo of how it might look. So here what I've done is that there's a delivery stop mention in the particular area. So there are four different delivery routes, delivery spots from your location. And then I'm routing them based on the cooler temperature.

**[15:09.700]** So you can see the paths that come up. You can see the overall distance exposure as well. You can define the exposure score based on your particular, either scientific standard or your particular standard. I think wetbilt, as I mentioned, is the most important one here because you'll be using that to measure the outdoor worker stress as well. So wetbilt is the go-to for the guys who are building this puller route model. You'll be using that a lot.

**[15:44.700]** So you can then predict the comfort hours as well. You can predict the windows as well where you think it will be most suitable for the workers to deliver, for the logistics to move, and for the cargo protection as well. You can pick out those windows. And then you can, based on this analysis, you can then recommend them certain things as well. So this is again one of the additions. So this is the next step, as I told you.

**[16:10.700]** Once you have the data and you have analyzed something, then there should be a next step to it as well. Either a decision by an agent or by a stakeholder, and you should see clearly the value in it as well and from where it is coming as well. So this is just one of the examples. You can pick the start time delivery date and the types of cargoes as well. So if you want to go one step ahead, you can pick different types and based on those, you can have specific algorithms. So for example, for frozen items, there's a different level of threshold that needs to be maintained for it to be particularly cool and then move in different areas.

**[16:49.700]** Similarly, for farmers, for vaccines, for fresh produce, there's a different category for each and for each category, you have a different threshold level as well, based on which you can customize this. Then there is grid peak. So peak load. Here I said the peak demand forecasting can come through combining the solar data, the heat data with different sources of information. So you can actually use open source information, grid pricing information as well. There's something called eGrid as well.

**[17:28.700]** So you can actually combine this. So now this is an example of how combining 40 guards information with a third party information can actually be useful for you guys. So you can develop this net demand forecasting system. So it can be a model itself as well. So you can combine these features with 40 guard features and build a machine learning model as well. If you guys are choosing that track that that will particularly be then then combining data and then training and then you have the output as well.

**[18:00.700]** And if you feel like you want to build a fast product just by combining data directly into the dashboard and feeding it, that is also possible. So you can predict transformer loads demand response. Again, you can pick the arts for each art. You can pick the parent temperatures, regional temperatures, demand forecasting as well. And the transformer percentages, how much the transformer will be utilized. So you can see in the cards, the utilization is more because because of the temperature.

**[18:36.700]** So this information is itself very useful. And now you have this information again, the same concept repeats. You can use this context for your agents for your systems to feed them and then they can make a decision on top of this. So again, this is really important. So you can build charts as well. You can build drafts as well. There's a lot of data and information available.

**[19:00.700]** The presenting of your presentation of your solution is actually the critical part. So if you have all the information, but you are not able to present it in a way where a decision maker can take a decision confidently, then obviously it's of no use. So you have to think about ways why through which it can be useful for the final decision maker as well. Then I think there is thermal grid as well. I think this is actually the same concept. It is just for the data centers.

**[19:38.700]** So you can predict heat for data centers as well. And you can basically do a lot of on demand forecasting as well for them, catering different use cases. So for data centers, you know that they release a lot of heat and that is one of the concerns. So you can build alert systems around that. And if in a particular neighborhood, you see that in particular time windows, the temperature is increasing. There's a lot of heat in the neighborhood and it is affecting the health facilities there.

**[20:12.700]** So you can link it back to health data. So again, this is again one of the examples where combining for regards temperature with different other sources of information can give you really insightful information. So that is again one of the examples. Thermal score for insurances. I think this is pretty obvious from the example that I gave earlier about Los Angeles fire incident that happened. And I mean, there were a lot of damages and insurances actually care a lot about heat predictions and forecasting and seeing the climate of a certain area in future as well.

**[20:58.700]** So you can build a forecast prediction system for them as well for each area. You can analyze the historical data and then you can combine it with the pricing information, the open source available information from these insurances as well. And they pass records as well and using that information and combining it with 40 guards historical analysis and forecasting capability. You can actually build really solid products out of it and you can actually show these insurances that how you can actually save costs or build good insurance plans for different clients. So again, this is one of the use case. Then there is carbon lens, the final one for the day.

**[21:48.700]** This is actually for air quality forecasting. So in areas where air quality is bad, it affects health, it affects businesses, it affects routing, it affects traffic. So it affects four to five to six different things, if you imagine, just a single AQI value. So if you think from that point of view, by just using AQI, you can build products in six different industries, for example. So there are six different use cases for you and six different ideas. So just a single parameter is giving you so much potential.

**[22:30.700]** So that's what I want to stress upon as well, that you have a lot on your plate in terms of like information and intelligence and how you use it is upon you. So you can make good use of it as well by combining it or thinking about creative ways, or you can just directly use that information and state plane temperatures as well, plane AQI values as well, which gives no real information and no real value as well. So that again depends on you and how you want to utilize that. So there's CO2, there's AQI, there's solar radiance, there's wet build. All of these informations are really good in terms of helping you guys.

**[23:17.700]** And you can do the R by R analysis as well. And this gives you some insight about which R's are most vulnerable, where the intervention should come, in which R's the business should operate. So all of these things are really useful to commercial clients and stakeholders and they will really value this insights and these informations. So I think that is it from my side in terms of like explaining you guys the overall product use case directions. And if you guys have something to ask, I'm open to answering your questions. Thank you so much, Ashan, for that in depth session. People have been asking a lot of questions about the projects that you have built as well.

**[24:16.700]** And they are now seeing how API can be used and taken into so many different directions, by the way. If you want, you can stop sharing because you can just focus on giving all attention to the Q&A. People were asking, people were very interested in the cool routing and cool scope, by the way. Can you talk more about how you thought about the project itself? Okay, so cool routing is interesting, definitely. I am also predicting that most of you guys are building it.

**[24:49.700]** Just because it's right now really important, if you see in US as well, in summer, the heat waves are there and businesses are being affected by this heat. So you have to build solutions which can direct people towards cooler routes and delivery routes. Mainly the important thing with cool routes will be to utilize the build temperature because it's mostly for outdoor work at stress. And think about windows where the temperature is less or maybe ideal for deliveries. Pick those windows and then the next thing would be to combine this bodyguards data at each point or parcel level with maybe OpenStreetMap. This is an open source library you can use to map or route those things.

**[25:43.700]** You can pick the example routes to show your use case and show how it is choosing a cooler efficient route instead of a heat worker stress route. This way you can build your algorithms around it, pick different kind of shortest route, cooler route algorithms. I'm sure the technical people know about all the cooling route algorithms, maybe the shortest route algorithms. The cooling route is just adapting those algorithms to a better temperature. So that comes in as an additional feature or a factor in and you can modify that particular algorithm to cater that temperature value as well. So that's about it. And then your creativity, it is upon you.

**[26:27.700]** As I said, you can build recommendation systems on top of it. You can combine more useful information. Different kinds of businesses need different kind of information so you can cater to each business in this specific cooling route project as well. And then you can build a lot of different solutions for it. And as far as I think CoolScope, I missed it. So CoolScope is for real estate mainly.

**[26:56.700]** I think that's where the most commercial value is. And I said three important endpoints. So you'll get temperature from heat map endpoint. Then you have the environmental endpoint, which is the best right now in terms of giving something more than temperature. Use that. And the third thing would be to build your solution or use the land cover as a basis or a context engine.

**[27:22.700]** So you can explain why this particular area is hot or why this particular area is cool. Yep. Do we have to apply all six ideas that you mentioned as they are or we can create something of our own related to this? This is as Ashon mentioned, Ashon you can pitch in as well. As he mentioned, these are all like starters in terms of ideas. These are like just brainstormers that he built in order to give you guys an idea, a path to if one of you are interested in any of the tracks which are there.

**[27:55.700]** As he was explaining about CoolScope that is related to the track which relates to real estate. So people who are interested in tracks, he has given you like six different directions to start from. And these are all starting ideas. If you have some ideas which are similar to these ideas as well, you can build on top of this as well. This is a visual representation of what you can do with the temperature API to show you the value and how you can start thinking about which track to choose and how to deliver it as well. Great.

**[28:33.700]** One question regarding CoolScope.com, Ashon, is it also using the ML for predicting the future temperature? So you guys are aware about that 40 guard API can forecast up to 12 parts. So I'm not really using a model right now to forecast. You can use 40 guards API and it gives you up to 12 parts of temperature forecasting. So I think there is one interesting question about combining it with other sources. So yeah, you are completely allowed to do that as long as you use 40 guards API.

**[29:14.700]** And if you want to combine it with some other source, you are more than welcome. There's one more question. That's a long one. So what if our idea requires API start on usually obtainable in designing an MVP, the user provides it themselves when using our program. Things like automation API is for smart devices or like automation API itself or even the agent for like API tokens. When do we declare our project a complete MVP?

**[29:55.700]** So if I understand this question correctly, obviously, we are not expecting you guys to build MVPs in the sense that they are not really useful and are not ready in the sense to go out in public. Obviously scaling is something that we don't expect at this point to be like handling thousands or multiple multi-thousand users. That's something that can be engineered or done later, but we expect a real working product for you from you guys. And if there's some API or some limitation from a third party or you think that this API cannot be achieved within like your either through fee, free means or through a budget, then you can probably skip that and think of alternatives or things where you can prove your value using openly available sources. And you can actually rely on those sources more than. Since yesterday's session that happened with Fawad, people are confused regarding did you build this on a VS code or a Jupyter notebook?

**[31:11.700]** So it doesn't really matter, by the way, but it's not a Jupyter notebook. Obviously Jupyter notebook is for testing RND. If you want to test before you build something, that's the way to do. And if you want to build a proper system, so it's a product, it's a complete software product. So you have to build it. ID is something that you can choose. So VS code is just my preference. You can choose other IDs and build your software here. Deploy them. That's the most important thing. I'm sure you guys are aware that deploying will be important. One question is that do we how often is the API data updated? So API is you can go back to like 2021 as like the historical and then for future, it's like latest up to date. So for example, current in future like 12 hours, you can forecast from right now in this moment.

**[32:15.700]** So it's like up to date till this point. And every hour as well, the forecasted data keeps on getting added in the catalog as well. So you will get your forecasted data as well. Can we combine different ideas from your presentation, Ashok? So by this you mean like combining different applications that you just built, people are asking regarding it. Yeah, I'm sure. I mean, if the track that you have picked, it falls under that it's completely fine and you can mix and play around. I see a lot of questions regarding submission. Guys, the submission criteria and everything will be shared with you guys soon. Just hang in tight and continue building what you're building in your projects.

**[33:21.700]** And within a day or two, you will be getting all the details on Slack as well as email. So let's not just spam the question answers and keep it relevant to the session itself. So I think this is important. Where should we deploy it? You can build it in VS Code, but where should we deploy it? Okay, so for deployment, you have a lot of free options available. You can use render, deploy, there's Versal. If you have like a static kind of thing, then GitHub Pages is also available. We'll suggest that you guys use open source resources. If you don't have that project for you guys at this point, but make sure that you keep hitting those endpoints because free versions usually die down as well. For us as a team to evaluate your products, we'll need to see those working live as well. So just keep that in mind.

**[34:24.699]** We use Cloud Code and spec kit. Any AI and LLM usage? I think you are allowed. Just declare it. Mention it that you use this particular AI agent and that's completely normal and accepted. Yeah, to just build on top of that, this is an AI hackathon as well. So we do encourage it. There is no penalty for that. We won't be penalizing you for using any AI, by the way. So you're free to use it. Is there any sustainability goal for project? So that is really good if you pick it. SDG goals are, I think, really important as well. And if you design your solutions around that, then obviously it will be good as well. So if you want to pick any specific goal, you're up on it and you can pick it.

**[35:24.699]** One thing which relates to your background, does the temperature API provide historical data at a sufficiently fine geographic and time resolution for building an ML model? And what would be the recommendation, a recommended approach for handling missing or inconsistent temperature data? So I mean, for historical, I said we have multi-year information available. And if you even train on a single year of information, I think it's enough to build a really good model. But you have multi years. So if you want to go one step ahead and build like something really good, then you can use train it multi years. And the strategy to handle missing data is really simple. If you find some inconsistencies, you can rely on interpolation approaches. You can think about different standards. That's something really common in ML. I will not go into the specific approaches, but those are completely normal and are accepted as well. So you can interpolate.

**[36:29.699]** All right. So I think that's about it for all the questions that we could see and we have answered as well.
