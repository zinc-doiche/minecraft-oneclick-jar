import sys
import platform
from file_util import *

PAPER_URL = "https://api.papermc.io/v2/projects/paper"
VANILLA_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"

JVM_ARGS = "-Xmx2G -Xms1G"

def extract_paper_download_url(json_data, version):
    builds = json_data['builds'][-1]
    last_build = builds['build']

    return f"{PAPER_URL}/versions/{version}/builds/{last_build}/downloads/paper-{version}-{last_build}.jar"


def extract_vanilla_download_url(json_data, version):
    meta_url = ""

    for version_data in json_data['versions']:
        if version_data['id'] == version:
            meta_url = version_data['url']
            break

    if meta_url == "":
        return None

    meta_data = fetch_json(meta_url)

    return meta_data['downloads']['server']['url']


def set_eula_and_run(save_path, jar_name):
    dir_name = os.path.dirname(save_path)

    run_name = "run.bat" if platform.system() == 'Windows' else "run.sh"

    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    with open(f'{save_path}/eula.txt', 'w', encoding='utf-8') as eula:
        eula.write('eula=true')

    with open(f'{save_path}/{run_name}', 'w', encoding='utf-8') as run_sh:

        if platform.system() != 'Windows':
            run_sh.write('#!/bin/bash\n')

        run_sh.write(f'java {JVM_ARGS} -jar {jar_name} nogui')

    return


def get_download_url(jar_type, version):
    json_data = {}
    download_url = ""

    if jar_type == "paper":
        json_data = fetch_json(f"{PAPER_URL}/versions/{version}/builds")

    elif jar_type == "vanilla":
        json_data = fetch_json(VANILLA_URL)

    else:
        print(f"Invalid jar_type: {jar_type}")
        return None

    if json_data is None:
        return None

    if jar_type == "paper":
        download_url = extract_paper_download_url(json_data, version)

    elif jar_type == "vanilla":
        download_url = extract_vanilla_download_url(json_data, version)

    return download_url


def create_version_folder(save_path, jar_type, version):
    directory_name = f"{save_path}/{jar_type}-{version}"

    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    return directory_name


def main():
    arguments = sys.argv

    if len(arguments) < 3:
        print(f"Usage: {arguments[0]} <jar_type> <version> [<save_path>]")
        return

    jar_type = arguments[1]
    version = arguments[2]
    save_path = arguments[3] if len(arguments) == 4 else "./"

    download_url = get_download_url(jar_type, version)
    jar_name = "server.jar"

    if download_url is None:
        return

    save_path = create_version_folder(save_path, jar_type, version)
    set_eula_and_run(save_path, jar_name)
    download_file(download_url, save_path)

    return


if __name__ == "__main__":
    main()

