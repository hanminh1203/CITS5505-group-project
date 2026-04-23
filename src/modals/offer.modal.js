import { BaseModal } from "./base.modal.js";
import { service } from "../services/data.service.js";

export class OfferModal extends BaseModal {
    constructor(onSaveCallback) {
        super('src/modals/offer.modal.html', null, 'offer-modal', onSaveCallback);
        this.data = null;
    }
    
    addEventHandlers() {
        const form = this.modalElement.querySelector('#offer-form');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.#onSubmit(e.target);
        });
    }

    #onSubmit(form) {
        const data = $(form).serializeArray()
            .reduce((values, x) => {
                values[x.name] = x.value;
                return values;
            }, {});
        this.close(data);
    }

    prefillData(data) {
        this.data = data;
        this.request = data.request;
        service.fillDataValue(this.jqueryElement, {
            request: this.request
         });
    }
}