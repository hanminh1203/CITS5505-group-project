import { BaseModal } from "./base.modal.js";

export class ConfirmationModal extends BaseModal {
    constructor(message, onSaveCallback) {
        super(`/modals/confirmation?message=${encodeURIComponent(message)}`, null, 'confirmation-modal', onSaveCallback);
    }

    addEventHandlers() {
        $("#btn-ok").click(() => {
            this.close(true);
        });
        $("#btn-cancel").click(() => {
            this.close(false);
        });
    }
}