import { BaseModal } from "./base.modal.js";
import { httpService } from "../services/http.service.js";
import { FormUtils } from "../utils/form.utils.js";

export class SkillModal extends BaseModal {
    formElem = null;
    constructor(id, onSaveCallback) {
        super(`/modals/skill?skill_id=${id || ''}`, null, 'skill-modal', onSaveCallback);
        this.id = id;
    }
    
    addEventHandlers() {
        this.formElem = $(this.modalElement.querySelector('#skill-form'));
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
            const url = this.id ? `/api/skills/${this.id}` : `/api/skills/`;
            const result = await httpService.post(csrf_token, url, formData);
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
