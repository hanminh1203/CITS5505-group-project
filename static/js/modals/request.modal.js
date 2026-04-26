import { BaseModal } from "./base.modal.js";
import { httpService } from "../services/http.service.js";
import { FormUtils } from "../utils/form.utils.js";

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

    async onSubmit(form) {
        const { csrf_token, ...formData} = FormUtils.extractFormData(this.formElem);
        const result = await httpService.post(csrf_token, `/api/requests`, formData);
        this.close();
    }
}