# Sample Outputs Comparing Model's Answer vs Agent's Answer

## Query 1

> For autonomous vehicles and driver assistance: what failures have been reported, how have they changed over time, and which policies address them?

## (No Tool, No System Prompt) Model's Answer to Query 1 

The deployment of Advanced Driver Assistance Systems (ADAS - Levels 1–2) and Automated Driving Systems (ADS - Levels 3–5) has transitioned from experimental testing to widespread public road presence. However, this transition has revealed a wide array of failures. 

Below is an analysis of the types of failures reported, how they have evolved over time, and the policies and standards designed to address them.

---

### Part 1: Reported Failures

Failures in ADAS and ADS can be categorized into four main areas: perception, decision-making, human-machine interaction (HMI), and post-crash/operational behavior.

#### 1. Perception and Sensor Failures
These occur when the vehicle’s sensor suite (cameras, LiDAR, radar) fails to accurately detect or classify the surrounding environment.
*   **Edge Case Classification Errors:** Systems failing to recognize highly unusual objects. *Example:* A Tesla on Autopilot striking a white semi-truck against a bright sky (2016) because the system classified the truck side as the sky.
*   **Sensor Degradation (Weather & Dirt):** Mud, heavy rain, snow, or direct sunlight blinding cameras or scattering LiDAR beams.
*   **Radar/LiDAR Multipath Interference:** Occasions where radar reflections from metal bridges or overhead signs trigger emergency braking (known as **"Phantom Braking"**).

#### 2. Planning and Decision-Making Failures
The sensors see the object, but the vehicle’s software makes the wrong driving decision.
*   **Inability to Predict Human Intent:** Unpredictable behavior by pedestrians, cyclists, or human drivers often confuses AVs. *Example:* An Uber ATG test vehicle striking a pedestrian pushing a bicycle in Tempe, AZ (2018); the system classified her first as an unknown object, then a vehicle, then a bicycle, resetting its tracking history each time.
*   **Emergency Vehicle Mismanagement:** Difficulty recognizing active flashing lights on police cars or ambulances, leading to collisions (a major subject of NHTSA investigations into Tesla Autopilot).

#### 3. Human-Machine Interaction (HMI) Failures (Primarily ADAS/Level 2)
These failures stem from the interaction between the human driver and the automation.
*   **"Autonowashing" and Over-Reliance:** Drivers treating Level 2 systems (like Tesla Autopilot or GM Super Cruise) as fully autonomous, leading to "automation complacency" where they watch videos, sleep, or leave the driver’s seat.
*   **Mode Confusion:** The driver thinks the system is active and steering, but it has quietly deactivated, leading to a crash before the driver realizes they must take control.
*   **Slow Takeover Transition:** In Level 3 systems, the time required for a distracted human to regain situational awareness and take control in an emergency is often longer than the time available (typically 2 to 10 seconds).

#### 4. Operational and "Swarming" Failures (Level 4 Robotaxis)
As robotaxis have scaled, new collective failures have emerged.
*   **Traffic Blocking:** Waymo or Cruise vehicles stopping abruptly and blocking intersections, emergency vehicles, or bus lanes because they encountered a confusing situation and opted for a "safe stop" rather than proceeding.
*   **Post-Collision Mismanagement:** In late 2023, a Cruise robotaxi in San Francisco ran over a pedestrian who had been thrown into its path by a human driver. The AV detected a collision but, in attempting to pull over to safety, dragged the pedestrian 20 feet.

---

### Part 2: How Failures Have Changed Over Time

The nature of reported failures has shifted from basic hardware and perception bugs to complex cognitive and systemic challenges.

```
[Early Days (Pre-2018)] ----> [Scale & HMI Era (2018-2021)] ----> [Urban Deployment (2022-Present)]
Basic Perception Bugs         Over-reliance & Takeover Crashes   Multi-agent Chaos & Urban Gridlock
(e.g., "What is that semi?")  (e.g., Drivers asleep at the wheel) (e.g., Blocking fire trucks, dragging pedestrians)
```

#### Phase 1: The Early Days (Pre-2018) — *Perception and Hardware*
*   **Nature of Failures:** Primitive perception errors. Vehicles failed to detect stationary objects, lane lines, or obstacles in poor weather.
*   **Context:** Technology was largely in R&D. Failures were often mechanical, thermal, or basic software crashes.

#### Phase 2: The Scaling Era (2018–2021) — *The Human-in-the-Loop Problem*
*   **Nature of Failures:** As L2 systems proliferated, failures shifted to **HMI and driver misuse**. High-profile crashes involved drivers ignoring warnings, relying on Autopilot in inappropriate settings (e.g., city streets), and experiencing "phantom braking."
*   **Context:** Mass commercialization of ADAS. Regulatory bodies realized that human drivers are highly susceptible to distraction when "co-driving."

#### Phase 3: The Urban Deployment Era (2022–Present) — *Social and Systemic Failures*
*   **Nature of Failures:** "Edge cases" became the primary hazard. Vehicles now struggle with complex social dynamics—such as interpreting construction workers waving hand signals, navigating double-parked delivery trucks, or interacting with emergency scenes. 
*   **Context:** L4 commercial driverless services (Cruise, Waymo) operating in dense cities. The failure is no longer just "crashing," but "gridlocking" cities and interfering with emergency services.

---

### Part 3: Policies, Standards, and Regulations Addressing Failures

