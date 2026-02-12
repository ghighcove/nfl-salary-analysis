import base64
from pathlib import Path
import re

def embed_table_images():
    """Convert table image URLs to embedded base64 data URIs"""

    # Read existing table images and convert to base64
    table_images = {}
    img_dir = Path('images/te_market_inefficiency')

    for img_path in sorted(img_dir.glob('table_*.png')):
        print(f"Encoding {img_path.name}...")
        with open(img_path, 'rb') as f:
            b64_data = base64.b64encode(f.read()).decode('utf-8')
            data_uri = f"data:image/png;base64,{b64_data}"
            table_images[img_path.name] = data_uri
        print(f"  -> {len(b64_data)} bytes (base64)")

    # Read HTML
    html_path = Path('te_market_inefficiency_medium_ready.html')
    html = html_path.read_text(encoding='utf-8')
    print(f"\nOriginal HTML size: {len(html)} bytes")

    # Replace table image URLs with data URIs
    # Keep chart images as external URLs (they work fine)
    for filename, data_uri in table_images.items():
        # Match only raw.githubusercontent.com URLs for table images
        pattern = f'src="https://raw.githubusercontent.com/[^"]+/article/images/te_market_inefficiency/{filename}"'
        html = re.sub(pattern, f'src="{data_uri}"', html)
        print(f"Embedded: {filename}")

    # Write updated HTML
    html_path.write_text(html, encoding='utf-8')
    print(f"\nUpdated HTML size: {len(html)} bytes")

    # Read original size again for accurate comparison
    original_size = len(html_path.read_text(encoding='utf-8'))
    print(f"Size increase: {original_size - len(html)} bytes")

    # Verify no table image URLs remain
    remaining = re.findall(r'table_\d+\.png', html)
    if remaining:
        print(f"\nWarning: Found {len(remaining)} remaining table image references")
    else:
        print("\n[OK] All table images successfully embedded as data URIs")

if __name__ == '__main__':
    embed_table_images()
