import { RequestModal } from "../modals/request.modal.js";
class RequestPage {
    requestId = null;
    constructor() {
        const dataElem = $("#request-data");
        this.requestId = dataElem.attr('data-request-id');
    }
    onInit() {
        $("#btn-edit-request").click(() => {
            const requestModal = new RequestModal(this.requestId, (data) => {
                location.reload();
            });
            requestModal.show(this.request);
        });
    }
}

export const Page = RequestPage;

$(document).ready(() => {
    new Page().onInit();
});