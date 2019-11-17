"""
This program creates uploader script that you can use to upload conda packages that are cached on your computer.
To run the script you first need to login to anaconda cloud by running

anaconda login

then you run created script and things will get uploaded

"""
import argparse
from pathlib import Path
import sys


def process_cml() -> argparse.Namespace:
    """
    Parses command line
    :return: {argparse.Namespace}
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('--conda-env-file', required=True)

    parser.add_argument('--work-dir', required=True, type=str)

    parser.add_argument('--conda-install-path', required=True)

    parser.add_argument('--channel-name', required=False, default='compucell3d', type=str,
                        help="anaconda channel name - packages will be uploaded there ")

    args = parser.parse_args()
    return args


def parse_conda_env(conda_env_file: str) -> dict:
    """
    Parses conda env file This file needs to be generated using
    conda list --explicit > <this file>
    to create env using this file use:
    conda create --name <env> --file <this file>
    :param conda_env_file:
    :return: dictionary with parsing results for easy postprocessing
    """

    header_lines = []
    pkg_urls = []

    pkg_names = []


    with open(conda_env_file, 'r') as fin:
        for line in fin.readlines():

            # skipping empty lines
            if not line.strip():
                continue

            if line.strip().startswith('#') or line.strip().startswith('@'):
                header_lines.append(line)
                continue

            url = Path(line.strip())
            pkg_name = url.parts[-1]

            pkg_urls.append(url)
            pkg_names.append(pkg_name)

    parse_dict = {
        'header_lines': header_lines,
        'pkg_urls': pkg_urls,
        'pkg_names': pkg_names,

    }
    return parse_dict


def create_upload_script(parse_dict: dict, work_dir: str, conda_install_path: str):
    """
    Generates bash or batch script (inside work_dir) that will upload packages.

    :param parse_dict:
    :param work_dir:
    :param conda_install_path:
    :return:
    """

    Path(work_dir).mkdir(parents=True, exist_ok=True)

    if sys.platform.startswith('win'):
        upload_script_path = Path(work_dir).joinpath('conda_upload.bat')
    else:
        upload_script_path = Path(work_dir).joinpath('conda_upload.sh')

    with open(upload_script_path, 'w') as sc_out:
        for pkg_name in parse_dict['pkg_names']:
            full_pkg_path = str(Path(conda_install_path).joinpath('pkgs', pkg_name))
            sc_out.write(f'anaconda upload {full_pkg_path}\n')


def create_modified_environment(parse_dict: dict, work_dir: str, environment_basename: str = 'conda_env.txt',
                                channel_name: str = 'compucell3d'):
    """
    Generates new environment file

    :param parse_dict:
    :param work_dir:
    :param environment_basename:
    :param channel_name:
    :return:
    """

    Path(work_dir).mkdir(parents=True, exist_ok=True)

    # Creating explicit environment file

    conda_env_fname = environment_basename + '.upload.txt'

    env_file_path = Path(work_dir).joinpath(conda_env_fname)

    path_header = f'https://conda.anaconda.org/{channel_name}/'
    with open(env_file_path, 'w') as env_out:
        for header_line in parse_dict['header_lines']:
            env_out.write(f'{header_line}')

        for pkg_url in parse_dict['pkg_urls']:
            pkg_url_path = Path(pkg_url)
            path_trail = pkg_url_path.parts[-2:]
            new_channel_path = path_header + str(Path().joinpath(*list(path_trail)))

            env_out.write(f'{new_channel_path}\n')


if __name__ == '__main__':
    args = process_cml()

    conda_env_file = args.conda_env_file
    work_dir = args.work_dir
    conda_install_path = args.conda_install_path
    channel_name = args.channel_name

    parse_dict = parse_conda_env(conda_env_file=conda_env_file)

    create_upload_script(parse_dict=parse_dict, work_dir=work_dir, conda_install_path=conda_install_path)

    modified_conda_env = Path(conda_env_file).stem

    create_modified_environment(parse_dict=parse_dict, work_dir=work_dir, environment_basename=modified_conda_env,
                                channel_name=channel_name)




