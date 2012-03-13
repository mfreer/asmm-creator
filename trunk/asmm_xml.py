'''
Created on Mar 8, 2012

@author: freer
'''

NAMESPACE_URI = 'http://www.eufar.net/ASMM'

import xml.dom.minidom
import xml.dom.ext

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QDate


def create_asmm_xml(self, out_file_name):
    doc = xml.dom.minidom.Document()

    doc_root = add_element(doc, "MissionMetadata", doc)


    ############################
    # Flight Information
    ############################
    flightInformation = add_element(doc, "FlightInformation", doc_root)

    add_element(doc, "FlightNumber", flightInformation, self.flightNumberLine.text())
    add_element(doc, "Date", flightInformation, self.dateLine.date().toString(Qt.ISODate))
    add_element(doc, "Campaign", flightInformation, self.campaignLine.text())
    add_element(doc, "MissionScientist", flightInformation, self.missionSciLine.text())
    add_element(doc, "FlightManager", flightInformation, self.flightManagerLine.text())
    add_element(doc, "Platform", flightInformation, self.platformLine.text())
    add_element(doc, "Operator", flightInformation, self.operatorLine.text())
    add_element(doc, "Country", flightInformation, self.countryLine.text())

    ###########################
    # Metadata Contact Info
    ###########################
    contactInfo = add_element(doc, "ContactInfo", doc_root)

    add_element(doc, "ContactName", contactInfo, self.contactNameLine.text())
    add_element(doc, "ContactRole", contactInfo, self.contactRoleBox.currentText())
    add_element(doc, "ContactEmail", contactInfo, self.contactEmailLine.text())

    ############################
    # Scientific Aims
    ############################
    scientificAims = add_element(doc, "ScientificAims", doc_root)

    add_check_elements(doc, self.scientific_aims_check_dict, "SA_Code", scientificAims)

    add_comment_element(doc , "SA_Other", scientificAims, self.SAOtherTextBox.toPlainText())

    ############################
    # Geographical Region
    ############################
    geographicalRegion = add_element(doc, "GeographicalRegion", doc_root)

    add_check_elements(doc, self.geographical_region_check_dict, "GR_Code", geographicalRegion)

    add_comment_element(doc, "GR_other", geographicalRegion, self.GROtherTextBox.toPlainText())

    ############################
    # Atmospheric Features
    ############################
    atmosphericFeatures = add_element(doc, "AtmosFeatures", doc_root)

    add_check_elements(doc, self.atmospheric_features_check_dict, "AF_Code", atmosphericFeatures)

    add_comment_element(doc, "AF_Other", atmosphericFeatures, self.AFOtherTextBox.toPlainText())

    ############################
    # Cloud Types
    ############################
    cloudTypes = add_element(doc, "CloudTypes", doc_root)

    add_check_elements(doc, self.cloud_types_check_dict, "CT_Code", cloudTypes)

    add_comment_element(doc, "CT_Other", cloudTypes, self.CTOtherTextBox.toPlainText())

    ############################
    # Particles Sampled
    ############################
    particlesSampled = add_element(doc, "ParticlesSampled", doc_root)

    add_check_elements(doc, self.particles_sampled_check_dict, "PS_Code", particlesSampled)

    add_comment_element(doc, "PS_Other", particlesSampled, self.PSOtherTextBox.toPlainText())

    ############################
    # Surfaces Overflown
    ############################
    surfacesOverflown = add_element(doc, "SurfacesOverflown", doc_root)

    add_check_elements(doc, self.surfaces_overflown_check_dict, "SO_Code", surfacesOverflown)

    add_comment_element(doc, "SO_Other", surfacesOverflown, self.SOOtherTextBox.toPlainText())

    ############################
    # Altitude Ranges
    ############################
    altitudeRanges = add_element(doc, "AltitudeRanges", doc_root)

    add_check_elements(doc, self.altitude_ranges_check_dict, "AR_Code", altitudeRanges)

    add_comment_element(doc, "AR_Other", altitudeRanges, self.AROtherTextBox.toPlainText())

    ############################
    # Flight Types
    ############################
    flightTypes = add_element(doc, "FlightTypes", doc_root)

    add_check_elements(doc, self.flight_types_check_dict, "FT_Code", flightTypes)

    add_comment_element(doc, "FT_Other", flightTypes, self.FTOtherTextBox.toPlainText())

    ############################
    # Satellite coordination
    ############################
    satelliteCoordination = add_element(doc, "SatelliteCoordination", doc_root)

    add_check_elements(doc, self.satellite_coordination_check_dict, "SC_Code", satelliteCoordination)

    add_comment_element(doc, "SC_Other", satelliteCoordination, self.SCOtherTextBox.toPlainText())

    ############################
    # Surface Observations
    ############################
    surfaceObs = add_element(doc, "SurfaceObs", doc_root)

    for item in self.ground_site_list:
        add_element(doc, "GroundSite", surfaceObs, item)

    for item in self.research_vessel_list:
        add_element(doc, "ResearchVessel", surfaceObs, item)

    for item in self.arm_site_list:
        add_element(doc, "ArmSite", surfaceObs, item)

    for item in self.arm_mobile_list:
        add_element(doc, "ArmMobile", surfaceObs, item)

    ############################
    # Other Comments
    ############################
    if self.OtherCommentsTextBox.toPlainText():
        add_element(doc, "OtherComments", doc_root, self.OtherCommentsTextBox.toPlainText())


    #xml.dom.ext.PrettyPrint(doc)
    f = open(out_file_name, 'w')
    xml.dom.ext.PrettyPrint(doc, f)
    f.close()

    self.saved = True
    self.modified = False


