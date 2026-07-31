import cv2
import os
import json
import shutil
from google.colab import files
from PIL import Image

# SETTINGS

VIDEO = files.upload()
VIDEO_FILE = list(VIDEO.keys())[0]

OUTPUT = "VideoDataPack"

WIDTH = 70
HEIGHT = 70

FPS = 20

ORIGIN_X = 0
ORIGIN_Y = 100
ORIGIN_Z = 0

# DO NOT EDIT BEYOND THIS POINT

colors = [
    ((234, 236, 237), "white_wool"),
    ((142, 142, 135), "light_gray_wool"),
    ((62, 68, 71), "gray_wool"),
    ((22, 22, 27), "black_wool"),
    ((114, 72, 41), "brown_wool"),
    ((161, 39, 34), "red_wool"),
    ((240, 118, 19), "orange_wool"),
    ((249, 198, 40), "yellow_wool"),
    ((128, 199, 31), "lime_wool"),
    ((84, 109, 27), "green_wool"),
    ((21, 137, 145), "cyan_wool"),
    ((58, 179, 218), "light_blue_wool"),
    ((53, 57, 157), "blue_wool"),
    ((121, 42, 172), "purple_wool"),
    ((189, 68, 179), "magenta_wool"),
    ((237, 141, 172), "pink_wool"),

    ((207, 213, 214), "white_concrete"),
    ((125, 125, 115), "light_gray_concrete"),
    ((54, 57, 61), "gray_concrete"),
    ((8, 10, 15), "black_concrete"),
    ((96, 59, 31), "brown_concrete"),
    ((142, 32, 32), "red_concrete"),
    ((224, 97, 0), "orange_concrete"),
    ((241, 175, 21), "yellow_concrete"),
    ((94, 169, 24), "lime_concrete"),
    ((73, 91, 36), "green_concrete"),
    ((21, 119, 136), "cyan_concrete"),
    ((36, 137, 199), "light_blue_concrete"),
    ((44, 46, 143), "blue_concrete"),
    ((100, 31, 156), "purple_concrete"),
    ((170, 48, 160), "magenta_concrete"),
    ((214, 101, 143), "pink_concrete"),

    ((126, 126, 126), "stone"),
    ((123, 123, 123), "cobblestone"),
    ((106, 121, 90), "mossy_cobblestone"),
    ((122, 121, 122), "stone_bricks"),
    ((116, 120, 106), "mossy_stone_bricks"),
    ((79, 79, 84), "deepslate"),
    ((73, 73, 77), "cobbled_deepslate"),
    ((81, 81, 86), "polished_deepslate"),
    ((110, 112, 106), "tuff"),
    ((224, 224, 221), "calcite"),
    ((136, 136, 136), "andesite"),
    ((188, 188, 188), "diorite"),
    ((150, 104, 89), "granite"),

    ((216, 202, 155), "sandstone"),
    ((223, 211, 161), "smooth_sandstone"),
    ((182, 97, 48), "red_sandstone"),
    ((190, 101, 50), "smooth_red_sandstone"),
    ((219, 207, 163), "sand"),
    ((191, 103, 33), "red_sand"),

    ((134, 96, 67), "dirt"),
    ((119, 85, 59), "coarse_dirt"),
    ((61, 58, 73), "mud"),
    ((159, 164, 177), "clay"),
    ((136, 126, 126), "gravel"),

    ((240, 251, 251), "snow_block"),
    ((138, 180, 248), "ice"),
    ((142, 180, 250), "packed_ice"),
    ((115, 168, 253), "blue_ice"),

    ((162, 130, 79), "oak_planks"),
    ((114, 84, 48), "spruce_planks"),
    ((196, 180, 123), "birch_planks"),
    ((170, 117, 71), "jungle_planks"),
    ((168, 91, 50), "acacia_planks"),
    ((66, 43, 20), "dark_oak_planks"),
    ((118, 54, 48), "mangrove_planks"),
    ((228, 190, 185), "cherry_planks"),
    ((193, 173, 89), "bamboo_planks"),
    ((101, 48, 70), "crimson_planks"),
    ((43, 104, 99), "warped_planks"),

    ((109, 85, 50), "oak_log"),
    ((63, 50, 31), "spruce_log"),
    ((214, 206, 161), "birch_log"),
    ((104, 83, 50), "jungle_log"),
    ((108, 97, 86), "acacia_log"),
    ((61, 46, 27), "dark_oak_log"),
    ((89, 49, 41), "mangrove_log"),
    ((95, 62, 66), "cherry_log"),
    ((190, 172, 92), "bamboo_block"),

    ((151, 97, 83), "bricks"),
    ((137, 104, 79), "mud_bricks"),
    ((44, 21, 26), "nether_bricks"),
    ((69, 8, 9), "red_nether_bricks"),

    ((219, 223, 158), "end_stone"),
    ((217, 222, 159), "end_stone_bricks"),
    ((170, 126, 170), "purpur_block"),

    ((99, 156, 151), "prismarine"),
    ((98, 172, 158), "prismarine_bricks"),
    ((51, 91, 75), "dark_prismarine"),
    ((172, 199, 190), "sea_lantern"),

    ((236, 233, 226), "quartz_block"),
    ((239, 236, 229), "smooth_quartz"),

    ((20, 20, 20), "coal_block"),
    ((220, 220, 220), "iron_block"),
    ((249, 236, 78), "gold_block"),
    ((97, 219, 213), "diamond_block"),
    ((42, 203, 87), "emerald_block"),

    ((195, 125, 89), "copper_block"),
    ((82, 162, 136), "oxidized_copper"),

    ((133, 96, 191), "amethyst_block"),
    ((245, 183, 57), "honey_block"),
    ((112, 192, 91), "slime_block"),

    ((21, 18, 30), "obsidian"),
    ((48, 24, 71), "crying_obsidian"),
    ((143, 118, 70), "glowstone"),

    ((195, 192, 74), "sponge"),
    ((151, 155, 73), "wet_sponge"),

    ((166, 136, 38), "hay_block"),
    ((227, 223, 207), "bone_block")
]

