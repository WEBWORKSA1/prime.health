"""Tool content: nutrition, sleep, women's health, prevention."""
from tf import F, pm, SEX, AGE, HEIGHT, WEIGHT, ACTIVITY, MIFFLIN, NASEM_MACRO, USPSTF

SLEEP_SRC = ("Watson NF, et al. Recommended amount of sleep for a healthy adult (AASM/SRS consensus). Sleep, 2015", pm("Watson 2015 recommended amount of sleep healthy adult consensus"))

TOOLS_B = [
# ------------------------------------------------------------------ NUTRITION
dict(
 slug="calories", cat="nutrition", name="Calorie calculator (TDEE)", short="Calorie calculator", blurb="Daily calories to maintain, lose or gain",
 title="Calorie Calculator: TDEE and Calories to Lose or Gain Weight",
 desc="Estimate your daily calorie needs (TDEE) with the Mifflin-St Jeor equation and see targets to maintain, lose 0.25–0.5 kg a week or gain.",
 h1="Calorie calculator (TDEE)",
 lede="Estimate how many calories you burn in a day and what intake would maintain, lose or gain weight at a sensible pace.",
 fields=[SEX, AGE, HEIGHT, WEIGHT, ACTIVITY], cta="Calculate calories",
 how="""<p>First we estimate your basal metabolic rate (BMR) with the Mifflin-St Jeor equation, which a 2005 review by the American Dietetic Association found the most accurate of the common equations for healthy adults:</p>
<p class="formula">Men: 10 × kg + 6.25 × cm − 5 × age + 5 &nbsp;|&nbsp; Women: 10 × kg + 6.25 × cm − 5 × age − 161</p>
<p>Then we multiply by an activity factor from 1.2 (sedentary) to 1.9 (very hard daily training) to get total daily energy expenditure (TDEE). Weight-change targets use the rule of thumb that about 7,700 kcal equals 1 kg of body fat, so a 550 kcal daily deficit loses about 0.5 kg a week.</p>""",
 read="""<p>Treat the maintenance figure as a starting estimate. Eat close to it for two to three weeks while weighing yourself a few mornings a week. If the trend is flat, the estimate fits; if not, adjust by 100–200 kcal. Slower loss (0.25–0.5 kg a week) preserves more muscle, especially with adequate protein and strength training.</p>""",
 limits="""<p>Equations predict real energy use within about 10% for most people but can miss by more in very muscular, very lean or older adults, and in some medical conditions. People who are pregnant, breastfeeding, under 18 or managing an eating disorder should get individual advice rather than use a calculator.</p>""",
 faq=[("How many calories should I eat to lose weight?", "About 300–550 kcal below your maintenance figure gives steady loss of roughly 0.25–0.5 kg (0.5–1 lb) a week."),
      ("Which activity level should I choose?", "Most office workers who exercise two or three times a week fit 'lightly active'. People often overestimate; if unsure, pick the lower level."),
      ("Why is my weight loss slower than predicted?", "Energy expenditure falls a little as you lose weight, and water shifts mask fat loss. Judge progress over three to four weeks.")],
 sources=[MIFFLIN, ("Frankenfield D, et al. Comparison of predictive equations for resting metabolic rate. J Am Diet Assoc, 2005", pm("Frankenfield 2005 comparison predictive equations resting metabolic rate")), NASEM_MACRO],
 related=["macros", "bmr", "protein"], guides=["nutrition-patterns", "protein"]),

dict(
 slug="bmr", cat="nutrition", name="BMR calculator", short="BMR calculator", blurb="Basal metabolic rate with three equations",
 title="BMR Calculator: Basal Metabolic Rate (Mifflin, Harris-Benedict, Katch-McArdle)",
 desc="Calculate your basal metabolic rate with Mifflin-St Jeor, the revised Harris-Benedict and, if you know your body fat, Katch-McArdle.",
 h1="BMR calculator",
 lede="Your basal metabolic rate is the energy you burn lying still all day: breathing, circulation and keeping organs running. It is usually 60–70% of daily calories.",
 fields=[SEX, AGE, HEIGHT, WEIGHT, F("bodyfat", "num", "Body fat", opt=True, unit="%", ph="22", min=3, max=70, help="Adds the Katch-McArdle estimate.")],
 how="""<p class="formula">Mifflin-St Jeor: 10W + 6.25H − 5A + 5 (men) or − 161 (women)</p>
<p class="formula">Harris-Benedict (revised 1984): 88.362 + 13.397W + 4.799H − 5.677A (men); 447.593 + 9.247W + 3.098H − 4.330A (women)</p>
<p class="formula">Katch-McArdle: 370 + 21.6 × lean body mass (kg)</p>
<p>W = weight in kg, H = height in cm, A = age in years.</p>""",
 read="""<p>Mifflin-St Jeor is the default because it performs best in validation studies. Katch-McArdle can be more accurate for lean, muscular people because it is based on lean mass. To turn BMR into daily needs, use the <a href="calories.html">calorie calculator</a>.</p>""",
 limits="""<p>BMR estimates are averages. Thyroid conditions, some medicines, recent dieting and body composition all shift the true value. Indirect calorimetry is the only way to measure it precisely.</p>""",
 faq=[("What is a normal BMR?", "For many adults it falls between about 1,200 and 2,000 kcal a day, depending on size, sex and age."),
      ("Does muscle raise BMR?", "Yes, modestly. Each kilogram of muscle burns roughly 13 kcal a day at rest, but its bigger benefits are strength and metabolic health."),
      ("Should I eat below my BMR to lose weight?", "Generally no. Eat between BMR and TDEE so you lose fat without severe hunger or nutrient gaps.")],
 sources=[MIFFLIN, ("Roza AM, Shizgal HM. The Harris Benedict equation reevaluated. Am J Clin Nutr, 1984", pm("Roza Shizgal 1984 Harris Benedict equation reevaluated"))],
 related=["calories", "body-fat", "macros"], guides=["nutrition-patterns"]),

dict(
 slug="macros", cat="nutrition", name="Macro calculator", short="Macro calculator", blurb="Protein, carbs and fat in grams per day",
 title="Macro Calculator: Protein, Carbs and Fat for Your Goal",
 desc="Get daily protein, carbohydrate and fat targets in grams for fat loss, maintenance or muscle gain, with per-meal amounts.",
 h1="Macro calculator",
 lede="Set protein first, fat second and fill the rest with carbohydrate. Choose a style that suits how you like to eat.",
 fields=[SEX, AGE, HEIGHT, WEIGHT, ACTIVITY,
         F("goal", "select", "Goal", options=[("lose", "Lose fat (about −500 kcal)"), ("maintain", "Maintain"), ("gain", "Build muscle (about +300 kcal)")], default="maintain"),
         F("style", "select", "Eating style", options=[("balanced", "Balanced"), ("lowcarb", "Lower carb"), ("highcarb", "Higher carb (endurance)")], default="balanced")],
 cta="Calculate macros",
 how="""<p>Calories come from your TDEE (Mifflin-St Jeor × activity) plus the goal adjustment. Then:</p>
<ul><li><b>Protein</b>: 1.4–1.8 g per kg of body weight depending on style (at BMI over 30, a reference weight at BMI 27.5 is used).</li>
<li><b>Fat</b>: 22–40% of calories depending on style.</li><li><b>Carbohydrate</b>: the remaining calories (at least 50 g).</li></ul>
<p>Energy values: protein and carbohydrate 4 kcal per gram, fat 9 kcal per gram.</p>""",
 read="""<p>All three styles fall within the National Academies' acceptable ranges (carbohydrate 45–65%, fat 20–35%, protein 10–35% of energy) or close to their edges for the lower-carb option. The best split is the one you can keep: hit your protein and calorie targets most days and let carbs and fat flex.</p>""",
 limits="""<p>Targets are estimates. People with diabetes, kidney disease or on medicines that affect blood sugar should set macros with their care team.</p>""",
 faq=[("Do I need to hit my macros exactly?", "No. Within 10% on most days is plenty. Protein and total calories matter most."),
      ("Is low-carb better for fat loss?", "Trials show similar fat loss when calories and protein are matched. Choose what keeps you full and consistent."),
      ("How much fibre should I eat?", "About 14 g per 1,000 kcal, roughly 25–38 g a day for most adults.")],
 sources=[NASEM_MACRO, ("Jäger R, et al. ISSN position stand: protein and exercise. J Int Soc Sports Nutr, 2017", pm("Jager 2017 International Society of Sports Nutrition position stand protein and exercise")), MIFFLIN],
 related=["calories", "protein", "water"], guides=["protein", "nutrition-patterns"]),

dict(
 slug="protein", cat="nutrition", name="Protein calculator", short="Protein calculator", blurb="Daily and per-meal protein by goal and age",
 title="Protein Calculator: How Much Protein Do You Need Per Day?",
 desc="Find your daily protein target by goal and age, plus per-meal amounts, based on the RDA, ISSN and PROT-AGE recommendations.",
 h1="Protein calculator",
 lede="The RDA of 0.8 g per kg prevents deficiency. Building or keeping muscle, especially after 50, usually takes more.",
 fields=[WEIGHT, F("age", "num", "Age", ph="45", unit="years", min=18, max=100, step=1),
         F("goal", "select", "Goal", wide=True, default="active", options=[("general", "General health, little exercise"), ("active", "Regular exercise"), ("build", "Build muscle with strength training"), ("cut", "Lose fat while keeping muscle")])],
 cta="Calculate protein",
 how="""<table><thead><tr><th>Situation</th><th>Grams per kg per day</th><th>Basis</th></tr></thead><tbody>
<tr><td>General health</td><td>0.8–1.0</td><td>RDA (National Academies)</td></tr><tr><td>Adults 65+</td><td>1.0–1.2</td><td>PROT-AGE group</td></tr>
<tr><td>Regular exercise</td><td>1.2–1.6</td><td>ISSN position stand</td></tr><tr><td>Building muscle</td><td>1.6–2.2</td><td>ISSN; meta-analyses of resistance training</td></tr><tr><td>Fat loss, keeping muscle</td><td>1.6–2.4</td><td>Higher end protects lean mass in a deficit</td></tr></tbody></table>""",
 read="""<p>Split the total across three or four meals. About 0.4 g per kg per meal (roughly 25–40 g for most adults) maximises muscle building at each sitting. Breakfast is usually the gap: eggs, Greek yogurt, cottage cheese, tofu or a protein-rich smoothie close it.</p>""",
 limits="""<p>People with chronic kidney disease may need less protein; check with a clinician. Needs during pregnancy and breastfeeding are higher and should be set individually.</p>""",
 faq=[("Is high protein bad for your kidneys?", "In healthy kidneys, intakes up to about 2 g per kg have not been shown to cause harm. With existing kidney disease, follow medical advice."),
      ("Can I get enough protein on a plant-based diet?", "Yes. Combine legumes, soy, grains, nuts and seeds, and aim for the upper end of your range."),
      ("Does protein timing matter?", "Total daily intake matters most; spreading it evenly helps a little more.")],
 sources=[NASEM_MACRO, ("Bauer J, et al. Evidence-based recommendations for optimal dietary protein intake in older people (PROT-AGE). JAMDA, 2013", pm("Bauer 2013 PROT-AGE dietary protein older people")),
          ("Schoenfeld BJ, Aragon AA. How much protein can the body use in a single meal? JISSN, 2018", pm("Schoenfeld Aragon 2018 how much protein single meal"))],
 related=["macros", "one-rep-max", "calories"], guides=["protein", "strength-training"]),

dict(
 slug="water", cat="nutrition", name="Water intake calculator", short="Water intake calculator", blurb="Daily fluid for weight, exercise and heat",
 title="Water Intake Calculator: How Much Water Should You Drink?",
 desc="Estimate how much water to drink a day based on weight, exercise, hot weather, pregnancy and breastfeeding, with cups and bottles.",
 h1="Water intake calculator",
 lede="A personal starting point for daily fluids, adjusted for your size, training and climate.",
 fields=[SEX, WEIGHT, F("exercise", "num", "Exercise per day", ph="30", unit="min", min=0, max=600), F("status", "select", "Pregnancy or breastfeeding", options=[("none", "Neither"), ("pregnant", "Pregnant"), ("breastfeeding", "Breastfeeding")]),
         F("hot", "check", "I live or train in hot weather", wide=True)],
 how="""<p>We start at about 33 mL per kg of body weight, then add about 0.6 L per hour of exercise, 0.5 L for hot conditions, 0.3 L in pregnancy and 0.7 L when breastfeeding. For reference, the U.S. National Academies set adequate total water intakes of about 3.7 L a day for men and 2.7 L for women, roughly 80% of which comes from drinks.</p>""",
 read="""<p>Spread fluid through the day and drink to thirst. Urine that is pale yellow is a simple sign you are on track. Water, milk, tea and coffee all count; caffeinated drinks hydrate nearly as well as water at normal intakes.</p>""",
 limits="""<p>Heart failure, kidney disease and some medicines require fluid limits; follow your clinician's instructions. Very high intakes over a short time can be dangerous, particularly during long endurance events.</p>""",
 faq=[("Do I really need 8 glasses a day?", "It is a reasonable rough guide, not a rule. Needs vary with size, activity and climate."),
      ("Does coffee dehydrate you?", "Not at usual intakes. Coffee and tea count toward your fluid total."),
      ("How do I know if I am dehydrated?", "Dark urine, thirst, headache and fatigue are common signs.")],
 sources=[("National Academies: Dietary Reference Intakes for water, potassium, sodium, chloride and sulfate", "https://nap.nationalacademies.org/catalog/10925"), ("CDC: Water and healthier drinks", "https://www.cdc.gov/healthy-weight-growth/water-healthy-drinks/")],
 related=["caffeine", "calories-burned", "macros"], guides=["nutrition-patterns"]),

dict(
 slug="caffeine", cat="nutrition", name="Caffeine calculator", short="Caffeine calculator", blurb="Daily total vs the 400 mg limit, plus bedtime carry-over",
 title="Caffeine Calculator: Daily Total and How Much Is Left at Bedtime",
 desc="Add up caffeine from coffee, tea, energy drinks and more, compare with the 400 mg (200 mg in pregnancy) limit and estimate what is left at bedtime.",
 h1="Caffeine calculator",
 lede="Tally today's caffeine, compare it with safe limits and see roughly how much will still be circulating when you go to bed.",
 fields=[F("coffee", "num", "Brewed coffee, 8 oz cup (~95 mg)", min=0, step=1, ph="0"), F("espresso", "num", "Espresso shots (~63 mg)", min=0, step=1, ph="0"),
         F("blacktea", "num", "Black tea, cup (~47 mg)", min=0, step=1, ph="0"), F("greentea", "num", "Green tea, cup (~28 mg)", min=0, step=1, ph="0"),
         F("cola", "num", "Cola, 12 oz can (~34 mg)", min=0, step=1, ph="0"), F("energy", "num", "Energy drink, 8.4 oz (~80 mg)", min=0, step=1, ph="0"),
         F("preworkout", "num", "Pre-workout scoop (~200 mg)", min=0, step=1, ph="0"), F("chocolate", "num", "Dark chocolate, 1 oz (~20 mg)", min=0, step=1, ph="0"),
         F("last", "time", "Time of your last caffeine", opt=True), F("bed", "time", "Bedtime", opt=True), F("pregnant", "check", "I am pregnant or trying to conceive", wide=True)],
 cta="Add it up",
 how="""<p>Totals use typical caffeine contents. Carry-over at bedtime uses a 5-hour half-life, treating all of today's caffeine as if taken at your last drink, so it is an upper estimate:</p>
<p class="formula">remaining = total × 0.5^(hours until bed ÷ 5)</p>""",
 read="""<p>The U.S. FDA cites 400 mg a day as an amount not generally linked to negative effects in healthy adults. During pregnancy, obstetric guidance advises staying below 200 mg. If you sleep poorly, try a caffeine cut-off about eight hours before bed.</p>""",
 limits="""<p>Caffeine content varies widely: a large coffee-shop brew can exceed 300 mg. Sensitivity also varies; some medicines, pregnancy and liver conditions slow clearance, while smoking speeds it up.</p>""",
 faq=[("How much caffeine is too much?", "Above 400 mg a day for most healthy adults, or less if you notice jitters, a racing heart or poor sleep."),
      ("How long does caffeine last?", "Its half-life averages about 5 hours, so half of an afternoon coffee may still be active at bedtime."),
      ("Is decaf caffeine-free?", "Nearly. A cup typically has 2–15 mg.")],
 sources=[("U.S. FDA: Spilling the beans: how much caffeine is too much?", "https://www.fda.gov/consumers/consumer-updates/spilling-beans-how-much-caffeine-too-much"),
          ("American College of Obstetricians and Gynecologists: Moderate caffeine consumption during pregnancy", ""), ("USDA FoodData Central", "https://fdc.nal.usda.gov/")],
 related=["sleep", "sleep-debt", "water"], guides=["sleep"]),

# ------------------------------------------------------------------ SLEEP
dict(
 slug="sleep", cat="sleep", name="Sleep cycle calculator", short="Sleep cycle calculator", blurb="When to go to bed or wake up",
 title="Sleep Calculator: Best Bedtime and Wake-Up Time by Sleep Cycles",
 desc="Find the best time to go to bed or wake up based on 90-minute sleep cycles, so you wake between cycles feeling less groggy.",
 h1="Sleep cycle calculator",
 lede="Plan bedtime around 90-minute sleep cycles so your alarm is more likely to go off between cycles rather than in deep sleep.",
 fields=[F("mode", "radio", "I want to", options=[("wake", "Wake up at a set time"), ("bed", "Go to bed now or at a set time")], default="wake", wide=True),
         F("time", "time", "Time", default="07:00"), F("latency", "num", "Minutes to fall asleep", default="15", unit="min", min=0, max=90)],
 cta="Find my times",
 how="""<p>Sleep runs in cycles of light sleep, deep sleep and REM, each lasting roughly 90 minutes. The calculator counts back (or forward) in 90-minute steps from your chosen time and adds the minutes it usually takes you to fall asleep.</p>""",
 read="""<p>Five cycles (7.5 hours) or six (9 hours) fit the adult recommendation of 7–9 hours. Four cycles (6 hours) falls short and builds sleep debt if repeated. A fixed wake-up time, seven days a week, is the single most effective habit for steady sleep.</p>""",
 limits="""<p>Cycle length varies between people and through the night, from about 70 to 120 minutes, so these times are a guide. Persistent trouble sleeping, loud snoring or daytime sleepiness deserves a conversation with a clinician.</p>""",
 faq=[("How many hours of sleep do adults need?", "At least 7 hours a night, according to the American Academy of Sleep Medicine and Sleep Research Society."),
      ("Why do I wake up groggy after 8 hours?", "You may be waking from deep sleep, or the 8 hours includes long time awake in bed. Try shifting bedtime by 15–30 minutes."),
      ("Are naps OK?", "Short naps of 10–20 minutes before mid-afternoon refresh without hurting night sleep for most people.")],
 sources=[SLEEP_SRC, ("CDC: Sleep", "https://www.cdc.gov/sleep/")],
 related=["sleep-debt", "caffeine", "heart-rate-zones"], guides=["sleep"]),

dict(
 slug="sleep-debt", cat="sleep", name="Sleep debt calculator", short="Sleep debt calculator", blurb="Track a week of sleep against your need",
 title="Sleep Debt Calculator: How Much Sleep Do You Owe?",
 desc="Enter last week's sleep to see your sleep debt, nightly average and a realistic plan to pay it back.",
 h1="Sleep debt calculator",
 lede="Enter how long you slept each of the last seven nights to see what you owe and how to pay it back without wrecking your body clock.",
 fields=[F("need", "num", "Sleep you need per night", default="8", unit="h", min=6, max=10, step=0.25, wide=True),
         F("n1", "num", "Night 1", ph="7", unit="h", min=0, max=16), F("n2", "num", "Night 2", ph="6.5", unit="h", min=0, max=16), F("n3", "num", "Night 3", ph="7", unit="h", min=0, max=16),
         F("n4", "num", "Night 4", ph="6", unit="h", min=0, max=16), F("n5", "num", "Night 5", ph="7.5", unit="h", min=0, max=16), F("n6", "num", "Night 6", ph="8", unit="h", min=0, max=16), F("n7", "num", "Night 7", ph="8.5", unit="h", min=0, max=16)],
 cta="Calculate my sleep debt",
 how="""<p class="formula">Sleep debt = Σ (nightly need − hours slept)</p>
<p>Extra sleep on some nights offsets shortfalls on others. Count actual sleep, not time in bed.</p>""",
 read="""<p>A few hours of debt is common and recoverable. Pay it back with 30–60 extra minutes a night by going to bed earlier, keeping your wake-up time fixed. Long weekend lie-ins shift your body clock and make Monday harder.</p>""",
 limits="""<p>Chronic short sleep is not fully undone by catch-up sleep. If you need much more than 9 hours or feel sleepy despite enough time in bed, check for sleep disorders such as sleep apnoea.</p>""",
 faq=[("Can you really repay sleep debt?", "Short-term debt, yes, partly. The better strategy is to stop accruing it."),
      ("How do I know my sleep need?", "On a holiday without alarms, the amount you settle at after a few days is a good estimate. Most adults land between 7 and 9 hours."),
      ("Do sleep trackers measure sleep accurately?", "They estimate total sleep reasonably well but are less reliable for sleep stages.")],
 sources=[SLEEP_SRC, ("CDC: Sleep", "https://www.cdc.gov/sleep/")],
 related=["sleep", "caffeine", "steps"], guides=["sleep", "stress-recovery"]),

# ------------------------------------------------------------------ WOMEN'S HEALTH
dict(
 slug="due-date", cat="women", name="Pregnancy due date calculator", short="Due date calculator", blurb="Due date, weeks pregnant and milestones",
 title="Due Date Calculator: When Is My Baby Due?",
 desc="Estimate your due date from your last period (adjusted for cycle length) or conception date, see how many weeks along you are and key pregnancy milestones.",
 h1="Pregnancy due date calculator",
 lede="Estimate your due date from the first day of your last period or from the conception date, and see the milestones ahead.",
 fields=[F("method", "radio", "Calculate from", options=[("lmp", "First day of last period"), ("conception", "Conception date")], default="lmp", wide=True),
         F("date", "date", "Date"), F("cycle", "num", "Average cycle length", default="28", unit="days", min=21, max=45, step=1, show="method=lmp")],
 cta="Calculate due date",
 how="""<p>Pregnancy is dated from the first day of the last menstrual period (LMP). Naegele's rule adds 280 days (40 weeks), adjusted here for cycles longer or shorter than 28 days:</p>
<p class="formula">Due date = LMP + 280 days + (cycle length − 28)</p>
<p>From a known conception date, the due date is 266 days later.</p>""",
 read="""<p>The milestone table shows when common checks typically happen: the anatomy scan around 18–22 weeks and glucose screening around 24–28 weeks. Full term is 39 weeks 0 days to 40 weeks 6 days. The American College of Obstetricians and Gynecologists notes that an ultrasound in the first trimester is the most accurate way to confirm the due date.</p>""",
 limits="""<p>Only a small share of babies arrive on the due date itself. Irregular cycles, IVF and recent hormonal contraception change dating. Your care provider will set the official date.</p>""",
 faq=[("How accurate is a due date?", "It is an estimate. Most babies are born within two weeks before or after it."),
      ("What if I don't remember my last period?", "An early ultrasound can date the pregnancy accurately. Book an appointment with your provider."),
      ("How is IVF dated?", "From the embryo transfer date and embryo age; ask your clinic for the exact date.")],
 sources=[("ACOG Committee Opinion 700: Methods for estimating the due date", "https://www.acog.org/clinical/clinical-guidance/committee-opinion/articles/2017/05/methods-for-estimating-the-due-date"),
          ("ACOG Committee Opinion 579: Definition of term pregnancy", "")],
 related=["ovulation", "caffeine", "water"], guides=["screenings-by-age"]),

dict(
 slug="ovulation", cat="women", name="Ovulation calculator", short="Ovulation calculator", blurb="Fertile window for the next three cycles",
 title="Ovulation Calculator: Fertile Window for the Next 3 Cycles",
 desc="Estimate your ovulation day and fertile window for your next three cycles from the first day of your last period and your cycle length.",
 h1="Ovulation calculator",
 lede="Estimate your fertile window for the next three cycles. Pair it with ovulation tests for the best timing.",
 fields=[F("date", "date", "First day of your last period"), F("cycle", "num", "Average cycle length", default="28", unit="days", min=21, max=45, step=1)],
 cta="Find my fertile window",
 how="""<p>Ovulation usually happens about 14 days before the next period, because the phase after ovulation is fairly constant. So:</p>
<p class="formula">Ovulation ≈ period start + cycle length − 14 days</p>
<p>The fertile window is the five days before ovulation plus the day of ovulation, because sperm can survive several days.</p>""",
 read="""<p>The two days before ovulation and the day itself carry the highest chance of conception. If cycles vary by more than a few days, use LH ovulation test strips from a few days before the predicted date.</p>""",
 limits="""<p>Calendar methods are estimates and should not be used for contraception. If you are under 35 and have not conceived after 12 months of trying (6 months if 35 or older), talk with a clinician.</p>""",
 faq=[("Can I get pregnant outside the fertile window?", "Unlikely but possible, because ovulation timing varies from cycle to cycle."),
      ("Do apps predict ovulation better?", "Apps that use only dates have similar accuracy. Those that add temperature or LH test data do better."),
      ("What if my cycles are irregular?", "Calendar estimates are less reliable. Ovulation tests and a clinician visit help.")],
 sources=[("Wilcox AJ, et al. Timing of sexual intercourse in relation to ovulation. N Engl J Med, 1995", pm("Wilcox 1995 timing of sexual intercourse in relation to ovulation")), ("Office on Women's Health: Trying to conceive", "https://www.womenshealth.gov/")],
 related=["due-date", "caffeine", "bmi"], guides=[]),

# ------------------------------------------------------------------ PREVENTION
dict(
 slug="screenings", cat="prevention", name="Preventive screening planner", short="Screening planner", blurb="Which checks are due at your age",
 title="Preventive Screening Planner: Which Health Checks Are Due at Your Age?",
 desc="Find out which screenings are recommended for your age, sex and smoking history, from blood pressure and cholesterol to cancer screening, based on USPSTF guidance.",
 h1="Preventive screening planner",
 lede="Answer a few questions to see the screenings recommended for people like you, and which ones to raise at your next visit.",
 fields=[F("age", "num", "Age", min=18, max=100, step=1, ph="50", unit="years"), F("sex", "radio", "Sex at birth", options=[("f", "Female"), ("m", "Male")]),
         F("smoke", "select", "Smoking history", options=[("never", "Never smoked"), ("former", "Former smoker"), ("current", "Current smoker")], default="never"),
         F("packyears", "num", "Pack-years", opt=True, ph="20", help="Packs per day × years smoked."), F("quit", "num", "Years since quitting", opt=True, ph="5", show="smoke=former"),
         F("overweight", "check", "My BMI is 25 or higher (23 or higher if Asian American)", wide=True)],
 cta="Show my screenings",
 how="""<p>The planner applies the U.S. Preventive Services Task Force (USPSTF) recommendations graded A or B, which means there is good evidence of net benefit, plus a few graded C that call for a personal decision. Examples:</p>
<ul><li>Colorectal cancer screening from 45 to 75</li><li>Mammograms every two years from 40 to 74</li><li>Cervical screening from 21 to 65</li><li>Yearly low-dose CT lung screening from 50 to 80 for people with 20 or more pack-years who smoke or quit within 15 years</li>
<li>Diabetes screening from 35 to 70 with overweight or obesity</li><li>A one-time hepatitis C test from 18 to 79</li></ul>""",
 read="""<p>Use the list as a conversation starter at your next check-up. “Recommended for you” means the evidence supports screening people with your profile; your clinician may adjust timing for family history, past results or symptoms. Screening is for people without symptoms; new symptoms need prompt assessment, not a screening test.</p>""",
 limits="""<p>The planner follows U.S. guidance. Canada's Task Force on Preventive Health Care, the UK's NHS screening programmes and others differ in ages and intervals. It does not cover everything, such as vision, dental and hearing checks, or vaccines.</p>""",
 faq=[("What does a USPSTF grade A or B mean?", "High or moderate certainty that the service has a net benefit. Under U.S. law, most private plans must cover A and B services without cost-sharing."),
      ("Why did breast screening start at 40?", "In 2024 the USPSTF lowered the start age from 50 to 40 for screening every two years, citing rising incidence in women in their 40s."),
      ("I have a family history of cancer. Does this apply?", "You may need earlier or more frequent screening. Share your family history with your clinician.")],
 sources=[USPSTF, ("MyHealthfinder (U.S. Office of Disease Prevention and Health Promotion)", "https://odphp.health.gov/myhealthfinder"), ("American Diabetes Association: Standards of Care, screening", "https://diabetes.org/")],
 related=["blood-pressure", "a1c", "cholesterol"], guides=["screenings-by-age"]),
]
