import sqlite3
import random

db_path = 'bpoms.sqlite'

industries = ["Retail & E-commerce", "Software / SaaS", "Healthcare", "Finance", "Travel & Hospitality", "Logistics", "EdTech", "Real Estate"]
project_types = ["Support Expansion", "Service Migration", "Holiday Surge Coverage", "Process Optimization", "Digital Transformation", "CX Strategy"]
skills_list = ["Customer Support", "Technical Triage", "Financial Reconciliation", "Lead Generation", "Data Processing"]

templates = [
    "Thrilled to share that we've successfully completed a major {project_type} initiative for our {industry} partner. We achieved an outstanding {csat}/5 CSAT score and delivered the full scope in just {days} days. Exceptional effort by our dedicated delivery team! #BPO #Success #ClientExperience",
    "Efficiency at scale: Just wrapped up a {project_type} optimization task. We were able to reduce average handling time by {aht}% while maintaining a {sla}% SLA compliance rate. A truly rewarding experience collaborating with such a forward-thinking client! #Operations #BPOResults #Efficiency",
    "Milestone achieved! 🚀 Our team has officially managed over {volume} customer interactions for our newest {industry} account with a first-contact resolution rate of {fcr}%. Proud of the empathy and technical skill our specialists continue to display every day. #CustomerSuccess #BPOExperts",
    "Case Study Update: We recently implemented a dedicated {skills} unit for an international {industry} conglomerate. The transition was seamless, completed in {days} days, and has already resulted in a {nps} point increase in Net Promoter Score. Looking forward to continued growth! #StrategicPartnership #BPOCommunity",
    "We recently partnered with a leading {industry} firm to scale their {skills} operations. The project was a massive success, exceeding all KPIs within the first {days} days. It's an honor to work with clients who value top-tier operational excellence. #GlobalPartners #BPO #Scale",
    "Reflecting on a successful Q1: We've successfully onboarded {volume}+ new users for our {industry} client, maintaining a quality score of {sla}% throughout the peak period. Our team's commitment to {skills} is second to none! #TeamSuccess #QuarterlyReview"
]

def update_posts():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute('SELECT id FROM feed_posts')
    post_ids = [row[0] for row in cur.fetchall()]

    print(f"Updating {len(post_ids)} posts with detailed LinkedIn-style content...")

    for pid in post_ids:
        template = random.choice(templates)
        content = template.format(
            industry=random.choice(industries),
            project_type=random.choice(project_types),
            skills=random.choice(skills_list),
            csat=round(random.uniform(4.2, 5.0), 1),
            days=random.randint(15, 60),
            aht=random.randint(10, 35),
            sla=random.randint(95, 100),
            volume=random.randint(1000, 50000),
            fcr=random.randint(85, 98),
            nps=random.randint(15, 45)
        )
        
        cur.execute('UPDATE feed_posts SET content = ? WHERE id = ?', (content, pid))

    conn.commit()
    conn.close()
    print("All posts updated with detailed, professional content.")

if __name__ == "__main__":
    update_posts()
