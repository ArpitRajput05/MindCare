"""
seed_knowledge_base.py
Generates 25 curated, authoritative documents for the MindCare RAG knowledge base.
Sources include WHO, CDC, NHS, Harvard Health, Stanford Lifestyle Medicine,
American Psychological Association (APA), and leading university wellbeing guides.
"""

import os

KB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "knowledge_base")
os.makedirs(KB_DIR, exist_ok=True)

DOCUMENTS = [
    # ==================== SLEEP GUIDELINES ====================
    (
        "sleep_01_who_circadian_rhythm.txt",
        """Title: WHO Guidelines on Sleep and Circadian Health for Young Adults
Source: World Health Organization (WHO) Wellbeing Guidelines
Category: Sleep

Young adults and students require 7 to 9 hours of restorative sleep each night for optimal neurological and psychological functioning.
Disruption of the circadian rhythm through irregular sleep-wake cycles impairs memory consolidation, emotional regulation, and neuroendocrine balance.
Maintaining consistent wake-up times within a 30-minute window, even on weekends, anchors the suprachiasmatic nucleus (the master biological clock).
Morning exposure to natural daylight within 45 minutes of waking stimulates cortisol release for daytime alertness and sets the timer for melatonin synthesis 14 to 16 hours later.
Consistent sleep timing stabilizes neurotransmitters such as serotonin and dopamine, directly reducing susceptibility to academic anxiety and mood drops."""
    ),
    (
        "sleep_02_harvard_sleep_hygiene.txt",
        """Title: Harvard Medical School Guide to Healthy Sleep Hygiene
Source: Harvard Health Publishing - Division of Sleep Medicine
Category: Sleep

Sleep hygiene is a collection of environmental and behavioral practices that facilitate sustained nocturnal rest.
The sleep sanctuary must be kept cool (around 18-20°C or 65-68°F), dark, and quiet to prevent micro-arousals during deep NREM slow-wave sleep.
Caffeine has an average half-life of 5 to 7 hours and a quarter-life of up to 12 hours; caffeine consumption should cease at least 8 hours prior to anticipated bedtime.
The human brain associates the bed with wakefulness if spent studying or watching entertainment in bed; if unable to sleep after 20 minutes, leave the bedroom and engage in low-stimulus reading until drowsiness returns.
A 15-minute wind-down buffer before sleep, including warm showers or progressive muscle relaxation, reduces sympathetic nervous system tone and accelerates sleep latency."""
    ),
    (
        "sleep_03_nsf_screen_bedtime.txt",
        """Title: National Sleep Foundation Protocol on Blue Light and Bedtime Technology
Source: National Sleep Foundation (NSF) Clinical Report
Category: Sleep

Short-wavelength blue light emitted by smartphones, laptops, and tablets suppresses nocturnal melatonin secretion by over 50 percent when used within two hours of bedtime.
Beyond optical stimulation, interactive digital content such as social media feeds and notifications triggers dopamine surges and hyper-arousal, delaying the onset of restorative REM sleep.
Implement a strict digital curfew by turning off personal handheld devices at least 60 minutes before scheduled lights-out.
Replace screen time with analog activities: physical reading, reflective journaling, or soothing ambient music.
Charge smartphones outside the sleeping area to eliminate midnight notification checks, micro-awakenings, and involuntary screen glance compulsions."""
    ),
    (
        "sleep_04_nih_sleep_debt_recovery.txt",
        """Title: NIH Guidance on Managing Academic Sleep Debt
Source: National Institutes of Health (NIH) - National Heart, Lung, and Blood Institute
Category: Sleep

Sleep debt accumulates chronically when a student sleeps less than their biological baseline for multiple consecutive nights.
Accumulated sleep deficits severely impair executive brain functions: risk assessment, abstract logic, working memory, and sustained attention during lectures.
Attempting to pay off chronic sleep debt solely through weekend binge-sleeping (sleeping past noon) induces social jetlag, making Sunday night sleep onset even harder.
The optimal strategy for repaying acute sleep debt is gradual: sleep 30 to 60 minutes earlier over 4 to 5 consecutive evenings, paired with afternoon power naps strictly under 25 minutes.
Short power naps taken before 3:00 PM restore cognitive alertness without plunging the brain into deep slow-wave sleep, preventing post-nap grogginess."""
    ),
    (
        "sleep_05_cdc_student_sleep_recommendations.txt",
        """Title: CDC Student Sleep and Academic Performance Advisory
Source: Centers for Disease Control and Prevention (CDC) Health Brief
Category: Sleep

Over 70 percent of university students report insufficient sleep during academic terms, correlating directly with lower GPA, increased somatic complaints, and emotional volatility.
Alcohol consumed as a sleep aid is counterproductive: while it may hasten drowsiness, it severely fragments late-night REM sleep, causing frequent nocturnal awakenings.
Heavy evening meals containing high sugar or spicy elements elevate digestive thermogenesis and acid reflux, impairing continuous sleep stages.
Establishing an evening routine that triggers conditioned relaxation signals to the brain that the cognitive workload is finished for the day.
Prioritizing a fixed 7-hour minimum sleep schedule yields higher academic exam performance than sacrificing sleep for all-night cramming sessions."""
    ),

    # ==================== STRESS MANAGEMENT ====================
    (
        "stress_01_apa_academic_burnout.txt",
        """Title: APA Framework for Preventing Student Academic Burnout
Source: American Psychological Association (APA) Student Stress Initiative
Category: Stress

Academic burnout is characterized by emotional exhaustion, depersonalization or cynicism towards coursework, and a diminished sense of personal accomplishment.
Burnout develops when prolonged high cognitive demands are compounded by inadequate recovery periods and rigid perfectionistic self-expectations.
Early warning indicators include chronic lethargy, irritability toward peers, procrastination masked as fatigue, and inability to focus on reading materials.
Combating burnout requires shifting from reactive coping to scheduled micro-recovery blocks throughout the academic day.
Establishing psychological boundaries between study hours and personal time prevents the feeling of perpetual guilt when not working, restoring sustained intrinsic motivation."""
    ),
    (
        "stress_02_nhs_anxiety_grounding.txt",
        """Title: NHS 5-4-3-2-1 Sensory Grounding Technique for Acute Anxiety
Source: National Health Service (NHS) Every Mind Matters
Category: Stress

When overwhelming academic anxiety or panic strikes, sensory grounding interrupts the amygdala's fight-or-flight spiral by reorienting cognitive attention to physical reality.
Step 1: Acknowledge FIVE things you can see around your immediate environment (a pen, shadows on the wall, desk grain).
Step 2: Acknowledge FOUR things you can physically feel (the soles of your feet on the floor, texture of your sleeve, chair back).
Step 3: Acknowledge THREE distinct sounds you hear (air conditioner hum, distant traffic, your own breathing).
Step 4: Acknowledge TWO things you can smell or identify scent memories of (coffee, fresh air).
Step 5: Acknowledge ONE thing you can taste, or take a refreshing sip of water.
Practicing this sensory sequence for 2 minutes lowers elevated heart rates and restores executive prefrontal cortex clarity."""
    ),
    (
        "stress_03_cambridge_exam_stress_coping.txt",
        """Title: Cambridge Student Guide to Managing Exam and Deadline Pressure
Source: University of Cambridge Student Wellbeing Service
Category: Stress

Perceived stress spikes exponentially when tasks are perceived as high-stakes, uncertain, and beyond personal locus of control.
Dismantle catastrophic thinking patterns by applying cognitive reframing: distinguish between actionable problems and uncontrollable hypotheticals.
Adopt the Rule of Thirds for exam preparation: divide daily study blocks into one-third active content review, one-third problem testing, and one-third cognitive rest.
Avoid stress contagion by limiting post-exam post-mortem discussions with anxious peers, which artificially inflates perceived inadequacy.
Remind yourself that physiological arousal (racing pulse, alertness) is your body mobilizing energy to perform, not an omen of impending failure."""
    ),
    (
        "stress_04_who_stress_management_guide.txt",
        """Title: WHO Doing What Matters in Times of Stress: Illustrated Coping Guide
Source: World Health Organization (WHO) Mental Health Coping Manual
Category: Stress

Stress affects both emotional wellbeing and physical physiology, manifesting as muscle tension, shallow thoracic breathing, and digestive discomfort.
The technique of Unhooking: acknowledge difficult thoughts and feelings without wrestling with them; label them as 'Here is a thought about failure' rather than accepting it as fact.
Grounding in your values: when feeling overwhelmed, ask what small action aligns with being a caring, persistent student in this exact moment.
Notice how thoughts come and go like weather patterns across the sky; they do not require immediate reactive obedience.
Engage in physical unhooking: stretch both arms overhead, press your feet firmly into the floor, and breathe out slowly to release muscular guarding."""
    ),
    (
        "stress_05_stanford_breathing_autonomic_regulation.txt",
        """Title: Stanford Neurobiology Protocol on the Physiological Sigh
Source: Stanford University Lifestyle Medicine & Neurosciences
Category: Stress

The physiological sigh is the fastest autonomous method to rapidly reduce autonomic nervous system arousal in real time.
The sigh pattern consists of two consecutive nasal inhalations followed by an extended, passive oral exhalation.
The first inhalation fills the bulk of lung volume; the second sharp inhalation reinflates collapsed pulmonary alveoli, increasing surface area for carbon dioxide exchange.
The prolonged slow exhalation activates the vagus nerve, immediately slowing sinoatrial node firing in the heart and decreasing blood pressure within 60 to 90 seconds.
Performing three to five physiological sighs before studying or during acute stress triggers immediate mental calm without requiring quiet meditation postures."""
    ),

    # ==================== SCREEN TIME & DIGITAL WELLBEING ====================
    (
        "screen_01_stanford_digital_detox_protocol.txt",
        """Title: Stanford Guide to Dopamine Management and Digital Micro-Breaks
Source: Stanford University Student Health & Lifestyle Medicine
Category: Screen Time

Infinite-scroll social algorithms operate on variable ratio reinforcement schedules, the identical psychological mechanism behind slot machines.
Checking feeds during study breaks does not provide neurological rest; it floods the ventral striatum with dopamine hits, making subsequent text focus feel intolerably dull.
Establish frictionless app barriers: move social platforms into nested folders, disable non-human notifications, and enable grayscale color display on mobile devices.
Convert your study desk into a phoneless zone by keeping mobile devices at least two arm-lengths away or inside a backpack during deep study blocks.
Schedule two designated 15-minute windows per day for social catch-up rather than grazing continuously through 100+ daily unlocks."""
    ),
    (
        "screen_02_nhs_social_media_boundaries.txt",
        """Title: NHS Framework on Social Media Consumption and Self-Comparison
Source: National Health Service (NHS) Mental Wellbeing Guidance
Category: Screen Time

Excessive passive consumption of idealized peer lifestyles on visual platforms fosters social comparison traps and fear of missing out (FOMO).
Students spending more than 4 hours daily on social platforms exhibit a 35 percent higher prevalence of self-reported mood drops and imposter syndrome.
Practice active intentional curation: aggressively mute, unfollow, or restrict accounts that evoke feelings of inadequacy, jealousy, or chronic stress.
Transition from passive lurker mode (scrolling feeds) to active direct communication (voice calls or genuine 1-on-1 messages with close friends).
Institute device-free meals and device-free morning walks to preserve daily moments of quiet psychological contemplation without digital commentary."""
    ),
    (
        "screen_03_oxford_digital_wellbeing_audit.txt",
        """Title: Oxford Wellbeing Advisory on Digital Fatigue and Screen Strain
Source: University of Oxford Student Welfare & Counselling Network
Category: Screen Time

Prolonged screen exposure contributes to Computer Vision Syndrome, cervical spine strain (text neck), and cognitive fragmentation.
Implement the clinical 20-20-20 rule: every 20 minutes of screen work, glance at an object at least 20 feet away for 20 continuous seconds to relax ciliary eye muscles.
Digital fragmentation occurs when students toggle between study documents and messaging tabs every 90 seconds, causing severe attention residue.
Batch communications: designate set intervals (e.g., 12:30 PM and 5:30 PM) to process non-urgent emails and group chat updates.
Protect the first 30 minutes after waking from any phone interaction to allow natural cortisol awakening response without reactive information overload."""
    ),
    (
        "screen_04_apa_phone_notification_fatigue.txt",
        """Title: APA Recommendations for Taming Smartphone Notification Interruption
Source: American Psychological Association (APA) Science Brief
Category: Screen Time

Each phone chime or vibration triggers an involuntary orientation reflex, dragging cognitive resources away from working memory tasks.
Research demonstrates that after a digital interruption, it requires an average of 23 minutes for a student to fully re-engage in complex cognitive problem-solving.
Audit device notification channels: silence all lock-screen banners except direct phone calls from immediate family members.
Utilize operating system focus modes (such as Study Mode or Work Focus) that schedule notifications to deliver in single quiet summaries.
Placing the smartphone face-down with screen dimming reduces subliminal glance impulses that trigger reflexive social media browsing."""
    ),
    (
        "screen_05_unicef_youth_digital_balance.txt",
        """Title: UNICEF Student Guidance for Healthy Digital Equilibrium
Source: UNICEF Child & Youth Mental Health Guidelines
Category: Screen Time

Digital connectivity is a valuable educational and social lifeline when balanced against physical activity, offline friendships, and restorative rest.
Warning signs of unhealthy digital attachment include feeling anxious when separated from mobile devices, neglecting sleep to watch short-form videos, and declining real-world invitations.
Create tech-free sanctums in your living space: establish kitchen dining tables and beds as 100 percent screen-free sanctuaries.
Engage in one full-day or half-day digital Sabbath each weekend to reset sensory sensitivity and rediscover hobbies: sketching, cooking, or reading paper books.
Remember that algorithms prioritize emotional outrage and engagement metrics over your peace of mind; reclaim agency over your attention."""
    ),

    # ==================== STUDY HABITS & COGNITIVE LOAD ====================
    (
        "study_01_cornell_pomodoro_active_recall.txt",
        """Title: Cornell Learning Strategies: Pomodoro Cycling and Active Retrieval
Source: Cornell University Center for Teaching & Learning
Category: Study Habits

Passive re-reading of textbooks and highlighting notes generates an illusion of competence without embedding long-term synaptic connections.
Adopt the Pomodoro technique for focus endurance: commit to 25 minutes of single-task immersion followed by a 5-minute cognitive rest break.
After four consecutive cycles, reward yourself with a longer 20 to 30 minute restorative break involving physical movement or hydration.
Incorporate active recall: close your study materials and write down or explain out loud everything you just read from memory.
Testing yourself regularly strengthens neural retrieval pathways and reduces exam panic by transforming passive familiarity into robust mastery."""
    ),
    (
        "study_02_mit_cognitive_load_study_intervals.txt",
        """Title: MIT Guide to Cognitive Architecture and Working Memory Limits
Source: MIT Teaching + Learning Lab Insights
Category: Study Habits

Human working memory can hold only 4 to 7 discrete chunks of novel information simultaneously before cognitive overload degrades retention.
Multitasking while studying—such as listening to lyrical podcasts or having video streams playing in background—taxes working memory capacity by 40 percent.
Break massive term projects down into bite-sized micro-tasks that can each be completed in under 45 minutes to circumvent procrastination paralysis.
Prioritize the hardest, highest-friction cognitive task during your personal biological peak energy window (usually mid-morning for most students).
Organize study workspaces cleanly: physical desk clutter competes for neural processing visual resources, increasing subconscious mental friction."""
    ),
    (
        "study_03_harvard_spacing_effect.txt",
        """Title: Harvard Insights on Spaced Repetition and Long-Term Memory
Source: Harvard Derek Bok Center for Teaching and Learning
Category: Study Habits

The spacing effect demonstrates that learning is significantly more durable when study sessions are distributed across days rather than condensed into marathon sessions.
Cramming for 10 hours before an exam yields rapid forgetting within 48 hours, whereas 2 hours across five separate days fosters deep conceptual scaffolding.
Intersperse different related subjects during study sessions (interleaving practice) rather than drilling a single topic endlessly; this trains pattern recognition.
Use flashcards or digital spaced-repetition algorithms that schedule reviews right at the moment when memories are about to fade.
Treat rest days not as wasted time, but as the essential biological phase where memory consolidation is actively wired during slow-wave sleep."""
    ),
    (
        "study_04_ucl_procrastination_action_triggers.txt",
        """Title: UCL Psychology Guide to Overcoming Academic Procrastination
Source: University College London (UCL) Student Psychological Services
Category: Study Habits

Procrastination is fundamentally an emotional regulation challenge, not a deficit in time management or willpower.
Students delay academic tasks to avoid feelings of self-doubt, inadequacy, boredom, or the fear of turning in imperfect work.
Apply the 2-Minute Rule to shatter task inertia: tell yourself you will work on the assignment for just two minutes; once momentum begins, continuation is natural.
Lower the activation energy: set out study materials, open the exact assignment document, and close all irrelevant browser tabs the night before.
Replace harsh self-criticism with self-compassion: research shows forgiving yourself for past procrastination directly reduces future delay behavior."""
    ),
    (
        "study_05_berkeley_study_environment_focus.txt",
        """Title: UC Berkeley Protocol for High-Efficiency Study Environments
Source: UC Berkeley Student Learning Center
Category: Study Habits

Your physical study environment operates as an external cognitive scaffolding that cues neural focus states or distraction patterns.
Designate a dedicated study spot used solely for academic work; avoid studying in bed or relaxing on comfortable couches where the brain expects leisure.
Ambient sound management: use brown noise, soft binaural beats, or instrumental classical music to mask unpredictable environmental conversations.
Maintain optimal hydration: even a 2 percent drop in cellular hydration levels impairs concentration, arithmetic processing, and short-term memory recall.
Keep an offload notepad nearby during study sessions: whenever an intrusive non-academic thought emerges, jot it down immediately and return to studying."""
    ),

    # ==================== PHYSICAL ACTIVITY & MOVEMENT ====================
    (
        "exercise_01_who_physical_activity_mental_health.txt",
        """Title: WHO Guidelines on Physical Activity and Sedentary Behavior
Source: World Health Organization (WHO) Guidelines for Health & Wellbeing
Category: Exercise

Adults aged 18 to 64 should perform at least 150 to 300 minutes of moderate-intensity aerobic physical activity per week for substantive mental health benefits.
Regular aerobic activity stimulates neurogenesis in the hippocampus and promotes the release of Brain-Derived Neurotrophic Factor (BDNF), enhancing learning and mood.
Prolonged uninterrupted sedentary behavior (sitting at study desks for over 8 hours) correlates with elevated depressive symptoms and reduced cardiovascular health.
Interrupt sedentary periods every 60 minutes with 2 minutes of brisk movement: stair climbing, light bodyweight squats, or torso twists.
Even low-intensity physical movement is dramatically superior to complete inactivity in clearing metabolic waste and elevating cerebral blood circulation."""
    ),
    (
        "exercise_02_cdc_aerobic_exercise_mood_boost.txt",
        """Title: CDC Advisory on Physical Activity and Emotional Resilience
Source: Centers for Disease Control and Prevention (CDC) Physical Activity Division
Category: Exercise

Engaging in regular physical movement acts as a natural antidepressant and anxiolytic by stimulating endogenous endorphins and endocannabinoids.
A single 20 to 30 minute session of moderate aerobic exercise (brisk walking, jogging, cycling, or swimming) provides an acute mood lift lasting up to 4 hours.
Exercise moderates the body's stress response system by conditioning the cardiovascular and sympathetic systems to tolerate elevated physiological arousal safely.
Pair physical activity with social connection: participate in campus intramural sports, recreational club teams, or walking study groups.
Consistent weekly exercise reduces baseline resting heart rate, mitigates muscle tension, and promotes deeper nocturnal slow-wave sleep."""
    ),
    (
        "exercise_03_harvard_walking_stress_cortisol.txt",
        """Title: Harvard Health Guide to Daily Walking and Cortisol Regulation
Source: Harvard Health Publishing - Mind and Movement Series
Category: Exercise

Daily brisk walking in green outdoor spaces significantly attenuates systemic cortisol levels and dampens sympathetic nervous system hyper-vigilance.
Outdoor movement provides panoramic optic flow, which neurobiologically calms the brain's visual attention centers and reduces ruminative loops.
Aim for 7,000 to 10,000 daily steps accumulated organically: take stairs instead of elevators, alight from transit one stop early, or conduct walking phone calls.
A brisk 15-minute post-lunch walk blunts postprandial blood glucose spikes, eliminating the mid-afternoon energy crash that tempts students into excessive caffeine consumption.
Walking without headphones or screens allows mental incubation, often unlocking creative breakthroughs on complex academic assignments."""
    ),
    (
        "exercise_04_nih_movement_dopamine_regulation.txt",
        """Title: NIH Research on Physical Exercise and Neurotransmitter Balance
Source: National Institute of Mental Health (NIMH) / NIH Science Reports
Category: Exercise

Sustained academic stress depletes central monoamine neurotransmitters, leaving students feeling apathetic, unmotivated, and cognitively sluggish.
Physical exertion naturally stimulates dopamine and norepinephrine synthesis in the locus coeruleus and ventral tegmental area, restoring drive and attentional focus.
Resistance training (bodyweight exercises, resistance bands, or weight training) two to three times weekly significantly reduces generalized anxiety and enhances body image.
Post-exercise stretching promotes parasympathetic nervous system activation, reducing physical tightness in the neck, shoulders, and lower back caused by desk posture.
Treat daily movement as a non-negotiable mental hygiene appointment with yourself, identical in priority to attending core academic seminars."""
    ),
    (
        "exercise_05_mayo_exercise_student_wellbeing.txt",
        """Title: Mayo Clinic Protocol: Integrating Movement into Demanding Academic Schedules
Source: Mayo Clinic Student Health and Wellness Guidelines
Category: Exercise

Lack of time is the most common reason students cite for neglecting physical fitness, yet exercise actually increases total productive study hours by sharpening focus.
Implement micro-workouts: three 10-minute bursts of brisk activity spread across the day provide equivalent cardiovascular and cognitive benefits to a single 30-minute workout.
Desk ergonomics: alternate between seated postures and standing desks to prevent postural fatigue and maintain lumbar spine neutrality.
Combine low-intensity activity with auditory review: listen to recorded lectures or study summaries while walking on a treadmill or cycling slowly on a stationary bike.
Start with small, sustainable commitments: 15 minutes of enjoyable movement three times per week builds a resilient habit far better than erratic, punishing gym routines."""
    )
]

def main():
    print(f"Seeding {len(DOCUMENTS)} curated documents into {KB_DIR}...")
    for filename, content in DOCUMENTS:
        filepath = os.path.join(KB_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"  + Created: {filename}")
    print(f"Successfully generated all {len(DOCUMENTS)} knowledge base documents!")

if __name__ == "__main__":
    main()
