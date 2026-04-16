from app import create_app, db
from app.models import User, Client, Project, ProjectTask, HireRequest, Review
from datetime import datetime, timezone

def prep_dashboards():
    app = create_app()
    with app.app_context():
        vendor1 = User.query.filter_by(email='vendor1@bpoms.com').first()
        client1 = User.query.filter_by(email='client1@bpoms.com').first()
        
        if not vendor1 or not client1:
            print("Could not find vendor1 or client1")
            return

        client_comp = Client.query.filter_by(user_id=client1.id).first()

        # Connect them primarily with an in-progress project
        p = Project(
            client_id=client1.id, 
            agent_id=vendor1.id,
            title=f"{client_comp.company_name} - Priority Service Agreement",
            description=f"Exclusive dashboard population demo project. Focuses on {vendor1.skills}.",
            status='In Progress',
            timeline="Q2 to Q4",
            progress=55
        )
        db.session.add(p)
        db.session.flush()

        # Add tasks
        db.session.add(ProjectTask(project_id=p.id, name="Contract Signing & NDA", is_completed=True))
        db.session.add(ProjectTask(project_id=p.id, name="Platform Integration", is_completed=True))
        db.session.add(ProjectTask(project_id=p.id, name="Live Agent Deployment", is_completed=False))
        db.session.add(ProjectTask(project_id=p.id, name="Q3 Review", is_completed=False))

        # Completed project for review sake
        p2 = Project(
            client_id=client1.id, 
            agent_id=vendor1.id,
            title=f"Initial Audit & Consulting",
            description=f"Preliminary setup.",
            status='Completed',
            timeline="Last Month",
            progress=100
        )
        db.session.add(p2)
        db.session.flush()
        db.session.add(ProjectTask(project_id=p2.id, name="Audit Report Delivered", is_completed=True))
        db.session.add(Review(reviewer_id=client1.id, reviewee_id=vendor1.id, rating=5, comment="Exceptional onboarding support and rapid analytics setup. Highlight recommended!"))

        # Add a HireRequest to show pending pipeline
        h = HireRequest(client_id=client1.id, agent_id=vendor1.id, work_description="Request for an additional 50 seats next quarter.", status='Pending')
        db.session.add(h)

        # Ensure vendor1 has multiple other active projects 
        client2 = User.query.filter_by(email='client2@bpoms.com').first()
        if client2:
            p3 = Project(
                client_id=client2.id, agent_id=vendor1.id, title="Secondary Overflow Support", description="...", status="In Progress", timeline="TBD", progress=20
            )
            db.session.add(p3)

        db.session.commit()
        print("Dashboards populated for vendor1 and client1!")

if __name__ == '__main__':
    prep_dashboards()
