import os
import time
import click
from tqdm import tqdm
import pyautogui
from PIL import ImageGrab


def parse_coordinates(s: str) -> tuple[int]:
    l = [int(value.strip()) for value in s.split(",")]
    if len(l) != 2:
        raise ValueError("2 coordinate values must be provided")
    return tuple(l)


def parse_rect(s: str) -> tuple[int]:
    l = [int(value.strip()) for value in s.split(",")]
    if len(l) != 4:
        raise ValueError("4 coordinate values must be provided for rects")
    return tuple(l)


# fmt: off
@click.command()
@click.option("--nextpos", type=parse_coordinates, help="coordinates of the next button (comma seperated list)")
@click.option("--offpos", type=parse_coordinates, help="coordinates of a position outside the book")
@click.option("--screenrect", type=parse_rect, help="coordinates of the rect to be screenshotted (comma seperated list: top left x, top left y, bottom right x, botom right y)")
@click.option("--pagenum", type=int, help="number of pages the scanned book has")
@click.option("--outdir", type=click.Path(file_okay=False), help="path to save the grabbed images to")
# fmt: on
def scan(
    nextpos: tuple[int],
    offpos: tuple[int],
    screenrect: tuple[int],
    pagenum: int,
    outdir: str,
) -> None:
    os.makedirs(outdir, exist_ok=True)

    for i in range(3, 0, -1):
        print(f"starting in {i} seconds...")
        time.sleep(1)

    number_width = len(str(pagenum + 1))
    for i in tqdm(range(pagenum)):
        image = ImageGrab.grab(screenrect)
        image.save(os.path.join(outdir, f"page_{str(i + 1).zfill(number_width)}.png"))

        pyautogui.click(*nextpos)
        time.sleep(3)
        pyautogui.moveTo(*offpos)
        time.sleep(2)

    print(f"finished scanning {pagenum} pages")


if __name__ == "__main__":
    scan()
