import os
import json
import parameters.Constants as Constants


def get_report():
    TotalDLTransmissionShell = "grep -P \"<DLMessageSizeByteWithStandardSolution> : [+-]?[0-9]+([.][0-9]+)?\" " + Constants.LOG_FILE_DIR + "/processors.Postprocessor -o | awk '$3!=0' | wc -l"
    TotalULTransmissionShell = "grep -P \"<TotalULTransmission> : \d+\" " + Constants.LOG_FILE_DIR + "/processors.Postprocessor -o | awk '{s+=$3}END{print s}'"
    TotalULMessageSizeByteShell = "grep -P \"<TotalULMessageSizeByte> : [+-]?[0-9]+([.][0-9]+)?\" " + Constants.LOG_FILE_DIR + "/processors.Postprocessor -o | awk '{s+=$3}END{print s}'"
    DLMessageSizeByteWithStandardSolutionShell = "grep -P \"<DLMessageSizeByteWithStandardSolution> : [+-]?[0-9]+([.][0-9]+)?\" " + Constants.LOG_FILE_DIR + "/processors.Postprocessor -o | awk '{s+=$3}END{print s}'"
    DLMessageSizeByteWithExpressionSolutionShell = "grep -P \"<DLMessageSizeByteWithExpressionSolution> : [+-]?[0-9]+([.][0-9]+)?\" " + Constants.LOG_FILE_DIR + "/processors.Postprocessor -o | awk '{s+=$3}END{print s}'"

    TotalDLTransmission = os.popen(TotalDLTransmissionShell).read()
    TotalULTransmission = os.popen(TotalULTransmissionShell).read()
    TotalULMessageSizeByte = os.popen(TotalULMessageSizeByteShell).read()
    DLMessageSizeByteWithStandardSolution = os.popen(DLMessageSizeByteWithStandardSolutionShell).read()
    DLMessageSizeByteWithExpressionSolution = os.popen(DLMessageSizeByteWithExpressionSolutionShell).read()

    result_object = {}

    result_object['ULXmtCnt'] = str(TotalULTransmission.strip())
    result_object['DLAckCount'] = str(TotalDLTransmission.strip())
    result_object['ULMsgSz'] = str(TotalULMessageSizeByte.strip())
    result_object['DLAckSzWOExp'] = str(DLMessageSizeByteWithStandardSolution.strip())
    result_object['DLAckSzWExp'] = str(DLMessageSizeByteWithExpressionSolution.strip())

    _r_json = json.dumps(result_object)

    with open(Constants.LOG_FILE_DIR + "/ProposedSolutionTraffic", 'a') as the_file:
        the_file.write(_r_json)