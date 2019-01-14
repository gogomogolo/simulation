from results.conversionlogic.FileToGroupAnalysis import FileToGroupAnalysis
from results.converter.ObjectConverter import ObjectConverter
from results.reader.FileReader import FileReader


def get_group_analysis(path):
    group_details_reader = FileReader(path)
    file_to_group_analysis_logic = FileToGroupAnalysis()

    file_to_group_analysis_converter = ObjectConverter(group_details_reader, file_to_group_analysis_logic)

def get_super_grou_analysis():