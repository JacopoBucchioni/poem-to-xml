import os
import argparse
import xml.etree.ElementTree as ET

supportedTextExtension = ['.txt']


def dir_path(path):
    if os.path.exists(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not valid")


parser = argparse.ArgumentParser()
parser.add_argument("--path", type=dir_path, required=True, help="path of file or directory")
parser.add_argument("--encoding", help="text file encoding")

args = parser.parse_args()


def get_XMLs(path, encoding='UTF-8'):
    if os.path.isdir(path):
        for fileName in os.listdir(path):
            file_to_xml(path+'/'+fileName, encoding)

    elif os.path.isfile(path):
        file_to_xml(path, encoding)


def file_to_xml(filePath, encoding):
    p = os.path.splitext(filePath)
    if p[1] in supportedTextExtension:

        file = open(filePath, "r", encoding=encoding)
        text = file.read()
        lines = text.splitlines()
        file.close()

        root = ET.Element("lg")
        strofa = ET.SubElement(root, "lg")
        for line in lines:
            if line:
                l = ET.SubElement(strofa, "l")
                l.text = line
            else:
                strofa = ET.SubElement(root, "lg")
        xml = ET.ElementTree(root)

        dir = os.path.dirname(p[0]) + '/xml'
        if not os.path.exists(dir):
            os.makedirs(dir)
        xml.write(dir + '/' + os.path.basename(p[0]) + '.xml', encoding=encoding)


if __name__ == '__main__':
    get_XMLs(args.path, args.encoding)
