import { BaseModal } from "./base.modal.js";
import { httpService } from "../services/http.service.js";

export class RequestModal extends BaseModal {
    formElem = null;
    constructor(id, onSaveCallback) {
        super(`/requests/${id}/edit`, '/static/css/modals/request.modal.css', 'request-modal', onSaveCallback);
        this.id = id;
        this.data = null;
    }
    
    addEventHandlers() {
        this.formElem = this.modalElement.querySelector('#request-form');
        this.formElem.addEventListener('submit', (e) => {
            e.preventDefault();
            this.onSubmit(e.target);
        });
    }

    extractFormData() {
        return $(this.formElem).serializeArray()
            .reduce((values, x) => {
                values[x.name] = x.value;
                return values;
            }, {});
    }

    async onSubmit(form) {
        const { csrf_token, ...formData} = this.extractFormData();
        const result = await httpService.post(csrf_token, `/api/requests`, formData);
        this.close();
    }
}