# Detailed Analysis of Data Corpora for Wrestling LLM Fine-Tuning

This document provides a detailed breakdown of the types of data required to fine-tune Small Language Models (SLMs) for the professional wrestling domain. It expands on the categories identified previously, exploring sub-categories, content characteristics, potential sources, and considerations for data volume and composition.

## Category 1: Promo Scripts and Transcripts

Promos are a cornerstone of professional wrestling, establishing character, advancing storylines, and engaging the audience. Access to a diverse and well-structured corpus of promo material is critical.

### Sub-Categories:

1.  **Heel Turn Promos:**
    *   **Content Characteristics:** Speeches where a wrestler transitions from a fan favorite (face) to a villain (heel). Often involve betrayal, expressions of bitterness, arrogance, or a new, aggressive demeanor. Key for understanding character arc shifts.
    *   **Potential Sources:** Transcripts from weekly shows (e.g., WWE Raw, SmackDown, AEW Dynamite), pay-per-view events, historical wrestling archives, fan transcription sites.
    *   **Estimated Data Impact:** A collection of 100-200 distinct, high-quality heel turn promos (ranging from 200-1000 words each) would be impactful for teaching this specific narrative beat.

2.  **Face Turn Promos:**
    *   **Content Characteristics:** Speeches where a wrestler transitions from a villain to a fan favorite. Often involve apologies, saving another wrestler, declarations of fighting for the fans, or standing up to a bully. Crucial for understanding redemption arcs.
    *   **Potential Sources:** Similar to heel turn promos – show transcripts, PPVs, archives.
    *   **Estimated Data Impact:** 100-200 distinct face turn promos would provide a good dataset for this arc.

3.  **Championship Win/Challenge Promos:**
    *   **Content Characteristics:** Expressions of ambition, declarations of intent to win a title, or triumphant speeches after a championship victory. Often involve calling out opponents or staking a claim.
    *   **Potential Sources:** Post-match interviews, in-ring segments from shows/PPVs.
    *   **Estimated Data Impact:** 200-300 promos in this category, covering various championships (world, mid-card, tag team), would be beneficial.

4.  **Storyline Advancement Promos:**
    *   **Content Characteristics:** General promos that build feuds, explain motivations, issue warnings, or add layers to ongoing narratives without necessarily being a turn or directly about a championship.
    *   **Potential Sources:** Weekly show transcripts are the primary source.
    *   **Estimated Data Impact:** This would be the largest sub-category, ideally 1000+ diverse promos to cover a wide range of interpersonal dynamics and storyline developments.

5.  **Retirement/Farewell Promos:**
    *   **Content Characteristics:** Emotional speeches where a wrestler announces their departure from in-ring competition. Often reflective, thanking fans, and sometimes leaving the door open for a return or being interrupted to start a new angle.
    *   **Potential Sources:** Show transcripts, PPV segments.
    *   **Estimated Data Impact:** 50-100 high-quality retirement promos could capture the specific tone and themes.

6.  **Debut/Return Promos:**
    *   **Content Characteristics:** Promos introducing a new character or re-introducing a returning one. Focus on establishing their gimmick, intentions, and impact.
    *   **Potential Sources:** Show transcripts, PPV surprise appearances.
    *   **Estimated Data Impact:** 100-150 debut/return promos to cover various entry styles.

7.  **Catchphrase Repetition/Emphasis Promos:**
    *   **Content Characteristics:** Segments where a wrestler heavily emphasizes their signature catchphrases. Useful for the model to learn and correctly attribute these key identifiers.
    *   **Potential Sources:** Can be extracted from various promo types; specific compilation scripts might be needed.
    *   **Estimated Data Impact:** Several hundred examples of catchphrases being delivered in context (even short clips/segments) would be important for character voice.

### General Considerations for Promo Data:

