from .database import SessionLocal
from .models import Service


def main():
    db=SessionLocal()
    try:
        services=db.query(Service).order_by(Service.id).all()
        official=sum(s.fee_status in {"VERIFIED","VERIFIED_OFFICIAL"} for s in services)
        demo=sum(s.fee_status=="DEMO_DATA" for s in services)
        print(f"SERVICES={len(services)} OFFICIAL={official} DEMO={demo}")
        assert len(services)==20
        assert official==2
        assert demo==18
        assert all((s.government_fee or 0)>0 for s in services)
        print("CHECK_OK")
    finally: db.close()

if __name__=="__main__": main()
