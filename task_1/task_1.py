import argparse
import asyncio

from aiopath import AsyncPath
from aioshutil import copyfile
import logging

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

args = vars(parser.parse_args())

source = AsyncPath(args.get("source"))
output = AsyncPath(args.get("output"))


async def read_folder(path: AsyncPath):
    async for el in path.iterdir():
        if await el.is_dir():
            await read_folder(el)
        else:
            await copy_file(el)


async def copy_file(file):
    ext_folder = output / file.suffix[1:]
    try:
        await ext_folder.mkdir(exist_ok=True, parents=True)
        await copyfile(file, ext_folder / file.name)
    except OSError as e:
        logging.error(e)

if __name__ == "__main__":
    message_format = "%(threadName)s %(asctime)s: %(message)s"
    logging.basicConfig(format=message_format, level=logging.INFO, datefmt="%H:%M:%S")

    #  python task_1.py -s picture -o output
    asyncio.run(read_folder(source))

    print("Done!")



