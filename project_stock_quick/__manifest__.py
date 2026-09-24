{
    "name": "Project Stock Quick",
    "version": "19.0.1.0.0",
    "category": "Services/Project",
    "author": "ADHOC SA",
    "website": "www.adhoc.com.ar",
    "license": "AGPL-3",
    "summary": "Create stock pickings from a project task and keep them linked to that task",
    "depends": [
        # brings stock.picking.project_id, the base for our task_id
        "project_stock",
    ],
    "data": [
        "views/project_project_views.xml",
        "views/project_task_views.xml",
        "views/stock_picking_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
