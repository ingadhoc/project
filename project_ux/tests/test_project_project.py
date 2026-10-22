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