def read_asmm_xml(self, in_file_name):

    f = open(in_file_name, 'r')
    doc = xml.dom.minidom.parse(f)

    ############################
    # Flight Information
    ############################

    flightInformation = get_element(doc, "FlightInformation")

    set_text_value(self.flightNumberLine, flightInformation, "FlightNumber")
    date = get_element_value(flightInformation, "Date")
    self.dateLine.setDate(QDate.fromString(date, Qt.ISODate))
    set_text_value(self.campaignLine, flightInformation, "Campaign")
    set_text_value(self.missionSciLine, flightInformation, "MissionScientist")
    set_text_value(self.flightManagerLine, flightInformation, "FlightManager")
    set_text_value(self.platformLine, flightInformation, "Platform")
    set_text_value(self.operatorLine, flightInformation, "Operator")
    set_text_value(self.countryLine, flightInformation, "Country")

    #############################
    # Metadata Contact Info
    #############################

    contactInfo = get_element(doc, "ContactInfo")

    set_text_value(self.contactNameLine, contactInfo, "ContactName")
    set_text_value(self.contactEmailLine, contactInfo, "ContactEmail")
    combo_text = get_element_value(contactInfo, "ContactRole")
    self.contactRoleBox.setCurrentIndex(self.contactRoleBox.findText(combo_text))

    #############################
    # Scientific Aims
    #############################

    scientificAims = get_element(doc, "ScientificAims")

    set_check_values(self.scientific_aims_check_dict, scientificAims, "SA_Code")
    set_text_value(self.SAOtherTextBox, scientificAims, "SA_Other")

    #############################
    # Geographical Region
    #############################

    geographicalRegion = get_element(doc, "GeographicalRegion")

    set_check_values(self.geographical_region_check_dict, geographicalRegion, "GR_Code")
    set_text_value(self.GROtherTextBox, geographicalRegion, "GR_Other")

    #############################
    # Atmospheric Features
    #############################

    atmosphericFeatures = get_element(doc, "AtmosFeatures")

    set_check_values(self.atmospheric_features_check_dict, atmosphericFeatures, "AF_Code")
    set_text_value(self.AFOtherTextBox, atmosphericFeatures, "AF_Other")

    #############################
    # Cloud Types
    #############################

    cloudTypes = get_element(doc, "CloudTypes")

    set_check_values(self.cloud_types_check_dict, cloudTypes, "CT_Code")
    set_text_value(self.CTOtherTextBox, cloudTypes, "CT_Other")

    #############################
    # Particles Sampled
    #############################

    particlesSampled = get_element(doc, "ParticlesSampled")

    set_check_values(self.particles_sampled_check_dict, particlesSampled, "PS_Code")
    set_text_value(self.PSOtherTextBox, particlesSampled, "PS_Other")

    #############################
    # Surfaces Overflown
    #############################

    surfacesOverflown = get_element(doc, "SurfacesOverflown")

    set_check_values(self.surfaces_overflown_check_dict, surfacesOverflown, "SO_Code")
    set_text_value(self.SOOtherTextBox, surfacesOverflown, "SO_Other")

    #############################
    # Altitude Ranges
    #############################

    altitudeRanges = get_element(doc, "AltitudeRanges")

    set_check_values(self.altitude_ranges_check_dict, altitudeRanges, "AR_Code")
    set_text_value(self.AROtherTextBox, altitudeRanges, "AR_Other")

    #############################
    # Flight Types
    #############################

    flightTypes = get_element(doc, "FlightTypes")

    set_check_values(self.flight_types_check_dict, flightTypes, "FT_Code")
    set_text_value(self.FTOtherTextBox, flightTypes, "FT_Other")

    #############################
    # Satellite Coordination
    #############################

    satelliteCoordination = get_element(doc, "SatelliteCoordination")

    set_check_values(self.satellite_coordination_check_dict, satelliteCoordination, "SC_Code")
    set_text_value(self.SCOtherTextBox, satelliteCoordination, "SC_Other")

    #############################
    # Surface Observations
    #############################

    surfaceObservations = get_element(doc, "SurfaceObs")

    self.ground_site_list = get_element_values(surfaceObservations, "GroundSite")
    self.groundListWidget.addItems(self.ground_site_list)

    self.research_vessel_list = get_element_values(surfaceObservations, "ResearchVessel")
    self.vesselListWidget.addItems(self.research_vessel_list)

    self.arm_site_list = get_element_values(surfaceObservations, "ArmSite")
    self.armListWidget.addItems(self.arm_site_list)

    self.arm_mobile_list = get_element_values(surfaceObservations, "ArmMobile")
    self.armMobileListWidget.addItems(self.arm_mobile_list)

    ##############################
    # Other Comments
    ##############################

    set_text_value(self.OtherCommentsTextBox, doc, "OtherComments")


