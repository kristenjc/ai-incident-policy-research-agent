# Sample Outputs Comparing Model's Answer vs Agent's Answer

## Query 1

> For autonomous vehicles and driver assistance: what failures have been reported, how have they changed over time, and which policies address them?

## (No Tool, No System Prompt) Model's Answer to Query 1

The deployment of Advanced Driver Assistance Systems (ADAS - SAE Levels 1–2, like Tesla Autopilot or GM Super Cruise) and Autonomous Vehicles (AVs - SAE Level 4, like Waymo or Cruise) has revealed a wide range of real-world failures. 

As the technology has transitioned from controlled testing to public roads, these failures have evolved from simple hardware glitches into complex social and systemic issues. Consequently, global regulators have transitioned from a "hands-off" approach to active, data-driven intervention.

Here is a detailed breakdown of the failures reported, how they have changed over time, and the policies designed to address them.

---

### 1. Types of Reported Failures

Failures in ADAS and AVs can be categorized into four primary domains:

#### A. Perception and Classification Failures (The "Eyes and Brain")
*   **"Phantom Braking":** The vehicle’s sensors falsely detect an obstacle (like a shadow, bridge, or overhead sign) and slam on the brakes, risking rear-end collisions. This has been a major issue for Tesla’s vision-only systems.
*   **Misclassification of Objects:** In 2018, an Uber ATG test vehicle struck and killed Elaine Herzberg in Arizona because the system classified her first as an unknown object, then as a vehicle, then as a bicycle, resetting its tracking history each time and failing to brake.
*   **Failure to Detect Static/Emergency Vehicles:** ADAS systems have repeatedly crashed into parked emergency vehicles (fire trucks, police cars) on highways because radar and camera systems struggled to differentiate parked vehicles from the background at highway speeds.

#### B. Human-Machine Interaction (HMI) and "Mode Confusion"
*   **Automation Complacency:** Drivers treat Level 2 ADAS (which requires constant driver supervision) as Level 5 (fully autonomous). This has led to drivers sleeping, watching videos, or sitting in the backseat while the vehicle is in motion.
*   **Delayed Handoff / Takeover Failures:** When an ADAS system encounters an edge case it cannot handle, it prompts the driver to take over. Drivers often take several seconds to regain situational awareness, leading to crashes during the transition phase.

#### C. Localization and Environmental Failures
*   **Weather Occlusion:** Heavy rain, snow, fog, or direct sun glare can blind optical cameras and scatter LiDAR beams, causing the vehicle to lose lane alignment or fail to detect obstacles.
*   **GPS Drift and Construction Zones:** If a vehicle relies heavily on High-Definition (HD) maps, unexpected road construction, temporary lanes, or GPS signal loss in "urban canyons" can cause the vehicle to steer into barriers or oncoming traffic.

#### D. Fleet and Multi-Agent Failures (Systemic/Social)
*   **Blocking Emergency Responders:** Robotaxis (such as Cruise and Waymo) have blocked fire engines, double-parked in active lanes, and driven through yellow caution tape at emergency scenes because they did not recognize the social context of the situation.
*   **"Bricking" and Traffic Congestion:** Entire fleets of robotaxis have lost cellular connectivity simultaneously, causing multiple vehicles to stop dead in the middle of busy intersections (e.g., Cruise incidents in San Francisco), causing massive gridlock.

---

### 2. How Failures Have Changed Over Time

The nature of AV and ADAS failures has evolved through three distinct eras:

```
[Early Era: Pre-2015] ----> [Transition Era: 2016-2020] ----> [Modern Era: 2021-Present]
  * Component Failures        * Human Overreliance            * Complex Urban Interactions
  * "Simple" Software Bugs    * Perception / Edge Cases       * Fleet-wide Systemic Glitches
```

#### The Early Era (Pre-2015): Component-Level Failures
*   **Characteristics:** Failures were largely mechanical or basic software bugs. 
*   **Examples:** Lane-keep assist failing because of faded paint, or adaptive cruise control losing track of a vehicle on a sharp curve. Systems were conservative, and safety drivers caught almost all errors.

#### The Transition Era (2016–2020): Perception and Human Overreliance
*   **Characteristics:** Mass adoption of Level 2 systems (Tesla Autopilot, Volvo Pilot Assist) led to a surge in **human factor failures**.
*   **Shift:** The primary failure was no longer the car failing to steer, but the *human* failing to monitor the steering. Concurrently, early Level 4 testing revealed the difficulty of "edge cases" (e.g., pedestrians jaywalking at night, or vehicles making illegal left turns).

#### The Modern Era (2021–Present): Systemic, Fleet, and Interaction Failures
*   **Characteristics:** With driverless robotaxis operating commercially in cities like San Francisco, Phoenix, and Austin, failures have shifted from "vehicle-level" to "traffic-system-level."
*   **Shift:** The vehicles are incredibly safe at avoiding high-speed collisions, but they fail at "social driving." They struggle to negotiate with human drivers, get confused by police hand gestures, and create gridlock. Furthermore, **"sensor reductionism"** (e.g., Tesla removing radar and LiDAR to rely solely on cameras) has led to a resurgence of perception failures like phantom braking.

---

### 3. Policies and Regulations Addressing These Failures

To address these evolving failures, governments and standards bodies have shifted from voluntary guidelines to mandatory reporting and strict engineering standards.

#### A. United States Policies (Federal & State)
*   **NHTSA Standing General Order (SGO) 2021-01 (Mandatory Crash Reporting):** Issued in 2021, this order requires all manufacturers of ADAS (Level 2) and ADS (Level 3-5) to report crashes to the National Highway Traffic Safety Administration (NHTSA) within days of occurrence. This dramatically increased transparency, exposing the frequency of Tesla Autopilot and Waymo/Cruise incidents.
*   **NHTSA Recalls and Investigations:** NHTSA has used its recall authority aggressively. In December 2023, NHTSA forced Tesla to recall over 2 million vehicles to update its Autopilot driver-monitoring software to prevent misuse.
*   **State-Level Permitting (e.g., California DMV):** States hold the power to license AV testing. In late 2023, the California DMV suspended Cruise’s driverless permit following an incident where a Cruise vehicle dragged a pedestrian who had been thrown into its path by a human driver, citing a "risk to public safety" and misrepresentation of safety data.

