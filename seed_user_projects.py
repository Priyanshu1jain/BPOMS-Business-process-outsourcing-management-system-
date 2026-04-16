from app import create_app, db
from app.models import User, Project, ProjectTask, Review, Client
import json
import random
from datetime import datetime, timezone, timedelta

def seed_projects_for_user():
    app = create_app()
    with app.app_context():
        # Find the specific user 'Elite Ops 0'
        user = User.query.filter_by(name='Elite Ops 0').first()
        if not user:
            print("User 'Elite Ops 0' not found.")
            return

        print(f"Adding projects for user: {user.name}")

        # Find a client to associate with
        client_user = User.query.join(User.role).filter_by(name='client').first()
        if not client_user:
            print("No client found in database.")
            return

        # Add 3 projects
        project_data = [
            {"title": "Global Logistics Support", "industry": "Logistics", "desc": "International shipping coordination and customer support."},
            {"title": "Prime Tech Integration", "industry": "Software / SaaS", "desc": "Technical helpdesk and API migration assistance."},
            {"title": "Quantum FinTech Audit", "industry": "Finance", "desc": "Quarterly financial records reconciliation and compliance check."}
        ]

        for data in project_data:
            status = random.choice(['In Progress', 'Completed'])
            progress = 100 if status == 'Completed' else random.randint(30, 85)
            
            history = []
            now = datetime.now(timezone.utc)
            steps = random.randint(4, 7)
            for s in range(steps):
                p_val = int((s+1) * (progress/steps))
                date = now - timedelta(days=(steps-s)*3)
                history.append({"date": date.isoformat(), "progress": p_val})

            p = Project(
                client_id=client_user.id,
                agent_id=user.id,
                title=data['title'],
                description=data['desc'],
                status=status,
                timeline="3 Months",
                start_date=(now - timedelta(days=60)).strftime('%Y-%m-%d'),
                progress=progress,
                progress_history=json.dumps(history)
            )
            db.session.add(p)
            db.session.flush()

            # Add some tasks
            tasks = ["Infrastructure Setup", "Core Training", "Live Operations", "Efficiency Audit"]
            for i_t, t_name in enumerate(tasks):
                is_done = (progress > (i_t * 25))
                db.session.add(ProjectTask(project_id=p.id, name=t_name, is_completed=is_done))

            if status == 'Completed':
                db.session.add(Review(reviewer_id=client_user.id, reviewee_id=user.id, project_id=p.id, rating=5, comment="Exceptional work on the logistics project!"))

        db.session.commit()
        print("Success: Added 3 projects to 'Elite Ops 0'")

if __name__ == "__main__":
    seed_projects_for_user()
