import sys
import os
from sqlalchemy.orm import Session

# Insert parent directory of 'scripts' to sys.path to resolve 'app' imports
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.lead import Lead
from app.models.lead_activity import LeadActivity
from app.models.enums import LeadStatus, ActivityType
from app.dependencies import SessionLocal, engine

# Realistic seed data
LEADS_SEED = [
    {
        "name": "Sofía Rodríguez",
        "email": "sofia.rodriguez@tecnosoluciones.com",
        "company": "TecnoSoluciones S.A.",
        "phone": "+54 11 5555-1234",
        "status": LeadStatus.NEW.value,
        "activities": [
            {"type": ActivityType.NOTE.value, "notes": "Ingresó solicitud a través del formulario de contacto web."}
        ]
    },
    {
        "name": "Carlos Mendoza",
        "email": "carlos.mendoza@logisticaexpress.com",
        "company": "Logística Express",
        "phone": "+34 91 555-5678",
        "status": LeadStatus.NEW.value,
        "activities": [
            {"type": ActivityType.NOTE.value, "notes": "Lead derivado del partner comercial de distribución regional."}
        ]
    },
    {
        "name": "Lucía Fernández",
        "email": "lucia.f@alimentosdelsur.cl",
        "company": "Alimentos del Sur",
        "phone": "+56 2 2555-9876",
        "status": LeadStatus.NEW.value,
        "activities": []
    },
    {
        "name": "Diego Gómez",
        "email": "dgomez@constructoranorte.co",
        "company": "Constructora del Norte",
        "phone": "+57 1 555-4321",
        "status": LeadStatus.CONTACTED.value,
        "activities": [
            {"type": ActivityType.EMAIL.value, "notes": "Enviado correo de presentación con brochure de servicios corporativos."},
            {"type": ActivityType.CALL.value, "notes": "Llamada telefónica de seguimiento. Coordinada reunión para el próximo martes."}
        ]
    },
    {
        "name": "Mariana Silva",
        "email": "msilva@inversionesglobales.com",
        "company": "Inversiones Globales",
        "phone": "+55 11 5555-8888",
        "status": LeadStatus.CONTACTED.value,
        "activities": [
            {"type": ActivityType.CALL.value, "notes": "Llamada de prospección inicial. Solicita cotización detallada de planes corporativos."},
            {"type": ActivityType.EMAIL.value, "notes": "Enviada propuesta comercial técnica de servicios solicitados."}
        ]
    },
    {
        "name": "Alejandro Ruiz",
        "email": "aruiz@retailcommerce.mx",
        "company": "Retail & Commerce",
        "phone": "+52 55 5555-7777",
        "status": LeadStatus.CONTACTED.value,
        "activities": [
            {"type": ActivityType.NOTE.value, "notes": "Reunión virtual de alineación completada con el gerente de compras."}
        ]
    },
    {
        "name": "Camila Ortega",
        "email": "camila.ortega@sistemasmedicos.com.ar",
        "company": "Sistemas Médicos",
        "phone": "+54 351 555-9999",
        "status": LeadStatus.QUALIFIED.value,
        "activities": [
            {"type": ActivityType.NOTE.value, "notes": "Registro de requisitos completado. El cliente cumple con el presupuesto y perfil técnico."},
            {"type": ActivityType.EMAIL.value, "notes": "Enviado borrador del contrato de servicio para revisión legal."},
            {"type": ActivityType.CALL.value, "notes": "Llamada corta confirmando recepción de contrato. Conversaron sobre cláusulas de soporte."}
        ]
    },
    {
        "name": "Santiago Herrera",
        "email": "sherrera@bancadigital.com",
        "company": "BancaDigital S.A.",
        "phone": "+34 93 555-4433",
        "status": LeadStatus.QUALIFIED.value,
        "activities": [
            {"type": ActivityType.NOTE.value, "notes": "Demo técnica de la plataforma completada exitosamente con el equipo de TI."},
            {"type": ActivityType.CALL.value, "notes": "Llamada de cierre con el CTO. Aprobó la arquitectura y dio luz verde para avanzar."}
        ]
    },
    {
        "name": "Valeria Castro",
        "email": "vcastro@textilamericana.pe",
        "company": "Textil Americana",
        "phone": "+51 1 555-2211",
        "status": LeadStatus.LOST.value,
        "activities": [
            {"type": ActivityType.CALL.value, "notes": "Llamada de seguimiento. El cliente indica que pospondrá el proyecto para el próximo año."},
            {"type": ActivityType.NOTE.value, "notes": "Oportunidad perdida por presupuesto congelado. Cerrado sin éxito."}
        ]
    },
    {
        "name": "Martín Pineda",
        "email": "mpineda@agroindustriaseje.com",
        "company": "AgroIndustrias del Eje",
        "phone": "+57 6 555-9900",
        "status": LeadStatus.LOST.value,
        "activities": [
            {"type": ActivityType.EMAIL.value, "notes": "Propuesta comercial inicial enviada."},
            {"type": ActivityType.CALL.value, "notes": "Llamada de seguimiento. Optaron por desarrollar una solución interna a medida."},
            {"type": ActivityType.NOTE.value, "notes": "Cerrado. Pérdida frente a desarrollo in-house."}
        ]
    }
]

def seed_db(db: Session) -> None:
    """
    Idempotent function that seeds the database with Leads and activities.
    Checks if a Lead already exists by email before inserting.
    """
    print("Starting database seeding...")
    leads_inserted = 0
    activities_inserted = 0
    
    for lead_data in LEADS_SEED:
        # Check uniqueness by email
        existing_lead = db.query(Lead).filter(Lead.email == lead_data["email"]).first()
        if existing_lead:
            print(f"Skipping lead '{lead_data['name']}' (Email '{lead_data['email']}' already registered).")
            continue
            
        # Create Lead
        new_lead = Lead(
            name=lead_data["name"],
            email=lead_data["email"],
            company=lead_data["company"],
            phone=lead_data["phone"],
            status=lead_data["status"]
        )
        db.add(new_lead)
        db.flush()  # Obtain lead.id
        leads_inserted += 1
        
        # Create associated activities
        for act_data in lead_data["activities"]:
            new_activity = LeadActivity(
                lead_id=new_lead.id,
                type=act_data["type"],
                notes=act_data["notes"]
            )
            db.add(new_activity)
            activities_inserted += 1
            
    db.commit()
    print(f"Seeding completed successfully: {leads_inserted} leads and {activities_inserted} activities registered.")

if __name__ == "__main__":
    db_session = SessionLocal()
    try:
        seed_db(db_session)
    except Exception as e:
        db_session.rollback()
        print(f"Seeding error occurred: {str(e)}")
        sys.exit(1)
    finally:
        db_session.close()