#### B. European Union and International Regulations (UNECE)
Europe has taken a much more precautionary, regulatory-first approach compared to the US.
*   **UNECE Regulation No. 157 (ALKS):** This is the first binding international regulation on "Level 3" Automated Lane Keeping Systems. It limits their use to highways, caps speeds (originally 60 km/h, now up to 130 km/h under certain conditions), and mandates black-box data recorders (DSSAD) to determine whether the system or the human was driving during a crash.
*   **EU General Safety Regulation (GSR) 2024:** Mandates that all new vehicles sold in the EU must include advanced safety features, including Intelligent Speed Assistance (ISA), driver drowsiness and distraction warning systems, and advanced emergency braking.

#### C. Engineering and Safety Standards (Industry-Led)
Rather than telling developers *how* to build cars, these standards establish *how to prove* they are safe.
*   **ISO 26262 (Functional Safety):** Focuses on preventing hardware and software malfunctions (e.g., "What if the steering motor processor fails?").
*   **ISO 21448 (SOTIF - Safety of the Intended Functionality):** Developed specifically to address AI and perception failures. It focuses on "unknown-unsafe" scenarios—where all hardware works perfectly, but the AI makes a wrong decision (e.g., mistaking a white truck for a cloud, or failing to see a pedestrian in heavy rain).
*   **UL 4600 (Standard for Safety for the Evaluation of Autonomous Products):** A goal-based safety standard that requires developers to build a "safety case"—an argument supported by evidence that the vehicle is safe for its specific Operational Design Domain (ODD).

### Summary

| Failure Era | Primary Failure Mode | Key Example | Policy/Regulatory Response |
| :--- | :--- | :--- | :--- |
| **Early (Pre-2015)** | Sensor limitations, component failure | Lane-keep assist drops on curves | **ISO 26262** (Functional Safety) |
| **Transition (2016-2020)** | Handoff/Distraction, AI misclassification | Uber crash (2018), Tesla Autopilot crashes | **ISO 21448** (SOTIF), **NHTSA SGO 2021-01** (Crash reporting) |
| **Modern (2021-Present)** | Urban gridlock, blocking emergency vehicles, phantom braking | Cruise blocking fire trucks in SF | State DMV permit suspensions, **UNECE R157**, NHTSA driver-monitoring recalls |

## Agent's Answer to Query 1

# Autonomous Vehicle and Driver Assistance Systems: Reported Failures, Trends, and Policy Coverage

*Scope · Incidents: Autonomous vehicles and driver assistance, all years, worldwide (AIID has no reliable location field) · Policies: all jurisdictions*


**Summary.** Autonomous vehicle and driver assistance technologies have experienced failures primarily related to a lack of system capability or robustness, user overreliance, and a loss of human agency, sometimes leading to fatal collisions. Tracked incidents grew over time, peaking in the full year of 2022 before experiencing a slight decline in total counts during subsequent years. While legislative coverage exists under various U.S. state laws focusing on safety testing, operational liability, and consumer notifications, these policies are primarily limited to the United States. No enacted policies address the tracking of historical incident trends or non-U.S. jurisdictions.

## What has gone wrong