*   **Speaker Identification:** Crucial to have clear markers of who is speaking each line.
*   **Contextual Metadata:** Information like the date, event, involved wrestlers, and ongoing storyline can be highly beneficial for the model to learn context.
*   **Emotional Tone Annotation (Advanced):** If possible, annotating promos with emotional tones (e.g., angry, sarcastic, triumphant) could help in more nuanced persona generation.
*   **Volume:** Aiming for a total of at least 2,000-5,000 clean, well-attributed promo transcripts of varying lengths would form a strong foundation for this category. The more high-quality data, the better, especially for capturing a wide range of characters and eras.

## Category 2: Match Commentary Transcripts

Match commentary provides the soundtrack to in-ring action, explaining moves, telling stories, and conveying character dynamics from the perspective of announcers. This data is key for models that might generate match descriptions or adopt announcer personas.

### Sub-Categories:

1.  **Play-by-Play (PBP) Announcer Commentary:**
    *   **Content Characteristics:** Focuses on calling the in-ring action, naming moves, describing sequences, and maintaining the flow of the match narrative. Tends to be more objective, though excitement levels vary.
    *   **Examples:** Jim Ross, Mauro Ranallo, Michael Cole (PBP aspects), Excalibur.
    *   **Potential Sources:** Full match transcripts from TV shows and PPVs. Requires careful transcription and speaker attribution.
    *   **Estimated Data Impact:** Transcripts from 200-300 full matches, with clear PBP attribution, would be a good start. More is better to capture different styles and eras.

2.  **Color Commentator Commentary:**
    *   **Content Characteristics:** Provides analysis, character insights, storyline context, and often expresses bias (pro-heel or pro-face). More about the "why" and the "story" than the "what." Often injects personality and humor/outrage.
    *   **Examples:** Jerry "The King" Lawler, Bobby "The Brain" Heenan, Corey Graves, Taz (as color commentator), Paul Heyman (when on commentary).
    *   **Potential Sources:** Same as PBP – full match transcripts. Distinguishing between PBP and color commentary in transcripts is vital.
    *   **Estimated Data Impact:** Similar to PBP, transcripts from 200-300 matches, focusing on the color commentator's contributions.

3.  **Heel-Biased Color Commentary:**
    *   **Content Characteristics:** Specific type of color commentary that consistently favors and makes excuses for heel wrestlers, while criticizing faces. Important for capturing a specific announcer persona.
    *   **Potential Sources:** Matches featuring commentators known for this style (e.g., Jesse Ventura, Corey Graves, 90s Jerry Lawler).
    *   **Estimated Data Impact:** 100-150 matches with strong heel-biased commentary would help isolate this style.

4.  **Face-Biased Color Commentary (Less Common as a Deliberate Style but Exists):**
    *   **Content Characteristics:** Commentary that overtly roots for face wrestlers, praises their virtues, and criticizes heels. Often more subtle than overt heel bias but important for balance.
    *   **Potential Sources:** Matches with specific commentators or during specific eras/storylines.
    *   **Estimated Data Impact:** 50-100 matches demonstrating this style.

5.  **Specific Move/Sequence Calls:**
    *   **Content Characteristics:** Announcers calling signature moves, high spots, or critical sequences in a match. Often involves heightened excitement or specific phrasing.
    *   **Potential Sources:** Can be extracted from PBP commentary. May require specific tagging or searching for move names within transcripts.
    *   **Estimated Data Impact:** A collection of several hundred to a few thousand distinct move calls, linked to the moves themselves if possible, would be very valuable for a model needing to describe action.

6.  **Storytelling Commentary:**
    *   **Content Characteristics:** Announcers discussing the history between wrestlers, the implications of the match, character motivations, or how the current action ties into a larger narrative.
    *   **Potential Sources:** Extracted from both PBP and color commentary, often during slower points in a match or in pre/post-match segments.
    *   **Estimated Data Impact:** Segments from 300-500 matches focusing on these narrative elements.

