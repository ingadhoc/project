from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestProjectTaskType(TransactionCase):

    def setUp(self):
        super(TestProjectTaskType, self).setUp()
        self.ProjectTaskType = self.env['project.task.type']

    def test_state_change_constraint_error(self):
        """Test that UserError is raised when state_change is True and task_state is empty"""
        with self.assertRaises(UserError):
            self.ProjectTaskType.create({
                'name': 'Test Task Type',
                'state_change': True,
                'task_state': ''
            })
