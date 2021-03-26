import os
import argparse
import xml.etree.ElementTree as ET

supportedTextExtension = ['.txt']

dict = {2: 'couplet', 3: 'triplet', 4: 'quatrain', 6: 'sestet', 8: 'octave'}


def dir_path(path):
    if os.path.exists(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"path is not valid")


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", type=dir_path, required=True, help="path or directory of files do you want convert (required)")
parser.add_argument("-e", "--encoding", help="text encoding of files do you want convert (optional delault is utf-8)")

args = parser.parse_args()


def get_XMLs(path, encoding="UTF-8"):
    if os.path.isdir(path):
        for fileName in os.listdir(path):
            file_to_xml(path + '\\' + fileName, encoding)

    elif os.path.isfile(path):
        file_to_xml(path, encoding)


def get_lines(filePath, encoding, extension):
    lines = []
    if extension in supportedTextExtension:
        file = open(filePath, "r", encoding=encoding)

        if extension == '.txt':
            text = file.read()
            lines = text.splitlines()

        file.close()
    else:
        print("Error: " + "'" + filePath + "'" + " file extension is not supported")
        
    return lines


def file_to_xml(filePath, encoding):
    p = os.path.splitext(filePath)
    lines = get_lines(filePath, encoding, p[1])
    if lines:
        root = ET.Element("text")
        strofa = ET.SubElement(root, "lg")
        count = 0
        for line in lines:
            if line:
                l = ET.SubElement(strofa, "l")
                l.text = line
                count += 1
            else:
                if count in dict:
                    strofa.attrib['type'] = dict[count]
                count = 0
                strofa = ET.SubElement(root, "lg")
        if count in dict:
            strofa.attrib['type'] = dict[count]

        comment = ET.Comment('Created by bucchio! visit: https://github.com/JacopoBucchioni/text-to-xml')
        root.insert(0, comment)

        xml = ET.ElementTree(root)
        ET.indent(xml)

        dir = os.path.dirname(p[0]) + '\\xml'
        if not os.path.exists(dir):
            os.makedirs(dir)
        xmlpath = dir + '\\' + os.path.basename(p[0]) + '.xml'
        xml.write(xmlpath, encoding=encoding, xml_declaration=True)

        if os.path.exists(xmlpath):
            print("SUCCESS...." + xmlpath)
        else:
            print("ERROR...." + filePath)


if __name__ == '__main__':
    if args.encoding:
        get_XMLs(args.path, args.encoding)
    else:
        get_XMLs(args.path)