### General Considerations for Commentary Data:

*   **Accurate Speaker Attribution:** Essential to differentiate between PBP, color commentators, and any guest commentators.
*   **Timestamping (Ideal):** If possible, aligning commentary with specific match moments or video timestamps would be incredibly valuable for future multi-modal applications, though harder to acquire.
*   **Wrestling Era/Style Diversity:** Commentary styles have evolved. Capturing data from different eras (e.g., Attitude Era, Ruthless Aggression, current) and promotions (WWE, AEW, NJPW with English commentary) would create a more versatile model.
*   **Volume:** A corpus of 500-1000 fully transcribed matches, with clear speaker roles, would provide a robust dataset. This translates to many thousands of individual commentary lines.

## Category 3: Character Dialogues and Biographies

This category focuses on data that defines individual wrestling characters, their histories, motivations, and relationships, beyond what might be captured in promos or match commentary alone. This is crucial for fine-tuning models that need a deep understanding of specific personas or for generating content related to character backstories.

### Sub-Categories:

1.  **Official Character Profiles/Biographies:**
    *   **Content Characteristics:** Text from official sources (e.g., WWE.com, AEWrestling.com, old program magazines) describing a wrestler's gimmick, history, achievements, and key traits.
    *   **Potential Sources:** Official wrestling promotion websites, archived wrestling magazines, official encyclopedias or books.
    *   **Estimated Data Impact:** Profiles for 200-500 wrestlers, if available, would provide a good factual baseline for character attributes.

2.  **Fan-Created Wiki Entries (e.g., Wikipedia, Fandom Wikis):**
    *   **Content Characteristics:** Detailed, often community-curated information on a wrestler's career, storyline involvements, gimmick changes, move sets, and relationships. Can be very comprehensive but requires careful vetting for accuracy and neutrality (or deliberate selection for specific perceived personas).
    *   **Potential Sources:** Wikipedia (wrestling-related articles), specialized wrestling wikis (e.g., Pro Wrestling Wiki on Fandom), Cagematch.net (for career histories, though less prose-heavy).
    *   **Estimated Data Impact:** Data from several hundred comprehensive wiki pages, focusing on the prose sections describing character and storyline elements. Quality control is key here.

3.  **Wrestler Interviews (Out-of-Character or Kayfabe):**
    *   **Content Characteristics:** Transcripts or summaries of interviews where wrestlers discuss their characters, careers, philosophies, or specific storylines. "Shoot" interviews (out-of-character) can provide insight into the real person's thinking about their persona, while kayfabe interviews maintain the character's illusion.
    *   **Potential Sources:** Wrestling news websites that transcribe interviews, YouTube channels dedicated to wrestler interviews (transcription would be needed), wrestling podcasts, autobiographies.
    *   **Estimated Data Impact:** Transcripts of 100-200 insightful interviews, varying in length. Distinguishing between kayfabe and shoot interviews in the dataset is important.

4.  **Dialogue from Wrestling Video Games:**
    *   **Content Characteristics:** Scripted dialogue for characters in story modes or career modes of wrestling video games. This is often professionally written to reflect established personas.
    *   **Potential Sources:** Game script FAQs, direct extraction from game files if possible, fan transcriptions of story modes.
    *   **Estimated Data Impact:** Dialogue scripts from 5-10 wrestling games with extensive story modes could yield a significant amount of character-specific lines.

5.  **Character Interactions in Scripted Segments (Backstage, Vignettes):**
    *   **Content Characteristics:** Dialogue from non-promo, non-match segments like backstage altercations, comedic skits, or cinematic vignettes. These often reveal different facets of a character's personality and relationships.
    *   **Potential Sources:** Show transcripts, focusing on these specific segment types.
    *   **Estimated Data Impact:** Several hundred such segments, transcribed and attributed, would be valuable for capturing conversational style outside of formal promos.

### General Considerations for Character Data:

