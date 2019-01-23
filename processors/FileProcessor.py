from results.conversionlogic.FileToGroupPayloadAnalysis import FileToGroupPayloadAnalysis
from results.conversionlogic.FileToGroupTransmissionAnalysis import FileToGroupTransmissionAnalysis
from results.conversionlogic.FileToSuperGroupAnalysis import FileToSuperGroupAnalysis
from results.converter.ObjectConverter import ObjectConverter
from results.reader.FileReader import FileReader
import parameters.Constants as Constants
import math
import os


def get_group_payload_analysis(super_group_analysis):
    path = os.path.abspath(os.path.join(Constants.LOG_FILE_DIR, 'processors.Postprocessor'))
    group_details_reader = FileReader(path)
    sf_group_id = {}

    for analysis in super_group_analysis:
        sf = getattr(analysis, "sf")
        group_number = getattr(analysis, "group_number")
        group_ids = []
        for i in range(0, group_number):
            group_id = __get_bit_format(i, group_number)
            group_ids.append(group_id)

        sf_group_id[sf] = group_ids

    file_to_group_payload_analysis_logic = FileToGroupPayloadAnalysis(sf_group_id)
    file_to_group_payload_analysis_converter = ObjectConverter(group_details_reader,
                                                               file_to_group_payload_analysis_logic)

    return file_to_group_payload_analysis_converter.convert()


def get_group_analysis(super_group_analysis):
    path = os.path.abspath(os.path.join(Constants.LOG_FILE_DIR, 'tasks.subtasks.GroupTransmissionObserver'))
    group_details_reader = FileReader(path)
    group_analysis = {}

    for analysis in super_group_analysis:
        sf = getattr(analysis, "sf")
        group_number = getattr(analysis, "group_number")
        analysis = []
        for i in range(0, group_number):
            group_id = __get_bit_format(i, group_number)
            file_to_group_analysis_logic = FileToGroupTransmissionAnalysis(sf, group_id)
            file_to_group_analysis_converter = ObjectConverter(group_details_reader, file_to_group_analysis_logic)
            analysis.append(file_to_group_analysis_converter.convert())

        group_analysis[sf] = analysis

    return group_analysis


def get_super_group_analysis():
    path = os.path.abspath(os.path.join(Constants.LOG_FILE_DIR, 'generators.SuperGroupGenerator'))
    super_group_details_reader = FileReader(path)
    min_sf = Constants.MIN_SF
    max_sf = Constants.MAX_SF
    super_group_analysis = []
    for sf in range(min_sf, max_sf+1):
        file_to_super_group_analysis_logic = FileToSuperGroupAnalysis(sf)
        file_to_group_analysis_converter = \
            ObjectConverter(super_group_details_reader, file_to_super_group_analysis_logic)
        super_group_analysis.append(file_to_group_analysis_converter.convert())
    return super_group_analysis


def __get_bit_format(_id, max_id):
    _id_length = int(math.log(max_id, 2))
    _id_bit_notation = '0'+str(_id_length)+'b'
    return format(_id, _id_bit_notation)
