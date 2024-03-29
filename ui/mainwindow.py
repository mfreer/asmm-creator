# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import datetime

import netCDF4


from PyQt4 import QtGui
from PyQt4.QtCore import QDate
from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QString
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import QCheckBox
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QInputDialog
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QListWidget
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QTextEdit



from Ui_mainwindow import Ui_MainWindow
from _version import _version
from _version import _xml_version


from asmm_xml import create_asmm_xml
from asmm_xml import read_asmm_xml

from mapnik_widget import MapnikWidget



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
        self.create_date = None



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
            title_string = "ASMM Creator V{0} - ".format(_version) + self.out_file_name
        else:
            title_string = "ASMM Creator V{0} - Unsaved".format(_version)

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
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix('xml')
        out_file_name = unicode(file_dialog.getSaveFileName(self, "Save XML File", filter='XML Files (*.xml);;Text Files (*.txt)'))

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
        self.create_date = None
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
        out_file_name = unicode(out_file_name)
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
            item_list.append(new_item)
            listWidget.addItem(new_item)
            self.make_window_title()



    def removeListItem(self, listWidget, item_list):

        selected_line = listWidget.currentRow()
        if selected_line >= 0:
            selected_item = listWidget.currentItem()
            item_list.remove(unicode(selected_item.text()))
            listWidget.takeItem(selected_line)
            self.modified = True
            self.make_window_title()

    @pyqtSignature("")
    def on_actionASMM_CreatorAbout_triggered(self):
        """
        Slot documentation goes here.
        """

        aboutBox = QMessageBox()
        aboutBox.about(self, "About ASMM Metadata Creator",
                       "The ASMM Metadata Creator V{0} was developed by EUFAR using Python and PyQT. XML files generated by this version conform to V{1} of the ASMM XML standard. <br> <br>".format(_version, _xml_version) +
                       "For more information, or to submit a bug report, please contact <a href='mailto:eufarsp@eufar.net'>eufarsp@eufar.net</a> <br><br>" +
                       "The latest version and source code of the ASMM metadata creator can be found at <a href=http://asmm-creator.googlecode.com>http://asmm-creator.googlecode.com</a>")

    @pyqtSignature("")
    def on_readBoundingBoxButton_clicked(self):
        """
        Launches function allowing user to automatically populate geographic
        bounding box information from a NetCDF file. If NetCDF has global attributes
        geospatial_lat_max, geospatial_lat_min, geospatial_lon_max, geospatial_lon_min,
        geospatial_alt_max or geospatial_alt_min, then these are used to populate
        information. Otherwise, user is prompted to select correct fields from 
        NetCDF file.
        """

        lat_min = None
        lat_max = None
        lon_min = None
        lon_max = None
        alt_min = None
        alt_max = None


        filename = QFileDialog.getOpenFileName(self,
                                               'Open associated NetCDF',
                                               '',
                                               'NetCDF files (*.nc *.cdf);;All Files (*.*)')

        f = netCDF4.Dataset(str(filename))


        var_list = f.variables.keys()
        var_list.sort()

        try:

            lat_min = f.__dict__['geospatial_lat_min']
            lat_max = f.__dict__['geospatial_lat_max']
        except KeyError:
            [var_name, ok] = QInputDialog.getItem(self, "Latitude Variable Name", "ERROR: Latitude values not found. Please enter latitude variable name.", var_list, current=0, editable=False)
            if var_name and ok:
                lat_values = f.variables[str(var_name)][:]
                lat_min = min(lat_values[lat_values != 0])
                lat_max = max(lat_values[lat_values != 0])

                lat_values = f.variables[str(var_name)][:]

        try:

            lon_min = f.__dict__['geospatial_lon_min']
            lon_max = f.__dict__['geospatial_lon_max']
        except KeyError:
            [var_name, ok] = QInputDialog.getItem(self, "Longitude Variable Name", "ERROR: Longitude values not found. Please select longitude variable name.", var_list, current=0, editable=False)
            if var_name and ok:
                lon_values = f.variables[str(var_name)][:]
                lon_min = min(lon_values[lon_values != 0])
                lon_max = max(lon_values[lon_values != 0])

        try:

            alt_min = f.__dict__['geospatial_vertical_min']
            alt_max = f.__dict__['geospatial_vertical_max']
        except KeyError:
            [var_name, ok] = QInputDialog.getItem(self, "Altitude Variable Name", "ERROR: Altitude values not found. Please enter altitude variable name.", var_list, current=0, editable=False)
            if var_name and ok:
                alt_values = f.variables[str(var_name)][:]
                alt_min = min(alt_values[alt_values != 0])
                alt_max = max(alt_values[alt_values != 0])

        if lon_min:
            self.westBoundLongitudeLine.setText(str(lon_min))

        if lon_max:
            self.eastBoundLongitudeLine.setText(str(lon_max))

        if lat_max:
            self.northBoundLatitudeLine.setText(str(lat_max))

        if lat_min:
            self.southBoundLatitudeLine.setText(str(lat_min))

        if alt_min:
            self.minAltitudeLine.setText(str(alt_min))

        if alt_max:
            self.maxAltitudeLine.setText(str(alt_max))

    @pyqtSignature("")
    def on_actionLicense_triggered(self):
        """
        Shows license text for ASMM creator. 
        """

        f = open('LICENSE.txt')

        license_data = f.read()

        f.close()


        aboutBox = QMessageBox()
        aboutBox.about(self, "About ASMM Metadata Creator", license_data)

    @pyqtSignature("")
    def on_testMapButton_clicked(self):
        """
        Slot documentation goes here.
        """

        map_widget = MapnikWidget(self)

        map_widget.open('population.xml')
