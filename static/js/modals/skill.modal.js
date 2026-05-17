import { BaseModal } from "./base.modal.js";
import { httpService } from "../services/http.service.js";
import { FormUtils } from "../utils/form.utils.js";

export class SkillModal extends BaseModal {
    formElem = null;
    // it is a post request to add a new skill or update a existing skill
    constructor(id, onSaveCallback) {
        super(`/modals/skill?skill_id=${id || ''}`, null, 'skill-modal', onSaveCallback);
        this.id = id;
    }

    // use this.onSubmit to handle the submit event
    addEventHandlers() {
        this.formElem = $(this.modalElement.querySelector('#skill-form'));
        this.formElem.on('submit', (e) => {
            e.preventDefault();
            this.onSubmit(e.target);
        });
        this.clearError();
    }

    // clear error messages and remove the error form
    clearError() {
        this.formElem.find('.form-error').text('');
        this.formElem.find('.form-control, .form-select').removeClass('is-invalid');
    }

    async onSubmit(form) {
        this.clearError();
        const { csrf_token, ...formData } = FormUtils.extractFormData(this.formElem);
        try {
            // if this.id is null, it is a post request to add a new skill, 
            // otherwise it is a put request to update a existing skill
            const url = this.id ? `/api/skills/${this.id}` : `/api/skills/`;
            // it will post to app/features/skills/api.py
            const result = await httpService.post(csrf_token, url, formData);
            this.close(result);
        } catch (e) {
            // check the error data from e.responseJSON?.data
            const data = e.responseJSON?.data;
            // check every key in the error data
            if (data) {
                for (const field of Object.keys(data)) {
                    const fieldInput = this.formElem.find(`#${field}`);
                    // add invalid class to the field
                    fieldInput.addClass('is-invalid');
                    // add error message to the field
                    this.formElem.find(`#${field}-feedback`).text(data[field]);
                }
            }
        }
    }
}
