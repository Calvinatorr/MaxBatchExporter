-- Define macroscript to open our UI
macroScript OpenExportUI
category: "MaxBatchExporter"
tooltip: "Open Max Batch Exporter UI"
(
    userScriptsDir = GetDir #userScripts
    scriptDir = userScriptsDir + "\MaxBatchExporter\UI.py"
    Python.Executefile scriptDir
)

function initMenuBar = (
	-- Get main menu bar
	local mainMenuBar = menuMan.getMainMenuBar()

	-- Create new menu
	local menuName = "Max Batch Exporter"
	local subMenu = menuMan.findMenu menuName
	if (menu != undefined) do
	(
		menuMan.unRegisterMenu maxBatchExporterMenu
	)
	subMenu = menuMan.createMenu menuName

	-- Seperator
	local seperator = menuMan.createSeparatorItem()
	-- Actions
	local exportItem = menuMan.createActionItem "OpenExportUI" "MaxBatchExporter"
	-- Add action to menuitem
	subMenu.addItem seperator -1
	subMenu.addItem exportItem -1
	
	-- Create submenu item which calls our new menu
	subMenuItem = menuMan.createSubMenuItem "Max Batch Exporter" subMenu
	mainMenuBar.addItem subMenuItem -1

	-- Redraw menu
	menuMan.updateMenuBar()
)

initMenuBar()