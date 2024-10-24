.. |company| replace:: ADHOC SA

.. |company_logo| image:: https://raw.githubusercontent.com/ingadhoc/maintainer-tools/master/resources/adhoc-logo.png
   :alt: ADHOC SA
   :target: https://www.adhoc.com.ar

.. |icon| image:: https://raw.githubusercontent.com/ingadhoc/maintainer-tools/master/resources/adhoc-icon.png

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

==========
Project UX
==========


Several improvements to project:

#. Change default behavior when click on the project card in the kanban view, now will go to the project form view instead of the project task kanban view.
#. Add a boolean toggle button called "Don't send stage email" that gives the user the chance to avoid sending the email if the stage has an automatic template set. After the stage changes, this value returns to false if the stage has an email template.
#. Add a button "i" in the card kanban view that links directly to the proyect updates.
#. Adds:
   - 2 new filters: "Is Task"& "Is Sub-Task"
   - 1 new agroupation: "Parent-Task"
#. Re-incorporates the wizard that allows to select an existing task to be converted as a sub-task in the sub-task tab (in the migration to 17, when you press on "Add line" in the sub-task tab, you could only create new sub-tasks, not convert the existing tasks to sub-tasks)
#. Incorporates a tab inside the project form view called "Task stages" that allows to select (or create) the task stages that will apply to that project.
#. Incorporates an option inside the tasks stage configurations that allows to automatically set a state to the tasks when they are moved to these stages.
#. Re-incorporate the field is_closed in the tasks, under the label "Folded in kanban"

Installation
============

To install this module, you need to:

#. Just install the module.

Configuration
=============

To configure this module, you need to:

#. Nothing to configure

Usage
=====

#. Just Use the module.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: http://runbot.adhoc.com.ar/

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/ingadhoc/project/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* |company| |icon|

Contributors
------------

Maintainer
----------

|company_logo|

This module is maintained by the |company|.

To contribute to this module, please visit https://www.adhoc.com.ar.