color_cache = {}

def closest_color(rgb):

    rgb = tuple(rgb)

    if rgb in color_cache:
        return color_cache[rgb]

    best = None
    best_distance = 1e9

    for color, block in colors:
        d = (
            (rgb[0]-color[0])**2 +
            (rgb[1]-color[1])**2 +
            (rgb[2]-color[2])**2
        )

        if d < best_distance:
            best_distance = d
            best = block

    color_cache[rgb] = best
    return best

# Create folders

if os.path.exists(OUTPUT):
    shutil.rmtree(OUTPUT)

os.makedirs(
    OUTPUT + "/data/video/function/frames",
    exist_ok=True
)


# pack.mcmeta

with open(OUTPUT+"/pack.mcmeta","w") as f:
    json.dump({
        "pack":{
            "pack_format":48,
            "description":"MP4 Video Player"
        }
    }, f, indent=4)

video = cv2.VideoCapture(VIDEO_FILE)

frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

print("Frames:", frame_count)

previous_frame = None

frames = []
previous_frame = None

# Convert frames

for frame_number in range(frame_count):

    ok, frame = video.read()

    if not ok:
        break

    frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    img = Image.fromarray(frame)

    img = img.resize(
        (WIDTH, HEIGHT)
    )

    pixels = img.load()
    current = []

    for y in range(HEIGHT):
        for x in range(WIDTH):
            current.append(closest_color(pixels[x, y]))

    blocks = []

    for y in range(HEIGHT):

        x = 0

        while x < WIDTH:

            block = current[y*WIDTH+x]

            # Skip unchanged pixels
            if previous_frame and block == previous_frame[y*WIDTH+x]:
                x += 1
                continue

            start = x

            while (
                x + 1 < WIDTH and
                current[y*WIDTH+x+1] == block and
                (
                    previous_frame is None or
                    current[y*WIDTH+x+1] != previous_frame[y*WIDTH+x+1]
                )
            ):
                x += 1

            end = x

            if end - start >= 2:
                blocks.append(
                    f"fill {ORIGIN_X+start} {ORIGIN_Y-y} {ORIGIN_Z} "
                    f"{ORIGIN_X+end} {ORIGIN_Y-y} {ORIGIN_Z} {block}"
                )
            else:
                for xx in range(start, end+1):
                    blocks.append(
                        f"setblock {ORIGIN_X+xx} {ORIGIN_Y-y} {ORIGIN_Z} {block}"
                    )

            x += 1

    frames.append(blocks)

for i, frame in enumerate(frames):

    filename = (
        OUTPUT +
        f"/data/video/function/frames/frame_{i}.mcfunction"
    )

    with open(filename,"w") as f:

        for command in frame:
            f.write(command+"\n")

# Create playback loop

with open(
    OUTPUT+"/data/video/function/play.mcfunction",
    "w"
) as f:

    f.write(
"""scoreboard objectives add video dummy
scoreboard players set frame video 0
function video:loop
"""
    )


with open(
    OUTPUT+"/data/video/function/loop.mcfunction",
    "w"
) as f:

    for i in range(len(frames)):

        f.write(
            f"execute if score frame video matches {i} run function video:frames/frame_{i}\n"
        )

    f.write(
        f"scoreboard players add frame video 1\n"
    )

    f.write(
        f"execute if score frame video matches {len(frames)} run scoreboard players set frame video 0\n"
    )

    f.write(
        "schedule function video:loop 1t\n"
    )


print("Done!")
print("Put the folder into your world's datapacks folder.")
print("Run:")
print("/function video:play")

shutil.make_archive("VideoDataPack", "zip", "VideoDataPack")

files.download("VideoDataPack.zip")