*   **Consistency:** For a specific character, try to ensure the biographical and dialogue data is consistent with their most recognized or targeted persona, unless the goal is to model character evolution.
*   **Source Reliability:** Prioritize official sources, but supplement with well-regarded fan resources, being mindful of potential inaccuracies or biases in the latter.
*   **Gimmick Specificity:** Tagging data by specific gimmicks or eras of a wrestler's career (e.g., "Ministry of Darkness Undertaker" vs. "American Badass Undertaker") can help in fine-tuning for very specific versions of a character.
*   **Volume:** For a general understanding of many characters, a broad collection is good. For fine-tuning a *specific* character LLM, all available high-quality prose and dialogue for that single character should be amassed. This might range from a few dozen pages of text for a lesser-known character to hundreds for a legend.

## Category 4: Kayfabe Narratives and Storyline Summaries

This category includes texts that describe the fictional storylines, feuds, and dramatic arcs within wrestling as if they were real events. Understanding these narratives is essential for an LLM to grasp the context of promos, match outcomes, and character motivations.

### Sub-Categories:

1.  **Weekly Show Recaps/Results (Kayfabe Perspective):**
    *   **Content Characteristics:** Summaries of weekly TV shows (Raw, SmackDown, Dynamite, etc.) that narrate the events, promo outcomes, match results, and storyline developments from an in-universe perspective.
    *   **Potential Sources:** Wrestling news websites that provide show recaps (e.g., PWInsider, Figure Four Online/Wrestling Observer, PWTorch - focusing on their descriptive recaps rather than opinion pieces), official show summaries if available.
    *   **Estimated Data Impact:** Recaps from several years of major weekly shows would be ideal, potentially 500-1000+ show recaps. Each recap might range from 1000-3000 words.

2.  **PPV/Prizefight Event Recaps (Kayfabe Perspective):**
    *   **Content Characteristics:** Similar to weekly show recaps but for major monthly events. These often detail the culmination of feuds or significant turning points in storylines.
    *   **Potential Sources:** Wrestling news websites, historical wrestling sites.
    *   **Estimated Data Impact:** Recaps for 100-200 major PPV events across different promotions and eras.

3.  **Feud Summaries/Analyses (Written from an In-Universe Viewpoint):**
    *   **Content Characteristics:** Texts that specifically break down the history and progression of a notable feud between two or more wrestlers, detailing key events, promos, and matches that defined their rivalry, all while maintaining kayfabe.
    *   **Potential Sources:** Feature articles on wrestling history websites, special sections in wrestling magazines, fan-written feud analyses (requires vetting for quality and kayfabe adherence).
    *   **Estimated Data Impact:** Detailed summaries for 50-100 significant feuds.

4.  **Historical Retrospectives on Storylines/Eras (Kayfabe Focus):**
    *   **Content Characteristics:** Articles or book chapters that look back at specific storylines (e.g., the nWo invasion, the Summer of Punk) or eras (e.g., the Attitude Era) primarily from the perspective of the on-screen narrative.
    *   **Potential Sources:** Wrestling history books, specialized websites, anniversary articles.
    *   **Estimated Data Impact:** 20-30 in-depth articles or book excerpts focusing on major storylines/eras.

### General Considerations for Kayfabe Narratives:

*   **Maintaining Kayfabe:** The key is that these texts should treat the storylines as real within the context of the wrestling universe. Avoid texts that heavily break kayfabe or focus on backstage/real-world aspects unless specifically collecting data for a different purpose (like a "dirt sheet" model, which is not the primary goal here).
*   **Chronological Order:** If possible, having dates associated with these narratives helps the model understand the timeline of events and character developments.
*   **Detail and Nuance:** Good narrative summaries will not just state what happened but also hint at character motivations and emotional impact, as portrayed on screen.
*   **Volume:** A substantial corpus of kayfabe narratives, ideally covering multiple years and promotions, is necessary for the LLM to build a coherent "mental model" of the wrestling world. This could easily amount to millions of words.

