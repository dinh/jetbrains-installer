#!/usr/bin/env python3

import os
import subprocess
import sys
import tarfile
import requests
import glob
import argparse
import re


USER_HOME = os.getenv('HOME')

# Download file helper
# This helper download a file using filename and default params such as location and version. - return boolean
def download_file(filename, location = USER_HOME + '/Downloads', version = 'nd', protocol = 'https://', fqdn = 'download.jetbrains.com', uri = '/webide/', extension = '.tar.gz'):

    if (version == 'nd'):
        full_filename = filename + extension
    else:
        full_filename = filename + version + extension

    print('Selected file: ' + full_filename)

    url = protocol + fqdn + uri + full_filename

    print('File is located: ' + url)
    print()

    try:
        print('Downloading...')
        response = requests.get(url)
        if (response.status_code != 200):
            print("Invalid request: " + str(response.status_code))
            return False

        with open(location + full_filename, 'wb') as f:
            f.write(response.content)

        print('Download Completed\n')
        return True

    except Exception as e:
        print("Error during download file" + str(e))
        return False


# Extract file helper
# This helper extract a file using filename and default params such as location and version. - return boolean
def extract_file(filename, location = USER_HOME + '/Downloads', version = 'nd', extension = '.tar.gz'):

    if (extension != '.tar.gz'):
        print('Invalid extension')

    if (version == 'nd'):
        full_filename = filename + extension
    else:
        full_filename = filename + version + extension

    try:
        print('Extracting ' + location + full_filename + ' ...')
        with tarfile.open(location + full_filename) as tar:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, path=location)

        print('Extraction completed\n')
        return True

    except Exception as e:
        print("Error during extracting file" + str(e))
        return False

# Remove file helper
# This helper remove a file using filename and default params such as location and version. - return boolean
def remove_file(filename, location = USER_HOME + '/Downloads', version = 'nd', extension = '.tar.gz'):

    if (version == 'nd'):
        full_filename = filename + extension
    else:
        full_filename = filename + version + extension

    full_location = location + full_filename

    try:
        print('Deleting ' + full_location + ' ...')
        os.remove(full_location)
        print('Done\n')
        return True

    except Exception as e:
        print("Error during deleting file" + str(e))
        return False

# Rename file helper
# This helper rename a file using filename and default params such as location and version. - return boolean
def rename_file(filename, new_filename, location = USER_HOME + '/Downloads'):


    full_location = glob.glob(location + filename + '*')
    new_full_location = location + new_filename

    try:
        for f in full_location:

            print('Moving ' + f + ' to ' + new_full_location + ' ...')
            os.rename(f, new_full_location)
            print('Done')
            return True

    except Exception as e:
        print("Error during moving file" + str(e))
        return False

# Link file helper
# This helper link a file using filename, destination and default params such as location. - return boolean
def link_file(source, destination):

    # source = glob.glob(location + filename + '/bin/*.sh')

    try:
        # for f in source:
            print('Linking ' + source + ' to ' + destination + ' ...')
            os.symlink(source, destination)
            print('Done\n')
            return True

    except Exception as e:
        print("Error during linking file" + str(e))
        return False


def check_required_args(data, action):
    fields = data[action]

    required_fields = fields['required']

    for k, field in required_fields.items():
        if (field == None):
            print('Required ' + k + ' argument not provided')
            sys.exit(1)

def check_action(args):

    actions = [0, 0, 0]
    action = False

    for k, argument in args.items():
        if (argument != None):
            action = 1

            if (k == 'install'):
                index = 0
                actions[index] = action
            if (k == 'remove'):
                index = 1
                actions[index] = action
            if (k == 'upgrade'):
                index = 2
                actions[index] = action
            # if (k == 'version'):
            #     index = 3
            #     actions[index] = action

    return actions


def jetbrains_version(version, pat=re.compile(r"([0-9]+)\.([0-9])\.([0-9])")):
    if not pat.match(version):
        raise argparse.ArgumentTypeError
    return version


def jetbrains_build_version(version, pat=re.compile(r"([0-9]+)\.([0-9]+)\.([0-9]+)")):
    if not pat.match(version):
        raise argparse.ArgumentTypeError
    return version

def check_jetbrains_build_version(location, target):
    directory_contents = os.listdir(location)

    for directory_content in directory_contents:
        print(directory_content)
        print(type(directory_content))

        if target in directory_content:
            return directory_content



def install(target, version, location = '/opt/'):

    jb_products = {
        'phpstorm' : 'PhpStorm-',
        'clion' : 'CLion-',
        'pycharm' : 'pycharm-professional-',
        'webstorm' : 'WebStorm-',
        'datagrip' : 'datagrip-',
        'intellij' : 'ideaIU-'
    }

    for product in jb_products:
         if product == target:
             download_file(jb_products[target], location, version)
             extract_file(jb_products[target], location, version)
             remove_file(jb_products[target], location, version)
             link_file(check_jetbrains_build_version(location, jb_products[target]), location + target)
             link_file(target + '/bin/'+ target +'.sh', '/usr/local/bin/' + target)


def upgrade():
    # TODO: implementare funzione di update/upgrade
    pass

def unistall():
    # TODO: implementare funzione di delete/uninstall
    subprocess.call(["rm", "-Rf", '/opt/'])
    subprocess.call(["mkdir", "-p", '/opt/'])
    remove_file('phpstorm', '/usr/local/bin/', 'nd', '')




# Main
def main():

    parser = argparse.ArgumentParser(description='JETBRAINS-INSTALLER', usage='%(prog)s [options]')
    parser.add_argument('-i', '--install', help='test help install', action="store", type=str, required=False)
    parser.add_argument('-v', '--version', help='test help version', action="store", type=jetbrains_version, required=False)
    parser.add_argument('-r', '--remove', help='test help remove', action="store", type=str, required=False)
    parser.add_argument('-u', '--upgrade', help='test help upgrade', action="store", type=str, required=False)
    args = vars(parser.parse_args())

    #print(args)

    data = {
        'install_action': {
            'required': {
                'target': args['install'],
            },
            'optional': {
                'version': args['version']
            }
        },
        'remove_action': {
            'required': {
                'target': args['remove']
            },
            'optional': {
                'version': args['version']
            }
        },
        'upgrade_action': {
            'required': {
                'target': args['upgrade']
            },
            'optional': {
                'version': args['version']
            }
        }
    }

    #print(data)

    actions = check_action(args)
    print()
    print("Actions:")
    print(actions)
    #sys.exit(0)


    # check_required_args(data, 'install_action')


    if (actions[0] == 1 and actions[1] == 0 and actions[2] == 0):
        check_required_args(data, 'install_action')
        print('Eseguo install')
        install(data['install_action']['required']['target'], data['install_action']['optional']['version'])
        sys.exit(0)

    if (actions[0] == 0 and actions[1] == 1 and actions[2] == 0):
        check_required_args(data, 'remove_action')
        print('Eseguo remove')
        unistall()
        sys.exit(0)

    if (actions[0] == 0 and actions[1] == 0 and actions[2] == 1):
        check_required_args(data, 'upgrade_action')
        print('Eseguo upgrade')
        sys.exit(0)


    print("Invalid")






    # TODO: impostare logica core main (switch funzioni principali programma)

    # TODO: validazione input dati e chiamata alla funzione richiesta

    #install()

    #delete()



# Execute
if __name__ == '__main__':
    main()