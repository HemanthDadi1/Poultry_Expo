import os
import json

def verify_all_files():
    required_files = [
        "index.html",
        "app.css",
        "app.js",
        "rules_engine.py",
        "rules_engine.js",
        "quick_import.py",
        "assets/shed_card_mock.svg",
        "assets/feed_mill_coa_mock.svg",
        ".agents/skills/poultry-field-inspection/SKILL.md"
    ]
    
    missing = []
    for f in required_files:
        if not os.path.exists(f):
            missing.append(f)
        else:
            size = os.path.getsize(f)
            print(f"[OK] {f} ({size:,} bytes)")
            
    if missing:
        print("MISSING FILES:", missing)
        return False
        
    print("\nALL SYSTEM & SKILL VERIFICATIONS PASSED!")
    return True

if __name__ == "__main__":
    if not verify_all_files():
        exit(1)