## Category 5: Role-Specific Corpora

While the above categories provide broad data, creating highly specialized models for distinct roles (promoter, valet, specific announcer types, referee) requires curating datasets that specifically exemplify the language and interactions unique to those roles. This often means extracting relevant dialogues and monologues from more general data (like show transcripts) and tagging them for the specific role.

### Sub-Categories (Examples - to be expanded for each key role):

1.  **Promoter/Authority Figure Dialogue:**
    *   **Content Characteristics:** Announcements of matches, new rules, addressing the roster, making pronouncements, reacting to chaos. Language is often formal, authoritative, or manipulative depending on the character.
    *   **Potential Sources:** Extracted from promo segments, in-ring announcements, backstage segments featuring authority figures (e.g., Vince McMahon, Eric Bischoff, Tony Khan, Jack Tunney, William Regal as GM).
    *   **Estimated Data Impact:** Several hundred distinct segments (500-1000+ lines of dialogue) focused purely on authority figure speech patterns.

2.  **Valet/Manager Ringside and Interview Dialogue:**
    *   **Content Characteristics:** Comments made at ringside during a client\'s match (encouragement, distraction, complaints to the referee), interviews conducted alongside their client, promos where they speak for their client.
    *   **Potential Sources:** Extracted from match commentary (manager\'s interjections if audible and transcribed), promo transcripts, interview segments.
    *   **Estimated Data Impact:** Dialogue from 100-200 segments featuring prominent managers, focusing on their unique contributions.

3.  **Referee Instructions and Interactions:**
    *   **Content Characteristics:** Standard match instructions (e.g., "ask him," "get down," rope breaks), verbal exchanges with wrestlers (warnings, asking for submissions), calling for the bell. Limited vocabulary but specific to the role.
    *   **Potential Sources:** Difficult to isolate from general match audio. May require manual transcription of referee dialogue from many matches or finding specific "referee mic\'d up" segments if they exist.
    *   **Estimated Data Impact:** A smaller, specialized dataset of a few thousand common referee phrases and interaction patterns.

4.  **Ring Announcer Scripts/Style:**
    *   **Content Characteristics:** Formal introductions of wrestlers, cities, championship titles. Highly formulaic but with distinct stylistic variations between announcers.
    *   **Potential Sources:** Transcribing introductions from many matches by different announcers (e.g., Howard Finkel, Justin Roberts, Lilian Garcia).
    *   **Estimated Data Impact:** Scripts for 200-300 distinct wrestler introductions by various announcers to capture different styles.

### General Considerations for Role-Specific Corpora:

*   **Granularity:** The more specific the role, the harder it might be to gather a large volume of unique data. However, even smaller, highly focused datasets can be effective with PEFT methods like LoRA.
*   **Extraction and Tagging:** Significant effort will likely be involved in identifying and extracting role-specific speech from broader transcripts (e.g., isolating only what a manager says during a long promo segment involving multiple speakers).
*   **Defining "Role Voice":** For each role, it\'s important to define the key linguistic characteristics. For example, a heel manager\'s speech will differ significantly from a babyface manager or a neutral authority figure.
*   **Augmentation Potential:** For roles with limited vocabulary (like referees), data augmentation techniques (e.g., creating many variations of standard calls) might be useful.
*   **Volume:** Varies greatly by role. For a "promoter" role, one might amass thousands of lines. For a "referee," perhaps only a few hundred distinct phrases but repeated in many contexts.

This concludes the initial breakdown of the five core data categories. The next step will be to evaluate if these categories are sufficient and explore potential new ones.

## Evaluating Sufficiency of Data Categories and Proposing New Ones

While the five categories detailed above (Promo Scripts, Match Commentary, Character Dialogues/Biographies, Kayfabe Narratives, and Role-Specific Corpora) provide a strong foundation, the unique nature of professional wrestling and the goal of creating nuanced, persona-driven LLMs suggest a few additional categories or considerations could be beneficial.

### Critical Review of Existing Categories:

The current categories cover the primary forms of direct communication and narrative presentation in wrestling. However, the depth within each sub-category is key. For instance, simply having "promo scripts" is not enough; the differentiation by promo *type* (heel turn, face turn, championship challenge, etc.) is what will enable more nuanced understanding and generation.

### Proposed New Data Categories/Considerations:

1.  **Wrestling News and "Dirt Sheet" Reports (Use with Extreme Caution):**
    *   **Content Characteristics:** Articles from wrestling news websites, newsletters (like the Wrestling Observer Newsletter), and online forums that discuss backstage news, rumors, real-life contract situations, creative plans, and critiques of shows. This is often referred to as "dirt sheet" information.
    *   **Potential Value:** Could provide the LLM with an understanding of the meta-narrative of wrestling, how fans perceive the business, and the real-world context that sometimes bleeds into on-screen presentation. It might also capture a specific cynical or "smart mark" fan voice.
    *   **Significant Risks & Challenges:**
        *   **Kayfabe Contamination:** This data inherently breaks kayfabe and could confuse an LLM trying to maintain an in-universe persona.
        *   **Accuracy/Rumors:** Dirt sheets are notorious for inaccuracies and unconfirmed rumors. Feeding this to an LLM could lead it to generate false information.
        *   **Negativity/Bias:** Fan discussions and dirt sheets can be highly negative or biased.
    *   **Mitigation/Usage Strategy:** If used at all, this data should be:
        *   Kept in a *completely separate dataset* from kayfabe material.
        *   Potentially used to train a *specific* LLM persona (e.g., a "wrestling news analyst" or a "cynical fan") rather than a general wrestling or character LLM.
        *   Heavily curated to filter out the most egregious rumors or toxic content.
    *   **Estimated Data Impact:** A corpus of several thousand articles/posts, carefully selected, might be needed if this persona is pursued.

2.  **Fan Forum Discussions and Social Media Content (Wrestler and Fan):**
    *   **Content Characteristics:** Threads from forums (e.g., Reddit's r/SquaredCircle), comments on wrestling articles, wrestler social media posts (Twitter, Instagram), and fan reactions.
    *   **Potential Value:** Captures the modern fan lexicon, popular opinions, memes, how fans react to storylines and characters in real-time, and how wrestlers interact with fans directly (or maintain their persona online).
    *   **Risks & Challenges:**
        *   **Toxicity and Noise:** Online discussions can be extremely toxic, off-topic, or low-quality. Requires heavy filtering.
        *   **Informal Language:** Highly informal, full of slang, memes, and shorthand, which might be good for a casual fan persona but less so for a formal announcer.
        *   **Privacy:** Using fan PII is a concern.
    *   **Mitigation/Usage Strategy:** Anonymize data. Use advanced filtering for relevance and toxicity. Could be useful for training an LLM to understand fan sentiment or generate text in a very casual, modern fan style.
    *   **Estimated Data Impact:** A large, filtered dataset (tens of thousands to hundreds of thousands of posts/comments) to capture the diversity of fan voices.

3.  **Wrestling Move Encyclopedias and Technical Manuals:**
    *   **Content Characteristics:** Descriptions of wrestling moves, holds, and their execution. Could be from old wrestling school manuals, detailed move lists from wikis, or books on wrestling technique.
    *   **Potential Value:** Could help an LLM (especially one for a PBP announcer or a knowledgeable analyst persona) to accurately name and describe in-ring action with more technical detail.
    *   **Risks & Challenges:** Finding substantial textual descriptions beyond simple lists can be hard. The language might be very dry.
    *   **Estimated Data Impact:** Even a few well-detailed documents or a comprehensive, structured list of moves with descriptions could be beneficial.

4.  **Historical Results and Event Databases:**
    *   **Content Characteristics:** Structured data of match results, event cards, wrestler win/loss records, championship histories.
    *   **Potential Value:** While not prose, this data can be transformed into natural language statements (e.g., "Wrestler A defeated Wrestler B at Event X to win the Championship Y") to provide factual grounding and historical context for an LLM.
    *   **Risks & Challenges:** Requires effort to convert structured data into usable training sentences. Data might be incomplete or contain errors.
    *   **Potential Sources:** Cagematch.net, Wrestlingdata.com, other historical wrestling databases.
    *   **Estimated Data Impact:** Thousands of structured entries could be converted into factual statements.

### Sufficiency Evaluation:

For creating a *general* wrestling-aware LLM, the initial five categories, if sufficiently populated with diverse and high-quality data, are likely adequate as a strong starting point. The sub-categorization within them is crucial for adding depth.

For creating *highly specific personas* (e.g., a particular wrestler, a cynical dirt sheet writer, a specific type of fan), then incorporating some of the proposed new categories becomes more relevant, albeit with the significant caveats mentioned for each.

The decision to include these additional categories depends on the specific goals for the LLM and the resources available for data curation and risk mitigation.

## Discuss Data Formatting and Structuring for Fine-Tuning

Once the raw textual data for various wrestling categories has been collected, it needs to be formatted and structured appropriately for effective fine-tuning. The optimal format can depend on the specific fine-tuning task (e.g., general domain adaptation, instruction following, persona adoption) and the architecture of the chosen SLM.

### General Formatting Principles:

1.  **Cleanliness and Consistency:**
    *   Remove irrelevant characters, HTML tags (if scraped from web), excessive whitespace, and transcription errors.
    *   Standardize speaker names/tags (e.g., always "Stone Cold Steve Austin," not sometimes "Steve Austin" or "Austin").
    *   Ensure consistent punctuation and sentence casing, unless a specific character's style dictates otherwise.

2.  **Plain Text Format:**
    *   Most fine-tuning processes expect input data as plain text files (e.g., `.txt`, `.jsonl`).
    *   For `.jsonl` (JSON Lines), each line is a separate JSON object, often representing a single data sample (e.g., a prompt-response pair).

3.  **Clear Delimiters (if multiple turns or segments per record):**
    *   If a single data record contains multiple turns of a dialogue or different segments of text, use clear and consistent delimiters (e.g., special tokens like `<|SPEAKER_A|>`, `<|SPEAKER_B|>`, `<|END_OF_TURN|>`, or even just newline characters if the structure is simple).

### Common Fine-Tuning Formats:

1.  **Completion Format (for Causal Language Models like GPT, Llama, Mistral 7B):**
    *   **Structure:** Each training example is a continuous piece of text. The model learns to predict the next token given the preceding tokens.
    *   **Application for Wrestling:**
        *   **General Domain Adaptation:** Feed large, continuous blocks of wrestling text (articles, long promos, match commentary sections). The model learns the style, vocabulary, and common knowledge of wrestling.
        *   **Persona Adoption (Implicit):** If all text is from a single character (e.g., all known promos of The Rock), the model will implicitly learn The Rock's style by simply trying to complete sentences like he would.
        *   **Example:**
            ```text
            Finally, The Rock has come back to [City Name]! Do you smell what The Rock is cookin'? It doesn't matter what you smell! The Rock is the most electrifying man in sports entertainment, and tonight, he's going to lay the smack down on all their candy asses!
            ```

2.  **Instruction-Following Format (for Instruction-Tuned Models or to create them):**
    *   **Structure:** Typically uses a prompt/instruction and a desired response. The model learns to follow the instruction or answer the question in the style of the provided responses.
    *   **Common Templates (JSONL example):**
        ```json
        {"instruction": "Who is the greatest wrestler of all time?", "input": "", "output": "While many claim the title, figures like Ric Flair, Hulk Hogan, and Stone Cold Steve Austin are always in the conversation."}
        {"prompt": "How would a heel wrestler react to losing a match?", "response": "They'd probably blame the referee, claim their opponent cheated, or say they weren't 100% that night. Anything but admit they lost fair and square!"}
        {"text": "<s>[INST] As a wrestling promoter, announce the main event for the upcoming PPV. [/INST] Ladies and gentlemen, wrestling fans around the world! Get ready for a collision of titans! At 'WrestleMania Extravaganza,' for the Undisputed World Heavyweight Championship, it will be the reigning and defending champion, 'The Immortal' Hulk Hogan, taking on the challenger, the Eighth Wonder of the World, André the Giant! It's a main event for the ages! </s>"}
        ```
    *   **Application for Wrestling:**
        *   **Role-Playing:** "Act as a wrestling announcer calling a match where [ Wrestler A ] hits their finisher on [ Wrestler B ]."
        *   **Character Voice:** "In the style of Macho Man Randy Savage, respond to this challenge: ..."
        *   **Information Retrieval (Kayfabe):** "What was the outcome of the main event of WrestleMania III?"
    *   **Special Tokens:** Many instruction-tuned models use specific tokens to delineate instructions, inputs, and responses (e.g., `[INST]`, `[/INST]`, `<s>`, `</s>`, `### Human:`, `### Assistant:`). The exact format should match what the base model expects or what you define for your fine-tuning.

3.  **Dialogue Format:**
    *   **Structure:** Clearly demarcated turns between different speakers.
    *   **Example (Simple text):**
        ```text
        Interviewer: My guest at this time, The Undertaker. Undertaker, next week you face Mankind in Hell in a Cell...
The Undertaker: Mankind... you do not know what you have gotten yourself into. The darkness awaits... and in the cell, there will be no escape. Rest... in... peace.
        ```
    *   **Example (JSONL with speaker tags):
        ```json
        {"turns": [{"speaker": "Interviewer", "text": "My guest at this time, The Undertaker. Undertaker, next week you face Mankind in Hell in a Cell..."}, {"speaker": "The Undertaker", "text": "Mankind... you do not know what you have gotten yourself into. The darkness awaits... and in the cell, there will be no escape. Rest... in... peace."}]}
        ```
    *   **Application for Wrestling:** Ideal for training models on promo battles, interview segments, or announcer team banter.

### Structuring for Specific Personas:

*   **Persona Prefix:** For a specific character, you might prepend a consistent identifier or description to all their training data.
    *   Example (Completion format for The Undertaker):
        ```text
        [PERSONA: The Undertaker] The chill in the air is palpable. The druids slowly make their way to the ring, heralding the arrival of the Phenom. Tonight, someone's soul will belong to me.
        ```
*   **Instruction Tuning with Persona:**
    ```json
    {"instruction": "Deliver a catchphrase.", "input": "", "output": "Rest... in... peace.", "persona": "The Undertaker"}
    ```
    (The "persona" field might be used to select data for a specific LoRA adapter or as part of the input if the model is trained to switch personas based on a tag).

### Key Considerations:

*   **Base Model's Original Training:** If starting from a base model that was already instruction-tuned or dialogue-tuned, it's often best to try and match its original formatting conventions to leverage its existing capabilities.
*   **Data Augmentation:** Consider augmenting your dataset by rephrasing instructions, creating variations of responses, or even generating synthetic data (e.g., using a larger LLM to generate initial character dialogues based on a profile, then curating and refining it).
*   **Start Simple:** Begin with a straightforward completion or instruction format. Complexity can be added as needed.
*   **Tools:** Libraries like Hugging Face `datasets` can be very helpful for loading, processing, and managing datasets in various formats.

The choice of format will directly impact how the SLM learns and what kind of prompts it will respond to best after fine-tuning.
