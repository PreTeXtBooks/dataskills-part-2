#!/usr/bin/env python3
"""
Copy and convert images to PreTeXt generated-assets directory.
This script prepares images for the PreTeXt build process.
It intelligently matches image references in .ptx files with the generated images in the docs/ directory.
"""

import os
import re
import shutil
from pathlib import Path

def get_similarity_score(query, candidate, folder, folder_2):
    q = query.lower().replace(".png", "").replace(".jpg", "").replace(".jpeg", "")
    c = candidate.lower().replace(".png", "").replace(".jpg", "").replace(".jpeg", "")
    
    prefixes = [folder, folder_2, "images/", "linear-models/", "ml/", "img/"]
    
    stripped = True
    while stripped:
        stripped = False
        for prefix in prefixes:
            prefix = prefix.lower()
            if q.startswith(prefix):
                q = q[len(prefix):].strip("-/_")
                stripped = True
            if c.startswith(prefix):
                c = c[len(prefix):].strip("-/_")
                stripped = True
                
    q = q.strip("-/_")
    c = c.strip("-/_")
    
    for suffix in ["-1", "-2", "-3", "-4"]:
        if q.endswith(suffix):
            q = q[:-len(suffix)]
        if c.endswith(suffix):
            c = c[:-len(suffix)]
            
    q = q.strip("-/_")
    c = c.strip("-/_")
    
    if q == c:
        return 1000
        
    q_words = set(re.split(r"[-_ ]+", q))
    c_words = set(re.split(r"[-_ ]+", c))
    
    q_words = {w for w in q_words if w}
    c_words = {w for w in c_words if w}
    
    if not q_words or not c_words:
        return 0
        
    intersection = q_words.intersection(c_words)
    overlap_score = len(intersection) / max(len(q_words), len(c_words))
    
    partial_matches = 0
    for qw in q_words:
        for cw in c_words:
            if qw != cw:
                if qw in cw or cw in qw:
                    partial_matches += 0.5
                    
    score = overlap_score * 100 + partial_matches * 10
    
    if ("exercise" in q) != ("exercise" in c):
        score -= 150 # strong penalty for exercise mismatch
        
    return score

def write_placeholder_png(target_path):
    target_path = Path(target_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image, ImageDraw
        img = Image.new('RGB', (400, 250), color = (220, 220, 220))
        d = ImageDraw.Draw(img)
        d.text((150, 115), "Placeholder", fill=(100, 100, 100))
        img.save(target_path)
    except Exception:
        # Fallback to tiny 1x1 gray PNG if PIL is not available
        tiny_png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x08\x00\x00\x00\xf1\x18\xbf\x94\x00\x00\x00\nIDATx\x9cc\xbc\x02\x00\x00\xaa\x00\xa7\xae`b\x1d\x00\x00\x00\x00IEND\xaeB`\x82'
        target_path.write_bytes(tiny_png)

def main():
    script_dir = Path(__file__).parent
    ptx_dir = script_dir / "pretext" / "source"
    docs_dir = script_dir / "docs"
    pretext_assets = script_dir / "pretext" / "assets"
    
    print("Preparing and copying images for PreTeXt book...")
    print(f"Source: {docs_dir}")
    print(f"Target assets: {pretext_assets}")
    
    ptx_files = sorted(ptx_dir.glob("**/*.ptx"))
    
    total_images = 0
    copied_generated = 0
    copied_static = 0
    placeholders_created = 0
    
    for ptx_file in ptx_files:
        relative_path = ptx_file.relative_to(ptx_dir)
        parts = relative_path.parts
        if len(parts) < 2:
            continue
        folder = parts[0]
        folder_2 = parts[1].replace(".ptx", "")
        
        ptx_content = ptx_file.read_text()
        ptx_images = re.findall(r'<image\s+source="([^"]+)"', ptx_content)
        
        if not ptx_images:
            continue
            
        print(f"\nProcessing: {relative_path}")
        
        html_file = docs_dir / folder / f"{folder_2}.html"
        html_images = []
        if html_file.exists():
            html_content = html_file.read_text()
            html_images = re.findall(r'<img[^>]+src="([^"]+_files/figure-html/[^"]+)"', html_content)
        else:
            print(f"  Warning: HTML file {html_file.name} not found. Fallback to name similarity only.")
            
        # Filter static and identify generated
        non_static_ptx_images = []
        for img_src in ptx_images:
            total_images += 1
            target_path = pretext_assets / img_src
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 1. Check static file in repo root (e.g. ml/img/cv-1.png)
            static_repo_path = script_dir / img_src
            if static_repo_path.exists():
                shutil.copy2(static_repo_path, target_path)
                print(f"  Copied static (repo): {img_src}")
                copied_static += 1
                continue
                
            # 2. Check static file under docs/FOLDER/img/
            static_docs_path = docs_dir / folder / "img" / Path(img_src).name
            if static_docs_path.exists():
                shutil.copy2(static_docs_path, target_path)
                print(f"  Copied static (docs): {img_src}")
                copied_static += 1
                continue
                
            non_static_ptx_images.append(img_src)
            
        if not non_static_ptx_images:
            continue
            
        # Match generated images
        if len(non_static_ptx_images) == len(html_images):
            # Perfect 1-to-1 sequential match
            for ptx_img, html_img in zip(non_static_ptx_images, html_images):
                source_path = docs_dir / folder / html_img
                target_path = pretext_assets / ptx_img
                if source_path.exists():
                    shutil.copy2(source_path, target_path)
                    print(f"  Copied generated (1-to-1): {ptx_img} -> {html_img.split('/')[-1]}")
                    copied_generated += 1
                else:
                    write_placeholder_png(target_path)
                    print(f"  Created placeholder (missing source): {ptx_img}")
                    placeholders_created += 1
        else:
            # Fallback to similarity + index distance penalty
            for i, ptx_img in enumerate(non_static_ptx_images):
                target_path = pretext_assets / ptx_img
                best_cand = None
                best_score = -9999
                for j, html_img in enumerate(html_images):
                    cand_name = Path(html_img).name
                    score = get_similarity_score(ptx_img, cand_name, folder, folder_2)
                    
                    # Apply index distance penalty to preserve order
                    index_distance = abs(i - j)
                    score -= index_distance * 15
                    
                    if score > best_score:
                       best_score = score
                       best_cand = html_img
                        
                if best_score > -100 and best_cand:
                    source_path = docs_dir / folder / best_cand
                    if source_path.exists():
                       shutil.copy2(source_path, target_path)
                       print(f"  Copied generated (similarity): {ptx_img} -> {best_cand.split('/')[-1]}")
                       copied_generated += 1
                    else:
                       write_placeholder_png(target_path)
                       print(f"  Created placeholder (missing source): {ptx_img}")
                       placeholders_created += 1
                else:
                    # No good match, create placeholder
                    write_placeholder_png(target_path)
                    print(f"  Created placeholder (no match): {ptx_img}")
                    placeholders_created += 1
                    
    print("\nImage copying and preparation complete!")
    print(f"  Total images processed: {total_images}")
    print(f"  Copied generated images: {copied_generated}")
    print(f"  Copied static images: {copied_static}")
    print(f"  Placeholders created: {placeholders_created}")
    
    return 0

if __name__ == "__main__":
    exit(main())

