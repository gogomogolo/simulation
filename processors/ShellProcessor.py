import util.LogUtil as LogUtil
import os
import parameters.Constants as Constants


def get_report():
    max_attempt = int(Constants.SIMULATION_LIFE_TIME_IN_SECONDS/Constants.SF_TO_SUPER_GROUP_PERIOD_IN_SEC[7])

    SucceededTransmittersShell = "grep \"<Attempt> : " + str(max_attempt) + "\" " + Constants.LOG_FILE_DIR + "/tasks.subtasks.GroupTransmissionObserver | grep -P \"<SuccessfulTransmittersAmount> : \d+\" -o | awk '{s+=$3}END{print s}'"
    FailedTransmittersShell = "grep \"<Attempt> : " + str(max_attempt) + "\" " + Constants.LOG_FILE_DIR + "/tasks.subtasks.GroupTransmissionObserver | grep -P \"<FailedTransmittersAmount> : \d+\" -o | awk '{s+=$3}END{print s}'"
    TotalDLTransmissionShell = "grep -P \"<DLMessageSizeByteWithStandardSolution> : [+-]?[0-9]+([.][0-9]+)?\" " + Constants.LOG_FILE_DIR + "/processors.Postprocessor -o | awk '$3!=0' | wc -l"
    TotalULTransmissionShell = "grep -P \"<TotalULTransmission> : \d+\" " + Constants.LOG_FILE_DIR + "/processors.Postprocessor -o | awk '{s+=$3}END{print s}'"
    TotalULMessageSizeByteShell = "grep -P \"<TotalULMessageSizeByte> : [+-]?[0-9]+([.][0-9]+)?\" " + Constants.LOG_FILE_DIR + "/processors.Postprocessor -o | awk '{s+=$3}END{print s}'"
    DLMessageSizeByteWithStandardSolutionShell = "grep -P \"<DLMessageSizeByteWithStandardSolution> : [+-]?[0-9]+([.][0-9]+)?\" " + Constants.LOG_FILE_DIR + "/processors.Postprocessor -o | awk '{s+=$3}END{print s}'"
    DLMessageSizeByteWithExpressionSolutionShell = "grep -P \"<DLMessageSizeByteWithExpressionSolution> : [+-]?[0-9]+([.][0-9]+)?\" " + Constants.LOG_FILE_DIR + "/processors.Postprocessor -o | awk '{s+=$3}END{print s}'"

    SucceededTransmitters = os.popen(SucceededTransmittersShell).read()
    FailedTransmitters = os.popen(FailedTransmittersShell).read()
    TotalDLTransmission = os.popen(TotalDLTransmissionShell).read()
    TotalULTransmission = os.popen(TotalULTransmissionShell).read()
    TotalULMessageSizeByte = os.popen(TotalULMessageSizeByteShell).read()
    DLMessageSizeByteWithStandardSolution = os.popen(DLMessageSizeByteWithStandardSolutionShell).read()
    DLMessageSizeByteWithExpressionSolution = os.popen(DLMessageSizeByteWithExpressionSolutionShell).read()

    LogUtil.get_file_logger(__name__).info(
        "| <SucceededTransmitters> : %s | <FailedTransmitters> : %s "
        "| <TotalULTransmissionCount> : %s | <TotalDLTransmissionCount> : %s "
        "| <TotalULMessageSize> : %s "
        "| <TotalDLMessageSizeWithStandardSolution> : %s | <TotalDLMessageSizeWithExpressionSolution> : %s |",
        str(SucceededTransmitters),
        str(FailedTransmitters),
        str(TotalULTransmission), str(TotalDLTransmission),
        str(TotalULMessageSizeByte),
        str(DLMessageSizeByteWithStandardSolution), str(DLMessageSizeByteWithExpressionSolution)
    )