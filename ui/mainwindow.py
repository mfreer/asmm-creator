# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
from PyQt4 import QtGui
from PyQt4.QtCore import QDate
from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QPoint
from PyQt4.QtCore import QString
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import QCalendarWidget
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QInputDialog
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QListWidgetItem
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QTextEdit
from PyQt4.QtGui import QWidget



from Ui_mainwindow import Ui_MainWindow

from asmm_xml import create_asmm_xml
from asmm_xml import read_asmm_xml

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.ground_site_list = []
        self.research_vessel_list = []
        self.arm_site_list = []
        self.arm_mobile_list = []
        self.dateLine.setDate(QDate.currentDate())

        self.out_file_name = None
        self.saved = False
        self.modified = False



        all_check_boxes = self.findChildren(QCheckBox)
        for check_box in all_check_boxes:
            QObject.connect(check_box, SIGNAL("stateChanged(int)"), self.set_modified)

        all_text_edits = self.findChildren(QTextEdit)
        for widget in all_text_edits:
            QObject.connect(widget, SIGNAL("textChanged()"), self.set_modified)

        all_line_edits = self.findChildren(QLineEdit)
        for widget in all_line_edits:
            QObject.connect(widget, SIGNAL("textChanged(QString)"), self.set_modified)

        QObject.connect(self.dateLine, SIGNAL("dateChanged(QDate)"), self.set_modified)

        self.make_window_title()


        self.scientific_aims_check_dict = {self.satelliteCalValCheck:'satelliteCalVal',
                                          self.aerosolCheck:'aerosol',
                                          self.aerosolRadiativeCheck:'aerosolRadiative',
                                          self.aerosolMicrophysicalCheck:'aerosolMicrophysical',
                                          self.anthroPollutionCheck:'anthroPollution',
                                          self.mesoscaleImpactsCheck:'mesoscaleImpacts',
                                          self.cloudMicrophysicsCheck:'cloudMicrophysics',
                                          self.cloudDynamicsCheck:'cloudDynamics',
                                          self.cloudRadiativeCheck:'cloudRadiative',
                                          self.cloudConvectionCheck:'cloudConvection',
                                          self.blCloudCheck:'blCloud',
                                          self.blDynamicsCheck:'blDynamics',
                                          self.radiationCheck:'radiation',
                                          self.radiationAtmosSpectroscopyCheck:'radiationAtmosSpectroscopy',
                                          self.radiationOtherCheck:'radiationOther',
                                          self.gasChemCheck:'gasChem',
                                          self.gasChemOrganicsCheck:'gasChemOrganics',
                                          self.gasChemOxidantsCheck:'gasChemOxidants',
                                          self.gasChemOtherCheck:'gasChemOther'
                                          }

        self.geographical_region_check_dict = {self.polarCheck:'polar',
                                              self.midLatitudesCheck:'midLatitudes',
                                              self.subTropicalCheck:'subTropical',
                                              self.tropicalCheck:'tropical',
                                              self.maritimeCheck:'maritime',
                                              self.continentalCheck:'continental',
                                              self.oceanicIslandsCheck:'oceanicIslands',
                                              self.geogOtherCheck:'other'}

        self.atmospheric_features_check_dict = {self.stationaryCheck:'stationary',
                                                self.stationaryAnticyclonicCheck:'stationaryAnticyclonic',
                                                self.stationaryCyclonicCheck:'stationaryCyclonic',
                                                self.warmFrontCheck:'warmFront',
                                                self.warmConveyorBeltCheck:'warmConveyorBelt',
                                                self.coldFrontCheck:'coldFront',
                                                self.occludedFrontCheck:'occludedFront',
                                                self.warmSectorCheck:'warmSector',
                                                self.postColdFrontalAirMassCheck:'postColdFrontalAirMass',
                                                self.arcticColdAirOutbreakCheck:'arcticColdAirOutbreak',
                                                self.orographicInfluenceCheck:'orographicInfluence',
                                                self.seaBreezeFrontCheck:'seaBreezeFront',
                                                self.stratosphericFoldCheck:'stratosphericFold',
                                                self.extendedConvergenceLineCheck:'extendedConvergenceLine',
                                                self.easterlyWaveCheck:'easterlyWave',
                                                self.equatorialWaveCheck:'equatorialWave',
                                                self.tropicalCycloneCheck:'tropycalCyclone',
                                                self.mesoscaleOrganizedConvectionCheck:'mesoscaleOrganizedConvection'}

        self.cloud_types_check_dict = {self.waterCloudsCheck:'waterClouds',
                                       self.mixedPhaseCloudsCheck:'mixedPhaseClouds',
                                       self.iceCloudsCheck:'iceClouds',
                                       self.cirrusCheck:'cirrus',
                                       self.contrailsCheck:'contrails',
                                       self.stratocumulusCheck:'stratocumulus',
                                       self.shallowCumulusCheck:'shallowCumulus',
                                       self.cumulusCongestusCheck:'cumulusCongestus',
                                       self.cumulonimbusToweringCumulusCheck:'cumulonimbusToweringCumulus',
                                       self.altostratusAltocumulusCheck:'altostratusAltocumulus',
                                       self.waveCloudsCheck:'waveClouds',
                                       self.deepFrontalStratiformCloudsCheck:'deepFrontalStratiformClouds',
                                       self.cloudFreeAboveAircraftCheck:'cloudFreeAboveAircraft',
                                       self.cloudFreeBelowAircraftCheck:'cloudFreeBelowAircraft'}

        self.particles_sampled_check_dict = {self.rainCheck:'rain',
                                             self.drizzleCheck:'drizzle',
                                             self.dropletsCheck:'droplets',
                                             self.pristineIceCrystalsCheck:'pristineIceCrystals',
                                             self.snowOrAggregatesCheck:'snowOrAggregates',
                                             self.graupelOrHailCheck:'graupelOrHail',
                                             self.seaSaltAerosolCheck:'seaSaltAerosol',
                                             self.continentalAerosolCheck:'continentalAerosol',
                                             self.urbanPlumeCheck:'urbanPlume',
                                             self.biomassBurningCheck:'biomassBurning',
                                             self.desertOrMineralDustCheck:'desertOrMineralDust',
                                             self.volcanicAshCheck:'volcanicAsh'}

        self.surfaces_overflown_check_dict = {self.oceanCheck:'ocean',
                                              self.semiAridCheck:'semiArid',
                                              self.seaIceCheck:'seaIce',
                                              self.desertCheck:'desert',
                                              self.snowCheck:'snow',
                                              self.urbanCheck:'urban',
                                              self.lakeIceCheck:'lakeIce',
                                              self.mountainousCheck:'mountainous',
                                              self.vegetationCheck:'vegetation',
                                              self.hillyCheck:'hilly',
                                              self.forestCheck:'forest',
                                              self.flatCheck:'flat'}

        self.altitude_ranges_check_dict = {self.boundaryLayerCheck:'boundaryLayer',
                                           self.blNearSurfaceCheck:'blNearSurface',
                                           self.blSubCloudCheck:'blSubCloud',
                                           self.blInCloudCheck:'blInCloud',
                                           self.lowerTroposphereCheck:'lowerTroposphere',
                                           self.midTroposphereCheck:'midTroposphere',
                                           self.upperTroposphereCheck:'upperTroposphere',
                                           self.lowerStratosphereCheck:'lowerStratosphere'}

        self.flight_types_check_dict = {self.straightLevelRunsCheck:'straightLevelRuns',
                                        self.stackedStraightLevelRunsCheck:'stackedStraightLevelRuns',
                                        self.separatedStraightLevelRuns:'separatedStraightLevelRuns',
                                        self.racetracksCheck:'racetracks',
                                        self.orbitsCheck:'orbits',
                                        self.lagrangianDescentsCheck:'lagrangianDescents',
                                        self.deepProfileAscentDescentsCheck:'deepProfileAscentDescents',
                                        self.dropsondeDeployedCheck:'dropsondeDeployed',
                                        self.selfCalibrationCheck:'selfCalibration'}

        self.satellite_coordination_check_dict = {self.polarMetopCheck:'polarMetop',
                                                  self.polarNpoessCheck:'polarNpoess',
                                                  self.polarAtrainCheck:'polarAtrain',
                                                  self.polarOtherCheck:'polarOther',
                                                  self.geosynchMsgCheck:'geosynchMsg',
                                                  self.geosynchOtherCheck:'geosynchOther',
                                                  self.modisCheck:'modis',
                                                  self.cloudsatCheck:'cloudsat',
                                                  self.caliopCheck:'caliop',
                                                  self.iasiCheck:'iasi',
                                                  self.airsCheck:'airs',
                                                  self.crisCheck:'cris',
                                                  self.amsuMhsCheck:'amsuMhs'}


    @pyqtSignature("")
    def on_groundAddButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.addListItem("Add Ground Site", "Ground Site Name:",
                    self.groundListWidget, self.ground_site_list)

    @pyqtSignature("")
    def on_groundRemoveButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.removeListItem(self.groundListWidget, self.ground_site_list)

    @pyqtSignature("")
    def on_armAddButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.addListItem("Add ARM Site", "ARM Site Name:",
                    self.armListWidget, self.arm_site_list)

    @pyqtSignature("")
    def on_armRemoveButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.removeListItem(self.armListWidget, self.arm_site_list)

    @pyqtSignature("")
    def on_armMobileAddButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.addListItem("Add ARM Mobile Site", "ARM Mobile Site Name:",
                    self.armMobileListWidget, self.arm_mobile_list)

    @pyqtSignature("")
    def on_armMobileRemoveButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.removeListItem(self.armMobileListWidget, self.arm_mobile_list)

    @pyqtSignature("")
    def on_vesselAddButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.addListItem("Add Research Vessel", "Research Vessel Name:",
                    self.vesselListWidget, self.research_vessel_list)

    @pyqtSignature("")
    def on_vesselRemoveButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.removeListItem(self.vesselListWidget, self.research_vessel_list)

    @pyqtSignature("QModelIndex")
    def on_groundListWidget_doubleClicked(self, index):
        """
        Slot documentation goes here.
        """
        self.addListItem("Add Ground Site", "Ground Site Name:",
                    self.groundListWidget, self.ground_site_list)

    @pyqtSignature("QModelIndex")
    def on_armListWidget_doubleClicked(self, index):
        """
        Slot documentation goes here.
        """
        self.addListItem("Add ARM Site", "ARM Site Name:",
            self.armListWidget, self.arm_site_list)



    @pyqtSignature("QModelIndex")
    def on_armMobileListWidget_doubleClicked(self, index):
        """
        Slot documentation goes here.
        """
        self.addListItem("Add ARM Mobile Site", "ARM Mobile Site Name:",
            self.armMobileListWidget, self.arm_mobile_list)

    @pyqtSignature("QModelIndex")
    def on_vesselListWidget_doubleClicked(self, index):
        """
        Slot documentation goes here.
        """
        self.addListItem("Add Research Vessel", "Research Vessel Name:",
                         self.vesselListWidget, self.research_vessel_list)


    @pyqtSignature("")
    def on_generateXMLButton_clicked(self):
        """
        Slot documentation goes here.
        """

        self.save_document()


    @pyqtSignature("")
    def on_actionNew_triggered(self):
        """
        Slot documentation goes here.
        """
        if self.modified:
            result = self.make_onsave_msg_box()

            if result == QMessageBox.Save:
                self.save_document()
                if self.modified:
                    return
                else:
                    self.reset_all_fields()
            elif result == QMessageBox.Discard:
                self.reset_all_fields()
                return
            else:
                return

        self.reset_all_fields()


    @pyqtSignature("")
    def on_actionSave_triggered(self):
        """
        Slot documentation goes here.
        """
        self.save_document()

    @pyqtSignature("")
    def on_actionSave_As_triggered(self):
        """
        Slot documentation goes here.
        """

        self.save_document(save_as=True)

    @pyqtSignature("")
    def on_actionOpen_triggered(self):
        """
        Slot documentation goes here.
        """
        if self.modified:
            result = self.make_onsave_msg_box()

            if result == QMessageBox.Save:
                self.save_document()
                if self.modified:
                    return
                else:
                    self.reset_all_fields()
                    self.open_file()
                    return
            elif result == QMessageBox.Discard:
                self.reset_all_fields()
                self.open_file()
                return
            else:
                return

        self.reset_all_fields()
        self.open_file()



    @pyqtSignature("")
    def on_actionExit_triggered(self):
        """
        Slot documentation goes here.
        """
        self.close()

    def closeEvent(self, event):
        if self.modified:
            result = self.make_onsave_msg_box()

            if result == QMessageBox.Save:
                self.save_document()
                if self.modified:
                    event.ignore()
                else:
                    event.accept()
            elif result == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            self.close()

    def make_window_title(self):
        if self.saved:
            title_string = "ASMM Creator - " + self.out_file_name
        else:
            title_string = "ASMM Creator - Unsaved"

        if self.modified:
            title_string += '*'

        self.setWindowTitle(title_string)


    def set_modified(self):
        if not self.modified:
            self.modified = True
            self.make_window_title()

    def save_document(self, save_as=False):


        if not self.out_file_name or save_as:
            out_file_name = self.get_file_name()

            if out_file_name:
                create_asmm_xml(self, out_file_name)
                self.out_file_name = out_file_name
        else:
            create_asmm_xml(self, self.out_file_name)

        self.make_window_title()

    def get_file_name(self):
        out_file_name = QFileDialog.getSaveFileName(self, "Save XML File")
        return out_file_name

    def reset_all_fields(self):

        all_check_boxes = self.findChildren(QCheckBox)
        for check_box in all_check_boxes:
            check_box.setCheckState(False)

        all_text_edits = self.findChildren(QTextEdit)
        for widget in all_text_edits:
            widget.clear()

        all_line_edits = self.findChildren(QLineEdit)
        for widget in all_line_edits:
            widget.clear()

        all_list_widgets = self.findChildren(QListWidget)
        for widget in all_list_widgets:
            widget.clear()

        self.ground_site_list = []
        self.research_vessel_list = []
        self.arm_site_list = []
        self.arm_mobile_list = []
        self.dateLine.setDate(QDate.currentDate())

        self.out_file_name = None


        self.modified = False
        self.saved = False
        self.make_window_title()

    def make_onsave_msg_box(self):
        msgBox = QMessageBox()
        msgBox.setText("The document has been modified.")
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Save)
        msgBox.setIcon(QMessageBox.Warning)

        screen_center = QtGui.QDesktopWidget().availableGeometry().center()
        msgBox.move(screen_center)
        result = msgBox.exec_()

        return result

    def open_file(self):
        (out_file_name, filter) = QFileDialog.getOpenFileNameAndFilter(self, "Open XML File", filter="XML Files (*.xml)")

        if out_file_name:
            read_asmm_xml(self, out_file_name)

            self.saved = True
            self.modified = False
            self.out_file_name = out_file_name
            self.make_window_title()



    def addListItem(self, title, label, listWidget, item_list):
        (new_item, response) = QInputDialog.getText(self, title, label, text=QString(),)

        if new_item and response:
            self.modified = True
            self.saved = False
            item_list.append(new_item)
            listWidget.addItem(new_item)



    def removeListItem(self, listWidget, item_list):

        selected_line = listWidget.currentRow()

        if selected_line >= 0:
            selected_item = listWidget.currentItem()
            item_list.remove(selected_item.text())
            listWidget.takeItem(selected_line)

    @pyqtSignature("")
    def on_actionASMM_CreatorAbout_triggered(self):
        """
        Slot documentation goes here.
        """

        aboutBox = QMessageBox()
        aboutBox.about(self, "About ASMM Metadata Creator",
                       "The ASMM Metadata Creator was developed by EUFAR using Python and PyQT. <br> <br>" +
                       "For more information, or to submit a bug report, please contact <a href='mailto:eufarsp@eufar.net'>eufarsp@eufar.net</a> <br><br>" +
                       "The latest version and source code of the ASMM metadata creator can be found at <a href=http://asmm-creator.googlecode.com>http://asmm-creator.googlecode.com</a>")

