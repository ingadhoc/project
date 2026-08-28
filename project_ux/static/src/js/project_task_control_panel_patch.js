import { patch } from "@web/core/utils/patch";
import { ProjectTaskControlPanel } from "@project/views/project_task_control_panel/project_task_control_panel";
import { hasSubtaskLeaf } from "./subtask_domain";

patch(ProjectTaskControlPanel.prototype, {
    /**
     * The "Is Sub-Task" filter forces sub-tasks to be visible: the model drops
     * the `display_in_project` restriction while that filter is active (see
     * project_task_list_model_patch). While it is active the "Show Sub-Tasks"
     * toggle has no real effect.
     */
    get isSubtaskFilterActive() {
        return hasSubtaskLeaf(this.env.searchModel.domain);
    },

    /**
     * State the toggle is painted with: also selected when the filter forces
     * it, to avoid the confusing "off but showing sub-tasks" state.
     */
    get effectiveShowSubtasks() {
        return this.state.showSubtasks || this.isSubtaskFilterActive;
    },
});
