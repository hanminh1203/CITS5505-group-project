import { RequestModal } from "../modals/request.modal.js";
import { OfferModal } from "../modals/offer.modal.js";
class RequestPage {
    requestId = null;
    constructor() {
        const dataElem = $("#request-data");
        this.requestId = dataElem.attr('data-request-id');
    }
    onInit() {
        $("#btn-edit-request").click(() => {
            const requestModal = new RequestModal(this.requestId, (data) => this.reloadPage());
            requestModal.show();
        });
        $(".btn-offer").click(() => {
            const offerModal = new OfferModal(this.requestId, (data) => this.reloadPage());
            offerModal.show(this.request);
        });
    }

    reloadPage() {
        location.reload();
    }
}

export const Page = RequestPage;

$(document).ready(() => {
    new Page().onInit();
});