from ij import IJ
from ij.plugin.frame import RoiManager
from ij.gui import PolygonRoi
from ij.gui import Roi
from java.awt import FileDialog
from ij.io import DirectoryChooser

src_dir = DirectoryChooser("Select Folder").getDirectory()
folder = src_dir.getDirectory()

