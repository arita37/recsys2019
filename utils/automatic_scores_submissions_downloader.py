import paramiko
import os
from os.path import expanduser
from os.path import join
from utils.check_folder import check_folder
import easygui


def progress(bytes_so_far, bytes_to_be_transferred):
    print('progress: {}%'.format(
        (bytes_so_far/bytes_to_be_transferred)*100), end="\r")


"""
    it searches for a pattern in the folder scores and submissions of a remote ec2 machine
    then it downloads all the files matching the pattern, putting those in a folder named equal to the pattern 
"""


def download_scores_and_sub(pattern, user_name='ubuntu'):
    path_to_pem = easygui.fileopenbox(
        msg='pick the pem', default='~/Downloads')
    ip = easygui.enterbox("Whats the ip?")
    downloads_folder = join(expanduser("~"), 'Downloads')

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(ip, username=user_name, key_filename=path_to_pem)

    print("transferring scores")
    bp = '~/recsys2019/scores/'
    command = 'find {} -name "*{}*.npy"'.format(bp, pattern)
    stdin, stdout, stderr = ssh.exec_command(command)
    filelist = stdout.read().splitlines()
    sftp = ssh.open_sftp()
    for afile in filelist:
        filename = afile.decode("utf-8")
        print('transferring {}'.format(filename))
        check_folder(join(downloads_folder, pattern)+'/')
        sftp.get(filename, join(downloads_folder, pattern,
                                filename.split('/')[-1]), progress)

    print("transferring subs")
    bp = '~/recsys2019/submissions/'
    command = 'find {} -name "*{}*.csv"'.format(bp, pattern)
    stdin, stdout, stderr = ssh.exec_command(command)
    filelist = stdout.read().splitlines()
    sftp = ssh.open_sftp()
    for afile in filelist:
        filename = afile.decode("utf-8")
        print('transferring {}'.format(filename))
        check_folder(join(downloads_folder, pattern)+'/')
        sftp.get(filename, join(downloads_folder, pattern,
                                filename.split('/')[-1]), progress)

    print("transferring models")
    bp = '~/recsys2019/models/'
    command = 'find {} -name "*{}*.model"'.format(bp, pattern)
    stdin, stdout, stderr = ssh.exec_command(command)
    filelist = stdout.read().splitlines()
    sftp = ssh.open_sftp()
    for afile in filelist:
        filename = afile.decode("utf-8")
        print('transferring {}'.format(filename))
        check_folder(join(downloads_folder, pattern)+'/')
        sftp.get(filename, join(downloads_folder, pattern,
                                filename.split('/')[-1]), progress)

    sftp.close()


if __name__ == '__main__':
    download_scores_and_sub('cluster=no_cluster_kind=kind1_class_weights=False_learning_rate=0.039_min_child_weight=1_n_estimators=2917_max_depth=7_subsample=1_colsample_bytree=1_reg_lambda=0.425_reg_alpha=0.135')
