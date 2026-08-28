import { patch } from "@web/core/utils/patch";
import { Domain } from "@web/core/domain";
import { ProjectTaskRelationalModel } from "@project/views/project_task_relational_model";
import { hasSubtaskLeaf } from "./subtask_domain";

patch(ProjectTaskRelationalModel.prototype, {
    /**
     * When the user filters explicitly by sub-tasks ("Is Sub-Task" filter),
     * the core still hides them while the "Show Sub-Tasks" mode is off: it
     * injects `display_in_project = True`, which is False for any sub-task
     * sharing its parent's project. The result is an empty list with no hint,
     * so the sub-task looks like it does not exist.
     *
     * If the sub-task filter is active, drop that leaf to honor the filter and
     * show the sub-tasks without requiring the user to toggle the display mode
     * by hand.
     */
    _processSearchDomain(domain) {
        const processed = super._processSearchDomain(domain);
        if (hasSubtaskLeaf(domain)) {
            return Domain.removeDomainLeaves(processed, ["display_in_project"]).toList({});
        }
        return processed;
    },
});
