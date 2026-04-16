import random
import uuid
from app import create_app, db
from app.models import Role, User, Client

def seed_data():
    app = create_app()
    with app.app_context():
        agent_role = Role.query.filter_by(name='agent').first()
        client_role = Role.query.filter_by(name='client').first()

        skills_pool = [
            "Inbound Tech Support", "Billing Disputes", "Account Recovery", 
            "API Integration", "Sales", "Outbound Calls", 
            "Customer Retention", "Refunds Processing", "Network Debugging"
        ]
        
        company_pool = ["Corp", "Inc", "LLC", "Enterprises", "Solutions", "Dynamics", "Global", "Technologies"]

        print("Generating 100 Agents...")
        for i in range(100):
            # Using uuid to ensure unique emails
            unique_id = uuid.uuid4().hex[:6]
            agent = User(
                name=f"Agent {unique_id}", 
                email=f"agent_{unique_id}@bpoms.com", 
                role=agent_role, 
                skills=f"{random.choice(skills_pool)}, {random.choice(skills_pool)}"
            )
            agent.set_password("agent123")
            db.session.add(agent)

        print("Generating 100 Clients...")
        for i in range(100):
            unique_id = uuid.uuid4().hex[:6]
            client_user = User(
                name=f"Client {unique_id}", 
                email=f"client_{unique_id}@bpoms.com", 
                role=client_role
            )
            client_user.set_password("client123")
            db.session.add(client_user)
            db.session.flush() # Get the new id
            
            client_company = Client(
                user_id=client_user.id, 
                company_name=f"Random {random.choice(company_pool)} {unique_id}", 
                sla_details="Standard 24h SLA"
            )
            db.session.add(client_company)

        print("Committing to database...")
        db.session.commit()
        print("✅ Data seeding complete!")

if __name__ == "__main__":
    seed_data()
