import os
#import better_exceptions
import sys


class GanntChart:
    def __init__(self):
        self.SVG = ""
        self.Height = 0
        self.width = 0
        self.Scale = 0
        self.NumberOfMachine = 0
        self.NumberOfJobs = 0
        self.fontsize = 20

    def init(self, NumberOfMachine, TotalLength, Scale):
        self.NumberOfMachine = NumberOfMachine
        self.Height = NumberOfMachine * 80 + 80
        self.width = TotalLength * Scale
        self.Scale = Scale
        self.SVG = "<svg width=\"" + str(self.width + 100) + "\" height=\"" + str(
            self.Height + 100) + "\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">\n"
        self.SVG += "<line fill=\"none\" stroke=\"#000000\" stroke-width=\"3\"  x1=\"40\" y1=\"10\" x2=\"40\" y2=\"" + str(
            self.Height) + "\" />\n"
        for i in range(1, self.NumberOfMachine + 1):
            self.SVG += "<text fill=\"#000000\" stroke=\"#000000\" stroke-width=\"0\" font-size=\"20\" font-family=\"serif\" " + \
                        "text-anchor=\"left\" xml:space=\"preserve\" font-weight=\"bold\"  x=\"5\" y=\"" + str(
                60 + (i - 1) * 80) + "\" >M" + str(i) + "</text>\n\n"

        for i in range(10, self.width, 10):
            self.SVG += "<text fill=\"#000000\" stroke=\"#000000\" stroke-width=\"0\" font-size=\"14\" font-family=\"serif\" " + \
                        "text-anchor=\"center\" xml:space=\"preserve\" font-weight=\"bold\"  x=\"" + str(
                (i * self.Scale) + 40) + "\" y=\"" + str(self.Height + 25) + "\" >" + str(i) + "</text>\n\n"
            self.SVG += "<line fill=\"none\" stroke=\"#000000\" stroke-width=\"3\"  x1=\"" + str(
                (i * self.Scale) + 40) + "\" y1=\"" + str(self.Height - 5) + "\" x2=\"" + str(
                (i * self.Scale) + 40) + "\" y2=\"" + str(
                self.Height) + "\" id=\"\"/>\n"
        self.SVG += "<line fill=\"none\" stroke=\"#000000\" stroke-width=\"3\"  x1=\"40\" y1=\"" + str(
            self.Height) + "\" x2=\"" + str(self.width + 100) + "\" y2=\"" + str(self.Height) + "\" id=\"\"/>\n"

    def AddJob(self, JobName, Machine, Starting_Time, Processing_Time):
        self.SVG += "<rect width=\"" + str(
            self.Scale * Processing_Time) + "\" height=\"60\" style=\"fill:#FFFFFF;fill-opacity=1;stroke-width:1;\"  stroke=\"#000000 \" x=\"" \
                    + str(Starting_Time * self.Scale + 40) + "\" y=\"" + str(25 + (Machine - 1) * 80) + "\"  />\n\n"
        self.SVG += "<text fill=\"#000000\" stroke=\"#000000\" stroke-width=\"0\" font-size=\"" + str(
            self.fontsize) + "\" font-family=\"serif\" " + \
                    "text-anchor=\"center\" xml:space=\"preserve\" font-weight=\"bold\"  x=\"" + str(
            (2 * Starting_Time * self.Scale + Processing_Time * self.Scale) / 2 + 35) \
                    + "\" y=\"" + str(60 + (Machine - 1) * 80) + "\" >" + JobName + " </text>\n\n"
        self.SVG += "<text fill=\"#000000\" stroke=\"#000000\" stroke-width=\"0\" font-size=\"" + str(
            self.fontsize) + "\" font-family=\"serif\" " + \
                    "text-anchor=\"center\" xml:space=\"preserve\" font-weight=\"bold\"  x=\"" + str(
            (Starting_Time * self.Scale + Processing_Time * self.Scale + 40)) + "\" y=\"" \
                    + str(25 + (Machine - 1) * 80 + 75) + "\" >" + str(Starting_Time + Processing_Time) + "</text>\n\n"

    def SavetoFile(self, FileName):
        self.SVG += "</svg>"
        ow = open(FileName + ".svg", 'w')
        ow.write(self.SVG)
        ow.close()

    def SetFontSize(self, fontsize):
        self.fontsize = fontsize
