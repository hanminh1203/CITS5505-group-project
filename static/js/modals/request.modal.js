import { BaseModal } from "./base.modal.js";
import { httpService } from "../services/http.service.js";
import { FormUtils } from "../utils/form.utils.js";

export class RequestModal extends BaseModal {
    formElem = null;
    hasError = false;
    constructor(id, onSaveCallback) {
        super(`/requests/modal?request_id=${id || ''}`, null, 'request-modal', onSaveCallback);
        this.isNew = !!id;
        this.id = id;
    }
    
    addEventHandlers() {
        this.formElem = $(this.modalElement.querySelector('#request-form'));
        this.formElem.on('submit', (e) => {
            e.preventDefault();
            this.onSubmit(e.target);
        });
        this.clearError();
    }

    clearError() {
        this.formElem.find('.form-error').text('');
        this.formElem.find('.form-control, .form-select').removeClass('is-invalid');
    }

    async onSubmit(form) {
        this.clearError();
        const { csrf_token, ...formData} = FormUtils.extractFormData(this.formElem);
        try {
            const result = await httpService.post(csrf_token, `/api/requests`, formData);
            this.close(result);
        } catch (e) {
            const data = e.responseJSON?.data;
            if (data) {
                for (const field of Object.keys(data)) {
                    const fieldInput = this.formElem.find(`#${field}`);
                    fieldInput.addClass('is-invalid');
                    this.formElem.find(`#${field}-feedback`).text(data[field]);
                }
            }
        }
    }
}
