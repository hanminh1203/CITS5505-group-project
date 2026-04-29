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
            const requestModal = new RequestModal(this.requestId, (data) => {
                location.reload();
            });
            requestModal.show();
        });
        $(".btn-offer").click(() => {
            const offerModal = new OfferModal((data) => this.onMakeOffer(data));
            offerModal.show(this.request);
        });
    }

    onMakeOffer(data) {
        location.reload();
    }
}

export const Page = RequestPage;

$(document).ready(() => {
    new Page().onInit();
});