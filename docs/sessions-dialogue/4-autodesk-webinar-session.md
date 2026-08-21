# Breaking Silos with Autodesk: Bringing Context from Data to Design - Full Transcript & Summary

**Recording URL:** [Zoho Webinar Recording](https://webinar.zoho.com/meeting/public/videoprv?recordingId=a1a05b1bf15cdc9b02dfc2f9b9602e807bdfc239b371138c5a356c0b5136c0ba&x-meeting-org=935374719)

**Date:** August 19, 2026 | **Duration:** 1 hour 11 seconds (3,612s) | **Language:** English

**Speakers:**
- **Jay** - FortyGuard Host & Community Lead
- **Jordana Rosa** - Senior Technical Specialist at Autodesk (AEC / Sustainability / 4x Hackathon Winner)

---

## Executive Summary & Key Takeaways

In this mentorship session, **Jordana Rosa** (Senior Technical Specialist at Autodesk) discusses bridging the gap between raw geospatial/environmental data and architectural site design. She explores how integrating FortyGuard's microclimate data into Autodesk AEC workflows (Autodesk Forma, Revit, Civil 3D) allows architects and civil engineers to perform early-stage thermal performance evaluations before construction.

As a 4-time hackathon winner, Jordana also shares actionable frameworks on how to build winning hackathon prototypes, adopt a builder's mindset, cultivate team communication, and present solutions with clear industrial impact.

### Key Highlights

1. **Autodesk & FortyGuard Integration:** Bringing high-resolution microclimate temperature into AEC early-stage design tools (e.g. Autodesk Forma) to mitigate Urban Heat Islands (UHI).
2. **Early Thermal Evaluation:** Moving thermal modeling from post-design compliance checks into early generative site layout phases.
3. **Hackathon Winning Strategy:** Framing a real industrial problem, validating workflows, prioritizing team trust/synergy, rapid prototyping, and delivering a crisp value proposition.
4. **Sustainable Built Environment:** Balancing solar radiation, building envelope materials, shading, wind airflow, and thermal comfort indices.

---

## Subtitle & File Exports

- **SRT Subtitles:** [autodesk_subtitles.srt](file:///Users/karim/.gemini/antigravity/scratch/autodesk_subtitles.srt)
- **WebVTT Subtitles:** [autodesk_subtitles.vtt](file:///Users/karim/.gemini/antigravity/scratch/autodesk_subtitles.vtt)
- **Raw Text Transcript:** [autodesk_transcript.txt](file:///Users/karim/.gemini/antigravity/scratch/autodesk_transcript.txt)
- **Structured JSON:** [autodesk_transcript.json](file:///Users/karim/.gemini/antigravity/scratch/autodesk_transcript.json)

---

## Full Timestamped Transcript

**[00:30.000]** All right, we're waiting for Jordana to join us and then I'll start by introducing her.

**[03:19.000]** Hey, Jordana, how are you? Hi, doing great. What about you? I'm very good. Thank you so much for joining us today. I'm very excited for this session. And I'm excited specifically because Autodesk speaks to a lot of real applications. And I've reading your biography. I've learned that you've done a lot of acutons before and you are a winner yourself. So you understand a lot on the about the mindset of people who are joining.

**[03:54.000]** I'm also more excited because for regards just recently joined the Autodesk developer network. And it's it's very big. I think we're very excited about exploring how we could bring high resolution temperature and intelligence into architecture. Engineering and infrastructure workflows. And obviously our goal there will be to help teams evaluate thermal performance earlier. So when it comes to design, we can make a better decision. So everyone I'm really excited here to be presenting Jordana Rosa. She is a senior technical specialist for Autodesk for one. She's focused a lot on emerging technologies for the built environment.

**[04:40.000]** And what makes her unique is that she's a Brazilian civil engineer and she's got a master's degree in global management. So she has worked across architecture, engineering and digital practices. And she helped a lot of teams when it comes to how to adopt automation, then AI and sustainability focused workflows. Before Autodesk though, she held digital practices, practice roles in different companies such as WSP and Brickens and Well to very big companies where she let technology adoption and help scale Autodesk for more former site design across design teams. Now, again, why I think this mentorship session is very special is because Jordana is a four time design competition and hackathon winner.

**[05:43.000]** Which means she will bring you the builders mindset as she continues to provide her mentorship to the hackathon during this session. And I highly recommend us to just that we take advantage of their experience building and designing and winning hackathons before we have a winner here. She will help you understand how to start with a real industrial problem, how to prototype it fast, how to validate the workflow and how to use AI and automation where they create measurable value. And just before she starts, and I'll give you the platform now, Jordana. Jordana is not only going to tell you how to do well and your submission and your build solution and all of that, but she's going to inspire you and give you a lot of information. So whether it gives you immediate relevance to the solution you're building or not, I highly recommend that you take a lot of notes.

**[06:48.000]** We will obviously provide the recording and make sure that you give all your attention and time to this session because it's going to be really insightful. Jordana, floor is yours. Thank you, Jay. I'm going to invite you to my future presentation. She introduced me. It was a great job. Thank you so much. I feel important. Well, welcome everyone. And thank you for joining. A quick note before we start. Let me share my screen.

**[07:17.000]** Please let me know if you can see my screen and fits well framed. Perfect. Right. You're muted because this is a big audience. But if you want to interact with us, please use the Q&A chat. I will not be answering the questions myself, but we have people in the support and this webinar is being recorded so you can check it later. The introduction was great. So just go quickly here. If you want to connect on LinkedIn, this is the QR code and my background is all in AC. When you see me saying AC, it means architecture, engineering, construction, and sometimes you're going to see ACO, which means architecture, engineering, construction, and operations.

**[08:17.000]** So AC and ACO industries. I received some messages on LinkedIn. I'm sorry if I haven't replied everybody, but some people was asking me for advice for their first hackathon. So I wanted to share what helped me to win four times, but I also lost a few times. But all of these experiences were super important for my career and for myself learning. And I hope you take this from this hackathon. You can get to experience this moment. My first advice is remember that success is a team sport. A hackathon is not only about individual talent. You can have, for example, Neymar, Pelle, and Ronaldo, but if they don't play together as a strong team, they will not achieve their goals. This is a short.

**[09:27.000]** The stress is very high and the problems will happen. The project succeeds when the team succeeds. So you need each one of the members in your team to build trust, communication, and play as a team. And the hackathons that I fell were because we didn't get the team to work together. So it's extremely important. My second advice is about leadership. Just like in soccer, and we call football in Brazil because you play with your feet. You can have amazing talent in the field, but you still need someone helping the team to play together. And the coach is not the person to score the goal, but the coach helps the players understand the strategy, stay aligned, and use their strings together. In a hackathon, leadership works the same way. You have talented people on your team, but someone needs to help connect ideas, remove the blockers, and keep everyone moving towards the same goal. Questions.

**[10:44.000]** What comes to your mind when you think about leaders? Please put it in the chat. I want you to see. In the Q&A chat, please. Please come on. Control was done. Alright. Power. Okay, think about kings and queens. There is a scene on Game of Thrones that I will never forget. I hope you watch Game of Thrones so we can correlate here. This scene shows the mother of dragons taking the leadership of myriam, a city. And suddenly she has to spend her time listening to endless complaints from the people from her city.

**[11:30.000]** People were hungry, people were angry, people were afraid. Her dragons were eating the goats. How does this problem? The entire day. That episode shows how stressful leadership can be. The moment you became a leader, you also become responsible for others people's problems. Not just yours, but other people's problems, people that you probably never saw in your life. And that is one of the hardest part of leadership. People bring you their problems and your job is to serve, guide, and make decisions. They look to you for answers, direction, and hope.

**[12:13.000]** To me, that is the responsibility of a great leader. And hackathons are great creating leaders, people that will serve the team. Let's go for my third advice. Let's suppose in a residential building, the residents are complaining that they are spending too much time in the elevators. What's the solution here? Please, in the chat. Chat, chat, chat. Please feel free. Don't be afraid. Oh, too fast. Beat it up. Okay.

**[13:08.000]** Any other idea? Stairs. Oh, stairs. Seriously. That's bad. That's health, but bad. Upgrade the lift. Okay. Ah, someone read the same book that I read. Okay. See someone already knows the answer? Here it comes. The logical answer is make the elevator fast. Anybody can get to this conclusion because everybody has a brain. My third advice is do not jump too fast into the logical solution. The logical solution is easy to find, but sometimes the strongest solution is not obvious.

**[13:49.000]** Instead of investing in a new elevator, what about adding mirror shit? With mirrors, people get distracted and feel the weight is shorter. The complaints will went. That is not a logical, but a psychological solution. That shows the problem and saves the building owner some money. Better solution. In a hackathon, especially nowadays with AI and vibe coding, anyone can find a logical solution and build it.

**[14:22.000]** But what can make your project stronger is finding the solution others didn't see. And now I know it's hard to ask. Do not think logically because we have brains and it uses logic. But to help you find this unique solutions, I would recommend you to choose problems you deeply understand. You can see it from different angles, from multiple experiences you had. That is how you can find solutions that are unique because you see what others don't. Here we go.

**[15:13.000]** I will start my presentation. All of these slides were after receiving some messages on LinkedIn. The presentation is about how we can help you win this 40-yard hackathon. Jay, please help me here. We selected a few tracks where Autodesk will direct help you. We have the two main here.

**[15:43.000]** If you see opportunities, you can take whatever you are going to present here to whatever is the solution you are coming with. The first track was selected that really correlates with Autodesk as the resilient cities and infrastructure. The second track is the future building and energy. If you like my accent, if you want to stay around and learn something new, you are totally welcome to stay with us until the end. Quick safe harbor. The key point of the safe harbor is that anything related to future development should not be treated as promise, commitment, or basis for purchasing decisions.

**[16:37.000]** The agenda. Today we will move through four parts and then Q&A. The idea is that we will go deeper step by step. We will start with the highest level with Autodesk, then narrow into form as they see industry cloud, then go deeper into form as site design, and finally focus on form as site design extensions. The part that is most relevant to you as developers. The further we go, the more specific we become.

**[17:13.000]** And since we have very diverse audience, I want to make sure we first understand the big picture before diving into the more technical details. So we will start broad with Autodesk and then deeper into form as site design extensions. The API has packed. Welcome to Autodesk. Please let me know in the chat if you know Autodesk, just so I have a feeling of our audience to say yes, I know, no, I don't know what's it. Autodesk is a design and make company.

**[17:47.000]** I like to say we are the meta in our industry because we are huge. Our software supports the people who design and build the world around us from building and quick structure and cities to products, media and manufacturing. Autodesk has three main industry clouds. Forma for the ACO, Architects for Engineering Construction and Operations. The built environment. We have fusion for designing a manufacturer for products, machines and physical goods.

**[18:23.000]** We have the flow for media and entertainment such as film, games, animation and content production. Each platform is focused on a different industry, but the idea is the same. Connect to data, teams and workflows in the cloud. These three clouds are on top of one single in the bottom. Autodesk platform services in the future. Everything is connected.

**[18:55.000]** By the way, this is a real Oscar. It was awarded to Maya because Maya helps support so many movie productions that the Academy recognized its impact. And I said it's not his because Maya is a software on by Autodesk. It has been used in many major moves and visual effects. For example, my favorite avatar. Maya, Oscar and avatar are cool things, but for today we are going to focus specifically on the Forma platform.

**[19:33.000]** The Autodesk cloud platform for Architects, Engineering Construction and Operations, ACO or ACO. And I know that's what you have for today. You could be the next James Bond, but you chose the wrong path. All right, Autodesk Forma, which I love. I hope you love it as well. You're going to see the short ACO, AC industry cloud.

**[19:57.000]** Our industry has been asked to deliver more, better assets and higher performance. At the same time, teams have fewer resources with workforce gaps, skill gaps and material constraints. This is why cloud data and AI matters. They keep teams, they allow teams to make better decisions earlier. And that is extremely important. And that's where Forma fits in.

**[20:37.000]** Better decisions, better built world. And hopefully we can save the planet. Forma shifts us from disconnected files and silos to more connected data driven workflows. They go as to use better data, improve collaboration and make decisions based on outcomes earlier in the process. This is very specific to construction, but coincidentally most of your projects, real projects, even if it's not in construction, will face the same problem. The key idea here is simple.

**[21:13.000]** Early decisions have the biggest influence and are the cheapest to change. In traditional workflows, a lot of effort happens later when changes are already too expensive. With Forma, the shift more thinking, testing and analysis to the beginning so teams can make better decisions earlier with less reward later, cheaper decisions. Early exploration is where teams should test the most ideas, but it's often where they have the least time. When exploration is slow, teams test fewer options, make assumptions and may commit too early. Forma helps by making it faster to explore options, check visibility, understand performance and create stronger evidence for decisions before the design is locked.

**[22:17.000]** Forma connects the AC life cycle across planning, design, construction and operations. Instead of each phase living in a separate tool and disconnected files, the goal is one connected platform with shared data, workflows and collaboration. For today, we will focus on the front end on that workflow, which is called Forma site design. Forma site design is where teams can start with site contacts, explore visibility and make better early decisions. Now we will focus Forma site design and this is our site planning and analysis software that helps teams plan every site with confidence. So we want to provide you the data.

**[23:17.000]** Forma site design combines AI powered analysis, contextual data and 3D modeling in a cloud workflow. It helps teams understand the site before they commit to a design direction. And here we have a video. Can you hear the audio of the video? I don't think so. Okay, while I was speaking over it.

**[23:49.000]** You have all the information tools and contacts you need to get more done in the conceptual phase of projects. Welcome to Forma site design, AI powered cloud software for architects and designers. Set up your site in minutes with real world contextual data and precise geo coordinates to ensure your design is grounded and accurate from day one. SketchMassin studies define building levels with real time error metrics. So your design aligns with your program requirements. Drives smarter design outcomes from the start with environmental analysis supported by AI,

**[24:33.000]** return, daylight, noise, wind, carbon and more. Compare analysis results, evaluate tradeoffs and optimize building performance with confidence. With Forma board, you can collect ideas and document decisions made supported by metrics and visuals to present in a convincing design vision. Accelerate design reviews. You can connect Forma site design with Revit and broader Autodesk ecosystem.

**[25:16.000]** I will stop here because I was hearing the music and trying to present while the music was playing. But I hope you like this video. It's the market video. You can find it on YouTube and it welcomes arises what form is doing. And I think that was ridiculous me speaking over the video, but let's move further.

**[25:39.000]** There are three simple benefits to remember. Create the site and messing in minutes, task performance directly in the model and coordinate design reviews with the team. I'm shy because this talking over the video was ridiculous. But I will move. I think a lot of people found it really funny. Yeah, it was ridiculous.

**[26:07.000]** All right, I will never do it again. All right, Forma site design is based on outcome-based planning. That means we are not just drawing geometries. We are using site context, 3D modeling and environmental analysis to understand how different options perform. And for this hackathon, the important part is the last column, the open API. Forma can be extended, customized and connected to other tools,

**[26:46.000]** which is where developers can start creating workflows on top of the platform, combining Forma site design and FortiGuard. Please see the connection here. This is a big opportunity to win this hackathon.

**[27:07.000]** This is where the connection with FortiGuard becomes very relevant. Forma helps designers analyze sun, wind, light, carbon cost and more early in the design process. FortiGuard is focused on the hyper-local temperature intelligence and giving developers access to temperature data and APIs to build climate solutions. So the opportunity for you is to think, how can temperature data, AI and Forma site design come together to help cities, designers and communities make better decisions earlier? This is not just about building an extension. It's about building something that can support more resilient, comfortable and climate-aware urban environments.

**[28:05.000]** Now, the part that developers love, Forma site design extensions. The purpose of custom extensions is to let users build on top of Forma site design and complete workflows that are specific to their needs. Not every workflow can be solved by one standard product and sometimes the need comes from Autodesk, sometimes from a consultant and sometimes from the end user. For this hackathon, this is the opportunity. Think about what workflows missing, what data could be added and what extension could make Forma more useful for a specific project.

**[29:01.000]** I have a link to share with you guys in the chat. Jade, do you have it to send them? I will also send out the links at the end. So let's stay with me for now. Bear with me. This slide shows where developers can connect into Forma site design.

**[29:21.000]** Forma already has native capabilities like contextual data, design automation and analysis, but the API opens the door for the 30-part ecosystem. That means you can bring in external data, connect your own tools, create custom workflows and build new analysis on top of Forma. For this audience, the key message is Forma is not only a product you use, it's a platform to build on. Here we are looking at the Forma site design API documentation, which is the link that Jade just sent. This is where you can start understanding what is possible, what types of extensions you can build and how embedded views work inside the Forma. So during the hackathon, do not think of this as just a reference page.

**[30:19.000]** Think of it as your starting point for turning ideas into something that can actually run inside Forma environment. All the information you need, all day step by step, is here. There are three important resources, the developer documentation, the embedded view, as the key. The Vibe Coding Scale Package, I love this part. And the documentation basically explains the API, the SDK, helps you build the extension experience. And the SQL package helps AI coding agents understand the content of the application.

**[30:56.000]** The API, the SDK, helps you build the extension experience. And the SQL package helps AI coding agents understand Forma-specific things like coordination system, transforms, and extension structure. That is very important because in a hackathon, speed matters. These resources help you avoid common mistakes and move faster from idea to prototype. So use it. These are examples of extensions and workflows already being built around Forma.

**[31:36.000]** The point is not to copy these examples, but the point is to show that the ecosystem is real and the different teams are already using extensions to solve problems. For your hackathon project, ask yourself, what is the one capability that could make a designer's workflow faster, smarter, or more climate aware? For more examples, you are welcome to check the App Store. And I will show you how to get there in the marketplace. And the App Store in the marketplace are important because they show the long term vision. Forma is not just about Autodesk building every feature.

**[32:26.000]** It's also about enabling first part and third part solutions to explore and expand what the platform can do. That is where developers become important. And you can create tools that connect data, automate decisions, and solve problems that are too specific for a generic workflow. Here are the links, Jay, if you can share with them, I will appreciate. The first link is the Forma site design page. You can just go in Google and Google and type Autodesk Forma site design.

**[33:05.000]** It will take you to the main page where you can get the trial, 30 days trial for free. And then you have the Forma YouTube for self-learning. It's a very interesting page because the trainings are short. It's like five minutes to learn a tool. And then we have Forma Futures Challenge that's coming in three weeks from now. So if you want to participate in another challenge, this is a design challenge where you're going to be using Forma to develop incredible solutions for a CD.

**[33:43.000]** And then you have the Forma site design API, which is the documentation that will guide you through step-by-step how to develop using our APIs. We are in 1940. I have other videos here, but now if you have questions you are free to send them in the chat. I'm going to show a part that's not there yet in the documentation. And by the way, this is my LinkedIn. If you want to connect and come with questions later on, or if you forgot what's the link or you are welcome to join, I can't guarantee that I will be there answering all the questions, but I will try my best.

**[34:25.000]** I suggest everyone take a picture of this so you can connect with Jordanna on LinkedIn. Yes, you are welcome. Thank you, Jay. Let's see questions in the chat, please. Now I'm going to go deeper and more technical step-by-step for those that want to use our API. And I'm going to show you how to get the Autodesk account created and use the 30-day trial. All right, we can do that.

**[34:57.000]** And as you shared your screen, guys, using the Autodesk is not mandatory to building your solution. Jordanna is giving you access, which is free for 30 days. So you can, if you're choosing any of the first one or two tracks, or probably want to be inspired about how to build your solution, meaningfully, I think Jordanna has presented that opportunity to you. But again, it's not mandatory for you to build with it. If it is, I highly recommend that you stay for the next part, because this is the important part where you can sign up and get access to the solution. Jordanna.

**[35:39.000]** Yeah, thank you so much. And especially for those that understand the construction industry, out of the desk, I like to say that's kind of like meta. We are the big ones in construction. So most of the architects, engineers will be using software that comes from us. So if you are in this scenario, yes, the integration is very interesting. But let's say you are nothing correlated to construction, design, or making, then, yeah, maybe it's not the best way to go because you should focus on a problem that you deeply understand.

**[36:08.000]** That's my advice as a hack. All right, let's keep moving. I see some people stay. So thank you. Here we are on Google. First step is type.

**[36:24.000]** Forma site design out of the desk. You're going to go site design logging. This is our main page. You can scroll down and see some of more information about the form. What it's doing. Then you hit free trial.

**[36:40.000]** And this for triers for tools that are not in the construction company. If you are working in the construction industry, your company may already have access to this. So talk with your IT or the out of desk leader and this person can sign you a license. And this is already included in most of the packages. So you should not be that worried about, oh, we're going to have to pay. No, this is already included in most of our packages.

**[37:08.000]** But if you are new here, just a developer, not in the industry yet, you can come and see. You can come and enter your account information. I'm covering here because I was using my best friend's Camilla email and email address state company name. Then it's going to prompt you to some verification. Going to send you a code through email. Select the code.

**[37:35.000]** And hit next. If you don't have an out of desk account yet, it will send you to the out of desk registration. And here you're going to add your information name, last name, password. And these are for free because you're in the 30 days trial. So you don't need to be worried. Then you have the verification again.

**[37:58.000]** And just follow the steps. Welcome Camilla. You have 30 days trial and it does not start charging you. It's just going to end. So you don't need to be afraid about your credit card. All right.

**[38:12.000]** So here we go. Starting our experience. Just accept the terms read them as you like. Be responsible. So check them before unchecking or checking any of those boxes. And this is our front page.

**[38:32.000]** As a first time user, you're going to receive all this tutorials that go step by step. What you should be doing here. So for example, you start with the setup a project with real world time data, model contextual through the design minutes and optimize the living quantities and sustainability. And this is one of the reasons I'm not going through a demo, how to use formal with you guys in this presentation because you can self learn when you start. And the UI is just the best like anyone can use for my is meant to be simple and it is simple. So more information when you first time use it some helpers.

**[39:11.000]** And this is our first page. If you already use it a few times. That's the first page that you're going to see. You just need to enter an address. I'm using here. Miami.

**[39:25.000]** Because Miami has a characteristic challenge where floating zone. So I love to use my own as examples just to show how former can help cities, especially those in environmental issues. Okay, former has a limit in the area. It is two by two. So that's the limits of error that you can analyze here, which would be 1000 acres about that. But assume, oh, by the way, this is running in the web browser.

**[40:00.000]** This is in the cloud. So you don't need a strong computer. You just need a good Wi-Fi, which I didn't have yesterday when I was recording this. Yes. So this is our reception. We have the data marketplace where you can start ordering data such as satellite imageries or topography, building surroundings.

**[40:21.000]** And we have different providers here. Some more instructions how you can use this is your first time here. We want you to feel at home. More information. And then for you as developer, we're going to focus in the extensions portion. You can come here and hit add extensions.

**[40:41.000]** And then you're going to have a field that we're already approved in our marketplace, but you want to create extension. You're going to type my first extension mark box, check mark. And hit create. If you see, we have a message from Andrews in the side and from this message, you can get help. We have some articles, tutorials. Okay.

**[41:08.000]** Here you can set up who owns this. It's yourself. And then you can allow who can have access to this page. The idea of the project is basically in the URL of your project. That's this one that I'm highlighting at the top, but without the first. I forgot the name of this.

**[41:30.000]** Yeah, the first directory. Then. Yeah. That's way in this format here. Then you can hit save. Or if you want to explore more of these options that you have in the management, you can, you are welcome to do such as you can make it available to all the former users.

**[41:57.000]** That means that when you share your ID, ID, anyone can use in whatever is the project. Moving forward. This is pretty much what I have to you to start with. This will take, and I actually can share my screen, the real thing happening here. Okay. I'm going to share my screen with you.

**[42:19.000]** And since we have a few minutes yet, I'm going to take it a live demo. Form of design. Okay. Let's go here. Can you see my screen? This is where you're going to come.

**[42:34.000]** You're going to login. I already have my login, so I don't need to get the trial. And here, I think this is the simple project I used. This one that I used yesterday. Okay. This is how it's going to look the first, a second time you use it.

**[42:54.000]** And then to find your extension that we just created, you're going to come. Let me delete here first. Remove from my site. It's going to look like this for you. You're going to come add extensions. This is where you would go to create an extension, but this is where the extension that you created earlier will be.

**[43:19.000]** If you want to see examples, you are welcome to click and watch what other people has been creating and how they look like with Forma. You have different types. You have extensions that are free. You have extensions that will require a license. So you basically start from Forma, then you log in with your paid license and get what you need, bring to Forma, or extract from Forma.

**[43:44.000]** But each solution will have a page demonstrating what they are achieving and how to use the tool. And if you come to create our extension and want to share it with our app store, you are completely welcome to submit. We have a team at Autodesk that revise this information. And let me just see my chat because I hear some things. Please, Jay, if you need to stop, just interrupt me. You are welcome to see some examples, but your extension will be here.

**[44:26.000]** And then you just need to add, add extension, agree. And this is going to be here. Right now it's empty for me because I haven't developed anything. But basically whatever you develop will be shown here, here, or here floating. And you're going to see in the documentation that we have different positions, different windows for your extension. And depending on what you need, you can choose between how they show up and interact with our user interface.

**[44:59.000]** All right, I think we are short on time. We'll have 10 minutes. So I will open up for questions. And let's, yeah. All right. Thank you so much, Jordana.

**[45:14.000]** That was rich. I learned a lot myself. So I'm sure that the participants will learn. I can tell from the attendees number is that a lot of people were very interested. So they stayed. So there are a lot of builders in this meeting and call.

**[45:31.000]** So it's, it's really great. And again, guys, if you haven't connected with Jordana, this is your chance. Please connect with her on LinkedIn and she probably find the time to be of assistance to you. We're going to take roughly 10 minutes to answer your questions. So please go ahead, put your questions on the chat. If you put them so much earlier and we haven't answered them related to all of this, I really hope that you guys would put them again just because it's a lot of questions out there.

**[46:06.000]** And we want to make sure that we, we can answer all your questions. I can see some questions related to the hackathon. So our team in the back office is trying to, to handle all of those. But one common question I've seen is, is it mandatory or compulsory to use for one? No, it's not. It's only compulsory to use for regards API, which is our temperature API.

**[46:33.000]** This is another solution that thanks to Jordana and Autodesk, they've extended it to us so we can use it if it matches your track and it helps you build a solution that can deliver and obviously help you become a winner. This is one of the greatest solutions when it comes to engineering, when it comes to the tracks. There is nothing on top of Autodesk. I'm happy to say this comfortably. Autodesk has built the probably one of the best visual dashboards and solutions for builders like yourself. And I think immediately this is a solution that will resonate with you and the three general social extending 30 days trial time so you can use the dashboard to, to build with it.

**[47:29.000]** Now it requires a little bit or a level of sophistication, but this is where we know that you guys are there to, to build those sophisticated solutions so you can deliver the impact that you're promising to others. So let's go through some of those questions. I know that you can already see the questions, right? Yes. So if you want to jump in, just take one of the questions. It's up to you. I can ask you as well. And if the, can we unmute the audio for them?

**[48:04.000]** No, so it's only on the chat that we will take all the questions. So I see a question here from Mark is ArcJS required to use Formasite Design? No, it's not. We know that there's a license to use ArcJS. The contextual data that we provide some comes from ArcJS, but so far for free. But then if you want to connect with your ArcJS, we have an extension with ArcJS, we are partners with Esri. So you can completely bring information from ArcJS into Formasite Design.

**[48:42.000]** Let's see another one. If you don't know what ArcJS is for, just by show information, very common for CDs. I was, I'm at J at Esri. So that's how we met each other. Let's see. If I decide to use Forma, how could I export shared extension to add it to the package we have to submit?

**[49:08.000]** So basically, when you create an extension in Revit, you basically going to bring your code and connect in Forma, but everything is going to happen inside of your code. So the same code you can use in your submission. And we, for this hackathon, need to be used for FortiGuard. So we'll be a code that, for example, is structs the information from Forma. It can be a viewer, could be the data from the geometry, and then connects with the data that comes from FortiGuard.

**[49:37.000]** And this is going to be, like, let's say a web app or something else. And let's say in the future, you want to share with Autodesk, you can submit the same project to our app store, and we're going to check if you want to make it available for others. If you want to charge for the license, if you want to make it available for fee, that's up to you. One of the questions is about, is it okay to consult with mentors regarding the IDE and its implementation? I think it's okay if the mentors have the time to extend it to you.

**[50:13.000]** So what I would suggest is that all the mentors, they have their LinkedIn available. A lot of them are aware that you guys need the support, so they'll probably just respond to you. So I would suggest that you reach out to them. Just in case the mentors do not support, and you would like to get some technical feedback, we're also happy to do this as FortiGuard's team is available. So you just need to email us at hackathon.fortiGuard.com and we'll take out for you.

**[50:43.000]** Okay. We have one other question from, and I'm terrible with names, so I'm going to tell you the last name, which looks easier. Rania, I hope I said that right. If we integrate Forma site design on our solution, does the target would definitely be architects? Not necessarily, but definitely Forma is serving the AEC industry, architectural engineering, construction industry. So it would be interesting if you bring something that connects environment analysis with the built world.

**[51:19.000]** And that comes with, yeah, when we, in design for construction, look at planning a site, we care about temperature. We care about the city. We care about comfort. We care about the materials. So that's a strong connection between the construction and the FortiGuard. Can we answer that?

**[51:45.000]** Let me see if we have more questions. Most, Jay, please, there are some here with relative. Yeah, those are the team will probably handle. There's a question here that was just posted. Can Forma site design import external geospatial temperature data from an API like FortiGuard and visualize or analyze it directly within the site plan? Yes.

**[52:15.000]** Yeah, visualization. It would be very similar to our extension with ArcJS. So please go there and have a look in ArcJS. Let me see if I can open my screen here very quickly. If I can log in in my ArcJS account. But yeah, you add with ArcJS, you add the maps as layers and then you see, so for example, the floating zones, you add the floating zones and then on top of our city, on top of our screen, you're going to see the floating zones in between buildings and between the topography.

**[52:49.000]** There is another question as you share your screen. It asks, is it okay to use Revit or AutoCAD? Yeah, they are connected clients. Oh, that's great. Great question. They are connected clients and we have great integration with Revit, which means you can go back and forth.

**[53:09.000]** It's a live synchronization. So whenever you do some designing Revit, you can send to Forma, Forma to Revit. And with AutoCAD, we just release our export to CAD and import from DXF. So you definitely can use them. Can you see my screen? Yes, perfect.

**[53:27.000]** Okay. So here I'm going to give a taste of what's possible here, contextual data. Someone asked about ArcJS data. If you see here at the top, you're going to see where this data is coming from. This, for example, is coming from Esri, which owns ArcJS. I typically like to use the spec, which already includes almost everything that architects will look at first.

**[53:48.000]** Let's bring imagery from Esri as well. And then very quickly, you're going to have this viewing Forma. And then for the Esri purpose, for example, we have here the extension. I'm not sure if I remember my password for Esri for ArcJS. Let me see my phone. I have it saved some more.

**[54:15.000]** Esri is going to be here. Oh, it's logged. Thanks, guys. I would not remember the... And this is how, for example, your app could look like. You could have this floating windows that brings your information.

**[54:31.000]** And then you can come and add layers, floating. I think this one that works. Add. Here. So now you have the visual aspect of the floating zones correlating with your environment site. Then you can close.

**[54:53.000]** And this is going to live here. And this could be, for example, temperature, hitting zones. Examples come with your idea. Other questions here? I think two more questions will take them very quickly. So would it be complex to use Forma?

**[55:17.000]** Or is it more efficient as an approach? And I think this is for you to decide, but I definitely think on our end that it's the efficient approach. So do use Forma if you're comfortable with it. I think the other question here is, can we integrate Autodesk Forma with our project built in VS Code using its API? I will check the documentation, but my short answer is yes. I can be wrong here, but my short is yes.

**[55:57.000]** And related to the tools that you're going to use to create your code, you have whatever you want. You're going to be just connecting the code inside of our UI. I'm sorry, I was most asking. I'm not sure if I got the right question. I was looking. So please, if I answer it mistakenly, I didn't understand the question.

**[56:20.000]** Please send again. But I am looking here for the connection with Revit that I want to show you guys. I have a MySlide deck. Yeah, but basically, let me show you live. Basically, in Forma, you have all the connections here. And to send to Revit, you're literally going to come to your propose and download the Revit adding and send to Revit.

**[56:50.000]** When you send to Revit, you're going to see the same view with this imagery, with this topography. It's very flat, Miami, but with the topography, everything Revit. And most of the geometry, you can further edit in Revit. And if you're looking more into the building aspect, you have the building design that allows you to design the building itself. So facades, layouts, you're welcome to learn more in Forma building design. Or in our YouTube channel that I shared earlier.

**[57:24.000]** And by the way, when you search in YouTube, in Google, you may going to see Forma build. This is another thing. You want to use the building design. Not the Forma build, because Forma build is for operations. So Forma building design. So this is more in the facade level, internal layouts, but also correlates with the temperature.

**[57:52.000]** And you may take benefit from this. Yeah, this is pretty much what I have. Fantastic. So I think we came to the end of this session where three minutes even over the time, but it's great. We received a lot of questions, a lot of attendees stayed here for this very informative session. And I think one question that was asked and I'd like to take the time to answer it and then conclude is that I love people who build solo, but I also really enjoy teams.

**[58:28.000]** So if you're building solo, that's okay. But try to find your team because people and ideas when they come together, they bring something greater. So it's not about how fast can you go. It's about how can we go together. If we go together, I think we can achieve something meaningful. Jordana, this was one of my favorite sessions.

**[58:51.000]** Again, I heard a lot. All of this is already an amazing partner. You've been great to us and we're truly thankful. I think every participant at the hackathon is thankful to you. There are a lot of people who will watch the recording as well. They'll probably connect with you later and reach out for questions, but we really appreciate your time.

**[59:15.000]** We really appreciate the information that you shared with us and the experience that you just laid out to us after so many years that you've spent in this industry. So thank you so much for your time. Yes. And for the audience, please have fun. You're going to learn so much about yourself when you put yourself in challenges like that. And especially if you go with a group, you're going to build leadership.

**[59:38.000]** You're going to learn about how to support each other. That's a very good opportunity for you to grow. So good luck. Thank you, Jordana. And for all the attendees, you will receive the recording. So every day in the morning, you receive an email on your inbox where the recording of the previous sessions are so you can follow down and anything as well to update you about the hackathon.

**[01:00:03.000]** Thank you all for staying until the end of this and we'll see you very soon. Bye now. Bye bye.
