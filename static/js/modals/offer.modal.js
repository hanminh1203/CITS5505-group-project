import { FormModal } from "./form.modal.js";

export class OfferModal extends FormModal {
    constructor(requestId, onSaveCallback) {
        super(`/requests/${requestId}/offer`, null, 'offer-modal', onSaveCallback,
            `/api/requests/${requestId}/offer`
        );
    }
}