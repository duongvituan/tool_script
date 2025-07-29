import os
from PIL import Image
from collections import defaultdict

# === Configuration ===
input_folder = "input"         # Input root directory
output_folder = "output"       # Output root directory
keep_alpha = True              # Preserve alpha channel (RGBA)

# Store size statistics per directory
size_stats = defaultdict(lambda: {"before": 0, "after": 0})

# Walk through all subdirectories and files
for root, _, files in os.walk(input_folder):
    for filename in files:
        if filename.lower().endswith(".png"):
            input_path = os.path.join(root, filename)
            relative_path = os.path.relpath(input_path, input_folder)
            output_path = os.path.join(output_folder, relative_path)

            # Ensure output subdirectories exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            try:
                # Get file size before optimization
                original_size = os.path.getsize(input_path)

                with Image.open(input_path) as img:
                    # Convert mode if needed
                    if keep_alpha:
                        img = img.convert("RGBA")
                    else:
                        img = img.convert("RGB")

                    # Save optimized image
                    img.save(output_path, format="PNG", optimize=True)

                # Get file size after optimization
                new_size = os.path.getsize(output_path)

                # Update size statistics
                folder_key = os.path.dirname(relative_path)
                size_stats[folder_key]["before"] += original_size
                size_stats[folder_key]["after"] += new_size

                # Print result in one line
                status = "✅" if new_size <= original_size else "⚠️"
                print(f"{status} {relative_path} | Before: {original_size / 1024:.2f} KB | After: {new_size / 1024:.2f} KB")

            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")

# === Summary ===
print("\n=== Summary by folder ===")
total_before = 0
total_after = 0
for folder, sizes in size_stats.items():
    folder_display = folder or "[root]"
    before_kb = sizes["before"] / 1024
    after_kb = sizes["after"] / 1024
    print(f"{folder_display}: Before = {before_kb:.2f} KB | After = {after_kb:.2f} KB")
    total_before += sizes["before"]
    total_after += sizes["after"]

print("\n=== Total summary ===")
print(f"Total before: {total_before / 1024:.2f} KB")
print(f"Total after : {total_after / 1024:.2f} KB")