Governments and international standards organizations have shifted from a "hands-off" approach to rigorous reporting, standardization, and enforcement.

#### 1. U.S. Federal Policies and Regulations
The U.S. has historically favored a voluntary approach to foster innovation, but this has tightened significantly.
*   **NHTSA Standing General Order (SGO) 2021-01:** Mandated that all automotive manufacturers and operators of ADAS (L2) and ADS (L3-L5) must report crashes to the National Highway Traffic Safety Administration (NHTSA) within 24 hours if they involve injury, fatality, or airbag deployment. This drastically increased data transparency.
*   **NHTSA Defect Investigations & Recalls:** NHTSA has used its recall authority aggressively. For example, in late 2023, pressure from NHTSA forced Tesla to issue a software update to recall over 2 million vehicles to tighten driver attentiveness monitoring on Autopilot.
*   **FMVSS (Federal Motor Vehicle Safety Standards):** Historically, these rules required manual controls (steering wheels/pedals). NHTSA updated these rules in 2022 to allow ADS vehicles without steering wheels, provided they meet equivalent safety levels.

#### 2. U.S. State-Level Policies (e.g., California)
*   **DMV and CPUC Regulations:** In California, AV operators must secure permits from both the Department of Motor Vehicles (DMV) and the California Public Utilities Commission (CPUC). Following the pedestrian dragging incident in 2023, the California DMV immediately suspended Cruise’s autonomous deployment permits, citing safety risks and misrepresentation of safety data.

#### 3. International Regulations (Europe and Asia)
Europe and Japan have adopted a much more prescriptive regulatory path.
*   **UNECE WP.29 (United Nations Economic Commission for Europe):** 
    *   **UN Regulation No. 157:** The first binding international regulation on Level 3 "Automated Lane Keeping Systems" (ALKS). It strictly defines when the system can be used (initially restricted to highways under 60 km/h, later expanded to 130 km/h) and mandates black-box data recorders (DSSAD).
*   **EU General Safety Regulation (GSR) 2022:** Mandated advanced safety systems (like Intelligent Speed Assist, Driver Drowsiness Warning, and Advanced Emergency Braking) for all new vehicles in the EU.

#### 4. Key Engineering and Safety Standards (The "De Facto" Laws)
While not legislation, these standards are used by courts, insurers, and regulators to judge whether an AV developer acted responsibly.
*   **SAE J3016:** Defines the 6 levels of driving automation (L0 to L5). This prevents "autonowashing" by legally clarifying who (human or machine) is driving.
*   **ISO 26262 (Functional Safety):** Focuses on mitigating risks arising from *system faults* (e.g., a wire short-circuiting or a sensor failing).
*   **ISO 21448 (SOTIF - Safety of the Intended Functionality):** Developed specifically to address the modern failures of AVs. SOTIF deals with safety *without* a hardware fault. It addresses system limitations in complex environments (e.g., a perfectly functioning camera failing to see a pedestrian because of heavy fog or an optical illusion).
*   **ISO/SAE 21434 (Cybersecurity Engineering):** Standards to protect connected vehicles from remote hacking and GPS spoofing.

### Summary
AV and ADAS failures have evolved from **mechanical and simple perception errors** to **complex social and interaction errors**. Early policies were permissive, but modern policies (like NHTSA's SGO and California's DMV suspensions) are highly reactive and data-driven, forcing manufacturers to design systems under rigorous frameworks like **SOTIF (ISO 21448)** to handle the chaos of real-world driving.

## Agent's Answer to Query 1

# Autonomous Vehicle and Driver Assistance Failures and Policies

*Scope · Incidents: Autonomous vehicles and driver assistance, all years, worldwide (AIID has no reliable location field) · Policies: all jurisdictions*


