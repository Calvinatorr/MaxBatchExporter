import sys, importlib

# Append system path
sys.path += [ r"C:\Users\calvinsimpson\Documents\Git\MaxBatchExporter\MaxBatchExporter" ]

import MaxBatchExporter.UI
importlib.reload(MaxBatchExporter.UI)

MaxBatchExporter.UI.show()