import os
from PIL import Image


def create_comparison(person_name, cloth_name, output_dir, final_dir):
    person_path = os.path.join("D:/projects/VITON-HD/test/image", person_name)
    cloth_path = os.path.join("D:/projects/VITON-HD/test/cloth", cloth_name)
    tryon_path = os.path.join(
        "results/viton/result", person_name.replace(".jpg", ".png")
    )

    if not (
        os.path.exists(person_path)
        and os.path.exists(cloth_path)
        and os.path.exists(tryon_path)
    ):
        print(f"Skipping {person_name} as some files are missing.")
        return

    img_person = Image.open(person_path)
    img_cloth = Image.open(cloth_path)
    img_tryon = Image.open(tryon_path)

    # Resize them to have the same height
    h = 512
    w_p = int(img_person.width * (h / img_person.height))
    w_c = int(img_cloth.width * (h / img_cloth.height))
    w_t = int(img_tryon.width * (h / img_tryon.height))

    img_person = img_person.resize((w_p, h), Image.Resampling.LANCZOS)
    img_cloth = img_cloth.resize((w_c, h), Image.Resampling.LANCZOS)
    img_tryon = img_tryon.resize((w_t, h), Image.Resampling.LANCZOS)

    # Create canvas
    spacing = 15
    total_width = w_p + w_c + w_t + spacing * 2
    canvas = Image.new("RGB", (total_width, h), (255, 255, 255))

    canvas.paste(img_person, (0, 0))
    canvas.paste(img_cloth, (w_p + spacing, 0))
    canvas.paste(img_tryon, (w_p + w_c + spacing * 2, 0))

    out_path = os.path.join(final_dir, f"comparison_{person_name.split('_')[0]}.png")
    canvas.save(out_path)
    print(f"Saved comparison to: {out_path}")


import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--person", type=str, default=None, help="Person image filename")
    parser.add_argument("--cloth", type=str, default=None, help="Cloth image filename")
    args = parser.parse_args()

    final_dir = "results/viton/comparisons"
    os.makedirs(final_dir, exist_ok=True)

    if args.person and args.cloth:
        pairs = [(args.person.strip(), args.cloth.strip())]
    else:
        pairs = [
            ("01409_00.jpg", "01190_00.jpg"),
        ]

    for p, c in pairs:
        create_comparison(p, c, "results/viton/result", final_dir)


if __name__ == "__main__":
    main()
