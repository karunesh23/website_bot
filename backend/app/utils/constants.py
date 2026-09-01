GREETING = "GREETING"
KNOWLEDGE = "KNOWLEDGE"

# Main routing
NEW_ENQUIRY = "NEW_ENQUIRY"
EXISTING_ENQUIRY = "EXISTING_ENQUIRY"

# Sub flows
FOLLOW_UP_TICKET = "FOLLOW_UP_TICKET"
RAISE_NEW_TICKET = "RAISE_NEW_TICKET"

TICKET_CREATED = "TICKET_CREATED"
LEAD_CREATED = "LEAD_CREATED"
CALLBACK_SCHEDULED = "CALLBACK_SCHEDULED"

OPEN = "OPEN"
CLOSED = "CLOSED"

# ITC India common service questions (shown as quick buttons)
ITC_SERVICE_QUESTIONS = [
    "What is electrical product testing?",
    "How do I get my product tested at ITC?",
    "What is IEC 60335 safety testing?",
    "What is EMC/EMI testing?",
    "What is IP (Ingress Protection) testing?",
    "What is Calibration and do you offer it?",
    "How long does testing usually take?",
    "What documents are needed for testing?",
]

# New enquiry service options
SERVICE_OPTIONS = [
    "Electrical Safety Testing",
    "EMC/EMI Testing",
    "Electro-Medical Equipment",
    "Photometry (LM-79/LM-80)",
    "Environmental / IP Testing",
    "Calibration Services",
    "Packaging Testing",
    "Software Testing",
    "Information Security",
]

# What each service includes (shown when the user clicks a service button)
SERVICE_INFO = {
    "Electrical Safety Testing": (
        "Safety testing of electrical & electronic products to confirm they are safe "
        "for household, commercial and industrial use.\n\n"
        "• **Standards covered**: IEC 60335, IEC 60947, IEC 61010, IS 302, IS 7872 "
        "and more\n"
        "• **Tests included**: insulation resistance, earthing/earth continuity, "
        "leakage current, dielectric strength, temperature rise, endurance, abnormal "
        "operation and glow-wire testing\n"
        "• **Products**: kitchen appliances, irons, washing machines, heaters, "
        "switchgear, power tools, electric fence energizers and more"
    ),
    "EMC/EMI Testing": (
        "Electromagnetic Compatibility (EMC) & Electro-Magnetic Interference (EMI) "
        "testing ensures your product neither disturbs others nor gets disturbed.\n\n"
        "• **Standards covered**: IEC 61000 series, CISPR 11/14/32\n"
        "• **Emissions tests**: conducted & radiated emissions\n"
        "• **Immunity tests**: ESD, surge, EFT/burst, RF field immunity, voltage "
        "dips & interruptions\n"
        "• **Products**: household appliances, lighting, industrial equipment, "
        "medical devices and more"
    ),
    "Electro-Medical Equipment": (
        "Testing & certification of medical electrical equipment for patient and "
        "operator safety.\n\n"
        "• **Standards covered**: IEC 60601-1 (safety), IEC 60601-1-2 (EMC), "
        "IEC 62304 (medical device software)\n"
        "• **Tests included**: electrical safety, EMC, protection against electric "
        "shock, temperature, mechanical & radiation safety\n"
        "• **Products**: patient monitors, ventilators, diagnostic equipment, "
        "robots & personal-care devices"
    ),
    "Photometry (LM-79/LM-80)": (
        "Photometric & lumen-maintenance testing of LED lighting products.\n\n"
        "• **Standards covered**: IES LM-79 (photometry), IES LM-80 (lumen "
        "depreciation)\n"
        "• **Measured parameters**: luminous flux, CCT (colour temperature), CRI, "
        "efficacy, input power, power factor, chromaticity\n"
        "• **Deliverables**: lifetime / lumen-maintenance projection for your LED "
        "fixtures and luminaires"
    ),
    "Environmental / IP Testing": (
        "Ingress Protection (IP) & environmental stress testing to prove your "
        "product survives real-world conditions.\n\n"
        "• **IP testing**: IEC 60529, ISO 20653 (IP ratings e.g. IP66, IP67, IP68)\n"
        "• **Environmental tests**: temperature, humidity, salt spray, sand & dust, "
        "solar radiation\n"
        "• **Mechanical/reliability**: vibration, shock, drop, thermal cycling "
        "per MIL-STD-810, IEC 60068, IEC 61373 and JSS/RDSO specifications"
    ),
    "Calibration Services": (
        "NABL-accredited calibration of test & measuring instruments with "
        "traceability to national/international standards.\n\n"
        "• **Parameters**: electrical, temperature, pressure, dimensional, "
        "humidity, mass and more\n"
        "• **Deliverables**: calibration certificates with uncertainty statements, "
        "ensuring compliance with ISO 9001 / ISO/IEC 17025 requirements"
    ),
    "Packaging Testing": (
        "Testing of packaging and transport packaging to ensure your product "
        "arrives safely.\n\n"
        "• **Standards covered**: ISTA 1A/1B/1C/1D, ISTA 2A/2B/2C, ASTM D999\n"
        "• **Tests included**: vibration, drop, compression & stacking, "
        "inclined-impact and climate conditioning tests"
    ),
    "Software Testing": (
        "Independent software testing & verification for quality and compliance.\n\n"
        "• **Functional & performance testing** of web/mobile/desktop applications\n"
        "• **Medical device software** per IEC 62304\n"
        "• **Embedded / IoT & drone software** testing\n"
        "• **Deliverables**: test reports, defect management and compliance "
        "documentation"
    ),
    "Information Security": (
        "Cybersecurity testing & assessment to protect your products and data.\n\n"
        "• **Penetration testing** & vulnerability assessment of applications and "
        "networks\n"
        "• **Security testing** of drones, IoT devices, connected products and "
        "information systems\n"
        "• **Deliverables**: security assessment reports with remediation guidance"
    ),
}

