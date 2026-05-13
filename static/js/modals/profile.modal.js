import { BaseModal } from "./base.modal.js";
import { httpService } from "../services/http.service.js";
import { FormUtils } from "../utils/form.utils.js";
import { FormModal } from "./form.modal.js";

export class ProfileModal extends FormModal {
    formElem = null;
    constructor(onSaveCallback) {
        super('/modals/profile', null, 'profile-modal', onSaveCallback,
            '/api/users/me'
        );
    }

    doSubmitRequest(csrf_token, formData) {
        return httpService.put(csrf_token, this.submitUrl, formData);
    }
}
