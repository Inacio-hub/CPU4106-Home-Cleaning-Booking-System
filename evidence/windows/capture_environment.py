"""Read-only environment/source/database evidence for this corrected release."""
import hashlib, json, platform, sqlite3, sys
from pathlib import Path
root = Path(__file__).resolve().parent
source = root.parents[1] / 'Home_Cleaning_Audit_Current' / 'Home_Cleaning_Project'
result = {'python': sys.version, 'interpreter': sys.executable,
          'windows': platform.platform(), 'sqlite': sqlite3.sqlite_version,
          'source_folder': str(source),
          'source_sha256': {name: hashlib.sha256((source/name).read_bytes()).hexdigest()
                            for name in ['app.py','index.html','schema.sql','test_app.py','test_week4.py','test_audit.py']}}
database = root / 'audit_fictional_fresh.db'
if database.exists():
    db = sqlite3.connect(f'file:{database.as_posix()}?mode=ro', uri=True)
    try:
        db.row_factory = sqlite3.Row
        result['integrity_check'] = db.execute('PRAGMA integrity_check').fetchone()[0]
        result['foreign_key_check'] = [list(r) for r in db.execute('PRAGMA foreign_key_check')]
        result['bookings'] = [dict(r) for r in db.execute('SELECT * FROM Bookings ORDER BY booking_id')]
    finally:
        db.close()
(root/'environment_final.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