# Buttons shown after an enquiry is submitted (services + new/existing query)

CALLBACK_OPTIONS = [
    "As soon as possible",
    "Today (Afternoon)",
    "Tomorrow Morning",
    "Tomorrow Afternoon",
]

# Friendly onboarding messages (Eurocert/SOPHIA-style)
WELCOME_MSG = (
    "Hi! I am **Priya**, your AI Compliance Companion.\n\n"
    "Welcome to **ITC India** 👋\n\n"
    "Before we begin, may I know your **NAME** and your **EMAIL ADDRESS**? "
    "It will help me personalize our conversation and assist you more "
    "effectively. 😊"
)

INTRO_MSG = (
    "Welcome, **{name}**! 👋\n\n"
    "**ITC India Pvt Ltd** is an NABL-accredited electrical safety testing laboratory. "
    "We provide comprehensive testing services—including EMC, IP, Photometry, Medical Device "
    "testing, and many more—to ensure your products meet global compliance and safety standards.\n\n"
    "May I know are you a **New Customer** or an **Existing Customer**?\n"
    "I'll help you raise a **Service Ticket** for your query or make an informed decision about the right certification for your "
    "product.\n\n"
    "**Please select an option below, or simply type your query to get started.** 💬"
)

GREETING_OPTIONS = [
    "New Customer",
    "Existing Customer",
]

POST_SUBMIT_OPTIONS = SERVICE_OPTIONS + ["Request a Callback"]

POST_CALL_SCHEDULED_OPTIONS = (
    SERVICE_OPTIONS
)

SCHEDULE_CALL_MSG = (
    "Great choice! 📞 Our team has received your request and will call you "
    "at your preferred time on your registered number."
)

# Country dial codes with expected number of local digits (excluding the +xx code)
COUNTRY_DIAL_CODES = {
    "+91": {"name": "India", "min_digits": 10, "max_digits": 10},
    "+98": {"name": "Iran", "min_digits": 10, "max_digits": 10},
    "+971": {"name": "UAE", "min_digits": 9, "max_digits": 9},
    "+966": {"name": "Saudi Arabia", "min_digits": 9, "max_digits": 9},
    "+974": {"name": "Qatar", "min_digits": 8, "max_digits": 8},
    "+965": {"name": "Kuwait", "min_digits": 8, "max_digits": 8},
    "+92": {"name": "Pakistan", "min_digits": 10, "max_digits": 10},
    "+880": {"name": "Bangladesh", "min_digits": 10, "max_digits": 10},
    "+1": {"name": "USA / Canada", "min_digits": 10, "max_digits": 10},
    "+44": {"name": "United Kingdom", "min_digits": 9, "max_digits": 10},
    "+61": {"name": "Australia", "min_digits": 9, "max_digits": 9},
    "+90": {"name": "Turkey", "min_digits": 10, "max_digits": 10},
    "+20": {"name": "Egypt", "min_digits": 10, "max_digits": 10},
    "+86": {"name": "China", "min_digits": 11, "max_digits": 11},
    "+81": {"name": "Japan", "min_digits": 10, "max_digits": 10},
}