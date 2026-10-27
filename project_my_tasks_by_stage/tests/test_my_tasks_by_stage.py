from odoo.tests.common import TransactionCase
from odoo.tools.safe_eval import safe_eval


class TestMyTasksByStage(TransactionCase):
    def setUp(self):
        super().setUp()
        self.action = self.env.ref("project.action_view_my_task")
        self.context = safe_eval(self.action.context, {"uid": self.env.uid})

    def test_my_tasks_are_grouped_by_project_stage(self):
        """My Tasks must group by the project task stage, not the personal one."""
        self.assertEqual(self.context["group_by"], "stage_id")

    def test_my_tasks_keeps_open_filter_and_default_assignee(self):
        self.assertEqual(self.context["search_default_open_tasks"], 1)
        self.assertEqual(self.context["default_user_ids"], [(4, self.env.uid)])

    def test_grouping_by_stage_is_valid_on_tasks(self):
        """The grouping of the action must be accepted by the task model."""
        stage = self.env["project.task.type"].create({"name": "Stage"})
        project = self.env["project.project"].create({"name": "Project", "type_ids": [(6, 0, stage.ids)]})
        self.env["project.task"].create(
            {
                "name": "Task",
                "project_id": project.id,
                "stage_id": stage.id,
                "user_ids": [(4, self.env.uid)],
            }
        )
        groups = self.env["project.task"]._read_group(
            [("user_ids", "in", self.env.uid)],
            groupby=[self.context["group_by"]],
            aggregates=["__count"],
        )
        self.assertIn(stage, [group[0] for group in groups])
