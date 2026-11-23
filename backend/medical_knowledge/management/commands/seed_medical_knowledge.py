import json
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from medical_knowledge.models import MedicalKnowledge

EXPANDED_KNOWLEDGE = [
    # ==========================================================
    # DOMAIN B: SKIN & DERMATOLOGY
    # ==========================================================
    {
        "topic": "Hyperhidrosis (Excessive Sweating)",
        "category": "Skin and Dermatology",
        "keywords": "hyperhidrosis, excessive sweating, sweat in hands, sweaty palms, sweaty feet, wet hands, palms wet, underarms sweating, diaphoresis, eccrine glands, dripping sweat, clammy hands, sweaty armpits, palmar hyperhidrosis, plantar hyperhidrosis, axillary hyperhidrosis",
        "description": "Hyperhidrosis is a medical condition characterized by abnormally excessive perspiration beyond what is needed to regulate body temperature. It most frequently impacts the palms of the hands (palmar hyperhidrosis), the soles of the feet (plantar hyperhidrosis), the underarms (axillary hyperhidrosis), or the face and scalp. It can be primary (idiopathic focal hyperhidrosis, often genetic) or secondary (caused by an underlying condition like thyroid overactivity, medication side effects, or hormonal fluctuations).",
        "symptoms": [
            "Excessive, visible sweating on palms, soles, or underarms during resting or cool conditions",
            "Clammy or consistently wet hands that interfere with gripping objects or writing",
            "Sweating that soaks through clothing repeatedly during the day",
            "Skin maceration, peeling, or fungal/bacterial skin irritation due to persistent dampness",
            "Social embarrassment, avoidance of handshakes, or anxiety regarding sweat marks"
        ],
        "causes": "Primary hyperhidrosis is caused by hyperactive sympathetic nervous signaling to eccrine sweat glands, often with a genetic predisposition. Triggers include emotional stress, anxiety, spicy foods, warm environments, and caffeine. Secondary hyperhidrosis can be caused by hyperthyroidism, diabetes, menopause, infection, or medications (such as certain antidepressants).",
        "prevention": "General Management & Relief Strategies:\n• Topical Clinical Antiperspirants: Aluminum chloride hexahydrate lotions/roll-ons applied to dry skin at bedtime.\n• Foot and Hand Hygiene: Wash with antibacterial soap daily, dry thoroughly, and apply absorbent powders.\n• Breathable Footwear & Fabrics: Wear natural fibers (cotton, bamboo, merino wool), moisture-wicking socks, and breathable leather or mesh shoes. Change socks twice daily if needed.\n• Medical Interventions (under dermatologist care): Iontophoresis (using water baths and weak electrical currents for hands/feet), botulinum toxin (Botox) injections to block sweat gland nerves, oral anticholinergic medications (e.g., glycopyrrolate), or miraDry microwave thermolysis for underarms.\n• Lifestyle Adjustments: Limit caffeine, alcohol, and spicy foods which stimulate sympathetic sweat triggers.",
        "when_to_seek_care": "Seek medical evaluation if sweating is accompanied by chest discomfort, sudden weight loss, fever, or night sweats (drenching sheets at night), or if it starts abruptly in adulthood. Consult a dermatologist if it interferes with daily tasks or causes skin breakdown.",
        "references": [
            {"source": "MedlinePlus", "title": "Hyperhidrosis", "url": "https://medlineplus.gov/ency/article/007259.htm"},
            {"source": "NHS UK", "title": "Excessive Sweating (Hyperhidrosis)", "url": "https://www.nhs.uk/conditions/excessive-sweating-hyperhidrosis/"},
            {"source": "American Academy of Dermatology", "title": "Hyperhidrosis Overview", "url": "https://www.aad.org/public/diseases/a-z/hyperhidrosis-overview"}
        ]
    },
    {
        "topic": "Acne Vulgaris and Breakouts",
        "category": "Skin and Dermatology",
        "keywords": "acne, pimples, zits, blackheads, whiteheads, cystic acne, breakouts, facial spots, comedones, clogged pores, sebum",
        "description": "Acne vulgaris is a chronic inflammatory skin condition that occurs when hair follicles become clogged with excess sebum (oil) and dead skin cells, leading to bacterial proliferation (Cutibacterium acnes) and inflammation.",
        "symptoms": [
            "Whiteheads (closed plugged pores) and blackheads (open plugged pores)",
            "Inflamed red papules and pus-filled pustules",
            "Deep, painful solid lumps beneath the skin (nodules or cystic lesions)",
            "Post-inflammatory hyperpigmentation or scarring"
        ],
        "causes": "Excess sebum production stimulated by androgens, accumulation of dead keratinocytes, bacterial colonisation, hormonal fluctuations (puberty, menstrual cycle, PCOS), high glycemic diets, and pore-clogging comedogenic cosmetic products.",
        "prevention": "Management & Care:\n• Gentle Cleansing: Wash with a mild, non-soap foaming cleanser twice daily; avoid harsh scrubbing.\n• Topical Ingredients: Over-the-counter benzoyl peroxide (antibacterial), salicylic acid (unclogs pores), and topical retinoids (adapalene) to promote cell turnover.\n• Non-Comedogenic Products: Use oil-free, non-comedogenic sunscreens, moisturizers, and cosmetics.\n• Avoid Popping or Picking: Squeezing lesions increases inflammation and permanent scarring risk.\n• Medical Consultation: Severe or cystic acne requires prescription topical/oral retinoids, antibiotics, or hormonal therapy from a dermatologist.",
        "when_to_seek_care": "Consult a dermatologist if over-the-counter treatments fail after 8–12 weeks, if acne causes deep painful cysts, or if lesions leave physical scarring or cause emotional distress.",
        "references": [
            {"source": "NHS UK", "title": "Acne", "url": "https://www.nhs.uk/conditions/acne/"},
            {"source": "MedlinePlus", "title": "Acne", "url": "https://medlineplus.gov/acne.html"}
        ]
    },
    {
        "topic": "Eczema (Atopic Dermatitis)",
        "category": "Skin and Dermatology",
        "keywords": "eczema, atopic dermatitis, itchy skin, dry skin, skin itching, skin allergy, rash, skin inflammation, dermatitis flare",
        "description": "Eczema, most commonly atopic dermatitis, is a chronic inflammatory condition resulting from an impaired skin barrier, leading to dry, intensely itchy, and irritated skin.",
        "symptoms": [
            "Intense itching (pruritus), often worsening at night",
            "Dry, cracked, sensitive, and leathery patches of skin",
            "Red to brownish-gray patches, commonly on flexural creases (elbows, behind knees, neck, wrists)",
            "Small raised bumps that may weep clear fluid and crust over when scratched"
        ],
        "causes": "Complex interplay of genetic barrier defects (filaggrin gene mutations), immune dysregulation, and environmental triggers such as harsh soaps, detergents, dry cold air, dust mites, stress, and wool fabrics.",
        "prevention": "Management & Self-Care:\n• Frequent Moisturization: Apply thick ceramide-rich creams or ointments within 3 minutes of bathing while skin is damp.\n• Short, Lukewarm Showers: Avoid hot water; use soap-free, fragrance-free cleansers.\n• Trigger Avoidance: Wear breathable cotton clothing; avoid fragranced laundry detergents.\n• Scratch Control: Keep fingernails trimmed; consider cool damp compresses for itch relief.\n• Medical Care: Prescription topical corticosteroids or calcineurin inhibitors during acute flares under medical guidance.",
        "when_to_seek_care": "Seek medical attention if skin becomes oozing with yellow crusting, intensely painful, or warm (signs of secondary bacterial infection), or if eczema disrupts sleep.",
        "references": [
            {"source": "NHS UK", "title": "Atopic Eczema", "url": "https://www.nhs.uk/conditions/atopic-eczema/"},
            {"source": "MedlinePlus", "title": "Eczema", "url": "https://medlineplus.gov/eczema.html"}
        ]
    },
    {
        "topic": "Psoriasis and Scaly Skin",
        "category": "Skin and Dermatology",
        "keywords": "psoriasis, scaly skin, plaque psoriasis, silvery scales, red plaques, elbow scales, scalp psoriasis, skin scaling",
        "description": "Psoriasis is a chronic autoimmune condition that speeds up the growth cycle of skin cells, causing them to build up rapidly on the surface and form thick, silvery scales and itchy, dry, red plaques.",
        "symptoms": [
            "Red patches of skin covered with thick, silvery scales",
            "Dry, cracked skin that may bleed",
            "Itching, burning, or soreness around plaques",
            "Pitted, thickened, or ridged fingernails and toenails",
            "Stiff, swollen joints (in psoriatic arthritis)"
        ],
        "causes": "Autoimmune T-cell hyperactivation targeting healthy skin tissue. Triggers include physical skin injury (Koebner phenomenon), emotional stress, smoking, heavy alcohol use, cold dry weather, and certain medications.",
        "prevention": "Care & Management:\n• Regular Emollients: Keep skin well hydrated with heavy ointments.\n• Sunlight Exposure: Controlled, short exposure to natural sunlight can improve plaques.\n• Avoid Triggers: Cease smoking, manage stress, and avoid skin trauma.\n• Medical Therapies: Topical vitamin D analogues, topical steroids, phototherapy, and systemic biologic agents prescribed by dermatologists.",
        "when_to_seek_care": "Consult a physician or dermatologist for formal diagnosis, if plaques cover significant body areas, or if accompanied by joint pain or morning stiffness.",
        "references": [
            {"source": "WHO", "title": "Global report on Psoriasis", "url": "https://www.who.int/publications/i/item/9789241565189"},
            {"source": "NHS UK", "title": "Psoriasis", "url": "https://www.nhs.uk/conditions/psoriasis/"}
        ]
    },
    {
        "topic": "Hair Fall and Alopecia",
        "category": "Skin and Dermatology",
        "keywords": "hair fall, hair loss, hair falling, alopecia, losing hair, thinning hair, bald spots, telogen effluvium, shedding hair",
        "description": "Hair fall involves excessive shedding or thinning of hair. While losing 50–100 hairs daily is normal, substantial loss can occur due to androgenetic alopecia, telogen effluvium, nutritional deficiencies, or hormonal shifts.",
        "symptoms": [
            "Gradual thinning on top of the head or widening part line",
            "Circular or patchy bald spots (alopecia areata)",
            "Sudden loosening of hair and handfuls coming out while brushing or washing",
            "Excessive hair accumulating on pillows, combs, and shower drains"
        ],
        "causes": "Genetics (male/female pattern baldness), acute emotional or physical stress (telogen effluvium), nutritional deficiencies (iron, ferritin, zinc, vitamin D, protein), thyroid disorders, PCOS, postpartum hormone drops, or tight hairstyles (traction alopecia).",
        "prevention": "Management:\n• Balanced Diet: Ensure adequate dietary protein, iron, zinc, and biotin.\n• Gentle Hair Care: Avoid tight ponytails, harsh chemical dyes, and excessive heat styling.\n• Blood Testing: Check Ferritin, CBC, Vitamin D, and TSH levels.\n• Clinical Treatments: Topical minoxidil, anti-androgen therapies, or dermatological treatments after professional diagnosis.",
        "when_to_seek_care": "Seek medical evaluation if hair loss is sudden, patchy, accompanied by scalp redness/itching/scaling, or occurs alongside unexpected weight changes or fatigue.",
        "references": [
            {"source": "MedlinePlus", "title": "Hair Loss", "url": "https://medlineplus.gov/hairloss.html"},
            {"source": "NHS UK", "title": "Hair loss", "url": "https://www.nhs.uk/conditions/hair-loss/"}
        ]
    },

    # ==========================================================
    # DOMAIN A: GENERAL MEDICINE & SYMPTOMS
    # ==========================================================
    {
        "topic": "Common Cold and Viral Cough",
        "category": "General Medicine",
        "keywords": "cold, common cold, cough, coughing, runny nose, sneezing, sore throat, stuffy nose, rhinovirus, chest congestion, phlegm, what can i take for cold, cold medicines, prevent cold",
        "description": "The common cold is a mild viral upper respiratory tract infection, most commonly caused by rhinoviruses. It causes inflammation of the mucous membranes lining the nose and throat, frequently accompanied by cough and mild malaise.",
        "symptoms": [
            "Runny, congested, or stuffy nose with clear or cloudy mucus",
            "Sneezing, watery eyes, and post-nasal drip",
            "Scratchy or sore throat, especially during the first 48 hours",
            "Dry hacking or mild chesty cough",
            "Low-grade fever (under 38°C / 100.4°F), mild headache, and fatigue"
        ],
        "causes": "Over 200 distinct viral strains, predominantly rhinoviruses, coronaviruses, respiratory syncytial virus (RSV), and adenoviruses, transmitted via airborne respiratory droplets or contaminated surfaces.",
        "prevention": "Safe Supportive Care & General Treatment Categories:\n• Hydration & Warm Liquids: Drink warm water, herbal teas with honey, and clear broths to thin secretions and soothe throat.\n• Honey: A natural demulcent (1-2 teaspoons for adults and children over 1 year) proven effective for nighttime cough.\n• Saline Nasal Sprays / Rinses: Flush mucus and ease nasal congestion safely without rebound effects.\n• General OTC Options (consult pharmacist): Paracetamol or ibuprofen for aches/fever; saline gargles for throat; decongestants (short-term use, avoid if hypertensive).\n• ⚠️ ANTIBIOTIC WARNING: Antibiotics DO NOT work against cold viruses. Taking them provides no benefit and causes harm.\n• Prevention: Wash hands frequently, avoid touching eyes and mouth, and sanitize shared surfaces.",
        "when_to_seek_care": "Seek prompt medical care if experiencing shortness of breath, chest pain, high fever over 39°C (102°F) lasting >3 days, coughing up blood, or symptoms worsening after initial improvement.",
        "references": [
            {"source": "CDC", "title": "Common Cold", "url": "https://www.cdc.gov/antibiotic-use/colds.html"},
            {"source": "NHS UK", "title": "Common cold", "url": "https://www.nhs.uk/conditions/common-cold/"}
        ]
    },
    {
        "topic": "Fever (Pyrexia)",
        "category": "General Medicine",
        "keywords": "fever, pyrexia, high temperature, feverish, chills, shivering, feeling hot, body temp, fevr",
        "description": "A fever is a temporary elevation in core body temperature, typically defined as 38.0°C (100.4°F) or above. It is an adaptive physiological defense mechanism orchestrated by the hypothalamus in response to infections or inflammatory signals.",
        "symptoms": [
            "Core body temperature measuring 38.0°C (100.4°F) or higher",
            "Chills, shivering, and shivering sensations as body temperature rises",
            "Sweating and flushing as body temperature breaks",
            "Generalized headache, muscle aches, and weakness",
            "Dehydration, dry mouth, and loss of appetite"
        ],
        "causes": "Viral infections (influenza, common cold, COVID-19), bacterial infections (strep throat, urinary tract infections), inflammatory illnesses, heat exhaustion, or post-vaccination immune responses.",
        "prevention": "Home Care & Management:\n• Hydration: Drink plenty of water, oral rehydration solutions, or clear broths.\n• Rest: Avoid physical exertion to conserve metabolic energy.\n• Comfortable Environment: Wear lightweight, breathable clothing; keep room temperature moderate; do not use ice-cold baths.\n• Antipyretics (educational info): Paracetamol or ibuprofen can be used according to package instructions to relieve discomfort. Never give aspirin to children or teenagers due to Reye's syndrome risk.",
        "when_to_seek_care": "Seek urgent medical attention if fever exceeds 39.4°C (103°F) in adults, lasts longer than 3 consecutive days, is accompanied by a stiff neck, confusion, shortness of breath, seizure, or in infants under 3 months with temperature ≥ 38.0°C.",
        "references": [
            {"source": "NHS UK", "title": "High temperature (fever) in adults", "url": "https://www.nhs.uk/conditions/fever-in-adults/"},
            {"source": "MedlinePlus", "title": "Fever", "url": "https://medlineplus.gov/fever.html"}
        ]
    },
    {
        "topic": "Headaches (Tension, Migraine, and Cluster)",
        "category": "General Medicine",
        "keywords": "headache, head pain, hedache, tension headache, migraine, cluster headache, head hurts, throbbing head, forehead pressure",
        "description": "Headaches are among the most common neurological complaints, categorized primarily into tension-type headaches (band-like dull ache), migraines (unilateral throbbing pain with sensory sensitivities), and cluster headaches (severe piercing periorbital pain).",
        "symptoms": [
            "Tension: Constant dull, aching pressure around forehead, temples, or back of the neck",
            "Migraine: Moderate-to-severe throbbing unilateral pain, nausea, sensitivity to light (photophobia) and sound (phonophobia)",
            "Visual disturbances (aura): Flickering lights or zigzag lines before migraine onset",
            "Muscle tenderness in shoulders, neck, and scalp"
        ],
        "causes": "Stress, muscular tension from poor posture, screen strain, dehydration, irregular sleep, caffeine withdrawal, hormonal shifts, and specific sensory or dietary triggers (aged cheese, artificial sweeteners).",
        "prevention": "Relief & Lifestyle Prevention:\n• Hydrate: Drink 1–2 tall glasses of water immediately upon symptom onset.\n• Rest in a Quiet, Dark Room: Reduce sensory stimuli during migraine flares.\n• Temperature Therapy: Apply a cool damp cloth or ice pack to forehead, or a warm compress to tight neck muscles.\n• Ergonomics: Position monitors at eye level and take 20-second breaks every 20 minutes.\n• Over-the-counter options: Paracetamol or NSAIDs taken early, under pharmacist guidance. Avoid overuse (>10 days/month) to prevent medication-overuse headaches.",
        "when_to_seek_care": "Seek EMERGENCY medical care for a 'thunderclap' headache (sudden explosive pain peaking in seconds), or headache accompanied by fever, stiff neck, confusion, weakness on one side, or speech difficulty.",
        "references": [
            {"source": "WHO", "title": "Headache disorders", "url": "https://www.who.int/news-room/fact-sheets/detail/headache-disorders"},
            {"source": "NHS UK", "title": "Headaches", "url": "https://www.nhs.uk/conditions/headaches/"}
        ]
    },
    {
        "topic": "Abdominal Pain and Stomach Ache",
        "category": "General Medicine",
        "keywords": "stomach pain, abdominal pain, tummy ache, belly hurts, stomach cramps, stomach burning after food, gut ache, cramps in stomach, stomac",
        "description": "Abdominal pain refers to discomfort or cramping anywhere between the ribs and the groin. It can originate from the stomach, intestines, liver, gallbladder, pancreas, or abdominal wall.",
        "symptoms": [
            "Dull ache, sharp spasm, or cramping sensation in abdominal area",
            "Bloating, excessive gas, or feelings of fullness after small meals",
            "Epigastric burning or heartburn",
            "Nausea, mild indigestion, or bowel habit fluctuations"
        ],
        "causes": "Indigestion (dyspepsia), trapped intestinal gas, mild gastritis, gastroesophageal reflux (GERD), food intolerances, viral gastroenteritis, constipation, or menstrual cramps.",
        "prevention": "Self-Care & Clarification Steps:\n• Clarify Details: Track whether pain is upper, lower, left, or right, and whether it worsens after eating spicy/acidic foods.\n• Gentle Hydration: Sip water or electrolyte liquids slowly.\n• Bland Diet (BRAT): Bananas, rice, applesauce, toast when feeling up to eating.\n• Avoid NSAIDs: Do not take ibuprofen, naproxen, or aspirin on an upset stomach as they irritate gastric mucosa.\n• Posture: Avoid lying flat immediately after eating.",
        "when_to_seek_care": "Seek EMERGENCY care if stomach pain is sudden and severe, radiates to shoulder/back, or is accompanied by vomiting blood, black tarry stools, high fever, or rigid/board-like abdomen.",
        "references": [
            {"source": "NHS UK", "title": "Stomach ache", "url": "https://www.nhs.uk/conditions/stomach-ache/"},
            {"source": "MedlinePlus", "title": "Abdominal pain", "url": "https://medlineplus.gov/ency/article/003120.htm"}
        ]
    },

    # ==========================================================
    # DOMAIN C: RESPIRATORY HEALTH
    # ==========================================================
    {
        "topic": "Asthma and Respiratory Allergies",
        "category": "Respiratory Health",
        "keywords": "asthma, wheezing, shortness of breath, asthma attack, tight chest, inhaler, bronchial spasm, breathing difficulty, bronchospasm, breathing problem",
        "description": "Asthma is a chronic inflammatory disorder of the airways that causes bronchial hyperresponsiveness, mucosal swelling, and excess mucus production, leading to recurrent episodes of wheezing, breathlessness, and chest tightness.",
        "symptoms": [
            "High-pitched musical whistling or wheezing sound when exhaling",
            "Shortness of breath and difficulty drawing full breaths",
            "Chest tightness or sensation of constriction",
            "Chronic cough that worsens at night, during exercise, or in cold air"
        ],
        "causes": "Genetic predisposition interacting with environmental triggers including airborne allergens (dust mites, pollen, pet dander), viral respiratory infections, cold air, exercise, air pollution, and stress.",
        "prevention": "Management Strategies:\n• Identify and Avoid Triggers: Use dust-mite covers, keep indoor humidity below 50%, avoid smoke.\n• Medication Adherence: Controller (inhaled corticosteroid) inhalers taken daily as prescribed by a physician to reduce inflammation; fast-acting bronchodilator (albuterol) inhalers for acute relief.\n• Asthma Action Plan: Understand personal peak flow metrics and dosage adjustments directed by a doctor.",
        "when_to_seek_care": "Seek EMERGENCY assistance immediately if rescue inhaler fails to provide relief, if speaking full sentences is impossible due to breathlessness, if chest and ribs pull inward deeply during breathing (retractions), or if lips/fingers turn blue.",
        "references": [
            {"source": "WHO", "title": "Asthma Fact Sheet", "url": "https://www.who.int/news-room/fact-sheets/detail/asthma"},
            {"source": "CDC", "title": "Asthma", "url": "https://www.cdc.gov/asthma/default.htm"}
        ]
    },
    {
        "topic": "Bronchitis (Acute and Chronic)",
        "category": "Respiratory Health",
        "keywords": "bronchitis, chest cold, bronchial inflammation, productive cough, yellow phlegm, deep cough, lung congestion",
        "description": "Bronchitis is an inflammation of the lining of the bronchial tubes, which carry air to and from your lungs. Acute bronchitis (chest cold) is usually viral and resolves in 2–3 weeks, while chronic bronchitis is a component of COPD typically linked to smoking.",
        "symptoms": [
            "Persistent cough producing clear, yellowish, or greenish mucus",
            "Chest soreness or constriction aggravated by deep coughing",
            "Mild fever, chills, and generalized fatigue",
            "Shortness of breath or mild wheezing"
        ],
        "causes": "Over 90% of acute bronchitis cases are viral (influenza, rhinovirus, RSV). Chronic bronchitis is caused by prolonged airway irritation, overwhelmingly cigarette smoke, chemical fumes, or heavy air pollution.",
        "prevention": "Care:\n• Rest and fluids to thin bronchial secretions.\n• Cool-mist humidifier or warm steam inhalation.\n• Avoid smoke and secondhand smoke entirely.\n• Note: Antibiotics are NOT indicated for acute viral bronchitis.",
        "when_to_seek_care": "Consult a doctor if cough lasts longer than 3 weeks, produces blood, prevents sleep, or is accompanied by high fever or breathlessness.",
        "references": [
            {"source": "MedlinePlus", "title": "Acute Bronchitis", "url": "https://medlineplus.gov/ency/article/001087.htm"},
            {"source": "NHS UK", "title": "Bronchitis", "url": "https://www.nhs.uk/conditions/bronchitis/"}
        ]
    },

    # ==========================================================
    # DOMAIN D: CARDIOVASCULAR HEALTH
    # ==========================================================
    {
        "topic": "Hypertension (High Blood Pressure)",
        "category": "Cardiovascular Health",
        "keywords": "hypertension, high blood pressure, high bp, systolic, diastolic, bp reading, cardiovascular, arterial pressure",
        "description": "Hypertension is a chronic medical condition where the arterial blood pressure is persistently elevated (systolic ≥ 130 mmHg or diastolic ≥ 80 mmHg). Known as the 'silent killer', it often produces no symptoms for years while silently damaging arteries, heart, brain, and kidneys.",
        "symptoms": [
            "Often completely asymptomatic in mild to moderate stages",
            "Occasional morning headaches or dull occipital pressure",
            "Shortness of breath during exertion",
            "Dizziness, visual changes, or nosebleeds (in severe spikes)"
        ],
        "causes": "High dietary sodium intake, lack of physical activity, obesity, chronic stress, genetics, alcohol intake, and aging.",
        "prevention": "Management Guidelines:\n• DASH Diet: High in vegetables, fruits, whole grains; low in sodium (<2,300 mg/day, ideally 1,500 mg).\n• Aerobic Movement: 150 minutes of moderate aerobic exercise (walking, swimming) weekly.\n• Weight Reduction: Losing 5–10% of excess body weight significantly lowers blood pressure.\n• Home Monitoring: Log readings at consistent morning and evening times.\n• Physician-directed antihypertensives (ACE inhibitors, ARBs, CCBs, diuretics) taken as prescribed.",
        "when_to_seek_care": "Seek EMERGENCY care for hypertensive crisis (readings > 180/120 mmHg) accompanied by chest pain, shortness of breath, blurry vision, or numbness/speech difficulty.",
        "references": [
            {"source": "WHO", "title": "Hypertension", "url": "https://www.who.int/news-room/fact-sheets/detail/hypertension"},
            {"source": "AHA", "title": "Understanding Blood Pressure Readings", "url": "https://www.heart.org/en/health-topics/high-blood-pressure"}
        ]
    },
    {
        "topic": "Cholesterol and Lipid Health",
        "category": "Cardiovascular Health",
        "keywords": "cholesterol, high cholesterol, ldl, hdl, triglycerides, hyperlipidemia, lipid panel, artery plaque, cardiovascular risk",
        "description": "Cholesterol is a waxy substance used to build cell membranes and hormones. However, elevated levels of low-density lipoprotein (LDL, 'bad' cholesterol) lead to arterial plaque accumulation (atherosclerosis), increasing heart attack and stroke risk.",
        "symptoms": [
            "Typically asymptomatic; detected via a fasting Lipid Profile blood test",
            "Rare physical signs in genetic familial hypercholesterolemia: xanthomas (fatty deposits on tendons/eyelids) or corneal arcus"
        ],
        "causes": "Diets high in saturated and trans fats, physical inactivity, obesity, smoking, genetics (familial hypercholesterolemia), and diabetes.",
        "prevention": "Lifestyle Steps:\n• Soluble Fiber: Consume oats, barley, beans, lentils, and apples to bind cholesterol in the gut.\n• Healthy Fats: Replace butter and trans fats with olive oil, avocados, and omega-3 rich fish (salmon, sardines).\n• Regular Exercise: Raises beneficial HDL cholesterol.\n• Medical Guidance: Statin therapy prescribed by a doctor for high cardiovascular risk scores.",
        "when_to_seek_care": "Get a lipid panel blood test every 4–6 years starting at age 20 (or more frequently if risk factors exist).",
        "references": [
            {"source": "CDC", "title": "Cholesterol", "url": "https://www.cdc.gov/cholesterol/index.htm"},
            {"source": "NHS UK", "title": "High cholesterol", "url": "https://www.nhs.uk/conditions/high-cholesterol/"}
        ]
    },

    # ==========================================================
    # DOMAIN E: ENDOCRINE & METABOLIC HEALTH
    # ==========================================================
    {
        "topic": "Type 2 Diabetes and Blood Sugar",
        "category": "Endocrine and Metabolic Health",
        "keywords": "diabetes, type 2 diabetes, high blood sugar, insulin resistance, hyperglycemia, hba1c, glucose, excessive thirst, frequent urination",
        "description": "Type 2 diabetes is a chronic metabolic disorder characterized by insulin resistance—where the body's cells do not respond effectively to insulin—resulting in elevated circulating blood glucose levels and progressive pancreatic beta-cell strain.",
        "symptoms": [
            "Increased thirst (polydipsia) and dry mouth",
            "Frequent urination (polyuria), particularly at night",
            "Persistent fatigue, weakness, and lack of energy",
            "Unexplained weight loss despite normal or increased appetite",
            "Slow-healing cuts, sores, and recurring infections",
            "Blurred vision and peripheral tingling/numbness in fingers or toes"
        ],
        "causes": "Insulin resistance driven by excess visceral adiposity, physical inactivity, genetic predisposition, poor dietary patterns, and aging.",
        "prevention": "Prevention & Management:\n• Low-Glycemic, High-Fiber Diet: Whole grains, legumes, non-starchy vegetables, and lean proteins; avoid sugary drinks.\n• Regular Physical Activity: Aerobic and resistance training improve cellular glucose uptake without requiring insulin.\n• Routine Lab Monitoring: Maintain HbA1c below target (typically < 7.0% under physician direction).\n• Physician Guidance: Follow prescribed oral medications (metformin, SGLT2i, GLP-1 RA) or insulin as directed.",
        "when_to_seek_care": "Seek urgent medical attention if experiencing symptoms of hyperosmolar hyperglycemic state (extreme thirst, confusion, blood sugar > 300 mg/dL) or hypoglycemia (shakiness, sweating, confusion from medication).",
        "references": [
            {"source": "WHO", "title": "Diabetes", "url": "https://www.who.int/news-room/fact-sheets/detail/diabetes"},
            {"source": "ADA", "title": "Standards of Care in Diabetes", "url": "https://diabetes.org/"}
        ]
    },
    {
        "topic": "Thyroid Disorders (Hypothyroidism and Hyperthyroidism)",
        "category": "Endocrine and Metabolic Health",
        "keywords": "thyroid, hypothyroidism, hyperthyroidism, tsh, underactive thyroid, overactive thyroid, goiter, sluggish metabolism, weight gain thyroid, thyroid nodules",
        "description": "The thyroid gland in the neck regulates bodily metabolism through hormones T3 and T4. In hypothyroidism (underactive), metabolism slows down, while in hyperthyroidism (overactive), metabolism accelerates excessively.",
        "symptoms": [
            "Hypothyroidism: Fatigue, unexplained weight gain, cold intolerance, dry skin, constipation, hair thinning, depression",
            "Hyperthyroidism: Rapid heartbeat, palpitations, unexpected weight loss, heat intolerance, tremor in hands, nervousness, diarrhea",
            "Swelling at the base of the neck (goiter) or difficulty swallowing"
        ],
        "causes": "Autoimmune conditions (Hashimoto's thyroiditis for hypothyroidism; Graves' disease for hyperthyroidism), iodine imbalances, thyroid surgery, or postpartum thyroiditis.",
        "prevention": "Management:\n• Testing: Check Thyroid Stimulating Hormone (TSH) and Free T4 via blood test.\n• Medical Treatment: Hypothyroidism is treated with daily synthetic levothyroxine taken on an empty stomach. Hyperthyroidism is treated with anti-thyroid drugs, radioactive iodine, or beta-blockers under endocrinologist care.\n• Nutrition: Ensure adequate dietary iodine (iodized salt) without taking excessive kelp/iodine megadoses.",
        "when_to_seek_care": "Consult a doctor for unexplained weight shifts, chronic lethargy, or heart palpitations, or if noticing a visible neck lump.",
        "references": [
            {"source": "MedlinePlus", "title": "Thyroid Diseases", "url": "https://medlineplus.gov/thyroiddiseases.html"},
            {"source": "NHS UK", "title": "Underactive thyroid (hypothyroidism)", "url": "https://www.nhs.uk/conditions/underactive-thyroid-hypothyroidism/"}
        ]
    },
    {
        "topic": "Polycystic Ovary Syndrome (PCOS)",
        "category": "Endocrine and Metabolic Health",
        "keywords": "pcos, polycystic ovary syndrome, irregular periods, missed periods, facial hair women, hirsutism, ovarian cysts, hormonal imbalance women",
        "description": "Polycystic Ovary Syndrome (PCOS) is a common hormonal disorder among women of reproductive age, characterized by irregular ovulatory cycles, elevated androgens (male hormones), and enlarged ovaries with small immature follicles.",
        "symptoms": [
            "Irregular, infrequent, prolonged, or absent menstrual cycles",
            "Excess facial and body hair growth (hirsutism) on chin, chest, or abdomen",
            "Severe adult acne and oily skin",
            "Male-pattern hair thinning on the scalp",
            "Weight gain and difficulty losing weight due to underlying insulin resistance"
        ],
        "causes": "Insulin resistance (excess insulin stimulates ovarian androgen production), low-grade chronic inflammation, and genetic factors.",
        "prevention": "Management:\n• Insulin-Sensitizing Nutrition: Low-glycemic, anti-inflammatory dietary pattern with abundant fiber and lean protein.\n• Regular Physical Activity: Helps muscles utilize glucose and reduces insulin levels.\n• Medical Care (consult gynecologist/endocrinologist): Combined hormonal contraceptives to regulate cycles, anti-androgens (spironolactone) for hair/acne, or metformin for insulin resistance.",
        "when_to_seek_care": "Consult a gynecologist or endocrinologist if periods are persistently irregular (fewer than 9 per year), or for difficulties conceiving.",
        "references": [
            {"source": "WHO", "title": "Polycystic ovary syndrome", "url": "https://www.who.int/news-room/fact-sheets/detail/polycystic-ovary-syndrome"},
            {"source": "NHS UK", "title": "Polycystic ovary syndrome (PCOS)", "url": "https://www.nhs.uk/conditions/polycystic-ovary-syndrome-pcos/"}
        ]
    },

    # ==========================================================
    # DOMAIN F: MENTAL HEALTH & SLEEP
    # ==========================================================
    {
        "topic": "Insomnia and Sleep Difficulties",
        "category": "Mental Health and Sleep",
        "keywords": "insomnia, sleep difficulty, cannot sleep, can't sleep, trouble sleeping, sleeplessness, not getting sleep, wake up at night, sleep hygiene, poor sleep, irregular sleep",
        "description": "Insomnia is a prevalent sleep disorder characterized by persistent difficulty initiating sleep, maintaining sleep throughout the night, or achieving restorative sleep, leading to daytime cognitive impairment and fatigue.",
        "symptoms": [
            "Lying awake for extended periods unable to fall asleep (>30 minutes)",
            "Frequent nocturnal awakenings and difficulty falling back asleep",
            "Waking up prematurely in the morning unrefreshed",
            "Daytime fatigue, irritability, brain fog, and concentration difficulties"
        ],
        "causes": "Evening blue light exposure from screens, late caffeine/alcohol intake, psychological stress, irregular bedtime schedules, ambient noise/heat, and underlying conditions like sleep apnea or restless legs.",
        "prevention": "Evidence-Based Sleep Hygiene:\n• Consistent Schedule: Sleep and rise at the exact same hour daily, including weekends.\n• 20-Minute Rule: If still awake after 20 minutes, move to a dim room and read calmly until sleepy; avoid lying in bed frustrated.\n• Dark & Cool Bedroom: Maintain a room temperature around 18–20°C (65–68°F) in complete darkness.\n• Caffeine Cutoff: Discontinue caffeine at least 6 hours before bedtime.\n• Screen Wind-Down: Disengage from phones, tablets, and computers 45–60 minutes before bed.",
        "when_to_seek_care": "Consult a physician or sleep specialist if sleeplessness lasts more than a month, severely disrupts daytime work, or is accompanied by loud snoring or gasping for air.",
        "references": [
            {"source": "CDC", "title": "Sleep and Sleep Disorders", "url": "https://www.cdc.gov/sleep/index.html"},
            {"source": "NHS UK", "title": "Insomnia", "url": "https://www.nhs.uk/conditions/insomnia/"}
        ]
    },
    {
        "topic": "Stress Management and Anxiety Awareness",
        "category": "Mental Health and Sleep",
        "keywords": "anxiety, stress, chronic stress, panic attack, worry, overwhelmed, nervous, mental burnout, cortisol, racing thoughts, emotional tension",
        "description": "Stress is the body's autonomic response to external pressures, while anxiety is a persistent internal state of apprehension, excessive worry, and physiological tension even in the absence of an immediate threat.",
        "symptoms": [
            "Persistent feeling of being on edge, restlessness, or irritability",
            "Physical symptoms: muscle tension, clenched jaw, racing heartbeat, shallow breathing",
            "Sleep disturbances and difficulty quietening racing thoughts",
            "Digestive upset, tension headaches, and chronic fatigue"
        ],
        "causes": "Work pressures, financial strains, major life transitions, social isolation, genetic vulnerability, and neurochemical imbalances.",
        "prevention": "Evidence-Based Stress Reduction:\n• Physiological Sigh Breathing: Two quick inhales through the nose followed by one long, slow exhale through the mouth activates parasympathetic recovery.\n• Daily Physical Exercise: 30 minutes of aerobic exercise metabolizes stress hormones.\n• Mindfulness & Cognitive Reframing: Practicing meditation and questioning catastrophic thoughts.\n• Professional Therapy: Cognitive Behavioral Therapy (CBT) under a licensed psychologist or counselor.",
        "when_to_seek_care": "Seek professional mental healthcare if anxiety disrupts daily work or relationships. In crisis or having thoughts of self-harm, call 988 (US/Canada) or 112 (Europe/India).",
        "references": [
            {"source": "WHO", "title": "Anxiety disorders", "url": "https://www.who.int/news-room/fact-sheets/detail/anxiety-disorders"},
            {"source": "NIMH", "title": "Anxiety Disorders", "url": "https://www.nimh.nih.gov/health/topics/anxiety-disorders"}
        ]
    },

    # ==========================================================
    # DOMAIN G: DIGESTIVE HEALTH
    # ==========================================================
    {
        "topic": "Digestive Health & Gastroesophageal Reflux (GERD)",
        "category": "Digestive Health",
        "keywords": "acid reflux, gerd, heartburn, gastritis, stomach burning after food, acid regurgitation, indigestion, dyspepsia, burning in stomach",
        "description": "GERD is a chronic digestive disease occurring when stomach acid and bile flow back into the esophagus, irritating the mucosal lining and causing uncomfortable burning sensations and indigestion.",
        "symptoms": [
            "Heartburn: Burning sensation in chest, typically behind breastbone after meals",
            "Acid regurgitation leaving a sour or bitter taste in throat or mouth",
            "Upper stomach burning or postprandial discomfort",
            "Difficulty swallowing (dysphagia), chronic dry cough, or morning hoarseness"
        ],
        "causes": "Weakness or inappropriate transient relaxation of the lower esophageal sphincter (LES), obesity, hiatal hernia, pregnancy, late-night meals, and dietary triggers (spicy, fatty, or tomato-based foods, chocolate, citrus, caffeine, alcohol).",
        "prevention": "Self-Care & Management:\n• Elevation: Elevate the head of the bed by 15 cm (6 inches) using bed risers (not just extra pillows).\n• Timing of Meals: Finish dinner at least 3 hours before lying down or going to sleep.\n• Portion Size: Eat smaller, more frequent meals rather than large heavy dinners.\n• Trigger Elimination: Avoid known personal food triggers and carbonated beverages.\n• Medication Classes (consult doctor/pharmacist): Antacids for quick short-term neutralization; H2-receptor antagonists or proton pump inhibitors (PPIs) for acid suppression.",
        "when_to_seek_care": "Seek medical review if symptoms occur more than twice weekly, if food feels stuck in throat, or if accompanied by unintended weight loss, vomiting blood, or black stools.",
        "references": [
            {"source": "NIH NIDDK", "title": "Acid Reflux (GER & GERD) in Adults", "url": "https://www.niddk.nih.gov/health-information/digestive-diseases/acid-reflux-ger-gerd-adults"},
            {"source": "NHS UK", "title": "Heartburn and acid reflux", "url": "https://www.nhs.uk/conditions/heartburn-and-acid-reflux/"}
        ]
    },

    # ==========================================================
    # DOMAIN H: NUTRITION & LIFESTYLE
    # ==========================================================
    {
        "topic": "Iron-Deficiency Anemia and Hemoglobin Health",
        "category": "Nutrition and Lifestyle",
        "keywords": "hemoglobin, haemoglobin, boost hemoglobin, low hb, iron deficiency, anemia, ferritin, red blood cells, iron rich foods, increase hemoglobin, low blood",
        "description": "Hemoglobin is an iron-rich protein in red blood cells that carries oxygen from the lungs to all body tissues. Iron deficiency is the most widespread nutritional disorder globally and the leading cause of anemia.",
        "symptoms": [
            "Persistent fatigue, weakness, and low physical stamina",
            "Pale skin, pale inner eyelids, and brittle nails (koilonychia)",
            "Cold intolerance, cold hands, and cold feet",
            "Shortness of breath and dizziness during mild exertion",
            "Unusual cravings for non-nutritive substances like ice (pica)"
        ],
        "causes": "Inadequate dietary iron intake, chronic blood loss (heavy menstrual periods, gastrointestinal bleeding), increased physiological demand (pregnancy), or malabsorption (celiac disease).",
        "prevention": "Nutritional Guidance:\n• Heme Iron (high absorption): Lean poultry, fish, eggs, and lean meats.\n• Non-Heme Iron (plant-based): Spinach, lentils, chickpeas, black beans, pumpkin seeds, tofu, and fortified cereals.\n• Vitamin C Synergy: Pair non-heme plant iron with Vitamin C (citrus, tomatoes, bell peppers, amla) to multiply iron absorption up to 300%.\n• Avoid Iron Blockers with Meals: Do not drink black tea or coffee within 1–2 hours of meals, as polyphenols and tannins inhibit iron uptake.\n• Testing: Request a Complete Blood Count (CBC) and Serum Ferritin test before starting high-dose iron supplements.",
        "when_to_seek_care": "Consult a healthcare provider for severe fatigue, persistent dizziness, or heart palpitations to confirm deficiency through laboratory blood panels.",
        "references": [
            {"source": "WHO", "title": "Anaemia in women and children", "url": "https://www.who.int/data/gho/data/themes/topics/anaemia_in_women_and_children"},
            {"source": "NIH ODS", "title": "Iron Dietary Supplement Fact Sheet", "url": "https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/"}
        ]
    },
    {
        "topic": "Balanced Nutrition and Dietary Guidelines",
        "category": "Nutrition and Lifestyle",
        "keywords": "balanced diet, healthy diet, nutrition, what to eat, healthy lifestyle, vitamins, minerals, fiber, eatwell plate, mediterranean diet, dash diet",
        "description": "A balanced diet provides all essential macro-nutrients (proteins, carbohydrates, healthy fats) and micronutrients (vitamins, minerals) necessary for cellular energy, immune defense, organ function, and disease prevention.",
        "symptoms": [
            "Poor nutrition signs: fatigue, impaired immunity, dry hair/skin, slow wound healing, digestive irregularities"
        ],
        "causes": "Diets dominated by ultra-processed foods, high refined sugars, trans fats, and inadequate vegetable/fiber consumption.",
        "prevention": "Key Principles:\n• The Half-Plate Rule: Fill half your meal plate with non-starchy vegetables and fruits.\n• Quarter-Plate Whole Grains: Brown rice, oats, quinoa, whole wheat.\n• Quarter-Plate Clean Protein: Fish, poultry, beans, lentils, tofu, eggs.\n• Dietary Fiber: Aim for 25–35 grams of prebiotic fiber daily to nurture gut microbiome diversity.\n• Hydration: Drink 2–3 liters of water daily, adjusting for activity level.",
        "when_to_seek_care": "Consult a registered dietitian or physician for specialized medical nutrition therapy (diabetes, kidney disease, celiac).",
        "references": [
            {"source": "WHO", "title": "Healthy diet", "url": "https://www.who.int/news-room/fact-sheets/detail/healthy-diet"},
            {"source": "NHS UK", "title": "The Eatwell Guide", "url": "https://www.nhs.uk/live-well/eat-well/food-guidelines-and-food-labels/the-eatwell-guide/"}
        ]
    },
    {
        "topic": "Dietary Protein and Daily Requirements",
        "category": "Nutrition and Lifestyle",
        "keywords": "protein, dietary protein, protein requirements, protein per day, lean protein, plant protein, muscle recovery, how much protein",
        "description": "Protein is made of amino acids essential for building and repairing muscles, synthesizing hormones and enzymes, and maintaining immune antibodies. Adequate daily protein is vital across all stages of life.",
        "symptoms": [
            "Signs of protein deficiency: muscle wasting, weakness, brittle hair and nails, persistent hunger, edema"
        ],
        "causes": "Inadequate total caloric or protein intake, restrictive eating patterns, or increased catabolic states.",
        "prevention": "Guidelines:\n• Recommended Intake: Sedentary adults need approx. 0.8 g per kg of body weight daily (e.g. ~56g for a 70kg person). Active individuals and older adults benefit from 1.2–1.6 g/kg daily.\n• Quality Protein Sources: Eggs, poultry, salmon, greek yogurt, cottage cheese, lentils, chickpeas, soybeans, edamame, and nuts.\n• Distribution: Distribute protein evenly across 3 meals (20–35g per meal) to optimize muscle protein synthesis.",
        "when_to_seek_care": "Individuals with chronic kidney disease must consult their nephrologist regarding protein targets, as high protein can increase renal workload.",
        "references": [
            {"source": "NIH ODS", "title": "Protein and Amino Acids", "url": "https://ods.od.nih.gov/"},
            {"source": "Harvard T.H. Chan", "title": "The Nutrition Source - Protein", "url": "https://www.hsph.harvard.edu/nutritionsource/what-should-you-eat/protein/"}
        ]
    },

    # ==========================================================
    # DOMAIN J: GENERAL MEDICAL EDUCATION
    # ==========================================================
    {
        "topic": "Differences Between Viruses and Bacteria",
        "category": "General Medical Education",
        "keywords": "difference between virus and bacteria, virus vs bacteria, antibiotics on viruses, bacterial infection, viral infection, bacteria and virus",
        "description": "Viruses and bacteria are fundamentally different microscopic pathogens. Bacteria are independent, living, single-celled organisms, while viruses are non-living packages of genetic material (DNA or RNA) enclosed in a protein coat that require a living host cell to replicate.",
        "symptoms": [
            "Both can cause fever, fatigue, inflammation, and coughing, making laboratory testing or clinical evaluation necessary to differentiate"
        ],
        "causes": "Infections caused by pathogenic bacterial strains (e.g. Streptococcus, E. coli) vs viral agents (e.g. Influenza, Rhinovirus, SARS-CoV-2).",
        "prevention": "Critical Distinctions & Management:\n• Bacteria: Living cells with cell walls and internal machinery. Treated with **Antibiotics** (which disrupt cell walls or bacterial protein synthesis).\n• Viruses: Non-living genetic strands that hijack host cells. **Antibiotics DO NOT kill viruses.** Taking antibiotics for viral colds or flu is completely ineffective and fuels antibiotic resistance.\n• Viral Treatment: Rest, fluids, symptom management, and in select cases, specific antiviral medications.\n• Prevention: Vaccines train the immune system against both; thorough handwashing prevents transmission of both.",
        "when_to_seek_care": "Consult a physician when experiencing high fever, difficulty breathing, stiff neck, or symptoms that fail to improve after 7–10 days, to determine whether a bacterial infection requiring prescription medication is present.",
        "references": [
            {"source": "CDC", "title": "Antibiotic Resistance - Viruses or Bacteria", "url": "https://www.cdc.gov/antibiotic-use/index.html"},
            {"source": "MedlinePlus", "title": "Bacterial vs. Viral Infections", "url": "https://medlineplus.gov/bacterialinfections.html"}
        ]
    },
    {
        "topic": "Basic First Aid and Emergency Preparedness",
        "category": "General Medical Education",
        "keywords": "first aid, emergency first aid, burn first aid, cut first aid, sprain first aid, choking first aid, nosebleed, fainting first aid",
        "description": "First aid encompasses immediate, temporary care provided to an ill or injured person before professional emergency medical assistance arrives.",
        "symptoms": [
            "Minor burns, bleeding wounds, sprains, choking episodes, epistaxis (nosebleed), or vasovagal syncope (fainting)"
        ],
        "causes": "Thermal burns, mechanical trauma, sports injuries, airway obstruction, or sudden blood pressure drops.",
        "prevention": "First Aid Protocols:\n• Minor Burns: Hold under cool running tap water for 10–20 minutes. Do NOT apply ice, butter, or toothpaste. Cover loosely with sterile dressing.\n• Bleeding Wounds: Apply direct firm pressure with a clean cloth or gauze for 5–10 minutes continuously. Elevate above heart level if on limb.\n• Sprains (R.I.C.E.): Rest, Ice (wrapped in towel, 15 min), Compression (elastic bandage), Elevation.\n• Choking (Conscious Adult): Perform 5 back blows followed by 5 abdominal thrusts (Heimlich maneuver).\n• Nosebleed: Sit upright and lean slightly FORWARD (do not tilt head back). Pinch the soft part of nose firmly for 10 minutes.\n• Fainting: Lay person flat on back and elevate legs 30 cm (12 inches) to restore cerebral blood flow.",
        "when_to_seek_care": "Call EMERGENCY services (911/999/112) immediately for deep gaping wounds, uncontrollable bleeding, third-degree burns, severe head trauma, or unresponsiveness.",
        "references": [
            {"source": "American Red Cross", "title": "First Aid Guidelines", "url": "https://www.redcross.org/take-a-class/first-aid"},
            {"source": "NHS UK", "title": "First aid", "url": "https://www.nhs.uk/conditions/first-aid/"}
        ]
    }
]

class Command(BaseCommand):
    help = "Seeds database with comprehensive, verified medical knowledge topics across all medical domains."

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for item in EXPANDED_KNOWLEDGE:
            slug = slugify(item['topic'])
            obj, created = MedicalKnowledge.objects.update_or_create(
                slug=slug,
                defaults={
                    'topic': item['topic'],
                    'category': item['category'],
                    'keywords': item['keywords'],
                    'description': item['description'],
                    'symptoms': item['symptoms'],
                    'causes': item['causes'],
                    'prevention': item['prevention'],
                    'when_to_seek_care': item['when_to_seek_care'],
                    'references': item['references']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created topic: {item['topic']}"))
            else:
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated topic: {item['topic']}"))

        total = MedicalKnowledge.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f"Successfully updated medical knowledge base! Created: {created_count}, Updated: {updated_count}, Total Records in DB: {total}"
        ))
