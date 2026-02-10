import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from .logger import log

class Updater:
    def __init__(self, new_file: str, existing_file: str):
        self.new_file = new_file
        self.existing_file = existing_file

    def sync(self, output_file: str):
        """
        Append new test cases to existing Markdown file
        Preserve history, append new rows with Created Date
        """
        log.info(f"🔄 Syncing: {self.new_file} -> {self.existing_file}")
        
        if not os.path.exists(self.existing_file):
            log.warning("Existing file not found. Synchronization skipped.")
            return

        try:
            # Read Existing
            with open(self.existing_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()

            # Read New (JSON)
            with open(self.new_file, 'r', encoding='utf-8') as f:
                new_data = json.load(f)
            
            new_cases = new_data.get('test_cases', []) if isinstance(new_data, dict) else new_data
            log.info(f"   -> Found {len(new_cases)} new test cases.")

            # Create Backup
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            input_dir = os.path.dirname(self.existing_file)
            backup_path = os.path.join(input_dir, f"backup_{timestamp}.md")
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(existing_content)
            log.info(f"   -> Backup created: {backup_path}")

            # Prepare New Rows
            today = datetime.now().strftime('%Y-%m-%d')
            new_rows = []
            
            # Simple check for duplicates by ID in existing content could be added here
            
            for tc in new_cases:
                # Format: | id | priority | title | steps | expected | status | notes | created |
                # Ensure fields exist
                t_id = tc.get('id', '')
                t_prio = tc.get('priority', '')
                t_title = tc.get('title', '').replace('|', '\|').replace('\n', ' ')
                
                # Flatten steps
                steps = tc.get('steps', [])
                if isinstance(steps, list): t_steps = " • ".join(steps)
                else: t_steps = str(steps).replace('\n', ' • ')
                t_steps = t_steps.replace('|', '\|')

                t_exp = tc.get('expected_result', '').replace('|', '\|').replace('\n', ' ')
                
                row = f"| {t_id} | {t_prio} | {t_title} | {t_steps} | {t_exp} | [ ] Pass / [ ] Fail / [ ] Skip / [ ] Blocked | | {today} |"
                new_rows.append(row)

            # Append
            if new_rows:
                updated_content = existing_content.strip() + '\n' + '\n'.join(new_rows) + '\n'
                with open(self.existing_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                log.info(f"✅ Sync Complete. Added {len(new_rows)} rows to {self.existing_file}")
            else:
                log.info("   -> No new rows to add.")

        except Exception as e:
            log.error(f"Sync failed: {e}")

if __name__ == "__main__":
    pass
