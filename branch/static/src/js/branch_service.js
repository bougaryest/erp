/** @odoo-module **/

import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { symmetricalDifference } from "@web/core/utils/arrays";
import { session } from "@web/session";


function parseBranchIds(bidsFromHash) {
    const bids = [];
    if (typeof bidsFromHash === "string") {
        bids.push(...bidsFromHash.split(",").map(Number));
    } else if (typeof bidsFromHash === "number") {
        bids.push(bidsFromHash);
    }
    return bids;
}

function computeAllowedBranchIds(bids) {
    const { user_branches } = session;
    let allowedBranchIds = bids || [];
    const availableBranchesFromSession = user_branches.allowed_branches;
    const notReallyAllowedBranches = allowedBranchIds.filter(
        (id) => !(id in availableBranchesFromSession)
    );

    if (!allowedBranchIds.length || notReallyAllowedBranches.length) {
        allowedBranchIds = [user_branches.current_branch];
    }
    return allowedBranchIds;
}

export const branchService = {
    dependencies: ["user", "router", "cookie"],
    start(env, { user, router, cookie }) {
        let bids;
        if ("bids" in router.current.hash) {
            bids = parseBranchIds(router.current.hash.bids);
        } else if ("bids" in cookie.current) {
            bids = parseBranchIds(cookie.current.bids);
        }
        let allowedBranchIds = computeAllowedBranchIds(bids);
        const stringBIds = allowedBranchIds.join(",");
        router.replaceState({ bids: stringBIds }, { lock: true });
        cookie.setCookie("bids", stringBIds);

        user.updateContext({ allowed_branch_ids: allowedBranchIds });
        const availableBranches = session.user_branches.allowed_branches;

        return {
            availableBranches,
            get allowedBranchIds() {
                return allowedBranchIds.slice();
            },
            get currentBranch() {
                return availableBranches[allowedBranchIds[0]];
            },
            setBranches(mode, ...branchIds) {
                // compute next branch ids
                let nextBranchIds;
                if (mode === "toggle") {
                    nextBranchIds = symmetricalDifference(allowedBranchIds, branchIds);
                } else if (mode === "loginto") {
                    const branchId = branchIds[0];
                    if (allowedBranchIds.length === 1) {
                        // 1 enabled branch: stay in single branch mode
                        nextBranchIds = [branchId];
                    } else {
                        // multi branch mode
                        nextBranchIds = [
                            branchId,
                            ...allowedBranchIds.filter((id) => id !== branchId),
                        ];
                    }
                }
                nextBranchIds = nextBranchIds.length ? nextBranchIds : [branchIds[0]];

                // apply them
                router.pushState({ bids: nextBranchIds }, { lock: true });
                cookie.setCookie("bids", nextBranchIds);
                browser.setTimeout(() => browser.location.reload()); // history.pushState is a little async
            },
        };
    },
};

registry.category("services").add("branch", branchService);