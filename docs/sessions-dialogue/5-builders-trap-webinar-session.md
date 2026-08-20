# Escaping the Builder's Trap: Building Minimum Lovable Products (MLP) with Google Cloud — Full Transcript & Summary

**Date:** August 20, 2026 | **Duration:** ~45 minutes | **Language:** English

**Speakers:**
- **Nahil** — FortyGuard Community Lead & Hackathon Organizer
- **Ahmed Abdelkhalek** — Head of Digital Natives & Startups at Google Cloud / Hackathon Judge & Mentor

---

## Executive Summary & Key Takeaways

In this mentorship masterclass, **Ahmed Abdelkhalek** (Head of Digital Natives & Startups at Google Cloud and Hackathon Judge) shares fundamental frameworks on how developers and startup founders can avoid the **"Builder's Trap"**—the common mistake of building complex, expensive technology for the sake of tech rather than solving a tangible, painfully felt customer problem.

Ahmed draws on his experience evaluating thousands of startups and building iconic products at Google (such as **Google Cardboard**) to explain how to move from rapid ideation to a **Minimum Lovable Product (MLP)**. He challenges builders to critically evaluate their AI choices, adopt resource budgeting discipline, and focus on delivering measurable commercial value to judges and end users.

---

### Key Highlights & Strategic Frameworks

1. **The Google Cardboard Case Study (Speed over Over-Engineering):**
   - While the market was investing millions in building $1,000–$2,000 VR headsets, Google engineers tested the VR market using a simple piece of cardboard, lenses, and an existing smartphone.
   - They prioritized rapid iteration on the core user experience rather than spending years on custom hardware that might fail in the market.

2. **Evaluating AI Critically (Avoiding AI Hype, Latency & Cost):**
   - *"AI can solve almost everything, but should it be used to solve everything? And at what cost?"*
   - Example: Resizing images does not require a multimodal Gemini call when a 2-line Python script is faster, cheaper, and 100% deterministic.
   - Use traditional deterministic code (regex, Python scripts, relational queries) for predictable tasks, and reserve LLMs/AI models for cognitive reasoning, contextual translation, and autonomous tool orchestration.

3. **From MVP to MLP (Minimum Lovable Product):**
   - A Minimum Viable Product often feels transactional. A **Minimum Lovable Product** comes from "falling in love with the problem."
   - The best startup ideas come from observing the most mundane, manual, repetitive tasks consuming an operator's or CEO's time every day.

4. **The 15-Minute Pre-Build Decision Checklist:**
   - Every feature or hackathon project idea must pass 4 tests: **Hero** (exact persona), **Pain** (manual/expensive workflow), **AI Justification** (is AI genuinely necessary?), and **Kill Switch** (fastest 24-hour validation test).

