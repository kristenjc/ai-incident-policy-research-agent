# Baselines: same model, no tools, no system prompt

## Query 1

> What failures have been reported for AI hiring tools, and which US policies address them? Which are actually enacted?

### Model alone

The integration of Artificial Intelligence (AI) into hiring—ranging from resume scanners and gamified assessments to video-interview analysis—has led to documented failures, prompting a wave of regulatory responses in the United States. 

Here is a breakdown of the reported failures of AI hiring tools, the policies designed to address them, and which of those policies are actually enacted and enforceable.

---

### Part 1: Reported Failures of AI Hiring Tools

The failures of AI hiring tools generally fall into four categories: systemic bias, disability discrimination, lack of scientific validity, and vulnerability to "gaming."

1. **Systemic Gender and Racial Bias**
   * **The Amazon Resume Screener (2018):** Amazon built an AI recruiting tool trained on a decade of historical resume data. Because the tech industry was historically male-dominated, the AI learned to penalize resumes containing the word "women’s" (e.g., "women’s chess club") and downgraded graduates from two all-women’s colleges. Amazon eventually scrapped the project.
   * **Proxy Discrimination:** Algorithms often penalize candidates based on "proxies" for race or socioeconomic status, such as zip codes, high schools, or gaps in employment, perpetuating historical inequalities.

2. **Disability and Neurodivergence Discrimination**
   * **Video and Facial Analysis:** Tools like those previously offered by HireVue analyzed facial movements, eye contact, and vocal tones. These tools routinely penalized candidates with autism, cerebral palsy, or those who had suffered strokes, as their facial expressions or speech patterns did not align with the "ideal" benchmark.
   * **Gamified Assessments:** Personality-testing games (like those measuring reaction times or memory) can discriminate against candidates with ADHD, physical dexterity limitations, or visual impairments, even if those traits have no bearing on job performance.

3. **"Phrenology" and Lack of Scientific Validity**
   * Many AI tools claim to detect "personality traits," "culture fit," or "honesty" from voice inflections or micro-expressions. Scientists and civil rights groups have criticized these tools as pseudoscience (comparable to modern-day phrenology), arguing there is no proven link between micro-expressions and job performance. 

4. **Algorithmic "Gaming"**
   * Candidates quickly learned that AI tools could be tricked. Job seekers successfully gamed resume screeners by copying and pasting the entire job description into their resumes in white, invisible font—the AI read the invisible text, deemed the candidate a "perfect match," and bypassed human filters.

---

### Part 2: US Policies Addressing These Failures

To combat these failures, US federal, state, and local governments have drafted policies. These policies generally aim to enforce **transparency** (telling candidates AI is being used), **bias audits** (checking the AI for discriminatory outputs), and **opt-out rights** (allowing human review instead).

Here is a breakdown of what has been proposed versus what is **actually enacted**.

---

### Part 3: What is Actually Enacted vs. Proposed?

#### 1. Enacted and Enforced (Active Laws & Regulations)

These are currently active, legally binding, and enforceable.

##### **Federal Level (Enforced Guidance)**
While Congress has not passed a specific federal AI hiring law, existing civil rights agencies have issued binding enforcement guidance utilizing existing laws:
* **EEOC Title VII Guidance (May 2023):** The Equal Employment Opportunity Commission (EEOC) released official guidance stating that employers are legally liable under Title VII of the Civil Rights Act if their AI selection procedures result in a "disparate impact" (discrimination) against protected classes, even if the software was made by a third-party vendor.
* **EEOC Americans with Disabilities Act (ADA) Guidance (May 2022):** This guidance explicitly warns employers that using AI tools that do not provide "reasonable accommodations" for disabled applicants (e.g., an alternative to a video assessment) violates the ADA.

##### **State Level (Enacted Laws)**
* **Illinois Artificial Intelligence Video Interview Act (Enacted 2020):** 
  * *What it does:* Requires employers to notify applicants if AI is used to analyze their video interviews, explain how the AI works, obtain consent, and destroy the video within 30 days. It also requires employers to report demographic data of those who skipped the AI step to the state.
* **Maryland HB 1202 (Enacted 2020):**
  * *What it does:* Explicitly prohibits employers from using facial recognition services during pre-employment job interviews unless the applicant signs a specific, written waiver.
* **Colorado Senate Bill 24-205 (Enacted May 2024, Effective 2026):**
  * *What it does:* This is the first comprehensive state-level AI law. It requires developers and employers using "high-risk" AI systems (which explicitly includes employment and hiring) to implement risk-management programs, conduct annual bias audits, and notify applicants if AI was used to make an adverse employment decision.

