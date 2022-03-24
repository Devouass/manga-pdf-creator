import argparse
import os
from utils import Logger
from fpdf import FPDF
from PIL import Image

class MainClass:

	CONFIG_BASE_DIRECTORY = "config/"
	PDF_DIRECTORY = "pdf"
	MANGA_DIRECTORY = "manga/one_piece"

	def __init__(self):
		self.logger = Logger.getLogger()

	def createPdf(self, args):
		#check if number of chapter is good
		tomeNumber, chapters = self._getChapters()
		if tomeNumber:
			while tomeNumber != None:
				self._createPdf(tomeNumber, chapters)
				self._log("try to create new tome from chapter {}".format(tomeNumber + "9"))
				tomeNumber, chapters = self._getChapters(tomeNumber + "9")


	def _createPdf(self, tomeNumber, chapters):
		self._log("create One Piece {}.pdf from chapter {} to {}".format(tomeNumber,chapters[0],chapters[9]))

		pdfName = MainClass.PDF_DIRECTORY + "/" + "One Piece " + tomeNumber + ".pdf"
		#then if ok log + create create pdfs
		pdf = FPDF(unit = "pt")
		# imagelist is the list with all image filenames
		for chapter in chapters:
			dir = MainClass.MANGA_DIRECTORY + "/" + chapter
			self._log("add chapter {}".format(chapter))
			images = os.listdir(dir)
			images.sort()
			for image in images:
				imagePath = dir + "/" + image
				self._log("add image {} from chapter {}".format(image, dir), "DEBUG")
				im = Image.open(imagePath)
				w, h = im.size
				pdf.add_page(orientation = "P", format = (w, h), same = False)
				self.logger.printSameLine("*")
				pdf.image(imagePath, 0, 0)
			self.logger.printSameLine("",True)

		pdf.output(pdfName, "F")
		self._log("{} created".format(pdfName))

	def _getChapters(self, firstChapter = None):
		chapters = os.listdir(MainClass.MANGA_DIRECTORY)
		newChapters = [ int(x) for x in chapters ]
		newChapters.sort()
		chapters = [ str(x) for x in newChapters ]
		if firstChapter:
			#get the index
			index = 0
			found = False
			for chapter in chapters:
				if int(firstChapter) != int(chapter) and found == False:
					index = index + 1
				else:
					found = True
			chapters = chapters[index:]

		if len(chapters) > 9:
			tomeChapters = chapters[:10]
			tomeNumber = chapters[9][:-1]
			self._log("tome number {}".format(tomeNumber), "DEBUG")
			tmp = int(chapters[0])
			chapterAreReady = True
			for chapter in tomeChapters:
				if int(chapter) != tmp:
					chapterAreReady = False
					self._log("chapter {} missing for tome {}".format(chapter, tomeNumber), "ERROR")
				else:
					self._log("add chapter {} to tome {}".format(chapter, tomeNumber), "DEBUG")
				tmp = tmp + 1

			if chapterAreReady:
				return tomeNumber, tomeChapters
		else:
			self._log("unable to create new tome {}, not enough chapter".format(firstChapter), "ERROR")
		return None, None


	def _log(self, message, mode=""):
		if self.logger is not None:
			if mode == "ERROR":
				self.logger.error("{}".format(message))
			elif mode == "DEBUG":
				self.logger.debug("{}".format(message))
			else:
				self.logger.info("{}".format(message))


if __name__ == '__main__':

	#parser arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--verbose", action="store_true", help="print debug logs")

	args = parser.parse_args()

	Logger.getLogger().setMode( "DEBUG" if args.verbose else "INFO")
	MainClass().createPdf(args)
	Logger.getLogger().close()