5. **Google Cloud for Startups Program Overview:**
   - **Start Tier:** $2,000 in GCP credits in Year 1 for bootstrapping builders. (Run lean on a single $70/month VM + open-source stack instead of over-engineering global multi-region clusters for zero users).
   - **Scale Tier:** Up to $100,000 in Year 1 + 20% coverage (up to $100,000) in Year 2 for funded startups (up to $250,000 in Year 1 for AI-first startups).
   - **The 4 Program Pillars:** Financial credits, Technical 1-on-1 architecture reviews, Business networking & customer introductions (*the #1 most enduring asset*), and Community.
   - *Note:* FortyGuard is a Google for Startups portfolio company, and CEO Jay Sadiq is a Google-appointed startup mentor.

6. **Agentic AI Architecture & API Failure Management:**
   - Multi-API agents require robust fallbacks, graceful degradation, and rate-limit safeguards.
   - With global chip and GPU shortages, the future belongs to lean, CPU-optimized models and efficient API routing rather than brute-force compute consumption.

7. **UI vs. Performance vs. Problem Solving:**
   - Google.com's minimalist white screen with a single search bar proves that solving the user's intent with extreme simplicity beats complex UI clutter every time.

---

## 📋 The 15-Minute Pre-Build Decision Checklist

Before writing code or architecting complex LLM pipelines, run your project through Ahmed's 4-step filter:

| Step | Dimension | Core Question to Answer |
| :-: | :--- | :--- |
| **1** | **Hero** | *Who is the exact person, job title, and industry who will use and pay for this?* |
| **2** | **Pain** | *What is the specific manual, slow, or expensive task they are forced to do today?* |
| **3** | **AI Justification** | *Is AI genuinely required, or are we adding latency and cost just for hype points?* |
| **4** | **Kill Switch** | *What is the absolute simplest version we can build to test our hypothesis in 24 hours?* |

---

## ⏱️ Agenda & Topic Breakdown

| Timeline | Topic / Discussion Area | Lead Speaker |
| :--- | :--- | :--- |
| `00:00 - 06:30` | The Google Cardboard Case Study: Speed & Lean Prototyping | Ahmed Abdelkhalek |
| `06:30 - 13:00` | Critical AI Evaluation: Deterministic Code vs. LLM Hype | Ahmed Abdelkhalek |
| `13:00 - 18:30` | The 15-Minute Pre-Build Decision Checklist | Ahmed Abdelkhalek |
| `18:30 - 27:00` | Google Cloud for Startups Program: Start vs. Scale Tiers & The 4 Pillars | Ahmed Abdelkhalek |
| `27:00 - 32:00` | Startup Monetization & Iteration (Facebook/Kodak Case Study) | Ahmed & Nahil |
| `32:00 - 37:00` | Moving from MVP to MLP (Minimum Lovable Product) | Ahmed Abdelkhalek |
| `37:00 - 41:00` | Multi-API Error Handling, Rate Limits & Compute Efficiency | Ahmed Abdelkhalek |
| `41:00 - 45:00` | Simplicity vs. Complexity (Google.com Philosophy) & Hackathon Advice | Ahmed & Nahil |

---

## 🎙️ Complete Spoken Transcript (Timestamped & Attributed)

When we thought about it, we thought about, okay.

How many people are going to buy $1000 or $2000 worth of VR headsets? What are they trying to do with it? What's the actual problem? We're not saying that that doesn't solve a problem. But then the way we think about it is how many iterations does it take you to actually test the market to identify and solidify the problem statement to build a solution on it? And what Google started thinking, the engineer started thinking of. The reason why they call the cardboard is because they actually got a piece of cardboard. And then they started ideation, brainstorming. How do we do this? How do you do that?

What are we trying to do? We're trying to introduce a new experience to the end user, to a consumer.

And then Instead of building a lot of hardware and spending a lot of time and a lot of investment and then launching it to market and then potentially it might fail, It would take a lot of time. What we're going to do is We're gonna build a cardboard. That acts as a glass. And you insert your mobile phone or device inside the cardboard. And there's a piece of application that basically changes that cardboard into VR experience. So you didn't spend time building hardware. and iterations and a lot of investments in order to go to market. With a very simple tool, And actual technology is you focussed on the experience within the operating system of the phone that it's in the hands of everyone. And you're able to introduce and bring that experience to life.

That is affordable, very cost efficient when it comes to building, but also very cost efficient for the stakeholder that you're solving the pain for.

And this is when we talk about, You need to iterate, reiterate, one, two, three, four, five, six, seven, on the actual core problem. Because you'd need to optimize your product to learn. Speed. Don't perfect it from day one. And anyways, nothing is perfect, right? You build a product that you think is perfect. You grow it, you find issues, challenges, obstacles, new things. So it doesn't become perfect anymore and so on and so forth. You keep on iterating the rest of your life.

Speed of identifying the go to market for the product that you're building is the most important thing that you need to focus on. And again, it doesn't matter who you are. It matters the most, I think, from my experience. To the people who are building. But also, Puts you in a completely different category. So you would be able to find your unique. Advantage and quality of identifying the problem statement, making sure that what you're building is you're building it for that. You're not building, you know, because you're using the best database. The product is not successful because it uses it has the best UI UX.

Because it solves a problem very simply.

And then we get into AI. Which, again, for me, super exciting, and I think it's also, it's exciting for everyone. It's a completely different era that we're living in.

But you need to evaluate AI choices critically. ensuring that we're not introducing unnecessary latency and cost just for the height. What do I mean by that?

You can use AI to build.

You can use AI to build. But you don't have to use AI every single time you're trying to solve a problem.

If you're building a tool or a product that does very simple example, image resizing. You'd use them, you know, Gemini models, whatever models available, open source, LLMs.

To resize an image. Now, That, and actually that's a real example because someone came and asked me about that. Can Gemini resize images back in the early days? And the 1st question asked them, What are you trying to do? So I have images. And I want to, you know, publish them on X, Y, Z website. But I want to do that at scale. The question is, why do you want AI to do that? It's like because we can use AI, it makes things easier. Like, sure, yes, you can.

But should you?

How much money is it going to cost you?

Versus, you know, writing a couple of lines of Apython script. To actually resize images for you.

And that's what I always challenge everyone that, you know, whether it's my personal experiences or customers, startups, developers,

AI can solve everything.

Fact. To some extent. But should it be actually used to solve everything? And the follow-up question is at what cost? And this is where, you know, it's incredibly powerful, but it's not a silver bullet for everything.

It's good, but should it? Right? And that's kind of the questions that I would start asking myself when I'm using AI. Use AI for syntax, for code syntex, for structuring. Whatever for things that for functions. For things not, The, you know, software engineering used to be. You're a good software engineer, if you build the most efficient code. The most, the best syntax, the shortest number of lines, of code. That was true. Pre-A. Post AI.

This is one thing that I think That would evolve and get software engineering and development back to its roots. Which is problem solving. Don't spend a lot of time about, you know, you know, fixing your code and things like that. Does it mean 100% of the code is going to be written by AI, but then reviewing it, optimizing it.

But building a feature 100% using AI? Maybe. Maybe not. Again, it goes back to. What are you solving for?

And always, and I was going to talk about this a little bit in the next, the next part of the next section of the, of the, of the presentation of the session. Please be responsible with your resource budget. There's nothing free in the world.

Traditional deterministic code is faster, cheaper, and entirely predictable.

Whatever budgets you have and resources, budget doesn't have to necessarily be cost, dollar. It could be resources of whatever, um, whatever uh, type, which then translates into how much you pay and how much you spend. I will give you some examples in the 2nd part of the session, but this is very, this is very important. Regx versus LLMs. Cognitive reasoning, autonomous action. You know, it depends, again. There's always the quality to cost balance is very important. It's very very important. So make sure to be responsible.

The last part of the 1st uh, or the last slide of the 1st session is your checklist.

15 minute before you've been. Anything, for you, Bill, anything. And listen, I'm more than happy to optimize it updated, hear feedback. What do you think of it? Sorry, I'm not looking at the chat if anyone is posting anything, but because, you know, because of the screen sharing and so on. Um, but um, feel free. Love to have those conversations separately or whatever it is. But what I would, you know, one takeaway is this checklist. So run every feature or project idea through this. If it passes, you have a lean targeted path forward to prove your hypothesis.

One is zero. Who's the hero? Named exact person. Rule, industry who will actually use this. Second is pain. What is the manual? Slow or expensive thing they're doing right now. AI justification, is AI generally required to solve this? Or are we just using it to earn high points at the expense of latency and cost? And then the kill switch. What is the absolute simplest version of this product we can build to prove our hypothesis within the next 24 hours?

And these are the 4 points that I would, you know, recommend and suggest everyone to, you know, go through. And make sure that You answer those questions. Which will then help you to the closest route to. The product that you need to build today right now for that hero, for that day.

All right. Um, That's the 1st part of the session, which for me is super exciting, super interesting. I still use a lot of that today. Um, I always remind myself when I'm speaking to, you know, the startups that I work with, um, You know, uh, because startups are fun. They're always up to speed on tech. Um, you know, they're always hands on. And with the excitement of technology and what's happening around us. It is sometimes.

It most of the time, it happens that we forget about what we're actually solving for and why are we building this?

The next part is a little bit more related to if you are a developer, if you are part of a startup, if you're building your next startup, I want to make sure that you have access to what I'm going to show you today.

And tell a little bit about our program for startups.

Startups, stop startups globally, use Google Cloud for speed, intelligence, savings, and our partnership.

The program is 2 main builders, start and scale. If you're earlier in your startup journey, and not yet backed with startup equity funding, you may be eligible for the start here. I'll tell you about the benefits later.

If you're backed with startup equity funding from pre-C to series A, you may be eligible for the scale here. You get access to Google Cloud, workspace, Google Maps platform and Google ads, and you get different benefits across each product portfolio.

There's a QR code at the end of the presentation. Feel free to scan it. And go through the application platform. If you're today, a start early stage startup. Or you're scaling anywhere between PC to series.

We understand the journey of every single startup. I've been through it myself. I love it. Um, I can't live without it because this is what keeps me up at night.

We understand the journey, even as Google. You're trying to move from an idea.

Two, typically people are used to MVPs, minimal viable products. But from now on, we're going to use from an idea to a minimum loveable product. Find product market fit, scale, all while facing significant hurdles across different journeys within your, within your actual journey. Resources are tight, you need d-technical expertise. It's hard to find, and you have to build it for future scale that you can't yet collect. That's why we created the go for startup scout program to provide more than just infrastructure.

We aim to be your true partner. providing comprehensive guidance from Googlers and technical resources through our Google Club platform specifically. To help you build and scale.

What is our program built on? It's built on 4 key pillars. And I'll tell you my my favourite. Obviously, 99% of everyone I present this program to their favourite is financially. That's my least favourite, and I'll tell you why. But we have a financial pillar, where we provide significant crowd credits to remove the initial cost barrier of building your infrastructure. We offer everything from hands-on workshops and training to direct one-to-one guidance, from our engineers to help you with architecture, AI or security, and that's within our technical plan. The business side. We hope you navigate the broader Google ecosystem, connect you with customers and partners through our network.

And finally, community, because we know how valuability is to connect with peers and experts, who have been on the same journey. We make sure that our community is accessible to everyone who's on the program.

I don't want to put the poll on, but I'll just tell you right away what's my favourite? My least favourite is financially. My most favourite is business. And the reason why is because Any credits that you get on any platform. They're not forever. But any relationship you built through the business side. Will last forever.

So financial is something that is point in time, I would save X amount of money. It will help me in the next. Uh, you know, a couple of burns. And then I'll start paying.

And what I try to focus on is with early stage and with the ecosystem. How do I make sure to, you know, again, guide startups and support them throughout the journey of how they're building and what they're building and focussing on the problem statement.

And then take that to the right buyer. to get their 1st customer. This for me is you cannot weigh that with any amount of money for any financials.

Because again, financials, are not permanent, they're temp. You're going to finish them. can burn them overnight. Today, you can burn financials overnight and I'll show you the numbers.

But business relationships and and networking and what you build there, even if that customer didn't buy from you. But if you build that relationship, They will tell their colleagues or other businesses that makes sense for them to buy your product.

And this is where you build trust, and once you build trust, it's forever. And that's why I try to focus as much as possible with every start of that. I'm, you know, uh, uh, Grateful to work with them.

to focus on that. And when you look at the financial part. You need to be very responsible. You have a cool idea. I want to run a couple of GPUs, LTPUs just to see if that cool idea would work. And then you burn $1000 in a couple of hours, even if not less. And then you end up not solving the problem. And even if you solve it, that cool idea. You don't know if it's, if it's easy if it has a market fit or not.

We know that every startups journey is unique. Everyone is not the same. And that's why our approaches is simple. We meet you where you are. It's not a one size fits all program.

Have an idea. All the way through to scaling your business globe. We start with the start here. For those of you who are at the very beginning or thinking of building their own startup, the founding and bootstrap stage, working on ideation and prototyping, the start tier is designed for you to take you off the ground. And building with.

Building with $2000 worth of Google Cloud credits for your 1st year. I am 1000% sure that Everyone on the call today. Who have seen $2000 and I'm seeing it with a lot. I saying it with a lot of passion and excitement, you start, you're laughing already behind the screen. And I know why because of, again, we've we've seen that with a lot of steps. 2000 What am I going to do with $2000? I need this. I need that. I need to scale. I need to be ready. I, I, I, I. When you sit in the room, What are you spending today on?

What do you want to spend in 2000? I want to build a virtual machine and then I want to build reliability so I want, you know, um, high availability, and then cross region availability because when we go global, I want to make sure that our product is accessible, scalable. How many customers you have, zero.

Then have a single virtual machine, Linux. Open source databases, open source technologies, in a single machine, That shouldn't cost you more than $70 a month, Prototype, MVP, do whatever you want.

And make sure that you don't finish those $2000 in a year. Well, you have to, otherwise they're going to expire, but the idea is, the point is, $2000 is a lot if you're MVPing. If you're still trying to figure out what are you going to do?

Now, going on to, um, the next year. Which is the launched. And skating team. So basically, you grow, you secure institution funding. Your needs change. You have product in the market. And you're ready to scale. That's where our scale tier comes in.

In your 1st year, You get access to Up to $100,000 worth of Google Cloud credits.

But we know that scaling is a multi-year journey.

So our partnership continues also in year two. In year two. We cover 20% of your usage up to another $100,000.

To help you manage your costs and you expand and expand your customer base. Responsibility is the keyword. Why? Because You can burn this amount of money overnight. On clients?

How you maximize the value of this benefit. Do not apply for the program if you're not ready to spend this money over 12 months.

Because if you only spend 20 K, so that means you're still not that ready to scale, where you're so efficient, so you potentially don't need it.

Timing is very important. When you actually get access to those credits is very important, how you use the credits is even more important.

And if you are a, An AI 1st started. And institutionally funded.

In the 1st year, you'll be eligible. And we increase our support significantly from a 100 K in year one to $250,000 of credits in year one.

And because We know that it's a multi-tier partnership, Year 2, we're still there for you. We cover 20% of your bill, up to $100,000 as well.

So if you're a 1st prototype, To global launch, we have a program designed to support you every step of the way. And that's our deep commitment to fostering innovation and ensuring that the next generation of AI power solution. Is built on Google Cloud.

To wrap up, I want to leave you with 4 key takeaways. First, AR evolution is real, and as startups, your speed and agility are your greatest advantages.

You'll have to do it alone. Our program is here to support you and to partner with you every step of the way.

We also offer you and provide you a complete stack where it gives you an enabled choice for whatever you're building, whether it's open source. Or 1st party solutions. Or even 3rd party. And finally, and the most important piece. Focus on solving real problems for who you're building for. The checklist, always have it. Keep it in mind. And use technology only as a tool, to build something that is powerful, but the power of what you're building is in how much impact does it have? On the user or the stakeholder that feels that pain.

And if you, so, If you're inspired to start building, and I know that throughout the 40 guard hackthon, you'd be super inspired with the amazing team and everyone else in the lineup. We're here to help. You can scan the QR code to learn more about the program and apply whenever you're ready, not necessarily today. Connect with me directly. I'm more than happy to Talk more. And to make sure that you have the right tools and the right platform. Thank you so much for your time. Stop presenting. And back to your snail.

Thank you so much, Emma, for that amazing session, by the way. I do want to highlight the 2nd part of the session that you just talked about. We, as 40 guard, would vouch for the startup program, the Google Startup program, which is there, because 40 guard is also affiliated and is under the Google Startup programs. And that is how we have Emma here, who is currently vouching for bodyguard as well as he is so dedicated and close to the product and to the company as well. Not only that, our CEO and founder, J. Sadik, is also Google appointed mentor for the Google for startup programs as well. So we do vouch for what Emma is saying and it is very, very crucial in order to shape a startup. And I just want to thank you again, Emma, for the time that you have given. There are a lot of questions that came up, and we have been trying to answer a lot, and um, there are a few that I highlight for you, and I'll ask you right away.

So you mentioned designing products to solve the problem of 1st paying customers. But for 1st few years, Facebook was not even sure how to make money from the users. So how did they grow to the skill now?

I think it's a very good question. Um, I don't know the details of how Facebook now met the, you know, solve the issues and problems. But like you're rightly said,

The only thing that I think every single company starts working on is how do you? Uh, you know, build small and try to scale, uh, or build small. To solidify the problem statement again. At the Facebook Times, I think I was, I read an article before about what happened. Um, And how innovation and evolution changed.

Facebook initially, in my understanding, started as a a pictures company, right? So you can upload your pictures and believed in the distal era. And there, believe it or not, in that article, um, It was stated that there were competing in the main competitor at the time was Kodak. I don't know how many of you still know Kodak, right? But, um, Kodak was basically a very a typical studio where you go take pictures, put it in a frame, and then keep it at home. your wallets or whatever. So I think at the time, Kodak was on the SMP 500. Um, It will call that cleft SNP 500 because of distant era. Facebook started climbing at the time when they started growing. But then Facebook started with a very simple app, a very simple idea.

They didn't know how to Make money out of it because I think. What Facebook solves for today is not what Facebook was built to solve for when they were born. And that's how the iterative approach is very important. You start small with something that you believe is a problem statement. How do you make money out of it is a different, I'd say, ball game in the sense of, if you solve the right problem.

I think you'll be able to sell it and make money from it. If you're not able to make money there's something missing. And the iteration, if you're not able to envoid the 1st customer. Now, onboarding 1st customers, not sitting after 3 meetings and saying, hey, my product is not working. Absolutely not. Different stakeholders have different requirements and so on and challenges. So how much time have you actually spent to picture product? How much time have you spent to reiterate to get feedback? to change to update? So that flexibility is very important, which will then give you speed? Which would eventually make you realize how do you make money out of it?

Um, Facebook specifically today, they're making money out of their ads business. That's the core kind of uh, um, uh, um, revenue stream. And that has changed throughout the years. Ads was not a things back in the days, they still add specifically. Right? Maybe at the time it was still then distant ads wasn't a thing, it was everything still on, you know, you have the advertisers on your physical newspaper, et cetera, et cetera. So I think it depends on the era. Um, and the problem that you're solving for. There are things that a lot of companies have built, didn't know it succeed. Um, but it's succeeded for a lot of different interesting, interesting reasons.

Um, a part of it is uh, focussing on the problem statement. One of the examples that I Actually, for the guard, I don't know if everyone in the audience knows the actual story or for the guard or not. Uh, you know, how the amazing J started. But it touches a lot of, uh, a lot of the things that I talked about, uh, and I got a lot of inspiration from how the story started and then completely shifted, right? Um, so, Again, there's not one right answer um, to, to how do you make money out of a, out of a product. I would always, you know, don't worry about making money out of the product until you figure out whether this is the real problem statement that you're solving or not.

Got it. So you talked about MVPs and MLPs a lot as well in the presentation. There is a particular question. It is very inspiring to see how you, uh, how your MVP evolved into an MLP. How do you think the shifts that change builders approach to their core idea?

Um.

In order to get to most loveable product, you need to get to falling in love with the problem or the core idea. Right? Falling in love with the problem is not easy because the problem causes Spain. If you're feeding it every single day, then that touches you or touches someone else. Um, when you think, About as a builder. I still, you know, do things on my own just for the fun of it. Um, I sit with a lot of my friends and uh, who own, you know, a lot of their startups or small businesses, et cetera.

And then I asked them those questions. So he's like, yeah, I'm trying to learn this tool, this AI tool, that AI tool. I want to make sure that I use it, but I don't have engineering. I don't have tech. What do I do? How do I do it?

Which gives you a signal that builders are not going away. You need more builders. Um, and the reason why you need more builders, you need more builders that can identify the actual problem statement. So I spent a lot of hours and days and weeks not to build. But to try to understand his processes. And I asked a very simple question to him. He said, I told him, What is the most mundane task that you do or task it to do every single day?

He starts listing them. And sometimes people don't realize the problems that they have. So I always say.

As a founder. I don't want to get into a lot of details because then I have an, you know, an idea about the difference between a founder and entrepreneur, 2 different things. They're not the same. Uh, an entrepreneur would be a founder, but not every founder is an entrepreneur that doesn't make anyone better than the other, but it's just different foundations and different mindsets. Um, but what I wanted to say is, I always, I know it's boring, it sounds a lot of, you know, not fun. But getting to the nitty gritty details of the boring process that is manual that is taking up a CEO's or business owner's time every single day. is hands on what I will focus on and spend more time on.

Looking at another aspect of your expertise, which is AI agents. There are questions regarding that as well. If our agents uses multiple APIs or LLM services, how should we manage like failures when one API becomes unavailable or reaches its limit? How do we efficiently use the API itself?

No, is okay, I'm just reading questions from copy, right? If I'm pronouncing the name correctly.

Yeah, if our agent uses multiple APIs or alum services, how should we manage failures when one API becomes unavailable or reaches its straight limit? There's a bunch of ways you can do that. Um, in terms of, uh, you know, fallbacks and so on and so forth. So. Again, um, you can, there's a lot of different ways how you do uh, air handling. Um, it's not uh, It's not things that are unheard of. Um, But then, When we talk about APIs, there are solutions for that when we talk about LNMs, it's a completely different ballgame, but they're related together. I know that our API's team always say, um, there's no AI without API. Right?

Because of the the term of both. APIs are very important. There's a lot of ways where you can safeguard rate limits and make sure that your APIs and LMs are always responsive. We can talk about that in a lot more detail. I can share with you some resources as well that I usually go back to to make sure that you have something in hand. But, um,

Um, when when someone comes and asks me that, I always, again, the boring question. Why are you getting into those limits? What are you trying to do? What is it that you're building? Is there a different way where you can approach the solution for that? Again, resources are not unlimited. Right? Resources unlimited, regardless of how big of a company are or how big of a tech provider you're using. Today we have a global challenge. There's not enough infrastructure AI. Not enough chips.

It's a very good problem to have, but then what? What do I do? Do I wait for it? Do I reserve it? Do I buy $1000000 worth of chips to make sure I have access to it? I try to find another way. Right? And there's a big shift that's going to potentially happen, which is how do you rely less on GPUs or more in CPUs back to the old days. And you build efficient LMs that can actually run and do the same thing on CPUs. There's a lot of things out there that talk about that.

Um, And that's what we try to do at Google as well, right? Yes, TPUs are amazing from Google. Um, they optimize a lot in terms of performance, cost, et cetera. But then we're solving, uh, and into, and temporary problem of LMs require that amount of inference and training. But we're also looking at how do you optimize LLMs? That's why you have different sizes and so on and so forth. Um, so I can share a bunch of best practises. And um, and then happy to discuss that offline as well in more detail. Or sure, like if you can share with us, I can share like the 40 guard team can share with the participants here as well. Via email and Slack, we'll update you on the resources.

One last question, which is there. Is there any criteria to apply for the partnership program? I think you mentioned that there is an, uh, email, like a link that they can go to. Can you provide this that link so that we can provide it to the chart as well? Oh, absolutely. So you can always...

I think I can, I can write into the podcast, right? You can just write it on the Qa section.

Guys, feel free to check it out, check out the criteria and apply for the partnership program. If you feature each other as well, if you have any questions. We have already pasted your LinkedIn as well. I'll just base your link again. Okay, so that people can reach out. And then someone asks, what gets the start of the more users? Is it UI or the performance?

I think again, boring answer, here is the problem that you're solving. Last example I know we're on time. Google dot com.

We used to remember a couple of years ago, we used to, when we go to, you know, present Google Tech because people

Didn't know Google Clown, but new Google.com. Um.

I don't think there's a single application in the world. That it's UI landing page, or even when you get into it, is as simple as possible as Google.com.

Before AI mode came to Google. You land on Google.com. You land on a white page. It's a white screen with one box.

Very basic. Nothing fancy. Very simple. But the engineering behind that one box. Is the problem that you're trying to solve for? Focus on the user. Performance is important. But when that happens, is going to be different. We once had an incident where. When I search for one product on google.com.

It would result, uh, the results would come completely unrelevant. It was about the time. And then what we started noticing is, How much people trusted Google, They actually started buying those products that they weren't interested in or they didn't even search for it. Because they did, oh, maybe because I've searched for this, this came up, this sounds relevant, or maybe it's not, but maybe it's a good product, et cetera. So there's a lot of iteration in terms of how do we think about the consumer behaviour? How do you think about their problems? What are they trying to solve for? What are we trying to solve for them? And how do we scale? Um, once you get to the go to market, you know, uh, product market fit and then uh, scale from there? I will stop looking at the questions because they're very tempting, uh handle oversnail to you.

Um and that's it. All right, and that's a wrap holiday session, by the way, let's give a huge thank you to Ahmed for sparing the time and also giving so much inspiration and guidance. Honestly, guys, there is so much gold in there. Like the presentation that he has given, the problem 1st mindset, knowing when to actually reach for AI versus when not to, and that whole framework for landing your 1st paying customer. In your use case, it would be getting it to the judges, showing the value to the judges, judges itself. That's the kind of thinking that separates projects that went from, you know, just projects, that just looked good. And Emma, right here, is a judge again in the Hackathon itself. He is not just a mentor. He is giving you guidance so that you guys excel and go and reach greater heights within the hackathon itself. So take those lessons and put them straight to your work in your bills. And thank you, Emma, that was fantastic by your end.

And before we close out, I just want to give another heads up, which is there, so people don't miss what's coming up next. We have got Tarek founder and CA of Narrative One, a genuine communication powerhouse, who's worked with the biggest names in media and helps scaled over 100s startups across the Mina region. So guys, please stick around. I'll be pasting the link in the chat as well. So that people who haven't registered yet, get a chance to come and join the talk as well. Just give me 12nd.

And there it is. I'll just spam it a bunch of times so that people do get access to it. And again, thank you so much, Ahmed. Thank you for sparing the time and it was great learning from you. We learned, especially I learned a lot from you. Thank you so much. App appreciate it. Thanks, everyone, and tune in to Thor session. It's going to be, it's going to be exciting. So much.

Thanks everyone. We're building, I would on the bye. Bye bye. The recording has been stopped. Thank you for joining. Goodbye.