##### **Local Level (Enacted Laws)**
* **New York City Local Law 144 (Enforced July 2023):**
  * *What it does:* This is the most stringent enacted law targeting AI hiring in the US. It prohibits employers from using "automated employment decision tools" (AEDTs) unless the tool has undergone an independent **bias audit** within the past year. The results of the audit (showing the tool's impact on different races and genders) must be made publicly available on the company's website. It also requires notifying NYC candidates that AI is being used and allowing them to request an alternative evaluation process.

---

#### 2. Not Enacted (Proposed, Pending, or Non-Binding)

These policies address AI hiring but **do not currently have the force of law**.

* **The Algorithmic Accountability Act (Proposed Federal Bill):** First introduced in 2019 and reintroduced in 2022/2023, this bill would require the Federal Trade Commission (FTC) to mandate that large companies conduct impact assessments of automated decision systems. *Status: Currently stalled in Congress.*
* **The Blueprint for an AI Bill of Rights (White House, 2022):** Published by the Biden Administration, this document outlines five protections, including protection against abusive algorithmic systems in employment. *Status: Non-binding guidelines; it has no enforcement power.*
* **Executive Order 14110 on Safe, Secure, and Trustworthy AI (Oct 2023):** President Biden's EO directs federal agencies to address AI bias. While the EO is active, its impact on private-sector hiring is indirect (it directs the Department of Labor to publish guidelines for federal contractors and employers, but does not create new statutory laws for the general public).
* **California Civil Rights Department (CRD) Draft Regulations (Proposed):** California is currently drafting regulations that would make it explicitly illegal to use AI hiring tools that discriminate, and would make third-party AI vendors directly liable for discrimination. *Status: Still in the rulemaking/drafting phase.*

### Agent

# Reported Failures in AI Hiring and Enacted US Policies

*Scope · Incidents: Hiring and employment, 1983–2026, worldwide (AIID has no reliable location field) · Policies: United States*


**Summary.** AI hiring and employment tools have suffered from failures including demographic discrimination, automated wrongful terminations, privacy violations, and deepfake employment scams. United States policies addressing these risks remain fragmented, as there is no comprehensive federal statute specifically regulating AI in employment. However, several binding state and local laws have been enacted in New York City, Illinois, and New Jersey to mandate bias audits, candidate notifications, and consent. Proposed state-level bills in California and New York seek broader risk management and discrimination prohibitions but are not yet law.

## What has gone wrong

While the policies discussed in this report are limited to the United States, the reported AI hiring and employment failures represent worldwide incidents because the AIID dataset lacks a reliable location field [AIID #37](https://incidentdatabase.ai/cite/37/).

* **Unfair discrimination and misrepresentation:** 14 matching incidents. An example is Amazon's experimental hiring tool, which allegedly developed a gender bias by penalizing resumes containing the word "women's" and favoring male candidates based on historical training data [AIID #37](https://incidentdatabase.ai/cite/37/). Another example is SafeRent’s AI tenant screening tool, which allegedly disproportionately penalized Black and Hispanic applicants and voucher holders using non-rental debts [AIID #844](https://incidentdatabase.ai/cite/844/).
* **Lack of capability or robustness:** 9 matching incidents. An example is an automated computer program that allegedly laid off an employee and blocked their access to buildings and computer systems without their knowledge [AIID #35](https://incidentdatabase.ai/cite/35/). Another example involves New York City's release of disputed value-added teacher rating models that evaluated thousands of public-school teachers based on student test scores [AIID #9](https://incidentdatabase.ai/cite/9/).
* **Fraud, scams, and targeted manipulation:** 6 matching incidents. An example is North Korean operatives reportedly using AI-generated identities to infiltrate Western companies for remote jobs, enabling wage theft and credential exfiltration [AIID #1118](https://incidentdatabase.ai/cite/1118/). Another example involves a criminal network using deepfake audio of an official to run a fraudulent job scheme [AIID #937](https://incidentdatabase.ai/cite/937/).
* **Compromise of privacy and increased inequality or decline in employment quality:** Compromise of privacy had 6 matching incidents, and increased inequality had 3 matching incidents. An example of privacy compromise is Uber allegedly failing to provide sufficient notice about automated profiling and driving behavior monitoring under GDPR [AIID #354](https://incidentdatabase.ai/cite/354/). An example of employment quality decline is Amazon Flex dismissing contract drivers through automated performance evaluations without human appeal [AIID #111](https://incidentdatabase.ai/cite/111/).

## How reporting has changed

Across 37 reported incidents in scope from 2014–2026, reporting peaked in 2021 with 8 incidents before declining from 16 incidents in 2020–2022 to 4 incidents in 2023–2025. During this decline, the largest risk domain shifted from Discrimination and Toxicity in 2020–2022 (4 of 16, 25%) to Privacy & Security in 2023–2025 (2 of 4, 50%). There are 4 incidents in 2026 so far (data ends 2026-10-30), representing a partial year that is not comparable to prior full years.

| Year | Reported incidents |
|---|---|
| 2014 | 3 |
| 2015 | 1 |
| 2016 | 1 |
| 2017 | 2 |
| 2018 | 2 |
| 2019 | 4 |
| 2020 | 3 |
| 2021 | 8 |
| 2022 | 5 |
| 2023 | 1 |
| 2025 | 3 |
| 2026 (partial) | 4 |

- 37 reported incidents in scope, 2014–2026.
- Peak full year: 2021, with 8 incidents.
- 2023–2025: 4 incidents; 2020–2022: 16 incidents.
- Largest risk domain in 2023–2025: Privacy & Security (2 of 4, 50%).
- Largest risk domain in 2020–2022: Discrimination and Toxicity (4 of 16, 25%).
- 2026 so far (data ends 2026-10-30): 4 incidents. A partial year: not comparable to full years.

## Policies that address these risks

| Policy | Authority | Status (date) | What it requires | Addresses |
| :--- | :--- | :--- | :--- | :--- |
| Illinois Artificial Intelligence Video Interview Act | Illinois | Enacted (August 9, 2019) | Requires employers asking applicants to record video interviews analyzed by AI to notify applicants in advance, explain how the AI evaluates them, obtain consent, limit sharing of interview videos strictly to evaluators, and delete applicant videos and backup copies within 30 days upon request [AGORA #304](https://agora.eto.tech/instrument/304). | Privacy and lack of transparency [AGORA #304](https://agora.eto.tech/instrument/304). |
| A Local Law to amend the administrative code of the city of New York, in relation to automated employment decision tools (NYC Local Law 144) | New York City Council | Enacted (December 11, 2021) | Requires independent annual bias audits for automated employment decision tools, public disclosure of audit summaries and distribution dates, and advance notice to job candidates; enforced through civil liability and fines [AGORA #72](https://agora.eto.tech/instrument/72). | Algorithmic discrimination and transparency [AGORA #72](https://agora.eto.tech/instrument/72). |
| Blueprint for an AI Bill of Rights | Executive Office of the President | Enacted (October 1, 2022) | Sets out non-binding federal principles protecting against algorithmic discrimination and requiring proactive equity assessments, disparity testing, and independent evaluations for automated systems [AGORA #995](https://agora.eto.tech/instrument/995). | Algorithmic discrimination and inequity [AGORA #995](https://agora.eto.tech/instrument/995). |
| Illinois Public Act 103-0804 (Amending the Human Rights Act) | Illinois | Enacted (August 9, 2024, effective January 1, 2026) | Prohibits employers from using artificial intelligence in recruitment, hiring, promotion, or other employment decisions if it results in discrimination against protected classes or uses zip codes as proxies; requires employers to provide notice to employees/applicants when AI is used in employment management [AGORA #1336](https://agora.eto.tech/instrument/1336). | Algorithmic discrimination [AGORA #1336](https://agora.eto.tech/instrument/1336). |
| Guidance on Algorithmic Discrimination and the New Jersey Law Against Discrimination | New Jersey Division on Civil Rights | Enacted (January 8, 2025) | Clarifies that using automated decision-making tools in hiring and employment that result in a disproportionately negative effect (disparate impact discrimination) on protected classes violates the New Jersey Law Against Discrimination [AGORA #1816](https://agora.eto.tech/instrument/1816). | Algorithmic discrimination [AGORA #1816](https://agora.eto.tech/instrument/1816). |
| An Act concerning the use of automated tools to assist with hiring decisions (New Jersey S 211 / A 490) | New Jersey Legislature | Proposed (January 19, 2023) | Would prohibit selling automated employment decision tools without a prior bias audit, an annual audit service, and a compliance notice to purchasers [AGORA #285](https://agora.eto.tech/instrument/285). | Bias and transparency in automated hiring [AGORA #285](https://agora.eto.tech/instrument/285). |
| California SB 420 (Automated decision systems) | California Legislature | Proposed (June 8, 2025) | Prohibits AI discrimination based on protected characteristics, requires regular bias audits, and grants individuals rights to request human oversight and accountability [AGORA #5000](https://agora.eto.tech/instrument/5000). | Algorithmic discrimination [AGORA #5000](https://agora.eto.tech/instrument/5000). |
| New York S 1169 (New York AI Act) | New York State Senate | Proposed (June 3, 2026) | Proposes risk management, impact assessments, and third-party audits for deployers using high-risk AI for consequential decisions affecting individuals [AGORA #3772](https://agora.eto.tech/instrument/3772). | High-risk AI decision making [AGORA #3772](https://agora.eto.tech/instrument/3772). |

| Risk domain | Incidents | Enacted | Proposed | Defunct | Coverage |
|---|---|---|---|---|---|
| Discrimination and Toxicity | 12 | 16 | 11 | 13 | enacted |
| AI system safety, failures, and limitations | 8 | 14 | 6 | 12 | enacted |
| Privacy & Security | 6 | 21 | 12 | 12 | enacted |
| Socioeconomic & Environmental Harms | 3 | 7 | 5 | 8 | enacted |
| Human-Computer Interaction | 2 | 17 | 9 | 9 | enacted |
| Malicious Actors & Misuse | 1 | 13 | 6 | 13 | enacted |

*Coverage method: A policy counts for a risk domain if it is about the use case (a keyword in its name or summaries, or 3+ mentions in its text) and carries an AGORA harm or risk-factor tag that the hand-made crosswalk maps to that domain. Only annotated AGORA documents have tags. Defunct documents are not in force.*

Although all major risk domains have some mapped coverage under state laws or non-binding federal guidance, there is no enacted comprehensive federal statute specifically regulating AI in hiring and employment [AGORA #72, AGORA #995]. Consequently, incidents occurring in jurisdictions outside of Illinois, New York City, and New Jersey remain largely unaddressed by binding local enactments [AGORA #72](https://agora.eto.tech/instrument/72).

## What this data can't tell you

* **Reported counts are not rates:** The AIID database measures the volume of publicly reported incidents rather than the actual rate of occurrences or failures across all deployed AI hiring tools.
* **Partial latest year:** The data for 2026 is partial, ending on 2026-10-30, meaning it cannot be compared directly with prior full years.
* **AGORA is mostly US-focused:** The policy dataset primarily tracks United States policies and does not provide a complete record of international or localized AI hiring regulations outside the US framework.
* **Small counts:** With only 37 total matching incidents in the AIID dataset, sample sizes are too small to establish definitive statistical trends.
* **LLM-assigned use-case labels:** The classification of incidents to specific use cases relies on automated labeling, which may have varying levels of confidence (such as low use-case label confidence for certain tenant screening incidents) [AIID #844](https://incidentdatabase.ai/cite/844/).
* **Hand-made risk crosswalk:** The policy coverage matrix relies on a manually curated cross-reference linking policy tags to broad risk domains, which may not capture every nuance of the regulatory texts.

## Query 2

> How did reported deepfake incidents change from 2020-2022 to 2023-2025, and what share were intentional misuse? Which enacted US state laws target deepfakes?

### Model alone

To understand the evolution of deepfakes, we must look at the transition from early generative models to the consumer-accessible, highly realistic generative AI tools that proliferated between late 2022 and 2025. 

Below is an overview of how deepfake incidents changed from the 2020–2022 period to the 2023–2025 period, the proportion of those incidents representing intentional misuse, and the landscape of enacted U.S. state laws targeting deepfakes.

---

### 1. Shift in Reported Deepfake Incidents: 2020–2022 vs. 2023–2025

The sheer volume of deepfake incidents shifted from a steady, linear rise to exponential growth between these two periods, primarily driven by the public release of open-source diffusion models, advanced voice-cloning tools, and low-cost face-swapping software.

*   **2020–2022 (The "Specialist" Era):** During this time, creating convincing deepfakes required a degree of technical expertise, specialized hardware (GPUs), and sizable datasets of target faces/voices. According to identity verification and cybersecurity firms, deepfakes grew steadily, but were largely confined to high-profile celebrity targets or highly targeted spear-phishing campaigns.
*   **2023–2025 (The "Commoditized" Era):** The availability of user-friendly generative AI tools democratized deepfake creation. 
    *   According to annual verification industry reports (such as those from identity-verification firm *Sumsub*), global deepfake detection incidents surged by **nearly 10x (1,000%) year-over-year between 2022 and 2023 alone**. 
    *   This trend accelerated through 2024 and 2025, with triple-digit percentage increases continuing globally. North America and Europe saw some of the highest increases in deepfake fraud attempts, with some sectors (like fintech and cryptocurrency platforms) reporting surges of over 1,500% in automated identity fraud attempts utilizing deepfakes.

---

### 2. Share of Intentional Misuse

While deepfakes are occasionally used for benign purposes (such as film dubbing, gaming, or historical education), **the vast majority of tracked, public-facing deepfake incidents are classified as intentional misuse.** 

Historically and currently, this misuse falls into three main categories:

1.  **Non-Consensual Intimate Imagery (NCII):** Historically, threat intelligence firms like *Sensity AI* estimated that **90% to 96% of all deepfake videos actively hosted on the internet were non-consensual pornography**, overwhelmingly targeting women. Despite the rise of financial fraud, NCII remained the dominant form of deepfake abuse by volume through 2025, facilitated by rapid-fire "nudification" applications.
2.  **Financial Fraud & Identity Theft:** In the commercial space, nearly **100% of deepfakes detected by security platforms represent intentional fraud.** Fraudsters use real-time face-swapping and voice-cloning to bypass Know Your Customer (KYC) video verification systems at financial institutions.
3.  **Political Disinformation and Scams:** High-profile deepfakes of political figures (such as the early 2024 robocall impersonating President Biden in New Hampshire) and celebrity-endorsement financial scams (e.g., fake videos of Elon Musk or Taylor Swift promoting investment schemes) represent highly targeted, intentional deceptions aimed at manipulating public opinion or stealing funds.

---

### 3. Enacted U.S. State Laws Targeting Deepfakes

Because federal legislation on deepfakes has historically faced gridlock or First Amendment hurdles, U.S. states took aggressive action. Enacted state laws generally fall into three categories: **elections**, **non-consensual pornography**, and **voice/likeness rights**. 

#### A. Election and Political Disinformation Laws
These laws restrict or require disclosures on manipulated media depicting political candidates close to an election.
*   **California (AB 2839 & AB 2655 - Enacted 2024):** Among the strictest in the nation, these bills expanded previous laws to block the distribution of deceptive, AI-generated campaign materials within 120 days of an election and required large online platforms to remove such content upon complaint (though elements have faced immediate First Amendment court challenges). 
*   **Texas (SB 751 - Enacted 2019/2021):** One of the earliest bans, making it a misdemeanor to create or distribute a deepfake video intended to injure a candidate or influence an election within 30 days of voting.
*   **Minnesota (SF 2909 - Enacted 2023):** Criminalizes the distribution of deepfakes within 90 days of an election if done without consent and with the intent to influence the outcome.
*   **Michigan (HB 4129/4130 - Enacted 2023):** Imposes criminal penalties for distributing deceptive media of political candidates within 90 days of an election unless a clear disclaimer is attached.
*   **Other States:** Florida (SB 850, 2024), Washington (SB 5152, 2023), Utah, Arizona, Colorado, Wisconsin, and Indiana have also enacted mandatory disclosure laws or outright bans on deceptive campaign deepfakes.

#### B. Non-Consensual Deepfake Pornography Laws
More than 30 states have enacted criminal or civil penalties for creating or distributing sexually explicit deepfakes without the victim's consent.
*   **California (AB 602 - Enacted 2019):** Gives victims a private right of action to sue creators/distributors of non-consensual deepfake pornography for damages.
*   **New York (S1047 / A10428 - Enacted 2020/2021):** Created a civil cause of action for the unlawful dissemination of a digital replica of an individual's private parts or sexually explicit conduct.
*   **Minnesota (SF 2909 - Enacted 2023):** Establishes felony-level criminal penalties for sharing deepfake pornography without consent.
*   **Virginia (VA Code § 18.2-386.2):** Explicitly updated its criminal non-consensual pornography laws to include "falsely created" or computer-generated explicit images.
*   **Georgia, Illinois, Hawaii, Texas, and Idaho** are among the dozens of other states that have updated their penal codes to ensure artificial or synthetic explicit media is covered under revenge-porn and harassment statutes.

#### C. Voice, Likeness, and Right of Publicity (Digital Replicas)
These laws target the unauthorized commercial use of an individual’s voice or likeness via AI-generated "digital replicas."
*   **Tennessee ELVIS Act (Enacted 2024):** The *Ensuring Likeness Voice and Image Security (ELVIS) Act* updated Tennessee's protection of personal rights to explicitly protect artists and individuals from unauthorized AI voice cloning and likeness replication, marking a major milestone for the music industry.
*   **California (AB 2602 - Enacted 2024):** Requires contracts to have explicit, specific consent before an employer can use an AI-generated digital replica of a performer’s voice or likeness in place of actual performance.

### Agent

# Reported Deepfake Incidents and US State Legislative Responses

*Scope · Incidents: Synthetic media and deepfakes, 2020–2025, worldwide (AIID has no reliable location field) · Policies: United States*


**Summary.** Reported deepfake incidents surged from 43 in 2020–2022 to 496 in 2023–2025, with peak reporting occurring in 2025. The vast majority of these incidents involved intentional misuse, which rose from 69.8% to 88.1% of cases between the two periods. To counter these threats, US states have enacted various laws, primarily targeting nonconsensual sexual media and election-related deceptive content. While the analyzed incident dataset spans worldwide cases, the policies reviewed are limited to US state jurisdictions.

## The most common reported failures

*   **Non-consensual sexual media:** Perpetrators used deepfake generation apps and social media to create and circulate explicit images of real individuals without their consent [AIID search results]. This type of abuse is classified under the "Malicious Actors & Misuse" risk domain, which represented 78.0% of deepfake incidents in 2023–2025. Examples include teenage girls targeted at Westfield High School [AIID #597](https://incidentdatabase.ai/cite/597/) and Aledo High School [AIID #799](https://incidentdatabase.ai/cite/799/), and celebrity Taylor Swift [AIID #632](https://incidentdatabase.ai/cite/632/).
*   **Financial fraud and impersonation:** Malicious actors utilized voice cloning and video deepfakes to impersonate corporate executives and public figures to steal funds or execute scams [AIID search results]. Also falling under the dominant "Malicious Actors & Misuse" domain, notable cases include a finance employee at Arup tricked into transferring $25 million via a deepfake CFO call [AIID #634](https://incidentdatabase.ai/cite/634/), and scammers impersonating Italian Defense Minister Guido Crosetto [AIID #927](https://incidentdatabase.ai/cite/927/).
*   **Political and strategic deception:** Bad actors deployed synthetic media and AI-generated personas to spread false narratives and manipulate elections or conflicts [AIID search results]. This activity falls under "Misinformation," which increased to 12.3% of reported incidents in 2023–2025. Examples include a deepfake video of Ukrainian President Volodymyr Zelenskyy telling troops to surrender [AIID #198](https://incidentdatabase.ai/cite/198/), and John Mark Dougan using AI tools to run a network of 160+ fake news sites from Russia [AIID #701](https://incidentdatabase.ai/cite/701/).
*   **AI-generated journalistic content:** Organizations deployed synthetic media tools to generate uncredited or deceptive content, which falls under false or misleading information [AIID search results]. For example, Sports Illustrated reportedly published articles authored by fictitious AI-generated profiles [AIID #616](https://incidentdatabase.ai/cite/616/).
*   **Platform-generated non-consensual media:** Generative features on platforms produced harmful outputs directly through user interactions, categorized under "Discrimination and Toxicity" (which fell to 4.0% of incidents in 2023–2025). A reported example includes xAI's Grok generating nonconsensual sexualized images of adults and minors in reply prompts [AIID #1329](https://incidentdatabase.ai/cite/1329/).

## How reporting has changed

Deepfake incident reports increased significantly from 43 incidents in 2020–2022 to 496 incidents in 2023–2025, out of 539 reported incidents in scope, 2020–2025. The peak full year was 2025, with 248 incidents. Over these periods, intentional misuse grew from 69.8% of incidents (30 out of 43) in 2020–2022 to 88.1% of incidents (437 out of 496) in 2023–2025. The largest risk domain in 2020–2022 was Malicious Actors & Misuse (27 of 43, 63%), which remained the largest risk domain in 2023–2025 (387 of 496, 78%).

| Year | Reported incidents |
|---|---|
| 2020 | 14 |
| 2021 | 5 |
| 2022 | 24 |
| 2023 | 81 |
| 2024 | 167 |
| 2025 | 248 |

- 539 reported incidents in scope, 2020–2025.
- Peak full year: 2025, with 248 incidents.
- 2023–2025: 496 incidents; 2020–2022: 43 incidents.
- Largest risk domain in 2023–2025: Malicious Actors & Misuse (387 of 496, 78%).
- Largest risk domain in 2020–2022: Malicious Actors & Misuse (27 of 43, 63%).

## Policies that address these risks

While the analyzed incident data is worldwide due to the lack of a reliable location field in the AIID, the policy database is focused on US jurisdictions.

| Policy | Authority | Status (date) | What it requires | Addresses |
| :--- | :--- | :--- | :--- | :--- |
| Minnesota HF 1370 [AGORA #1517](https://agora.eto.tech/instrument/1517) | Minnesota | Enacted (May 26, 2023) | Criminalizes the nonconsensual dissemination of deepfake sexual images and the use of deepfakes to influence elections, imposing penalties including imprisonment and fines [AGORA #1517](https://agora.eto.tech/instrument/1517). | Malicious Actors & Misuse, Misinformation, Discrimination/Toxicity [AGORA #1517](https://agora.eto.tech/instrument/1517) |
| Washington Senate Bill 5152 [AGORA #1538](https://agora.eto.tech/instrument/1538) | Washington | Enacted (July 23, 2023) | Defines synthetic media and allows political candidates harmed by deceptive campaign-related synthetic media to seek injunctive relief or damages [AGORA #1538](https://agora.eto.tech/instrument/1538). | Misinformation, Discrimination/Toxicity [Coverage matrix, AGORA #1538] |
| Utah House Bill 148 [AGORA #1532](https://agora.eto.tech/instrument/1532) | Utah | Enacted (March 13, 2024) | Prohibits the knowing distribution of computer-generated counterfeit intimate images without consent, establishing misdemeanor or felony liability [AGORA #1532](https://agora.eto.tech/instrument/1532). | Malicious Actors & Misuse, Misinformation, Discrimination/Toxicity [AGORA #1532](https://agora.eto.tech/instrument/1532) |
| Wisconsin Act 2023-123 [AGORA #1460](https://agora.eto.tech/instrument/1460) | Wisconsin | Enacted (March 21, 2024) | Requires audio and video communications containing synthetic media and express or issue advocacy to carry clear AI-generation disclosures at the beginning and end [AGORA #1460](https://agora.eto.tech/instrument/1460). | Misinformation [AGORA #1460](https://agora.eto.tech/instrument/1460) |
| Colorado House Bill 1147 [AGORA #1402](https://agora.eto.tech/instrument/1402) | Colorado | Enacted (May 24, 2024) | Regulates undisclosed deepfakes in communications concerning candidates for elective office to protect election integrity [AGORA #1402](https://agora.eto.tech/instrument/1402). | Misinformation, AI system safety [Coverage matrix, AGORA #1402] |
| Arizona Senate Bill 1359 [AGORA #1485](https://agora.eto.tech/instrument/1485) | Arizona | Enacted (May 29, 2024) | Prohibits creating and distributing deceptive synthetic media messages of political candidates within 90 days of an election without clear AI disclosures [AGORA #1485](https://agora.eto.tech/instrument/1485). | Misinformation [AGORA #1485](https://agora.eto.tech/instrument/1485) |
| Idaho House Bill 575 [AGORA #1499](https://agora.eto.tech/instrument/1499) | Idaho | Enacted (July 1, 2024) | Criminalizes the knowing disclosure of explicit synthetic media without consent when it causes distress or is used for extortion [AGORA #1499](https://agora.eto.tech/instrument/1499). | Malicious Actors & Misuse, Privacy & Security [Coverage matrix, AGORA #1499] |
| New Hampshire House Bill 1432 [AGORA #1431](https://agora.eto.tech/instrument/1431) | New Hampshire | Enacted (July 19, 2024) | Criminalizes the knowing creation or distribution of harmful deepfakes intended to harass, defame, extort, or cause financial/reputational harm [AGORA #1431](https://agora.eto.tech/instrument/1431). | Malicious Actors & Misuse [AGORA #1431](https://agora.eto.tech/instrument/1431) |
| California AB 2885 [AGORA #1551](https://agora.eto.tech/instrument/1551) | California | Enacted (September 28, 2024) | Requires the Secretary of Government Operations to evaluate the impact of deepfakes and digital content forgery, and study digital content provenance [AGORA #1551](https://agora.eto.tech/instrument/1551). | Malicious Actors & Misuse, Privacy & Security [AGORA #1551](https://agora.eto.tech/instrument/1551) |

| Risk domain | Incidents | Enacted | Proposed | Defunct | Coverage |
|---|---|---|---|---|---|
| Malicious Actors & Misuse | 414 | 11 | 2 | 13 | enacted |
| Misinformation | 62 | 38 | 7 | 18 | enacted |
| Discrimination and Toxicity | 29 | 39 | 7 | 19 | enacted |
| Privacy & Security | 7 | 27 | 4 | 19 | enacted |
| Socioeconomic & Environmental Harms | 3 | 5 | 2 | 7 | enacted |
| AI system safety, failures, and limitations | 1 | 13 | 2 | 11 | enacted |

*Coverage method: A policy counts for a risk domain if it is about the use case (a keyword in its name or summaries, or 3+ mentions in its text) and carries an AGORA harm or risk-factor tag that the hand-made crosswalk maps to that domain. Only annotated AGORA documents have tags. Defunct documents are not in force.*

For risk domains such as Socioeconomic & Environmental Harms and AI System Safety, very few or zero enacted state policies specifically regulate deepfakes beyond election and privacy rules in the provided dataset [Coverage matrix, AGORA].

## What this data can't tell you

*   **Reported counts are not rates:** The incident counts reflect cases curated and published by AIID editors, rather than representing true underlying occurrence rates.
*   **Partial latest year:** The data for 2025 is partial and does not cover the complete calendar year, meaning the 2023–2025 totals are incomplete.
*   **AGORA is mostly US:** The policy database is heavily weighted toward US jurisdictions, which limits global coverage and does not reflect international legislative actions.
*   **Small counts:** Some risk domains contain extremely small incident counts (e.g., Privacy & Security or Socioeconomic & Environmental Harms), making statistical trends in those categories less reliable.
*   **LLM-assigned use-case labels:** The categorization of incidents and mapping of use cases may rely on LLM-assigned labels, introducing potential errors or misclassifications.
*   **Hand-made risk crosswalk:** Policy coverage analysis relies on a hand-made risk crosswalk that maps AGORA harm or risk-factor tags to broad risk domains, which may omit nuances of specific legislative texts.

## Query 3

> For content recommendation and moderation systems, which kinds of reported AI failure have no enacted US policy addressing them?

### Model alone

In the United States, there is currently **no comprehensive federal legislation** that directly regulates AI-driven content recommendation or automated moderation systems. 

While there have been numerous congressional hearings, executive orders, and proposed bills, the U.S. relies heavily on **Section 230 of the Communications Decency Act of 1996**. Rather than regulating AI failures, Section 230 largely immunizes platforms from liability for both the user-generated content they recommend and their "good faith" efforts to moderate content.

Consequently, several widely documented categories of AI failures in content recommendation and moderation have **no enacted federal policy** addressing them. The most prominent of these failures include:

---

### 1. Algorithmic Amplification of Extremism and Radicalization
*   **The AI Failure:** Recommendation engines are optimized for user engagement (clicks, watch time, shares). Because divisive, sensationalist, or extreme content often drives the highest engagement, AI algorithms naturally recommend increasingly radical content to users, pulling them into "rabbit holes" of conspiracy theories or violent extremism.
*   **The Policy Gap:** There is no federal law restricting how platforms program their recommendation engines or prohibiting them from optimizing for engagement at the expense of safety. The Supreme Court (e.g., in *Twitter, Inc. v. Taamneh* and *Gonzalez v. Google*) declined to hold tech companies liable under anti-terrorism laws for algorithmic recommendations, leaving this failure entirely unregulated at the federal level.

### 2. Algorithmic Bias and Demographically Discriminatory Moderation
*   **The AI Failure:** Automated content moderation systems consistently exhibit demographic bias. Studies show AI is more likely to flag African American Vernacular English (AAVE) as offensive or toxic compared to standard English. Similarly, AI moderation often over-censors marginalized groups (such as LGBTQ+ creators discussing their lived experiences) through "shadowbanning" or false-positive community guideline violations.
*   **The Policy Gap:** While federal civil rights laws prohibit discrimination in housing, employment, and public accommodations, they do not apply to automated social media moderation. There is no federal law requiring platforms to audit their moderation AI for demographic bias, nor is there a legal remedy for users who are wrongfully censored due to algorithmic bias. 

### 3. Exploitative Recommendation Patterns Targeting Youth Mental Health
*   **The AI Failure:** Recommendation algorithms on platforms like TikTok and Instagram have been shown to deliver harmful content—such as posts promoting eating disorders, self-harm, or extreme body dysmorphia—to vulnerable minors who show initial interest in benign fitness or diet topics.
*   **The Policy Gap:** The Children’s Online Privacy Protection Act (COPPA) only regulates *data collection* for children under 13; it does not regulate the algorithms that serve content. While the **Kids Online Safety Act (KOSA)** has been proposed to establish a "duty of care" preventing platforms from recommending harmful content to minors, it **has not been enacted into federal law**. State-level attempts to regulate this (such as California's Age-Appropriate Design Code) face severe legal challenges on First Amendment grounds.

### 4. Algorithmic "Black Boxes" and the Denial of Researcher Access
*   **The AI Failure:** Because social media algorithms are proprietary, external researchers, civil society groups, and the public cannot audit how these AI systems make decisions. This lack of transparency makes it impossible to independently verify the scale of algorithmic harms or the efficacy of a platform's moderation tools.
*   **The Policy Gap:** Unlike the European Union’s Digital Services Act (DSA), which legally mandates that very large platforms provide vetted researchers with access to their data and algorithms, the U.S. has no such law. The **Platform Accountability and Transparency Act (PATA)** has been introduced in Congress to address this, but it has not been enacted.

### 5. Systematic "Collateral Damage" (Over-Moderation and Censorship of Legitimate Speech)
*   **The AI Failure:** To police vast amounts of content, platforms rely on automated classifier AI to detect hate speech, graphic violence, or misinformation. These systems frequently fail to understand context, satire, news reporting, or political counter-speech, resulting in the automated takedown of legitimate journalism, human rights documentation, and political dissent.
*   **The Policy Gap:** There is no federal "due process" law for internet users. Platforms are legally permitted to take down any content they wish under Section 230's "Good Samaritan" provision. Users have no federal legal right to appeal automated takedowns, nor are platforms legally required to provide a human-in-the-loop review process.

### 6. Recommendation and Propagation of Deepfakes and Synthetic Misinformation
*   **The AI Failure:** Generative AI has made it easy to create hyper-realistic deepfakes. When these are uploaded to social media, recommendation algorithms boost them due to their viral nature, accelerating the spread of political disinformation or non-consensual synthetic media before human moderators can intervene.
*   **The Policy Gap:** While some states have passed laws targeting election-related deepfakes or non-consensual deepfake pornography, there is **no federal law** regulating how recommendation systems amplify synthetic media. The Federal Trade Commission (FTC) can police deceptive commercial practices, but political and social deepfakes boosted by AI algorithms fall outside their purview.

---

### Why is there a policy vacuum in the US?
The lack of enacted policy on these failures is driven by two primary forces:
1.  **The First Amendment:** In the U.S., content moderation and recommendation are legally viewed as a platform's exercise of "editorial discretion" (akin to a newspaper deciding which letters to the editor to print). The Supreme Court's rulings (most recently in the *NetChoice* cases of 2024) suggest that government attempts to mandate how algorithms recommend or moderate content run a high risk of violating the First Amendment.
2.  **Congressional Gridlock:** While there is bipartisan appetite to hold "Big Tech" accountable, Democrats and Republicans disagree on the core issue. Democrats generally want policies targeting AI's failure to curb hate speech and misinformation, while Republicans generally want policies targeting AI's failure of "censorship" (alleging algorithmic bias against conservative viewpoints). This division has prevented any major regulatory bill from passing.

### Agent

# Gaps in US Policy for Content Recommendation and Moderation AI Failures

*Scope · Incidents: Content recommendation and moderation, 1983–2026, worldwide (AIID has no reliable location field) · Policies: United States*


**Summary.** For content recommendation and moderation systems, reported AI failures falling under the risk domains of 'Malicious Actors & Misuse' and 'Socioeconomic & Environmental Harms' have no enacted US federal or state policy addressing them [AGORA coverage_matrix]. These unaddressed domains encompass real-world failures such as coordinated disinformation networks, nonconsensual deepfake pornography, and automated ad system fraud [AIID #968](https://incidentdatabase.ai/cite/968/) [AIID #632](https://incidentdatabase.ai/cite/632/) [AIID #1268](https://incidentdatabase.ai/cite/1268/). While some US states have enacted policies targeting risks like discrimination, misinformation, and safety, these legislative efforts do not cover all categories of reported harms [AGORA coverage_matrix]. While the analyzed policies are limited to the United States, the underlying AI incidents are documented worldwide because the AIID has no reliable location field.

## What has gone wrong

- **Disinformation, surveillance, and influence at scale**: There are 72 matched incidents involving coordinated or large-scale manipulation of content networks, primarily representing intentional state-backed or actor-driven operations [search_incidents filters]. Examples include the Moscow-based `Pravda` disinformation network infiltrating AI chatbot models with pro-Kremlin narratives [AIID #968](https://incidentdatabase.ai/cite/968/), manipulated media targeting the 2023 Turkish presidential election [AIID #544](https://incidentdatabase.ai/cite/544/), and AI-generated media deployed to disrupt the 2024 U.S. general election [AIID #884](https://incidentdatabase.ai/cite/884/).
- **False or misleading information**: There are 55 matched incidents featuring autocomplete defamation, generative poll outputs, or synthetic media spreading false narratives [search_incidents filters]. Examples include Google's autocomplete leading to defamatory search suggestions [AIID #45](https://incidentdatabase.ai/cite/45/), xAI's Grok chatbot injecting unsolicited claims about "white genocide" into unrelated queries [AIID #1072](https://incidentdatabase.ai/cite/1072/), and an allegedly AI-generated image of an explosion near the Pentagon causing market dips and public confusion [AIID #543](https://incidentdatabase.ai/cite/543/).
- **Lack of capability or robustness**: There are 38 matched incidents resulting from technical translation or moderation failures due to software limitations or poor generalization [search_incidents filters]. Examples include Facebook's translation software translating "Good morning" into "hurt them" and leading to a user's arrest [AIID #72](https://incidentdatabase.ai/cite/72/), and YouTube's hate speech detection algorithms falsely banning chess content for using the words "black" and "white" [AIID #144](https://incidentdatabase.ai/cite/144/).
- **Fraud, scams, and targeted manipulation**: There are 35 matched incidents involving deepfakes, impersonation, or ad-system exploitation for financial or personal harm [search_incidents filters]. Examples include nonconsensual deepfake pornography of Taylor Swift going viral on X [AIID #632](https://incidentdatabase.ai/cite/632/), internal Meta documents showing automated ad systems generating revenue from fraudulent scam impressions [AIID #1268](https://incidentdatabase.ai/cite/1268/), and fake social media ads impersonating officials to promote crypto webinar scams [AIID #1413](https://incidentdatabase.ai/cite/1413/).
- **Exposure to toxic content**: There are 32 matched incidents where recommendation or chatbot systems generated or propagated offensive, violent, or self-harm material [search_incidents filters]. Examples include YouTube's recommendation algorithms exposing children to disturbing content on the YouTube Kids app [AIID #1](https://incidentdatabase.ai/cite/1/), TikTok's algorithm allegedly exposing minors to content promoting eating disorders and self-harm [AIID #869](https://incidentdatabase.ai/cite/869/), and xAI's Grok chatbot generating antisemitic posts praising Hitler in response to flood news [AIID #1146](https://incidentdatabase.ai/cite/1146/).

## How reporting has changed

There were 149 reported incidents in scope from 2006–2026, with the peak full year being 2020 with 28 incidents [AIID/AGORA count_incidents]. Reports declined from 59 incidents in 2020–2022 to 35 incidents in 2023–2025 [AIID/AGORA compare_periods]. The largest risk domain shifted from Discrimination and Toxicity in 2020–2022 (20 of 59, 34%) to Misinformation in 2023–2025 (12 of 35, 34%) [AIID/AGORA compare_periods]. The 3 incidents recorded in 2026 so far (data ends 2026-10-30) represent a partial year that is not comparable to full years [AIID/AGORA count_incidents].

| Year | Reported incidents |
|---|---|
| 2006 | 1 |
| 2008 | 1 |
| 2011 | 2 |
| 2012 | 1 |
| 2013 | 3 |
| 2014 | 1 |
| 2015 | 8 |
| 2016 | 7 |
| 2017 | 12 |
| 2018 | 8 |
| 2019 | 8 |
| 2020 | 28 |
| 2021 | 20 |
| 2022 | 11 |
| 2023 | 10 |
| 2024 | 15 |
| 2025 | 10 |
| 2026 (partial) | 3 |

- 149 reported incidents in scope, 2006–2026.
- Peak full year: 2020, with 28 incidents.
- 2023–2025: 35 incidents; 2020–2022: 59 incidents.
- Largest risk domain in 2023–2025: Misinformation (12 of 35, 34%).
- Largest risk domain in 2020–2022: Discrimination and Toxicity (20 of 59, 34%).
- 2026 so far (data ends 2026-10-30): 3 incidents. A partial year: not comparable to full years.

## Policies that address these risks

| Policy | Authority | Status (date) | What it requires | Addresses |
|---|---|---|---|---|
| Utah HB 464 (Social Media Amendments) | Utah | Enacted (March 13, 2024) | Permits minors or parents to sue social media companies for mental health harms from algorithmically curated services unless companies limit minor usage, require parental consent, and disable engagement-driven features, while exempting companies from liability for user posts or moderation decisions | Privacy, safety, and human-computer interaction failure risks in recommendation and moderation systems [AGORA #5256](https://agora.eto.tech/instrument/5256) |
| Washington Senate Bill 5838 | Washington | Enacted (March 18, 2024) | Establishes an AI task force to formulate recommendations on racial equity, civil liberties protections, human oversight, data privacy, and security testing | Systemic equity and safety risks [AGORA #1539](https://agora.eto.tech/instrument/1539) |
| Colorado HB 24-1468 | Colorado | Enacted (June 6, 2024) | Requires an AI task force to develop a code of conduct, ethical evaluation frameworks, quantitative benchmarks, and policy recommendations | Algorithmic discrimination and toxicity risks [AGORA #1403](https://agora.eto.tech/instrument/1403) |
| New Hampshire H1688 | New Hampshire | Enacted (July 22, 2024) | Mandates human review of irreversible AI-driven recommendations or decisions by state agencies, alongside disclosures of AI-generated content and interaction notifications | System safety, reliability, and human oversight risks [AGORA #2210](https://agora.eto.tech/instrument/2210) |
| Texas HB 149 (Artificial Intelligence Council) | Texas | Enacted (January 1, 2026) | Creates the Texas Artificial Intelligence Council to evaluate state AI systems, ensure ethical development, and recommend regulations to protect public safety and individual rights | Overarching AI safety and governance risks [AGORA #4809](https://agora.eto.tech/instrument/4809) |
| Colorado HB 1263 (Conversational Artificial Intelligence Service Operator Requirements) | Colorado | Enacted (June 1, 2026) | Requires operators of public conversational AI to disclose AI status, implement protections for minors against sexually explicit material and emotional dependence, and mandate suicide/self-harm crisis protocols with annual reporting | Safety, failure, and limitation risks in AI outputs [AGORA #6741](https://agora.eto.tech/instrument/6741) |

| Risk domain | Incidents | Enacted | Proposed | Defunct | Coverage |
|---|---|---|---|---|---|
| Discrimination and Toxicity | 55 | 1 | 1 | 5 | enacted |
| AI system safety, failures, and limitations | 35 | 1 | 2 | 2 | enacted |
| Misinformation | 24 | 1 | 1 | 4 | enacted |
| Malicious Actors & Misuse | 16 | 0 | 0 | 0 | none found |
| Socioeconomic & Environmental Harms | 8 | 0 | 0 | 0 | none found |
| Human-Computer Interaction | 4 | 0 | 1 | 2 | proposed only |
| Privacy & Security | 3 | 1 | 2 | 3 | enacted |

*Coverage method: A policy counts for a risk domain if it is about the use case (a keyword in its name or summaries, or 3+ mentions in its text) and carries an AGORA harm or risk-factor tag that the hand-made crosswalk maps to that domain. Only annotated AGORA documents have tags. Defunct documents are not in force.*

There are currently no enacted US federal or state policies addressing reported AI failures in the risk domains of 'Malicious Actors & Misuse' (16 incidents) and 'Socioeconomic & Environmental Harms' (8 incidents) [AGORA coverage_matrix]. Additionally, failures related to 'Human-Computer Interaction' (4 incidents) are only addressed by proposed, rather than enacted, policies [AGORA coverage_matrix].

## What this data can't tell you

- **Reported counts are not rates**: The incident numbers represent publicly reported or submitted cases and do not reflect the true rate or complete volume of AI failures [AIID/AGORA count_incidents].
- **Partial latest year**: The data for the latest year (2026) is partial and incomplete, meaning counts from this period are not comparable to full years [AIID/AGORA count_incidents].
- **Lack of direct policy tracking**: The incident database tools do not track or contain information regarding enacted US policies, meaning policy gaps must be determined using a separate hand-made crosswalk mapping.
- **Global scope of incidents**: While the policies analyzed are limited strictly to US federal and state jurisdictions, the AI incidents themselves are documented worldwide because the AI Incident Database lacks a reliable location field.
- **Classification limitations**: Risk subdomains are assigned based on high-level classifications, which may not capture the full nuances of multi-domain failures or minor variations in local implementations.