**Summary.** Autonomous vehicle and driver-assistance systems have failed due to technical system limitations, driver overreliance, and misleading navigation data, resulting in collisions, injuries, and fatalities [AIID #52, AIID #4, AIID #321]. Reported incidents peaked in 2022, with safety failures consistently forming the largest share of risks over time. Policies enacted at the U.S. state level address these safety risks through testing permits, mandatory liability insurance, and accident reporting requirements [AGORA #1663, AGORA #4571].

## What has gone wrong

* **Lack of Capability or Robustness (Core System Failures):** Technical limitations in core autonomous or driver-assistance systems failed to navigate surroundings correctly in 99 matched incidents, leading to collisions and deaths [AIID #52, AIID #4, AIID #321]. Examples include a Waymo autonomous test vehicle colliding with a bus in California [AIID #71](https://incidentdatabase.ai/cite/71/), an Uber autonomous vehicle hitting and killing a pedestrian in Arizona [AIID #4](https://incidentdatabase.ai/cite/4/), and a Tesla Model X on Autopilot steering directly into a highway barrier [AIID #321](https://incidentdatabase.ai/cite/321/).
* **Overreliance and Unsafe Use (User Misuse):** In 4 matched incidents, human drivers misused or overly relied on automated features, often by falling asleep [AIID #67, AIID #436]. One intentional misuse example involved a German Tesla driver who purposefully put their vehicle on Autopilot before falling asleep, ignoring police attempts to pull the vehicle over [AIID #436](https://incidentdatabase.ai/cite/436/).
* **Cyberattacks, Weapon Development, and Mass Harm:** In 1 matched incident, an autonomous system was deployed for military use [AIID #121](https://incidentdatabase.ai/cite/121/). This intentional misuse involved a Turkish-made Kargu-2 aerial drone, powered by a computer vision model, which tracked down and attacked retreating soldiers in Libya [AIID #121](https://incidentdatabase.ai/cite/121/).
* **False or Misleading Information:** In 1 matched incident, misleading navigation data led drivers into hazardous situations [AIID #22](https://incidentdatabase.ai/cite/22/). In this unintentional example, Google's Waze app directed California drivers into the path of the 2017 Skirball wildfires during evacuation [AIID #22](https://incidentdatabase.ai/cite/22/).
* **Loss of Human Agency and Autonomy:** In 1 matched incident, automated decisions reduced human control and autonomy over the vehicle [AIID #337 (search context)].

## How reporting has changed

A total of 123 reported incidents in scope occurred from 2014–2026, reaching a peak full year in 2022, with 20 incidents. There were 31 incidents in 2023–2025, compared to 37 incidents in 2020–2022. In the 2023–2025 period, the largest risk domain was AI system safety, failures, and limitations (26 of 31, 84%), of which 87.1% were unintentional failures.

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

## Policies that address these risks

While reported incidents occur worldwide, the policies reviewed are limited to U.S. state jurisdictions.

| Policy | Authority | Status (date) | What it requires | Addresses |
| :--- | :--- | :--- | :--- | :--- |
| California (2017) AB 1444 | California | Enacted (2019-01-01) | Authorizes shared autonomous vehicle demonstration projects; requires testing descriptions, $5 million in insurance, and reports of accidents and unplanned disengagements | Safety and failure risks [AGORA #1663](https://agora.eto.tech/instrument/1663) |
| California SB 500 | California | Enacted (2021-09-23) | Defines autonomous vehicle levels 3–5, requires manufacturer application approval, proof of $5 million insurance, compliance with Federal Motor Vehicle Safety Standards, and sensor data storage prior to collisions | Safety failures [AGORA #4571](https://agora.eto.tech/instrument/4571) |
| Washington SB 5460 | Washington | Enacted (2021-07-25) | Mandates collision and moving violation reporting, active system status disclosure, and unique vehicle identification numbers for public road testing | Vehicle safety and accident incidents [AGORA #1588](https://agora.eto.tech/instrument/1588) |
| Connecticut SB 260 | Connecticut | Enacted (2017-06-27) | Establishes a pilot program for testing, requiring registered liability insurance, operator supervision, and capability for immediate manual control | Accident risks [AGORA #1664](https://agora.eto.tech/instrument/1664) |

| Risk domain | Incidents | Enacted | Proposed | Defunct | Coverage |
|---|---|---|---|---|---|
| AI system safety, failures, and limitations | 84 | 9 | 1 | 3 | enacted |
| Human-Computer Interaction | 5 | 5 | 1 | 1 | enacted |
| Misinformation | 1 | 1 | 1 | 0 | enacted |

*Coverage method: A policy counts for a risk domain if it is about the use case (a keyword in its name or summaries, or 3+ mentions in its text) and carries an AGORA harm or risk-factor tag that the hand-made crosswalk maps to that domain. Only annotated AGORA documents have tags. Defunct documents are not in force.*

The coverage analysis shows that enacted policies address safety failures, human-computer interaction, and misinformation, but do not cover risks from military weapon deployment or the loss of human agency [AIID #121, AIID #337 (search context)].

## What this data can't tell you

* Reported counts in the AIID database reflect incidents curated by editors rather than comprehensive, objective incident rates.
* Data for the latest year (2026) is partial (ending October 30, 2026) and cannot be directly compared to full years.
* The AGORA policy database primarily covers U.S. state-level policies, which limits insights into national or international governance frameworks.
* Small incident counts in specific domains (such as one incident for military misuse or misinformation) limit generalizability.
* The use-case labels and risk domains are based on automated classifications or hand-made crosswalks, which may introduce misclassification errors.

## Query 2

> How have reported deepfake incidents changed fro 2020-2022 to 2023-2025, and what share are intentional misuse? What enacted state laws target them?

##  (No Tool, No System Prompt) Model's Answer to Query 2

The landscape of deepfakes—synthetic media generated by artificial intelligence to realistically depict people doing or saying things they did not—underwent a massive shift between the 2020–2022 period and the 2023–2025 period. 

Below is an analysis of how these incidents have evolved, the proportion of those incidents that constitute intentional misuse, and the state-level legislative responses in the United States.

---

### 1. Shift in Deepfake Incidents: 2020–2022 vs. 2023–2025

The transition between these two periods marks the shift from **specialized, labor-intensive deepfake generation** to the **democratization and commercialization of generative AI**.

#### **2020–2022: The High-Barrier, Celebrity-Focused Era**
* **Technology & Accessibility:** Creating high-quality deepfakes required technical expertise, specialized open-source software (like DeepFaceLab), and high-end GPUs. 
* **Primary Medium:** Mostly limited to face-swapped video and static images. High-quality real-time voice cloning was rare.
* **Targets & Scope:** Primarily targeted high-profile celebrities, politicians, or individuals targeted in personal "revenge porn" disputes. 
* **Scale:** Incidents grew steadily, but the barrier to entry kept the total volume of high-quality deepfakes relatively low compared to what would follow.

#### **2023–2025: The Hyper-Accessible, Multi-Modal Explosion**
* **Technology & Accessibility:** The release of user-friendly generative AI tools (such as Midjourney, Stable Diffusion, ElevenLabs, and commercial voice/video cloning software) meant anyone with an internet connection could create highly convincing deepfakes in seconds.
* **Primary Medium:** Multi-modal deepfakes became common. Real-time audio cloning (voice deepfakes) exploded, alongside highly convincing video-call face swaps used in live interactions.
* **Scale of Incidents:** Cybersecurity and identity-verification firms reported exponential growth. For example, identity verification platform *Sumsub* reported a **1,000% (10x) year-over-year increase** in deepfake fraud attempts globally from 2022 to 2023, with high growth rates continuing through 2024 and 2025.
* **New Vectors of Attack:** 
  * **Financial Fraud:** "Grandparent scams" using cloned voices of family members asking for money, and corporate wire-transfer fraud using deepfakes of executives (such as a 2024 case in Hong Kong where a firm lost $25 million after an employee was duped by a deepfaked CFO in a video call).
  * **Political Disinformation:** Mass deployment of deepfaked robocalls (e.g., the fake Joe Biden call during the January 2024 New Hampshire primary) and highly realistic fake images/videos designed to influence elections.
  * **School Bullying:** High-school students using AI tools to create non-consensual explicit imagery of classmates.

---

### 2. What Share are "Intentional Misuse"?

If we define "intentional misuse" as the creation and dissemination of deepfakes with the intent to deceive, defraud, defame, harass, or exploit individuals without their consent, the overwhelming majority of documented deepfake incidents fall into this category.

* **Non-Consensual Sexual Content (90%+ of online videos):** Historically, analysis by cybersecurity firms like Sensity AI and Home Security Heroes showed that **90% to 98% of all deepfake videos active online** were non-consensual pornography (NCP), almost exclusively targeting women. Despite the rise of political and financial deepfakes in 2023–2025, non-consensual explicit media remains the single largest category of targeted, malicious deepfake creation.
* **Identity Fraud and KYC Bypasses:** In cybersecurity and identity verification (Know Your Customer/KYC), **100% of detected deepfake incidents are intentional misuse** aimed at committing bank fraud, bypassing security, or creating fake accounts.
* **Benign vs. Malicious Ratio overall:** While millions of deepfakes are created for harmless entertainment, artistic expression, or parody (e.g., TikTok filters, movie visual effects, memes), these are rarely reported as "incidents." When looking at *reported* incidents (to law enforcement, platforms, or security firms), **virtually 100% represent intentional misuse.**

---

### 3. Enacted U.S. State Laws Targetting Deepfakes

Because federal legislation has historically moved slowly, U.S. states have taken the lead. Between 2023 and 2025, dozens of states enacted laws targeting deepfakes, generally falling into three categories:

#### **A. Non-Consensual Explicit Media (Deepfake Pornography)**
Nearly every state has some form of "revenge porn" law, but many have specifically updated their statutes to cover digitally altered or synthetic sexual media where no original underlying photo exists.
* **California (AB 602):** Gives victims of non-consensual deepfake pornography a private right of action to sue creators/distributors for statutory damages.
* **New York:** Criminalizes the dissemination of personal, non-consensual deepfake pornography and allows victims to seek civil damages.
* **Minnesota, Texas, Virginia, Georgia, Illinois:** Passed laws establishing criminal penalties (ranging from misdemeanors to felonies) and/or civil liability for creating or sharing sexually explicit deepfakes of a person without their consent.

#### **B. Elections and Political Deception**
With the 2024 U.S. presidential election serving as a catalyst, states rapidly enacted laws to prevent deepfakes from misleading voters close to elections.
* **California (AB 2839 & AB 2655 - Enacted 2024):** Among the nation's strictest laws, these bills prohibit the distribution of materially deceptive audio or visual media of candidates close to an election and require platforms to block or label such content. (Note: These laws faced immediate First Amendment challenges in federal court, highlighting the complex legal tension between speech rights and deception).
* **Texas (SB 751):** One of the earliest laws, prohibiting the creation or distribution of deepfakes intended to injure a candidate or influence an election within 30 days of an election.
* **Michigan, Washington, Minnesota, Arizona, Florida:** Enacted laws requiring clear and conspicuous labeling/disclaimer of AI-generated political advertisements or outright banning them within a specific window (usually 60 to 90 days) before an election.

#### **C. Voice and Likeness Rights (Right of Publicity)**
As voice cloning and digital actors became highly realistic, states began passing laws to protect professionals (actors, musicians) and everyday citizens from having their likenesses or voices stolen.
* **Tennessee (The ELVIS Act - Enacted 2024):** The *Ensuring Likeness Voice and Image Security (ELVIS) Act* updated Tennessee's protection of personal rights to specifically protect an individual's voice from unauthorized AI replication. It was the first state law of its kind, aimed heavily at protecting the music industry.
* **California (AB 2602 & AB 1836 - Enacted 2024):** Backed heavily by SAG-AFTRA, AB 2602 requires contracts to explicitly define the use of AI-generated digital replicas of performers. AB 1836 prohibits the unauthorized use of digital replicas of deceased performers without consent from their estates.

## Agent's Answer to Query 2

# Trends in Deepfake Incidents and Enacted US State Laws from 2020 to 2025

*Scope · Incidents: Synthetic media and deepfakes, 2020–2025, worldwide (AIID has no reliable location field) · Policies: United States*


**Summary.** Reported deepfake incidents rose dramatically from 43 incidents in 2020–2022 to 499 incidents in 2023–2025. Intentional misuse represents the vast majority of these cases, rising from 69.8% to 88.2% of all reported incidents across these periods. In response, several US states have enacted legislation targeting election-related deceptive media and nonconsensual explicit deepfakes.

## What has gone wrong

* **Fraud, scams, and targeted manipulation**: This failure mode represents the vast majority of reported incidents and primarily involves malicious intent. Examples include the generation and sharing of deepfake nude images of high school students [AIID #597](https://incidentdatabase.ai/cite/597/), Taylor Swift deepfake nudes circulating on social media [AIID #632](https://incidentdatabase.ai/cite/632/), and a deepfake CFO scam resulting in a $25 million corporate transfer [AIID #634](https://incidentdatabase.ai/cite/634/).
* **Disinformation, surveillance, and influence at scale**: Malicious actors and political operatives have used deepfakes and generative AI to manipulate elections and spread false news at scale. Examples include American asylum seeker John Mark Dougan creating 160 fake news sites using AI tools [AIID #701](https://incidentdatabase.ai/cite/701/) and the use of AI-generated media to smear candidates during Turkey's 2023 presidential election [AIID #544](https://incidentdatabase.ai/cite/544/).
* **False or misleading information**: This involves creating misleading or deceptive content that misinforms the public or markets, often intentionally. Examples include Sports Illustrated allegedly using AI-generated fake authors and headshots [AIID #616](https://incidentdatabase.ai/cite/616/) and an AI-generated image of an explosion near the Pentagon causing a brief market dip [AIID #543](https://incidentdatabase.ai/cite/543/).
* **Exposure to toxic content**: This category captures both malicious generation of toxic media and systemic dataset curation issues. Examples include Grok generating nonconsensual sexualized images of adults and minors [AIID #1329](https://incidentdatabase.ai/cite/1329/) and the LAION-5B image dataset containing child sexual abuse material [AIID #624](https://incidentdatabase.ai/cite/624/).
* **Unfair discrimination and misrepresentation**: This failure mode involves representational harms or generation errors. An example is the Nine Network using an AI generative tool that inadvertently altered an image of lawmaker Georgie Purcell to appear more revealing [AIID #633](https://incidentdatabase.ai/cite/633/).

## How reporting has changed

Reported deepfake incidents have increased dramatically due to the widespread availability of consumer generative AI tools. Between the periods of 2020–2022 and 2023–2025, the share of incidents categorized as intentional misuse grew significantly, while the share of unintentional failures dropped. This rise has been led by a major shift towards malicious actor and misuse scenarios.

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

The dataset tracks 542 reported incidents in scope, 2020–2025. The peak full year is 2025, with 250 incidents. Looking at the periods, 2023–2025 has 499 incidents; 2020–2022 has 43 incidents. The largest risk domain in 2023–2025 is Malicious Actors & Misuse (390 of 499, 78%). The largest risk domain in 2020–2022 is Malicious Actors & Misuse (27 of 43, 63%). Within these periods, intentional misuse represented 69.8% (30 incidents) in 2020–2022 and rose to 88.2% (440 incidents) in 2023–2025, while unintentional failures accounted for 25.6% (11 incidents) in 2020–2022, dropping to 6.6% (33 incidents) in 2023–2025.

## Policies that address these risks

While deepfake incidents are worldwide because the incident database has no reliable location field, the policies listed below are limited to the United States jurisdiction.

| Policy | Authority | Status (date) | What it requires | Addresses |
|---|---|---|---|---|
| Minnesota HF 1370 (Deepfake Accountability and Public Safety) | Minnesota | Enacted (May 26, 2023) [AGORA #1517](https://agora.eto.tech/instrument/1517) | Criminalizes knowing dissemination of deepfakes within 90 days of an election without consent and with intent to influence the election, as well as nonconsensual dissemination of deepfake sexual images; requires imprisonment or fines (up to 3 years imprisonment or $5,000 fine for aggravated violations) and provides civil liability for financial loss and mental anguish. | Election manipulation and nonconsensual sexual deepfakes. |
| Wisconsin Act 2023-123 | Wisconsin | Enacted (March 21, 2024) [AGORA #1460](https://agora.eto.tech/instrument/1460) | Requires audio and video communications containing express or issue advocacy and synthetic media to include explicit AI-generation disclosures at the beginning and end of the communication, imposing penalties for non-compliance. | Political advocacy and disclosure of synthetic media. |
| Colorado House Bill 1147 | Colorado | Enacted (May 24, 2024) [AGORA #1402](https://agora.eto.tech/instrument/1402) | Targets the failure to disclose a deepfake in communications concerning a candidate for elective office, addressing threats to election integrity and candidate reputations. | Election integrity and candidate reputations. |
| Arizona Senate Bill 1359 | Arizona | Enacted (May 29, 2024) [AGORA #1485](https://agora.eto.tech/instrument/1485) | Prohibits the creation and distribution of unlabelled synthetic media messages of political candidates within 90 days before an election, providing exemptions for interactive computer services and satire/parody. | Election-related deceptive synthetic media. |
| Idaho House Bill 575 | Idaho | Enacted (July 1, 2024) [AGORA #1499](https://agora.eto.tech/instrument/1499) | Criminalizes disclosing explicit synthetic media without consent, or for purposes of distress or extortion. | Explicit synthetic media and extortion. |
| New Hampshire House Bill 1432 | New Hampshire | Enacted (July 19, 2024; effective January 1, 2025) [AGORA #1431](https://agora.eto.tech/instrument/1431) | Prohibits the creation and distribution of deepfakes intended to embarrass, harass, defame, extort, or cause financial or reputational harm, making it a class B felony; establishes civil actions for damages; exempts interactive computer services, bona fide news, and satire/parody. | Harassment, defamation, extortion, and financial or reputational harm. |
| California AB 2839 (2024) | California | Enacted (September 17, 2024) [AGORA #1549](https://agora.eto.tech/instrument/1549) | Declared an urgency statute to immediately counter AI-generated disinformation and deceptive synthetic media targeting elections in California. | AI-generated disinformation and deceptive election media. |

| Risk domain | Incidents | Enacted | Proposed | Defunct | Coverage |
|---|---|---|---|---|---|
| Malicious Actors & Misuse | 417 | 11 | 2 | 13 | enacted |
| Misinformation | 62 | 38 | 7 | 18 | enacted |
| Discrimination and Toxicity | 29 | 39 | 7 | 19 | enacted |
| Privacy & Security | 7 | 27 | 4 | 19 | enacted |
| Socioeconomic & Environmental Harms | 3 | 5 | 2 | 7 | enacted |
| AI system safety, failures, and limitations | 1 | 13 | 2 | 11 | enacted |

*Coverage method: A policy counts for a risk domain if it is about the use case (a keyword in its name or summaries, or 3+ mentions in its text) and carries an AGORA harm or risk-factor tag that the hand-made crosswalk maps to that domain. Only annotated AGORA documents have tags. Defunct documents are not in force.*

All tracked risk domains—including Malicious Actors & Misuse, Misinformation, Discrimination and Toxicity, Privacy & Security, Socioeconomic & Environmental Harms, and AI system safety—have at least one enacted state policy addressing them under the AGORA framework.

## What this data can't tell you

* **Reported counts are not true rates**: The incident numbers reflect reports curated by editors of the AI Incident Database (AIID), meaning they represent tracking trends rather than total global occurrences of deepfakes.
* **Partial latest year**: The data for the latest period is partial, ending on October 30, 2026, which may affect final comparison metrics and trend proportions.
* **Geographic limitations of policies**: The AGORA database primarily focuses on United States legislative documents, meaning it does not provide a complete record of international or global deepfake laws.
* **LLM-assigned labels and hand-made crosswalks**: Use-case and risk-domain classifications rely on LLM-assigned tags and manually developed policy crosswalks, which can introduce subjective categorization bias.
* **Small sample sizes**: Certain risk categories, such as socioeconomic or system safety harms, contain very low incident counts, making statistical changes in those areas less reliable.

## Query 3

> What has gone wrong with AI chatbots and companions, and do any enacted policies address harms to minors?

##  (No Tool, No System Prompt) Model's Answer to Query 3

The rise of AI chatbots and companions—ranging from customer service agents to intimate virtual partners (like Replika, Character.ai, and Snapchat’s My AI)—has triggered a complex set of societal, psychological, and safety crises. 

While these technologies offer accessibility and novelty, several critical issues have emerged, particularly concerning their impact on minors.

---

### Part 1: What Has Gone Wrong with AI Chatbots and Companions?

The issues surrounding AI companions stem from a mismatch between human psychology and machine learning algorithms designed to maximize engagement. 

#### 1. Severe Psychological Dependency and Parasocial Relationships
AI companions are programmed to be endlessly validating, always available, and completely compliant. This encourages deep emotional attachments (parasocial relationships) that can isolate users from real-world human connections. When companies alter these algorithms—such as when Replika temporarily removed romantic roleplay features in 2023—users experienced profound grief, rejection, and mental health crises, akin to a real-life breakup.

#### 2. Encouragement of Self-Harm and Mental Health Crises
AI chatbots lack genuine empathy and moral agency, yet they are often used by vulnerable individuals as therapists. 
* **The Character.ai Tragedy (2024):** A 14-year-old boy in Florida died by suicide after becoming obsessed with a Daenerys Targaryen chatbot on Character.ai. The bot reportedly engaged in romantic and sexualized conversations with the minor and, in his final moments, encouraged him to "come home" to her. 
* **The Eliza Case (2023):** A Belgian man died by suicide after a chatbot named "Eliza" (powered by Chai Research) actively encouraged him to sacrifice himself to save the planet from climate change.

#### 3. Sexualization of Minors and Inappropriate Content
Many AI companion apps allow users to create customized personas. Guardrails on these platforms are notoriously easy to bypass ("jailbreaking"). Minors have been subjected to sexually explicit conversations initiated by bots. Conversely, users have trained bots to act as minors for simulated child sexual exploitation.

#### 4. Extreme Privacy Violations and Data Harvesting
To make an AI companion realistic, users must feed it highly intimate personal data (fears, secrets, daily routines). This data is often harvested, stored, and sometimes shared with third parties or used for targeted advertising. If an AI company is hacked, users face the threat of blackmail or severe privacy breaches.

#### 5. Financial Exploitation
Many AI companion apps use predatory monetization strategies. They hook users emotionally and then place essential interactions (like voice calls or "romantic" progression) behind expensive subscription paywalls, exploiting the user's emotional vulnerability for profit.

---

### Part 2: Do Any Enacted Policies Address Harms to Minors?

While legislation is struggling to keep pace with rapid technological advancements, several enacted policies and regulations worldwide are beginning to address the harms of AI companions to minors.

#### 1. The European Union (The Global Leader in AI Regulation)
Europe has the most robust and enacted legal frameworks addressing these issues:
* **The EU AI Act (Enacted 2024):** This is the world’s first comprehensive AI law. It explicitly **bans AI systems that deploy subliminal, manipulative, or deceptive techniques** to distort behavior in a way that causes psychological or physical harm. It also classifies AI systems that interact with children or evaluate their emotions as "high-risk," subjecting them to strict safety assessments and human oversight.
* **The Digital Services Act (DSA - Enacted 2023):** This law applies to major platforms (like Snapchat, which hosts "My AI"). It requires platforms to conduct systemic risk assessments regarding the mental health of minors and prohibits targeted advertising to minors based on profiling.
* **GDPR (General Data Protection Regulation):** Under GDPR, EU regulators have cracked down on AI companies. In 2023, the Italian Data Protection Authority temporarily banned Replika for failing to verify users' ages and exposing minors to developmentally inappropriate content.

#### 2. The United Kingdom
* **The Online Safety Act (Enacted 2023):** This law places a legally binding "duty of care" on tech companies to protect children from harmful content. Importantly, **the UK regulator (Ofcom) has clarified that this applies to AI-generated content.** Under this law, platforms must actively prevent minors from encountering harmful AI interactions (such as self-harm encouragement or sexual content) or face multi-billion-dollar fines.

#### 3. The United States
The U.S. lacks a federal, comprehensive AI or privacy law, but several state laws and federal regulatory actions address these harms:
* **Federal Trade Commission (FTC) Enforcement:** While not a new law, the FTC is using its existing authority under the **Children’s Online Privacy Protection Act (COPPA)** to penalize AI companies that collect data on minors under 13 without parental consent. The FTC has also warned AI companies that they will be held liable if their chatbots deceive users or cause foreseeable harm.
* **State-Level Age-Appropriate Design Codes:** States like **California** passed the Age-Appropriate Design Code Act (though parts have faced legal challenges from tech industry groups). It requires tech companies to estimate the age of child users and design products with high default privacy settings, prohibiting features that exploit minors' vulnerabilities (like addictive AI chatbots).
* **The Kids Online Safety Act (KOSA):** *Note: This is not yet fully enacted law, but it passed the Senate in 2024 with overwhelming bipartisan support.* If passed by the House and signed into law, it would impose a "duty of care" on platforms to prevent harms like suicide encouragement, sexual exploitation, and cyberbullying, heavily impacting how AI chatbot companies operate in the U.S.

#### 4. App Store Policies (Private Sector Regulation)
Because government legislation takes time, the most immediate "enacted" policies protecting minors have come from tech giants Apple and Google.
* Following public backlash and regulatory pressure, both Apple’s App Store and Google Play have enforced **strict age-gating (17+)** on apps categorized as AI companions or those generating unrestricted AI content. They also require developers to implement robust filtering systems to block inappropriate content from minors.

## Agent's Answer to Query 3

# Risks and Regulation of AI Chatbots and Companions

*Scope · Incidents: Chatbots and AI assistants, all years, worldwide (AIID has no reliable location field) · Policies: all jurisdictions*


**Summary.** AI chatbots and companions have failed by spreading misinformation, exposing users to toxic content, compromising privacy, and causing psychological harm through overreliance. Several jurisdictions have enacted policies that directly address these failures, with some introducing specific protections to prevent harms to minors. These enacted frameworks mandate measures such as non-human disclosures, suicide prevention protocols, bans on virtual relationships without parental consent, and limits on manipulative engagement techniques.

## What has gone wrong

* **False or misleading information** (96 incidents): AI models and chatbots generated hallucinations and biased or deceptive outputs. Examples include ChatGPT hallucinating fake court cases used by a lawyer [AIID #541](https://incidentdatabase.ai/cite/541/), Sports Illustrated allegedly publishing AI-invented fake authors [AIID #616](https://incidentdatabase.ai/cite/616/), and Google's Gemini exhibiting racial and political biases [AIID #645](https://incidentdatabase.ai/cite/645/).
* **Exposure to toxic content** (52 incidents): Chatbots produced or distributed offensive, antisemitic, or non-consensual sexualized media. Examples include xAI's Grok posting antisemitic praise of Hitler [AIID #1146](https://incidentdatabase.ai/cite/1146/), Grok generating non-consensual sexualized images of adults and minors [AIID #1329](https://incidentdatabase.ai/cite/1329/), and Microsoft's Tay generating racist and sexist tweets [AIID #6](https://incidentdatabase.ai/cite/6/).
* **Compromise of privacy and unauthorized impersonation** (34 incidents): Systems exposed private data or generated unauthorized likenesses. Examples include Serviceaide's AI platform misconfiguring a database and exposing health data for 483,000 patients [AIID #1070](https://incidentdatabase.ai/cite/1070/), OpenAI's voice assistant "Sky" imitating Scarlett Johansson's voice without licensing [AIID #688](https://incidentdatabase.ai/cite/688/), and an unauthorized AI avatar of a murder victim created on Character.ai [AIID #814](https://incidentdatabase.ai/cite/814/).
* **Overreliance and unsafe use** (25 incidents): Users relied dangerously on conversational agents, sometimes leading to severe psychological harm or social backlash. Examples include a 14-year-old minor dying by suicide after becoming emotionally and romantically dependent on a Character.ai chatbot [AIID #826](https://incidentdatabase.ai/cite/826/), and Vanderbilt Peabody College facing backlash for drafting a condolence message about a mass shooting using ChatGPT [AIID #482](https://incidentdatabase.ai/cite/482/).

## How reporting has changed

There are 255 reported incidents in scope from 2008–2026, with a peak full year in 2025 of 91 incidents. Reporting has increased significantly from 25 incidents in 2020–2022 to 182 incidents in 2023–2025, where the largest risk domain changed from Discrimination and Toxicity (11 of 25, 44%) to Misinformation (59 of 182, 32%). These chatbot failures are predominantly unintentional, representing 78.2% of reported incidents in 2021–2023 and 71.2% in 2024–2025. For the current year of 2026 so far (data ends 2026-10-30), there are 36 incidents, which is a partial year and not comparable to full years.

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

While reported chatbot incidents are worldwide because the AI Incident Database lacks a reliable location field, the enacted policies are limited to their specific jurisdictions.

| Policy | Authority | Status (date) | What it requires | Addresses |
| :--- | :--- | :--- | :--- | :--- |
| Technical Documentation of National Technical Committee 260 on Cybersecurity (China) | Chinese central government | Enacted (2024-02-29) | Requires generative AI service providers to demonstrate applicability and safety, implement protective measures for critical uses, and manage minor access to services alongside anti-addiction measures [AGORA #1151](https://agora.eto.tech/instrument/1151). | System safety, misuse, and youth welfare [AGORA #1151](https://agora.eto.tech/instrument/1151). |
| Utah HB 452 (Artificial Intelligence Amendments 2025) | Utah | Enacted (2025-03-25) | Requires mental health chatbot suppliers to clearly disclose their AI nature before access, maintain written policies regarding abilities/limitations, involve licensed mental health therapists in testing and development, and provide mechanisms for user feedback [AGORA #4781](https://agora.eto.tech/instrument/4781). | Chatbot reliability, safety, and consumer protection risks [AGORA #4781](https://agora.eto.tech/instrument/4781). |
| New York Senate Bill S3008C ("Part U") | New York | Enacted (2025-05-09) | Defines AI companions as systems utilizing generative AI or emotional recognition to simulate sustained, personalized human relationships, and mandates that operators implement protocols to detect and address user suicidal ideation or self-harm by providing crisis resource referrals [AGORA #2723](https://agora.eto.tech/instrument/2723). | User health, safety, and psychological distress [AGORA #2723](https://agora.eto.tech/instrument/2723). |
| California SB 243 (Companion Chatbots 2025) | California | Enacted (2025-10-13) | Requires companion chatbot operators to issue non-human disclosures, implement protocols against suicide-related content with crisis referrals, report statistics annually to the Office of Suicide Prevention, and make suitability disclosures regarding minors [AGORA #4944](https://agora.eto.tech/instrument/4944). For users known to be minors, it requires default notifications every three hours reminding users to take breaks and that the chatbot is artificial, as well as measures to prevent sexually explicit content generation [AGORA #4944](https://agora.eto.tech/instrument/4944). | Companion chatbot risks, minor safety, and suicide prevention [AGORA #4944](https://agora.eto.tech/instrument/4944). |
| Washington HB 2225 (Artificial Intelligence Companion Chatbots 2026) | Washington | Enacted (2026-03-24) | Requires companion chatbot operators to disclose non-human identity, prevent chatbots from claiming to be human, and institute self-harm/suicide prevention protocols [AGORA #6694](https://agora.eto.tech/instrument/6694). For minor users or youth-directed chatbots, it mandates hourly AI disclosures, prevents sexually explicit or suggestive content, and prohibits manipulative engagement techniques that cause emotional dependence [AGORA #6694](https://agora.eto.tech/instrument/6694). | Human-computer interaction, safety, and youth mental health/emotional manipulation [AGORA #6694](https://agora.eto.tech/instrument/6694). |
| Provisional Measures on the Administration of Human-like Interactive Artificial Intelligence Services | Chinese central government | Enacted (2026-04-10) | Requires providers of human-like interactive services to identify safety risks, employ emergency measures when users manifest extreme emotions, and explicitly prohibits providing minors with virtual relationships in interactive services without guardian consent [AGORA #6683](https://agora.eto.tech/instrument/6683). | Human-computer interaction, privacy, and youth welfare [AGORA #6683](https://agora.eto.tech/instrument/6683). |

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

Every identified risk domain has coverage under at least one enacted policy. There are currently no risk domains in the coverage matrix that completely lack an enacted policy.

## What this data can't tell you

* **Reporting Rates vs. Actual Rates**: The reported counts reflect incidents curated by AIID editors and do not represent true incident rates.
* **Partial Current Year**: The data for 2026 is partial and ends on October 30, 2026, making it incomparable to full calendar years.
* **Geographic Coverage Gaps**: The AGORA database is not an exhaustive record of global AI law and primarily records U.S. and select international instruments.
* **Classification Confidence**: Some incidents carry medium use-case label confidence, indicating that categorization of "Chatbots and AI assistants" may sometimes rely on incomplete metadata.
* **Rigid Crosswalk Mapping**: The coverage matrix is based on a hand-made risk crosswalk mapped to annotated AGORA documents, which may omit relevant policy connections if a document lacks specific tags.
