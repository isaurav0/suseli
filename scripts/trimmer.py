import os
import sys
import subprocess


# -i represents input folder path
# Input Folder may contain subfolders
# -o represents output folder path. Output folder path is named as
# chosen by -o. Output subfolders are named the same as they were before.
# Each file inside folder is named from starting from 00000.mp3 and so on.

def trim_audio(input_file, output_file):
    print("Input File: ", input_file)
    print("Output File: ", output_file)
    # command
    # ffmpeg -ss 10 -i input_file -t 40 output_file

    subprocess.call(['ffmpeg', '-ss', '10', '-i', input_file, '-t', '40', output_file])

    # input_file = '\ '.join(input_file.split(' '))
    # with open(input_file, 'rb') as ip:
    #     for data in ip.readlines():
    #         with open(output_file, 'wb') as fw:
    #             fw.write(data)



def ismp4(file):
    formats = ['mp4']
    if file.split('.')[-1] in formats:
        return True
    return False


def main():
    input_file = None
    input_directory = None
    output_directory = None
    output_file = None

    for i, value in enumerate(sys.argv, 0):
        if value == '-if':
            input_file = sys.argv[i + 1]
        if value == '-of':
            output_file = sys.argv[i + 1]
        if value == '-id':
            input_directory = sys.argv[i + 1]
        if value == '-od':
            output_directory = sys.argv[i + 1]

    if not input_file and not input_directory:
        raise Exception("Input File(-if) or Input Directory(-id) Needed.")

    if input_file:
        if not os.path.exists(input_file):
            raise Exception("Input File Doesn't exist.")
            exit()

        output_file = output_file if output_file else 'cut_' + input_file
        trim_audio(input_file, output_file, format="mp3")
        exit()

    if input_directory:
        if not os.path.exists(input_directory):
            raise Exception("Input Directory Doesn't exist.")
            exit()

        if not output_directory:
            output_directory =  os.path.join('/'.join(sys.argv[0].split('/')[:-1]), input_directory.split('/')[-1] + '_trimmed')

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

    for folder, subs, files in os.walk(input_directory):
        # print(files)
        print("Folder: ", folder)
        print("SUb Folders: ", subs)
        print("Files: ", files)
        print("---------------------")
        for i, file in enumerate(files):
            if not ismp4(file):
                continue
            input_file = os.path.join(folder, file)
            sub_directory = folder.split('/')[-1]
            output_sub_directory = os.path.join(output_directory, sub_directory)
            if not os.path.exists(output_sub_directory):
                print("Creating sub directory: ", output_sub_directory)
                os.makedirs(output_sub_directory)
            out_format = 'mp3'
            output_file = os.path.join(output_sub_directory, str(i) + '.' + out_format)
            trim_audio(input_file, output_file)
            print('+++++++Converted+++++++++++')




if __name__ == "__main__":
    main()

