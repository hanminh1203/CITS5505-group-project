import { BaseModal } from "./base.modal.js";

export class ErrorModal extends BaseModal {
    constructor(message, stacktrace, onSaveCallback) {
        const query = { message, stacktrace };
        super(`/modals/error?${new URLSearchParams(query).toString()}`, null, 'error-modal', onSaveCallback);
    }

    addEventHandlers() {
        this.jqueryElement.find("#btn-ok").click(() => {
            this.close();
        });
    }
}