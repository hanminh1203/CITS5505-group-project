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
        })
    }

    async onSubmit() {
        const {csrf_token, ...data} = FormUtils.extractFormData(this.formElem);
        const result = await httpService.post(csrf_token, '/login', data);
        
        window.location.href = "/dashboard";
    }
}

export const Page = LoginPage;

$(document).ready(() => {
    new Page().onInit();
});