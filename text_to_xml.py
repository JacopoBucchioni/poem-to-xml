import os
import argparse
import xml.etree.ElementTree as ET

supportedTextExtension = ['.txt']

dict = {2: 'distico', 3: 'terzina', 4: 'quartina', 6: 'sestina', 8: 'ottava'}


def dir_path(path):
    if os.path.exists(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"path is not valid")


parser = argparse.ArgumentParser()
parser.add_argument("-path", type=dir_path, required=True, help="path of file or directory")
parser.add_argument("-encoding", help="text file encoding")

args = parser.parse_args()


def get_XMLs(path, encoding="UTF-8"):
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
        strofa.attrib['type'] = dict[count]

        xml = ET.ElementTree(root)
        ET.indent(xml)

        dir = os.path.dirname(p[0]) + '/xml'
        if not os.path.exists(dir):
            os.makedirs(dir)
        xml.write(dir + '/' + os.path.basename(p[0]) + '.xml', encoding=encoding, xml_declaration=True)


if __name__ == '__main__':
    if args.encoding:
        get_XMLs(args.path, args.encoding)
    else:
        get_XMLs(args.path)
