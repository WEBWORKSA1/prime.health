"""Tool content: body composition, heart & metabolic, fitness."""
from tf import F, pm, SEX, AGE, HEIGHT, WEIGHT, CDC_BMI, WHO_PA, AHA_BP, ACC_AHA_2025, NHLBI_METS, KODAMA, DING, COMPENDIUM

TOOLS_A = [
# ------------------------------------------------------------------ BODY
dict(
 slug="bmi", cat="body", name="BMI & BMI Prime calculator", short="BMI calculator", blurb="Body mass index plus BMI Prime and your healthy weight range",
 title="BMI Calculator with BMI Prime (Metric & US Units)",
 desc="Calculate your BMI and BMI Prime in seconds. See your healthy weight range, standard and Asian cut-offs, and what BMI can and cannot tell you.",
 h1="BMI & BMI Prime calculator",
 lede="Body mass index compares your weight with your height. BMI Prime divides it by 25, the top of the healthy range, so 1.00 is the line to stay at or under.",
 fields=[HEIGHT, WEIGHT, F("asian", "check", "Use Asian cut-offs (WHO expert consultation)", wide=True, help="Health risks rise at lower BMIs in many Asian populations.")],
 cta="Calculate BMI",
 how="""<p>BMI is your weight in kilograms divided by the square of your height in metres. In US units the same number comes from pounds and inches multiplied by 703.</p>
<p class="formula">BMI = weight (kg) ÷ height (m)² &nbsp;&nbsp;|&nbsp;&nbsp; BMI = 703 × weight (lb) ÷ height (in)²</p>
<p>BMI Prime, introduced in a 2006 medical paper, divides your BMI by 25, the upper limit of the healthy range:</p>
<p class="formula">BMI Prime = BMI ÷ 25</p>
<p>That turns BMI into a ratio. A BMI Prime of 1.00 sits exactly on the healthy limit. A value of 1.20 means you are 20% above it, and 0.90 means you have a 10% margin. It is the same information as BMI, expressed in a way that makes progress easy to read.</p>""",
 read="""<table><thead><tr><th>BMI</th><th>BMI Prime</th><th>Category (adults)</th></tr></thead><tbody>
<tr><td>Below 18.5</td><td>Below 0.74</td><td>Underweight</td></tr><tr><td>18.5–24.9</td><td>0.74–1.00</td><td>Healthy weight</td></tr>
<tr><td>25–29.9</td><td>1.00–1.20</td><td>Overweight</td></tr><tr><td>30–34.9</td><td>1.20–1.40</td><td>Obesity class I</td></tr>
<tr><td>35–39.9</td><td>1.40–1.60</td><td>Obesity class II</td></tr><tr><td>40 and above</td><td>1.60 and above</td><td>Obesity class III</td></tr></tbody></table>
<p>With Asian cut-offs, a BMI of 23–27.4 signals increased risk and 27.5 or more signals high risk, following the World Health Organization expert consultation. The calculator also shows the weight range that keeps you between BMI 18.5 and the healthy upper limit for your height.</p>""",
 limits="""<ul><li><b>Muscle looks like fat.</b> Strength athletes often score as overweight while carrying little fat.</li>
<li><b>Fat location matters more than weight.</b> Fat around the waist carries more risk. Check your <a href="waist-to-height.html">waist-to-height ratio</a> too.</li>
<li><b>Older adults</b> can have a normal BMI with low muscle mass.</li>
<li><b>Not for children, teens or pregnancy.</b> Under 20, BMI is read against age- and sex-specific percentiles.</li></ul>""",
 faq=[("Is BMI accurate?", "BMI is a fast, free screening number that tracks with health risk across large groups. It is less accurate for individuals with a lot of muscle, older adults and some ethnic groups, so pair it with waist measures."),
      ("What is a good BMI Prime?", "Between 0.74 and 1.00, which equals a BMI of 18.5 to 24.9. Below 0.74 is underweight; above 1.00 is over the healthy limit."),
      ("Should I use the Asian cut-offs?", "If you have South Asian, East Asian or Southeast Asian ancestry, the lower cut-offs better reflect the BMI at which risks of type 2 diabetes and heart disease begin to climb.")],
 sources=[CDC_BMI, ("WHO expert consultation. Appropriate BMI for Asian populations. Lancet, 2004", pm("WHO expert consultation appropriate body-mass index Asian populations 2004")),
          ("Gadzik J. 'How much should I weigh?' Quetelet's equation, upper weight limits and BMI Prime. Conn Med, 2006", pm("Gadzik BMI prime 2006"))],
 related=["waist-to-height", "body-fat", "ideal-weight"], guides=["prime-numbers", "metabolic-health"]),

dict(
 slug="body-fat", cat="body", name="Body fat calculator (US Navy method)", short="Body fat calculator", blurb="Estimate body fat % from a tape measure",
 title="Body Fat Calculator: U.S. Navy Tape Method",
 desc="Estimate your body fat percentage with a tape measure using the U.S. Navy formula. See fat mass, lean mass and where you fall in the ACE categories.",
 h1="Body fat calculator",
 lede="A tape measure and three or four measurements give a body fat estimate that is usually within a few percentage points of lab methods.",
 fields=[SEX, HEIGHT, F("neck", "len", "Neck", ph="38", ph_i="15"), F("waist", "len", "Waist", ph="86", ph_i="34"),
         F("hip", "len", "Hip", ph="100", ph_i="39", show="sex=f"), F("weight", "weight", "Weight", opt=True, help="Adds fat mass and lean mass.")],
 how="""<p>The U.S. Navy method, developed by Hodgdon and Beckett in 1984, predicts body fat from circumferences. The metric versions are:</p>
<p class="formula">Men: %BF = 495 ÷ (1.0324 − 0.19077·log₁₀(waist − neck) + 0.15456·log₁₀(height)) − 450</p>
<p class="formula">Women: %BF = 495 ÷ (1.29579 − 0.35004·log₁₀(waist + hip − neck) + 0.22100·log₁₀(height)) − 450</p>
<p>All measurements are in centimetres. <b>How to measure:</b> neck just below the larynx, tape sloping slightly down to the front; waist at the navel for men and at the narrowest point for women, relaxed, after a normal breath out; hips at the widest point of the buttocks. Measure twice and use the average.</p>""",
 read="""<table><thead><tr><th>Category (ACE)</th><th>Women</th><th>Men</th></tr></thead><tbody>
<tr><td>Essential fat</td><td>10–13%</td><td>2–5%</td></tr><tr><td>Athletes</td><td>14–20%</td><td>6–13%</td></tr><tr><td>Fitness</td><td>21–24%</td><td>14–17%</td></tr>
<tr><td>Average</td><td>25–31%</td><td>18–24%</td></tr><tr><td>Obese</td><td>32% and above</td><td>25% and above</td></tr></tbody></table>
<p>Women carry more essential fat for hormonal and reproductive health, which is why the ranges differ. If you add your weight, the calculator splits it into fat mass and lean mass, which is the most useful number to track while training.</p>""",
 limits="""<p>Tape methods typically land within 3–4 percentage points of DEXA or underwater weighing, and errors are larger at very high or very low body fat. Measurement technique causes most of the error, so be consistent: same time of day, same tape, same spots. Watch the trend over weeks rather than a single reading.</p>""",
 faq=[("Is the Navy method accurate?", "For most people it is within a few percentage points of lab methods, which is comparable to many home scales. It is good for tracking change over time."),
      ("Why does it need my neck?", "Neck size is a proxy for lean mass in the upper body. Subtracting it from waist (and hip) isolates fat-heavy circumference."),
      ("What body fat should I aim for?", "For health, the fitness and lower average ranges are a sensible target: about 14–24% for men and 21–31% for women.")],
 sources=[("Hodgdon JA, Beckett MB. Prediction of percent body fat for U.S. Navy men and women from body circumferences and height. Naval Health Research Center, 1984", ""),
          ("American Council on Exercise: body-fat percentage categories", ""), ("U.S. Department of Defense body composition program (DoDI 1308.03)", "")],
 related=["bmi", "waist-to-height", "protein"], guides=["strength-training", "metabolic-health"]),

dict(
 slug="waist-to-height", cat="body", name="Waist-to-height ratio calculator", short="Waist-to-height ratio", blurb="Keep your waist under half your height",
 title="Waist-to-Height Ratio Calculator: Is Your Waist Under Half Your Height?",
 desc="Check your waist-to-height ratio, the simple measure of belly fat linked to heart and metabolic risk. Target: below 0.5.",
 h1="Waist-to-height ratio calculator",
 lede="One rule, two numbers: keep your waist to less than half your height. It flags belly fat that BMI misses.",
 fields=[F("waist", "len", "Waist", ph="86", ph_i="34", help="Halfway between your lowest rib and the top of your hip bone, after breathing out."), HEIGHT],
 how="""<p>Divide your waist circumference by your height, using the same unit for both.</p>
<p class="formula">WHtR = waist ÷ height</p>
<p>Fat stored around the organs (visceral fat) drives insulin resistance, raised blood pressure and unhealthy cholesterol. Waist size tracks visceral fat far better than weight, and dividing by height makes the number fair for tall and short people. Research reviews have found waist-to-height ratio predicts heart and metabolic risk at least as well as BMI or waist alone, and the UK's NICE guidance adopted the 0.5 boundary for adults in 2022.</p>""",
 read="""<table><thead><tr><th>Ratio</th><th>Meaning</th></tr></thead><tbody>
<tr><td>0.40–0.49</td><td>Healthy central fat. No increased risk.</td></tr><tr><td>0.50–0.59</td><td>Increased health risk. Worth acting on.</td></tr>
<tr><td>0.60 and above</td><td>High health risk. Talk to a clinician about blood pressure, glucose and lipids.</td></tr></tbody></table>
<p>A ratio below 0.40 can occur in very lean people; it is not itself a disease marker, but if you are also underweight by BMI, look at nutrition. The calculator shows the waist size that would put you exactly at 0.5.</p>""",
 limits="""<p>The boundary values were set for adults. They are not designed for pregnancy, and some athletes with very large torsos may read high. Measure at the same point each time; moving the tape a few centimetres changes the result.</p>""",
 faq=[("Where exactly do I measure my waist?", "Find the bottom of your lowest rib and the top of your hip bone. Measure halfway between them, tape level, after a normal breath out. Do not suck in."),
      ("Is this better than BMI?", "They answer different questions. BMI is about overall size; waist-to-height ratio is about where fat sits. Together they give a fuller picture."),
      ("How fast can it change?", "Waist size responds to activity and diet within weeks. A 2–3 cm drop is meaningful.")],
 sources=[("Ashwell M, et al. Waist-to-height ratio is a better screening tool than waist circumference and BMI. Obes Rev, 2012", pm("Ashwell waist-to-height ratio meta-analysis 2012")),
          ("NICE: obesity identification and classification, waist-to-height ratio", "https://www.nice.org.uk/search?q=waist-to-height+ratio")],
 related=["bmi", "waist-to-hip", "metabolic"], guides=["metabolic-health", "prime-numbers"]),

dict(
 slug="waist-to-hip", cat="body", name="Waist-to-hip ratio calculator", short="Waist-to-hip ratio", blurb="WHO waist and waist-to-hip cut-offs",
 title="Waist-to-Hip Ratio Calculator with WHO Cut-offs",
 desc="Calculate your waist-to-hip ratio and compare it, and your waist size, with World Health Organization risk cut-offs for men and women.",
 h1="Waist-to-hip ratio calculator",
 lede="Compares the narrowest point of your waist with the widest point of your hips. A higher ratio means more fat stored around the middle.",
 fields=[SEX, F("waist", "len", "Waist", ph="86", ph_i="34"), F("hip", "len", "Hip", ph="100", ph_i="39")],
 how="""<p class="formula">WHR = waist circumference ÷ hip circumference</p>
<p>The World Health Organization's 2008 expert report on waist measures links a ratio of 0.90 or more in men and 0.85 or more in women with substantially increased metabolic risk. The same report sets waist-circumference action levels: increased risk above 94 cm (37 in) in men and 80 cm (31.5 in) in women; substantially increased above 102 cm (40 in) and 88 cm (35 in).</p>
<p>Measure the waist midway between the lowest rib and the top of the hip bone and the hips at the widest part of the buttocks, standing with feet together.</p>""",
 read="""<p>Below the cut-off for your sex is the target. Above it, central fat is likely contributing to risk even if your weight is normal. The second bar shows your waist alone against the WHO levels, which some clinicians prefer because it needs only one measurement.</p>""",
 limits="""<p>The ratio can stay the same while both measures shrink, so also track waist on its own. Cut-offs differ for some populations; for many Asian adults, guidelines use lower waist thresholds (about 90 cm for men and 80 cm for women).</p>""",
 faq=[("What is a healthy waist-to-hip ratio?", "Below 0.90 for men and below 0.85 for women, according to the World Health Organization."),
      ("Waist-to-hip or waist-to-height: which is better?", "Both flag central fat. Waist-to-height has a single cut-off (0.5) for everyone and has slightly stronger evidence for predicting risk."),
      ("Why does my ratio go up as I get older?", "After midlife, fat tends to shift toward the abdomen, especially after menopause, even when weight is stable.")],
 sources=[("WHO. Waist circumference and waist–hip ratio: report of a WHO expert consultation, 2008", "https://www.who.int/publications/i/item/9789241501491"), NHLBI_METS],
 related=["waist-to-height", "bmi", "body-fat"], guides=["metabolic-health"]),

dict(
 slug="ideal-weight", cat="body", name="Ideal weight calculator", short="Ideal weight calculator", blurb="Four classic formulas plus the healthy BMI range",
 title="Ideal Weight Calculator: Devine, Robinson, Miller & Hamwi",
 desc="See your ideal body weight from four classic formulas side by side, plus the healthy BMI weight range for your height.",
 h1="Ideal weight calculator",
 lede="Four formulas used in medicine for decades, compared side by side, plus the healthy-BMI range that is the better target for most people.",
 fields=[SEX, HEIGHT],
 how="""<p>Each formula starts from a base weight at 5 feet (152.4 cm) and adds a fixed amount per inch above it:</p>
<table><thead><tr><th>Formula</th><th>Men</th><th>Women</th></tr></thead><tbody>
<tr><td>Devine (1974)</td><td>50 kg + 2.3 kg/inch</td><td>45.5 kg + 2.3 kg/inch</td></tr><tr><td>Robinson (1983)</td><td>52 kg + 1.9 kg/inch</td><td>49 kg + 1.7 kg/inch</td></tr>
<tr><td>Miller (1983)</td><td>56.2 kg + 1.41 kg/inch</td><td>53.1 kg + 1.36 kg/inch</td></tr><tr><td>Hamwi (1964)</td><td>48 kg + 2.7 kg/inch</td><td>45.5 kg + 2.2 kg/inch</td></tr></tbody></table>
<p>Devine's formula was created to dose medicines, not to define a healthy body, yet it spread into general use. The calculator shows all four and the range they span.</p>""",
 read="""<p>Read the spread, not a single number. The healthy BMI range (18.5–24.9) for your height is shown beneath the table; it is linked to health outcomes, so use it as your main target and the formulas as a reference point.</p>""",
 limits="""<p>None of these formulas account for muscle, frame size or age, and they were built for heights of 5 ft and above. Athletes may sit well above them while being lean.</p>""",
 faq=[("Which ideal weight formula is best?", "None is clearly best for health. Robinson and Miller tend to give more realistic figures for women; Hamwi is the most generous for tall men. The healthy BMI range is the more meaningful target."),
      ("Why do hospitals still use ideal body weight?", "Some drug doses and ventilator settings are based on ideal body weight because they relate to lean tissue rather than total weight."),
      ("I am below 5 feet. Does this work?", "The formulas become unreliable below 5 ft. Use the healthy BMI range instead.")],
 sources=[("Devine BJ. Gentamicin therapy. Drug Intell Clin Pharm, 1974", pm("Devine 1974 gentamicin therapy ideal body weight")), ("Robinson JD, et al. Determination of ideal body weight for drug dosage calculations. Am J Hosp Pharm, 1983", pm("Robinson 1983 ideal body weight drug dosage")), CDC_BMI],
 related=["bmi", "body-fat", "calories"], guides=["prime-numbers"]),

# ------------------------------------------------------------------ HEART & METABOLIC
dict(
 slug="blood-pressure", cat="heart", name="Blood pressure checker", short="Blood pressure checker", blurb="2025 guideline categories, averaged readings",
 title="Blood Pressure Checker: What Your Reading Means (2025 Guideline)",
 desc="Enter up to three blood pressure readings to see your average and category under the 2025 AHA/ACC guideline: normal, elevated, stage 1 or stage 2.",
 h1="Blood pressure checker",
 lede="Enter up to three readings. We average them and place you in the categories of the 2025 American Heart Association and American College of Cardiology guideline.",
 fields=[F("s1", "num", "Reading 1: top number (systolic)", ph="122", unit="mm Hg", min=60, max=260), F("d1", "num", "Reading 1: bottom number (diastolic)", ph="78", unit="mm Hg", min=30, max=160),
         F("s2", "num", "Reading 2: systolic", ph="120", unit="mm Hg", opt=True), F("d2", "num", "Reading 2: diastolic", ph="76", unit="mm Hg", opt=True),
         F("s3", "num", "Reading 3: systolic", ph="", unit="mm Hg", opt=True), F("d3", "num", "Reading 3: diastolic", ph="", unit="mm Hg", opt=True)],
 cta="Check my reading",
 how="""<p>Blood pressure has two numbers. Systolic (top) is the pressure when the heart beats; diastolic (bottom) is the pressure between beats. Your category is set by whichever number falls in the higher category.</p>
<table><thead><tr><th>Category</th><th>Systolic</th><th></th><th>Diastolic</th></tr></thead><tbody>
<tr><td>Normal</td><td>below 120</td><td>and</td><td>below 80</td></tr><tr><td>Elevated</td><td>120–129</td><td>and</td><td>below 80</td></tr>
<tr><td>Stage 1 hypertension</td><td>130–139</td><td>or</td><td>80–89</td></tr><tr><td>Stage 2 hypertension</td><td>140 or higher</td><td>or</td><td>90 or higher</td></tr>
<tr><td>Severe range</td><td>above 180</td><td>and/or</td><td>above 120</td></tr></tbody></table>
<p>The 2025 guideline kept the 2017 categories, set a target below 130/80 for most adults and introduced the PREVENT risk calculator to guide treatment decisions.</p>""",
 read="""<p><b>How to measure well:</b> sit quietly for 5 minutes with your back supported and feet flat; rest your arm at heart level on a table; use a cuff that fits your upper arm; no caffeine, exercise or smoking for 30 minutes; take two readings a minute apart and average them. Home readings over a week are more reliable than a single clinic reading.</p>
<p>Elevated and stage 1 readings usually start with lifestyle steps: less sodium, more potassium-rich foods, regular activity, weight loss if needed and limiting alcohol. Your clinician decides on medication based on your overall risk.</p>""",
 limits="""<p>This tool sorts readings into categories; it cannot diagnose hypertension, which needs repeated readings over time. Wrist and finger devices are less accurate than validated upper-arm cuffs. If you are pregnant, different thresholds apply.</p>""",
 faq=[("Is 130/80 high blood pressure?", "Yes. Since 2017, and confirmed in the 2025 guideline, 130/80 marks stage 1 hypertension in the U.S. guideline. Some other countries still use 140/90 as the threshold."),
      ("Why is my reading higher at the doctor's office?", "Many people have 'white coat' effect. Home or 24-hour monitoring gives a truer picture."),
      ("What is a dangerous blood pressure?", "Above 180/120 is the severe range. Re-check after 5 minutes of rest. If it stays that high, contact your doctor straight away; with symptoms such as chest pain or trouble speaking, call emergency services.")],
 sources=[AHA_BP, ACC_AHA_2025, ("CDC: High blood pressure facts", "https://www.cdc.gov/high-blood-pressure/")],
 related=["metabolic", "cholesterol", "heart-rate-zones"], guides=["blood-pressure", "prime-numbers"]),

dict(
 slug="a1c", cat="heart", name="A1C to average glucose converter", short="A1C converter", blurb="A1C ↔ eAG in mg/dL and mmol/L, with ADA ranges",
 title="A1C Calculator: Convert A1C to Average Blood Sugar (eAG)",
 desc="Convert A1C to estimated average glucose in mg/dL and mmol/L, or back again, and see whether it falls in the normal, prediabetes or diabetes range.",
 h1="A1C to average glucose converter",
 lede="A1C reflects your average blood sugar over about three months. Convert it to everyday glucose units, or turn a meter or sensor average into an A1C estimate.",
 fields=[F("dir", "radio", "I want to convert", options=[("a1c", "A1C → average glucose"), ("eag", "Average glucose → A1C")], default="a1c", wide=True),
         F("a1c", "num", "A1C", ph="5.6", unit="%", min=3, max=20, show="dir=a1c"),
         F("eag", "num", "Average glucose", ph="114", show="dir=eag"), F("gunit", "select", "Glucose unit", options=[("mgdl", "mg/dL"), ("mmol", "mmol/L")], show="dir=eag")],
 cta="Convert",
 how="""<p>The conversion comes from the A1C-Derived Average Glucose study, which compared A1C with continuous glucose readings:</p>
<p class="formula">eAG (mg/dL) = 28.7 × A1C − 46.7 &nbsp;&nbsp;|&nbsp;&nbsp; eAG (mmol/L) = eAG (mg/dL) ÷ 18</p>
<p>The calculator also shows the IFCC unit used in many countries: mmol/mol = (A1C% − 2.15) × 10.929.</p>""",
 read="""<table><thead><tr><th>A1C</th><th>Estimated average glucose</th><th>Range (ADA)</th></tr></thead><tbody>
<tr><td>Below 5.7%</td><td>below 117 mg/dL (6.5 mmol/L)</td><td>Normal</td></tr><tr><td>5.7–6.4%</td><td>117–137 mg/dL</td><td>Prediabetes range</td></tr><tr><td>6.5% or higher</td><td>140 mg/dL (7.8 mmol/L) or higher</td><td>Diabetes range</td></tr></tbody></table>
<p>For many adults living with diabetes, a common treatment goal is below 7%, set individually with their care team. Each one-point drop in A1C is linked to fewer eye, kidney and nerve complications.</p>""",
 limits="""<p>A1C can read falsely high or low with anaemia, recent blood loss or transfusion, kidney disease, pregnancy and some inherited haemoglobin variants. Diagnosis needs a lab test, usually repeated. Sensor averages over 14 days and lab A1C may differ; the gap is normal.</p>""",
 faq=[("What is a normal A1C?", "Below 5.7%. Between 5.7% and 6.4% is the prediabetes range; 6.5% or higher on two tests indicates diabetes."),
      ("How often should A1C be checked?", "Without diabetes, as part of screening every 1–3 years depending on risk. With diabetes, usually every 3–6 months."),
      ("Can I lower my A1C without medicine?", "In the prediabetes range, structured lifestyle programs that combine activity and modest weight loss lower the chance of progressing to type 2 diabetes. Discuss a plan with your clinician.")],
 sources=[("American Diabetes Association: Understanding A1C", "https://diabetes.org/about-diabetes/a1c"), ("Nathan DM, et al. Translating the A1C assay into estimated average glucose values. Diabetes Care, 2008", pm("Nathan 2008 translating A1C assay estimated average glucose")),
          ("CDC: Diabetes testing", "https://www.cdc.gov/diabetes/")],
 related=["metabolic", "bmi", "screenings"], guides=["metabolic-health", "prime-numbers"]),

dict(
 slug="cholesterol", cat="heart", name="Cholesterol calculator (non-HDL & ratios)", short="Cholesterol calculator", blurb="Non-HDL, HDL, LDL bands and total/HDL ratio",
 title="Cholesterol Calculator: Non-HDL Cholesterol and Ratios Explained",
 desc="Enter your lipid panel to calculate non-HDL cholesterol and the total/HDL ratio, and see where HDL, LDL and triglycerides fall. mg/dL or mmol/L.",
 h1="Cholesterol calculator",
 lede="Turn your lipid panel into the two numbers many experts watch most: non-HDL cholesterol and the total-to-HDL ratio.",
 fields=[F("unit", "select", "Lab units", options=[("mgdl", "mg/dL (US)"), ("mmol", "mmol/L (Canada, UK, EU, Australia)")], wide=True), SEX,
         F("tc", "num", "Total cholesterol", ph="190"), F("hdl", "num", "HDL cholesterol", ph="55"), F("ldl", "num", "LDL cholesterol", ph="110", opt=True), F("tg", "num", "Triglycerides", ph="120", opt=True)],
 how="""<p class="formula">Non-HDL cholesterol = total cholesterol − HDL &nbsp;&nbsp;|&nbsp;&nbsp; Ratio = total ÷ HDL</p>
<p>Non-HDL cholesterol captures every cholesterol-carrying particle that can lodge in artery walls (LDL, VLDL, remnants and Lp(a)). It does not need fasting and stays accurate when triglycerides are high, which is why the National Lipid Association treats it as a primary target. To convert mmol/L to mg/dL, multiply cholesterol values by 38.67 and triglycerides by 88.57.</p>""",
 read="""<table><thead><tr><th>Non-HDL (mg/dL)</th><th>mmol/L</th><th>Category</th></tr></thead><tbody>
<tr><td>below 130</td><td>below 3.4</td><td>Desirable</td></tr><tr><td>130–159</td><td>3.4–4.1</td><td>Above desirable</td></tr><tr><td>160–189</td><td>4.1–4.9</td><td>Borderline high</td></tr>
<tr><td>190–219</td><td>4.9–5.7</td><td>High</td></tr><tr><td>220 or more</td><td>5.7 or more</td><td>Very high</td></tr></tbody></table>
<p>HDL below 40 mg/dL in men or 50 mg/dL in women counts as low. LDL categories follow the long-standing NCEP bands (optimal below 100 mg/dL). Triglycerides below 150 mg/dL are normal. Your clinician combines these with age, blood pressure, diabetes and smoking to estimate 10-year risk.</p>""",
 limits="""<p>Targets are lower if you already have heart disease, diabetes or very high risk, and are set with your clinician. LDL of 190 mg/dL (4.9 mmol/L) or more can point to familial hypercholesterolaemia, which runs in families and deserves early attention. Lipoprotein(a) is inherited and not shown on a standard panel; consider asking for it once.</p>""",
 faq=[("What is a good non-HDL cholesterol?", "Below 130 mg/dL (3.4 mmol/L) for most adults without heart disease."),
      ("Do I need to fast before a cholesterol test?", "Usually not. Non-fasting panels are fine for most people; fasting may be requested if triglycerides are very high."),
      ("Can I raise HDL to cancel out high LDL?", "No. Raising HDL with drugs did not cut heart attacks in trials. Lowering LDL and non-HDL is what reduces risk.")],
 sources=[("Jacobson TA, et al. National Lipid Association recommendations for patient-centered management of dyslipidemia, 2015", pm("Jacobson 2015 National Lipid Association recommendations dyslipidemia")),
          ("NHLBI: ATP III at a glance", "https://www.nhlbi.nih.gov/files/docs/guidelines/atglance.pdf"), ("CDC: Cholesterol", "https://www.cdc.gov/cholesterol/")],
 related=["metabolic", "blood-pressure", "screenings"], guides=["prime-numbers", "nutrition-patterns"]),

dict(
 slug="metabolic", cat="heart", name="Metabolic syndrome checker", short="Metabolic health check", blurb="Five markers: waist, triglycerides, HDL, BP, glucose",
 title="Metabolic Syndrome Checker: Count Your 5 Markers",
 desc="Check the five markers of metabolic syndrome (waist, triglycerides, HDL, blood pressure, fasting glucose) against the harmonized international definition.",
 h1="Metabolic health check",
 lede="Five everyday measurements define metabolic syndrome. Three or more out of range roughly doubles the risk of heart disease and sharply raises diabetes risk.",
 fields=[SEX, F("pop", "select", "Waist cut-off to use", options=[("std", "Standard (US/Europe)"), ("asian", "Asian populations")]), F("waist", "len", "Waist", opt=True, ph="92", ph_i="36"),
         F("unit", "select", "Lab units", options=[("mgdl", "mg/dL"), ("mmol", "mmol/L")]), F("tg", "num", "Triglycerides", opt=True, ph="140"), F("hdl", "num", "HDL cholesterol", opt=True, ph="48"),
         F("fg", "num", "Fasting glucose", opt=True, ph="95"), F("sbp", "num", "Blood pressure: systolic", opt=True, ph="124", unit="mm Hg"), F("dbp", "num", "Blood pressure: diastolic", opt=True, ph="80", unit="mm Hg"),
         F("bpmed", "check", "I take blood pressure medicine", wide=True), F("lipidmed", "check", "I take medicine for high triglycerides or low HDL", wide=True), F("glucmed", "check", "I take medicine to lower blood sugar", wide=True)],
 cta="Check my markers",
 how="""<p>The 2009 harmonized definition, agreed by the International Diabetes Federation, the American Heart Association, NHLBI and others, diagnoses metabolic syndrome when <b>any three</b> of these five are present:</p>
<ul><li>Waist at or above the population cut-off (102 cm men / 88 cm women in US-style use; 90 / 80 cm for Asian populations)</li>
<li>Triglycerides 150 mg/dL (1.7 mmol/L) or more, or on treatment</li><li>HDL below 40 mg/dL (1.0 mmol/L) in men or 50 mg/dL (1.3 mmol/L) in women, or on treatment</li>
<li>Blood pressure 130/85 or more, or on treatment</li><li>Fasting glucose 100 mg/dL (5.6 mmol/L) or more, or on treatment</li></ul>""",
 read="""<p>Zero criteria is the goal. One or two means a marker needs attention before it becomes three. Three or more meets the definition; it does not mean you are ill today, but it is a strong signal to act and to review the numbers with a clinician. The same changes improve every marker at once: more movement, less refined carbohydrate and alcohol, better sleep and, if needed, weight loss of 5–10%.</p>""",
 limits="""<p>Leave out what you do not know; the tool counts only what you enter and tells you how many markers are missing. Lab values should be from a fasting sample for glucose. This is a screening aid, not a diagnosis.</p>""",
 faq=[("How common is metabolic syndrome?", "Roughly one in three U.S. adults meets the definition, and the share rises with age."),
      ("Can metabolic syndrome be reversed?", "Yes. Lifestyle change can bring markers back under the cut-offs; many people move from three criteria to fewer within months."),
      ("Why does waist count when weight does not?", "Waist size reflects fat around the organs, which drives insulin resistance and the other four markers.")],
 sources=[("Alberti KGMM, et al. Harmonizing the metabolic syndrome. Circulation, 2009", pm("Alberti 2009 harmonizing the metabolic syndrome")), NHLBI_METS],
 related=["waist-to-height", "a1c", "cholesterol"], guides=["metabolic-health"]),

# ------------------------------------------------------------------ FITNESS
dict(
 slug="heart-rate-zones", cat="fitness", name="Heart rate zone calculator", short="Heart rate zones", blurb="Zone 2 and all five training zones",
 title="Heart Rate Zone Calculator: Find Your Zone 2",
 desc="Calculate your maximum heart rate and five training zones, including Zone 2, using the Tanaka or 220-minus-age formula and optional resting heart rate.",
 h1="Heart rate zone calculator",
 lede="Find your five training zones, including the conversational Zone 2 that builds your aerobic base. Add your resting pulse for a personalised version.",
 fields=[F("age", "num", "Age", min=15, max=100, step=1, ph="40", unit="years"), F("rhr", "num", "Resting heart rate", opt=True, ph="62", unit="bpm", help="Count your pulse for 60 seconds before getting out of bed."),
         F("method", "radio", "Max heart rate formula", options=[("tanaka", "Tanaka (208 − 0.7 × age)"), ("classic", "Classic (220 − age)")], default="tanaka", wide=True)],
 cta="Show my zones",
 how="""<p>Maximum heart rate falls with age. The Tanaka formula, from a 2001 meta-analysis of 351 studies, fits adults better than the classic 220 − age, especially after 40:</p>
<p class="formula">HRmax = 208 − 0.7 × age</p>
<p>If you enter a resting heart rate, zones use the Karvonen method, which scales the zones to your heart-rate reserve:</p>
<p class="formula">Target = resting HR + (HRmax − resting HR) × intensity %</p>""",
 read="""<p><b>Zone 2</b> (about 60–70%) is where you can talk in full sentences but would rather not sing. Long, easy sessions here build the mitochondria and capillaries behind endurance. <b>Zones 4–5</b> are short, hard efforts that raise VO₂ max. A common evidence-informed split is mostly easy training with one or two harder sessions each week. Guidelines count Zones 2–3 as moderate activity and Zones 4–5 as vigorous.</p>
<p>A resting heart rate between 60 and 100 bpm is considered normal for adults; fit people often sit below 60.</p>""",
 limits="""<p>Any formula can be 10–12 bpm away from your true maximum. Beta-blockers and some other medicines lower heart rate, so zones will not apply; use perceived effort instead. If you have heart disease, ask your clinician for safe training ranges.</p>""",
 faq=[("What is Zone 2 heart rate?", "About 60–70% of maximum heart rate, or 60–70% of heart-rate reserve with Karvonen. The talk test is a reliable check."),
      ("Is 220 minus age accurate?", "It is a rough rule that tends to underestimate maximum heart rate in older adults. Tanaka's formula fits better on average."),
      ("How much Zone 2 should I do?", "WHO advises 150–300 minutes of moderate activity a week. Much of that can be Zone 2.")],
 sources=[("Tanaka H, Monahan KD, Seals DR. Age-predicted maximal heart rate revisited. J Am Coll Cardiol, 2001", pm("Tanaka 2001 age-predicted maximal heart rate revisited")),
          ("American Heart Association: Target heart rates", "https://www.heart.org/en/healthy-living/fitness/fitness-basics/target-heart-rates"), WHO_PA],
 related=["vo2max", "calories-burned", "pace"], guides=["vo2max-zone2"]),

dict(
 slug="vo2max", cat="fitness", name="VO₂ max calculator", short="VO₂ max estimator", blurb="Estimate from resting pulse or a 12-minute run",
 title="VO2 Max Calculator: Estimate Your Fitness From Heart Rate or a 12-Minute Run",
 desc="Estimate your VO2 max from resting heart rate (Uth–Sørensen) or the Cooper 12-minute run test, and see your fitness in METs.",
 h1="VO₂ max calculator",
 lede="VO₂ max is the most oxygen your body can use. It is one of the strongest predictors of how long and how well people live, and it responds to training at any age.",
 fields=[F("method", "radio", "Method", options=[("rest", "Resting heart rate"), ("cooper", "12-minute run test")], default="rest", wide=True),
         F("age", "num", "Age", ph="40", unit="years", show="method=rest"), F("rhr", "num", "Resting heart rate", ph="60", unit="bpm", show="method=rest"),
         F("hrmax", "num", "Measured max heart rate", opt=True, ph="", unit="bpm", show="method=rest"), F("dist", "dist", "Distance in 12 minutes", show="method=cooper")],
 cta="Estimate VO₂ max",
 how="""<p><b>Resting heart-rate method</b> (Uth–Sørensen, 2004):</p><p class="formula">VO₂ max ≈ 15.3 × HRmax ÷ HRrest</p>
<p>If you do not enter a measured maximum, the tool uses Tanaka's 208 − 0.7 × age.</p>
<p><b>Cooper 12-minute test</b> (1968): warm up, then run or walk as far as you can in 12 minutes on a flat track.</p><p class="formula">VO₂ max ≈ (distance in metres − 504.9) ÷ 44.73</p>
<p>The result is shown in mL of oxygen per kg per minute and in METs (1 MET = 3.5 mL/kg/min).</p>""",
 read="""<p>Higher is better at every age. In a 2009 JAMA meta-analysis of 33 studies, each 1-MET increase in fitness was associated with about 13% lower risk of death from any cause and 15% lower risk of heart disease events. A 2018 study of more than 120,000 treadmill tests found people in the lowest fitness group had a higher risk of death than those with diabetes or a smoking history. Use the “next milestone” figure as your target for the next few months.</p>""",
 limits="""<p>Field estimates usually fall within about 10% of a lab test but can miss by more. The resting method is weaker for very fit or unfit people and anyone on heart-rate-lowering medicine. Do not attempt a maximal run test if you have chest symptoms or heart disease without medical clearance.</p>""",
 faq=[("What is a good VO₂ max?", "It depends on age and sex. Rather than chase a label, aim to sit above the average for your age and add 1 MET (3.5 mL/kg/min) over the next few months."),
      ("How do I raise my VO₂ max?", "Combine plenty of easy aerobic work with one weekly session of hard intervals, such as 4 × 4 minutes at a hard effort with 3 minutes easy between."),
      ("Are smartwatch VO₂ max numbers reliable?", "They are reasonable for tracking trends but can be off by 5–15% for individuals.")],
 sources=[KODAMA, ("Mandsager K, et al. Cardiorespiratory fitness and long-term mortality. JAMA Netw Open, 2018", pm("Mandsager 2018 cardiorespiratory fitness long-term mortality")),
          ("Uth N, et al. Estimation of VO2max from the ratio between HRmax and HRrest. Eur J Appl Physiol, 2004", pm("Uth 2004 estimation of VO2max ratio HRmax HRrest")), ("Cooper KH. A means of assessing maximal oxygen intake. JAMA, 1968", pm("Cooper 1968 means of assessing maximal oxygen intake"))],
 related=["heart-rate-zones", "pace", "steps"], guides=["vo2max-zone2"]),

dict(
 slug="one-rep-max", cat="fitness", name="One-rep max calculator", short="One-rep max", blurb="Estimate 1RM and training loads",
 title="One-Rep Max Calculator (Epley, Brzycki, Lombardi)",
 desc="Estimate your one-rep max from any set of 1–12 reps, then get a load table for every training percentage.",
 h1="One-rep max calculator",
 lede="Estimate the most you could lift once from a set you can already do, then plan training loads without testing a true max.",
 fields=[F("load", "load", "Weight lifted", ph="80"), F("reps", "num", "Reps completed", min=1, max=20, step=1, ph="5")],
 cta="Estimate 1RM",
 how="""<p>Three widely used formulas, averaged:</p>
<p class="formula">Epley: w × (1 + reps ÷ 30) &nbsp;|&nbsp; Brzycki: w × 36 ÷ (37 − reps) &nbsp;|&nbsp; Lombardi: w × reps^0.10</p>
<p>Each was fitted to lifters' data and works best between 2 and 10 reps taken close to failure with good form.</p>""",
 read="""<p>The table translates your estimated max into loads for common rep targets. For general strength and healthy ageing, two sessions a week of 2–3 sets at 60–80% of 1RM, stopping 1–3 reps short of failure, is effective and sustainable.</p>""",
 limits="""<p>Estimates drift above 10 reps and vary by exercise; machines and isolation lifts behave differently from squats and presses. Never test a true max without a spotter or safety arms.</p>""",
 faq=[("Which 1RM formula is most accurate?", "They agree closely at low reps. Averaging three reduces the error of any single one."),
      ("Should beginners test a one-rep max?", "No need. Estimate from a set of 5–8 instead; it is safer and nearly as useful."),
      ("How often should I re-estimate?", "Every 4–8 weeks, or whenever your working sets feel clearly easier.")],
 sources=[("Epley B. Poundage chart. Boyd Epley Workout, 1985", ""), ("Brzycki M. Strength testing: predicting a one-rep max from reps-to-fatigue. JOPERD, 1993", ""),
          ("Momma H, et al. Muscle-strengthening activities and mortality: a meta-analysis. Br J Sports Med, 2022", pm("Momma 2022 muscle-strengthening activities mortality meta-analysis"))],
 related=["protein", "calories-burned", "body-fat"], guides=["strength-training"]),

dict(
 slug="pace", cat="fitness", name="Running pace calculator", short="Pace calculator", blurb="Pace, speed and race-time predictions",
 title="Running Pace Calculator with Race Time Predictions",
 desc="Work out your pace per km and per mile, your speed, and predicted 5K, 10K, half marathon and marathon times with the Riegel formula.",
 h1="Running pace calculator",
 lede="Enter a distance and time to get your pace and speed, plus predictions for the classic race distances.",
 fields=[F("preset", "select", "Distance", options=[("5", "5K"), ("10", "10K"), ("21.0975", "Half marathon"), ("42.195", "Marathon"), ("custom", "Custom distance")], default="5"),
         F("dist", "dist", "Custom distance", ph="8", ph_i="5", show="preset=custom"),
         F("hh", "num", "Hours", min=0, max=48, step=1, ph="0"), F("mm", "num", "Minutes", min=0, max=59, step=1, ph="28"), F("ss", "num", "Seconds", min=0, max=59, step=1, ph="30")],
 how="""<p>Pace is time divided by distance. Predictions use Pete Riegel's 1981 endurance model, which says time grows slightly faster than distance:</p>
<p class="formula">T₂ = T₁ × (D₂ ÷ D₁)^1.06</p>""",
 read="""<p>Use the highlighted row to sanity-check your goal. If your training rarely goes beyond 10 km, add 5–10% to the half-marathon and marathon predictions. Easy runs should feel conversational, usually 60–90 seconds per km slower than 10K race pace.</p>""",
 limits="""<p>Heat, hills, wind and fuelling all change real results. Predictions assume you have trained for the target distance.</p>""",
 faq=[("What is a good 5K time?", "Anything you can improve on. Recreational runners commonly finish between 25 and 40 minutes."),
      ("How accurate is the Riegel formula?", "Good from 5K to half marathon for trained runners; it tends to be optimistic for first marathons."),
      ("How do I convert pace per km to per mile?", "Multiply by 1.609. The calculator shows both.")],
 sources=[("Riegel PS. Athletic records and human endurance. American Scientist, 1981", ""), WHO_PA],
 related=["heart-rate-zones", "vo2max", "calories-burned"], guides=["vo2max-zone2"]),

dict(
 slug="steps", cat="fitness", name="Steps to distance & calories calculator", short="Steps calculator", blurb="Convert steps to distance, time and calories",
 title="Steps Calculator: Convert Steps to Miles, km and Calories",
 desc="Convert daily steps into distance, walking time and calories, and see how you compare with the 7,000-step evidence.",
 h1="Steps to distance & calories",
 lede="Turn your step count into kilometres or miles, minutes and calories, and see how close you are to the 7,000 steps linked to a longer life.",
 fields=[F("steps", "num", "Steps", ph="7500", min=1, step=1), SEX, HEIGHT, F("weight", "weight", "Weight", opt=True),
         F("pace", "select", "Walking pace", options=[("casual", "Casual (about 3 mph / 4.8 km/h)"), ("brisk", "Brisk (about 3.5 mph / 5.6 km/h)"), ("fast", "Fast (about 4 mph / 6.4 km/h)")], default="brisk")],
 how="""<p>Stride length is estimated from height: about 41.5% of height for men and 41.3% for women. Distance = steps × stride. Time comes from your chosen pace, and calories from the walking MET value for that pace:</p>
<p class="formula">kcal = MET × 3.5 × weight (kg) ÷ 200 × minutes</p>""",
 read="""<p>A 2025 Lancet Public Health meta-analysis of 57 studies found that, compared with 2,000 steps a day, about 7,000 steps was linked to 47% lower risk of death from any cause, 25% lower cardiovascular disease and 38% lower dementia risk. Benefits kept rising toward 10,000 for some outcomes but flattened for others. Even moving from 2,000 to 4,000 steps helped.</p>""",
 limits="""<p>Stride estimates can be 10% off; measure 10 strides on a track to personalise. Phone step counts undercount when the phone is in a bag.</p>""",
 faq=[("How many steps a day do I need?", "About 7,000 captures most of the benefit for most adults. If you are below 4,000, add 1,000 a day each week."),
      ("How many steps is a mile?", "About 2,000–2,500 for most adults, depending on height and pace."),
      ("Do steps count as exercise?", "Brisk walking is moderate activity and counts toward the 150 minutes a week WHO recommends.")],
 sources=[DING, COMPENDIUM, WHO_PA],
 related=["calories-burned", "heart-rate-zones", "calories"], guides=["walking-steps"]),

dict(
 slug="calories-burned", cat="fitness", name="Calories burned calculator", short="Calories burned", blurb="Calories for 25+ activities by MET",
 title="Calories Burned Calculator for Walking, Running, Cycling & More",
 desc="Estimate calories burned for more than 25 activities using MET values from the Compendium of Physical Activities, your weight and duration.",
 h1="Calories burned calculator",
 lede="Estimate the energy you use in walking, running, cycling, swimming, strength training, sport and everyday chores.",
 fields=[WEIGHT, F("activity", "select", "Activity", default="4.3", wide=True, options=[
    ("3.0", "Walking, slow (2.5 mph / 4 km/h)"), ("3.5", "Walking, moderate (3 mph / 4.8 km/h)"), ("4.3", "Walking, brisk (3.5 mph / 5.6 km/h)"), ("5.0", "Walking, very brisk (4 mph / 6.4 km/h)"),
    ("6.0", "Hiking"), ("4.0", "Climbing stairs, slow"), ("8.3", "Running, 5 mph (8 km/h)"), ("9.8", "Running, 6 mph (9.7 km/h)"), ("11.0", "Running, 7 mph (11.3 km/h)"),
    ("11.8", "Running, 8 mph (12.9 km/h)"), ("6.8", "Cycling, leisure (10–12 mph)"), ("8.0", "Cycling, moderate (12–14 mph)"), ("7.0", "Stationary bike, moderate"),
    ("5.8", "Swimming laps, moderate"), ("9.8", "Swimming laps, vigorous"), ("7.0", "Rowing machine, moderate"), ("5.0", "Elliptical, moderate"),
    ("3.5", "Strength training, moderate"), ("6.0", "Strength training, vigorous"), ("8.0", "Circuit training / HIIT"), ("2.5", "Yoga (hatha)"), ("3.0", "Pilates"),
    ("7.3", "Dance fitness"), ("8.0", "Tennis, singles"), ("8.0", "Basketball, game"), ("7.0", "Soccer, casual"), ("11.8", "Jump rope, moderate"), ("3.8", "Gardening"), ("3.5", "House cleaning")]),
         F("minutes", "num", "Duration", ph="30", unit="min", min=1)],
 how="""<p>A MET (metabolic equivalent) is a multiple of resting energy use. Sitting quietly is 1 MET; brisk walking is about 4.3. The Compendium of Physical Activities lists measured MET values for hundreds of activities.</p>
<p class="formula">kcal per minute = MET × 3.5 × weight (kg) ÷ 200</p>""",
 read="""<p>The headline is gross calories, which includes what you would burn at rest anyway. The “above resting” figure subtracts that and is the fairer number if you are matching exercise against food. Activities at 3–5.9 METs count as moderate and 6 or more as vigorous in physical activity guidelines.</p>""",
 limits="""<p>MET values are averages for adults. Fitness level, technique, terrain and heat can change your real burn by 20% or more. Fitness trackers have similar error ranges.</p>""",
 faq=[("Should I eat back the calories I burn?", "Partly, if you are training hard or losing weight fast. Many people overestimate exercise calories, so start with about half."),
      ("What burns the most calories?", "Sustained vigorous activities like running, rowing and fast cycling. The best choice is the one you will do consistently."),
      ("Does strength training burn many calories?", "Fewer during the session than cardio, but it builds muscle that supports metabolic health and healthy ageing.")],
 sources=[COMPENDIUM, ("Ainsworth BE, et al. Compendium of Physical Activities: second update of codes and MET values. Med Sci Sports Exerc, 2011", pm("Ainsworth 2011 compendium of physical activities second update")), WHO_PA],
 related=["steps", "calories", "heart-rate-zones"], guides=["walking-steps", "vo2max-zone2"]),
]
