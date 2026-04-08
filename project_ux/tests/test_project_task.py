from odoo.tests.common import TransactionCase


class TestTaskModel(TransactionCase):
    def setUp(self):
        super(TestTaskModel, self).setUp()
        self.Project = self.env["project.project"]
        self.Task = self.env["project.task"]
        self.Stage = self.env["project.task.type"]
        self.Template = self.env["mail.template"]

        mail_template = self.Template.create(
            {
                "name": "Test Template",
                "email_from": "test@example.com",
                "subject": "Test Subject",
                "body_html": "<p>Test Body</p>",
            }
        )

        self.test_stage = self.Stage.create({"name": "Test Stage", "mail_template_id": mail_template.id})
        self.test_project = self.Project.create({"name": "Test Project"})

        self.test_task = self.Task.create(
            {
                "name": "Test Task",
                "project_id": self.test_project.id,
                "stage_id": self.test_stage.id,
                "state": "01_in_progress",
            }
        )

    def test_compute_state_with_dependencies(self):
        """Test _compute_state method when dependencies are present"""
        dependent_task = self.Task.create(
            {"name": "Dependent Task", "stage_id": self.test_stage.id, "state": "01_in_progress"}
        )
        self.test_task.write({"depend_on_ids": [(4, dependent_task.id)], "allow_task_dependencies": True})
        self.test_task._compute_state()
        self.assertEqual(self.test_task.state, "04_waiting_normal")
        dependent_task.state = "1_done"
        self.test_task._compute_state()
        self.assertEqual(self.test_task.state, "01_in_progress")

    def test_task_display_name_shows_id_when_enabled_on_project(self):
        self.assertEqual(self.test_task.display_name, "Test Task")

        self.test_project.show_task_id = True

        self.assertEqual(self.test_task.display_name, f"Test Task (#{self.test_task.id})")

    def test_task_display_name_hides_id_when_disabled_on_project(self):
        self.test_project.show_task_id = True
        self.assertEqual(self.test_task.display_name, f"Test Task (#{self.test_task.id})")

        self.test_project.show_task_id = False

        self.assertEqual(self.test_task.display_name, "Test Task")

    def test_name_search_finds_task_by_plain_id_when_enabled_on_project(self):
        self.test_project.show_task_id = True

        result = self.Task.name_search(str(self.test_task.id), limit=1)

        self.assertEqual(result, [(self.test_task.id, f"Test Task (#{self.test_task.id})")])

    def test_name_search_finds_task_by_hash_prefixed_id_when_enabled_on_project(self):
        self.test_project.show_task_id = True

        result = self.Task.name_search(f"#{self.test_task.id}", limit=1)

        self.assertEqual(result, [(self.test_task.id, f"Test Task (#{self.test_task.id})")])

    def test_name_search_finds_tasks_by_id_prefix_when_enabled_on_project(self):
        self.test_project.show_task_id = True

        tasks = self.test_task
        while tasks[-1].id < 10:
            tasks |= self.Task.create(
                {
                    "name": f"Test Task {len(tasks)}",
                    "project_id": self.test_project.id,
                    "stage_id": self.test_stage.id,
                    "state": "01_in_progress",
                }
            )

        prefix = str(tasks[-1].id)[:-1]
        result_ids = [task_id for task_id, __ in self.Task.name_search(prefix, limit=20)]

        self.assertIn(tasks[-1].id, result_ids)

    def test_name_search_does_not_find_task_by_id_when_disabled_on_project(self):
        result_ids = [task_id for task_id, __ in self.Task.name_search(str(self.test_task.id), limit=20)]

        self.assertNotIn(self.test_task.id, result_ids)
