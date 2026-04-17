import { RequestModal } from "../modals/request.modal.js";
class RequestPage {
    onInit() {
        $("#btn-edit-request").click(() => {
            const requestModal = new RequestModal((data) => {
                console.log(data);
            });
            requestModal.show(this.request);
        });
    }
}

export const Page = RequestPage;

$(document).ready(() => {
    new Page().onInit();
});