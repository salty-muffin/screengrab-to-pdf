import os
import click
from PIL import Image
from glob import glob


# fmt: off
@click.command()
@click.option("--dir", type=click.Path(exists=True, file_okay=False), help="path to the grabbed images")
@click.option("--outfile", type=click.Path(dir_okay=False), help="path to output pdf")
# fmt: on
def print(dir: str, outfile: str) -> None:
    if dirname := os.path.dirname(outfile):
        os.makedirs(dirname, exist_ok=True)

    images = [Image.open(f) for f in sorted(glob(os.path.join(dir, "*")))]

    if len(images):
        images[0].save(
            outfile,
            "PDF",
            resolution=100.0,
            save_all=True,
            append_images=images[1:] if len(images) > 1 else None,
        )


if __name__ == "__main__":
    print()
