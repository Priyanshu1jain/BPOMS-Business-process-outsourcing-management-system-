from app import create_app, db
from app.models import Role, User, Client, Process, Ticket, Call, HireRequest

app = create_app()

def reset_database():
    with app.app_context():
        # Drop and recreate all tables
        db.drop_all()
        db.create_all()

        # 1. Create Roles
        roles_data = ['admin', 'manager', 'agent', 'client']
        roles = {}
        for role_name in roles_data:
            role = Role(name=role_name)
            db.session.add(role)
            roles[role_name] = role
        db.session.commit()

        # 2. Create Users
        admin_user = User(name="System Admin", email="admin@bpoms.com", role=roles['admin'])
        admin_user.set_password("admin123")

        manager_user = User(name="Operations Manager", email="manager@bpoms.com", role=roles['manager'])
        manager_user.set_password("manager123")

        agent_user_1 = User(name="Agent Smith", email="agent1@bpoms.com", role=roles['agent'], skills="Inbound Tech Support, API Integration")
        agent_user_1.set_password("agent123")

        agent_user_2 = User(name="Agent Neo", email="agent2@bpoms.com", role=roles['agent'], skills="Billing Disputes, Account Recovery")
        agent_user_2.set_password("agent123")

        client_user = User(name="Weyland Corp Contact", email="client@weyland.com", role=roles['client'])
        client_user.set_password("client123")

        db.session.add_all([admin_user, manager_user, agent_user_1, agent_user_2, client_user])
        db.session.commit()

        # 3. Create Clients
        client_company = Client(user_id=client_user.id, company_name="Weyland Corporation", sla_details="SLA: 24h resolution time. 99.9% uptime.")
        db.session.add(client_company)
        db.session.commit()

        # 4. Create Processes
        process_inbound = Process(client_id=client_company.id, name="Inbound Tech Support", description="Handling tech queries for Weyland products.")
        process_billing = Process(client_id=client_company.id, name="Billing Disputes", description="Handling billing issues.")
        db.session.add_all([process_inbound, process_billing])
        db.session.commit()

        # 5. Create Tickets
        tickets = [
            Ticket(title="Cannot access core systems", description="Getting a 500 error on the main dashboard.", status="Open", priority="High", process_id=process_inbound.id, assigned_to=agent_user_1.id),
            Ticket(title="Invoice overcharged", description="The last invoice shows 10 extra licenses.", status="In Progress", priority="Medium", process_id=process_billing.id, assigned_to=agent_user_2.id),
            Ticket(title="Password Reset Request", description="User lost their password.", status="Resolved", priority="Low", process_id=process_inbound.id, assigned_to=agent_user_1.id),
            Ticket(title="System crash during checkout", description="Platform crashes instantly.", status="Escalated", priority="High", process_id=process_inbound.id, assigned_to=agent_user_2.id),
            Ticket(title="Need help setting up account", description="Can't find the activation link.", status="Open", priority="Low", process_id=process_inbound.id, assigned_to=agent_user_1.id),
        ]
        db.session.add_all(tickets)
        db.session.commit()

        print("Database initialized with dummy data successfully!")

if __name__ == '__main__':
    reset_database()
