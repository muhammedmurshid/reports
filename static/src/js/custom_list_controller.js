/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { ListRenderer } from "@web/views/list/list_renderer";
import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";

    export class CustomListController extends ListController {
        setup() {
            super.setup();
            this.totalAmount = 100;
        }

        get rendererProps() {
            return {
                ...super.rendererProps,
                totalAmount: this.totalAmount,
            };
        }
    }

    export class CustomListRenderer extends ListRenderer {
        setup() {
            super.setup();
            this.totalAmount = this.props.totalAmount;
        }
    }

    registry.category("views").add("custom_list_view", {
        ...listView,
        Controller: CustomListController,
        Renderer: CustomListRenderer,

    });

