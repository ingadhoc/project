from odoo.tests.common import TransactionCase

class TestTaskModel(TransactionCase):

    def setUp(self):
        super(TestTaskModel, self).setUp()
        self.Task = self.env['project.task']
        self.Stage = self.env['project.task.type']
        self.Template = self.env['mail.template']

        mail_template = self.Template.create({
            'name': 'Test Template',
            'email_from': 'test@example.com',
            'subject': 'Test Subject',
            'body_html': '<p>Test Body</p>'
        })

        self.test_stage = self.Stage.create({
            'name': 'Test Stage',
            'mail_template_id': mail_template.id
        })

        self.test_task = self.Task.create({
            'name': 'Test Task',
            'stage_id': self.test_stage.id,
            'state': '01_in_progress',
        })

    def test_compute_state_with_dependencies(self):
        """Test _compute_state method when dependencies are present"""
        dependent_task = self.Task.create({
            'name': 'Dependent Task',
            'stage_id': self.test_stage.id,
            'state': '01_in_progress'
        })
        self.test_task.write({'depend_on_ids': [(4, dependent_task.id)], 'allow_task_dependencies': True})
        self.test_task._compute_state()
        self.assertEqual(self.test_task.state, '04_waiting_normal')
        dependent_task.state = '1_done'
        self.test_task._compute_state()
        self.assertEqual(self.test_task.state, '01_in_progress')