def get_element(parent, element_name):

    return parent.getElementsByTagNameNS(NAMESPACE_URI, element_name)[0]

def get_element_value(parent, element_name):

    elements = parent.getElementsByTagNameNS(NAMESPACE_URI, element_name)
    if elements:
        element = elements[0]

        nodes = element.childNodes
        for node in nodes:
            if node.nodeType == node.TEXT_NODE:
                return node.data

def get_element_values(parent, element_name):

    value_list = []

    elements = parent.getElementsByTagNameNS(NAMESPACE_URI, element_name)
    for element in elements:
        value_list.append(element.childNodes[0].data)

    return value_list

def set_check_values(check_dict, parent, element_name):

    elements = parent.getElementsByTagNameNS(NAMESPACE_URI, element_name)
    for element in elements:

        check_widget = find_key(check_dict, element.childNodes[0].data)
        check_widget.setChecked(True)



def set_text_value(text_widget, parent, element_name):

    node_data = get_element_value(parent, element_name)
    if node_data:
        text_widget.setText(node_data)


def add_element(doc, element_name, parent, value=None):
    new_element = doc.createElementNS(NAMESPACE_URI, "asmm:" + element_name)
    if value:
        new_text = doc.createTextNode(str(value))
        new_element.appendChild(new_text)

    parent.appendChild(new_element)

    return new_element

def add_comment_element(doc, element_name, parent, value):
    if value:
        add_element(doc, element_name, parent, value)

def add_check_elements(doc, check_dict, code_name, parent):

    for key, val in check_dict.iteritems():
        if key.isChecked():
            add_element(doc, code_name, parent, val)

def find_key(dic, val):
    return [k for k, v in dic.iteritems() if v == val][0]
