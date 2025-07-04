/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { ListRenderer } from "@web/views/list/list_renderer";
import { listView } from "@web/views/list/list_view";
import { registry } from "@web/core/registry";

export class CustomTaxableListController extends ListController {
    setup() {
        super.setup();

        const rows = this.model.root.records;
        const total = rows.reduce((acc, record) => {
            const value = parseFloat(record.data.taxable_amount || 0);
            return acc + (isNaN(value) ? 0 : value);
        }, 0);

        this.totalTaxableAmount = total;
    }

    get rendererProps() {
        return {
            ...super.rendererProps,
            totalTaxableAmount: this.totalTaxableAmount.toFixed(2),
        };
    }
}

export class CustomTaxableListRenderer extends ListRenderer {
    setup() {
        super.setup();
    }
}

registry.category("views").add("custom_taxable_list", {
    ...listView,
    Controller: CustomTaxableListController,
    Renderer: CustomTaxableListRenderer,
});
