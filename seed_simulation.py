import random
import json
from datetime import datetime, timezone, timedelta
from app import create_app, db
from app.models import Role, User, Client, Project, ProjectTask, Review, FeedPost, Notification, HireRequest

def generate_dicebear_logo(seed, style="shapes"):
    return f"https://api.dicebear.com/8.x/{style}/svg?seed={seed.replace(' ', '%20')}"

def seed_db():
    app = create_app()
    with app.app_context():
        # Clean Database completely
        db.drop_all()
        db.create_all()

        # Re-Add Roles
        admin_role = Role(name='admin')
        manager_role = Role(name='manager')
        agent_role = Role(name='agent')
        client_role = Role(name='client')
        db.session.add_all([admin_role, manager_role, agent_role, client_role])
        db.session.commit()

        # Add default users (admin)
        admin = User(name='Admin', email='admin@bpoms.com', role=admin_role, profile_image_url=generate_dicebear_logo("Admin", "initials"))
        admin.set_password('admin123')
        db.session.add(admin)

        # Generate 50 Realistic Businesses (Clients)
        industries = ["Retail & E-commerce", "Software / SaaS", "Healthcare", "Finance", "Travel & Hospitality", "Logistics", "EdTech", "Real Estate"]
        company_prefixes = ["Global", "Apex", "Nova", "Tech", "Prime", "Quantum", "Synergy", "Oasis", "NextGen", "Alpha"]
        company_suffixes = ["Corp", "LLC", "Solutions", "Dynamics", "Enterprises", "Partners", "Group", "Network"]

        clients = []
        for i in range(50):
            comp_name = f"{random.choice(company_prefixes)} {random.choice(company_suffixes)} {i}"
            ind = random.choice(industries)
            u = User(
                name=f"Admin {comp_name}", 
                email=f"client{i+1}@bpoms.com", 
                role=client_role,
                profile_image_url=generate_dicebear_logo(comp_name, "identicon")
            )
            u.set_password('client123')
            db.session.add(u)
            db.session.flush()

            c = Client(user_id=u.id, company_name=comp_name, industry=ind, description=f"A leading company in the {ind} industry.", sla_details="Standard 24h SLA")
            db.session.add(c)
            clients.append(u)

        # Generate 50 Service Providers (BPO Vendors)
        bpo_prefixes = ["Connect", "Resolve", "Service", "CX", "Frontline", "Trust", "Elite", "Agile", "Rapid", "Pro"]
        bpo_suffixes = ["BPO", "Support", "Outsourcing", "Ops", "Hub", "Network", "Experts", "Partners"]
        skills_pool = [
            "Customer Service, Dispute Resolution", 
            "Tech Support, API Integration", 
            "Healthcare Billing, Empathy", 
            "Sales, Calling, Lead Gen", 
            "Travel Booking, Customer Retention", 
            "Refunds, Inbound Tech", 
            "E-commerce Support, Live Chat", 
            "Project Management, Admin", 
            "Onboarding, KYC Verification", 
            "Level 1 Support, Triage"
        ]

        agents = []
        for i in range(50):
            vendor_name = f"{random.choice(bpo_prefixes)} {random.choice(bpo_suffixes)} {i}"
            skills = random.choice(skills_pool)
            u = User(
                name=vendor_name, 
                email=f"vendor{i+1}@bpoms.com", 
                role=agent_role, 
                skills=skills, 
                profile_description=f"Specializing in {skills}. Delivering excellence globally.",
                profile_image_url=generate_dicebear_logo(vendor_name, "shapes")
            )
            u.set_password('agent123')
            db.session.add(u)
            agents.append(u)

        db.session.commit()

        # Generating 150 Projects
        print("Generating Projects...")
        projects = []
        statuses = ['Pending', 'Accepted', 'In Progress', 'Completed', 'Rejected']

        for i in range(150):
            client = random.choice(clients)
            agent = random.choice(agents)
            status = random.choices(statuses, weights=[10, 10, 30, 40, 10])[0]

            timeline = f"Week {random.randint(1,4)} to Week {random.randint(5,12)}"
            
            hq = HireRequest(client_id=client.id, agent_id=agent.id, work_description=f"Requesting {agent.skills} services.", status='Approved' if status in ['Accepted', 'In Progress', 'Completed'] else status)
            db.session.add(hq)

            if status in ['Accepted', 'In Progress', 'Completed']:
                progress = 100 if status == 'Completed' else random.randint(10, 80)
                if status == 'Accepted': progress = 0
                
                client_obj = Client.query.filter_by(user_id=client.id).first()
                if not client_obj: continue

                # Generate realistic progress history
                history = []
                now = datetime.now(timezone.utc)
                if progress > 0:
                    steps = random.randint(3, 8)
                    for s in range(steps):
                        p_val = int((s + 1) * (progress / steps))
                        # Spread points over the last 30 days
                        point_date = now - timedelta(days=(steps - s) * random.randint(2, 4))
                        history.append({
                            "date": point_date.isoformat(),
                            "progress": p_val
                        })
                
                p = Project(
                    client_id=client.id, 
                    agent_id=agent.id,
                    title=f"{client_obj.company_name} - {random.choice(['Support Expansion', 'Service Migration', 'Holiday Surge Coverage', 'Process Optimization'])}",
                    description=f"Handle tasks for {client_obj.industry} with focus on {agent.skills}.",
                    status=status,
                    timeline=timeline,
                    progress=progress,
                    progress_history=json.dumps(history)
                )
                db.session.add(p)
                db.session.flush()

                task_names = ["Onboarding", "Infrastructure Setup", "Live Operations", "QA Review", "Final Handoff"]
                for i_t, t_name in enumerate(task_names):
                    is_done = False
                    if status == 'Completed': is_done = True
                    elif status == 'In Progress' and i_t < 2: is_done = True
                    db.session.add(ProjectTask(project_id=p.id, name=t_name, is_completed=is_done))
            
                if status == 'Completed':
                    db.session.add(Review(reviewer_id=client.id, reviewee_id=agent.id, rating=random.randint(4,5), comment=f"Excellent delivery by {agent.name}!"))

        db.session.commit()

        # Generating 200 Feed Posts for the Recent Activity Feed
        print("Generating Feed Posts...")
        import urllib.parse
        image_keywords = ['technology', 'business', 'office', 'meeting', 'team', 'success', 'growth', 'analytics', 'marketing', 'support']

        for _ in range(200):
            a = random.choice(agents)
            post_date = datetime.now(timezone.utc) - timedelta(days=random.randint(0, 100), hours=random.randint(0, 24))
            gap = random.randint(0, 3)
            
            templates = [
                f"Thrilled to share that we've successfully completed a major {random.choice(['Support Expansion', 'Service Migration', 'Holiday Surge Coverage', 'Process Optimization'])} initiative for our {random.choice(industries)} partner. We achieved an outstanding {round(random.uniform(4.3, 5.0), 1)}/5 CSAT score and delivered the full scope in just {random.randint(15, 60)} days. Exceptional effort by our dedicated delivery team! #BPO #Success #ClientExperience",
                f"Efficiency at scale: Just wrapped up a process optimization task. We were able to reduce average handling time by {random.randint(10, 35)}% while maintaining a {random.randint(95, 100)}% SLA compliance rate. A truly rewarding experience collaborating with such a forward-thinking client! #Operations #BPOResults #Efficiency",
                f"Milestone achieved! \ud83d\ude80 Our team has officially managed over {random.randint(1000, 50000)} customer interactions for our newest {random.choice(industries)} account with a first-contact resolution rate of {random.randint(85, 98)}%. Proud of the empathy and technical skill our specialists continue to display every day. #CustomerSuccess #BPOExperts",
                f"Case Study Update: We recently implemented a dedicated support unit for an international {random.choice(industries)} conglomerate. The transition was seamless, completed in {random.randint(20, 45)} days, and has already resulted in a {random.randint(15, 45)} point increase in Net Promoter Score. Looking forward to continued growth! #StrategicPartnership #BPOCommunity",
                f"We recently partnered with a leading firm to scale their operations. The project was a massive success, exceeding all KPIs within the first {random.randint(10, 30)} days. It's an honor to work with clients who value top-tier operational excellence. #GlobalPartners #BPO #Scale"
            ]
            
            content = random.choice(templates)
            
            post = FeedPost(
                author_id=a.id, 
                content=content, 
                likes=random.randint(5, 500), 
                comments_count=random.randint(0, 50), 
                created_at=post_date,
                image_url=f"https://picsum.photos/seed/{random.randint(1, 10000)}/800/400" if random.random() > 0.6 else None
            )
            db.session.add(post)

        db.session.commit()
        print("✅ Large Scale Simulation Data Seeding complete!")

if __name__ == "__main__":
    seed_db()
