import { httpService } from "../services/http.service.js";
import { FormUtils } from "../utils/form.utils.js";
import { RequestModal } from "../modals/request.modal.js";

class DashBoardPage {
    createRequestButton = null;
    constructor() {
        this.createRequestButton = $("#btnCreateRequest");
    }
    onInit() {
        this.createRequestButton.click((e) => {
            const requestModal = new RequestModal(null, (data) => {
                this.navigateToRequestDetail(data.id);
            });
            requestModal.show();
        })
    }

    navigateToRequestDetail(id) {
        window.location.href = `/requests/${id}`;
    }

    async onSubmit() {
        const {csrf_token, ...data} = FormUtils.extractFormData(this.formElem);
        const result = await httpService.post(csrf_token, '/api/login', data);
        
        window.location.href = "/dashboard";
    }
}

export const Page = DashBoardPage;

$(document).ready(() => {
    new Page().onInit();
});