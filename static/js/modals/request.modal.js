import { FormModal } from "./form.modal.js";

export class RequestModal extends FormModal {
    constructor(id, onSaveCallback) {
        super(`/requests/modal?request_id=${id || ''}`, null, 'request-modal', onSaveCallback,
            `/api/requests`
        );
    }
}