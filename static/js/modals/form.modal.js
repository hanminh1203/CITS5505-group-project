import { httpService } from "../services/http.service.js";
import { FormUtils } from "../utils/form.utils.js";
import { BaseModal } from "./base.modal.js";

export class FormModal extends BaseModal {
    constructor(htmlPath, cssPath, modalId, onCloseCallback, submitUrl) {
        super(htmlPath, cssPath, modalId, onCloseCallback);
        this.data = null;
        this.submitUrl = submitUrl;
    }

    clearError() {
        this.jqueryElement.find('.form-error').text('');
        this.jqueryElement.find('.form-control, .form-select').removeClass('is-invalid');
    }

    addEventHandlers() {
        this.formElement = this.modalElement.querySelector('form');
        if (this.formElement) {
            this.formElement.addEventListener('submit', (e) => {
                e.preventDefault();
                this.onSubmit();
            });
        }
    }

    async onSubmit() {
        this.clearError();
        const { csft_token, ...formData} = FormUtils.extractFormData(this.formElement);
        try {
            const result = await httpService.post(csrf_token, this.submitUrl, formData);
            this.close(result);
        } catch (e) {
            const {data} = e.responseJSON
            if (data) {
                for (const field of Object.keys(data)) {
                    const fieldInput = this.jqueryElement.find(`#${field}`);
                    fieldInput.addClass('is-invalid');
                    this.jqueryElement.find(`#${field}-feedback`).text(data[field]);
                }
            }
        }
    }
}