"""
Populates the current_affairs table with sample data so the feed isn't
empty while you build the UI. This is placeholder content for development —
replace with the real ingestion pipeline (Phase 1.2) once it's ready.

Run with:  python -m app.seed   (from inside backend/)
"""

from datetime import date, timedelta

from .database import Base, SessionLocal, engine
from .models import CurrentAffair, Category, Importance

TODAY = date.today()

SAMPLE_DATA = [
    {
        "headline": "RBI's Monetary Policy Committee Holds Repo Rate Steady",
        "summary": (
            "The MPC kept the repo rate unchanged, balancing inflation control against "
            "growth support. Useful for questions on monetary policy tools, MPC composition, "
            "and the RBI's inflation-targeting mandate."
        ),
        "source_name": "RBI Press Release",
        "source_url": "https://www.rbi.org.in",
        "published_date": TODAY,
        "category": Category.ECONOMY,
        "exam_tags": ["UPSC", "Banking", "State PSC"],
        "importance": Importance.HIGH,
    },
    {
        "headline": "Parliament Passes Amendment to Strengthen Data Protection Board",
        "summary": (
            "The amendment expands the Data Protection Board's powers to levy penalties "
            "and handle cross-border data complaints. Ties into the DPDP Act, 2023 and the "
            "broader digital governance framework."
        ),
        "source_name": "PRS Legislative Research",
        "source_url": "https://prsindia.org",
        "published_date": TODAY,
        "category": Category.POLITY_GOVERNANCE,
        "exam_tags": ["UPSC", "SSC", "State PSC"],
        "importance": Importance.HIGH,
    },
    {
        "headline": "India, Australia Sign MoU on Critical Minerals Supply Chain",
        "summary": (
            "The agreement aims to secure lithium and cobalt supply for India's battery and "
            "EV manufacturing sector. Relevant for questions on critical mineral security and "
            "India's bilateral partnerships in the Indo-Pacific."
        ),
        "source_name": "Ministry of External Affairs",
        "source_url": "https://mea.gov.in",
        "published_date": TODAY - timedelta(days=1),
        "category": Category.INTERNATIONAL_RELATIONS,
        "exam_tags": ["UPSC"],
        "importance": Importance.MEDIUM,
    },
    {
        "headline": "ISRO Successfully Tests Reusable Launch Vehicle Landing",
        "summary": (
            "The test demonstrated autonomous landing capability, a key step toward "
            "lowering launch costs. Connects to India's space policy goals and ISRO's "
            "roadmap for reusable rocket technology."
        ),
        "source_name": "ISRO",
        "source_url": "https://isro.gov.in",
        "published_date": TODAY - timedelta(days=1),
        "category": Category.SCIENCE_TECH,
        "exam_tags": ["UPSC", "SSC"],
        "importance": Importance.HIGH,
    },
    {
        "headline": "New Ramsar Sites Added, Boosting India's Wetland Count",
        "summary": (
            "Three new wetlands received Ramsar designation for their biodiversity value. "
            "Useful for questions on wetland conservation, the Ramsar Convention, and India's "
            "total tally of internationally recognized wetlands."
        ),
        "source_name": "Ministry of Environment, Forest and Climate Change",
        "source_url": "https://moef.gov.in",
        "published_date": TODAY - timedelta(days=2),
        "category": Category.ENVIRONMENT_ECOLOGY,
        "exam_tags": ["UPSC", "State PSC"],
        "importance": Importance.MEDIUM,
    },
    {
        "headline": "Government Expands PM Awas Yojana Rural Housing Targets",
        "summary": (
            "The scheme's rural component now targets additional housing units, with revised "
            "cost-sharing between the Centre and States. Relevant for questions on flagship "
            "housing and rural welfare schemes."
        ),
        "source_name": "Ministry of Rural Development",
        "source_url": "https://rural.gov.in",
        "published_date": TODAY - timedelta(days=2),
        "category": Category.SCHEMES_POLICIES,
        "exam_tags": ["UPSC", "SSC", "Banking"],
        "importance": Importance.MEDIUM,
    },
    {
        "headline": "India Climbs in Global Innovation Index Rankings",
        "summary": (
            "The improved ranking is attributed to growth in patent filings and R&D "
            "investment. A recurring exam topic — useful to track year-on-year rank changes "
            "alongside the Ease of Doing Business and Human Development Index."
        ),
        "source_name": "World Intellectual Property Organization",
        "source_url": "https://www.wipo.int",
        "published_date": TODAY - timedelta(days=3),
        "category": Category.REPORTS_INDICES,
        "exam_tags": ["UPSC", "State PSC"],
        "importance": Importance.MEDIUM,
    },
    {
        "headline": "National Security Advisor Holds Talks on Regional Maritime Security",
        "summary": (
            "Discussions focused on coordinated patrolling and information-sharing in the "
            "Indian Ocean Region. Relevant to India's maritime strategy and defence "
            "diplomacy questions."
        ),
        "source_name": "Press Information Bureau",
        "source_url": "https://pib.gov.in",
        "published_date": TODAY - timedelta(days=3),
        "category": Category.DEFENCE_SECURITY,
        "exam_tags": ["UPSC"],
        "importance": Importance.MEDIUM,
    },
    {
        "headline": "Veteran Para-Athlete Honoured with Highest Sporting Award",
        "summary": (
            "The award recognizes a career of multiple Paralympic medals. Awards-and-honours "
            "questions frequently test the current recipient list alongside past winners."
        ),
        "source_name": "Ministry of Youth Affairs and Sports",
        "source_url": "https://yas.gov.in",
        "published_date": TODAY - timedelta(days=4),
        "category": Category.AWARDS_HONOURS,
        "exam_tags": ["UPSC", "SSC", "Railways"],
        "importance": Importance.LOW,
    },
    {
        "headline": "India Wins Continental Team Championship in Badminton",
        "summary": (
            "The team title is India's first in the tournament's history, led by strong "
            "performances in mixed doubles. Sports current affairs are a staple of SSC and "
            "Railways prelims."
        ),
        "source_name": "Badminton Association of India",
        "source_url": "https://www.badmintonindia.org",
        "published_date": TODAY - timedelta(days=4),
        "category": Category.SPORTS,
        "exam_tags": ["SSC", "Railways"],
        "importance": Importance.LOW,
    },
    {
        "headline": "New Governor Appointed for North-Eastern State",
        "summary": (
            "The appointment follows the usual constitutional process under Article 155. "
            "'Person in News' items like this are commonly tested alongside the appointee's "
            "prior role and the state's political context."
        ),
        "source_name": "Rashtrapati Bhavan",
        "source_url": "https://presidentofindia.nic.in",
        "published_date": TODAY - timedelta(days=5),
        "category": Category.PERSON_IN_NEWS,
        "exam_tags": ["UPSC", "State PSC"],
        "importance": Importance.LOW,
    },
    {
        "headline": "Ancient Trade Route Site Gets UNESCO Tentative List Status",
        "summary": (
            "The site is now under consideration for full World Heritage inscription. "
            "'Place in News' items often pair with the site's historical period and "
            "associated dynasty or event."
        ),
        "source_name": "Archaeological Survey of India",
        "source_url": "https://asi.nic.in",
        "published_date": TODAY - timedelta(days=5),
        "category": Category.PLACE_IN_NEWS,
        "exam_tags": ["UPSC"],
        "importance": Importance.LOW,
    },
]


def run() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(CurrentAffair).count() > 0:
            print("current_affairs already has data — skipping seed.")
            return
        for entry in SAMPLE_DATA:
            db.add(CurrentAffair(**entry))
        db.commit()
        print(f"Seeded {len(SAMPLE_DATA)} sample current affairs items.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
