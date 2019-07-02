# -*-coding:utf-8-*-
from lxml import etree
import os


class VOCAnnotation(object):
    def __init__(self, imageFileName, width, height):
        annotation = etree.Element("annotation")
        self.__newTextElement(annotation, "folder", "BITVehicle")
        self.__newTextElement(annotation, "filename", imageFileName)

        source = self.__newElement(annotation, "source")
        self.__newTextElement(source, "database", "BIT-Vehicle dataset")
        self.__newTextElement(source, "annotation", "BIT-Vehicle")
        # self.__newTextElement(source, "image", "flickr")
        # self.__newTextElement(source, "flickrid", "341012865")

        owner = self.__newElement(annotation, "owner")
        # self.__newTextElement(owner, "flickrid", "Fried Camels")
        self.__newTextElement(owner, "name", "BIOT")

        size = self.__newElement(annotation, "size")
        self.__newIntElement(size, "width", width)
        self.__newIntElement(size, "height", height)
        self.__newIntElement(size, "depth", 3)

        self.__newTextElement(annotation, "segmented", "0")

        self._annotation = annotation

    def __newElement(self, parent, name):
        node = etree.SubElement(parent, name)
        return node

    def __newTextElement(self, parent, name, text):
        node = self.__newElement(parent, name)
        node.text = text

    def __newIntElement(self, parent, name, num):
        node = self.__newElement(parent, name)
        node.text = "%d" % num

    def addBoundingBox(self, xmin, ymin, xmax, ymax, name):
        object = self.__newElement(self._annotation, "object")

        self.__newTextElement(object, "name", name)
        self.__newTextElement(object, "pose", "Unspecified")
        self.__newTextElement(object, "truncated", "0")
        self.__newTextElement(object, "difficult", "0")

        bndbox = self.__newElement(object, "bndbox")
        self.__newIntElement(bndbox, "xmin", xmin)
        self.__newIntElement(bndbox, "ymin", ymin)
        self.__newIntElement(bndbox, "xmax", xmax)
        self.__newIntElement(bndbox, "ymax", ymax)

    def save(self, saveFileName):
        tree = etree.ElementTree(self._annotation)
        tree.write(saveFileName, pretty_print=True)


if __name__ == '__main__':
    voc = VOCAnnotation("2.png", 100, 100)
    voc.addBoundingBox(1, 2, 3, 4, "person")
    voc.addBoundingBox(5, 6, 7, 8, "person")
    voc.save("test.xml")
