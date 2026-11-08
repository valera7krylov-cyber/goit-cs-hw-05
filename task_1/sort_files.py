import argparse
import asyncio
import logging
import shutil
from pathlib import Path

from aiopath import AsyncPath

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Sort files by extension asynchronously"
    )

    parser.add_argument("source", help="Source folder")
    parser.add_argument("output", help="Output folder")

    return parser.parse_args()

async def read_folder(
    source: AsyncPath,
    output: AsyncPath,
    tasks: list[asyncio.Task[None]]
):
    try:
        async for item in source.iterdir():
            if await item.is_dir():
                await read_folder(item, output, tasks)
            else:
                tasks.append(
                    asyncio.create_task(copy_file(item, output))
                )

    except OSError:
        logging.exception(f"Error reading folder: {source}")

async def copy_file(source_file: AsyncPath, output: AsyncPath):
    try:
        extension = source_file.suffix[1:].lower() or "no_extension"

        target_folder = output / extension

        await target_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        target_file = target_folder / source_file.name

        await asyncio.to_thread(
            shutil.copy2,
            source_file,
            target_file
        )

        logging.info(f"Copied: {source_file} -> {target_file}")

    except Exception:
        logging.exception(f"Error copying file: {source_file}")

async def main():
    args = parse_arguments()

    source_path = Path(args.source).resolve()
    output_path = Path(args.output).resolve()

    if output_path == source_path or source_path in output_path.parents:
        logging.error("Output folder must not be inside source folder")
        return

    source = AsyncPath(source_path)
    output = AsyncPath(output_path)

    if not await source.is_dir():
        logging.error("Source folder does not exist")
        return

    await output.mkdir(parents=True, exist_ok=True)

    tasks = []
    await read_folder(source, output, tasks)
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    asyncio.run(main())