import os

DIST_DIR = "./dist"

landing_pages = {
    "solar": "Luxury Solar Tinting Services - Palm Springs & Joshua Tree",
    "baby": "Premium Organic Baby Clothing & Essentials",
    "lawatches": "Curated Luxury Timepieces & Custom Watches"
}

print("🔨 Starting cloud building engine...")

# This builds your actual directory folders and pages
for folder, title in landing_pages.items():
    folder_path = os.path.join(DIST_DIR, folder)
    os.makedirs(folder_path, exist_ok=True)
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: sans-serif; padding: 50px; text-align: center; background: #0f0f10; color: white; }}
        h1 {{ color: #61dafb; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p>Building something incredible ~!</p>
    <p>Served directly via HTTP Cloud Server.</p>
</body>
</html>"""
    
    with open(os.path.join(folder_path, "index.html"), "w") as f:
        f.write(html_content)
    print(f"✅ Created folder and page layout for: /{folder}")
