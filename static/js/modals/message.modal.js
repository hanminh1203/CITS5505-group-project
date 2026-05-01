import { BaseModal } from "./base.modal.js";

export class MessageModal extends BaseModal {
    constructor(message, onSaveCallback) {
        super(`/modals/message?message=${encodeURIComponent(message)}`, null, 'message-modal', onSaveCallback);
    }

    addEventHandlers() {
        $("#btn-ok").click(() => {
            this.close();
        });
    }
}