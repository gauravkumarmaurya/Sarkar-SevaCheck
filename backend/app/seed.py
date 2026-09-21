from .database import Base, SessionLocal, engine
from .models import Service, User

APUNI_SARKAR = "https://eservices.uk.gov.in/"
APUNI_MANUAL = "https://it.uk.gov.in/apuni-sarkar/"
VERIFIED_ON = "20-09-2026"


def S(department, name, description, documents, processing_days, fee, status="DEMO_DATA", source_url=APUNI_MANUAL, office="Relevant Uttarakhand office"):
    return dict(
        state="Uttarakhand", department=department, name=name, description=description,
        government_fee=fee, authorized_service_charge=0, other_allowed_charge=0,
        processing_days=processing_days, documents=documents,
        official_portal=APUNI_SARKAR, source_url=source_url,
        source_document="", fee_status=status,
        verified_on=VERIFIED_ON if status == "VERIFIED_OFFICIAL" else "",
        office_name=office,
    )


SERVICES = [
    S("Panchayati Raj / Local Administration", "Birth Certificate", "DEMO DATA: Synthetic hackathon test amount. Not an official government fee.", "Birth record/hospital record where applicable; parent identity/address documents.", "Demo processing time", 120, office="Registrar of Births and Deaths"),
    S("Revenue Department", "Caste Certificate", "Official Apuni Sarkar service record. Fee and timeline verified from the current official service page.", "Applicant photo; identity/address proof; land registry/Khatauni or residence-related document; Aadhaar; family register copy.", "Demo processing time", 120, status="DEMO_DATA", source_url=APUNI_MANUAL", office="Tehsildar / Revenue Office"),
    S("Revenue Department", "Character Certificate", "DEMO DATA: Synthetic hackathon test amount. Not an official government fee.", "Applicant photo; identity proof; address/residence proof; other applicable documents.", "Demo processing time", 100, office="Revenue / Police Authority"),
    S("Panchayati Raj / Local Administration", "Death Certificate", "DEMO DATA: Synthetic hackathon test amount. Not an official government fee.", "Death record/hospital record where applicable; applicant identity/address documents.", "Demo processing time", 120, office="Registrar of Births and Deaths"),
    S("Registration Department", "Document Registration / Deed Registration", "DEMO DATA: Synthetic hackathon test amount. Not an official government fee.", "Identity proof; deed/document; property-related documents where applicable.", "Demo processing time", 500, office="Sub-Registrar Office"),
    S("Revenue Department", "Domicile / Permanent Residence Certificate", "DEMO DATA: Synthetic hackathon test amount. Not an official government fee.", "Applicant photo; identity proof; residence proof; other required documents.", "Demo processing time", 100, office="Tehsil / Revenue Office"),
    S("Transport Department", "Driving Licence Related Service", "DEMO DATA: Synthetic hackathon test amount. Not an official government fee.", "Age proof; address proof; photographs; medical/document requirements as applicable.", "Demo processing time", 200, office="Regional Transport Office"),
    S("Revenue Department", "EWS Certificate", "DEMO DATA: Synthetic hackathon test amount. Not an official government fee.", "Applicant photo; identity proof; residence proof; income/assets related documents.", "Demo processing time", 100, office="Tehsil / Revenue Office"),
    S("Employment Department", "Employment Registration", "Official Apuni Sarkar employment registration service. Fee and timeline verified from the current official service page.", "Applicant photo; date-of-birth proof; Uttarakhand permanent residence certificate; highest qualification marksheet.", "3 Days", 40, status="VERIFIED_OFFICIAL", source_url="https://eservices.uk.gov.in/service/new-employment-registration", office="Employment Officer"),
    S("Revenue Department", "Income Certificate", "DEMO DATA: Synthetic hackathon test amount. Not an official government fee.", "Applicant photo; identity/address proof; required income-related documents.", "Demo processing time", 150, office="Tehsil / Revenue Office"),
    S("Revenue Department", "Khatauni / RoR Information", "DEMO DATA: Synthetic hackathon test amount. Not an official government fee.", "Land details; Khata/Khasra information; identity proof where required.", "Demo processing time", 80, office="Revenue Record Office"),
    S("Revenue Department", "Land / Revenue Record Copy", "DEMO DATA: Synthetic hackathon test amount. Not an official government fee.", "Identity proof; land/property details; Khatauni or related record information.", "Demo processing time", 100, office="Revenue Record Office"),
    S("Revenue Department", "Legal Heir / Family Register Related Service", "DEMO DATA: Synthetic hackathon test amount. Not an official government fee.", "Identity proof; family register related documents; death certificate where applicable.", "Demo processing time", 120, office="Tehsil / Revenue Office"),
    S("Urban Local Bodies", "Marriage Registration", "DEMO DATA: Synthetic hackathon test amount. Not an official government fee.", "Age proof; identity proof; address proof; photographs; marriage-related documents.", "Demo processing time", 250, office="Marriage Registrar / Local Authority"),
    S("Revenue Department", "Mutation / Land Record Service", "DEMO DATA: Synthetic hackathon test amount. Not an official government fee.", "Registered deed or inheritance documents; land records; identity proof.", "Demo processing time", 300, office="Tehsil / Revenue Office"),
    S("Urban Local Bodies", "Property Tax Related Service", "DEMO DATA: Synthetic hackathon test amount. Not an official government fee.", "Property details; ownership documents; previous tax information where applicable.", "Demo processing time", 200, office="Municipal / Local Body Office"),
    S("Social Welfare Department", "Scholarship / Welfare Application", "DEMO DATA: Synthetic hackathon test amount. Not an official government fee.", "Identity proof; bank details; category/income documents; educational documents.", "Demo processing time", 50, office="Social Welfare Department"),
    S("Revenue Department", "Solvency Certificate", "DEMO DATA: Synthetic hackathon test amount. Not an official government fee.", "Identity proof; residence proof; property/financial documents as applicable.", "Demo processing time", 200, office="Tehsil / Revenue Office"),
    S("Urban Local Bodies", "Trade Licence", "DEMO DATA: Synthetic hackathon test amount. Not an official government fee.", "Applicant/business identity documents; premises proof; business details.", "Demo processing time", 350, office="Municipal / Local Body Office"),
    S("Transport Department", "Vehicle Registration Related Service", "DEMO DATA: Synthetic hackathon test amount. Not an official government fee.", "Vehicle documents; insurance; identity/address proof; applicable forms.", "Demo processing time", 300, office="Regional Transport Office"),
]


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for mobile, name, admin in [
            ("9999999999", "Demo Admin", True),
            ("9876543210", "Demo Citizen", False),
        ]:
            user = db.query(User).filter(User.mobile == mobile).first()
            if not user:
                db.add(User(name=name, mobile=mobile, is_admin=admin))
            else:
                user.name = name
                user.is_admin = admin

        for payload in SERVICES:
            existing = db.query(Service).filter(Service.name == payload["name"]).first()
            if existing:
                for key, value in payload.items():
                    setattr(existing, key, value)
            else:
                db.add(Service(**payload))

        db.commit()

        print("=" * 60)
        print("SARKAR SEVACHECK - DEMO SEED COMPLETE")
        print("=" * 60)
        print(f"Total services: {len(SERVICES)}")
        print("Official verified: 2")
        print("Demo/Test data: 18")
        for item in SERVICES:
            print(f"{item['name']}: {item['fee_status']} -> â‚¹{item['government_fee']}")
        print("Demo Admin: 9999999999")
        print("Demo Citizen: 9876543210")
        print("All DEMO_DATA amounts are synthetic hackathon test values.")
        print("=" * 60)
    finally:
        db.close()


if __name__ == "__main__":
    main()

