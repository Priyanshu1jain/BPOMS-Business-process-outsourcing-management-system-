import sqlite3
import re

db_path = 'bpoms.sqlite'

image_map = {
    'Travel': 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?q=80&w=800&auto=format&fit=crop',
    'Software': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=800&auto=format&fit=crop',
    'Tech': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=800&auto=format&fit=crop',
    'API': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=800&auto=format&fit=crop',
    'Healthcare': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?q=80&w=800&auto=format&fit=crop',
    'Health': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?q=80&w=800&auto=format&fit=crop',
    'Finance': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=800&auto=format&fit=crop',
    'FinTech': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=800&auto=format&fit=crop',
    'Analytics': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=800&auto=format&fit=crop',
    'Data': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=800&auto=format&fit=crop',
    'Support': 'https://images.unsplash.com/photo-1534536281715-e28d76689b4d?q=80&w=800&auto=format&fit=crop',
    'Sales': 'https://images.unsplash.com/photo-1534536281715-e28d76689b4d?q=80&w=800&auto=format&fit=crop',
    'Live Chat': 'https://images.unsplash.com/photo-1534536281715-e28d76689b4d?q=80&w=800&auto=format&fit=crop',
    'Refunds': 'https://images.unsplash.com/photo-1534536281715-e28d76689b4d?q=80&w=800&auto=format&fit=crop',
    'Project Management': 'https://images.unsplash.com/photo-1531403009284-440f080d1e12?q=80&w=800&auto=format&fit=crop'
}

default_image = 'https://images.unsplash.com/photo-1521791136064-7986c2920216?q=80&w=800&auto=format&fit=crop'

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute('SELECT id, content FROM feed_posts')
posts = cur.fetchall()

print(f"Updating {len(posts)} posts with diverse images...")

for post_id, content in posts:
    # Use Picsum with post_id as seed for guaranteed variety
    assigned_url = f"https://picsum.photos/seed/post_{post_id}/800/400"
    cur.execute('UPDATE feed_posts SET image_url = ? WHERE id = ?', (assigned_url, post_id))

conn.commit()
conn.close()
print("Images updated with 100% diversity across all posts.")