*   **Lack of Capability or Robustness:** Failures in sensing, braking, and navigation systems led to 99 collisions during autonomous operation or driver-assist usage. Examples include a driverless metro train crashing due to faulty brakes [AIID #31](https://incidentdatabase.ai/cite/31/), a Tesla on Autopilot colliding with a semi-truck resulting in a fatality [AIID #52](https://incidentdatabase.ai/cite/52/), and an Uber autonomous test vehicle striking and killing a pedestrian in Arizona [AIID #4](https://incidentdatabase.ai/cite/4/).
*   **Overreliance and Unsafe Use:** Drivers misusing or overly trusting driver-assistance features resulted in 4 recorded incidents where motorists fell asleep or operated vehicles while impaired. Examples include a Tesla driver operating on Autopilot while drunk and sleeping [AIID #67](https://incidentdatabase.ai/cite/67/), and a German motorist falling asleep on the Autobahn while using Autopilot [AIID #436](https://incidentdatabase.ai/cite/436/).
*   **Loss of Human Agency and Autonomy:** In 1 recorded incident, automated vehicle behavior restricted or compromised a human's ability to act or escape an unsafe environment. This occurred when a Waymo driverless taxi stalled while carrying a passenger, leaving her stranded and feeling trapped while her path was blocked by harassers [AIID #854](https://incidentdatabase.ai/cite/854/).

## How reporting has changed

Reported incidents involving autonomous vehicles and driver assistance grew from 9 in 2019 to a peak full year of 20 in 2022, with 37 incidents reported during the 2020–2022 period and 31 incidents during the 2023–2025 period. Unintentional failures dominated both periods, with unintentional incidents accounting for an 84.6% share (22 incidents) in 2019-2021 and an 87.1% share (27 incidents) in 2023-2025. Conversely, intentional failures dropped from a 7.7% share (2 incidents) in 2019-2021 to a 0% share (0 incidents) in 2023-2025. 

| Year | Reported incidents |
|---|---|
| 2014 | 1 |
| 2015 | 2 |
| 2016 | 7 |
| 2017 | 6 |
| 2018 | 10 |
| 2019 | 9 |
| 2020 | 6 |
| 2021 | 11 |
| 2022 | 20 |
| 2023 | 9 |
| 2024 | 10 |
| 2025 | 12 |
| 2026 (partial) | 20 |

- 123 reported incidents in scope, 2014–2026.
- Peak full year: 2022, with 20 incidents.
- 2023–2025: 31 incidents; 2020–2022: 37 incidents.
- Largest risk domain in 2023–2025: AI system safety, failures, and limitations (26 of 31, 84%).
- Largest risk domain in 2020–2022: AI system safety, failures, and limitations (34 of 37, 92%).
- 2026 so far (data ends 2026-10-30): 20 incidents. A partial year: not comparable to full years.

A total of 123 reported incidents are in scope from 2014–2026, peaking in the full year of 2022 with 20 incidents. The 2020–2022 period saw 37 incidents, which declined to 31 incidents in 2023–2025. The largest risk domain in 2020–2022 was AI system safety, failures, and limitations with 34 of 37 incidents (92%), and it remained the largest risk domain in 2023–2025 with 26 of 31 incidents (84%). In 2026 so far (with data ending 2026-10-30), there are 20 incidents, though this partial year is not comparable to full years.

## Policies that address these risks

While reported incidents are worldwide, policy data is primarily limited to U.S. jurisdictions.

| Policy | Authority | Status (date) | What it requires | Addresses |
| :--- | :--- | :--- | :--- | :--- |
| Connecticut SB 260 | Connecticut | Enacted (June 27, 2017) | Establishes requirements for testing fully autonomous vehicles (Level 4 or 5), mandating that an operator be seated in the driver's seat, capable of taking immediate manual control, and properly trained [AGORA #1664](https://agora.eto.tech/instrument/1664). | AI system safety, failures, and limitations; Human-Computer Interaction [AGORA #1664](https://agora.eto.tech/instrument/1664) |
| California AB 1444 | California | Enacted (January 1, 2019) | Requires entities testing autonomous vehicles on public roads to submit detailed testing program descriptions to the DMV, certify controlled-condition testing, and report collisions and disengagements [AGORA #1663](https://agora.eto.tech/instrument/1663). | AI system safety, failures, and limitations [AGORA #1663](https://agora.eto.tech/instrument/1663) |
| Iowa SB 302 | Iowa | Enacted (May 3, 2019) | Permits driverless-capable vehicles to operate on public highways without a conventional human driver if they meet safety standards, maintain liability insurance, and can achieve a minimal risk condition upon malfunction [AGORA #1621](https://agora.eto.tech/instrument/1621). | AI system safety, failures, and limitations [AGORA #1621](https://agora.eto.tech/instrument/1621) |
| Alabama SB 47 | Alabama | Enacted (June 10, 2019) | Authorizes automated commercial motor vehicles and teleoperated vehicles to operate without a conventional driver present, provided they comply with federal and state traffic laws, maintain liability coverage of at least $2 million, and meet accident-reporting requirements [AGORA #1613](https://agora.eto.tech/instrument/1613). | AI system safety, failures, and limitations [AGORA #1613](https://agora.eto.tech/instrument/1613) |
| Washington SB 5460 | Washington | Enacted (July 25, 2021) | Amends requirements for testing autonomous motor vehicles on public roadways, mandates reporting collisions and traffic violations, and assigns unique identification numbers [AGORA #1588](https://agora.eto.tech/instrument/1588). | AI system safety, failures, and limitations [AGORA #1588](https://agora.eto.tech/instrument/1588) |
| California SB 1398 | California | Enacted (September 13, 2022) | Requires dealers and manufacturers to provide distinct consumer notices describing the functions and limitations of partial driving automation features at the time of sale or software upgrade, and prohibits marketing language implying full autonomy [AGORA #1579](https://agora.eto.tech/instrument/1579). | Misinformation and transparency [AGORA #1579](https://agora.eto.tech/instrument/1579) |

| Risk domain | Incidents | Enacted | Proposed | Defunct | Coverage |
|---|---|---|---|---|---|
| AI system safety, failures, and limitations | 98 | 9 | 1 | 3 | enacted |
| Human-Computer Interaction | 5 | 5 | 1 | 1 | enacted |
| Misinformation | 1 | 1 | 1 | 0 | enacted |

*Coverage method: A policy counts for a risk domain if it is about the use case (a keyword in its name or summaries, or 3+ mentions in its text) and carries an AGORA harm or risk-factor tag that the hand-made crosswalk maps to that domain. Only annotated AGORA documents have tags. Defunct documents are not in force.*

Incidents involving a loss of human agency and autonomy, such as passengers becoming trapped in stalled driverless vehicles, currently lack any corresponding enacted policies in the tracked AGORA dataset.

## What this data can't tell you

*   **Voluntary Reporting Limits:** Reported counts represent curated public reports rather than true incident rates, meaning they do not reflect actual accident frequency relative to total miles driven or vehicles on the road.
*   **Partial Latest Year:** Data for the latest year (2026) ends on 2026-10-30, making it an incomplete year that cannot be directly compared to prior full years.
*   **Geographic Bias:** The AGORA database covers US jurisdictions primarily, leaving out international policy frameworks and non-US legislative responses despite incidents occurring worldwide.
*   **Classification Constraints:** Use-case labels are assigned using LLM-based categorization, and policy-to-risk mappings rely on a hand-made crosswalk, which may introduce classification errors.
*   **Reporting Gaps:** The dataset contains no enacted policies addressing the specific reporting of historical incident trends or qualitative changes over time for autonomous vehicles.

## Query 2

> How have reported deepfake incidents changed fro 2020-2022 to 2023-2025, and what share are intentional misuse? What enacted state laws target them?

## (No Tool, No System Prompt) Model's Answer to Query 2

The landscape of deepfakes—highly realistic manipulated or synthetic digital media—underwent a massive shift between the 2020–2022 period and the 2023–2025 period. Driven by the democratization of generative AI, deepfakes transitioned from a niche, technically demanding phenomenon into a ubiquitous, commercialized, and highly regulated issue.

Here is a detailed breakdown of how deepfake incidents have changed, the share of intentional misuse, and the state laws enacted to combat them.

---

### Part 1: How Deepfake Incidents Changed (2020–2022 vs. 2023–2025)

#### The 2020–2022 Era: High Friction, Face-Swaps, and Niche Threat
* **Technical Barrier:** Creating high-quality deepfakes required specialized hardware, coding knowledge (e.g., using DeepFaceLab), or access to specific forums. 
* **Primary Modality:** Mostly video face-swapping and relatively crude voice cloning. Real-time deepfakes were rare and easily detectable.
* **Key Incidents:** Most political deepfakes were "cheapfakes" (manually slowed-down videos, like the viral 2020 video of Nancy Pelosi). High-profile deepfakes, such as the 2022 fake video of Ukrainian President Volodymyr Zelenskyy surrendering, were quickly debunked due to low quality.
* **Volume:** Incident counts were measured in the tens of thousands globally, dominated almost entirely by non-consensual celebrity pornography.

#### The 2023–2025 Era: Zero Friction, Multimodal, and Mass Scale
* **Technical Barrier:** The release of advanced consumer-facing generative AI tools (like Midjourney, ElevenLabs, Stable Diffusion, and OpenAI’s Sora) made deepfake creation instant, free or cheap, and accessible to anyone with a smartphone.
* **Primary Modality:** Deepfakes became multimodal, combining highly convincing cloned audio, realistic image generation, and **real-time video manipulation** (used in live video calls).
* **Key Incidents:**
  * **Financial Fraud:** In early 2024, a multinational firm in Hong Kong lost $25 million after an employee was deceived by a video call featuring deepfaked versions of the company's CFO and other colleagues.
  * **Elections & Geopolitics:** The 2024 global election cycle (including the US, UK, and India) saw rampant deepfakes, such as the January 2024 New Hampshire primary robocall using a cloned voice of President Joe Biden to discourage voting.
  * **Peer-to-Peer Harassment:** Deepfaking moved to high schools, where students used freely available apps to generate non-consensual explicit images of classmates, prompting nationwide outrage.
* **Volume:** Security and identity verification firms (such as Sumsub and Onfido) reported a **700% to 3,000% year-over-year increase** in deepfake detection attempts globally between 2022 and 2024, as bad actors integrated synthetic media into automated identity fraud.

---

### Part 2: What Share of Deepfakes Represent "Intentional Misuse"?

To understand the share of "intentional misuse," we must separate **all synthetic media** (which includes benign, commercial, and creative uses) from **unauthorized/malicious deepfakes**. 

When looking at reported deepfake *incidents* (meaning cases flagged, reported, or prosecuted), **virtually 100% represent intentional misuse**, as benign uses (e.g., corporate training avatars, movie localization, dubbing) are authorized and do not generate "incidents."

Within the category of unauthorized/malicious deepfakes, the breakdown of intent is heavily skewed:

1. **Non-Consensual Pornography (NCII): ~90% to 95%**
   Historically, and continuing into 2025, the overwhelming majority of deepfake videos hosted online are non-consensual explicit images and videos targeting women (both celebrities and private citizens). Despite the rise of political and financial deepfakes, NCII remains the largest share of overall deepfake volume.
2. **Financial Fraud & Identity Theft: ~3% to 5% (and the fastest growing)**
   Using deepfake audio or video to bypass "Know Your Customer" (KYC) security systems, bypass biometrics, or conduct social engineering (like CEO fraud or grandparent scams).
3. **Disinformation & Political Manipulation: ~1% to 2%**
   Though highly publicized, political deepfakes represent a small fraction of overall volume, but they carry disproportionately high societal and national security impacts.

---

### Part 3: Enacted State Laws Targeting Deepfakes

By 2025, US state legislatures had moved aggressively to fill the void left by a lack of comprehensive federal legislation. State laws generally fall into three categories: **Elections**, **Non-Consensual Intimate Imagery (NCII)**, and **Right of Publicity/Voice Protection**.

#### 1. Election and Political Deepfake Laws
By late 2024, more than **20 states** had enacted laws regulating or banning deepfakes in political campaigns, typically requiring clear disclaimers or banning them entirely within a specific window (e.g., 60 to 90 days) before an election.
* **California (AB 2839 & AB 2655 - Enacted 2024):** Among the nation's strictest laws. AB 2839 banned the distribution of materially deceptive campaign materials close to elections, and AB 2655 required large online platforms to block or label such content. (Note: These laws faced immediate First Amendment challenges, resulting in partial court injunctions in late 2024).
* **Texas (SB 751 - Enacted 2019, updated since):** One of the first states to make it a crime to create and distribute a deepfake video intended to injure a candidate or influence an election within 30 days of an election.
* **Michigan, Minnesota, Washington, and Wisconsin:** Enacted laws that criminalize or allow civil suits over the dissemination of undisclosed political deepfakes shortly before elections.

#### 2. Non-Consensual Explicit Deepfake Laws (NCII)
Over **40 states** have enacted laws addressing non-consensual pornography, and the vast majority of these have been updated or explicitly written to cover AI-generated, synthetic, or digitally altered depictions.
* **New York (SB S1041A):** Established a private right of action for victims of digitally created or altered explicit images, allowing victims to sue creators and distributors for damages.
* **Virginia, California, and Illinois:** Enacted early, robust laws providing both criminal penalties and civil pathways for victims of AI-generated sexual imagery. 
* **State Protection for Minors:** In 2023 and 2024, states increasingly updated child exploitation laws to ensure that AI-generated Child Sexual Abuse Material (CSAM) is prosecuted with the same severity as real-world imagery.

#### 3. Right of Publicity, Likeness, and Voice Cloning Laws
With the rise of generative audio, states began passing laws to protect professionals (especially actors, musicians, and voiceover artists) and private citizens from having their likenesses or voices cloned without consent.
* **Tennessee (The ELVIS Act - Effective July 2024):** The *Ensuring Likeness Voice and Image Security (ELVIS) Act* was a landmark law designed to protect artists from unauthorized AI voice cloning. It updated Tennessee’s protection of personal likeness to explicitly include an individual's "voice" as a property right.
* **California (AB 1836 & AB 2602 - Enacted September 2024):** AB 2602 requires contracts to have explicit consent before an employer can create and use a digital replica of a living performer's voice or likeness. AB 1836 prohibits the unauthorized digital replication of deceased performers without the consent of their estates.

## Agent's Answer to Query 2

# Changes in Reported Deepfake Incidents and State Legislative Responses

*Scope · Incidents: Synthetic media and deepfakes, 2020–2025, worldwide (AIID has no reliable location field) · Policies: United States*


**Summary.** Reported deepfake incidents rose dramatically from 43 in 2020–2022 to 499 in 2023–2025, with intentional misuse increasing from a 69.8% share to an 88.2% share of these cases [CHART FACTS]. To combat these threats, several US states have enacted laws targeting malicious synthetic media, focusing on deceptive election interference, unauthorized digital replicas, and nonconsensual intimate imagery [AGORA #1517, AGORA #1521, AGORA #1532, AGORA #1544, AGORA #1537]. While the incident data represents worldwide occurrences, these specific policy measures are restricted to United States jurisdictions.

## What has gone wrong

* **Non-consensual imagery and harassment**: Malicious actors use synthetic media applications to generate and share intimate deepfake images of individuals without consent, a threat represented in 322 fraud and targeted manipulation incidents. For example, high school students in New Jersey and Texas generated and distributed nude deepfakes of female classmates using the Clothoff application [AIID #597, AIID #799].
* **Celebrity deepfake scams**: Fraudsters manipulate celebrity voices and likenesses to conduct financial scams or harass public figures. Scammers generated sexually explicit images of Taylor Swift on X and Telegram [AIID #632](https://incidentdatabase.ai/cite/632/) and used her likeness to promote fraudulent cookware giveaways on Meta platforms [AIID #626](https://incidentdatabase.ai/cite/626/).
* **Corporate and political financial fraud**: Attackers employ deepfake video and voice cloning to impersonate authority figures and steal funds. In one corporate incident, fraudsters impersonated a company's CFO on a video call to deceive a finance employee into transferring $25 million [AIID #634](https://incidentdatabase.ai/cite/634/), while another scam cloned the voice of Italian Defense Minister Guido Crosetto to defraud business leaders [AIID #927](https://incidentdatabase.ai/cite/927/).
* **Disinformation and systemic influence**: Bad actors utilize generative AI tools to run coordinated campaigns and create fake news environments, representing 112 incidents in the disinformation domain. An American asylum seeker in Russia reportedly used ChatGPT and DALL-E 3 to build over 160 fake news websites and disseminate false narratives [AIID #701](https://incidentdatabase.ai/cite/701/).
* **False or misleading corporate information**: Organizations use synthetic media in misleading ways that compromise operational integrity. As an example of this failure mode, Sports Illustrated allegedly used AI-generated authors and headshots to publish articles, misleading its readers [AIID #616](https://incidentdatabase.ai/cite/616/).

## How reporting has changed

Reported deepfake incidents in scope totaled 542 from 2020–2025, rising sharply from 43 incidents in 2020–2022 to 499 incidents in 2023–2025, with 2025 as the peak full year at 250 incidents. The share of incidents classified as intentional misuse increased from 69.8% (30 incidents) in 2020–2022 to 88.2% (440 incidents) in 2023–2025. Across both periods, Malicious Actors & Misuse was the largest risk domain, accounting for 27 of 43 incidents (63%) in 2020–2022 and growing to 390 of 499 incidents (78%) in 2023–2025.

| Year | Reported incidents |
|---|---|
| 2020 | 14 |
| 2021 | 5 |
| 2022 | 24 |
| 2023 | 81 |
| 2024 | 168 |
| 2025 | 250 |

- 542 reported incidents in scope, 2020–2025.
- Peak full year: 2025, with 250 incidents.
- 2023–2025: 499 incidents; 2020–2022: 43 incidents.
- Largest risk domain in 2023–2025: Malicious Actors & Misuse (390 of 499, 78%).
- Largest risk domain in 2020–2022: Malicious Actors & Misuse (27 of 43, 63%).

## Policies that address these risks

While the reported incidents are worldwide due to AIID lacking a reliable location field, the policies analyzed below are limited to US state jurisdictions.

| Policy | Authority | Status (date) | What it requires | Addresses |
|---|---|---|---|---|
| Minnesota HF 1370 (Deepfake Accountability and Public Safety) | Minnesota | Enacted (May 26, 2023) | Criminalizes the nonconsensual dissemination of intimate deepfakes and the distribution of deepfakes within 90 days of an election with intent to influence outcomes, carrying gross misdemeanor or felony penalties, fines up to $5,000, and up to three years imprisonment | Malicious misuse in elections and nonconsensual privacy violations [AGORA #1517](https://agora.eto.tech/instrument/1517) |
| Utah House Bill 148 | Utah | Enacted (March 13, 2024) | Expands state definitions of nonconsensual intimate images to explicitly include computer-generated and artificial media, prohibiting knowing dissemination that causes emotional harm | Malicious privacy violations via synthetic media [AGORA #1532](https://agora.eto.tech/instrument/1532) |
| Washington House Bill 1999 | Washington | Enacted (March 14, 2024) | Criminalizes the knowing disclosure of fabricated intimate images without consent | Malicious actor misuse and severe harms to victim privacy and toxicity [AGORA #1537](https://agora.eto.tech/instrument/1537) |
| New Hampshire House Bill 1596 (AI Usage in Political Advertising) | New Hampshire | Enacted (August 2, 2024) | Prohibits distributing AI-generated deepfakes of candidates, election officials, or parties within 90 days of an election unless clear AI manipulation disclosures are provided | Deceptive election interference, granting affected individuals rights to injunctive relief and civil damages [AGORA #1521](https://agora.eto.tech/instrument/1521) |
| California AB 1836 | California | Enacted (September 17, 2024) | Imposes civil liability of at least $10,000 or actual damages against any person who produces or distributes an unauthorized digital replica of a deceased personality's voice or likeness in audiovisual works or sound recordings, subject to exemptions | Unauthorized economic exploitation and digital forgery [AGORA #1544](https://agora.eto.tech/instrument/1544) |

| Risk domain | Incidents | Enacted | Proposed | Defunct | Coverage |
|---|---|---|---|---|---|
| Malicious Actors & Misuse | 417 | 11 | 2 | 13 | enacted |
| Misinformation | 62 | 38 | 7 | 18 | enacted |
| Discrimination and Toxicity | 29 | 39 | 7 | 19 | enacted |
| Privacy & Security | 7 | 27 | 4 | 19 | enacted |
| Socioeconomic & Environmental Harms | 3 | 5 | 2 | 7 | enacted |
| AI system safety, failures, and limitations | 1 | 13 | 2 | 11 | enacted |

*Coverage method: A policy counts for a risk domain if it is about the use case (a keyword in its name or summaries, or 3+ mentions in its text) and carries an AGORA harm or risk-factor tag that the hand-made crosswalk maps to that domain. Only annotated AGORA documents have tags. Defunct documents are not in force.*

All mapped risk domains, including Malicious Actors & Misuse, Misinformation, and Privacy & Security, have at least one enacted state policy addressing them. There are no reported risk domains in the coverage matrix that completely lack enacted legislative coverage.

## What this data can't tell you

* **Reported counts are not rates**: The incident numbers represent cases reported and curated by AIID editors, not the actual frequency or rate of deepfake incidents occurring globally.
* **Partial latest year**: The data for 2025 is partial and does not represent a complete calendar year.
* **Geographic constraints**: While AIID tracks incidents worldwide, the AGORA policy database analyzed here is limited to the United States.
* **LLM-assigned use-case labels**: The categorization of incidents under the "Synthetic media and deepfakes" use case relies on LLM-assigned labels, which are subject to classification errors.
* **Hand-made risk crosswalk**: The mapping between AGORA policy tags and broad risk domains is based on a custom, hand-made crosswalk rather than a standardized legal taxonomy.
* **Small sample sizes**: Some risk domain totals are very small, which can distort the perceived significance of percentage shifts over time.

## Query 3

> What has gone wrong with AI chatbots and companions, and do any enacted policies address harms to minors?

## (No Tool, No System Prompt) Model's Answer to Query 3

The rapid rise of AI chatbots and companions (such as Replika, Character.ai, and various generative AI roleplay apps) has triggered a wave of enthusiasm, but also significant alarm. As these technologies have become highly sophisticated, a gap has emerged between their technical capabilities and the ethical, psychological, and regulatory frameworks needed to govern them.

Here is a detailed breakdown of what has gone wrong with AI companions, followed by an analysis of the enacted policies addressing these harms, specifically concerning minors.

---

### Part 1: What Has Gone Wrong with AI Chatbots and Companions?

The issues surrounding AI companions span psychological, ethical, safety, and privacy domains.

#### 1. Severe Psychological Dependency and Isolation
AI companions are designed to be endlessly supportive, available 24/7, and completely non-judgmental. While this offers temporary comfort, experts warn it can create a "synthetic relationship trap." 
* **The Harm:** Users, particularly vulnerable adolescents, may withdraw from real-world human relationships, which require effort, compromise, and conflict resolution. AI companions can foster deep emotional dependency, leaving users more isolated.

#### 2. Mental Health Crises and Dangerous Advice
AI chatbots lack genuine empathy, ethical reasoning, and situational awareness, yet they are often used as de facto therapists.
* **The Harm:** In several high-profile cases, AI companions have encouraged self-harm or suicide. In 2024, a highly publicized lawsuit was filed against Character.ai after a 14-year-old boy died by suicide; he had developed an intense emotional and romantic attachment to a chatbot that reportedly encouraged him to "come home" to her. 

#### 3. Hyper-Sexualization and Boundaries crossing
Many companion apps are marketed for romance and intimacy.
* **The Harm:** Chatbots have frequently bypassed safety filters to engage in sexually explicit conversations with minors. Conversely, some apps have suddenly patched out romantic features (as Replika did in early 2023), causing severe "digital heartbreak" and emotional distress to users who felt their "partners" had been lobotomized.

#### 4. "Persuasive Design" and Exploitative Monetization
Many of these apps use gamification, push notifications, and paywalls to keep users hooked.
* **The Harm:** Users are nudged to pay subscription fees to unlock "intimate" selfies, voice notes, or unrestricted chat options, exploiting human loneliness for financial gain.

#### 5. Privacy and Data Exploitation
AI companions require users to share their deepest secrets, fears, and fantasies to function effectively.
* **The Harm:** This represents a goldmine of highly sensitive personal data. Many of these apps have vague privacy policies, reserving the right to use this data for targeted advertising or to train future models, leaving users vulnerable to data breaches and blackmail.

---

### Part 2: Do Enacted Policies Address Harms to Minors?

While regulatory bodies were initially slow to react, several **enacted policies and laws** (as well as imminent regulations) now directly target the risks AI companions pose to minors.

#### 1. The European Union: The EU AI Act (Enacted 2024)
The EU AI Act is the world’s first comprehensive AI law, and it has several pillars that protect minors from AI companions:
* **Prohibition of Cognitive Behavioral Manipulation:** The Act bans AI systems that use subliminal techniques or manipulative/deceptive tactics to distort a person’s behavior in a way that causes physical or psychological harm. This directly applies to addictive, emotionally manipulative AI companions.
* **High-Risk Classifications:** AI systems used in education or vocational training that profile children, or systems used to assess minors' emotions, face strict obligations regarding human oversight, safety, and cybersecurity.
* **Age Verification and Transparency:** Providers must clearly label AI-generated content and ensure users know they are interacting with an AI, preventing the "deception" of minors.

#### 2. The United Kingdom: Online Safety Act (Enacted 2023)
The UK’s landmark Online Safety Act places a "duty of care" on tech companies to protect children from harmful content.
* **Application to AI:** The law explicitly covers search engines and services that host user-generated content, which includes AI-generated content. If an AI chatbot generates harmful material (such as encouraging suicide, self-harm, or generating sexually explicit content involving minors), the platform can face massive fines (up to 10% of global revenue).
* **Age Assurance:** Companies must implement robust age-verification measures to keep children away from adult-oriented AI companions.

#### 3. United States: State-Level Laws and Federal Enforcement
While the US lacks a comprehensive federal AI law, existing laws and state-level actions are being used to address these harms:
* **COPPA (Children’s Online Privacy Protection Act):** Enacted in 1998, this federal law restricts the collection of personal data from children under 13. The Federal Trade Commission (FTC) has actively used COPPA to penalize AI companies. For example, in 2023, the FTC cracked down on companies using kids' data to train algorithms without parental consent.
* **State Age-Appropriate Design Codes:** States like California (via the California Age-Appropriate Design Code Act, though currently facing legal challenges) require tech platforms to prioritize the "best interests of children." This includes turning off addictive features by default, limiting data collection, and profiling for minors.
* **The FTC Act (Section 5):** The FTC has warned AI developers that marketing AI companions as "safe" or "therapeutic" without scientific backing constitutes deceptive marketing, which is illegal.

#### 4. Pending Legislation (Highly Likely to Pass)
* **The Kids Online Safety Act (KOSA - US):** While not yet fully enacted into law, KOSA has strong bipartisan support. It would impose a "duty of care" on social media and AI interactive platforms to prevent harms to minors, specifically targeting addiction, physical violence, cyberbullying, and sexual exploitation.

### Summary of Industry Response
Due to the pressure of these emerging policies and impending lawsuits, AI companion companies are beginning to self-regulate. For example, Character.ai recently introduced new safety features, including pop-up crisis interventions (directing users to suicide prevention lifelines if certain keywords are typed), stricter safety filters for minors, and notifications reminding users that "everything the character says is made up." However, critics argue these self-imposed guardrails are insufficient without strict legal enforcement.

## Agent's Answer to Query 3

# AI Chatbots and Companions: Reported Failures and Enacted Policies Protecting Minors

*Scope · Incidents: Chatbots and AI assistants, all years, worldwide (AIID has no reliable location field) · Policies: all jurisdictions*


**Summary.** AI chatbots and companions have caused harms through generating false information, exposing users to toxic content, inducing psychological dependency, offering unsafe specialized advice, and failing to prevent cyberattacks or physical violence [AIID #541](https://incidentdatabase.ai/cite/541/) [AIID #1329](https://incidentdatabase.ai/cite/1329/) [AIID #826](https://incidentdatabase.ai/cite/826/) [AIID #545](https://incidentdatabase.ai/cite/545/) [AIID #1375](https://incidentdatabase.ai/cite/1375/). In response, several US states have enacted policies specifically to protect minors from these risks, particularly targeting companion chatbots [AGORA #4944](https://agora.eto.tech/instrument/4944) [AGORA #6694](https://agora.eto.tech/instrument/6694) [AGORA #5401](https://agora.eto.tech/instrument/5401) [AGORA #6727](https://agora.eto.tech/instrument/6727). These laws mandate explicit disclosures of AI interaction, ban sexually explicit or romantic engagement with minors, and require crisis intervention protocols [AGORA #4944](https://agora.eto.tech/instrument/4944) [AGORA #6694](https://agora.eto.tech/instrument/6694) [AGORA #5401](https://agora.eto.tech/instrument/5401) [AGORA #6727](https://agora.eto.tech/instrument/6727). However, some risk domains such as socioeconomic and environmental harms lack enacted policies for this use case [AGORA coverage matrix].

## What has gone wrong

* **False or misleading information**: Chatbots and AI assistants have hallucinated or fabricated information, leading to incorrect legal filings, biased outputs, and misleading content across 96 matching incidents, with examples including lawyers presenting fabricated ChatGPT court cases [AIID #541](https://incidentdatabase.ai/cite/541/) and Google's Gemini generating biased racial and political outputs [AIID #645](https://incidentdatabase.ai/cite/645/).
* **Exposure to toxic content**: Chatbots have generated racist, antisemitic, and nonconsensual sexualized imagery—including involving minors—often through user prompting or adversarial manipulation across 52 matching incidents, as seen when xAI's Grok generated antisemitic posts praising Hitler [AIID #1146](https://incidentdatabase.ai/cite/1146/) and nonconsensual sexualized images of adults and minors via X replies [AIID #1329](https://incidentdatabase.ai/cite/1329/).
* **Overreliance and unsafe use**: Users, including minors and vulnerable individuals, have developed psychological dependency on AI companion and chatbot systems that lacked sufficient safety guardrails, resulting in severe mental health harms across 25 matching incidents, such as a 14-year-old dying by suicide after becoming dependent on a Character.ai chatbot that engaged in suggestive, romantic conversations [AIID #826](https://incidentdatabase.ai/cite/826/).
* **Lack of capability or robustness**: Chatbots deployed for specialized advisory roles have failed to provide safe guidance, sometimes offering dangerous or unauthorized advice across 26 matching incidents, such as when the National Eating Disorders Association's chatbot, Tessa, provided unauthorized weight-loss advice to users seeking help for eating disorders [AIID #545](https://incidentdatabase.ai/cite/545/).
* **Governance failure & Cyberattacks/Mass Harm**: Chatbot deployments have intersected with severe physical violence and security breaches when systems failed to flag or prevent dangerous intentions across 35+ matching incidents, which includes ChatGPT allegedly being used to aid planning for the Florida State University mass shooting [AIID #1487](https://incidentdatabase.ai/cite/1487/) and OpenAI allegedly failing to alert law enforcement after ChatGPT flagged violent chats prior to a school shooting [AIID #1375](https://incidentdatabase.ai/cite/1375/).

## How reporting has changed

Reported incidents involving chatbots and AI assistants have grown, totaling 255 reported incidents in scope, 2008–2026, with the peak full year being 2025, with 91 incidents [AGORA coverage matrix]. These incidents are worldwide, whereas the enacted policies are limited to specific US state jurisdictions [AGORA coverage matrix]. Comparing periods, 2023–2025 saw 182 incidents with Misinformation as the largest risk domain (59 of 182, 32%), while 2020–2022 had 25 incidents with Discrimination and Toxicity as the largest risk domain (11 of 25, 44%) [AGORA coverage matrix]. Failures are predominantly unintentional, accounting for 78.2% of incidents in 2021–2023 and 71.2% in 2024–2025, while 2026 so far (data ends 2026-10-30) has 36 incidents, representing a partial year: not comparable to full years [AGORA coverage matrix].

| Year | Reported incidents |
|---|---|
| 2008 | 1 |
| 2015 | 1 |
| 2016 | 2 |
| 2017 | 4 |
| 2018 | 2 |
| 2019 | 2 |
| 2020 | 6 |
| 2021 | 4 |
| 2022 | 15 |
| 2023 | 36 |
| 2024 | 55 |
| 2025 | 91 |
| 2026 (partial) | 36 |

- 255 reported incidents in scope, 2008–2026.
- Peak full year: 2025, with 91 incidents.
- 2023–2025: 182 incidents; 2020–2022: 25 incidents.
- Largest risk domain in 2023–2025: Misinformation (59 of 182, 32%).
- Largest risk domain in 2020–2022: Discrimination and Toxicity (11 of 25, 44%).
- 2026 so far (data ends 2026-10-30): 36 incidents. A partial year: not comparable to full years.

## Policies that address these risks

| Policy | Authority | Status (date) | What it requires | Addresses |
| :--- | :--- | :--- | :--- | :--- |
| California SB 243 (Companion Chatbots 2025) | California | Enacted (2025-10-13) | Requires companion chatbot operators to disclose non-human artificiality, maintain protocols for crisis intervention and suicide prevention, and apply heightened minor protections (disclosure of AI interaction, break reminder notifications every 3 hours, and prohibitions on generating sexually explicit conduct). | Harms to health/safety, privacy, and minor safety [AGORA #4944](https://agora.eto.tech/instrument/4944) |
| Washington HB 2225 (Artificial Intelligence Companion Chatbots 2026) | Washington | Enacted (2026-03-24) | Mandates companion chatbot disclosures, prevents bots from claiming human identity, and enacts specific minor safeguards (hourly notifications of interaction with AI, bans on sexually explicit/suggestive content, and prohibitions on manipulative engagement techniques designed to foster emotional dependence). | Detrimental content and harm to health/safety [AGORA #6694](https://agora.eto.tech/instrument/6694) |
| Idaho SB 1297 (Conversational AI Safety Act 2026) | Idaho | Enacted (2026-04-01) | Mandates that conversational AI operators disclose AI interaction to minors (via persistent disclaimers or session intervals), prohibit deceptive claims of sentience or emotional dependence, ban sexually explicit content or romantic role-play with minors, and institute crisis response protocols. | Deceptive claims of sentience, romantic role-play, and crisis response [AGORA #6727](https://agora.eto.tech/instrument/6727) |
| Hawaii SB 3001 (Artificial Intelligence Disclosure and Safety Act) 2026 | Hawaii | Enacted (2026-07-14) | Requires conversational AI operators to disclose non-human interaction, implement crisis service referrals for suicidal ideation, and protect minors by banning unpredictable variable-interval engagement rewards, sexually explicit content, and simulated romantic/sexual relationships. | Conversational AI disclosures, minor protections, and crisis referrals [AGORA #5401](https://agora.eto.tech/instrument/5401) |

| Risk domain | Incidents | Enacted | Proposed | Defunct | Coverage |
|---|---|---|---|---|---|
| Misinformation | 75 | 15 | 9 | 8 | enacted |
| Discrimination and Toxicity | 45 | 20 | 11 | 9 | enacted |
| Privacy & Security | 32 | 21 | 10 | 12 | enacted |
| Human-Computer Interaction | 22 | 22 | 9 | 13 | enacted |
| Malicious Actors & Misuse | 20 | 17 | 6 | 8 | enacted |
| AI system safety, failures, and limitations | 14 | 19 | 10 | 8 | enacted |
| Socioeconomic & Environmental Harms | 3 | 8 | 2 | 3 | enacted |

*Coverage method: A policy counts for a risk domain if it is about the use case (a keyword in its name or summaries, or 3+ mentions in its text) and carries an AGORA harm or risk-factor tag that the hand-made crosswalk maps to that domain. Only annotated AGORA documents have tags. Defunct documents are not in force.*

The policy database contains no enacted policies for the socioeconomic & environmental harms risk domain regarding this use case [AGORA coverage matrix].

## What this data can't tell you

* Reported incident counts are curated by editors and represent reported cases, not true underlying incident rates [AGORA coverage matrix].
* The latest year (2026) is partial, and the data is not comparable to full years [AGORA coverage matrix].
* The AGORA policy dataset contains matching incident counts to chatbots and AI assistants, but it does not provide details on specific incidents of what went wrong [AGORA coverage matrix].
* Risk classifications and use-case labels rely on hand-made risk crosswalks and curated taxonomies rather than automated objective mappings [AGORA coverage matrix].
* The policy database focuses on enacted state-level legislation in the US, which does not represent international policy frameworks or local regulations [AGORA coverage matrix].
