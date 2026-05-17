import { BaseModal } from "./base.modal.js";
import { httpService } from "../services/http.service.js";
import { FormUtils } from "../utils/form.utils.js";
import { FormModal } from "./form.modal.js";

export class ProfileModal extends FormModal {
    formElem = null;
    // when user click the edit button, this modal will be shown
    constructor(onSaveCallback) {
        super('/modals/profile', null, 'profile-modal', onSaveCallback,
            '/api/users/me'
        );
    }

    // when user click the submit button, this function will be called
    doSubmitRequest(csrf_token, formData) {
        // it is a put request so it need a csrf token
        // it will send to app/features/users/api.py
        return httpService.put(csrf_token, this.submitUrl, formData);
    }
}
