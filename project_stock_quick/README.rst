.. |company| replace:: ADHOC SA

.. |company_logo| image:: https://raw.githubusercontent.com/ingadhoc/maintainer-tools/master/resources/adhoc-logo.png
   :alt: ADHOC SA
   :target: https://www.adhoc.com.ar

.. |icon| image:: https://raw.githubusercontent.com/ingadhoc/maintainer-tools/master/resources/adhoc-icon.png

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

===================
Project Stock Quick
===================

Create stock pickings from a project task and keep them linked to that task.

The native ``project_stock`` module already links pickings to the **project**,
but not to the **task**. This module adds that missing link:

#. New boolean **Transfer management** on the project (Settings tab, Inventory
   group), only visible to inventory users.
#. When enabled, two optional settings show up:

   - **Default operation type**: pickings created from the tasks start with
     that operation type. If empty, the user picks it.
   - **Stages that allow transfers**: if set, the create button only shows up
     when the task is in one of those stages. If empty, any stage allows it.
#. New **New transfer** header button on the task, which opens a picking form
   with the task's partner, project, company and the task name as source
   document already set.
#. New **Transfers** stat button on the task, with the count of pickings
   originated on it.
#. New **Task** field on the picking form, next to the project that
   ``project_stock`` provides. Setting it by hand aligns project and partner.

Technical notes:

- ``stock.picking.task_id`` is a plain many2one (indexed, with
  ``check_company``), not a stored related or compute, to avoid mass
  recomputations on a high volume transactional model. Project and partner are
  propagated through the action defaults and an onchange.
- The create button is resolved by
  ``project.task.display_create_picking_button`` and
  ``action_create_stock_picking`` validates the same conditions server side:
  hiding a button is not a control.

Installation
============

To install this module, you need to:

#. Just install the module. ``project_stock`` is a native module, auto
   installed with ``project`` and ``stock``.

Configuration
=============

To configure this module, you need to:

#. Go to the project, Settings tab, Inventory group, and enable
   **Transfer management**.
#. Optionally set **Default operation type** and **Stages that allow
   transfers**.

Usage
=====

To use this module, you need to:

#. Open a task of that project and press **New transfer**.
#. Complete the products and save: the picking stays linked to the task.
#. Back on the task, the **Transfers** stat button shows the linked pickings.
#. To link an existing picking, open it and set the **Task** field.

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
