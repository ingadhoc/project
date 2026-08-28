/**
 * Whether a search domain explicitly restricts results to sub-tasks, i.e. it
 * contains a `parent_id != False` leaf (as emitted by the "Is Sub-Task"
 * filter). Walks the domain in list form, including nested sub-domains.
 *
 * @param {Array} domain domain in list form
 * @returns {boolean}
 */
export function hasSubtaskLeaf(domain) {
    if (!Array.isArray(domain)) {
        return false;
    }
    for (const item of domain) {
        if (!Array.isArray(item)) {
            continue;
        }
        if (item.length === 3) {
            if (item[0] === "parent_id" && item[1] === "!=" && item[2] === false) {
                return true;
            }
        } else if (hasSubtaskLeaf(item)) {
            return true;
        }
    }
    return false;
}
