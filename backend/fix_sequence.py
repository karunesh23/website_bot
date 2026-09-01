import psycopg2

def fix_sequences():
    conn = psycopg2.connect("dbname=itc user=postgres password=password host=localhost")
    cur = conn.cursor()

    cur.execute("SELECT id FROM leads ORDER BY id")
    leads = cur.fetchall()

    mapping = {}
    current = 1
    for (old_id,) in leads:
        if old_id != current:
            mapping[old_id] = current
        current += 1

    if mapping:
        print(f"Found {len(mapping)} gaps in sequence. Fixing...")
        
        # Drop constraints
        cur.execute('ALTER TABLE callbacks DROP CONSTRAINT IF EXISTS callbacks_lead_id_fkey')
        cur.execute('ALTER TABLE escalations DROP CONSTRAINT IF EXISTS escalations_lead_id_fkey')
        cur.execute('ALTER TABLE tickets DROP CONSTRAINT IF EXISTS tickets_lead_id_fkey')
        
        for old_id, new_id in mapping.items():
            print(f"Mapping {old_id} -> {new_id}")
            cur.execute('UPDATE callbacks SET lead_id = %s WHERE lead_id = %s', (new_id, old_id))
            cur.execute('UPDATE escalations SET lead_id = %s WHERE lead_id = %s', (new_id, old_id))
            cur.execute('UPDATE tickets SET lead_id = %s WHERE lead_id = %s', (new_id, old_id))
            cur.execute('UPDATE leads SET id = %s WHERE id = %s', (new_id, old_id))
            
        # Re-add constraints
        cur.execute('ALTER TABLE callbacks ADD CONSTRAINT callbacks_lead_id_fkey FOREIGN KEY (lead_id) REFERENCES leads(id)')
        cur.execute('ALTER TABLE escalations ADD CONSTRAINT escalations_lead_id_fkey FOREIGN KEY (lead_id) REFERENCES leads(id)')
        cur.execute('ALTER TABLE tickets ADD CONSTRAINT tickets_lead_id_fkey FOREIGN KEY (lead_id) REFERENCES leads(id)')
        
        # Reset sequence
        cur.execute("SELECT setval('leads_id_seq', (SELECT MAX(id) FROM leads))")
        print("Sequence reset successfully.")
    else:
        print("No gaps found.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix_sequences()
