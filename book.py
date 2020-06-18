# -*- coding:utf-8 -*-
'''
@Description: 合并小说
@Author: lamborghini1993
@Date: 2019-08-13 16:56:10
@UpdateDate: 2019-08-13 19:05:54
'''

import os


class MergerTxt:
    m_SourDir = "/home/duoyi/spider/quanshuwang"
    m_DesDir = "/home/duoyi/spider/全书网2/"

    def Start(self):
        for filename in os.listdir(self.m_SourDir):
            filepath = os.path.join(self.m_SourDir, filename)
            if os.path.isfile(filepath):
                continue
            self.MergerBook(filepath, filename)

    def MergerBook(self, bookDir: str, bookname: str):
        lstChapter = os.listdir(bookDir)
        lstChapter = sorted(lstChapter)
        newfile = os.path.join(self.m_DesDir, bookname + ".txt")
        if os.path.exists(newfile):
            return
        bookf = open(newfile, "a+", encoding="utf-8")
        for filename in lstChapter:
            if not filename.endswith(".txt"):
                continue
            filepath = os.path.join(bookDir, filename)
            lines = []
            chapter = filename[:-4].split("_", 1)[1]
            with open(filepath, "r") as f:
                lines = f.readlines()
                firstline = lines[0]
                if firstline.find("章") == -1:
                    lines.insert(0, "\r\n" + chapter + "\r\n\r\n")
            bookf.writelines(lines)
        bookf.close()
        print(f"{newfile}...{len(lstChapter)-1}")


if __name__ == "__main__":
    MergerTxt().Start()
