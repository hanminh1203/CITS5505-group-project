import { BaseModal } from "./base.modal.js";
import { httpService } from "../services/http.service.js";
import { FormUtils } from "../utils/form.utils.js";

export class ProfileModal extends BaseModal {
    formElem = null;
    constructor(onSaveCallback) {
        super('/modals/profile', null, 'profile-modal', onSaveCallback);
    }
    
    addEventHandlers() {
        this.formElem = $(this.modalElement.querySelector('#profile-form'));
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
            const result = await httpService.put(csrf_token, '/api/users/me', formData);
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
