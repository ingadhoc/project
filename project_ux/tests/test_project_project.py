from lxml import etree
from odoo.tests.common import TransactionCase


class TestProjectProject(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Project = self.env["project.project"]

    def test_create_project_modal_button_opens_form(self):
        """The "Create project" button of the New modal must open the project
        form (via the standard get_record_default_action), not the task pipeline
        (action_view_tasks).
        """
        view = self.env.ref("project.project_project_view_form_simplified_footer")
        combined_arch = view.get_combined_arch()
        self.assertIn('name="get_record_default_action"', combined_arch)
        self.assertNotIn('name="action_view_tasks"', combined_arch)

    def test_get_record_default_action_lands_on_project_form(self):
        """get_record_default_action opens the created project's own form."""
        project = self.Project.create({"name": "New Project"})

        action = project.get_record_default_action()

        self.assertEqual(action["res_model"], "project.project")
        self.assertEqual(action["res_id"], project.id)
        self.assertEqual(action["target"], "current")
        self.assertTrue(any(view_type == "form" for __, view_type in action["views"]))

    def test_task_counter_is_a_link_to_the_tasks(self):
        """The card click opens the project form, so the task counter needs a
        link of its own: in 20.0 it is a plain div that only the card action
        opens.
        """
        arch = etree.fromstring(self.env.ref("project.view_project_card").get_combined_arch())

        links = arch.xpath("//a[@name='action_view_tasks'][@type='object'][.//field[@name='open_task_count']]")

        self.assertEqual(len(links), 1)

    def test_card_click_has_no_action_of_its_own(self):
        """Clicking anywhere else on the card opens the project form: the
        module drops the card-level action that 20.0 brings.
        """
        arch = etree.fromstring(self.env.ref("project.view_project_kanban").get_combined_arch())

        self.assertFalse(arch.get("action"))
