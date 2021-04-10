macroScript MaxBatchExporter
category: "Custom"
tooltip: "Max Batch Exporter"
(
    userScriptsDir = GetDir #userScripts
    scriptDir = userScriptsDir + "\MaxBatchExporter\UI.py"
    Python.Executefile scriptDir
)