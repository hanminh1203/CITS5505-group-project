import { httpService } from "../services/http.service.js";
import { FormUtils } from "../utils/form.utils.js";

class LoginPage {
    formElem = null;
    constructor() {
        this.formElem = $("#loginForm");
    }
    onInit() {
        this.formElem.submit((e) => {
            e.preventDefault();
            this.onSubmit();
        });
        this.clearError();
    }

    clearError() {
        this.formElem.find('#form-feedback').text('');
    }

    async onSubmit() {
        this.clearError();
        const {csrf_token, ...data} = FormUtils.extractFormData(this.formElem);
        try {
            const result = await httpService.post(csrf_token, '/api/login', data);
            window.location.href = "/dashboard";
        } catch {
            this.formElem.find('#form-feedback').text('Invalid email or password');
        }
    }
}

export const Page = LoginPage;

$(document).ready(() => {
    new Page().onInit();
});