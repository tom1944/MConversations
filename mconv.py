import sys

from mconv.datapack_updater import DatapackUpdater

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f'Usage: python {sys.argv[0]} <path-to-data-pack>')
        exit(-1)

    datapack_path = sys.argv[1]

    datapack_updater = DatapackUpdater(datapack_path)
    datapack_updater.update_datapack()

    print(f"Data pack {datapack_path} updated. Run '/reload' from your minecraft game to reload the data pack")
